
class Trie:
    def __init__(self, letter=""):
        self.letter = letter
        self.children = {}
        self.isWordEnd = False

    def add_word(self, word, idx=0):
        if word[idx] not in self.children:
            self.children[word[idx]] = Trie(word[idx])        
        if idx < len(word)-1:
            self.children[word[idx]].add_word(word, idx+1)
        if idx == len(word)-1:
            self.children[word[idx]].isWordEnd = True
        

    def print_trie(self, word=""):
        if self.isWordEnd:
            print(word+self.letter)
        for c in self.children.keys():
            self.children[c].print_trie(word+self.letter)
    
