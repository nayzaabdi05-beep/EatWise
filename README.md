# 🥗 Dashboard Analisis Nutrisi & Rekomendasi Makanan Sehat

Proyek ini merupakan dashboard interaktif untuk menganalisis pola konsumsi makanan pengguna berdasarkan kandungan nutrisi, ambang batas kalori harian, dan klaster kategori makanan. Dashboard ini dibuat menggunakan Streamlit dan didasarkan pada dataset nutrisi makanan lokal Indonesia.

## Pertanyaan Bisnis
1. Bagaimana EatWise dapat mengidentifikasi pola konsumsi makanan yang menyebabkan pengguna melebihi **30% kebutuhan kalori atau lemak harian** dalam periode 7 hari berdasarkan integrasi data nutrisi dan histori konsumsi pengguna?
2. Bagaimana EatWise dapat merekomendasikan alternatif makanan dalam kategori yang sama yang memiliki kandungan kalori, gula, atau lemak **minimal 20% lebih rendah** berdasarkan data nutrisi makanan?

## 📌 Fitur Utama
- **Ringkasan Metrik:** Menampilkan total jenis makanan, rata-rata health score, jumlah makanan berisiko, dan persentase makanan waspada secara real-time berdasarkan filter.
- **EDA & Visualisasi:** Scatter plot interaktif kalori vs lemak berdasarkan klaster kategori nutrisi untuk mengidentifikasi pengelompokan makanan.
- **Pola Konsumsi 7 Hari:** Input asupan kalori harian dan visualisasi tren mingguan vs ambang batas 30% di atas target.
- **Rekomendasi Sehat:** Pilih makanan yang ingin diganti dan dapatkan 5 alternatif dengan kalori ≥20% lebih rendah beserta health score tertinggi.

## 📂 Struktur Proyek
```text
Capstone_EatWise/
├── dashboard.py                  # File utama dashboard Streamlit
├── nutrition.csv                 # Dataset nutrisi makanan mentah (raw)
├── eatwise_final_dataset.csv     # Dataset final hasil feature engineering & clustering
├── Capstone_EatWise.ipynb        # Notebook analisis data (EDA & Cleaning)
├── README.md                     # Dokumentasi proyek
└── requirements.txt              # Daftar library Python yang dibutuhkan
```

### Alur Analisis

## Data Wrangling:
- **Gathering Data:** Memuat dataset `nutrition.csv` dengan delimiter `;`.
- **Assessing Data:** Memeriksa missing values, data duplikat, dan tipe data yang tidak sesuai pada kolom nutrisi (calories, proteins, fat, carbohydrate).
- **Cleaning Data:** Mengisi nilai kosong pada kolom nutrisi dengan 0, menghapus baris tanpa nama makanan, mengonversi kolom nutrisi ke tipe numerik (float), dan membersihkan whitespace pada nama makanan.

## Exploratory Data Analysis (EDA):
- Memvisualisasikan distribusi kalori seluruh makanan menggunakan histogram dan KDE untuk melihat persebaran dan nilai rata-rata.
- Mengidentifikasi Top 10 makanan berdasarkan kalori tertinggi dan protein tertinggi untuk memberikan label "Porsi Terkontrol".
- Menganalisis heatmap korelasi antar nutrisi (kalori, protein, lemak, karbohidrat) untuk membuktikan lemak sebagai driver utama kalori.
- **Visualization & Explanatory Analysis:**
  - Line Chart + Threshold: Menampilkan tren asupan kalori 7 hari dibandingkan target harian dan garis bahaya 30% di atasnya (Pertanyaan 1).
  - Tabel Alternatif: Menampilkan daftar makanan pengganti dengan kalori minimal 20% lebih rendah, diurutkan berdasarkan health score tertinggi (Pertanyaan 2).

### 📊 Kesimpulan
- **Analisis Pola Konsumsi:** Tanpa pemantauan aktif, pengguna berpotensi melebihi ambang batas 30% kebutuhan kalori harian, terutama pada hari Sabtu dan Minggu di mana kontrol makan cenderung lebih longgar.
- **Efektivitas Rekomendasi:** Sistem berhasil menemukan alternatif makanan dengan kalori 20% lebih rendah dari pilihan awal pengguna, mendukung perubahan perilaku makan yang lebih sehat secara bertahap.

