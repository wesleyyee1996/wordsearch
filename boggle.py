import pickle
from trie import Trie
from found_word import FoundWord
import copy
import time
import math
from move import Move

trie_corpus_file = open("trie_corpus", "rb")
root_trie = pickle.load(trie_corpus_file)
trie_corpus_file.close()

print("Loaded corpus!")

class WordSearch:
    def __init__(self, word_set):
        self.word_set = self.process_wordset(word_set)
        print(self.word_set)
        self.height_words = len(self.word_set)
        self.width_words = len(self.word_set[0])
        self.found_words_set = set()
        self.found_words_lst = []

    def process_wordset(self, word_set_raw):
        
        len_word_set = len(word_set_raw)
        sqrt_len = int(math.sqrt(len_word_set))

        word_set_processed = [[None for x in range(sqrt_len)] for y in range(sqrt_len)]
        # we have a valid board (it is a square)
        if math.floor(sqrt_len) == sqrt_len:
            for i in range(sqrt_len):
                for j in range(sqrt_len):
                    idx = sqrt_len*i + j
                    word_set_processed[i][j] = word_set_raw[idx]

        else:
            raise ValueError

        return word_set_processed


    def recurse(self, curr_pos, visited, trie_node, curr_str):
        if trie_node.isWordEnd and curr_str.word not in self.found_words_set:
            self.found_words_set.add(curr_str.word)
            self.found_words_lst.append(curr_str)

        x_idx = curr_pos[0]
        y_idx = curr_pos[1]

        for i in range(x_idx-1, x_idx+2):
            for j in range(y_idx-1, y_idx+2):
                if 0 <= i < self.width_words and 0 <= j < self.height_words and (i,j) not in visited:

                    if self.word_set[i][j] in trie_node.children:
                        new_visited = copy.deepcopy(visited)
                        new_visited.add((i,j))
                        new_str = copy.deepcopy(curr_str)
                        new_str.word = new_str.word + self.word_set[i][j]
                        new_str.path.append((i,j))
                        self.recurse((i,j), new_visited, trie_node.children[self.word_set[i][j]], new_str)

    def find_words(self, root_trie):

        empty_set = set()

        for i in range(self.height_words):
            for j in range(self.width_words):
                self.recurse((i,j), empty_set, root_trie, FoundWord("",[]))

        return sorted(self.found_words_lst, key= lambda x: len(x.word), reverse = True)

    

def do_word_search():

    try:
        move = Move()

        while True:
            try:
                word_set = input("Input board: ")
                wordsearch = WordSearch(word_set)

                i = 0
                for word in wordsearch.find_words(root_trie):
                    i += 1
                    if i == 10:
                        break
                    print("Writing word " + word.word + " at path: " + str(word.path))
                    for pos in word.path:
                        move.to_with_transform(pos)

            except ValueError:
                print("The inputted board was invalid: " + word_set)

    except KeyboardInterrupt:
        move.stepper.setUDStep(0,0,0,0)
        move.stepper.setLRStep(0,0,0,0)

if __name__ == '__main__':

    try:
        do_word_search()

    except Exception as ex:
        print("An error occurred: ",ex)

