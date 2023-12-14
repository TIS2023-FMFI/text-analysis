from collections import defaultdict
import re
import os
from datetime import datetime

class QueryModule:
    def __init__(self, filename):
        self.filename = filename
        self.data = self.load_data()
        
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



def query_interface(filename):
    query1 = QueryModule(filename)

    while True:
        print("\n===== Query Menu =====")
        print("1. Search through entire text")
        print("2. Search for a pair of words")
        print("3. Search for a single word")
        print("4. Back to initial menu")

        choice = input("\nEnter your choice (1-4): ")

        if choice == '1':
            amount = int(input("Enter the amount (0 for all): "))
            print("\nYou have chosen to search through entire text\n")
            query1.sort_and_display(amount)

        elif choice == '2':
            word1 = input("Enter the first word: ")
            word2 = input("Enter the second word: ")
            print("\nYou have chosen to search for a pair of words\n")
            result = query1.search_pair(word1, word2)
            if not result:
                print("No matching pair found.\n")
            else:
                for line in result:
                    print('; '.join(line))

        elif choice == '3':            
            word = input("Enter the word: ")
            amount = int(input("Enter the amount (0 for all): "))
            print("\nYou have chosen to search for a pair of words\n")
            result = query1.search_word(word, amount)
            if not result:
                print(f"\nNo lines containing the word '{word}' found.\n")
            else:
                for line in result:
                    print('; '.join(line))

        elif choice == '4':
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

def initial_menu():
    while True:
        print("\n===== Initial Menu =====")
        print("1. Analysis")
        print("2. Delete file")
        print("3. Query")
        print("4. End program")

        choice = input("\nEnter your choice (1-4): ")

        if choice == '1':
            print('\nYou have chosen analysis')
            file_path = input("Enter the path to the file: ")
            title = input("Enter title: ")
            description = input("Enter description: ")
            AnalysisModule.count_connections_and_store(file_path, title, description)
            print('\nAnalysis done')

        elif choice == '2':
            print('\nYou have chosen to delete a file')
            file_path_to_delete = input("Enter the path to the file you want to delete: ")
            confirm = input("Are you sure you want to delete this file? (Y/N): ")

            if confirm.upper() == 'Y':
                try:
            # Delete file
                    os.remove(file_path_to_delete)
                    print(f"File '{file_path_to_delete}' deleted successfully.")
            
            # Dodaj wpis do pliku Deleted_files_list.txt
                    deletion_info = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {file_path_to_delete}\n"
                    with open('Deleted_files_list.txt', 'a') as deleted_files_list:
                        deleted_files_list.write(deletion_info)

                except FileNotFoundError:
                    print(f"File '{file_path_to_delete}' not found.")
                except PermissionError:
                    print(f"Permission denied to delete '{file_path_to_delete}'.")
            else:
                print(f"Deletion of '{file_path_to_delete}' canceled.")
        
        
        elif choice == '3':
            print('\nYou have chosen query')
            filename = input("Enter the filename for query: ")
            query_interface(filename)

        elif choice == '4':
            print("Program ended. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 3.")

# Initial program execution
initial_menu()
