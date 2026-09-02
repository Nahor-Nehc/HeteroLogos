# HeteroLogos

HeteroLogos is a writing tool built specifically to aid in writing heterologous sentences.

## Definition of heterologos

Clarification: Hetero***logos*** is a noun, while hetero***logous*** is an adjective.

Heterologos is an extension of the idea of the historical linguistic [rebracketing](https://en.wikipedia.org/wiki/Rebracketing'), which is a process where a word originally derived from one set of morphemes is broken down or bracketed into a different set.

A heterologous phrase is a series of syllables which can be 'rebracketed' in two different ways into two distinct sentences of normal words. An example of a heterologous phrase would be: war terminates <=> water minutes.

We define strong heterologos to be where the syllables are exactly the same in both rebracketing apart from maybe stress, whereas a weak heterologos allows for some deviation in syllables such as: win terrible <=> winter bible.

In addition we also define simple heterologos to be when we use identical words (or segments of compound words) to ensure heterology such as: **war** pharaohs <=> **war**fare arose. Complex heterologos does not rely on using the same words such as the first two examples. Simple heterologos is likely to occur especially when using short necessary words such as articles or common verbs but complex heterologos is usually more desirable for aesthetic reasons because it is harder to achieve manually.


## Overview

The tools aims to aid but not solve the challenge of writing heterologically with three steps:
- IPA lookup
- LLM scoring
- Syntax analysis

The user will be shown two sections, one above the other. When they start typing, the section which is shorter will automatically suggest words that are heterologos to the overlapping longer section. We call this section between the ends of the two sections the 'overhang'.

The suggestions should be as strong and complex as possible but should weaken the constraints as fewer words fit the criteria. The user should still be able to edit the strength and complexity manually as well. The suggestions should also try to follow general linguistic syntax rules such as subject-verb-object ordering, and adjective-noun ordering.

### IPA lookup

The tool will attempt to find the [ARPABET](https://en.wikipedia.org/wiki/ARPABET) phonemes of every word inputted by querying a [local copy](https://raw.githubusercontent.com/cmusphinx/cmudict/refs/heads/master/cmudict.dict) of the [CMUdict](http://www.speech.cs.cmu.edu/cgi-bin/cmudict). If no result is found one will be attempted to be generated using [phonemizer](https://bootphon.github.io/phonemizer/), converted into the same symbols as CMUdict, then added to an additional file which will be used in conjunction with the CMUdict.

The second step is to search for all words which could populate the overhang. This step will be the most complex and computationally intense step (unless using local LLM). We could naively look at every possible word break location in the overhang, but since our main goal is simply predicting the next word, we can just look for the next word, trying to fit as much of the overhang as possible. This approach would populate results faster but comes at the disadvantage of not being able to pass phrases that could fit the overhang to the LLM scoring system. Instead we could procedurally populate the suggestion:
- Find all next possible single words (fast-ish as only n comparisons needed)
- (reorder suggestions with LLM scoring here?)
- For each possible word, recursively check for next possible word of the new overhang
- (store a tuple in a dictionary (word length, word location in overhang, word) which reduces repeat checks)


### LLM prediction

In order to refine the suggestions made, an open-weight (maybe local) LLM can be used to score each suggestion made by the brute force IPA lookup.

### Syntax analysis

This section may be made redundant by the implicit check performed by the LLM but it could be useful. However it would require categorising each word in the dictionary and potentially manually inputting syntax rules which would be time consuming.

## Design

### IPA lookup

(Need)
We want to find the phonemes of every word.
Decide whether we want to search the dictionary every time a character is entered or to wait until the end of the word has been typed.
If the word is not recognised by the CMUdict then we need to use phonemizer to guess the pronounciation.
We need a way for the user to correct the pronounciation though in case it is incorrect.
The phonemizer should not be used unless the word is finished.

(Want)
We need to consider if the word has multiple possible pronounciations. If it does, we need to be able to hold both pronounciations in memory, and when looking up the possible next word calculate the branches on both trees. Alternatively if this is too time intensive we could ask the user which pronounciation they want to use.

(Cosmetic)
We will try and link the two sequences of phonemes together using tags such as \[i\]gnore, \[o\]verhang, and \[f\]orce match.
During linking, we will just go through the phonemes one at a time and link them together. If a phoneme is marked ignore, we skip it entirely. If it is marked force match, we force them to link. We can then calculate the entire distance for the linked phonemes between each force match, and then possibly remove/add ignore tags to minimise the distance.

#### Trie

In order to efficiently look up matches to an overhang, a Trie structure will be used. It results in a search time complexity of $O(n)$ and is faster than hashing as there is no need to compute a hash. (?verify?)

##### Nodes

(Need)
Each node will contain a Phoneme (containing the string and the stress) and a list of all words which terminate at that phoneme. We do not want to create separate child nodes for each stress because it makes it easier to calculate strength of a suggestion (see later).

We delegate finding the distance to the Phoneme.

##### Phoneme

(Need)
Contains the ARPABET string representation and the stress given by CMUdict
0 - unstressed
1 - primary stress
2 - secondary stress

The difference in stress is not too important but can improve the strength of the heterology. The difference between stressed and unstressed to primary and secondary stress is larger (and prioritised).

It contains the method used for finding the distance between two phonemes.
Naive method: we will use the SPE feature vectors and calculate a simple Hamming distance between the features of the feature vectors. We will use a PhonemeDistanceMatrix to hold the pre-calculated values for the phonemes' distance.

Complex method:
- use SPE feature vector as baseline
- compute weights for each feature from confusion matricies in research (consonants)
- validate for vowels


##### Search

(Need)
The inputs are the trie and the list of phonemes to match.
Once the end of the overhang is hit by the search, we can just output every word left in the subtree.

We start (!!!)