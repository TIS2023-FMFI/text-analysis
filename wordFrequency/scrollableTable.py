import tkinter as tk
from tkinter import ttk
import dataConventor
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class ScrollableTable(tk.Frame):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.parent = parent
        self.data = data
        self.tableData = None
        if(not(data is None)):
            self.create_table()

    def create_table(self):
        self.tableData = dataConventor.queryModuleToListOfSet(self.data)
        self.tree = ttk.Treeview(self, show='headings')
        self.tree['columns'] = tuple(self.tableData[0].keys())
        print(self.tree['columns'])

        for col in self.tree['columns']:
            self.tree.heading(col, text=col, anchor=tk.CENTER)
            self.tree.column(col, anchor=tk.CENTER)

        for row in self.tableData:
            self.tree.insert('', 'end', values=tuple(row.values()))

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

    def update_table(self, data):
        if(self.data is None):
            self.data=data
            self.tableData=dataConventor.queryModuleToListOfSet(data)
            self.create_table()
            return
        # Clear existing columns and data
        self.data=data
        self.tableData = dataConventor.queryModuleToListOfSet(data)
        self.tree.delete(*self.tree.get_children())
        self.tree['columns'] = tuple(self.tableData[0].keys())
        for col in self.tree['columns']:
            self.tree.heading(col, text=col, anchor=tk.CENTER)
            self.tree.column(col, anchor=tk.CENTER)

        # Insert new data
        for row in self.tableData:
            self.tree.insert('', 'end', values=tuple(row.values()))

class BarChart(tk.Frame):
    def __init__(self, parent, data):
        super().__init__(parent)
        self.parent = parent
        self.data = data
        self.log_scale_var = tk.IntVar(value=0)  # Variable to store log scale state

        self.figure = Figure(figsize=(6, 4), tight_layout=True)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()

        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.ax = self.figure.add_subplot(111)

        if not (data is None):
            self.update_chart(data)

        # Add a button for toggling log scale
        self.log_scale_button = tk.Checkbutton(self, text="Log Scale", variable=self.log_scale_var, command=self.toggle_log_scale)
        self.log_scale_button.pack()

    def toggle_log_scale(self):
        if self.log_scale_var.get() == 1:
            self.ax.set_yscale("log")
        else:
            self.ax.set_yscale("linear")

        self.canvas.draw()

    def update_chart(self, data):
        # Clear existing data
        self.ax.clear()

        data = dataConventor.queryModuleToBarChartMap(data)
        labels, values = data.keys(), data.values()

        # Create a bar chart
        self.ax.bar(labels, values)

        # Set labels and title
        self.ax.set_xlabel('Words')
        self.ax.set_ylabel('Frequency')
        self.ax.set_title('Bar Chart')

        # Rotate category labels
        self.ax.set_xticks(range(len(labels)))
        self.ax.set_xticklabels(labels, rotation=45, ha='right')

        # Draw the chart
        self.canvas.draw()


class TextPath:
    path = ""
    title = ""
    about = ""

    def __init__(self, path, title="", about=""):
        self.path = path
        self.title = title
        self.about = about


if __name__ == "__main__":
    data = [
        {"Name": "Alice", "Age": 25},
        {"Name": "Bob", "Age": 30},
        {"Name": "Charlie", "Age": 22},
        # ... Add more data here
    ]
    data= [["Alice", 25],["Bob", 30],["Charlie", 22],]
        # ... Add more data here
    data2 = [["Alice","bob", 2500],["Bob","bob", 30],["Charlie","dud", 22],["joshua","joshua",10]]

    root = tk.Tk()  # Use Tk() to create the main window
    root.geometry("400x300")

    table =BarChart(root,data)
    #table = ScrollableTable(root, data)
    table.pack(fill=tk.BOTH, expand=1)

    root.after(3000, lambda: table.update_chart(data2))

    root.mainloop()
