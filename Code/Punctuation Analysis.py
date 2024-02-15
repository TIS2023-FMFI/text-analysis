import re
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import filedialog, messagebox

file_path = None  # Initialize file_path with None

def count_words_between_punctuation(file_path, punctuation_marks):
    # Create dictionary
    word_counts = defaultdict(int)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:  # Change the encoding if needed
            text = file.read()
    
        # Create a regex pattern based on user-defined punctuation marks
        pattern = f"[{''.join([re.escape(p) for p in punctuation_marks])}]\\s"
        # Split the text into segments based on the pattern
        segments = re.split(pattern, text)
    
        # Count words in each segment and add info to dictionary
        for segment in segments:
            words = segment.split()
            word_count = len(words)
            word_counts[word_count] += 1
    
    except:
        messagebox.showinfo("Error", "The file could not be read. This may be because the file is not a .txt file or because the file has been corrupted.") 
    return word_counts

def show_plot(result):
    global fig_canvas, canvas_frame
    if 'fig_canvas' in globals():
        fig_canvas.get_tk_widget().destroy()  # Remove existing plot canvas

        # Remove existing toolbar if it exists
        for widget in canvas_frame.winfo_children():
            widget.destroy()

    if 'canvas_frame' not in globals():
        canvas_frame = tk.Frame(root)
        canvas_frame.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky="nsew")

    fig, ax = plt.subplots(figsize=(8, 6))

    if log_x_axis.get():
        ax.set_xscale('log')
    if log_y_axis.get():
        ax.set_yscale('log')

    ax.bar(result.keys(), result.values(), color='skyblue')
    ax.set_xlabel('Distance Before Next Punctuation Mark (in words)')
    ax.set_ylabel('Frequency')
    ax.set_title('Segment Length Frequency')
    ax.grid(axis='y')  # Show gridlines on the y-axis
    
    fig_canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
    fig_canvas.draw()
    fig_canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    toolbar_frame = tk.Frame(canvas_frame)
    toolbar_frame.grid(row=1, column=0, sticky="ew")

    toolbar = NavigationToolbar2Tk(fig_canvas, toolbar_frame)
    toolbar.update()
    toolbar.grid(row=0, column=0, sticky="ew")
    
    # Add "Save Results" button
    save_button = tk.Button(canvas_frame, text="Save Results", command=lambda: save_results(result))
    save_button.grid(row=2, column=0, pady=10)


def save_results(result):
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        with open(file_path, 'w') as file:
            file.write('length, frequency\n')
            for length in range(max(result.keys()) + 1):  # Ensure the range covers all possible sentence lengths
                frequency = result.get(length, 0)  # Get the frequency or default to 0 if not present
                file.write(f"{length}\t{frequency}\n")
        messagebox.showinfo("Success", "Results saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error while saving results: {str(e)}")


def open_file():
    global file_path  # Use the global variable
    try:
        file_path = filedialog.askopenfilename()
        file_label.config(text=file_path)
    except:
        messagebox.showerror("Error", "Error while opening the file")
    
def submit_form():
    global file_path  # Use the global variable
    default_punctuation_marks = (''' ,.?!-':;–()/"[]{}''').split()
    if file_path:
        punctuation_marks = text_entry.get().strip()

        # Check if the input is empty or contains non-punctuation characters
        if not all(char in ''' ,.?!-':;–()/"[]{}''' for char in punctuation_marks):
            messagebox.showerror("Error", '''Invalid input for punctuation marks. Please use only , . ? ! - ' : ; – ( ) / " [ ] { }''')
            return

        if punctuation_marks:
            result = count_words_between_punctuation(file_path, punctuation_marks)
        else:
            result = count_words_between_punctuation(file_path, default_punctuation_marks)
        show_plot(result)
    else:
        messagebox.showinfo("Error", "Please select a file first.")   
        
# GUI
root = tk.Tk()
root.title("Punctuation Analysis")

# File selection
file_frame = tk.Frame(root)
file_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

file_label = tk.Label(file_frame, text="Selected File: ")
file_label.grid(row=0, column=0)

file_button = tk.Button(file_frame, text="Select File", command=open_file)
file_button.grid(row=0, column=1, pady=5)

# Text input
text_frame = tk.Frame(root)
text_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")

text_label = tk.Label(text_frame, text="Enter punctuation marks separated by spaces: (if none are given then all punctuation marks will be used) ")
text_label.grid(row=0, column=0, columnspan=2)

text_entry = tk.Entry(text_frame, width=30)
text_entry.grid(row=1, column=0, pady=5, columnspan=2)

log_x_axis = tk.BooleanVar()
log_y_axis = tk.BooleanVar()

log_x_checkbox = tk.Checkbutton(text_frame, text="Logarithmic X-axis", variable=log_x_axis)
log_x_checkbox.grid(row=2, column=0)

log_y_checkbox = tk.Checkbutton(text_frame, text="Logarithmic Y-axis", variable=log_y_axis)
log_y_checkbox.grid(row=2, column=1)

submit_button = tk.Button(text_frame, text="Submit", command=submit_form)
submit_button.grid(row=3, column=0, pady=5, columnspan=2)

# Graph display
canvas_frame = tk.Frame(root)
canvas_frame.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky="nsew")

root.mainloop()
