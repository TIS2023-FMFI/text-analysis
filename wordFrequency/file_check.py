from tkinter import messagebox
import codecs

def check_file(file_path):
    try:
        with codecs.open(file_path, 'r', encoding='utf-8') as file:
            file.read()
        messagebox.showinfo("File Check", "The file is appropriate.")
    except:
        messagebox.showerror("File Check", "The file is not appropriate. Make sure you are using a .txt file, some files may contain characters which are not compatable with UTF-8.")