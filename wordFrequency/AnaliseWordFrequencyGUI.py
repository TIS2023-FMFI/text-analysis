import tkinter as tk
from tkinter import filedialog
from tkinter import ttk,messagebox
import classQueryModule as cqm
import Analysis
import file_check
import os
import SaveLoadSystem

from scrollableTable import ScrollableTable, BarChart, TextPath

class BaseFrame(tk.Frame):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app.root, *args, **kwargs)
        self.app = app

    def hide_frame(self):
        self.pack_forget()

    def switch_to_frame(self, frame_class):
        self.app.show_frame(frame_class)

    def getFrame(self,frame_class):
        return self.app.getFrame(frame_class)

    def update(self):
        pass

class MainMenu(BaseFrame):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        #tk.Label(self, text="This is Window 1").pack(pady=10)
        tk.Button(self, text="Upload Text", command=lambda: self.switch_to_frame(UploadText)).pack(pady=10)
        tk.Button(self, text="Delete Text", command=lambda: self.switch_to_frame(DeleteText)).pack(pady=10)
        tk.Button(self, text="Show stats", command=lambda: self.switch_to_frame(SelectToAnaliseFrame)).pack(pady=10)

class UploadText(BaseFrame):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        #tk.Label(self, text="This is Window 2").pack(pady=10)
        tk.Button(self, text="Select file", command=self.upload_file).pack(pady=10)
        self.file_path=""
        self.status_label = tk.Label(self, text="No file selected")
        self.status_label.pack()
        self.label = tk.Label(self, text="Enter Name:")
        self.label.pack(pady=10)

        # Create a text entry widget
        self.tittleName = tk.Entry(self)
        self.tittleName.pack(pady=10)

        self.label2 = tk.Label(self, text="Enter description:")
        self.label2.pack(pady=10)

        # Create a text entry widget
        self.about = tk.Text(self, wrap="word", height=5, width=40)
        self.about.pack(pady=10)

        # Create a button to submit the text
        self.submit_button = tk.Button(self, text="Submit", command=self.on_submit)
        self.submit_button.pack(pady=10)

        tk.Button(self, text="Cancel", command=lambda: self.switch_to_frame(MainMenu)).pack(pady=10)

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
        Analysis.count_connections_and_store(self.file_path,f"{name}.txt",name)


        self.about.delete("1.0", tk.END)
        app.add_text_path(file_path,name,about)
        self.switch_to_frame(MainMenu)



    def upload_file(self):
        self.file_path = filedialog.askopenfilename(title="Select a file")
        file_check.check_file(self.file_path)
        if self.file_path:
            self.status_label.config(text=f"File selected: {self.file_path}")


class DeleteText(BaseFrame):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        tk.Label(self, text="Select file To be deleted").pack(pady=10)
        tk.Button(self, text="Go to Start", command=lambda: self.switch_to_frame(MainMenu)).pack(pady=10)
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
        self.combo_box['values']=values2
        self.combo_box.set('')

    def onDelete(self):
        text=self.selected_value.get()
        if(text==""):
            return
        try:
            path=app.get_text_path(text)
        except ValueError:
            messagebox.showinfo("document not find",F"documenent of name {text} was not found")
            return
        result = messagebox.askquestion("Confirmation", "Are you sure?")
        if result != 'yes':
            return
        app.remove_text_path(path)
        self.update()


class SelectToAnaliseFrame(BaseFrame):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        tk.Label(self, text="Sellect to analise").pack(pady=10)
        tk.Button(self, text="Go back to start", command=lambda: self.switch_to_frame(MainMenu)).pack(pady=10)

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

        #tk.Label(self, text="Logarithm scale").pack(pady=10)
        #vcmd = (self.register(self.allowFloat))

        #self.logScale = tk.Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        #self.logScale.pack(pady=10)


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
            messagebox.showinfo("Information", "document was not selected")
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
            if(self.amount.get()!=""):
                amount = int(self.amount.get())
            #print("Integer input:", numeric_value)
        except ValueError:
            messagebox.showinfo("Information","Invalid amount input")
            return
        logScale=0
        try:
            # Get the integer input from the StringVar
            logScale = 0
            #if (self.logScale.get() != ""):
            #    logScale = float(self.logScale.get())
            #print("Integer input:", numeric_value)
        except ValueError:
            messagebox.showinfo("Information","Invalid Logscale input")

        # this is return for file analisator it will run analises

        data={
            "path":filePath.path,
            "title":filePath.title,
            "analysisPath":f"{filePath.title}.txt",
            "about":filePath.about,
            "for_entire_text":forEntireText,
            "word1":word1,
            "word2":word2,
            "amount":amount,
            "logartihm_scale":logScale,
            "query":None
        }

        print(data["path"])

        quaryModule = cqm.QueryModule()
        output = quaryModule.call_query(data)
        print(output)
        name=output[0]
        data["query"]=output[1]
        print(output[1])

        if(name=="error"):#error mesage
            messagebox.showinfo("Information",output[1])
            return
        if(name=="search word"):

            A=self.getFrame(ForWordAnalises)
            ForWordAnalises.LoadData(A,data)
            self.switch_to_frame(ForWordAnalises)
        if(name=="sort and display"):
            A = self.getFrame(FullAnalises)
            FullAnalises.LoadData(A, data)
            self.switch_to_frame(FullAnalises)
        if(name=="search pair"):
            A = self.getFrame(SearchPairFrame)
            SearchPairFrame.LoadData(A, data)
            self.switch_to_frame(SearchPairFrame)


    def update(self):
        print('')
        values2 = self.app.getFilesTitles()
        print(values2)
        # self.selected_value = tk.StringVar()
        self.combo_box['values'] = values2
        self.combo_box.set('')


class StatsFrame(BaseFrame):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        tk.Button(self, text="Go to Start", command=lambda: self.switch_to_frame(MainMenu)).pack(pady=10)
        self.author_label = tk.Label(self, text="Author: ")
        self.author_label.pack(pady=10)

        self.title_label = tk.Label(self, text="Title: ")
        self.title_label.pack(pady=10)

        self.description_label = tk.Label(self, text="Additional description")
        self.description_label.pack(pady=10)

    def LoadData(self,data):
        #author_text = f"Author: {data.get('author', '')}"
        title_text = f"Title: {data.get('title', '')}"
        description_text = "description: "+data.get('about', ' ')

        #self.author_label.config(text=author_text)
        self.title_label.config(text=title_text)
        self.description_label.config(text=description_text)


class SearchPairFrame(StatsFrame):
    def __init__(self,app,*args,**kwargs):
        #tk.Label(self, text="Select file To be deleted").pack(pady=10)
        super().__init__(app, *args, **kwargs)
        self.resultLabel = tk.Label(self, text="Output")
        self.resultLabel.pack(pady = 10)

    def LoadData(self,data):
        resultText= f"Output: {data.get('word1', '')},{data.get('word2', '')},{data.get('query', '')}"

        self.resultLabel.config(text = resultText)
        super().LoadData(data)


#data input [[word1,word2...wordn, num],]
class Analises(StatsFrame):
    def __init__(self, app, *args, **kwargs):
        super().__init__(app, *args, **kwargs)

        self.BarChart = BarChart(self, None)
        self.BarChart.pack(side=tk.LEFT)  # Place BarChart on the left

        self.scrollable_table_frame = ScrollableTable(self, None)
        self.scrollable_table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    #arg([word,word,1])
    def LoadData(self,data):
        super().LoadData(data)
        self.data = data["query"]
        self.scrollable_table_frame.update_table(self.data)
        self.BarChart.update_chart(self.data)
        StatsFrame.LoadData(self,data)

class FullAnalises(Analises):
    def __init__(self,app, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
    def LoadData(self,data):
        super().LoadData(data)

class ForWordAnalises(Analises):
    def __init__(self,app, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.query_label = tk.Label(self, text="forWord")
        self.query_label.pack(pady=10)

    def LoadData(self,data):
        InfoText = f"Word You have chosen {data.get('word1', '')}"
        self.query_label.config(text=InfoText)
        super().LoadData(data)

class App:
    TextPathList = []
    def __init__(self, root):
        self.root = root
        self.root.title("App")

        self.frames = {}
        self.initialize_frames()

        self.TextPathList=SaveLoadSystem.load_objects_from_file('Data.pkl')
        self.TextPathList =  list(self.TextPathList.values())

        self.show_frame(MainMenu)

    def initialize_frames(self):
        self.frames[MainMenu] = MainMenu(self)
        self.frames[UploadText] = UploadText(self)
        self.frames[DeleteText] = DeleteText(self)
        self.frames[SelectToAnaliseFrame] = SelectToAnaliseFrame(self)
        self.frames[Analises]=Analises(self, None)#[{'word1': 'doorkeeper', 'word2': 'the', 'frequency': 18}, {'word1': 'man', 'word2': 'the', 'frequency': 8}, {'word1': 'his', 'word2': 'in', 'frequency': 7}, {'word1': 'law', 'word2': 'the', 'frequency': 6}, {'word1': 'am', 'word2': 'i', 'frequency': 4}, {'word1': 'of', 'word2': 'the', 'frequency': 4}])
        self.frames[SearchPairFrame]=SearchPairFrame(self)
        self.frames[FullAnalises]=FullAnalises(self)
        self.frames[ForWordAnalises]=ForWordAnalises(self)

    def show_frame(self, frame_class):
        for frame in self.frames.values():
            frame.pack_forget()

        self.frames[frame_class].update()
        self.frames[frame_class].pack()



    def add_text_path(self, path, title="", about=""):
        # Add a new TextPath instance to the list
        text_path = TextPath(path, title, about)
        self.TextPathList.append(text_path)

        SaveLoadSystem.save_objects_to_dict(self.TextPathList,'Data.pkl')

    def get_text_path(self,title):
        for path in self.TextPathList:
            if(title == path.title):
                return path
        raise ValueError

    def remove_text_path(self, textPath):
        os.remove(f'{textPath.title}.txt')
        self.TextPathList.remove(textPath)
        SaveLoadSystem.save_objects_to_dict(self.TextPathList,'Data.pkl')

    def getFilesTitles(self):
        TextPaths = self.TextPathList
        return [path.title for path in TextPaths]

    def getFrame(self,frame_class):
        return self.frames[frame_class]

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
