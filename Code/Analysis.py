from collections import defaultdict
import re

def count_connections_and_store(file_path, title, description):
    # Extract the text from the file
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    # Tokenize the text into words
    words = re.findall(r'\b\w+\b', text.lower())

    # Create a dictionary to store the frequency of adjacent word pairs
    adjacent_word_counts = defaultdict(int)

    # Iterate through the words and update the dictionary
    for i in range(len(words) - 1):
        word_pair = tuple(sorted([words[i], words[i + 1]]))
        adjacent_word_counts[word_pair] += 1

    # Sort the word pairs by frequency in descending order
    sorted_word_pairs = sorted(adjacent_word_counts.items(), key=lambda x: x[1], reverse=True)

    # make a new txt file with description and then all word connections
    with open(title, 'w') as file:
        file.write(f"{description}\n")
        for word_pair, frequency in sorted_word_pairs:
            word1, word2 = word_pair
            file.write(f"{word1};{word2};{frequency}\n")




# main (test scenario)
file_path = r"C:\Users\bidna\Documents\Study Abroad\WORK\Example book.txt"
description = 'This is an example text written in english and taken from project gottenburg. The author did not have aphasia i believe but i cannot say for sure.'
title = 'Test Output'

count_connections_and_store(file_path,title,description)
print('done')
