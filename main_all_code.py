import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

PASSWORD_FILE = "passwords.json"

def load_passwords():
    if not os.path.exists(PASSWORD_FILE):
        return {}
    with open(PASSWORD_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_passwords(passwords):
    with open(PASSWORD_FILE, "w") as f:
        json.dump(passwords, f, indent=4)

def refresh_list():
    listbox.delete(0, tk.END)
    passwords = load_passwords()
    for site in passwords.keys():
        listbox.insert(tk.END, site)

def add_password_gui():
    site = simpledialog.askstring("Add", "Enter site name:")
    if not site: return
    
    username = simpledialog.askstring("Add", "Enter username:")
    if not username: return
    
    password = simpledialog.askstring("Add", "Enter password:", show="*")
    if not password: return

    passwords = load_passwords()
    passwords[site] = {"username": username, "password": password}
    save_passwords(passwords)
    
    messagebox.showinfo("Success", f"Password for {site} added!")
    refresh_list()

def view_password_gui():
    try:
        selected_site = listbox.get(listbox.curselection())
    except tk.TclError:
        messagebox.showwarning("Error!", "To view a password, you must select a site from the list.")
        return

    passwords = load_passwords()
    cred = passwords.get(selected_site)
    if cred:
        info = f"Site: {selected_site}\nUsername: {cred['username']}\nPassword: {cred['password']}"
        messagebox.showinfo("Account Details", info)

def delete_password_gui():
    try:
        selected_site = listbox.get(listbox.curselection())
    except tk.TclError:
        messagebox.showwarning("Error!", "To delete a password, you must select a site from the list.")
        return

    if messagebox.askyesno("Alright!", f"Delete password for {selected_site}?"):
        passwords = load_passwords()
        if selected_site in passwords:
            del passwords[selected_site]
            save_passwords(passwords)
            messagebox.showinfo("Success", "Password deleted successfully.")
            refresh_list()

root = tk.Tk()
root.title("PassManager")
root.geometry("400x350")
root.configure(bg="#000000")

label = tk.Label(root, text="Your saved sites:", bg="#000000", fg="white", font=("Arial", 12, "bold"))
label.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=5)

scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
listbox = tk.Listbox(frame, width=40, height=10, yscrollcommand=scrollbar.set, font=("Arial", 10))
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

btn_frame = tk.Frame(root, bg="#000000")
btn_frame.pack(pady=15)

btn_add = tk.Button(btn_frame, text="Add", width=10, command=add_password_gui, bg="#ffffff", fg="black", font=("Arial", 10, "bold"))
btn_add.grid(row=0, column=0, padx=5)

btn_view = tk.Button(btn_frame, text="View", width=10, command=view_password_gui, bg="#ffffff", fg="black", font=("Arial", 10, "bold"))
btn_view.grid(row=0, column=1, padx=5)

btn_delete = tk.Button(btn_frame, text="Delete", width=10, command=delete_password_gui, bg="#ffffff", fg="black", font=("Arial", 10, "bold"))
btn_delete.grid(row=0, column=2, padx=5)

refresh_list()

root.mainloop()
