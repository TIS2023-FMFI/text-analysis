# text-analysis
Project for Development of Information Systems 2023 - Text Analysis

Our team:

Alonso - supervision of coding

Patrik - work management

Kamil - documentation, communication

Our goal was to develop two applications. First one will be used as a tool in a search for signs of aphasia in texts based on statistics of the closest connections between words. The system will analyze given input file and produce statistics of every word connection in it. On this basis system will produce graphs. 
Second system prepares statistics of punctuations marks in texts. The system will analyze given input file for number of punctuation mark and the lengths (measured in the number of words) between any two punctuation marks. On this basis of this statistics system will produce graphs.

To use the punctuation app, download the app's code. Place it in the same directory as PyInstaller, which will convert the code into an executable file. In PowerShell (Windows) or the terminal (Linux), navigate to that directory and run the following command: "pyinstaller ./name_of_file --onefile"

To use the text statistics app, download the app's code. Place it in the same directory as PyInstaller, which will convert the code into an executable file. In PowerShell (Windows) or the terminal (Linux), navigate to that directory and run the following command: "pyinstaller ./name_of_file --hidden-import matplotlib --onefile"
