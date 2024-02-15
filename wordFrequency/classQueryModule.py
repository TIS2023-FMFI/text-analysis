class QueryModule:

    # This method loads the file and prepare it for query
    def load_data(self):
        with open(self.filepath, 'r') as file:
            lines = file.readlines()
        return [line.strip().split(';') for line in lines]

    # 1st method runs query for entire text - it will print all records from file, sorted by number in linek, unless you change amount from None to the one you desire
    def sort_and_display(self, amount=None):
        sorted_data = sorted(self.data[1:], key=lambda x: int(x[-1]), reverse=True)

        print(f"Description: {self.data[0]}\n")

        if amount:
            sorted_data = sorted_data[:amount]

        sorted_data = [[line[0],line[1],int(line[2])] for line in sorted_data]

        return ["sort and display", sorted_data]


    # 2nd method searches for a pair of words and displays proper line

    def search_pair(self, word1, word2):
        result = []

        for line in self.data[1:]:
            #print(line)
            if word1 == word2:
                if line.count(word1) > 1:
                    result.append(line)
            elif word1 in line and word2 in line:
                result.append(line)

        print(f"Description: {self.data[0]}\n")

        if not result:
            print(f"No records found for words: {word1}, {word2}")
            return ["error", f"No records found for words: {word1}, {word2}"]

        return ["search pair"]+[int(result[0][2])]
    # 3rd method searches for one word in lines and displays all (or given amount of them) that contains it.

    def search_word(self, word, amount=None):
        result = [line for line in self.data[1:] if word in line]

        print(f"Description: {self.data[0]}\n")

        if amount:
            result = result[:amount]

        if not result:
            print(f"No records found for word: {word}")
            return ["error", f"No records found for word: {word}"]

        result = map(lambda line: [line[0] if (line[1]==word) else line[1]] + [int(line[2])],result)
        return ["search word", list(result)]

    def run_query(self, word1=None, word2=None, amount=None):
        if(word1==""):
            word1=None
        if(word2==""):
            word2=None
        if(amount==0):
            amount=None

        if word1 is None and word2 is None:
            return self.sort_and_display(amount)
        elif word1 is not None and word2 is not None:
            return self.search_pair(word1, word2)
        elif word1 is not None and word2 is None:
            return self.search_word(word1, amount)
        else:
            return ["error","Invalid arguments provided for query."]

    def call_query(self,input):
        self.filepath = input["analysisPath"]

        self.data = self.load_data()

        return self.run_query(input["word1"].lower(),input["word2"].lower(),input["amount"])



if __name__ == "__main__":
    # here you can change file
    filepath = "Kafka"
    query_module = QueryModule()


    # Test 1: sort_and_display
    print("Test 1: sort_and_display")
    data={
       "analysisPath":"Kafka",
       "word1":"",
       "word2":"",
       "amount":3,
    }
    t=query_module.call_query(data)
    print(t)

    # Test 2: search_pair
    print("\nTest 2: search_pair")
    data={
       "analysisPath":"Kafka",
       "word1":"it",
       "word2":"is",
       "amount":"",
    }
    t=query_module.call_query(data)
    print(t)

    # Test 3: search_word
    print("\nTest 3: search_word")
    data={
       "analysisPath":"Kafka",
       "word1":"the",
       "word2":"",
       "amount":2,
    }
    t=query_module.call_query(data)
    print(t)

    # Test 4: Invalid arguments
    print("\nTest 4: Invalid arguments")
    data={
       "analysisPath":"Kafka",
       "word1":"apple",
       "word2":"banana",
       "amount":3,
    }
    t=query_module.call_query(data)
    print(t)
    # Test 5: Invalid arguments
    print("\nTest 5: same word")
    data = {
        "analysisPath": "Kafka",
        "word1": "the",
        "word2": "the",
        "amount": 1,
    }
    t = query_module.call_query(data)
    print(t)
    print("\nTest 6: same word")
    data = {
        "analysisPath": "Kafka",
        "word1": "aaaa",
        "word2": "aaaa",
        "amount": 1,
    }
    t = query_module.call_query(data)
    print(t)
