from collections import defaultdict
import re
import json

class QueryModule:
    def __init__(self, filename):
        self.filename = filename
        self.data = self.load_data()
        self.for_entire_text = False

    def load_json_config(self, json_path):
            with open(json_path, 'r') as json_file:
                config_data = json.load(json_file)

            self.path = config_data.get('path')
            self.title = config_data.get('title')
            self.description = config_data.get('description')
            self.for_entire_text = config_data.get('for_entire_text', False)
            self.word1 = config_data.get('word1')
            self.word2 = config_data.get('word2')
            self.amount = config_data.get('amount')
            self.logarithmic_scale = config_data.get('logarithmic_scale')

        
# This method loads the file and prepare it for query
    def load_data(self):
        with open(self.filename, 'r') as file:
            lines = file.readlines()
        return [line.strip().split(';') for line in lines]

# 1st method runs query for entire text - it will print all records from file, sorted by number in linek, unless you change amount from None to the one you desire
    def sort_and_display(self, amount=None):
        sorted_data = sorted(self.data[1:], key=lambda x: int(x[-1]), reverse=True)

        print("Title: " + self.filename)
        print(f"Description: {self.data[0]}\n")
        
        if amount:
            sorted_data = sorted_data[:amount]

        for line in sorted_data:
            print('; '.join(line))

#2nd method searches for a pair of words and displays proper line
    
    def search_pair(self, word1, word2):
        result = []

        for line in self.data[1:]:
            if word1 in line and word2 in line:
                result.append(line)
        
        print("Title: " + self.filename)
        print(f"Description: {self.data[0]}\n")
        
        return result
    
    
# 3rd method searches for one word in lines and displays all (or given amount of them) that contains it.
    
    def search_word(self, word, amount=None):
        result = [line for line in self.data[1:] if word in line]
        
        print("Title: " + self.filename)
        print(f"Description: {self.data[0]}\n")
        
        return result          


class AnalysisModule:
    
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



def query_interface(query_module):
    print("\n===== Query Menu =====")
    print("1. Search through entire text")
    print("2. Search for a pair of words")
    print("3. Search for a single word")
    print("4. Back to initial menu")

    choice = input("\nEnter your choice (1-4): ")

    if choice == '1':
        amount = int(input("Enter the amount (0 for all): ")) if query_module.for_entire_text else None
        print("\nYou have chosen to search through entire text\n")
        query_module.sort_and_display(amount)

    elif choice == '2':
        word1 = query_module.word1
        word2 = query_module.word2
        print("\nYou have chosen to search for a pair of words\n")
        result = query_module.search_pair(word1, word2)
        if not result:
            print("No matching pair found.\n")
        else:
            for line in result:
                print('; '.join(line))

    elif choice == '3':
        word = query_module.word1  # Assuming you want to search a single word here
        amount = int(input("Enter the amount (0 for all): ")) if query_module.for_entire_text else None
        print("\nYou have chosen to search for a single word\n")
        result = query_module.search_word(word, amount)
        if not result:
            print(f"\nNo lines containing the word '{word}' found.\n")
        else:
            for line in result:
                print('; '.join(line))

    elif choice == '4':
        pass  # Do nothing, as we'll go back to the initial menu

    else:
        print("Invalid choice. Please enter a number between 1 and 4.")

def initial_menu():
    while True:
        print("\n===== Initial Menu =====")
        print("1. Analysis")
        print("2. Query")
        print("3. End program")

        choice = input("\nEnter your choice (1-3): ")

        if choice == '1':
            print('\nYou have chosen analysis')
            file_path = input("Enter the path to the file: ")
            title = input("Enter title: ")
            description = input("Enter description: ")
            AnalysisModule.count_connections_and_store(file_path, title, description)
            print('\nAnalysis done')

        elif choice == '2':
            print('\nYou have chosen query')
            json_path = input("Enter the path to the JSON file: ")
            query_module = QueryModule(json_path)
            query_interface(query_module)

        elif choice == '3':
            print("Program ended. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

# Initial program execution
initial_menu()
