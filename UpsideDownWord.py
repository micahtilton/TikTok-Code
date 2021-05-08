# these are the only letters that can be used to make a word that works with the mirror trick
accepted_letters = set('BCDEHIKOX')

# open the dictionary file and split the words into a list and make them all uppercase 
with open('words.txt', 'r') as dictionary_file:
    words = [word.upper() for word in dictionary_file.read().split('\n')]

# this is like a filter that only lets words that are only made up of the accepted letters
words = [word for word in words if set(word).issubset(accepted_letters)]

# sort the words by the length (key=len) because sorting by default is alphabetical
# reverse=True because sort will put the lowest value first ex: [0, 3, 4, 4, 5] we want the highest value first
words.sort(key=len, reverse=True)

# takes the first 15 words in the list and prints out the length along with the word itself
for word in words[:15]:
    print(len(word), word)
