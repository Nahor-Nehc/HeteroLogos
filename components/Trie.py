import os

from components.Phoneme import Phoneme
from components.PhonemeDistanceMatrix import PhonemeDistanceMatrix


class TrieNode:
    def __init__(self):
        self.children:dict[Phoneme, TrieNode] = {}       # phoneme -> TrieNode
        self.stress:int | None = None   # stress -> allows us to calculate strength
        self.words:list[str] = []          # words that end at this node (handles homophones)

class PhonemeTrie:
    def __init__(self):
        self.root = TrieNode()
        self.pdm = PhonemeDistanceMatrix(
            os.path.join("assets", "arpabet_ch_distance_matrix.csv"))
        
        # scoring parameters
        self.spw_threshold = 2 # score per word threshold
        self.max_children_checked = 4
        
        # use this for debugging mainly
        self._max_print_depth = 50
        self._current_print_depth = 0
    
    def __str__(self) -> str:
        self._current_print_depth = 0
        lines = []
        self._str_helper(self.root, prefix="", lines=lines, is_root=True)
        return "\n".join(lines)

    def _str_helper(self, node, prefix, lines, is_root):
        if self._current_print_depth > self._max_print_depth:
            return None
        
        self._current_print_depth += 1
        
        children = list(node.children.items())[:self._max_print_depth]

        if is_root:
            lines.append("ROOT")
        
        for i, (phoneme, child) in enumerate(children):
            is_last_child = (i == len(children) - 1)
            connector = "└── " if is_last_child else "├── "
            label = f"{str(phoneme)}  {child.words}" if child.words else str(phoneme)
            lines.append(f"{prefix}{connector}{label}")

            extension = "    " if is_last_child else "│   "
            self._str_helper(child, prefix + extension, lines, is_root=False)

    def insert(self, phonemes: list[str], word: str):
        """Insert a word indexed by its phoneme sequence."""
        
        node = self.root
        for p in phonemes:
            
            # get the components of the phoneme
            string = p
            stress = -1
            if p[-1].isnumeric():
                stress = int(p[-1])
                string = p[:-1]
            phoneme = Phoneme(string=string, stress=stress)
            
            # check if new child needs to be created
            if phoneme not in node.children:
                node.children[phoneme] = TrieNode()
            
            # go to the next node
            node = node.children[phoneme]
            
        node.words.append(word)  # terminal node stores the word

    def find_words_at_prefix(self, phonemes: list[Phoneme]) -> list[str]:
        """Return all words whose phoneme sequence exactly matches the given prefix."""
        node = self.root
        for phoneme in phonemes:
            if phoneme not in node.children:
                return []
            node = node.children[phoneme]
        return node.words  # only words that terminate exactly here

    def find_tilings(self, phonemes: list[Phoneme]) -> dict[tuple[str, ...], float]:
        """
        Find all ways to tile the phoneme sequence with known words.
        Returns a list of sentences (each sentence is a list of words).
        """
        
        # we want to have options to be able to check for
        # complexity and strength which we can pass into the helper _tile
        
        results = {}
        self._tile(phonemes, 0, self.root, [], False, 0, results)
        return results

    def get_all_words(self, start_node: TrieNode|None=None, inclusive: bool=True) -> list[str]:
        
        if start_node is None:
            start_node = self.root
        
        words = []
        stack:list[TrieNode] = [start_node]
        
        while stack:
            node = stack.pop()
            
            # check if we want the first node's words
            if node != start_node or inclusive:
                words.extend(node.words)
                
            stack.extend(node.children.values())
        
        return words
    
    
    def _tile(self, phonemes:list[Phoneme], position:int,
              current_node:TrieNode, current_sentence:list[str],
              word_added:bool,
              current_score:float, results:dict[tuple[str, ...], float]):
        """Recursively tiles the list of phonemes with a list of words

        :param phonemes: the list of phonemes to tile
        :type phonemes: list[Phoneme]
        :param position: the location to start tiling
        :type position: int
        :param current_node: node of the Trie to start
        :type current_node: TrieNode
        :param current_sentence: the current sentence accumulated
        :type current_sentence: list[str]
        :param word added: if a word was just added
        :type word added: bool
        :param current_score: the score of the current sentence
        :type current_score: float
        :param results: a dictionary of the results. the key is the
        tuple of words and the value is the score
        :type results: dict[tuple[str], float]
        """        
        
        
        # print()
        # print(f"_tile: {phonemes}, pos {position}")
        
        # check we have reached the end
        if position >= len(phonemes):
            if current_sentence:
                
                # check enough syllables
                if word_added:
                    # add the accumulated sentence to the results
                    results[tuple(current_sentence)] = current_score
                    
                else:
                    # flush the rest of the node and add to results
                    remaining_words = self.get_all_words(current_node, False)
                    
                    for remaining_word in remaining_words:
                        results[tuple(current_sentence + [remaining_word])] = current_score
                    
            return None
        
        # check node has no more children
        if not current_node.children:
            # do not add the accumulated sentence as there are no possible
            # sentences down this branch which can tile the phonemes
            return None
        
        # calculate the score per word
        if current_sentence:
            if current_score/len(current_sentence) >= self.spw_threshold:
                return None
        
        # get the next phoneme
        phoneme = phonemes[position]
        # print("next phoneme:", phoneme)
        
        # score against all children
        scored_children:list[tuple[Phoneme, float]] = []
        for child_phoneme, child_node in current_node.children.items():
            
            # score strength
            child_distance = phoneme.distance(child_phoneme, self.pdm)
            
            scored_children.append((child_phoneme, child_distance))
        
        # take the best scores (lowest)
        scored_children.sort(key=lambda x: x[1])
        #? temporary solution
        nodes_to_check = scored_children[:self.max_children_checked]
        
        # print(nodes_to_check)
        
        for child_phoneme, child_score in nodes_to_check:
            # check there are terminating words
            words = current_node.children[child_phoneme].words
            
            if words:
                for word in words:
                    
                    # score complexity
                    #? temporary solution -> longer words means better score
                    #? penalise short words
                    child_score /= 2**len(word) / 8
                    
                    # tile on root node
                    self._tile(
                        phonemes=phonemes,
                        position=position+1,
                        current_node=self.root,
                        current_sentence=current_sentence + [word],
                        word_added=True,
                        current_score=current_score + child_score,
                        results=results)
                    

            # then tile on child node
            self._tile(
                phonemes=phonemes,
                position=position+1,
                current_node=current_node.children[child_phoneme],
                current_sentence=current_sentence, 
                word_added=False,
                current_score=current_score + child_score,
                results=results
            )
            
        

def remove_comments(s:str) -> str:
    return s.split("#")[0].strip()

def create_trie():
    with open("cmudict.txt", "r") as f:
        text = f.read()
        
        cmudict = text.splitlines()

    trie = PhonemeTrie()

    for entry in cmudict:
        removed_comments = remove_comments(entry)
        if removed_comments:
            _entry = removed_comments.split(" ")
            word = _entry[0]
            phonemes = _entry[1:]
            trie.insert(word=word, phonemes=phonemes)

    with open("cmudict_trie.pkl", "wb") as file:
        pickle.dump(trie, file)

    # print(trie)
    
def create_baby_trie():
    with open("baby_cmudict.txt", "r") as f:
        text = f.read()
        
        cmudict = text.splitlines()

    trie = PhonemeTrie()

    for entry in cmudict:
        removed_comments = remove_comments(entry)
        if removed_comments:
            _entry = removed_comments.split(" ")
            word = _entry[0]
            phonemes = _entry[1:]
            trie.insert(word=word, phonemes=phonemes)
    

    with open("baby_cmudict_trie.pkl", "wb") as file:
        pickle.dump(trie, file)

def create_dictionary():
    pass

if __name__ == "__main__":
        
    import re
    import time, pickle
    
    create_trie()
