import pickle
import os

from components.Phoneme import Phoneme
from components.PhonemeDistanceMatrix import PhonemeDistanceMatrix
from components.Trie import PhonemeTrie, TrieNode, create_trie



create_trie()


with open(os.path.join("data", "cmudict_trie.pkl"), "rb") as file:
    loaded_data:PhonemeTrie = pickle.load(file)

print(type(loaded_data))
print(loaded_data)
# print(loaded_data.get_all_words())
t1 = [Phoneme("AH"), Phoneme("B"), Phoneme("EY"), Phoneme("T"), Phoneme("IH"), Phoneme("D")]
tilings = loaded_data.find_tilings(t1)

for t, v in tilings.items():
    print(t, ":", v)

print(loaded_data.get_all_words(loaded_data.root.children[Phoneme("AH",0)].children[Phoneme("B")].children[Phoneme("EY", 1)].children[Phoneme("T")],False))
