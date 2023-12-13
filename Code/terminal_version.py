from collections import defaultdict
import re
import json


class QueryModule:
    def __init__(self, filename):
        self.filename = filename
        self.data = self.load_data()
        self.last_query_results = []
        
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
        
        self.last_query_results = sorted_data

#2nd method searches for a pair of words and displays proper line
    
    def search_pair(self, word1, word2):
        result = []

        for line in self.data[1:]:
            if word1 in line and word2 in line:
                result.append(line)
        
        print("Title: " + self.filename)
        print(f"Description: {self.data[0]}\n")
        
        if not result:
            print("No matching pair found.\n")
        else:
            for line in result:
                print('; '.join(line))
        
        self.last_query_results = result
        
        return result
    
    
# 3rd method searches for one word in lines and displays all (or given amount of them) that contains it.
    
    def search_word(self, word, amount=None):
        result = [line for line in self.data[1:] if word in line]
        
        print("Title: " + self.filename)
        print(f"Description: {self.data[0]}\n")
        
        if not result:
            print(f"\nNo lines containing the word '{word}' found.\n")
        else:
            for line in result:
                print('; '.join(line))
        
        self.last_query_results = result
        
        return result     

# This method is for json export
    
    def save_results_to_json(self, title, description, query_settings, results):
        result_json = {
            "data": {
                "path": f"{title}.json",
                "title": title,
                "description": description,
                **query_settings  # Include all query settings
            },
            "results": results
        }

        # Save the JSON file with the title as the filename
        with open(f"{title}.json", 'w') as json_file:
            json.dump(result_json, json_file, indent=2)

  


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



def query_interface(filename):
    query1 = QueryModule(filename)

    while True:
        print("\n===== Query Menu =====")
        print("1. Search through entire text")
        print("2. Search for a pair of words")
        print("3. Search for a single word")
        print("4. Back to initial menu")

        choice = input("\nEnter your choice (1-4): ")

        query_settings = {
            "for_entire_text": False,
            "word1": "",
            "word2": "",
            "amount": 0,
            "logarithmic_scale": 0
        }

        if choice == '1':
            query_settings["for_entire_text"] = True
            query_settings["amount"] = int(input("Enter the amount (0 for all): "))
            print("\nYou have chosen to search through entire text\n")
            query1.sort_and_display(query_settings["amount"])

        elif choice == '2':
            query_settings["word1"] = input("Enter the first word: ")
            query_settings["word2"] = input("Enter the second word: ")
            print("\nYou have chosen to search for a pair of words\n")
            query1.search_pair(query_settings["word1"], query_settings["word2"])

        elif choice == '3':
            query_settings["word1"] = input("Enter the word: ")
            query_settings["amount"] = int(input("Enter the amount (0 for all): "))
            print("\nYou have chosen to search for one word\n")
            query1.search_word(query_settings["word1"], query_settings["amount"])

        elif choice == '4':
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

        query1.save_results_to_json(filename, query1.data[0], query_settings, query1.last_query_results)



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
            filename = input("Enter the filename for query: ")
            query_interface(filename)

        elif choice == '3':
            print("Program ended. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

# Initial program execution
initial_menu()