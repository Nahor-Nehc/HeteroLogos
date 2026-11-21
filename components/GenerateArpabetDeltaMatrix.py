"""
Created by Claude 19/11/2026
Modified by Rohan 19/11/2026

Build an ARPABET x ARPABET distance matrix from nltk.metrics.aline.delta.

Usage: python3 -I arpabet_delta_matrix.py [path/to/aline.py] [out.csv]
(With no path it imports nltk.metrics.aline.)

Design notes
------------
* delta() only compares single feature bundles, so every ARPABET phoneme is a
  tuple of one or two ALINE segments.
* Affricates CH/JH become ONE new segment each (ALINE already defines an unused
  'affricate' manner), so they stay single units.
* Diphthongs are a (nucleus, off-glide) pair of VOWEL segments (not j/w, which
  are consonants and would be far from any vowel under delta).
* As shipped, ALINE gives every vowel manner 'vowel2' and drops 'high' from R_v,
  so vowel height never affects delta (delta('i','a') == 0). We restore height
  by coding vowel manner as high/mid/low vowel (keys already in similarity_matrix).
* ALINE has no lax vowels or r-coloured vowels, so we add 'ɪ' (near-high),
  make 'ʊ' near-high, and build 'ɚ' as 'ɜ' + retroflex.
"""

import csv
import itertools
from nltk.metrics import aline

fm, sim = aline.feature_matrix, aline.similarity_matrix

# ---- 1. restore vowel height via 'manner' -----------------------------------
HEIGHT_TO_MANNER = {"high": "high vowel", "mid": "mid vowel", "low": "low vowel"}
sim["near-high vowel"] = 0.3  # between 'high vowel' (0.4) and 'mid vowel' (0.2)
for v in aline.vowels:
    fm[v] = dict(fm[v], manner=HEIGHT_TO_MANNER[fm[v]["high"]])

# ---- 2. add the segments ARPABET needs but ALINE lacks ----------------------
fm["ɪ"] = dict(fm["i"], manner="near-high vowel")
fm["ʊ"] = dict(fm["ʊ"], manner="near-high vowel")
fm["ɚ"] = dict(fm["ɜ"], retroflex="plus")                       # ER
fm["ʧ"] = dict(fm["ʃ"], manner="affricate")                     # CH
fm["ʤ"] = dict(fm["ʒ"], manner="affricate")                     # JH
aline.vowels += ["ɪ", "ɚ"]
aline.consonants += ["ʧ", "ʤ"]  # V() and R() test membership in this list

# ---- 3. ARPABET -> tuple of ALINE segments ----------------------------------
ARPA = {
    "P": ("p",), "B": ("b",), "T": ("t",), "D": ("d",), "K": ("k",), "G": ("g",),
    "CH": ("ʧ",), "JH": ("ʤ",),
    "F": ("f",), "V": ("v",), "TH": ("θ",), "DH": ("ð",), "S": ("s",), "Z": ("z",),
    "SH": ("ʃ",), "ZH": ("ʒ",), "HH": ("h",),
    "M": ("m",), "N": ("n",), "NG": ("ŋ",),
    "L": ("l",), "R": ("ɹ",), "W": ("w",), "Y": ("j",),
    "IY": ("i",), "IH": ("ɪ",), "EH": ("ɛ",), "AE": ("æ",), "AA": ("ɑ",),
    "AO": ("ɔ",), "UH": ("ʊ",), "UW": ("u",), "AH": ("ʌ",), "AX": ("ə",), "ER": ("ɚ",),
    "EY": ("e", "ɪ"), "AY": ("a", "ɪ"), "OY": ("ɔ", "ɪ"),
    "AW": ("a", "ʊ"), "OW": ("o", "ʊ"),
}
for segs in ARPA.values():
    for s in segs:
        assert s in fm, s

ONSET_WEIGHT = 0.7  # weight of first component in diphthong comparisons - prioritise onset vowel sound

def dist(P, Q, w=ONSET_WEIGHT):
    if len(P) == 1 and len(Q) == 1:
        return float(aline.delta(P[0], Q[0]))
    if len(P) == 2 and len(Q) == 2:
        return w * aline.delta(P[0], Q[0]) + (1 - w) * aline.delta(P[1], Q[1])
    if len(P) == 2:  # make P the single segment
        P, Q = Q, P
    return w * aline.delta(P[0], Q[0]) + (1 - w) * aline.delta(P[0], Q[1])


names = list(ARPA)
M = {(a, b): dist(ARPA[a], ARPA[b]) for a in names for b in names}

if __name__ == "__main__":
    out = "arpabet_delta_matrix.csv"
    with open(out, "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow([""] + names)
        for a in names:
            wr.writerow([a] + [f"{M[a, b]:.2f}" for b in names])
    print("wrote", out)

    # sanity checks
    asym = [(a, b) for a, b in itertools.combinations(names, 2) if abs(M[a, b] - M[b, a]) > 1e-9]
    zero = [(a, b) for a, b in itertools.combinations(names, 2) if M[a, b] == 0]
    print("asymmetric pairs:", asym)
    print("distinct phonemes at distance 0:", zero)
    for p in ["T", "CH", "IY", "IH", "EY", "AY", "ER", "AH", "S", "N"]:
        nn = sorted((M[p, q], q) for q in names if q != p)[:4]
        print(f"{p:>2} nearest:", ", ".join(f"{q} {d:.1f}" for d, q in nn))
