import tkinter as tk
import random
import json
import os
from tkinter import messagebox


# Load project ideas from a JSON file
def load_projects(filename):
    if not os.path.exists(filename):
        messagebox.showerror("File Not Found", f"The file {filename} does not exist.")
        return []
    with open(filename, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            messagebox.showerror("Invalid JSON", f"The file {filename} is not a valid JSON file.")
            return []

# Randomly select a project idea
def select_project():
    if not projects:
        project_label.config(text="No projects available.")
        return
    project = random.choice(projects)
    display_project(project)

# Display the selected project idea
def display_project(project):
    project_info = (
        f"Name: {project.get('name', 'No Name Provided')}\n\n"
        f"Description: {project.get('description', 'No Description Available')}\n\n"
        f"Difficulty: {project.get('difficulty', 'Not Specified')}\n\n"
        f"Allotted Time: {project.get('time_allotted', 'No Time Specified')}"
    )
    project_label.config(text=project_info)

# Add a new project idea
def add_project():
    name = name_entry.get()
    description = description_entry.get()
    difficulty = difficulty_entry.get()
    time_allotted = time_allotted_entry.get()

    if name and description and difficulty and time_allotted:
        new_project = {
            "name": name,
            "description": description,
            "difficulty": difficulty,
            "time_allotted": time_allotted
        }
        projects.append(new_project)
        save_projects('data/projects.json', projects)
        clear_entries()
        messagebox.showinfo("Success", "Project added successfully!")
    else:
        messagebox.showerror("Input Error", "All fields are required.")

# Save projects to a JSON file
def save_projects(filename, projects):
    with open(filename, 'w') as file:
        json.dump(projects, file, indent=4)

# Clear entry fields
def clear_entries():
    name_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    difficulty_entry.delete(0, tk.END)
    time_allotted_entry.delete(0, tk.END)

# Initialize the GUI
app = tk.Tk()
app.title("Random Project Selector")

# Load projects from JSON file
projects = load_projects('data/projects.json')

# Project Display Section
project_label = tk.Label(app, text="", font=("Helvetica", 14), wraplength=400)
project_label.pack(pady=20)

# Button to select a project
select_button = tk.Button(app, text="Select a Project", command=select_project)
select_button.pack(pady=10)

# Section to add new projects
tk.Label(app, text="Add New Project", font=("Helvetica", 16)).pack(pady=10)

tk.Label(app, text="Project:").pack()
name_entry = tk.Entry(app)
name_entry.pack()

tk.Label(app, text="Description:").pack()
description_entry = tk.Entry(app)
description_entry.pack()

tk.Label(app, text="Difficulty:").pack()
difficulty_entry = tk.Entry(app)
difficulty_entry.pack()

tk.Label(app, text="Allotted Time:").pack()
time_allotted_entry = tk.Entry(app)
time_allotted_entry.pack()

add_button = tk.Button(app, text="Add Project", command=add_project)
add_button.pack(pady=10)

app.mainloop()
