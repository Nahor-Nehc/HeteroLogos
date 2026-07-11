from Phoneme import Phoneme

class TrieNode:
    def __init__(self):
        self.children:dict[Phoneme, TrieNode] = {}       # phoneme -> TrieNode
        self.stress:int = None   # stress -> allows us to calculate strength
        self.words = []          # words that end at this node (handles homophones)

class PhonemeTrie:
    def __init__(self):
        self.root = TrieNode()
        
        # use this for debugging mainly
        self._max_print_depth = 50
        self._current_print_depth = 0
    
    def __str__(self):
        self._current_print_depth = 0
        lines = []
        self._str_helper(self.root, prefix="", lines=lines, is_root=True)
        return "\n".join(lines)

    def _str_helper(self, node, prefix, lines, is_root):
        #* refactor to use Phoneme
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
        
        #* refactor to use Phoneme
        node = self.root
        print(phonemes)
        for p in phonemes:
            print(p)
            string = p
            stress = -1
            if p[-1].isnumeric():
                print("yes")
                stress = int(p[-1])
                string = p[:-1]
            
            phoneme = Phoneme(string=string, stress=stress)
            print(phoneme)
            
            if phoneme not in node.children:
                node.children[phoneme] = TrieNode()
            
            node = node.children[phoneme]
        node.words.append(word)  # terminal node stores the word

    def find_words_at_prefix(self, phonemes: list[Phoneme]) -> list[str]:
        """Return all words whose phoneme sequence exactly matches the given prefix."""
        #* refactor to use Phoneme
        node = self.root
        for phoneme in phonemes:
            if phoneme not in node.children:
                return []
            node = node.children[phoneme]
        return node.words  # only words that terminate exactly here

    def find_tilings(self, phonemes: list[str]) -> list[list[str]]:
        """
        Find all ways to tile the phoneme sequence with known words.
        Returns a list of sentences (each sentence is a list of words).
        """
        
        # we want to have options to be able to check for
        # complexity and strength which we can pass into the helper _tile
        
        results = {}
        self._tile(phonemes, 0, self.root, [], 0, results)
        return results

    def get_all_words(self, start_node:TrieNode=None):
        
        if start_node is None:
            start_node = self.root
        
        words = []
        stack:list[TrieNode] = [start_node]
        
        while stack:
            node = stack.pop()
            words.extend(node.words)
            
            stack.extend(node.children.values())
        
        return words
    
    
    def _tile(self, phonemes:list[Phoneme], position:int,
              current_node:TrieNode, current_sentence:list[str],
              current_score:int, results:dict[list[str]:int]):
        print()
        print(f"_tile: {phonemes}, pos {position}")
        
        # check we have reached the end
        if position >= len(phonemes):
            if current_sentence:
                #! flush the rest of the node and add to results
                
                # add the accumulated sentence to the results
                results[tuple(current_sentence)] = current_score
            return None
        
        # check node has no more children
        if not current_node.children:
            # do not add the accumulated sentence as there are no possible
            # sentences down this branch which can tile the phonemes
            return None
        
        # get the next phoneme
        phoneme = phonemes[position]
        print("next phoneme:", phoneme)
        
        # score against all children
        scored_children:list[tuple[Phoneme, int]] = []
        for child_phoneme, child_node in current_node.children.items():
            child_distance = phoneme.distance(child_phoneme)
            scored_children.append((child_phoneme, child_distance))
        
        # take the best scores
        scored_children.sort(key=lambda x: x[1])
        nodes_to_check = scored_children[:5]        #? temporary solution
        print(nodes_to_check)
        
        for child_phoneme, child_score in nodes_to_check:
            # check there are terminating words
            words = current_node.children[child_phoneme].words
            
            if words:
                for word in words:
                    
                    # tile on root node
                    self._tile(
                        phonemes=phonemes,
                        position=position+1,
                        current_node=self.root,
                        current_sentence=current_sentence + [word],
                        current_score=current_score + child_score,
                        results=results)
                    

            else:
                # otherwise tile on child node
                self._tile(
                    phonemes=phonemes,
                    position=position+1,
                    current_node=current_node.children[child_phoneme],
                    current_sentence=current_sentence, 
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
    
    create_baby_trie()
