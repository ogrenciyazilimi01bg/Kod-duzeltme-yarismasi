"""
Mini Kütüphane 2.0
- Kitap ekleme, ödünç alma, iade etme
- Arama ve gecikenleri listeleme
- Kaydet/Yükle (JSON)

Öğrenci Görevleri:
1) BUGFIX bölümlerindeki hataları düzeltin.
2) TODO bölümlerini talimatlara göre doldurun.
3) tests.py dosyasını çalıştırarak doğrulayın.
"""

from datetime import datetime, timedelta
import json
from typing import List, Dict, Optional
import os

def _today_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def _in_days_str(days: int) -> str:
    return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")


# ---------------------------
# ÖRNEK VERİ
# ---------------------------
BOOKS: List[Dict] = [
    {"id": 1, "title": "Dune", "author": "Frank Herbert", "available": True,  "borrower": None, "due_date": None},
    {"id": 2, "title": "Kürk Mantolu Madonna", "author": "Sabahattin Ali", "available": True,  "borrower": None, "due_date": None},
    {"id": 3, "title": "1984", "author": "George Orwell", "available": False, "borrower": "ayse", "due_date": _in_days_str(-2)},  # gecikmiş örnek
]


# -------------------------------------------------
# GÖREV 1 — BUGFIX: kitap ID üretimindeki hata
# -------------------------------------------------
# Amaç: yeni kitap eklerken benzersiz ID ver.
# HATA: Maksimum ID'yi yanlış hesaplıyor, listedeki
#       son elemana bakıyor. Liste sırası değişirse patlar.
#       Ayrıca boş liste durumunu da bozuk ele alıyor.

def _next_book_id(books: List[Dict]) -> int:
    """ Yeni kitap eklenirken benzersiz ID üretir."""
    if not books:
        
        return 1
    else:
        
        max_id = max(book["id"] for book in books)
        return max_id + 1

# -------------------------------------------------
# GÖREV 2 — Fonksiyon: kitap ekle
# -------------------------------------------------
def add_book(books: List[Dict], title: str, author: str) -> Dict:
    """
    Yeni bir kitap ekler ve eklenen kitabı döner.
    - title/author boş bırakılamaz (boşsa ValueError)
    - available True, borrower/due_date None
    """
    
    if not title or not title.strip():
        raise ValueError("Kitap başlığı boş olamaz.")
    if not author or not author.strip():
        raise ValueError("Yazar adı boş olamaz.")

   
    new_id = _next_book_id(books)

    
    new_book = {
        "id": new_id,
        "title": title.strip(),
        "author": author.strip(),
        "available": True,
        "borrower": None,
        "due_date": None
    }

   
    books.append(new_book)

    return new_book
# -------------------------------------------------
# GÖREV 3 — BUGFIX: arama hataları
# -------------------------------------------------
def search_books(books: List[Dict], query: str) -> List[Dict]:
    """
    Başlık ya da yazarda 'query' geçenleri (case-insensitive) döndürür.
    Boş query -> boş liste.
    """
    if not query or not query.strip():
        return []

    q = query.strip().lower()
    return [
        b for b in books
        if (b.get("title") or "").lower().find(q) != -1
        or (b.get("author") or "").lower().find(q) != -1
    ]




    # -------------------------------------------------
# GÖREV 4 — Fonksiyon: ödünç alma
# -------------------------------------------------
def borrow_book(books: List[Dict], book_id: int, username: str, days: int = 14) -> bool:
    """
    book_id'li kitabı 'username' adına 'days' günlüğüne ayırır.
    Dönüş: True (başarılı) / False (kitap zaten müsait değil ya da yok)
    """
    for book in books:
        if book["id"] == book_id:
            if book["available"]:
                book["available"] = False
                book["borrower"] = username
                book["due_date"] = _in_days_str(days)
                return True
            else:
                return False
    return False  # ID eşleşen kitap yoksa



# -------------------------------------------------
# GÖREV 5 — Fonksiyon: iade etme
# -------------------------------------------------
def return_book(books: List[Dict], book_id: int) -> bool:
    """
    Kitabı iade eder; bulunursa alanları sıfırlar.
    True/False döner.
    """
    for book in books:
        if book["id"] == book_id:
            book["available"] = True
            book["borrower"] = None
            book["due_date"] = None
            return True
    return False  # Kitap bulunamazsa



# -------------------------------------------------
# GÖREV 6 — Gecikenleri listele
# -------------------------------------------------
def list_overdue(books: List[Dict], today: Optional[str] = None) -> List[Dict]:
    """
    'today' (YYYY-MM-DD) tarihine göre geciken kitapları döndür.
    Notlar:
      - available True olanlar gecikmiş sayılmaz
      - due_date None olanlar da değil
    """
    if today is None:
        today = _today_str()

    overdue = []
    for book in books:
        due = book.get("due_date")
        if due and not book.get("available", True) and due < today:
            overdue.append(book)
    return overdue



# -------------------------------------------------
# GÖREV 7 — Kaydet/Yükle (JSON)
# -------------------------------------------------
def save_to_file(books: List[Dict], path: str) -> None:
    """
    books listesini path'e JSON olarak kaydeder (UTF-8).
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)


def load_from_file(path: str) -> List[Dict]:
    """
    path'teki JSON içeriğini okuyup kitap listesi döndürür.
    Dosya yoksa boş liste döndür.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


# -------------------------------------------------
# Yardımcı CLI (isteğe bağlı)
# -------------------------------------------------
def _demo():
    print("Demo: kitap ara 'an'")
    print(search_books(BOOKS, "an"))

if __name__ == "__main__":
    _demo()

