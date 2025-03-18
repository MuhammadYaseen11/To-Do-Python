import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

tasks = []

# Load tasks from file
def load_tasks():
    global tasks
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
    show_tasks()

# Save tasks to file
def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)

# Show tasks in listbox based on filter
def show_tasks():
    task_list.delete(0, tk.END)
    filter_option = filter_var.get()

    for i, task in enumerate(tasks):
        if filter_option == "Completed" and not task["completed"]:
            continue
        elif filter_option == "Pending" and task["completed"]:
            continue

        display_text = f"[✓] {task['text']} (Due: {task['due_date']}, Priority: {task['priority']})" if task['completed'] else f"[ ] {task['text']} (Due: {task['due_date']}, Priority: {task['priority']})"
        task_list.insert(tk.END, display_text)

# Add a new task
def add_task():
    task_text = task_entry.get()
    due_date = due_date_entry.get()
    priority = priority_var.get()

    if task_text and due_date:
        tasks.append({"text": task_text, "completed": False, "due_date": due_date, "priority": priority})
        task_entry.delete(0, tk.END)
        due_date_entry.delete(0, tk.END)
        save_tasks()
        show_tasks()
    else:
        messagebox.showwarning("Warning", "Enter a task and due date.")

# Delete a selected task
def delete_task():
    try:
        selected_index = task_list.curselection()[0]
        del tasks[selected_index]
        save_tasks()
        show_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task to delete.")

# Toggle task completion
def toggle_task():
    try:
        selected_index = task_list.curselection()[0]
        tasks[selected_index]["completed"] = not tasks[selected_index]["completed"]
        save_tasks()
        show_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task.")

# Edit a selected task
def edit_task():
    try:
        selected_index = task_list.curselection()[0]
        new_task_text = task_entry.get()
        new_due_date = due_date_entry.get()
        new_priority = priority_var.get()

        if new_task_text and new_due_date:
            tasks[selected_index]["text"] = new_task_text
            tasks[selected_index]["due_date"] = new_due_date
            tasks[selected_index]["priority"] = new_priority
            task_entry.delete(0, tk.END)
            due_date_entry.delete(0, tk.END)
            save_tasks()
            show_tasks()
        else:
            messagebox.showwarning("Warning", "Enter task text and due date before editing.")
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task to edit.")

# Change theme
def toggle_theme():
    if theme_var.get() == "Dark":
        root.config(bg="black")
        task_list.config(bg="black", fg="white")
    else:
        root.config(bg="white")
        task_list.config(bg="white", fg="black")

# Exit the app
def exit_app():
    root.destroy()

# UI Setup
root = tk.Tk()
root.title("Advanced To-Do List App")
root.geometry("500x500")

frame = tk.Frame(root)
frame.pack(pady=10)

task_entry = tk.Entry(frame, width=30)
task_entry.pack(side=tk.LEFT, padx=5)

due_date_entry = tk.Entry(frame, width=20)
due_date_entry.pack(side=tk.LEFT, padx=5)
due_date_entry.insert(0, "Insert Dua Day/Time")

priority_var = tk.StringVar(value="Medium")
priority_menu = ttk.Combobox(frame, textvariable=priority_var, values=["High", "Medium", "Low"], width=8)
priority_menu.pack(side=tk.LEFT, padx=5)

add_button = tk.Button(frame, text="Add Task", command=add_task)
add_button.pack(side=tk.LEFT)

task_list = tk.Listbox(root, width=60, height=10)
task_list.pack(pady=10)

delete_button = tk.Button(root, text="Delete Task", command=delete_task)
delete_button.pack(pady=5)

toggle_button = tk.Button(root, text="Mark as Done/Undone", command=toggle_task)
toggle_button.pack(pady=5)

edit_button = tk.Button(root, text="Edit Task", command=edit_task)
edit_button.pack(pady=5)

# Filter dropdown
filter_var = tk.StringVar(value="All")
filter_menu = ttk.Combobox(root, textvariable=filter_var, values=["All", "Completed", "Pending"])
filter_menu.pack(pady=5)
filter_menu.bind("<<ComboboxSelected>>", lambda e: show_tasks())

# Theme Toggle
theme_var = tk.StringVar(value="Light")
theme_toggle = ttk.Combobox(root, textvariable=theme_var, values=["Light", "Dark"])
theme_toggle.pack(pady=5)
theme_toggle.bind("<<ComboboxSelected>>", lambda e: toggle_theme())

exit_button = tk.Button(root, text="Exit", command=exit_app)
exit_button.pack(pady=5)

load_tasks()
root.mainloop()
