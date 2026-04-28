import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.root.geometry("700x550")
        
        self.filename = "books.json"
        self.books = self.load_data()

        input_frame = tk.LabelFrame(root, text="Добавить новую книгу", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="w")
        self.title_entry = tk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Автор:").grid(row=1, column=0, sticky="w")
        self.author_entry = tk.Entry(input_frame, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Жанр:").grid(row=0, column=2, sticky="w", padx=(10, 0))
        self.genre_entry = tk.Entry(input_frame, width=20)
        self.genre_entry.grid(row=0, column=3, padx=5, pady=2)

        tk.Label(input_frame, text="Страниц:").grid(row=1, column=2, sticky="w", padx=(10, 0))
        self.pages_entry = tk.Entry(input_frame, width=20)
        self.pages_entry.grid(row=1, column=3, padx=5, pady=2)

        self.add_btn = tk.Button(input_frame, text="Добавить книгу", command=self.add_book, bg="#e1f5fe")
        self.add_btn.grid(row=2, column=0, columnspan=4, pady=10, sticky="we")

        filter_frame = tk.LabelFrame(root, text="Фильтрация", padx=10, pady=5)
        filter_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(filter_frame, text="Жанр:").grid(row=0, column=0)
        self.filter_genre = tk.Entry(filter_frame, width=15)
        self.filter_genre.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="Мин. страниц:").grid(row=0, column=2)
        self.filter_pages = tk.Entry(filter_frame, width=10)
        self.filter_pages.grid(row=0, column=3, padx=5)

        tk.Button(filter_frame, text="Применить", command=self.apply_filter).grid(row=0, column=4, padx=5)
        tk.Button(filter_frame, text="Сброс", command=self.refresh_table).grid(row=0, column=5, padx=5)

        self.tree = ttk.Treeview(root, columns=("title", "author", "genre", "pages"), show="headings")
        self.tree.heading("title", text="Название")
        self.tree.heading("author", text="Автор")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("pages", text="Страницы")
        
        self.tree.column("pages", width=80, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        self.refresh_table()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_data(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()

        if not all([title, author, genre, pages]):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return
        
        if not pages.isdigit():
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return

        new_book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": int(pages)
        }

        self.books.append(new_book)
        self.save_data()
        self.refresh_table()
        self.clear_entries()

    def refresh_table(self, data_to_show=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        display_list = data_to_show if data_to_show is not None else self.books
        for book in display_list:
            self.tree.insert("", "end", values=(book["title"], book["author"], book["genre"], book["pages"]))

    def apply_filter(self):
        genre_val = self.filter_genre.get().lower().strip()
        min_pages = self.filter_pages.get().strip()

        filtered = self.books

        if genre_val:
            filtered = [b for b in filtered if genre_val in b["genre"].lower()]
        
        if min_pages.isdigit():
            filtered = [b for b in filtered if b["pages"] >= int(min_pages)]

        self.refresh_table(filtered)

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()
