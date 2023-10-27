# Text analysis

from collections import defaultdict # dictionary with a default value, in this case 0 occurances of said word pair is the default value
import re # regular expressions

def count_adjacent_words(text):
    # Tokenize the text into words
    words = re.findall(r'\b\w+\b', text.lower())

    # Create a dictionary to store the frequency of adjacent word pairs
    adjacent_word_counts = defaultdict(int)

    # Iterate through the words and update the dictionary
    for i in range(len(words) - 1):
        # create a sorted tuple called word pair so that the order of words doesnt matter
        word_pair = tuple(sorted([words[i], words[i + 1]]))
        adjacent_word_counts[word_pair] += 1

    # Sort the word pairs by frequency in descending order
    sorted_word_pairs = sorted(adjacent_word_counts.items(), key=lambda x: x[1], reverse=True)

    return sorted_word_pairs

# Example usage:
if __name__ == "__main__":
    # Replace the following text with your own large body of text
    sample_text = """
    This is a sample text. This text can be replaced with your own large body of text.
    You can input any kind of text, and the program will count the frequency of adjacent words.
    """

    result = count_adjacent_words(sample_text)

    # Print the top 10 most frequent adjacent word pairs
    for word_pair, count in result[:10]:
        print(f"{word_pair}: {count} times")