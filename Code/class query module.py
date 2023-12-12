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

        print(self.filename)
        print(self.data[0])
        
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

        return result
    
    
# 3rd method searches for one word in lines and displays all (or given amount of them) that contains it.
    
    def search_word(self, word, amount=None):
        result = [line for line in self.data[1:] if word in line]
        return result             

#Here you can change the file or input method of 
filename = "Test Output"

query1 = QueryModule(filename)

#interface:

while True:
    print("\n===== Initial Menu =====")
    print("1. Search through entire text")
    print("2. Search for a pair of words")
    print("3. Search for a single word")
    print("4. End program")

    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        amount = int(input("Enter the amount (0 for all): "))
        query1.sort_and_display(amount)

    elif choice == '2':
        word1 = input("Enter the first word: ")
        word2 = input("Enter the second word: ")
        result = query1.search_pair(word1, word2)
        if not result:
            print("No matching pair found.")
        else:
            for line in result:
                print('; '.join(line))

    elif choice == '3':
        word = input("Enter the word: ")
        amount = int(input("Enter the amount (0 for all): "))
        result = query1.search_word(word, amount)
        if not result:
            print("No lines containing the word '{word}' found.")
        else:
            for line in result:
                print('; '.join(line))

    elif choice == '4':
        print("Program ended. Goodbye!")
        break

    else:
        print("Invalid choice. Please enter a number between 1 and 4.")


