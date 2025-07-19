from fastapi import APIRouter, HTTPException, BackgroundTasks
from api.models import Book
import sqlite3
import pandas as pd
from typing import List, Optional
import base64

# Importa sua função de scraping
from scraping.books import download_catalogue_data

router = APIRouter(prefix="/api/v1/books", tags=["Books"])

DB_PATH = "books.db"

def get_db_connection():
    """Cria conexão com o banco SQLite"""
    return sqlite3.connect(DB_PATH)

def get_books_from_db(limit: Optional[int] = None, category: Optional[str] = None) -> List[dict]:
    """Busca livros do banco de dados"""
    query = "SELECT * FROM books"
    params = []
    
    if category:
        query += " WHERE category = ?"
        params.append(category)
    
    if limit:
        query += f" LIMIT {limit}"
    
    with get_db_connection() as conn:
        df = pd.read_sql_query(query, conn, params=params)
        return df.to_dict('records')

def book_exists_in_db(book_id: int) -> bool:
    """Verifica se um livro existe no banco"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM books WHERE rowid = ?", (book_id,))
        return cursor.fetchone()[0] > 0

@router.get("/", response_model=List[Book])
def list_books(limit: Optional[int] = None, category: Optional[str] = None):
    """Lista todos os livros ou filtra por categoria"""
    try:
        books_data = get_books_from_db(limit=limit, category=category)
        
        books = []
        for i, book_data in enumerate(books_data, 1):
            # Converte bytes da imagem para base64 se necessário
            cover_data = book_data.get('cover')
            if isinstance(cover_data, bytes):
                cover_b64 = base64.b64encode(cover_data).decode('utf-8')
            else:
                cover_b64 = cover_data
            
            book = Book(
                id=i,  # ou rowid se quiser
                title=book_data['title'],
                price=book_data['price'],
                rating=book_data['rating'],
                stock=book_data['stock'],
                category=book_data.get('category', ''),
                cover=cover_b64
            )
            books.append(book)
        
        return books
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar livros: {str(e)}")

@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int):
    """Busca um livro específico pelo ID"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books WHERE rowid = ?", (book_id,))
            book_data = cursor.fetchone()
            
            if not book_data:
                raise HTTPException(status_code=404, detail="Book not found")
            
            # Pega os nomes das colunas
            columns = [description[0] for description in cursor.description]
            book_dict = dict(zip(columns, book_data))
            
            # Converte bytes da imagem para base64 se necessário
            cover_data = book_dict.get('cover')
            if isinstance(cover_data, bytes):
                cover_b64 = base64.b64encode(cover_data).decode('utf-8')
            else:
                cover_b64 = cover_data
            
            book = Book(
                id=book_id,
                title=book_dict['title'],
                price=book_dict['price'],
                rating=book_dict['rating'],
                stock=book_dict['stock'],
                category=book_dict.get('category', ''),
                cover=cover_b64
            )
            
            return book
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar livro: {str(e)}")

@router.get("/categories/", response_model=List[str])
def list_categories():
    """Lista todas as categorias disponíveis"""
    try:
        with get_db_connection() as conn:
            df = pd.read_sql_query("SELECT DISTINCT category FROM books WHERE category IS NOT NULL", conn)
            categories = sorted(df['category'].tolist())
            return categories
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar categorias: {str(e)}")


