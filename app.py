import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import json
import os
from datetime import datetime

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
    show_tasks()  # Auto-refresh the list after saving

# Show tasks in listbox with filter
def show_tasks():
    task_list.delete(0, tk.END)
    filter_option = filter_var.get()
    search_text = search_entry.get().lower()

    for task in sorted(tasks, key=lambda x: (x["priority"], x["due_date"])):
        if filter_option == "Completed" and not task["completed"]:
            continue
        elif filter_option == "Pending" and task["completed"]:
            continue
        if search_text and search_text not in task["text"].lower():
            continue

        display_text = f"[✓] {task['text']} (Due: {task['due_date']}, Priority: {task['priority']})" if task['completed'] else f"[ ] {task['text']} (Due: {task['due_date']}, Priority: {task['priority']})"
        task_list.insert(tk.END, display_text)

    check_due_dates()

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
    else:
        messagebox.showwarning("Warning", "Enter a task and due date.")

# Delete a selected task
def delete_task():
    try:
        selected_index = task_list.curselection()[0]
        del tasks[selected_index]
        save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task to delete.")

# Toggle task completion
def toggle_task():
    try:
        selected_index = task_list.curselection()[0]
        tasks[selected_index]["completed"] = not tasks[selected_index]["completed"]
        save_tasks()
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
        else:
            messagebox.showwarning("Warning", "Enter task text and due date before editing.")
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task to edit.")

# Search tasks
def search_task():
    show_tasks()

# Export tasks to text file
def export_tasks():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            for task in tasks:
                status = "✓" if task["completed"] else "✗"
                file.write(f"{status} {task['text']} | Due: {task['due_date']} | Priority: {task['priority']}\n")
        messagebox.showinfo("Export", "Tasks exported successfully!")

# Import tasks from JSON
def import_tasks():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, "r") as file:
            global tasks
            tasks = json.load(file)
        save_tasks()

# Check for overdue tasks
def check_due_dates():
    today = datetime.today().strftime('%Y-%m-%d')
    for task in tasks:
        if not task["completed"] and task["due_date"] <= today:
            messagebox.showwarning("Task Due Alert", f"Task '{task['text']}' is due!")

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
root.title("Ultimate To-Do List App")
root.geometry("600x550")

frame = tk.Frame(root)
frame.pack(pady=10)

task_entry = tk.Entry(frame, width=30)
task_entry.pack(side=tk.LEFT, padx=5)

due_date_entry = tk.Entry(frame, width=15)
due_date_entry.pack(side=tk.LEFT, padx=5)
due_date_entry.insert(0, "YYYY-MM-DD")

priority_var = tk.StringVar(value="Medium")
priority_menu = ttk.Combobox(frame, textvariable=priority_var, values=["High", "Medium", "Low"], width=8)
priority_menu.pack(side=tk.LEFT, padx=5)

add_button = tk.Button(frame, text="Add Task", command=add_task)
add_button.pack(side=tk.LEFT)

task_list = tk.Listbox(root, width=70, height=12)
task_list.pack(pady=10)

delete_button = tk.Button(root, text="Delete Task", command=delete_task)
delete_button.pack(pady=5)

toggle_button = tk.Button(root, text="Mark as Done/Undone", command=toggle_task)
toggle_button.pack(pady=5)

edit_button = tk.Button(root, text="Edit Task", command=edit_task)
edit_button.pack(pady=5)

# Search bar
search_frame = tk.Frame(root)
search_frame.pack(pady=5)
search_entry = tk.Entry(search_frame, width=30)
search_entry.pack(side=tk.LEFT, padx=5)
search_button = tk.Button(search_frame, text="Search", command=search_task)
search_button.pack(side=tk.LEFT)

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

# Export & Import buttons
export_button = tk.Button(root, text="Export Tasks", command=export_tasks)
export_button.pack(pady=5)

import_button = tk.Button(root, text="Import Tasks", command=import_tasks)
import_button.pack(pady=5)

exit_button = tk.Button(root, text="Exit", command=exit_app)
exit_button.pack(pady=5)

load_tasks()
root.mainloop()
