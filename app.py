import tkinter as tk
from tkinter import messagebox

tasks = []

def show_tasks():
    task_list.delete(0, tk.END)
    for task in tasks:
        task_list.insert(tk.END, task)

def add_task():
    task = task_entry.get()
    if task:
        tasks.append(task)
        task_entry.delete(0, tk.END)
        show_tasks()
    else:
        messagebox.showwarning("Warning", "You must enter a task.")

def delete_task():
    try:
        selected_task_index = task_list.curselection()[0]
        tasks.pop(selected_task_index)
        show_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task to delete.")

def exit_app():
    root.destroy()

root = tk.Tk()
root.title("To-Do List App")

frame = tk.Frame(root)
frame.pack(pady=10)

task_entry = tk.Entry(frame, width=50)
task_entry.pack(side=tk.LEFT, padx=10)

add_button = tk.Button(frame, text="Add Task", command=add_task)
add_button.pack(side=tk.LEFT)

task_list = tk.Listbox(root, width=50, height=10)
task_list.pack(pady=10)

delete_button = tk.Button(root, text="Delete Task", command=delete_task)
delete_button.pack(pady=5)

exit_button = tk.Button(root, text="Exit", command=exit_app)
exit_button.pack(pady=5)

root.mainloop()
