import sqlite3
import tkinter
from tkinter import *
import math

# Initialize the database
def initialize_db():
    conn = sqlite3.connect('Todolist.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                      id INTEGER PRIMARY KEY,
                      task TEXT NOT NULL,
                      status TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Load tasks from the database
def load_tasks():
    conn = sqlite3.connect('Todolist.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

# Add a new task to the database
def add_task_to_db(task):
    conn = sqlite3.connect('Todolist.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task, status) VALUES (?, ?)", (task, 'pending'))
    conn.commit()
    conn.close()

# Delete a task from the database
def delete_task_from_db(task):
    conn = sqlite3.connect('Todolist.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE task = ?", (task,))
    conn.commit()
    conn.close()

# Initialize the database
initialize_db()

el = Tk()
el.title("To-Do List")
el.geometry("400x650+400+100")
el.resizable(False, False)

task_list = []

def openTaskFile():
    global task_list
    tasks = load_tasks()
    for task in tasks:
        task_list.append(task[1])
        listbox.insert(END, task[1])

def addTask():
    task = task_entry.get()
    task_entry.delete(0, END)
    if task:
        add_task_to_db(task)
        task_list.append(task)
        listbox.insert(END, task)

def deleteTask():
    global task_list
    task = str(listbox.get(ANCHOR))
    if task in task_list:
        task_list.remove(task)
        delete_task_from_db(task)
        listbox.delete(ANCHOR)

# Icon for the Bar
icon = PhotoImage(file="Image/icon1.png")
el.iconphoto(False, icon)

# Top Bar
TopImage = PhotoImage(file="Image/Topbar1.png")
Label(el, image=TopImage).pack()

# Add task
addtask = PhotoImage(file="Image/addtask1.png")
Label(el, image=addtask).pack(pady=(20, 10))

# Main
frame = Frame(el, width=400, height=50, bg='white')
frame.place(x=0, y=180)

task = StringVar()
task_entry = Entry(frame, width=18, font="Alice 15", bd=0)
task_entry.place(x=10, y=7)
task_entry.focus()

button = Button(frame, text="Add", font="Anton 17 bold", width=6, bg="coral", fg="#fff", bd=0, command=addTask)
button.place(x=305, y=4)

# ListBox
frame1 = Frame(el, bd=3, width=700, height=280, bg="lightcoral")
frame1.pack(pady=(90, 0))

listbox = Listbox(frame1, font=("Anton", 12), width=40, height=16, bg="#32405b", fg="white", cursor="hand2", selectbackground="#5a95ff")
listbox.pack(side=LEFT, fill=BOTH, padx=2)

scrollbar = Scrollbar(frame1)
scrollbar.pack(side=RIGHT, fill=BOTH)

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

openTaskFile()

# Delete
Delete_icon = PhotoImage(file="Image/delete1.png")
Button(el, image=Delete_icon, bd=0, command=deleteTask).pack(side=BOTTOM, pady=13)

el.mainloop()
