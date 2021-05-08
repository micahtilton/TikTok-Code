with open("dictionary.txt", 'r') as dictionary_file:
    words = dictionary_file.read().split('\n')

translator = {
    'o':'0',
    'i':'1',
    'e':'3',
    'h':'4',
    's':'5',
    'g':'6',
    'l':'7',
    'b':'8',
}

accepted = []
possible_letters = set('oiehsglb')

for word in words:
    unique_letters = set(word)

    if unique_letters.issubset(possible_letters):
        number = ''.join([translator[letter] for letter in word][::-1])

        if number[0] == '0':
            number = '0.' + number[1:]
            
        length = len(word)

        accepted.append((word, number, length))

accepted.sort(key=lambda x: x[2], reverse=True)

for word in accepted[:100]:
    print(f"{word[2]}. {word[0].upper()} -> {word[1]}")
