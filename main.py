import tkinter as tk
from tkinter import filedialog, messagebox
import random
import json
import os
import sys
import re


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


# Function to handle loading a file
def load_file():
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=(("JSON files", "*.json"), ("All files", "*.*")),
        initialdir=os.path.join(os.getcwd(), "data")  # Default to the "data" folder
    )
    if file_path:
        global projects
        projects = load_projects(file_path)
        if projects:
            start_main_app()


# Function to handle creating a new file
def create_file():
    new_window = tk.Toplevel(app)
    new_window.title("Create New File")
    new_window.protocol("WM_DELETE_WINDOW", lambda: on_closing(new_window))  # Handle close event


# Function to display the startup prompt
def startup_prompt():
    prompt_window = tk.Toplevel(app)
    prompt_window.title("Welcome")

    tk.Label(prompt_window, text="What would you like to do?", font=("Helvetica", 14)).pack(pady=20)

    load_button = tk.Button(prompt_window, text="Load a File", command=load_file)
    load_button.pack(pady=10)

    create_button = tk.Button(prompt_window, text="Create a File", command=create_file)
    create_button.pack(pady=10)

    prompt_window.protocol("WM_DELETE_WINDOW", lambda: on_closing(prompt_window))  # Handle close event


# Start the main application (This function is called after loading projects)
def start_main_app():
    global project_label, name_entry, description_entry, difficulty_entry, time_allotted_entry

    main_window = tk.Toplevel(app)
    main_window.title("Random Project Selector")

    # Project Display Section
    project_label = tk.Label(main_window, text="", font=("Helvetica", 14), wraplength=400)
    project_label.pack(pady=20)

    # Button to select a project
    select_button = tk.Button(main_window, text="Select a Project", command=select_project)
    select_button.pack(pady=10)

    # Section to add new projects
    tk.Label(main_window, text="Add New Project", font=("Helvetica", 16)).pack(pady=10)

    tk.Label(main_window, text="Project:").pack()
    name_entry = tk.Entry(main_window)
    name_entry.pack()

    tk.Label(main_window, text="Description:").pack()
    description_entry = tk.Entry(main_window)
    description_entry.pack()

    tk.Label(main_window, text="Difficulty (integer):").pack()
    difficulty_entry = tk.Entry(main_window)
    difficulty_entry.pack()

    tk.Label(main_window, text="Allotted Time (decimal hours):").pack()
    time_allotted_entry = tk.Entry(main_window)
    time_allotted_entry.pack()

    add_button = tk.Button(main_window, text="Add Project", command=add_project)
    add_button.pack(pady=10)

    main_window.protocol("WM_DELETE_WINDOW", lambda: on_closing(main_window))  # Handle close event


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
    name = name_entry.get().strip()
    description = description_entry.get().strip()
    try:
        difficulty = int(difficulty_entry.get().strip())
        time_allotted = float(time_allotted_entry.get().strip())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for Difficulty and Allotted Time.")
        return

    # Validate the input fields
    if not name:
        messagebox.showerror("Input Error", "Project name cannot be empty.")
        return
    if not description:
        messagebox.showerror("Input Error", "Project description cannot be empty.")
        return
    if difficulty <= 0:
        messagebox.showerror("Input Error", "Difficulty must be a positive integer.")
        return
    if time_allotted <= 0:
        messagebox.showerror("Input Error", "Allotted time must be a positive number.")
        return

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


# Save projects to a JSON file
def save_projects(filename, projects):
    with open(filename, 'w') as file:
        json.dump(projects, file, indent=4)


# Function to handle creating a new file
def create_file():
    new_window = tk.Toplevel(app)
    new_window.title("Create New JSON File")

    tk.Label(new_window, text="Enter file name: ").pack(pady=10)
    file_name_entry = tk.Entry(new_window)
    file_name_entry.pack(pady=5)

    create_button = tk.Button(new_window, text="Create File", command=lambda: save_new_file(file_name_entry.get(), new_window))
    create_button.pack(pady=20)

    new_window.protocol("WM_DELETE_WINDOW", lambda: on_closing(new_window))  # Handle close event


# Function to validate file name
def validate_file_name(file_name):
    if not file_name:
        return False
    # Only allow alphanumeric characters and underscores in file names
    if not re.match(r'^[\w-]+$', file_name):
        return False
    return True


# Function to save the new file with a template
def save_new_file(file_name, window):
    # Validate the file name
    if not validate_file_name(file_name):
        messagebox.showerror("Invalid File Name", "File name must be alphanumeric and cannot contain special characters.")
        return

    # Ensure the file is saved in the "data" directory
    directory = os.path.join(os.getcwd(), "data")
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, f"{file_name}.json")

    # Automatically generate a basic template (e.g., an empty list)
    json_template = []

    # Write to the file securely
    try:
        with open(file_path, 'w') as file:
            json.dump(json_template, file, indent=4)
        messagebox.showinfo("Success", f"File '{file_name}.json' created successfully!")
        window.destroy()
    except Exception as e:
        messagebox.showerror("File Creation Error", f"An error occurred while creating the file: {e}")


# Clear entry fields
def clear_entries():
    name_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    difficulty_entry.delete(0, tk.END)
    time_allotted_entry.delete(0, tk.END)


# Function to handle window close event
def on_closing(window):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()
        if not any([isinstance(widget, tk.Toplevel) for widget in app.winfo_children()]):
            sys.exit()  # Ensure the program exits completely if all windows are closed


# Initialize the main Tkinter window
app = tk.Tk()
app.withdraw()  # Hide the root window

# Start the startup prompt
startup_prompt()

app.protocol("WM_DELETE_WINDOW", lambda: on_closing(app))  # Handle close event for the hidden root window

app.mainloop()
