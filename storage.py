"""
storage.py
Modul untuk menyimpan dan memuat data ke/dari file JSON.
"""

import json
import os

# Nama file untuk menyimpan data transaksi dan kategori
DATA_FILE = "finance_data.json"


def load_data():
    """
    Memuat data dari file JSON.
    Jika file tidak ada atau kosong, kembalikan struktur data default.
    
    Returns:
        dict: Data yang berisi 'transactions' dan 'categories'
    """
    # Struktur default jika belum ada data
    default_data = {
        "transactions": [],  # List untuk menyimpan semua transaksi
        "categories": {
            "income": ["Gaji", "Freelance", "Investasi", "Lainnya"],  # Kategori pemasukan default
            "expense": ["Makanan", "Transportasi", "Belanja", "Tagihan", "Hiburan", "Lainnya"]  # Kategori pengeluaran default
        }
    }
    
    # Cek apakah file data sudah ada
    if not os.path.exists(DATA_FILE):
        return default_data
    
    try:
        # Buka dan baca file JSON
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            # Pastikan struktur data lengkap (untuk backward compatibility)
            if "transactions" not in data:
                data["transactions"] = []
            if "categories" not in data:
                data["categories"] = default_data["categories"]
            return data
    except (json.JSONDecodeError, FileNotFoundError):
        # Jika file rusak atau tidak bisa dibaca, kembalikan default
        return default_data


def save_data(data):
    """
    Menyimpan data ke file JSON.
    
    Args:
        data (dict): Data yang akan disimpan (transactions dan categories)
    """
    # indent=2 membuat file JSON mudah dibaca manusia
    # ensure_ascii=False agar karakter non-ASCII (seperti huruf Indonesia) tersimpan dengan benar
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
