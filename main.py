from fastapi import FastAPI, HTTPException
import os
import json
from pydantic import BaseModel
from typing import Optional, Literal
from uuid import uuid4
from fastapi.encoders import jsonable_encoder

class Book(BaseModel):
    name: str
    book_id: Optional[str] = uuid4().hex
    price: float
    genre: Literal["fiction", "non-fiction"]
    

app = FastAPI()

# DB schema
BOOKS_FILE = "book.json"
BOOK_DATABASE = [
]

if os.path.exists(BOOKS_FILE):
    with open(BOOKS_FILE, "r") as f:
        BOOK_DATABASE = json.load(f)

# /
@app.get("/")
async def root():
    return {"message": "Hello World"}

# /list-books
@app.get("/list-books")
async def list_books():
    return {"books":BOOK_DATABASE}

# /book-by-index/{index: int}
@app.get("/book-by-index/{index}")
async def book_by_index(index: int):
    if index < 0 or index >= len(BOOK_DATABASE):
        raise HTTPException(404, f"Index {index} is out of range {len(BOOK_DATABASE)}") 
    else:
        return {"books":BOOK_DATABASE[index]}

# /add-book
@app.post("/add-book")
async def add_book(book: Book):
    book.book_id = uuid4().hex
    json_book = jsonable_encoder(book)
    BOOK_DATABASE.append(json_book)
    with open(BOOKS_FILE, "w") as fp:
        json.dump(BOOK_DATABASE, fp)
    return {"message": f"Book {book} was added"}

# /get-book?id=XYZ
@app.get("/get-book")
async def get_book(book_id: str):
    for book in BOOK_DATABASE:
        if book["book_id"] == book_id:
            return book
        
    raise HTTPException(404, f"Book id {book_id} not found") 

@app.get("/")
async def root():
    return {"message": "Hello World"}