class TrieNode:
    def __init__(self):
        self.children = {}       # phoneme -> TrieNode
        self.words = []          # words that end at this node (handles homophones)

class PhonemeTrie:
    def __init__(self):
        self.root = TrieNode()
        self._max_print_depth = 30
        self._current_print_depth = 0
    
    def __str__(self):
        self._current_print_depth = 0
        lines = []
        self._str_helper(self.root, prefix="", lines=lines, is_last=True, is_root=True)
        return "\n".join(lines)

    def _str_helper(self, node, prefix, lines, is_last, is_root):
        if self._current_print_depth > self._max_print_depth:
            return None
        
        self._current_print_depth += 1
        
        children = list(node.children.items())[:self._max_print_depth]

        if is_root:
            lines.append("ROOT")
        
        for i, (phoneme, child) in enumerate(children):
            is_last_child = (i == len(children) - 1)
            connector = "└── " if is_last_child else "├── "
            label = f"{phoneme}  {child.words}" if child.words else phoneme
            lines.append(f"{prefix}{connector}{label}")

            extension = "    " if is_last_child else "│   "
            self._str_helper(child, prefix + extension, lines, is_last_child, is_root=False)

    def insert(self, phonemes: list[str], word: str):
        """Insert a word indexed by its phoneme sequence."""
        node = self.root
        for phoneme in phonemes:
            if phoneme not in node.children:
                node.children[phoneme] = TrieNode()
            node = node.children[phoneme]
        node.words.append(word)  # terminal node stores the word

    def find_words_at_prefix(self, phonemes: list[str]) -> list[str]:
        """Return all words whose phoneme sequence exactly matches the given prefix."""
        node = self.root
        for phoneme in phonemes:
            if phoneme not in node.children:
                return []
            node = node.children[phoneme]
        return node.words  # only words that terminate exactly here

    def find_all_tilings(self, phonemes: list[str]) -> list[list[str]]:
        """
        Find all ways to tile the phoneme sequence with known words.
        Returns a list of sentences (each sentence is a list of words).
        """
        results = []
        self._tile(phonemes, 0, [], results)
        return results

    def _tile(self, phonemes, pos, current_sentence, results):
        if pos == len(phonemes):
            results.append(list(current_sentence))
            return None

        node = self.root
        for i in range(pos, len(phonemes)):
            phoneme = phonemes[i]
            if phoneme not in node.children:
                break                          # no words down this path, prune
            node = node.children[phoneme]
            if node.words:                     # a word ends here
                for word in node.words:
                    current_sentence.append(word)
                    self._tile(phonemes, i + 1, current_sentence, results)
                    current_sentence.pop()     # backtrack
       
       
                    
# import re

# with open("cmudict.txt", "r") as f:
#     text = f.read()
    
#     cmudict = text.splitlines()

# trie = PhonemeTrie()

# import time, pickle

# start = time.time_ns()
# for entry in cmudict:
#     if entry:
#         _entry = entry.split(" ")
#         word = _entry[0]
#         phonemes = _entry[1:]
#         trie.insert(word=word, phonemes=phonemes)
# end = time.time_ns()
# print("Time:", (end - start)/10**9)

# with open("cmudict_trie_stress.pkl", "wb") as file:
#     pickle.dump(trie, file)

# print(trie)