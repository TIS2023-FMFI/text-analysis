import re
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import filedialog, messagebox

file_path = None  # Initialize file_path with None

def count_words_between_punctuation(file_path, punctuation_marks):
    with open(file_path, 'r', encoding='utf-8') as file:  # Change the encoding if needed
        text = file.read()

    # Create a regex pattern based on user-defined punctuation marks
    pattern = f"[{''.join([re.escape(p) for p in punctuation_marks])}]\\s"
    # Split the text into segments based on the pattern
    segments = re.split(pattern, text)

    # Create dictionary
    word_counts = defaultdict(int)
    # Count words in each segment and add info to dictionary
    for segment in segments:
        words = segment.split()
        word_count = len(words)
        word_counts[word_count] += 1

    return word_counts

def show_plot(result):
    global fig_canvas, canvas_frame
    if 'fig_canvas' in globals():
        fig_canvas.get_tk_widget().destroy()  # Remove existing plot canvas

        # Remove existing toolbar if it exists
        for widget in root.winfo_children():
            if isinstance(widget, tk.Frame):
                for toolbar in widget.winfo_children():
                    if isinstance(toolbar, NavigationToolbar2Tk):
                        toolbar.destroy()

    if 'canvas_frame' not in globals():
        canvas_frame = tk.Frame(root)
        canvas_frame.pack(padx=10, pady=10)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(result.keys(), result.values(), color='skyblue')
    ax.set_xlabel('Distance Before Next Punctuation Mark (in words)')
    ax.set_ylabel('Frequency')
    ax.set_title('Segment Length Frequency')
    ax.grid(axis='y')  # Show gridlines on the y-axis
    
    fig_canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    fig_canvas.draw()
    fig_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(fig_canvas, canvas_frame)
    toolbar.update()
    fig_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def open_file():
    global file_path  # Use the global variable
    file_path = filedialog.askopenfilename()
    file_label.config(text=file_path)
    
def submit_form():
    global file_path  # Use the global variable
    default_punctuation_marks = ('.', ',', '?', '!')
    if file_path:
        punctuation_marks = text_entry.get()
        try:
            result = count_words_between_punctuation(file_path, punctuation_marks)
        except:
            result = count_words_between_punctuation(file_path, default_punctuation_marks)
        show_plot(result)
    else:
        messagebox.showinfo("Error", "Please select a file first.")     
        
# GUI
root = tk.Tk()
root.title("Punctuation Analysis")

# File selection
file_frame = tk.Frame(root)
file_frame.pack(padx=10, pady=10)

file_label = tk.Label(file_frame, text="Selected File: ")
file_label.pack()

file_button = tk.Button(file_frame, text="Select File", command=open_file)
file_button.pack(pady=5)

# Text input
text_frame = tk.Frame(root)
text_frame.pack(padx=10, pady=10)

text_label = tk.Label(text_frame, text="Enter punctuation marks separated by spaces: (if none are given then the default option will be used) ")
text_label.pack()

text_entry = tk.Entry(text_frame, width=30)
text_entry.pack(pady=5)

submit_button = tk.Button(text_frame, text="Submit", command=submit_form)
submit_button.pack(pady=5)

root.mainloop()