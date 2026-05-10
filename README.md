```markdown
# 💰 FinTrack CLI – Personal Finance Tracker

> Kelola pengeluaran dan pemasukan langsung dari terminal Linuxmu.  
> Cocok buat mahasiswa IT yang ingin punya kebiasaan finansial sehat tanpa ribet.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![JSON](https://img.shields.io/badge/storage-JSON-lightgrey) ![CLI](https://img.shields.io/badge/interface-CLI-green)

---

## 📖 Deskripsi

**FinTrack CLI** adalah aplikasi pengelola keuangan pribadi berbasis baris perintah (CLI) yang memungkinkan kamu mencatat pemasukan, pengeluaran, dan kategori secara **kustom**. Data disimpan secara permanen dalam file JSON, jadi tetap aman meskipun terminal ditutup.

Ideal untuk kamu yang terbiasa dengan Linux Mint XFCE (atau distro lain) dan ingin belajar konsep CRUD + manajemen file tanpa dependensi database eksternal.

---

## 🚀 Panduan Instalasi & Menjalankan

### 1. Clone repositori
```bash
git clone https://github.com/username/fintrack-cli.git
cd fintrack-cli
```

### 2. Jalankan aplikasi
Pastikan Python 3 terinstal (`python3 --version`). Lalu:
```bash
python3 main.py
```

> **Catatan:** File `data.json` akan dibuat secara otomatis saat pertama kali menjalankan program.

---

## ✨ Fitur Utama

| Fitur | Deskripsi |
|-------|------------|
| ➕ **Tambah transaksi** | Input pemasukan/pengeluaran dengan nominal, deskripsi, dan kategori |
| 👁️ **Lihat semua transaksi** | Tampilkan riwayat dalam tabel rapi di terminal |
| 🗑️ **Hapus transaksi** | Hapus berdasarkan ID unik |
| 🏷️ **Kategori kustom** | Kamu bisa **tambah kategori sendiri** (misal: `Olahraga`, `Skripsi`, `Healing`) – tidak terbatas! |
| 💾 **Penyimpanan JSON** | Semua data tersimpan di `data.json`, mudah dicadangkan atau diedit manual |

> 🌟 Nilai tambah: Bebas menentukan kategori sesuai gaya hidupmu, tidak seperti aplikasi lain yang hanya menyediakan pilihan terbatas.

---

## 📁 Struktur Folder

```
fintrack-cli/
│
├── main.py              # Entry point CLI (menu utama)
├── finance_manager.py   # Logika bisnis: menambah, lihat, hapus transaksi
├── storage.py           # Baca & tulis data ke file JSON
├── data.json            # File penyimpanan (otomatis dibuat)
└── README.md            # Ini dia
```

**Penjelasan singkat:**

- `main.py` → Tampilan menu dan interaksi dengan user.  
- `finance_manager.py` → Mengelola data transaksi di memori (list/dict).  
- `storage.py` → Fungsi `load_data()` dan `save_data()` untuk persistent storage.  
- `data.json` → Tempat semua catatan keuanganmu disimpan.

---

## 🧪 Contoh Penggunaan

```bash
$ python3 main.py

===== FinTrack CLI =====
1. Tambah Transaksi
2. Lihat Semua Transaksi
3. Hapus Transaksi
4. Kelola Kategori
5. Keluar

Pilih menu: 1

Masukkan deskripsi: Beli kopi
Masukkan nominal: 15000
Pilih kategori (atau ketik 'tambah' untuk baru): tambah
Nama kategori baru: Cafe
[Sukses] Transaksi ditambahkan!
```

---

## 🔮 Rencana Update (V2 – Web Version)

Kami sedang mengembangkan **FinTrack Web** menggunakan **Flask** + **Bootstrap**. Rencana fitur:

- Dashboard grafik pengeluaran mingguan  
- Export ke CSV/PDF  
- Multi-user (login sederhana)  
- Mode dark/light  

> Ikuti terus repository ini untuk kabar terbaru. PR & ide selalu terbuka!

---

## 🛠️ Tech Stack

- **Python 3.8+** – Logika utama  
- **JSON** – Penyimpanan data offline  
- **OS & sys module** – Interaksi file dan CLI  
- **Tabulate** (optional) – Untuk tabel terminal yang rapi (bisa ditambahkan di masa depan)

> Saat ini hanya menggunakan library bawaan Python, jadi **tanpa instalasi tambahan**.

---

## 🤝 Kontribusi

Pull request sangat dipersilakan! Jika kamu punya ide untuk:
- Filter transaksi berdasarkan tanggal  
- Laporan bulanan otomatis  
- Animasi loading yang keren di terminal  

Langsung fork dan buat PR ya. Jangan lupa bintangi ⭐ repositori ini jika terbantu.

---

## 📜 Lisensi

MIT License – bebas digunakan, dimodifikasi, dan disebarluaskan.

---

**Dibuat dengan ☕ dan terminal di Linux Mint XFCE**  
*Keep track, stay wealthy!*
