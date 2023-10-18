import tkinter as tk
from tkinter import *
from customtkinter import CTkButton
import PyPDF2
import latex2sympy2
import numpy as np

#drag and drop list on the left side of the main UI
class DragDropListbox(tk.Listbox):
    def __init__(self, master, **kw):
        tk.Listbox.__init__(self, master, **kw)
        self.bind("<ButtonPress-1>", self.onStart)
        self.bind("<B1-Motion>", self.onDrag)
        self.curIndex = None

    def onStart(self, event):
        self.curIndex = self.nearest(event.y)
    #reordering by dragging different files
    def onDrag(self, event):
        newIndex = self.nearest(event.y)
        if self.curIndex != newIndex:
            x = self.get(self.curIndex)
            self.delete(self.curIndex)
            self.insert(newIndex, x)
            self.curIndex = newIndex
#currently grabs the file path and name
def open_file():
    filepath = tk.filedialog.askopenfilename()
    with open(filepath, "r") as fil:
        quest = []
        for ln in fil:
            if ln.startswith("\q") or ln.startswith("("):
                
                quest.append(ln[1:])
    ques = np.array(quest)
    que = np.char.replace(ques, '\\', ' ')
    que = np.char.replace(que, ',', ' ')
    que = np.char.replace(que, '$', ' ')
    que = np.char.strip(que)
    print(que)
    #print(tes)
    #print(que)
    if filepath:
        for x in que:
            file_list.insert(tk.END, x)
#currently only for the header content changes
def apply_changes_to_canvas(header_content_text):
    # Retrieve content from the Text widget
    content = header_content_text.get("1.0", "end-1c")
    
    # Display content on the canvas (assuming sidebar2_canvas is globally accessible)
    sidebar2_canvas.delete("header_content")  # Remove previous content if any
    sidebar2_canvas.create_text(800, 50, text=content, fill="black", font=('Helvetica 12'), tags=("header_content"))

#replace the text in the list with new text
def replaceQues(change):
    for item in file_list.curselection():
        file_list.delete(item)
        file_list.insert(item, change)
        
def edit_Question():
    # Create a new window
    question_win = Toplevel(root)
    question_win.title("Edit Question")
    question_win.geometry("650x100")
    
    #Edit Question Text
    p = Label(question_win, text = "Edit Question:").place(relx=0.5, rely=.2, anchor='s') 
    t = Text(question_win, height = 1, width = 80)
    t.place(relx=0.5, rely=0.5, anchor='s')
    t.insert(END, file_list.get(ANCHOR))
    
    #Button to add the new text
    add_text_button = Button(question_win, text="Apply", command=lambda: replaceQues(t.get(1.0, END)))
    add_text_button.place(relx=0.5, rely=.8, anchor='s')   
    
    
def add_text():
    print("adding text")

def edit_header():
    # Create a new window
    header_window = Toplevel(root)
    header_window.title("Edit Header")
    header_window.geometry("450x250")

    #Title input is here now 
    Label(header_window, text="Title:").grid(row=0, column=0, padx=10, pady=5)
    k = Entry(header_window).grid(row=0, column=1, padx=10, pady=5)
    
    # Add widgets for adding their own name, class, and date
    Label(header_window, text="Header Content:").grid(row=1, column=0, padx=10, pady=5)
    header_content_text = tk.Text(header_window, height=5, width=30)  # Adjust height and width as needed
    header_content_text.grid(row=1, column=1, padx=10, pady=5)

    # Checkbutton for page numbering
    page_number_var = StringVar()
    Checkbutton(header_window, text="Add Page Numbering", variable=page_number_var, onvalue="Yes", offvalue="No").grid(row=4, columnspan=2, padx=10, pady=10)  
    
    btn_apply_changes = Button(header_window, text="Apply Changes", command=(apply_changes_to_canvas(header_content_text)))
    btn_apply_changes.grid(row=2, column=0, columnspan=2, pady=10)


root = tk.Tk()
root.title("Kappa Editor")

# Set the height and width of the app to the size of the screen
winWidth = root.winfo_screenwidth()
winHeight = root.winfo_screenheight()
root.geometry("%dx%d" % (winWidth-100, winHeight-100))
#create canvas for the display of the text entered
root.grid_rowconfigure(1, weight=1)  # This gives extra vertical space to the second row (index 1)
root.grid_columnconfigure(1, weight=1)  # This gives extra horizontal space to the second column (index 1)
sidebar2_canvas = Canvas(root, width = winWidth - 250, height=1, highlightbackground="grey", highlightthickness=1, bg="white")
sidebar2_canvas.grid(rowspan=2, column=1, pady= 5, padx=5, sticky="nse")

# Top bar menu
menu = Menu(root)
root.config(menu=menu)

# Top bar menu
main_menu = Menu(root)
root.config(menu=main_menu)

# File menu
file_menu = Menu(main_menu, tearoff=0)  # tearoff=0 removes the dashed line at the top of the menu
file_menu.add_command(label="Open", command=open_file)  # Replace with your function
file_menu.add_command(label="Save", command=None)  # Replace with your function
file_menu.add_command(label="Exit", command=root.quit)
main_menu.add_cascade(label="File", menu=file_menu)

# Edit menu
edit_menu = Menu(main_menu, tearoff=0)
edit_menu.add_command(label="Undo", command=None)  # Replace with undo
edit_menu.add_command(label="Redo", command=None)  # Replace with redo
edit_menu.add_command(label="header", command=edit_header) # Replace with header editer
main_menu.add_cascade(label="Edit", menu=edit_menu)

# Initialization of left-side sidebar
sidebar_frame = tk.Frame(root, bg="grey")
sidebar_frame.grid(row=0, column=0, sticky="ns")



# Method that sets up the title
def Get_Title():
    INPUT = inputTitle.get("1.0", "end-1c")
    sidebar2_canvas.delete("Title")
    sidebar2_canvas.create_text(800, 50, text=INPUT, fill="black", font=('Helvetica 24 bold'), tags=("Title"))

# Input textbox for the title
# inputTitle = Text(root, height=1, width=15, highlightbackground="grey", highlightthickness=1, bg="white")
# inputTitle.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")

# Button to Add Title to the canvas
Display = Button(root, text="Insert Title", command=lambda: Get_Title())
Display.grid(row=2, column=0, columnspan=2, pady=10)

file_list = DragDropListbox(sidebar_frame, exportselection=False)
file_list.grid(row=1, column=0, columnspan=2, sticky="nsew")

def deleteQues():
    file_list.delete(ANCHOR)
        
    
add_file_button = CTkButton(sidebar_frame, text="Add File", command=open_file)
add_file_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

add_text_button = CTkButton(sidebar_frame, text="Add Text", command='')  # Replace '' with the desired command
add_text_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")

deleteQuestionButt = CTkButton(sidebar_frame, text="Delete", command=deleteQues)
deleteQuestionButt.grid(row=2, column=0, padx=5, pady=5, sticky="w")

editQuestionButt = CTkButton(sidebar_frame, text="Edit Question", command=edit_Question)
editQuestionButt.grid(row=2, column=1, padx=5, pady=5, sticky="w")



# Configure the rows and columns for resizing
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
sidebar_frame.grid_rowconfigure(1, weight=1)
sidebar_frame.grid_columnconfigure(0, weight=1)
sidebar_frame.grid_columnconfigure(1, weight=1)

root.mainloop()

# def exit_program():
#     root.destroy()

# root = tk.Tk()
# root.title("Kappa Editor")
# #sets the hight and width of the app to size of screen
# #ignores taskbar for some reason, can't figure out an easy fix
# winWidth = root.winfo_screenwidth()
# winHeight = root.winfo_screenheight()
# root.geometry("%dx%d" % (winWidth, winHeight))
# #top bar menu
# menu = Menu(root)
# root.config(menu=menu)
# #file button of top menu
# file_menu = Menu(menu)
# menu.add_cascade(label="File", menu=file_menu)
# file_menu.add_command(label="Open", command=open_file)
# file_menu.add_command(label="Exit", command=exit_program)
# #insert button
# insert_menu = Menu(menu)
# menu.add_cascade(label="Insert", menu=insert_menu)
# #view button
# view_menu = Menu(menu)
# menu.add_cascade(label="View", menu=view_menu)
# #help button
# help_menu = Menu(menu)
# menu.add_cascade(label="Help", menu=help_menu)

# #initialization of leftside side bar
# sidebar_frame = tk.Frame(root, width=100, height=50, bg="grey")
# sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)


# #frame for where the exam you are making will be displayed
# #we can adjust this later i just figured a bounding box would help


# #Method that sets up the title
# def Get_Title():
#     INPUT = inputTitle.get("1.0", "end-1c")
#     sidebar2_canvas.delete("Title")
#     sidebar2_canvas.create_text(800, 50, text=INPUT, fill="black", font=('Helvetica 24 bold'), tags=("Title"))

# #Input textbox for the title
# inputTitle = Text(root, height = 1,width = 15, highlightbackground="grey", highlightthickness=1, bg = "white")
# inputTitle.pack(pady= 10)
# inputTitle.pack()
# #Button to Add Title to the canvas
# Display = Button(root, height = 1, width = 15, text ="Insert Title",command = lambda:Get_Title())
# Display.pack()

# file_list = DragDropListbox(sidebar_frame)
# #file_list.pack(fill=tk.BOTH, expand=1)
# file_list.grid(row=1, column=0, columnspan=2, sticky="nsew")
# add_file_button = CTkButton(sidebar_frame, text="Add File", command=open_file)
# add_file_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")
# add_text_button = CTkButton(sidebar_frame, text="Add Text", command='')  # Replace 'your_command_here' with the desired command
# add_text_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")

# root.mainloop()
