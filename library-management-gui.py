import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = True
        self.borrower = None
        self.borrow_date = None

    def to_dict(self):
        return {
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'is_available': self.is_available,
            'borrower': self.borrower,
            'borrow_date': self.borrow_date
        }

    @classmethod
    def from_dict(cls, data):
        book = cls(data['title'], data['author'], data['isbn'])
        book.is_available = data['is_available']
        book.borrower = data['borrower']
        book.borrow_date = data['borrow_date']
        return book

class LibraryManagementSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Library Management System")
        self.root.geometry("800x600")
        self.books = []
        self.load_books()
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)

        self.create_add_book_tab()
        self.create_borrow_return_tab()
        self.create_search_tab()
        self.create_view_books_tab()

        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[12, 8])
        style.configure('TButton', padding=[10, 5])

    def create_add_book_tab(self):
        add_frame = ttk.Frame(self.notebook)
        self.notebook.add(add_frame, text='Add Book')

        ttk.Label(add_frame, text="Add New Book", font=('Helvetica', 16, 'bold')).pack(pady=20)

        form_frame = ttk.Frame(add_frame)
        form_frame.pack(pady=20)
        ttk.Label(form_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = ttk.Entry(form_frame, width=40)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(form_frame, text="Author:").grid(row=1, column=0, padx=5, pady=5)
        self.author_entry = ttk.Entry(form_frame, width=40)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="ISBN:").grid(row=2, column=0, padx=5, pady=5)
        self.isbn_entry = ttk.Entry(form_frame, width=40)
        self.isbn_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(form_frame, text="Add Book", command=self.add_book).grid(row=3, column=0, columnspan=2, pady=20)

    def create_borrow_return_tab(self):
        borrow_frame = ttk.Frame(self.notebook)
        self.notebook.add(borrow_frame, text='Borrow/Return')

        ttk.Label(borrow_frame, text="Borrow Book", font=('Helvetica', 16, 'bold')).pack(pady=20)
        borrow_form = ttk.Frame(borrow_frame)
        borrow_form.pack(pady=10)
        ttk.Label(borrow_form, text="ISBN:").grid(row=0, column=0, padx=5, pady=5)
        self.borrow_isbn_entry = ttk.Entry(borrow_form, width=30)
        self.borrow_isbn_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(borrow_form, text="Borrower Name:").grid(row=1, column=0, padx=5, pady=5)
        self.borrower_entry = ttk.Entry(borrow_form, width=30)
        self.borrower_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(borrow_form, text="Borrow Book", command=self.borrow_book).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Label(borrow_frame, text="Return Book", font=('Helvetica', 16, 'bold')).pack(pady=20)
        return_form = ttk.Frame(borrow_frame)
        return_form.pack(pady=10)

        ttk.Label(return_form, text="ISBN:").grid(row=0, column=0, padx=5, pady=5)
        self.return_isbn_entry = ttk.Entry(return_form, width=30)
        self.return_isbn_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(return_form, text="Return Book", command=self.return_book).grid(row=1, column=0, columnspan=2, pady=10)

    def create_search_tab(self):
        search_frame = ttk.Frame(self.notebook)
        self.notebook.add(search_frame, text='Search')
        ttk.Label(search_frame, text="Search Books", font=('Helvetica', 16, 'bold')).pack(pady=20)

        search_form = ttk.Frame(search_frame)
        search_form.pack(pady=10)

        ttk.Label(search_form, text="Search Term:").grid(row=0, column=0, padx=5, pady=5)
        self.search_entry = ttk.Entry(search_form, width=40)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(search_form, text="Search", command=self.search_books).grid(row=1, column=0, columnspan=2, pady=10)
        self.search_results = ttk.Treeview(search_frame, columns=('Title', 'Author', 'ISBN', 'Status'), show='headings')
        self.search_results.heading('Title', text='Title')
        self.search_results.heading('Author', text='Author')
        self.search_results.heading('ISBN', text='ISBN')
        self.search_results.heading('Status', text='Status')
        self.search_results.pack(pady=10, padx=10, fill='both', expand=True)

    def create_view_books_tab(self):
        view_frame = ttk.Frame(self.notebook)
        self.notebook.add(view_frame, text='View All Books')
        self.books_table = ttk.Treeview(view_frame, columns=('Title', 'Author', 'ISBN', 'Status', 'Borrower'), show='headings')
        self.books_table.heading('Title', text='Title')
        self.books_table.heading('Author', text='Author')
        self.books_table.heading('ISBN', text='ISBN')
        self.books_table.heading('Status', text='Status')
        self.books_table.heading('Borrower', text='Borrower')
        self.books_table.pack(pady=20, padx=10, fill='both', expand=True)
        refresh_button = ttk.Button(view_frame, text="Refresh", command=self.refresh_books_table)
        refresh_button.pack(pady=10)

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        isbn = self.isbn_entry.get().strip()
        if not all([title, author, isbn]):
            messagebox.showerror("Error", "All fields are required!")
            return
        if any(book.isbn == isbn for book in self.books):
            messagebox.showerror("Error", "A book with this ISBN already exists!")
            return

        book = Book(title, author, isbn)
        self.books.append(book)
        self.save_books()
        
        messagebox.showinfo("Success", f"Book '{title}' has been added successfully!")
        self.clear_add_book_form()
        self.refresh_books_table()

    def borrow_book(self):
        isbn = self.borrow_isbn_entry.get().strip()
        borrower = self.borrower_entry.get().strip()

        if not all([isbn, borrower]):
            messagebox.showerror("Error", "Both ISBN and borrower name are required!")
            return

        book = self.find_book_by_isbn(isbn)
        if not book:
            messagebox.showerror("Error", "Book not found!")
            return

        if not book.is_available:
            messagebox.showerror("Error", "Book is already borrowed!")
            return

        book.is_available = False
        book.borrower = borrower
        book.borrow_date = datetime.now().strftime("%Y-%m-%d")
        self.save_books()
        
        messagebox.showinfo("Success", f"Book has been borrowed by {borrower}!")
        self.clear_borrow_form()
        self.refresh_books_table()

    def return_book(self):
        isbn = self.return_isbn_entry.get().strip()

        if not isbn:
            messagebox.showerror("Error", "ISBN is required!")
            return

        book = self.find_book_by_isbn(isbn)
        if not book:
            messagebox.showerror("Error", "Book not found!")
            return

        if book.is_available:
            messagebox.showerror("Error", "Book is already in the library!")
            return

        book.is_available = True
        book.borrower = None
        book.borrow_date = None
        self.save_books()
        
        messagebox.showinfo("Success", "Book has been returned successfully!")
        self.clear_return_form()
        self.refresh_books_table()

    def search_books(self):
        search_term = self.search_entry.get().strip().lower()
        
        if not search_term:
            messagebox.showerror("Error", "Please enter a search term!")
            return
        for item in self.search_results.get_children():
            self.search_results.delete(item)

        for book in self.books:
            if (search_term in book.title.lower() or 
                search_term in book.author.lower() or 
                search_term in book.isbn.lower()):
                status = "Available" if book.is_available else "Borrowed"
                self.search_results.insert('', 'end', values=(
                    book.title, book.author, book.isbn, status))

    def refresh_books_table(self):
        for item in self.books_table.get_children():
            self.books_table.delete(item)

        for book in self.books:
            status = "Available" if book.is_available else "Borrowed"
            borrower = book.borrower if book.borrower else "-"
            self.books_table.insert('', 'end', values=(
                book.title, book.author, book.isbn, status, borrower))

    def find_book_by_isbn(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def clear_add_book_form(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.isbn_entry.delete(0, tk.END)

    def clear_borrow_form(self):
        self.borrow_isbn_entry.delete(0, tk.END)
        self.borrower_entry.delete(0, tk.END)

    def clear_return_form(self):
        self.return_isbn_entry.delete(0, tk.END)

    def save_books(self):
        books_data = [book.to_dict() for book in self.books]
        with open('library_data.json', 'w') as f:
            json.dump(books_data, f)

    def load_books(self):
        try:
            with open('library_data.json', 'r') as f:
                books_data = json.load(f)
                self.books = [Book.from_dict(data) for data in books_data]
        except FileNotFoundError:
            self.books = []

    def run(self):
        self.refresh_books_table()
        self.root.mainloop()

if __name__ == "__main__":
    app = LibraryManagementSystem()
    app.run()
