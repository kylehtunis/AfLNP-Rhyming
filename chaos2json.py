#!/usr/bin/env python3

"""
Converts chaos.html into JSON. A sample of the input:

<xxx1><p>Dearest <i>creature</i> in <i>creation</i><br>
<xxx2>Studying English <i>pronunciation</i>,<br>
<xxx3><tt>&nbsp;&nbsp;&nbsp;</tt>I will teach you in my <i>verse</i><br>
<xxx4><tt>&nbsp;&nbsp;&nbsp;</tt>Sounds like <i>corpse</i>, <i>corps</i>, <i>horse</i> and <i>worse</i>.</p>

A hand-formatted portion of the output (note that indentation, line breaks,
order of dict entries, etc. don't matter as long as the data matches):

[
    ...
    {"stanza": 3,
     "lines": [
          {"lineId": "3-1", "lineNum": 1, "text": "Pray, console your loving poet,",
           "tokens": ["Pray", ",", "console", "your", "loving", "poet"],
           "rhymeWords": ["poet"]},
          {"lineId": "3-2", "lineNum": 2, "text": "Make my coat look new, dear, sew it!",
           "tokens": ["Make", "my", "coat", "look", "new", ",", "dear", ",", "sew", "it", "!"],
           "rhymeWords": ["sew", "it"]},
          ...
     ]},
    ...
    {"stanza": 9,
     "lines": [
          {"lineId": "9-1", "lineNum": 1, "text": "From \"desire\": desirable - admirable from \"admire\",",
           "tokens": ["From", "``", "desire", "''", ":", "desirable", "-", "admirable", "from", "``", "admire", "''", ","],
           "rhymeWords": ["admire"]},
          ...
     ]},
     ...
]
"""

import json, re
from nltk import word_tokenize

def hasalpha(token):
    return re.search('[a-zA-Z]', token)!=None

# regex that breaks an HTML line into parts: line number within the stanza, main portion, spacing
#LINE_RE = re.compile('<xxx([0-9])>(?:<tt>)?(?:\&nbsp;)*(?:</tt>)?(.*)') 
LINE_RE = re.compile(r'(?:&nbsp;)*(.*?)<.*?>')
RHYME_WORDS_RE = re.compile(r'<i>(\w*?)</i>')
LINE_NUM_RE = re.compile(r'<xxx([0-9])+>')
#print(RHYME_WORDS_RE.findall("<xxx2>Make your <i>head</i> with <i>heat</i> grow dizzy;<br>"))
#print(LINE_RE.findall("<xxx1><p><i>Pray</i>, console your loving <i>poet</i>,<br>"))
#print(LINE_NUM_RE.findall("<xxx3><tt>&nbsp;&nbsp;&nbsp;</tt><i>Tear</i> in eye, your dress you'll <i>tear</i>;<br>"))

# TODO: read from chaos.html, construct data structure, write to chaos.json

data = []
i=0
stanza = {'stanza':1}
lines=[]
linecount=0
with open('chaos.html', 'r') as chaos:
    line=chaos.readline()
    while(line!=''):
        #print(line)
        linenum=LINE_NUM_RE.findall(line)
        if linenum:
            linecount+=1
            linenum=linenum[0]
            if(linenum=='1'):
                stanza['lines']=lines
                #print(stanza)
                data.append(stanza.copy())
                stanza={'stanza':i}
                lines=[]
                i=i+1
            lineid=str(i)+'-'+str(linenum)
            words=''.join(LINE_RE.findall(line))
            rhymewords=str.split(' '.join(RHYME_WORDS_RE.findall(line)))
            tokens=word_tokenize(words)
            linedata = {}
            linedata['lineId'] = lineid
            linedata['lineNum'] = linenum
            linedata['text']=words
            linedata['tokens'] = tokens
            linedata['rhymeWords']=rhymewords
            lines.append(linedata.copy())
        line=chaos.readline()
chaos.closed
with open('chaos.json', 'w') as jf:
    json.dump(data, jf, indent=4)
jf.closed
print(linecount)