import tkinter as tk
from tkinter import ttk

class Library:
    def __init__(self, root):
        self.file = open("books.txt", "a+")
        self.root = root
        self.file = "books.txt"
        self.books = {}
        self.load_books()

    def load_books(self):
        with open(self.file, "r") as f:
            for line in f.read().splitlines():
                title, *_ = line.strip().split(',')
                title = title.strip()
                self.books[title.lower()] = self.books.get(title.lower(), 0) + 1

    def list_books(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        list_books_button = tk.Button(self.root, text="List Books", command=self.list_books)
        list_books_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        add_book_button = tk.Button(self.root, text="Add Book", command=add_book_gui)
        add_book_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        delete_book_button = tk.Button(self.root, text="Delete Book", command=delete_book_gui)
        delete_book_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        quit_button = tk.Button(self.root, text="Quit", command=quit_program)
        quit_button.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

        tree = ttk.Treeview(self.root, columns=("Title", "Author", "Pages", "Year", "Count"), show="headings")
        tree.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        tree.heading("Title", text="Title")
        tree.heading("Author", text="Author")
        tree.heading("Pages", text="Pages")
        tree.heading("Year", text="Year")
        tree.heading("Count", text="Count")

        with open(self.file, "r") as f:
            printed_books = set()
            for line in f.read().splitlines():
                title, author, pages, year = line.strip().split(',')
                title = title.strip()
                count = self.books.get(title.lower(), 0)
                if title.lower() not in printed_books:
                    tree.insert("", "end", values=(title, author, pages, year, count))
                    printed_books.add(title.lower())

    def add_book(self, title, author, pages, year, count):
        with open(self.file, "a") as f:
            for _ in range(int(count)):
                f.write(f"{title}, {author}, {pages}, {year}\n")
        self.books[title.lower()] = self.books.get(title.lower(), 0) + int(count)
        self.list_books() 

    def delete_book(self, title, count):
        title_lower = title.lower()
        if title_lower in self.books:
            if self.books[title_lower] >= count:
                self.books[title_lower] -= count
                lines_to_keep = []
                with open(self.file, "r") as f:
                    for line in f:
                        if title_lower in line.lower():
                            if count > 0:
                                count -= 1
                            else:
                                lines_to_keep.append(line)
                        else:
                            lines_to_keep.append(line)
                with open(self.file, "w") as f:
                    f.writelines(lines_to_keep)
        self.list_books()  

def add_book_gui():
    add_book_window = tk.Toplevel(root)
    add_book_window.title("Add Book")

    fields = ["Title", "Author", "Pages", "Year", "Count"]
    entries = []
    for i, field in enumerate(fields):
        label = tk.Label(add_book_window, text=field+": ")
        label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
        entry = tk.Entry(add_book_window)
        entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
        entries.append(entry)

    def add_book():
        values = [entry.get() for entry in entries]
        lib.add_book(*values)

    submit_button = tk.Button(add_book_window, text="Add Book", command=add_book)
    submit_button.grid(row=len(fields), columnspan=2, padx=5, pady=10)

def delete_book_gui():
    delete_book_window = tk.Toplevel(root)
    delete_book_window.title("Delete Book")

    title_label = tk.Label(delete_book_window, text="Title: ")
    title_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    title_entry = tk.Entry(delete_book_window)
    title_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    count_label = tk.Label(delete_book_window, text="Count: ")
    count_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    count_entry = tk.Entry(delete_book_window)
    count_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    def delete_book():
        title = title_entry.get()
        count = int(count_entry.get())
        lib.delete_book(title, count)

    submit_button = tk.Button(delete_book_window, text="Delete Book", command=delete_book)
    submit_button.grid(row=2, columnspan=2, padx=5, pady=10)

def quit_program():
    root.destroy()

root = tk.Tk()
root.title("Library Management System")

lib = Library(root)

list_books_button = tk.Button(root, text="List Books", command=lib.list_books)
list_books_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

add_book_button = tk.Button(root, text="Add Book", command=add_book_gui)
add_book_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

delete_book_button = tk.Button(root, text="Delete Book", command=delete_book_gui)
delete_book_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

quit_button = tk.Button(root, text="Quit", command=quit_program)
quit_button.grid(row=0, column=3, padx=10, pady=10, sticky="ew")

root.mainloop()
