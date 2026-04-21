# HeteroLogos

HeteroLogos is a writing tool built specifically to aid in writing heterologous sentences.

## Definition of heterologos

Heterologos is an extension of the idea of the historical linguistic [rebracketing](https://en.wikipedia.org/wiki/Rebracketing'). which is a process where a word originally derived from one set of morphemes is broken down or bracketed into a different set
A heterologous phrase is a series of syllables which can be 'rebracketed' in two different ways into two distinct sentences of normal words. An example of a heterologous phrase would be: war terminates <=> water minutes.
We define strong heterologos to be where the syllables are exactly the same in both rebracketing apart from stress whereas a weak heterologos allows for some deviation in syllables such as: win terrible <=> winter bible.
In addition we also define simple heterologos to be when we use identical words (or segments of compound words) to ensure heterology such as: **war** pharaohs <=> **war**fare arose. Complex heterologos does not rely on using the same words such as the first two examples. Simple heterologos is likely to occur especially when using short necessary words such as articles or common verbs but complex heterologos is usually more desirable for aesthetic reasons because it is harder to achieve manually.


## The tool

The tools aims to aid but not solve the challenge of writing heterologically with three steps 

- IPA lookup
- LLM scoring
- Syntax analysis

The user will be shown two sections, one above the other. When they start typing, the section which is shorter will automatically suggest words that are heterologos to the overlapping longer section. We call this section between the ends of the two sections the 'overhang'. Its suggestion should be as strong and complex as possible but should weaken the constraints as fewer words fit the criteria. The user should still be able to edit the settings manually as well. The suggestions should also try to follow general linguistic syntax rules such as subject verb object ordering, and adjective noun ordering.

### IPA lookup

The tool will attempt to find the phonemes of every word inputted by querying a [local copy](https://raw.githubusercontent.com/cmusphinx/cmudict/refs/heads/master/cmudict.dict) of the [CMUdict](http://www.speech.cs.cmu.edu/cgi-bin/cmudict). If no result is found one will be attempted to be generated using [phonemizer](https://bootphon.github.io/phonemizer/), converted into the same symbols as CMUdict, then added to an additional file which will be used in conjunction with the CMUdict.

### LLM prediction

In order to refine the suggestions made, an open-weight (maybe local) LLM can be used to score each suggestion made by the brute force lookup.

### Syntax analysis

This section may be made redundant by the implicit check performed by the LLM but it could be useful. However it would require categorising each word in the dictionary and potentially manually inputting syntax rules which would be time consuming.


