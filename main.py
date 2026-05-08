"""
main.py
Entry point aplikasi Personal Finance Tracker.
Berisi menu interaktif untuk navigasi fitur.
"""

from finance_manager import FinanceManager

# Inisialisasi manager di level modul agar bisa diakses semua fungsi
manager = FinanceManager()


def clear_screen():
    """Membersihkan layar terminal (cross-platform)."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title):
    """Menampilkan header dengan format yang rapi."""
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)


def print_line():
    """Menampilkan garis pemisah."""
    print("-" * 50)


def format_currency(amount):
    """Format angka menjadi format mata uang Indonesia."""
    return f"Rp {amount:,.0f}".replace(",", ".")


def pause():
    """Menunggu user menekan Enter untuk melanjutkan."""
    input("\nTekan Enter untuk melanjutkan...")


# ==================== MENU TRANSAKSI ====================

def add_transaction_menu():
    """Menu untuk menambah transaksi baru."""
    print_header("TAMBAH TRANSAKSI")
    
    # Pilih tipe transaksi
    print("\nTipe Transaksi:")
    print("  1. Pemasukan (Income)")
    print("  2. Pengeluaran (Expense)")
    
    choice = input("\nPilih [1/2]: ").strip()
    
    if choice == "1":
        trans_type = "income"
        type_label = "Pemasukan"
    elif choice == "2":
        trans_type = "expense"
        type_label = "Pengeluaran"
    else:
        print("Pilihan tidak valid!")
        return
    
    # Tampilkan kategori yang tersedia
    categories = manager.get_categories(trans_type)
    print(f"\nKategori {type_label}:")
    for i, cat in enumerate(categories, 1):
        print(f"  {i}. {cat}")
    
    # Pilih kategori
    try:
        cat_choice = int(input("\nPilih nomor kategori: ")) - 1
        if 0 <= cat_choice < len(categories):
            category = categories[cat_choice]
        else:
            print("Nomor kategori tidak valid!")
            return
    except ValueError:
        print("Input harus berupa angka!")
        return
    
    # Input jumlah uang
    try:
        amount = float(input("Jumlah (Rp): ").replace(".", "").replace(",", ""))
        if amount <= 0:
            print("Jumlah harus lebih dari 0!")
            return
    except ValueError:
        print("Input jumlah tidak valid!")
        return
    
    # Input deskripsi (opsional)
    description = input("Deskripsi (opsional, tekan Enter untuk skip): ").strip()
    
    # Simpan transaksi
    trans = manager.add_transaction(trans_type, category, amount, description)
    
    print_line()
    print("✓ Transaksi berhasil ditambahkan!")
    print(f"  Tipe     : {type_label}")
    print(f"  Kategori : {category}")
    print(f"  Jumlah   : {format_currency(amount)}")
    if description:
        print(f"  Deskripsi: {description}")


def view_transactions_menu():
    """Menu untuk melihat semua transaksi."""
    print_header("DAFTAR TRANSAKSI")
    
    transactions = manager.get_all_transactions()
    
    if not transactions:
        print("\nBelum ada transaksi.")
        return
    
    # Header tabel
    print(f"\n{'No':<4} {'Tanggal':<12} {'Tipe':<12} {'Kategori':<15} {'Jumlah':>15} {'Deskripsi':<20}")
    print_line()
    
    # Tampilkan setiap transaksi
    for i, trans in enumerate(transactions, 1):
        date_short = trans["date"][:10]  # Ambil tanggal saja (tanpa waktu)
        type_label = "Pemasukan" if trans["type"] == "income" else "Pengeluaran"
        amount_str = format_currency(trans["amount"])
        desc = trans.get("description", "")[:18]  # Potong jika terlalu panjang
        
        # Warna berbeda untuk income/expense (menggunakan prefix +/-)
        prefix = "+" if trans["type"] == "income" else "-"
        
        print(f"{i:<4} {date_short:<12} {type_label:<12} {trans['category']:<15} {prefix + amount_str:>15} {desc:<20}")
    
    print_line()
    print(f"Total: {len(transactions)} transaksi")


def delete_transaction_menu():
    """Menu untuk menghapus transaksi."""
    print_header("HAPUS TRANSAKSI")
    
    transactions = manager.get_all_transactions()
    
    if not transactions:
        print("\nBelum ada transaksi untuk dihapus.")
        return
    
    # Tampilkan daftar transaksi dengan nomor
    print(f"\n{'No':<4} {'Tanggal':<12} {'Kategori':<15} {'Jumlah':>15}")
    print_line()
    
    for i, trans in enumerate(transactions, 1):
        date_short = trans["date"][:10]
        amount_str = format_currency(trans["amount"])
        prefix = "+" if trans["type"] == "income" else "-"
        print(f"{i:<4} {date_short:<12} {trans['category']:<15} {prefix + amount_str:>15}")
    
    print_line()
    
    # Pilih transaksi yang akan dihapus
    try:
        choice = int(input("\nNomor transaksi yang akan dihapus (0 untuk batal): "))
        if choice == 0:
            return
        if 1 <= choice <= len(transactions):
            trans_to_delete = transactions[choice - 1]
            
            # Konfirmasi penghapusan
            confirm = input(f"Hapus transaksi {trans_to_delete['category']} - {format_currency(trans_to_delete['amount'])}? [y/n]: ")
            
            if confirm.lower() == 'y':
                if manager.delete_transaction(trans_to_delete["id"]):
                    print("✓ Transaksi berhasil dihapus!")
                else:
                    print("Gagal menghapus transaksi.")
        else:
            print("Nomor tidak valid!")
    except ValueError:
        print("Input harus berupa angka!")


def update_transaction_menu():
    """Menu untuk mengupdate transaksi."""
    print_header("UPDATE TRANSAKSI")
    
    transactions = manager.get_all_transactions()
    
    if not transactions:
        print("\nBelum ada transaksi untuk diupdate.")
        return
    
    # Tampilkan daftar transaksi
    print(f"\n{'No':<4} {'Tanggal':<12} {'Kategori':<15} {'Jumlah':>15} {'Deskripsi':<20}")
    print_line()
    
    for i, trans in enumerate(transactions, 1):
        date_short = trans["date"][:10]
        amount_str = format_currency(trans["amount"])
        desc = trans.get("description", "")[:18]
        print(f"{i:<4} {date_short:<12} {trans['category']:<15} {amount_str:>15} {desc:<20}")
    
    print_line()
    
    try:
        choice = int(input("\nNomor transaksi yang akan diupdate (0 untuk batal): "))
        if choice == 0:
            return
        if 1 <= choice <= len(transactions):
            trans = transactions[choice - 1]
            
            print(f"\nUpdate transaksi: {trans['category']} - {format_currency(trans['amount'])}")
            print("(Tekan Enter untuk tidak mengubah field)\n")
            
            # Input field baru
            new_amount = input(f"Jumlah baru [{format_currency(trans['amount'])}]: ").strip()
            new_desc = input(f"Deskripsi baru [{trans.get('description', '')}]: ").strip()
            
            # Siapkan data update
            updates = {}
            if new_amount:
                try:
                    updates["amount"] = float(new_amount.replace(".", "").replace(",", ""))
                except ValueError:
                    print("Jumlah tidak valid, tidak diubah.")
            if new_desc:
                updates["description"] = new_desc
            
            if updates:
                if manager.update_transaction(trans["id"], **updates):
                    print("✓ Transaksi berhasil diupdate!")
                else:
                    print("Gagal mengupdate transaksi.")
            else:
                print("Tidak ada perubahan.")
        else:
            print("Nomor tidak valid!")
    except ValueError:
        print("Input harus berupa angka!")


# ==================== MENU KATEGORI ====================

def manage_categories_menu():
    """Menu utama untuk manajemen kategori."""
    while True:
        print_header("MANAJEMEN KATEGORI")
        
        print("\n1. Lihat Kategori")
        print("2. Tambah Kategori")
        print("3. Hapus Kategori")
        print("0. Kembali")
        
        choice = input("\nPilih menu: ").strip()
        
        if choice == "1":
            view_categories()
        elif choice == "2":
            add_category_menu()
        elif choice == "3":
            delete_category_menu()
        elif choice == "0":
            break
        else:
            print("Pilihan tidak valid!")
        
        pause()


def view_categories():
    """Menampilkan semua kategori."""
    print_header("DAFTAR KATEGORI")
    
    print("\n[PEMASUKAN]")
    for i, cat in enumerate(manager.get_categories("income"), 1):
        print(f"  {i}. {cat}")
    
    print("\n[PENGELUARAN]")
    for i, cat in enumerate(manager.get_categories("expense"), 1):
        print(f"  {i}. {cat}")


def add_category_menu():
    """Menu untuk menambah kategori baru."""
    print_header("TAMBAH KATEGORI")
    
    print("\nTipe kategori:")
    print("  1. Pemasukan (Income)")
    print("  2. Pengeluaran (Expense)")
    
    choice = input("\nPilih [1/2]: ").strip()
    
    if choice == "1":
        trans_type = "income"
    elif choice == "2":
        trans_type = "expense"
    else:
        print("Pilihan tidak valid!")
        return
    
    # Tampilkan kategori yang sudah ada
    print(f"\nKategori yang sudah ada:")
    for cat in manager.get_categories(trans_type):
        print(f"  - {cat}")
    
    # Input nama kategori baru
    new_cat = input("\nNama kategori baru: ").strip()
    
    # Proses penambahan
    success, message = manager.add_category(trans_type, new_cat)
    if success:
        print(f"✓ {message}")
    else:
        print(f"✗ {message}")


def delete_category_menu():
    """Menu untuk menghapus kategori."""
    print_header("HAPUS KATEGORI")
    
    print("\nTipe kategori:")
    print("  1. Pemasukan (Income)")
    print("  2. Pengeluaran (Expense)")
    
    choice = input("\nPilih [1/2]: ").strip()
    
    if choice == "1":
        trans_type = "income"
    elif choice == "2":
        trans_type = "expense"
    else:
        print("Pilihan tidak valid!")
        return
    
    # Tampilkan kategori yang ada
    categories = manager.get_categories(trans_type)
    print(f"\nKategori yang tersedia:")
    for i, cat in enumerate(categories, 1):
        print(f"  {i}. {cat}")
    
    # Pilih kategori untuk dihapus
    try:
        cat_choice = int(input("\nNomor kategori yang akan dihapus (0 untuk batal): "))
        if cat_choice == 0:
            return
        if 1 <= cat_choice <= len(categories):
            cat_name = categories[cat_choice - 1]
            success, message = manager.delete_category(trans_type, cat_name)
            if success:
                print(f"✓ {message}")
            else:
                print(f"✗ {message}")
        else:
            print("Nomor tidak valid!")
    except ValueError:
        print("Input harus berupa angka!")


# ==================== MENU RINGKASAN ====================

def show_summary():
    """Menampilkan ringkasan keuangan."""
    print_header("RINGKASAN KEUANGAN")
    
    summary = manager.get_summary()
    
    print(f"\n  Total Pemasukan  : {format_currency(summary['total_income'])}")
    print(f"  Total Pengeluaran: {format_currency(summary['total_expense'])}")
    print_line()
    
    # Saldo dengan indikator positif/negatif
    balance = summary['balance']
    if balance >= 0:
        print(f"  SALDO            : {format_currency(balance)} ✓")
    else:
        print(f"  SALDO            : -{format_currency(abs(balance))} ⚠")
    
    # Ringkasan per kategori
    print("\n\n[PEMASUKAN PER KATEGORI]")
    income_by_cat = manager.get_summary_by_category("income")
    if income_by_cat:
        for cat, amount in sorted(income_by_cat.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat:<20} {format_currency(amount):>15}")
    else:
        print("  Belum ada data.")
    
    print("\n[PENGELUARAN PER KATEGORI]")
    expense_by_cat = manager.get_summary_by_category("expense")
    if expense_by_cat:
        for cat, amount in sorted(expense_by_cat.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat:<20} {format_currency(amount):>15}")
    else:
        print("  Belum ada data.")


# ==================== MENU UTAMA ====================

def main_menu():
    """Menu utama aplikasi."""
    while True:
        clear_screen()
        print_header("PERSONAL FINANCE TRACKER")
        
        print("\n  1. Tambah Transaksi")
        print("  2. Lihat Transaksi")
        print("  3. Update Transaksi")
        print("  4. Hapus Transaksi")
        print("  5. Manajemen Kategori")
        print("  6. Ringkasan Keuangan")
        print("  0. Keluar")
        
        print_line()
        choice = input("Pilih menu: ").strip()
        
        if choice == "1":
            add_transaction_menu()
        elif choice == "2":
            view_transactions_menu()
        elif choice == "3":
            update_transaction_menu()
        elif choice == "4":
            delete_transaction_menu()
        elif choice == "5":
            manage_categories_menu()
        elif choice == "6":
            show_summary()
        elif choice == "0":
            print("\nTerima kasih telah menggunakan Personal Finance Tracker!")
            print("Sampai jumpa! 👋\n")
            break
        else:
            print("Pilihan tidak valid!")
        
        if choice != "0":
            pause()


# Entry point: jalankan menu utama saat file dieksekusi langsung
if __name__ == "__main__":
    main_menu()
