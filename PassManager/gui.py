import tkinter as tk
from tkinter import messagebox, simpledialog

from main import refresh_list

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