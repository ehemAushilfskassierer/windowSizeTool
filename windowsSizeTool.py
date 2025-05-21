# Part 1: Basic GUI and Window List Setup

import tkinter as tk
from tkinter import ttk
import pygetwindow as gw

# Create main window
root = tk.Tk()
root.title("Window Info & Ratio Adjustment")
root.geometry("600x500")
root.configure(bg="#f0f2f5")

# Apply modern theme
style = ttk.Style(root)
style.theme_use("clam")
style.configure("TLabel", background="#f0f2f5", font=("Segoe UI", 11))
style.configure("TButton", font=("Segoe UI", 10), padding=5)
style.configure("TCombobox", padding=5)

# --- Window selection section ---
frame_select = ttk.Frame(root, padding=10)
frame_select.pack(pady=10, fill='x')

ttk.Label(frame_select, text="Select a window:").pack(anchor="w")

combo = ttk.Combobox(frame_select, width=60, state="readonly")
combo.pack(fill='x')

def refresh_window_list():
    windows = gw.getWindowsWithTitle("")
    titles = [w.title for w in windows if w.title.strip() != ""]
    combo['values'] = titles
    if titles:
        combo.current(0)
        update_window_info()

btn_refresh = ttk.Button(frame_select, text="Refresh window list", command=refresh_window_list)
btn_refresh.pack(pady=5)

combo.bind("<<ComboboxSelected>>", lambda e: update_window_info())

# Part 2: Displaying Window Information

# Text variable for displaying info
text_var = tk.StringVar()

# Info display section
frame_info = ttk.LabelFrame(root, text="Window Information", padding=10)
frame_info.pack(padx=10, pady=10, fill='both', expand=True)

label = ttk.Label(frame_info, textvariable=text_var, justify="left", font=("Segoe UI", 10))
label.pack(anchor="w")

def get_selected_window():
    title = combo.get()
    windows = gw.getWindowsWithTitle(title)
    return windows[0] if windows else None

def update_window_info():
    try:
        win = get_selected_window()
        if win:
            info = (
                f"Title: {win.title}\n"
                f"Position: ({win.left}, {win.top})\n"
                f"Size: {win.width} x {win.height}"
            )
        else:
            info = "Window not found."
    except Exception as e:
        info = f"Error: {e}"
    text_var.set(info)

# Part 3: Aspect Ratio Adjustment Input

# Ratio input section
frame_ratio = ttk.LabelFrame(root, text="Aspect Ratio", padding=10)
frame_ratio.pack(padx=10, pady=10, fill='x')

ttk.Label(frame_ratio, text="Width:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
entry_width = ttk.Entry(frame_ratio, width=5)
entry_width.insert(0, "9")
entry_width.grid(row=0, column=1, padx=5, pady=2)

ttk.Label(frame_ratio, text="Height:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
entry_height = ttk.Entry(frame_ratio, width=5)
entry_height.insert(0, "16")
entry_height.grid(row=1, column=1, padx=5, pady=2)

# Part 4: Applying Ratio and Starting the App

def set_aspect_ratio():
    try:
        win = get_selected_window()
        if not win:
            text_var.set("No valid window selected.")
            return

        ratio_w = int(entry_width.get())
        ratio_h = int(entry_height.get())

        new_height = win.height
        new_width = int((ratio_w / ratio_h) * new_height)

        win.resizeTo(new_width, new_height)
        update_window_info()

    except Exception as e:
        text_var.set(f"Error while setting aspect ratio: {e}")

# Apply ratio button
btn_apply = ttk.Button(root, text="Apply Aspect Ratio", command=set_aspect_ratio)
btn_apply.pack(pady=10)

# Initial window list refresh
refresh_window_list()

# Run the main loop
root.mainloop()
