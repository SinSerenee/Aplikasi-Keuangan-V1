"""
finance_manager.py
Modul berisi class FinanceManager untuk mengelola transaksi dan kategori.
"""

from datetime import datetime
from storage import load_data, save_data


class FinanceManager:
    """
    Class untuk mengelola semua operasi keuangan:
    - CRUD transaksi (Create, Read, Update, Delete)
    - Manajemen kategori kustom
    """
    
    def __init__(self):
        """Inisialisasi: muat data dari file saat objek dibuat."""
        self.data = load_data()
    
    def _save(self):
        """Method internal untuk menyimpan data ke file."""
        save_data(self.data)
    
    # ==================== CRUD TRANSAKSI ====================
    
    def add_transaction(self, trans_type, category, amount, description=""):
        """
        Menambah transaksi baru.
        
        Args:
            trans_type (str): Tipe transaksi ('income' atau 'expense')
            category (str): Kategori transaksi
            amount (float): Jumlah uang
            description (str): Deskripsi opsional
        
        Returns:
            dict: Transaksi yang baru ditambahkan
        """
        # Buat ID unik berdasarkan timestamp (miliseconds)
        transaction = {
            "id": int(datetime.now().timestamp() * 1000),
            "type": trans_type,
            "category": category,
            "amount": amount,
            "description": description,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format tanggal yang mudah dibaca
        }
        
        # Tambahkan ke list transaksi dan simpan
        self.data["transactions"].append(transaction)
        self._save()
        return transaction
    
    def get_all_transactions(self):
        """
        Mengambil semua transaksi.
        
        Returns:
            list: Semua transaksi, diurutkan dari terbaru
        """
        # Urutkan berdasarkan tanggal (terbaru di atas)
        return sorted(self.data["transactions"], key=lambda x: x["date"], reverse=True)
    
    def get_transaction_by_id(self, trans_id):
        """
        Mencari transaksi berdasarkan ID.
        
        Args:
            trans_id (int): ID transaksi yang dicari
        
        Returns:
            dict or None: Transaksi jika ditemukan, None jika tidak
        """
        for trans in self.data["transactions"]:
            if trans["id"] == trans_id:
                return trans
        return None
    
    def update_transaction(self, trans_id, **kwargs):
        """
        Mengupdate transaksi yang ada.
        
        Args:
            trans_id (int): ID transaksi yang akan diupdate
            **kwargs: Field yang akan diupdate (category, amount, description, type)
        
        Returns:
            bool: True jika berhasil, False jika transaksi tidak ditemukan
        """
        for i, trans in enumerate(self.data["transactions"]):
            if trans["id"] == trans_id:
                # Update hanya field yang diberikan
                for key, value in kwargs.items():
                    if key in ["category", "amount", "description", "type"]:
                        self.data["transactions"][i][key] = value
                # Tambahkan timestamp kapan diupdate
                self.data["transactions"][i]["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._save()
                return True
        return False
    
    def delete_transaction(self, trans_id):
        """
        Menghapus transaksi berdasarkan ID.
        
        Args:
            trans_id (int): ID transaksi yang akan dihapus
        
        Returns:
            bool: True jika berhasil, False jika tidak ditemukan
        """
        # Cari index transaksi dengan ID yang sesuai
        for i, trans in enumerate(self.data["transactions"]):
            if trans["id"] == trans_id:
                self.data["transactions"].pop(i)  # Hapus dari list
                self._save()
                return True
        return False
    
    # ==================== MANAJEMEN KATEGORI ====================
    
    def get_categories(self, trans_type):
        """
        Mengambil daftar kategori berdasarkan tipe.
        
        Args:
            trans_type (str): 'income' atau 'expense'
        
        Returns:
            list: Daftar kategori
        """
        return self.data["categories"].get(trans_type, [])
    
    def add_category(self, trans_type, category_name):
        """
        Menambah kategori baru.
        
        Args:
            trans_type (str): 'income' atau 'expense'
            category_name (str): Nama kategori baru
        
        Returns:
            tuple: (bool success, str message)
        """
        # Normalisasi: huruf pertama kapital
        category_name = category_name.strip().title()
        
        # Validasi input
        if not category_name:
            return False, "Nama kategori tidak boleh kosong"
        
        # Cek apakah kategori sudah ada (case-insensitive)
        existing = [c.lower() for c in self.data["categories"][trans_type]]
        if category_name.lower() in existing:
            return False, f"Kategori '{category_name}' sudah ada"
        
        # Tambahkan kategori baru
        self.data["categories"][trans_type].append(category_name)
        self._save()
        return True, f"Kategori '{category_name}' berhasil ditambahkan"
    
    def delete_category(self, trans_type, category_name):
        """
        Menghapus kategori.
        
        Args:
            trans_type (str): 'income' atau 'expense'
            category_name (str): Nama kategori yang akan dihapus
        
        Returns:
            tuple: (bool success, str message)
        """
        categories = self.data["categories"][trans_type]
        
        # Cari kategori (case-insensitive)
        for i, cat in enumerate(categories):
            if cat.lower() == category_name.lower():
                # Cek apakah ada transaksi yang menggunakan kategori ini
                in_use = any(
                    t["category"].lower() == category_name.lower() and t["type"] == trans_type
                    for t in self.data["transactions"]
                )
                
                if in_use:
                    return False, f"Kategori '{cat}' masih digunakan oleh beberapa transaksi"
                
                # Hapus kategori
                categories.pop(i)
                self._save()
                return True, f"Kategori '{cat}' berhasil dihapus"
        
        return False, f"Kategori '{category_name}' tidak ditemukan"
    
    # ==================== RINGKASAN & STATISTIK ====================
    
    def get_summary(self):
        """
        Menghitung ringkasan keuangan.
        
        Returns:
            dict: Total pemasukan, pengeluaran, dan saldo
        """
        total_income = sum(
            t["amount"] for t in self.data["transactions"] if t["type"] == "income"
        )
        total_expense = sum(
            t["amount"] for t in self.data["transactions"] if t["type"] == "expense"
        )
        
        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": total_income - total_expense  # Saldo = pemasukan - pengeluaran
        }
    
    def get_summary_by_category(self, trans_type):
        """
        Menghitung total per kategori.
        
        Args:
            trans_type (str): 'income' atau 'expense'
        
        Returns:
            dict: {nama_kategori: total_amount}
        """
        summary = {}
        for trans in self.data["transactions"]:
            if trans["type"] == trans_type:
                cat = trans["category"]
                # Akumulasi jumlah per kategori
                summary[cat] = summary.get(cat, 0) + trans["amount"]
        return summary
