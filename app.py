import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from tkcalendar import DateEntry  # Import DateEntry
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
    selected_index = None
    try:
        selected_index = task_list.curselection()[0]
    except IndexError:
        pass  # No task selected, nothing to track

    task_list.delete(0, tk.END)
    filter_option = filter_var.get()
    search_text = search_entry.get().lower()

    # Priority mapping to numeric values for correct sorting
    priority_map = {"High": 1, "Medium": 2, "Low": 3}

    for index, task in enumerate(sorted(tasks, key=lambda x: (priority_map.get(x["priority"], 2), x["due_date"]))):
        if filter_option == "Completed" and not task["completed"]:
            continue
        elif filter_option == "Pending" and task["completed"]:
            continue
        if search_text and search_text not in task["text"].lower():
            continue

        display_text = f"[✓] {task['text']} (Due: {task['due_date']}, Priority: {task['priority']})" if task['completed'] else f"[ ] {task['text']} (Due: {task['due_date']}, Priority: {task['priority']})"
        task_list.insert(tk.END, display_text)

    if selected_index is not None and selected_index < task_list.size():
        task_list.select_set(selected_index)  # Re-select the previously selected task

# Add a new task
def add_task():
    task_text = task_entry.get()
    due_date = due_date_entry.get_date()  # Get the selected date from the calendar widget
    priority = priority_var.get()

    if task_text and due_date:
        tasks.append({"text": task_text, "completed": False, "due_date": due_date.strftime('%Y-%m-%d'), "priority": priority})
        task_entry.delete(0, tk.END)
        due_date_entry.set_date(datetime.today())  # Reset the date picker to today after adding the task
        save_tasks()
        animate_button(add_button)  # Add animation when adding a task
    else:
        messagebox.showwarning("Warning", "Enter a task and due date.")

# Delete a selected task
def delete_task():
    try:
        selected_index = task_list.curselection()[0]
        task_text = task_list.get(selected_index).split("] ")[1].split(" (Due:")[0]
        for task in tasks:
            if task["text"] == task_text:
                tasks.remove(task)
                break
        save_tasks()  # Save the updated task list
        animate_button(delete_button)  # Add animation on task delete
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task to delete.")

# Toggle task completion
def toggle_task():
    try:
        selected_index = task_list.curselection()[0]
        task_text = task_list.get(selected_index).split("] ")[1].split(" (Due:")[0]
        for task in tasks:
            if task["text"] == task_text:
                task["completed"] = not task["completed"]  # Toggle completion status
                break
        save_tasks()  # Save the updated task list
        animate_button(toggle_button)  # Add animation on task toggle
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task.")

# Edit a selected task
def edit_task():
    try:
        selected_index = task_list.curselection()[0]
        task_text = task_list.get(selected_index).split("] ")[1].split(" (Due:")[0]
        new_task_text = task_entry.get()
        new_due_date = due_date_entry.get_date()  # Get the selected date from the calendar widget
        new_priority = priority_var.get()

        if new_task_text and new_due_date:
            for task in tasks:
                if task["text"] == task_text:
                    task["text"] = new_task_text
                    task["due_date"] = new_due_date.strftime('%Y-%m-%d')
                    task["priority"] = new_priority
                    break
            task_entry.delete(0, tk.END)
            due_date_entry.set_date(datetime.today())  # Reset the date picker to today after editing the task
            save_tasks()
            animate_button(edit_button)  # Add animation when editing a task
        else:
            messagebox.showwarning("Warning", "Enter task text and due date before editing.")
    except IndexError:
        messagebox.showwarning("Warning", "You must select a task to edit.")

# Search tasks
def search_task():
    show_tasks()

# Export tasks to a text file with UTF-8 encoding
def export_tasks():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as file:  # Ensure UTF-8 encoding
                for task in tasks:
                    status = "✔" if task["completed"] else "✘"  # Alternative symbols
                    file.write(f"{status} {task['text']} | Due: {task['due_date']} | Priority: {task['priority']}\n")
            messagebox.showinfo("Export", "Tasks exported successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export tasks: {e}")

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
    overdue_tasks = []
    for task in tasks:
        if not task["completed"] and task["due_date"] <= today:
            overdue_tasks.append(task)
    
    if overdue_tasks:
        task_texts = [task['text'] for task in overdue_tasks]
        messagebox.showwarning("Task Due Alert", f"The following tasks are due: \n" + "\n".join(task_texts))

    show_tasks()  # Refresh the list after showing the alert

# Change theme
def toggle_theme():
    if theme_var.get() == "Dark":
        root.config(bg="#2E2E2E")
        task_list.config(bg="#2E2E2E", fg="white")
        for widget in root.winfo_children():
            if isinstance(widget, tk.Button) or isinstance(widget, ttk.Combobox):
                widget.config(bg="#444444", fg="white")
    else:
        root.config(bg="white")
        task_list.config(bg="white", fg="black")
        for widget in root.winfo_children():
            if isinstance(widget, tk.Button) or isinstance(widget, ttk.Combobox):
                widget.config(bg="#F0F0F0", fg="black")

# Animate button press
def animate_button(button):
    button.config(bg="#4CAF50", fg="white")
    root.after(100, lambda: button.config(bg="#5F6368", fg="white"))

# Exit the app
def exit_app():
    root.destroy()

# UI Setup
root = tk.Tk()
root.title("Ultimate To-Do List App")
root.geometry("800x800")
root.config(bg="white")

frame = tk.Frame(root, bg="white")
frame.pack(pady=10)

task_entry = tk.Entry(frame, width=30, font=("Arial", 12), bd=2, relief="solid")
task_entry.pack(side=tk.LEFT, padx=5)

# Use DateEntry widget for selecting date
due_date_entry = DateEntry(frame, width=15, date_pattern="yyyy-mm-dd", font=("Arial", 12))
due_date_entry.pack(side=tk.LEFT, padx=5)
due_date_entry.set_date(datetime.today())  # Set the default date to today

priority_var = tk.StringVar(value="Medium")
priority_menu = ttk.Combobox(frame, textvariable=priority_var, values=["High", "Medium", "Low"], width=8, font=("Arial", 12))
priority_menu.pack(side=tk.LEFT, padx=5)

add_button = tk.Button(frame, text="Add Task", command=add_task, font=("Arial", 12), bg="#5F6368", fg="white", relief="solid", bd=2)
add_button.pack(side=tk.LEFT, padx=5)

task_list = tk.Listbox(root, width=70, height=12, font=("Arial", 12), bd=2, relief="solid")
task_list.pack(pady=10)

delete_button = tk.Button(root, text="Delete Task", command=delete_task, font=("Arial", 12), bg="#FF5733", fg="white", relief="solid", bd=2)
delete_button.pack(pady=5)

toggle_button = tk.Button(root, text="Mark as Done/Undone", command=toggle_task, font=("Arial", 12), bg="#FF8C00", fg="white", relief="solid", bd=2)
toggle_button.pack(pady=5)

edit_button = tk.Button(root, text="Edit Task", command=edit_task, font=("Arial", 12), bg="#1E88E5", fg="white", relief="solid", bd=2)
edit_button.pack(pady=5)

# Search bar
search_frame = tk.Frame(root, bg="white")
search_frame.pack(pady=5)
search_entry = tk.Entry(search_frame, width=30, font=("Arial", 12), bd=2, relief="solid")
search_entry.pack(side=tk.LEFT, padx=5)
search_button = tk.Button(search_frame, text="Search", command=search_task, font=("Arial", 12), bg="#42A5F5", fg="white", relief="solid", bd=2)
search_button.pack(side=tk.LEFT)

# Filter dropdown
filter_var = tk.StringVar(value="All")
filter_menu = ttk.Combobox(root, textvariable=filter_var, values=["All", "Completed", "Pending"], font=("Arial", 12))
filter_menu.pack(pady=5)
filter_menu.bind("<<ComboboxSelected>>", lambda e: show_tasks())

# Theme Toggle
theme_var = tk.StringVar(value="Light")
theme_toggle = ttk.Combobox(root, textvariable=theme_var, values=["Light", "Dark"], font=("Arial", 12))
theme_toggle.pack(pady=5)
theme_toggle.bind("<<ComboboxSelected>>", lambda e: toggle_theme())

# Export & Import buttons
export_button = tk.Button(root, text="Export Tasks", command=export_tasks, font=("Arial", 12), bg="#4CAF50", fg="white", relief="solid", bd=2)
export_button.pack(pady=5)

import_button = tk.Button(root, text="Import Tasks", command=import_tasks, font=("Arial", 12), bg="#FFC107", fg="white", relief="solid", bd=2)
import_button.pack(pady=5)

exit_button = tk.Button(root, text="Exit", command=exit_app, font=("Arial", 12), bg="#9E9E9E", fg="white", relief="solid", bd=2)
exit_button.pack(pady=5)

load_tasks()
root.mainloop()