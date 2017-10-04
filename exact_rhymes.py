#!/usr/bin/env python3

import json, re
from collections import defaultdict
from nltk.corpus import cmudict # need to have downloaded the data through NLTK

def isExactRhyme(p1, p2):
    """
    TODO: Explain your heuristic here.

    """
    return # TODO: whether pronunciations p1 and p2 rhyme

# Load chaos.pron.json
...

# For each pair of lines that are supposed to rhyme,
# check whether there are any pronunciations of the words that
# make them rhyme according to cmudict and your heuristic.
# Print the rhyme words with their pronunciations and whether
# they are deemed to rhyme or not
# so you can examine the effects of your rhyme detector.
# Count how many pairs are deemed to rhyme vs. not.
...

"""
TODO: Answer the questions briefly:

- How many pairs of lines that are supposed to rhyme actually have rhyming pronunciations
according to your heuristic and cmudict?

Answer: 52

...

- For how many lines does having the rhyming line help you disambiguate
between multiple possible pronunciations?

Answer: 35

...

- What are some reasons that lines supposed to rhyme do not,
according to your rhyme detector? Give examples.

Answer: Most non-rhymes are because the stanzas are in the form AABB, 
    so lines 2 and 3 of a stanza would not rhyme, nor would the first line of a stanza
    rhyme with the last line of the stanza before it

...

"""

def hasalpha(token):
    return re.search('[a-zA-Z]', token)!=None

with open('chaos.json', 'rb') as chaos:
    data = json.load(chaos)
    #print(data)
chaos.closed

rhymeCount=0
notRhymeCount=0
multipleProns=0
prevRhyme=''
prevRhymeWord=''
for stanza in data:
    stanzaNum=stanza['stanza']
    for line in stanza['lines']:
        if('rhymeProns' in line): 
            if(prevRhyme):
                rhyme = ''
                for word in reversed(line['tokens']):
                    if (hasalpha(word)):
                        if(word in line['rhymeWords']):
                            rhyme = word
                        break
                if(rhyme):
                    rhymeNotFound=True
                    for pron in line['rhymeProns'][-1]:
                        for prev in prevRhyme:
                            if(pron[-2:]==prev[-2:]):
                                rhymeNotFound=False
                                if(len(line['rhymeProns'][-1])>1 or len(prevRhyme)>1):
                                    multipleProns+=1
                    if(rhymeNotFound):
                        #print(prevRhymeWord)
                        #print(rhyme)
                        #print('\n')
                        notRhymeCount+=1
                    else:
                        rhymeCount+=1
            for word in reversed(line['tokens']):
                if (hasalpha(word)):
                    if(word in line['rhymeWords']):
                        prevRhyme = line['rhymeProns'][-1]
                        prevRhymeWord=word
                    else:
                        prevRhyme=''
                        prevRhymeWord=''
                    break
        else:
            prevRhyme=''
                    
print(rhymeCount)
print(notRhymeCount)
print(multipleProns)