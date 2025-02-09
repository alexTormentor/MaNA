from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from typing import List, Dict
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Путь к файлу с данными о книгах
BOOKS_FILE = "DB/book_data.json"

def load_books() -> List[Dict]:
    """Загрузка списка книг из JSON-файла."""
    with open(BOOKS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def filter_books(books: List[Dict], author: str = None, genre: str = None, setting: str = None) -> List[Dict]:
    """Фильтрация книг по тегам."""
    filtered_books = books
    if author:
        filtered_books = [book for book in filtered_books if book["author"] == author]
    if genre:
        filtered_books = [book for book in filtered_books if book["genre"] == genre]
    if setting:
        filtered_books = [book for book in filtered_books if book["setting"] == setting]
    return filtered_books

@app.get("/")
def get_books_page(request: Request):
    """Главная страница с книгами."""
    books = load_books()
    authors = sorted(set(book["author"] for book in books))
    genres = sorted(set(book["genre"] for book in books))
    settings = sorted(set(book["setting"] for book in books))
    return templates.TemplateResponse("books.html", {
        "request": request,
        "books": books,
        "authors": authors,
        "genres": genres,
        "settings": settings
    })

@app.post("/filter")
def post_filter_books(
    request: Request,
    author: str = Form(None),
    genre: str = Form(None),
    setting: str = Form(None)
):
    """Обработка фильтрации книг."""
    books = load_books()
    filtered_books = filter_books(books, author, genre, setting)
    authors = sorted(set(book["author"] for book in books))
    genres = sorted(set(book["genre"] for book in books))
    settings = sorted(set(book["setting"] for book in books))
    return templates.TemplateResponse("books.html", {
        "request": request,
        "books": filtered_books,
        "authors": authors,
        "genres": genres,
        "settings": settings
    })

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=5000)
