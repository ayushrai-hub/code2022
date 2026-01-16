import tkinter as tk
from tkinter import messagebox

def calculate_square():
    try:
        num = int(entry.get())
        if 1 <= num <= 10:
            square = num * num
            result_label.config(text=f"The square of {num} is {square}")
        else:
            messagebox.showerror("Error", "Please enter a number between 1 and 10.")
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter a valid integer.")

# Create the main window
window = tk.Tk()
window.title("Square Calculator")

# Input Label and Entry
input_label = tk.Label(window, text="Enter a number (1-10):")
input_label.grid(row=0, column=0, padx=5, pady=5)  # Use grid for layout

entry = tk.Entry(window)
entry.grid(row=0, column=1, padx=5, pady=5)

# Calculate Button
calculate_button = tk.Button(window, text="Calculate", command=calculate_square)
calculate_button.grid(row=1, column=0, columnspan=2, pady=10) # Span across two columns

# Result Label
result_label = tk.Label(window, text="")
result_label.grid(row=2, column=0, columnspan=2)

# Center the window (optional)
window.update_idletasks()  # Important for accurate window size
width = window.winfo_width()
height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width // 2) - (width // 2)
y = (screen_height // 2) - (height // 2)
window.geometry(f"+{x}+{y}") # Set the position


window.mainloop()