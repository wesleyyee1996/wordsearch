import pickle
import nltk
from trie import Trie

nltk.download('words')

from nltk.corpus import words

root_trie = Trie()

for word in words.words():
    root_trie.add_word(word)

trie_corpus = open("trie_corpus", "wb")
pickle.dump(root_trie, trie_corpus)
trie_corpus.close()

