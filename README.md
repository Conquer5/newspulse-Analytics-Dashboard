# 📊 Strategic Policy Monitor (NewsPulse)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-red)
![AI Engine](https://img.shields.io/badge/AI-Google%20Gemini-orange)

**Strategic Policy Monitor** (sebelumnya NewsPulse) adalah dashboard intelijen pasar yang dirancang untuk memantau perkembangan kebijakan di sektor strategis Indonesia (Nikel, Batubara, Tembaga, dan EBT).

Aplikasi ini menggunakan pendekatan **Data-Driven** untuk mengukur kesenjangan antara "Wacana" (Discourse) dan "Eksekusi" (Execution) menggunakan metrik kuantitatif.

## 🚀 Fitur Utama

### 1. Policy Maturity Index (PMI) 📈
Sistem scoring otomatis (skala 1.0 - 5.0) yang mengklasifikasikan berita menjadi:
- **1.0 - 2.5 (Wacana):** Rencana, janji, atau diskusi awal.
- **2.6 - 3.9 (Kebijakan):** Regulasi terbit, MoU ditandatangani.
- **4.0 - 5.0 (Eksekusi):** Groundbreaking, produksi komersial, realisasi investasi.

### 2. Risk & Volatility Engine ⚠️
Mendeteksi anomali pasar melalui dua indikator:
- **Volatility Index:** Mengukur ketidakpastian narasi media (berita positif vs negatif yang muncul bersamaan).
- **Structural Risk:** Mengakumulasi hambatan riil (regulasi yang tumpang tindih, gugatan hukum, atau kendala fisik).

### 3. AI Strategic Briefing 🤖
Terintegrasi dengan **Google Gemini (1.5/2.0)** untuk menghasilkan analisis eksekutif secara otomatis. AI mampu:
- Meringkas ratusan berita menjadi 5 poin strategis.
- Mendeteksi validitas konsensus media (mencegah *echo chamber*).
- Memberikan rekomendasi taktis bagi stakeholder.

### 4. Interactive Visualization
- **Sunburst Chart:** Melihat distribusi isu (misal: porsi isu Lingkungan vs Investasi).
- **Dual-Axis Chart:** Korelasi antara kenaikan risiko dan penurunan momentum kebijakan.

---

## 🛠️ Teknologi & Metodologi

Dashboard ini dibangun menggunakan stack Python modern:
- **Frontend:** Streamlit (v1.30+)
- **Data Processing:** Pandas & NumPy
- **Visualization:** Plotly Express & Graph Objects
- **LLM Integration:** Google Generative AI SDK (Gemini Models)

**Metodologi Klasifikasi:**
Data berita diproses melalui *Taxonomy Matrix* yang memfilter:
1. **Object:** Komoditas (Nikel, Coal, etc).
2. **Domain:** Konteks (Trade, Mining, ESG).
3. **Phase:** Tahapan proyek (Plan -> Policy -> Execution).

---

## 📂 Struktur Project

```text
strategic-policy-monitor/
├── app.py                      # Main Dashboard Application
├── classified_news_matrix.csv  # Dataset Berita Terklasifikasi (Output NLP)
├── weekly_pmi_stats_matrix.csv # Dataset Statistik Mingguan (Time Series)
├── requirements.txt            # Dependencies
└── README.md                   # Dokumentasi Project
