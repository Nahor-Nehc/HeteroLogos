import pickle
import os
import time

from components.Phoneme import Phoneme
from components.PhonemeDistanceMatrix import PhonemeDistanceMatrix
from components.Trie import PhonemeTrie, TrieNode, create_trie

create_trie()

print("hi")

with open(os.path.join("data", "cmudict_trie.pkl"), "rb") as file:
    loaded_data:PhonemeTrie = pickle.load(file)
    print(loaded_data.dpw_threshold)
    

print(type(loaded_data))
print(loaded_data)
# print(loaded_data.get_all_words())
t1 = [Phoneme("AH"), Phoneme("B"), Phoneme("EY"), Phoneme("T"), Phoneme("IH"), Phoneme("D")]
start = time.perf_counter_ns()
tilings = loaded_data.find_tilings(t1)
end = time.perf_counter_ns()

print("Time taken to tile:", end - start)
print()
print("All results")
for t, v in tilings.items():
    print(t, ":", v)

print()
print("Best distances")

best = sorted(list(tilings.items()), key=lambda x: x[-1])
print(best[:10])

most_residue = 3
for t, v in best[:10]:
    t_ = t
    if isinstance(t[-1], tuple):
        if len(t[-1]) > most_residue:
            t_ = list(t)
            t_[-1] = ",".join(t[-1][0:most_residue]) + ", ..."
            t_ = tuple(t_)

    print(t_, ":", v)

print(loaded_data.get_all_words(loaded_data.root.children[Phoneme("AH",0)].children[Phoneme("B")].children[Phoneme("EY", 1)].children[Phoneme("T")],False))

