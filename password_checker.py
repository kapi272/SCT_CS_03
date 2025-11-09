import tkinter as tk
import re, random, string
from tkinter import ttk
from tkinter import messagebox

SPECIALS = "!@#$%^&*()-_=+[]{}|;:,.<>?/"

def generate_password(length=14):
    chars = string.ascii_letters + string.digits + SPECIALS
    pw = "".join(random.choice(chars) for _ in range(length))
    entry.delete(0, tk.END)
    entry.insert(0, pw)
    check_strength()

def copy_password():
    pw = entry.get()
    if pw:
        root.clipboard_clear()
        root.clipboard_append(pw)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

def toggle_password_visibility():
    if entry.cget("show") == "":
        entry.config(show="•")
        btn_show.config(text="👁 Show")
    else:
        entry.config(show="")
        btn_show.config(text="🙈 Hide")

def check_strength(event=None):
    password = entry.get()
    score = 0
    suggestions = []

    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 8 characters")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        suggestions.append("Add an uppercase letter (A-Z)")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("Add a lowercase letter (a-z)")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        suggestions.append("Add at least one number (0-9)")

    if re.search(f"[{re.escape(SPECIALS)}]", password):
        score += 1
    else:
        suggestions.append("Add a special character (!@#$...)")

    progress["value"] = score * 20

    if score <= 2:
        lbl_strength.config(text="Weak", foreground="red")
    elif score == 3:
        lbl_strength.config(text="Moderate", foreground="orange")
    elif score == 4:
        lbl_strength.config(text="Strong", foreground="green")
    else:
        lbl_strength.config(text="Very Strong", foreground="blue")

    lbl_suggestions.config(text="\n".join(suggestions) if suggestions else "Looks good!")

root = tk.Tk()
root.title("Password Checker")
root.geometry("430x300")
root.resizable(False, False)

tk.Label(root, text="Enter Password:", font=("Arial", 12)).pack(pady=5)

entry = tk.Entry(root, font=("Arial", 14), width=28, show="•")
entry.pack()
entry.bind("<KeyRelease>", check_strength)

btn_show = tk.Button(root, text="👁 Show", command=toggle_password_visibility)
btn_show.pack(pady=4)

lbl_strength = tk.Label(root, text="", font=("Arial", 14, "bold"))
lbl_strength.pack(pady=5)

progress = ttk.Progressbar(root, length=300, mode="determinate")
progress.pack(pady=5)

lbl_suggestions = tk.Label(root, text="", font=("Arial", 10))
lbl_suggestions.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=8)

tk.Button(frame, text="Generate Password", command=generate_password).grid(row=0, column=0, padx=8)
tk.Button(frame, text="Copy Password", command=copy_password).grid(row=0, column=1, padx=8)

check_strength()
root.mainloop()
