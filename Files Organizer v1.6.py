import os
import shutil
from datetime import datetime
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Set the appearance mode and color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

# Get the username
username = os.environ.get('USERNAME')

# Detect the working directory
working_dir = os.getcwd()

# Function to organize files by date folder
def organize_by_date(directory, org_folder_path):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            creation_date = os.path.getmtime(file_path)  # Changed getcmtime to getmtime
            date_folder = datetime.fromtimestamp(creation_date).strftime('%Y-%m-%d')
            date_folder_path = os.path.join(org_folder_path, date_folder)
            if not os.path.exists(date_folder_path):
                os.makedirs(date_folder_path)
            try:
                shutil.move(file_path, date_folder_path)
            except PermissionError:
                print(f"Permission denied for file: {filename}")

# Function to organize files by extension
def organize_by_extension(directory, org_folder_path):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_ext = os.path.splitext(filename)[1][1:]
            ext_folder_path = os.path.join(org_folder_path, file_ext)
            if not os.path.exists(ext_folder_path):
                os.makedirs(ext_folder_path)
            try:
                shutil.move(file_path, ext_folder_path)
            except PermissionError:
                print(f"Permission denied for file: {filename}")

# Create the main window
root = ctk.CTk()
root.title(f"File Organizer v1.6")

# Disable window resizing and maximizing
root.resizable(False, False)
root.attributes("-toolwindow", True)

root.geometry("360x400")  # Set the window size

# Create the main frame
main_frame = ctk.CTkFrame(root)
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

# Create the organize options frame
organize_frame = ctk.CTkFrame(main_frame)
organize_frame.pack(padx=10, pady=10, side="left", fill="both", expand=True)

# Create the version label
version_label = ctk.CTkLabel(organize_frame, text="File Organizer v1.6 by BU5HM45T3R", font=("Arial", 14), anchor="center")
version_label.pack(padx=10, pady=10)

# Create the directory to organize button
def select_directory(initial_dir):
    selected_dir = ctk.filedialog.askdirectory(initialdir=initial_dir)
    if selected_dir:
        org_dir_button.configure(text=selected_dir)

org_dir_label = ctk.CTkLabel(organize_frame, text="Directory to Organize:", anchor="center")
org_dir_label.pack(padx=10, pady=5)
org_dir_button = ctk.CTkButton(organize_frame, text="Select Folder", command=lambda: select_directory(working_dir), width=50)
org_dir_button.pack(padx=10, pady=5)

# Create the location to organize button
def select_location(initial_dir):
    selected_dir = ctk.filedialog.askdirectory(initialdir=initial_dir)
    if selected_dir:
        org_location_button.configure(text=selected_dir)

org_location_label = ctk.CTkLabel(organize_frame, text="Location to Organize:", anchor="center")
org_location_label.pack(padx=10, pady=5)
org_location_button = ctk.CTkButton(organize_frame, text="Select Folder", command=lambda: select_location(working_dir), width=50)
org_location_button.pack(padx=10, pady=5)

# Create the organizing folder name entry
org_folder_label = ctk.CTkLabel(organize_frame, text="Organizing Folder Name:", anchor="center")
org_folder_label.pack(padx=10, pady=5)
org_folder_entry = ctk.CTkEntry(organize_frame, placeholder_text="Enter folder name")
org_folder_entry.pack(padx=10, pady=5)

# Create the toggle buttons and organize button container
toggle_and_organize_frame = ctk.CTkFrame(organize_frame)
toggle_and_organize_frame.pack(padx=10, pady=10, side="bottom", fill="both", expand=True)

# Create the toggle buttons
ext_active = False
date_active = False

def toggle_ext():
    global ext_active
    ext_active = not ext_active
    if ext_active:
        ext_button.configure(fg_color="#4CAF50")
    else:
        ext_button.configure(fg_color="#F44336")

def toggle_date():
    global date_active
    date_active = not date_active
    if date_active:
        date_button.configure(fg_color="#4CAF50")
    else:
        date_button.configure(fg_color="#F44336")

ext_button = ctk.CTkButton(toggle_and_organize_frame, text="EXT", command=toggle_ext, width=50)
ext_button.grid(row=0, column=0, padx=9, pady=8)

date_button = ctk.CTkButton(toggle_and_organize_frame, text="DATE", command=toggle_date, width=50)
date_button.grid(row=0, column=1, padx=2, pady=8)

# Create the organize button
def organize_button_click():
    org_dir = org_dir_button.cget("text")
    org_location = org_location_button.cget("text")
    org_folder = org_folder_entry.get()
    org_folder_path = os.path.join(org_location, org_folder)
    if not os.path.exists(org_folder_path):
        os.makedirs(org_folder_path)
    
    if ext_active and date_active:
        organize_by_extension(org_dir, org_folder_path)
        organize_by_date(org_dir, org_folder_path)
    elif ext_active:
        organize_by_extension(org_dir, org_folder_path)
    elif date_active:
        organize_by_date(org_dir, org_folder_path)
    else:
        # Move files to the mentioned folder
        for filename in os.listdir(org_dir):
            file_path = os.path.join(org_dir, filename)
            if os.path.isfile(file_path):
                try:
                    shutil.move(file_path, org_folder_path)
                except PermissionError:
                    print(f"Permission denied for file: {filename}")

organize_button = ctk.CTkButton(toggle_and_organize_frame, text="Organize Files", command=organize_button_click, anchor="center")
organize_button.grid(row=0, column=10, padx=10, pady=8)

# Resize the window to fit the content
root.update_idletasks()
root.geometry(f"360x400")

# Run the main loop
root.mainloop()
