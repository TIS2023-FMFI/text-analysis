import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

class BaseFrame(tk.Frame):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app.root, *args, **kwargs)
        self.app = app

    def hide_frame(self):
        self.pack_forget()

    def switch_to_frame(self, frame_class):
        self.app.show_frame(frame_class)

    def update(self):
        pass

class Frame1(BaseFrame):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        #tk.Label(self, text="This is Window 1").pack(pady=10)
        tk.Button(self, text="Upload Text", command=lambda: self.switch_to_frame(UploadText)).pack(pady=10)
        tk.Button(self, text="Delete Text", command=lambda: self.switch_to_frame(DeleteText)).pack(pady=10)
        tk.Button(self, text="Show stats", command=lambda: self.switch_to_frame(ShowStats)).pack(pady=10)

class UploadText(BaseFrame):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        #tk.Label(self, text="This is Window 2").pack(pady=10)
        tk.Button(self, text="chose file", command=self.upload_file).pack(pady=10)
        self.file_path=""
        self.status_label = tk.Label(self, text="No file selected")
        self.status_label.pack()
        self.label = tk.Label(self, text="Enter Name:")
        self.label.pack(pady=10)

        # Create a text entry widget
        self.tittleName = tk.Entry(self)
        self.tittleName.pack(pady=10)

        self.label2 = tk.Label(self, text="Enter about:")
        self.label2.pack(pady=10)

        # Create a text entry widget
        self.about = tk.Text(self, wrap="word", height=5, width=40)
        self.about.pack(pady=10)

        # Create a button to submit the text
        self.submit_button = tk.Button(self, text="Submit", command=self.on_submit)
        self.submit_button.pack(pady=10)

        tk.Button(self, text="Cancel", command=lambda: self.switch_to_frame(Frame1)).pack(pady=10)

    def on_submit(self):
        if self.file_path=="":
            return
        file_path=self.file_path
        name= self.tittleName.get()
        about = self.about.get("1.0", tk.END)
        if(name==""):
            return
        for savedPath in app.TextPathList:
            if savedPath.title == name:
                return

        self.about.delete("1.0", tk.END)
        app.add_text_path(file_path,name,about)
        self.switch_to_frame(Frame1)



    def upload_file(self):
        self.file_path = filedialog.askopenfilename(title="Select a file")
        if self.file_path:
            self.status_label.config(text=f"File selected: {self.file_path}")


class DeleteText(BaseFrame):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        tk.Label(self, text="This is Window 1").pack(pady=10)
        tk.Button(self, text="Go to Start", command=lambda: self.switch_to_frame(Frame1)).pack(pady=10)
        tk.Button(self, text = "Delete", command = self.onDelete).pack(pady=10)

        values2 = self.app.getFilesTitles()
        print(values2)

        # Create a StringVar to store the selected value
        self.selected_value = tk.StringVar()
        self.combo_box = ttk.Combobox(self, textvariable=self.selected_value,
                                      values=values2)
        self.combo_box.pack(pady=10)

    def update(self):
        values2 = self.app.getFilesTitles()
        print(values2)
        #self.selected_value = tk.StringVar()
        self.combo_box['values']=values2
        self.combo_box.set('')

    def onDelete(self):
        text=self.selected_value.get()
        if(text==""):
            return
        for path in app.TextPathList:
            if(text == path.title):
                app.TextPathList.remove(path)
                self.update()
                return


class ShowStats(BaseFrame):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        tk.Label(self, text="This is Window 2").pack(pady=10)
        tk.Button(self, text="Switch to Window 1", command=lambda: self.switch_to_frame(Frame1)).pack(pady=10)

        values=self.app.getFilesTitles()
        self.doc = tk.StringVar()
        self.combo_box = ttk.Combobox(self, textvariable=self.doc,
                                       values=values)
        self.combo_box.pack(pady=10)

        tk.Label(self, text="Word1").pack(pady=10)
        self.word1 = tk.Entry(self)
        self.word1.pack(pady=10)

        tk.Label(self, text="Word2").pack(pady=10)
        self.word2 = tk.Entry(self)
        self.word2.pack(pady=10)

        self.checkbox_var = tk.BooleanVar()

        # Create a checkbox
        self.checkbox = tk.Checkbutton(self, text="Show statistic for entire text", variable=self.checkbox_var)
        self.checkbox.pack(pady=10)

        tk.Label(self, text="Amount").pack(pady=10)
        vcmd = (self.register(self.allowInteger))

        self.amount= tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.amount.pack(pady=10)

        tk.Label(self, text="Logarithm scale").pack(pady=10)
        vcmd = (self.register(self.allowFloat))

        self.logScale = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.logScale.pack(pady=10)


        tk.Button(self, text = "See result", command = self.onSeeResults).pack(pady=10)

    def allowInteger(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    def allowFloat(self, P):
        if self.allowInteger(P.replace(".", "", 1)):
            return True
        else:
            return False

    def onSeeResults(self):
        doc = self.doc.get()
        if (doc == ""):
            return
        filePath=None
        for path in app.TextPathList:
            if (doc == path.title):
                filePath = path
        if(filePath==None):
            return
        word1 = self.word1.get()
        word2 = self.word2.get()
        forEntireText=self.checkbox_var.get()
        amount =0
        try:
            # Get the integer input from the StringVar
            amount = int(self.amount.get())
            #print("Integer input:", numeric_value)
        except ValueError:
            print("Invalid amount input")
        logScale=0
        try:
            # Get the integer input from the StringVar
            logScale = float(self.logScale.get())
            #print("Integer input:", numeric_value)
        except ValueError:
            print("Invalid Logscale input")
        print(filePath.title,word1,word2,forEntireText,amount,logScale)

    def update(self):
        print('')
        values2 = self.app.getFilesTitles()
        print(values2)
        # self.selected_value = tk.StringVar()
        self.combo_box['values'] = values2
        self.combo_box.set('')

class App:
    TextPathList = []
    def __init__(self, root):
        self.root = root
        self.root.title("App")

        self.frames = {}
        self.initialize_frames()

        self.TextPathList=[]

        self.show_frame(Frame1)

    def initialize_frames(self):
        self.frames[Frame1] = Frame1(self)
        self.frames[UploadText] = UploadText(self)
        self.frames[DeleteText] = DeleteText(self)
        self.frames[ShowStats] = ShowStats(self)

    def show_frame(self, frame_class):
        for frame in self.frames.values():
            frame.pack_forget()

        self.frames[frame_class].update()
        self.frames[frame_class].pack()



    def add_text_path(self, path, title="", about=""):
        # Add a new TextPath instance to the list
        text_path = TextPath(path, title, about)
        self.TextPathList.append(text_path)

    def getFilesTitles(self):
        TextPaths = self.TextPathList
        return [path.title for path in TextPaths]


class TextPath():
    path=""
    title=""
    about=""
    def __init__(self,path,title="",about=""):
        self.path=path
        self.title=title
        self.about=about

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()