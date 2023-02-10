"""
This is a Python GUI program using the Tkinter library. It allows the user to |ch for a file or folder within a selected directory.
Discover your lost or hard-to-find files.
requirements:
    customtkinter==5.0.5
"""

# import the necessary packages
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox, ttk
import customtkinter as ctk
import threading

# set the default color scheme
ctk.set_default_color_theme("dark-blue")


def search():
    match_case = match_case_var.get()
    item_name = entry.get()
    folder_label["text"] = start_path.get()
    results = []
    progressbar["value"] = 0
    progressbar["maximum"] = 9000000
    progressbar.update()

    def calculate_max_value():
        max_value = sum(len(files) + len(dirs) for _, dirs, files in os.walk(start_path.get()))
        progressbar["maximum"] = max_value
        progressbar.update()

    calculate_thread = threading.Thread(target=calculate_max_value)
    calculate_thread.start()

    def search_item(name, path):
        nonlocal results
        listbox.delete("1.0", "end")
        counter = 0

        for root, dirs, files in os.walk(path):
            if not match_case:
                name = name.lower()
                dirs = [dir.lower() for dir in dirs]
                files = [file.lower() for file in files]

            if name in dirs + files:
                results.append(os.path.join(root, name))
                # listbox.insert(tk.END, results[-1] + "\n")
                counter += 1
                if counter % 2 == 0:
                    listbox.insert(tk.END, results[-1] + "\n", ("odd"))
                else:
                    listbox.insert(tk.END, results[-1] + "\n", ("even"))
            progressbar["value"] += len(files) + len(dirs)
            progressbar.update()

    # disable widgets

    search_button.configure(state=tk.DISABLED)
    entry.configure(state=tk.DISABLED)
    select_folder_button.configure(state=tk.DISABLED)
    match_case_checkbox.configure(state=tk.DISABLED)

    search_item(item_name, start_path.get())
    if results:
        messagebox.showinfo("Result", f"{len(results)} items found.")
    else:
        messagebox.showinfo("Result", f"Item {item_name} not found.")

    # enable widgets

    search_button.configure(state=tk.NORMAL)
    entry.configure(state=tk.NORMAL)
    select_folder_button.configure(state=tk.NORMAL)
    match_case_checkbox.configure(state=tk.NORMAL)


# selct a folder
def select_folder():
    folder = filedialog.askdirectory()
    start_path.set(folder)
    folder_label.configure(text=start_path.get())
    folder_label.update()


# create the window
root = ctk.CTk()
root.title("File/Folder Search")
root.geometry("1280x720")
root.resizable(True, True)

# variable to hold the path of the selected folder
start_path = tk.StringVar()
start_path.set(os.path.expanduser("~"))


# widgets

label = ctk.CTkLabel(master=root, text="Enter the name of the item to search for:", font=("Helvetica", 12))
entry = ctk.CTkEntry(master=root, font=("Helvetica", 12))

search_button = ctk.CTkButton(master=root, text="Search", command=search, font=("Helvetica", 12))
select_folder_button = ctk.CTkButton(master=root, text="Select Folder", command=select_folder, font=("Helvetica", 12))

listbox = ctk.CTkTextbox(root, font=("Helvetica", 14), spacing1=8, text_color="#FAD6A5")
match_case_var = tk.BooleanVar()

progressbar = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
folder_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#3f3f3f", fg="#fff")

folder_label = ctk.CTkLabel(root, text=str(os.path.expanduser("~")), font=("Helvetica", 12))
match_case_checkbox = ctk.CTkCheckBox(master=root, text="Match case", variable=match_case_var, font=("Helvetica", 12))


# tags
listbox.tag_config("odd", foreground="#FF2E63")
listbox.tag_config("even", foreground="#00ADB5")


# pack widgets
label.pack(pady=10)
entry.pack(pady=10, fill="x")
search_button.pack(pady=10)
select_folder_button.pack(pady=10)
listbox.pack(fill="both", expand=True, padx=10, pady=10)
progressbar.pack(pady=10)
folder_label.pack(pady=10)
match_case_checkbox.pack(padx=10, pady=10)

# start the program
root.mainloop()
