def convert_input_to_list(input_text):
    lines = input_text.strip().split('\n')
    result_list = []

    for line in lines:
        words = line.split(';')
        if len(words) == 3:
            word1, word2, frequency = words
            result_list.append({'word1': word1, 'word2': word2, 'frequency': int(frequency)})

    return result_list

# Example usage
input_text = """doorkeeper;the;18
man;the;8
his;in;7
law;the;6
am;i;4
of;the;4"""

output_list = convert_input_to_list(input_text)
print(output_list)