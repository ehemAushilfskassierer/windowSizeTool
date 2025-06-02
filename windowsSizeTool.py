"""
Windows Size Tool

GUI which selects all open windows and lets you
reshape a selected window to the aspect ratio you
decide.

Author: ehem. Aushilfskassierer
"""

# Part 1

# Imports
import tkinter as tk
from tkinter import ttk 
import pygetwindow as gw

# Global variable for saving the current window text
selected_window = None

def refresh_window_list():
    """
    Refreshes the list of all currently open windows with
    titles.
    """
    windows = gw.getWindowsWithTitle("")  # All windows
    window_titles = [w.title for w in windows if 
                     w.title.strip() != ""]
    combo['values'] = window_titles
    if window_titles:
        combo.current(0)
        update_window_info()

def get_selected_window():
    """
    Returns the window currently selected in the combo box.
    """
    title = combo.get()
    windows = gw.getWindowsWithTitle(title)
    return windows[0] if windows else None

# --------------------------------------------------------------
# Part 2

def update_window_info():
    """
    Displays information (title, position, size) of the
    selected window.
    """
    try:
        win = get_selected_window()
        if win:
            info = f"Selected window:\n\nTitle: {win.title}\n\
                Position: ({win.left}, {win.top})\n\
                Size: {win.width} x {win.height}"
        else:
            info = "Window not found."
    except Exception as e:
        info = f"Error: {e}"
    text_var.set(info)

def set_aspect_ratio():
    """
    Adjusts the window size based on the aspect ratio entered.
    The window height remains the same, the width is adjusted.
    """
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
        text_var.set(f"Error setting window size: {e}")

# --------------------------------------------------------------
# Part 3: 

# GUI Setup
root = tk.Tk()
root.title("Window info & ratio adjustment")

# Window selection
frame_select = tk.Frame(root)
frame_select.pack(pady=10)

tk.Label(frame_select, text="Select window:").pack()
combo = ttk.Combobox(frame_select, width=60)
combo.pack()
combo.bind("<<ComboboxSelected>>", lambda e: update_window_info())

btn_refresh = tk.Button(frame_select,
                        text="Refresh window list",
                        command=refresh_window_list)
btn_refresh.pack(pady=5)

# Info display
text_var = tk.StringVar()
label = tk.Label(root, textvariable=text_var,
                 justify="left", font=("Arial", 12),
                 padx=10, pady=10)
label.pack()

# --------------------------------------------------------------
# Part 4

# Aspect ratio input
frame_ratio = tk.Frame(root)
frame_ratio.pack(pady=10)

tk.Label(frame_ratio, text="Aspect ratio:").grid(row=0,
                                    column=0, columnspan=2)

tk.Label(frame_ratio, text="Width").grid(row=1, column=0)
entry_width = tk.Entry(frame_ratio, width=5)
entry_width.insert(0, "9")
entry_width.grid(row=1, column=1)

tk.Label(frame_ratio, text="Height").grid(row=2, column=0)
entry_height = tk.Entry(frame_ratio, width=5)
entry_height.insert(0, "16")
entry_height.grid(row=2, column=1)

btn_set_ratio = tk.Button(root, text="Set size by ratio", 
                          command=set_aspect_ratio)
btn_set_ratio.pack(pady=10)

# Initial call
refresh_window_list()
root.mainloop()