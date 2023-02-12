"""
a multi-threaded GUI file downloader with a custom theme. 
It splits the file into segments for faster downloading.
requirements:
    customtkinter==5.0.5
    requests==2.28.2
    tqdm==4.64.1
"""

import requests
import os
import math
import concurrent.futures
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tqdm import tqdm
import customtkinter as ctk

ctk.set_default_color_theme("green")


def download_piece(url, piece_number, piece_size, file_name):
    start = piece_size * piece_number
    end = piece_size * (piece_number + 1) - 1
    headers = {"Range": f"bytes={start}-{end}"}
    response = requests.get(url, headers=headers, stream=True)

    total_size = int(response.headers.get("Content-Length", 0))
    chunk_size = 1024

    temp_folder = os.environ["TEMP"]
    with open(f"{temp_folder}/{file_name}.{piece_number}", "wb") as f:
        for chunk in tqdm(response.iter_content(chunk_size=chunk_size), total=math.ceil(total_size / chunk_size), unit="KB", unit_scale=True):
            f.write(chunk)


def download_split_file(url, number_pieces, save_path):
    file_name = url.split("/")[-1]
    response = requests.get(url, stream=True)
    file_size = int(response.headers.get("Content-Length", 0))
    piece_size = math.ceil(file_size / number_pieces)

    with concurrent.futures.ThreadPoolExecutor(max_workers=number_pieces) as executor:
        futures = [executor.submit(download_piece, url, i, piece_size, file_name) for i in range(number_pieces)]

    temp_folder = os.environ["TEMP"]
    with open(os.path.join(save_path, file_name), "wb") as f:
        for i in range(number_pieces):
            with open(f"{temp_folder}/{file_name}.{i}", "rb") as piece:
                f.write(piece.read())

    for i in range(number_pieces):
        os.remove(f"{temp_folder}/{file_name}.{i}")


app = ctk.CTk()
app.geometry("500x500")
app.title("File Downloader")
save_path = os.path.expanduser("~/Downloads")


def select_save_location():
    global save_path
    save_path = filedialog.askdirectory()
    path_label.configure(text=save_path)


def download():
    os.system("cls||clear")
    url = url_entry.get()
    number_pieces = int(pieces_entry.get())
    if not save_path:
        messagebox.showerror("Error", "Please select a save location")
        return
    try:
        download_split_file(url, number_pieces, save_path)
        messagebox.showinfo("Info", "File has been downloaded successfully")
    except Exception as e:
        messagebox.showerror("Error", str(e))


url_label = ctk.CTkLabel(app, text="URL:")
url_label.pack()
url_entry = ctk.CTkEntry(app)
url_entry.pack(fill=tk.X)
url_entry.insert(0, "https://speed.hetzner.de/100MB.bin")

pieces_label = ctk.CTkLabel(app, text="Segments:")
pieces_label.pack()
pieces_entry = ctk.CTkEntry(app)
pieces_entry.pack(fill=tk.X)
pieces_entry.insert(0, "16")

path_label = ctk.CTkLabel(master=app, text=str(save_path), font=("Helvetica", 12))
path_label.pack()
save_button = ctk.CTkButton(master=app, text="Save Location", command=select_save_location)
save_button.pack(padx=10, pady=10)


download_button = ctk.CTkButton(master=app, text="Download", command=download)
download_button.pack(padx=10, pady=10)


quit = ctk.CTkButton(master=app, text="Quit", command=app.destroy)
quit.pack(padx=10, pady=10)

app.mainloop()
