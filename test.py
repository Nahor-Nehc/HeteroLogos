import pickle
from Trie import PhonemeTrie, TrieNode
from Phoneme import Phoneme

with open("baby_cmudict_trie.pkl", "rb") as file:
    loaded_data:PhonemeTrie = pickle.load(file)

print(type(loaded_data))
print(loaded_data)
print(loaded_data.get_all_words())
t1 = [Phoneme("AH"), Phoneme("B"), Phoneme("EY"), Phoneme("T"), Phoneme("IH"), Phoneme("D")]
print(loaded_data.find_tilings(t1))