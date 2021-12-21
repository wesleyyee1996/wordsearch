from english_words import english_words_lower_set
from trie import Trie

trie = Trie()

word_set = [['a','l','g','r'],
['t','o','p','i'],
['d','e','r','l'],
['y','u','f','g']]

cnt = 0
for word in english_words_lower_set:
    if cnt > 1000:
        break
    cnt += 1
    trie.add_word(word)

for i in range(len(word_set)):
    for j in range(len(word_set[0])):
        