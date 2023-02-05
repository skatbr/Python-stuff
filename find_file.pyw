import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox, ttk
import customtkinter as ctk


def search():
    item_name = entry.get()
    folder_label["text"] = start_path.get()
    results = []
    max_value = sum(len(files) + len(dirs) for _, dirs, files in os.walk(start_path.get()))
    progressbar["maximum"] = max_value
    progressbar["value"] = 0
    progressbar.update()

    def search_item(name, path):
        nonlocal results
        listbox.delete("1.0", "end")

        for root, dirs, files in os.walk(path):
            if name in dirs + files:
                results.append(os.path.join(root, name))
                listbox.insert(tk.END, results[-1] + "\n")
            progressbar["value"] += len(files) + len(dirs)
            progressbar.update()

    search_item(item_name, start_path.get())
    if results:
        messagebox.showinfo("Result", f"{len(results)} items found.")
    else:
        messagebox.showinfo("Result", f"Item {item_name} not found.")


def update_progress():
    progressbar["value"] += 1
    progressbar.update()


def select_folder():
    folder = filedialog.askdirectory()
    start_path.set(folder)


root = ctk.CTk()
root.title("File/Folder Search")
root.geometry("500x600")
root.resizable(True, True)

start_path = tk.StringVar()
start_path.set(os.path.expanduser("~"))


label = ctk.CTkLabel(master=root, text="Enter the name of the item to search for:", font=("Helvetica", 12))
entry = ctk.CTkEntry(master=root, font=("Helvetica", 12))

search_button = ctk.CTkButton(master=root, text="Search", command=search, font=("Helvetica", 12))
select_folder_button = ctk.CTkButton(master=root, text="Select Folder", command=select_folder, font=("Helvetica", 12))
listbox = ctk.CTkTextbox(root, font=("Arial", 20))
progressbar = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
folder_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#3f3f3f", fg="#fff")
folder_label = ctk.CTkLabel(root, text=str(os.path.expanduser("~")), font=("Helvetica", 12))


label.pack(pady=10)
entry.pack(pady=10, fill="x")
search_button.pack(pady=10)
select_folder_button.pack(pady=10)
listbox.pack(fill="both", expand=True)
progressbar.pack(pady=10)
folder_label.pack(pady=10)


def fire_search(event=None):
    search()


# entry.bind("<Return>", fire_search)


root.mainloop()
