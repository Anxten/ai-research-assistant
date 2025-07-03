# 🤖 Asisten Riset AI Otonom

Sebuah sistem agen AI otonom yang ditenagai oleh **LangGraph**. Aplikasi ini menerima sebuah topik riset yang kompleks, lalu secara mandiri membuat rencana, mencari informasi live di internet, dan menyusun laporan akhir yang terstruktur.

---

## 🎯 Studi Kasus & Masalah yang Dipecahkan

Di dunia modern, kebutuhan akan riset yang cepat, mendalam, dan komprehensif sangatlah tinggi. Proses manual untuk mencari, mengumpulkan, menyaring, dan mensintesis informasi dari berbagai sumber di internet sangat memakan waktu dan tenaga.

Aplikasi ini dirancang untuk mengotomatiskan seluruh alur kerja tersebut. Cukup dengan memberikan satu topik, sistem ini akan bertindak sebagai tim riset pribadi Anda. Studi kasus yang digunakan dalam pengembangan adalah: *"Prospek dan tantangan investasi energi terbarukan di IKN pasca 2025"*.

---

## ⚙️ Arsitektur Solusi Berbasis Agen (LangGraph)

Aplikasi ini dibangun menggunakan arsitektur *multi-agent* dengan **LangGraph**, yang memungkinkan alur kerja yang logis dan berurutan antar agen:

1.  **Planner Node (Agen Perencana):** Menerima topik utama. Tugasnya adalah memecah topik tersebut menjadi sebuah rencana riset yang detail dan terstruktur, berisi pertanyaan-pertanyaan kunci yang perlu dijawab.
2.  **Searcher Node (Agen Pencari):** Menerima rencana dari Perencana. Ia secara cerdas merumuskan *query* pencarian yang efektif, lalu menggunakan **Tavily API** untuk mencari informasi relevan secara *live* di internet.
3.  **Writer Node (Agen Penulis):** Menerima hasil riset mentah dari Pencari. Tugasnya adalah mensintesis semua informasi tersebut, menjawab pertanyaan-pertanyaan dalam rencana, dan menyusunnya menjadi sebuah laporan akhir yang koheren dan mudah dibaca.

---

## 💻 Tumpukan Teknologi (Tech Stack)

* **Python**
* **LangGraph & LangChain**: Sebagai framework utama untuk membangun alur kerja agen yang stateful.
* **Groq API (Llama 3 70B)**: Berperan sebagai "otak" atau LLM untuk semua tugas berpikir, merencanakan, dan menulis.
* **Tavily API**: Sebagai "mata" atau alat pencarian internet yang andal dan dirancang untuk AI.
* **Dotenv**: Untuk manajemen kunci API yang aman.

---

## 🚀 Instalasi & Setup

1.  **Clone repositori ini:**
    ```bash
    git clone [https://github.com/Anxten/ai-research-assistant.git](https://github.com/Anxten/ai-research-assistant.git)
    cd ai-research-assistant
    ```

2.  **Buat dan aktifkan virtual environment:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install semua library yang dibutuhkan:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Buat file `.env` dan masukkan kunci API Anda:**
    ```
    # Kunci untuk "Otak" AI (LLM)
    GROQ_API_KEY='gsk_...'

    # Kunci untuk "Mata" AI (Alat Pencari)
    TAVILY_API_KEY='tvly-...'
    ```

---

## ▶️ Cara Penggunaan

Topik riset saat ini didefinisikan di dalam file `app.py`. Untuk menjalankan, cukup eksekusi file tersebut dari terminal.

```bash
python app.py