#!/usr/bin/env python3

import json, re, nltk
from collections import defaultdict
from nltk import word_tokenize
from nltk.corpus import cmudict # need to have downloaded the data through NLTK

""" Sample part of the output (hand-formatted):

{"lineId": "3-2", "lineNum": 2,
 "text": "Make my coat look new, dear, sew it!",
 "tokens": ["Make", "my", "coat", "look", "new", ",", "dear", ",", "sew", "it", "!"],
 "rhymeWords": ["sew", "it"],
 "rhymeProns": [["S OW1"], ["IH1 T", "IH0 T"]]
},
"""

# Load the cmudict entries into a data structure.
# Store each pronunciation as a STRING of phonemes (separated by spaces).
...

# Load chaos.json
...

# For each line of the poem, add a "rhymeProns" entry
# which is a list parallel with "rhymeWords".
# For each word, it contains a list of possible pronunciations.
...

# Write the enhanced data to chaos.pron.json
...

"""
TODO: Answer the question:

- How many rhyme words are NOT found in cmudict (they are "out-of-vocabulary", or "OOV")?
Give some examples.

Answer: 34 words were not found in cmudict, such as phlegm, gaol, gunwhale, and islington

...
"""

prons = cmudict.dict()
#print(prons)

#OOVcount = 0

with open('chaos.json', 'rb') as chaos:
    data = json.load(chaos)
    #print(data)
chaos.closed
for stanza in data:
    stanzaNum=stanza['stanza']
    for line in stanza['lines']:
        rhymeWords = line['rhymeWords']
        #print(rhymeWords)
        rhymeProns = []
        for word in rhymeWords:
            word = str.lower(word)
            if(word in prons):
                rhymeProns.append(prons[word].copy())
#            else:
#                print(word)
#                OOVcount=OOVcount+1
        if(len(rhymeProns)>0):
            line['rhymeProns']=rhymeProns.copy()
print(json.dumps(data, indent=4))
#print(OOVcount)

with open('chaos.json', 'w') as jf:
    json.dump(data, jf, indent=4)
jf.closed