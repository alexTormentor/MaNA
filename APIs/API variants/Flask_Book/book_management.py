from flask import Flask, render_template, request, redirect, url_for, jsonify
import json

app = Flask(__name__)

BOOKS_FILE = "DB/book_data.json"


def load_books():
    """Загрузка списка книг из JSON-файла."""
    with open(BOOKS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_books(books):
    """Сохранение списка книг в JSON-файл."""
    with open(BOOKS_FILE, "w", encoding="utf-8") as file:
        json.dump(books, file, indent=4, ensure_ascii=False)


def filter_books(books, author=None, genre=None, setting=None):
    """Фильтрация книг по тегам."""
    filtered_books = books
    if author:
        filtered_books = [book for book in filtered_books if book["author"] == author]
    if genre:
        filtered_books = [book for book in filtered_books if book["genre"] == genre]
    if setting:
        filtered_books = [book for book in filtered_books if book["setting"] == setting]
    return filtered_books


@app.route("/", methods=["GET", "POST"])
def index():
    """Главная страница с книгами и фильтрацией."""
    books = load_books()
    authors = sorted(set(book["author"] for book in books))
    genres = sorted(set(book["genre"] for book in books))
    settings = sorted(set(book["setting"] for book in books))

    if request.method == "POST":
        author = request.form.get("author")
        genre = request.form.get("genre")
        setting = request.form.get("setting")
        books = filter_books(books, author, genre, setting)

    return render_template("index.html", books=books, authors=authors, genres=genres, settings=settings)


@app.route("/rent/<int:book_id>", methods=["POST"])
def rent_book(book_id):
    """Аренда книги по ID."""
    books = load_books()
    for book in books:
        if book["id"] == book_id and not book["is_rented"]:
            book["is_rented"] = True
            save_books(books)
            return redirect(url_for("index"))
    return "Книга уже арендована или не найдена.", 400


@app.route("/return/<int:book_id>", methods=["POST"])
def return_book(book_id):
    """Возврат книги по ID."""
    books = load_books()
    for book in books:
        if book["id"] == book_id and book["is_rented"]:
            book["is_rented"] = False
            save_books(books)
            return redirect(url_for("index"))
    return "Книга не арендована или не найдена.", 400


if __name__ == "__main__":
    app.run(debug=True)
