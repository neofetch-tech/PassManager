import os
import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog
from cryptography.fernet import Fernet

DB_FILE = "passwords.db"
KEY_FILE = "secret.key"


def load_or_generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
    else:
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
    return Fernet(key)

cipher = load_or_generate_key()


def init_db():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        site TEXT UNIQUE NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)
    connection.commit()
    connection.close()


def refresh_list():
    listbox.delete(0, tk.END)
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute("SELECT site FROM accounts")
    rows = cursor.fetchall()
    connection.close()
    for row in rows:
        listbox.insert(tk.END, row[0])


def add_password_gui():
    site = simpledialog.askstring("Add", "Enter site name:")
    if not site:
        return
    username = simpledialog.askstring("Add", "Enter username:")
    if not username:
        return
    password = simpledialog.askstring("Add", "Enter password:", show="*")
    if not password:
        return

    encrypted_password = cipher.encrypt(password.encode()).decode()

    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT OR REPLACE INTO accounts (site, username, password) VALUES (?, ?, ?)",
            (site, username, encrypted_password),
        )
        connection.commit()
        messagebox.showinfo("Success", f"Password for {site} added!")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Something went wrong: {e}")
    finally:
        connection.close()

    refresh_list()


def view_password_gui():
    try:
        selected_site = listbox.get(listbox.curselection())
    except tk.TclError:
        messagebox.showwarning(
            "Error!",
            "To view a password, you must select a site from the list.",
        )
        return

    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT username, password FROM accounts WHERE site = ?",
        (selected_site,),
    )
    row = cursor.fetchone()
    connection.close()

    if row:
        username = row[0]
        encrypted_password = row[1]

        try:
            decrypted_password = cipher.decrypt(
                encrypted_password.encode()
            ).decode()
            info = f"Site: {selected_site}\nUsername: {username}\nPassword: {decrypted_password}"
            messagebox.showinfo("Account Details", info)
        except Exception:
            messagebox.showerror(
                "Error", "Failed to decrypt password. Key might be missing."
            )


def delete_password_gui():
    try:
        selected_site = listbox.get(listbox.curselection())
    except tk.TclError:
        messagebox.showwarning(
            "Error!",
            "To delete a password, you must select a site from the list.",
        )
        return

    if messagebox.askyesno("Alright!", f"Delete password for {selected_site}?"):
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM accounts WHERE site = ?", (selected_site,))
        connection.commit()
        connection.close()
        messagebox.showinfo("Success", "Password deleted successfully.")
        refresh_list()


init_db()

root = tk.Tk()
root.iconphoto(False, tk.PhotoImage(file='Eyes of war.png'))
root.title("PassManager")
root.geometry("400x350")
root.configure(bg="#000000")

label = tk.Label(
    root,
    text="Your saved sites:",
    bg="#000000",
    fg="white",
    font=("Arial", 12, "bold"),
)
label.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=5)

scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
listbox = tk.Listbox(
    frame, width=40, height=10, yscrollcommand=scrollbar.set, font=("Arial", 10)
)
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

btn_frame = tk.Frame(root, bg="#000000")
btn_frame.pack(pady=15)

btn_add = tk.Button(
    btn_frame,
    text="Add",
    width=10,
    command=add_password_gui,
    bg="#ffffff",
    fg="black",
    font=("Arial", 10, "bold"),
)
btn_add.grid(row=0, column=0, padx=5)

btn_view = tk.Button(
    btn_frame,
    text="View",
    width=10,
    command=view_password_gui,
    bg="#ffffff",
    fg="black",
    font=("Arial", 10, "bold"),
)
btn_view.grid(row=0, column=1, padx=5)

btn_delete = tk.Button(
    btn_frame,
    text="Delete",
    width=10,
    command=delete_password_gui,
    bg="#ffffff",
    fg="black",
    font=("Arial", 10, "bold"),
)
btn_delete.grid(row=0, column=2, padx=5)

refresh_list()
root.mainloop()
