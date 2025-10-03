# 🎙️ Sistem Print Berbasis Assistant (Voice PDF Printer)

Aplikasi desktop berbasis Python yang memungkinkan Anda mencetak file PDF menggunakan perintah suara. Cukup ucapkan "Halo Ella" dan sebutkan nama file yang ingin dicetak!

## ✨ Fitur

- 🎤 **Voice Recognition**: Mengenali perintah suara dalam Bahasa Indonesia
- 🤖 **Text-to-Speech**: Respon suara dari asisten menggunakan Google TTS
- 🖨️ **Auto Print**: Mencetak PDF secara otomatis ke printer default
- 📁 **Fuzzy Matching**: Menemukan file meskipun pengucapan tidak 100% tepat
- 🖥️ **GUI Interface**: Antarmuka grafis sederhana dengan log real-time

## 📋 Prasyarat

- Python 3.7 atau lebih baru
- Mikrofon yang berfungsi
- Koneksi internet (untuk speech recognition)
- Windows OS (untuk fitur print otomatis)
- Salah satu PDF reader: Adobe Reader atau SumatraPDF (opsional, untuk auto-print)

## 🚀 Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/wildanmkhdev/Sistem-Print-Berbasis-Asistant.git
cd Sistem-Print-Berbasis-Asistant
```

### 2. Buat Virtual Environment (Opsional tapi Disarankan)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Atau install secara manual:

```bash
pip install speechrecognition
pip install gtts
pip install playsound
pip install rapidfuzz
pip install pyaudio
```

**Note**: Jika `pyaudio` gagal install di Windows, download wheel file dari [sini](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) dan install dengan:

```bash
pip install PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl
```

Sesuaikan versi Python dan sistem operasi Anda.

### 4. Install PDF Reader (Opsional)

Untuk auto-print yang lebih baik, install salah satu:

- **Adobe Reader**: [Download](https://get.adobe.com/reader/)
- **SumatraPDF**: [Download](https://www.sumatrapdfreader.org/download-free-pdf-viewer)

## 📁 Struktur Folder

```
Sistem-Print-Berbasis-Asistant/
│
├── main.py                 # File utama aplikasi
├── pdf_files/              # Folder untuk menyimpan file PDF
│   ├── dokumen1.pdf
│   ├── surat.pdf
│   └── ...
├── requirements.txt        # Daftar dependencies
└── README.md              # Dokumentasi
```

## 🎯 Cara Menggunakan

### 1. Persiapkan File PDF

Letakkan file PDF yang ingin dicetak di folder `pdf_files/`:

```bash
mkdir pdf_files
# Copy file PDF Anda ke folder ini
```

### 2. Jalankan Aplikasi

```bash
python main.py
```

### 3. Aktifkan Listener

- Klik tombol **"ON"** pada GUI
- Tunggu sampai muncul pesan "Listener aktif"

### 4. Gunakan Perintah Suara

1. Ucapkan: **"Halo Ella"**
2. Tunggu respon dari asisten
3. Sebutkan **nama file PDF** yang ingin dicetak
4. File akan otomatis tercetak!

**Contoh:**
```
Anda: "Halo Ella"
Asisten: "Siap, sebutkan nama file PDF yang ingin dicetak."
Anda: "Surat lamaran"
Asisten: "Oke, saya print file surat_lamaran.pdf"
```

### 5. Matikan Listener

- Klik tombol **"OFF"** untuk menghentikan

## 🔧 Troubleshooting

### Mikrofon Tidak Terdeteksi

```python
# Test mikrofon dengan:
import speech_recognition as sr
print(sr.Microphone.list_microphone_names())
```

### Error PyAudio

Untuk Windows, install PyAudio dari wheel file atau gunakan pipwin:

```bash
pip install pipwin
pipwin install pyaudio
```

### Error Playsound

Jika playsound error, gunakan alternatif:

```bash
pip uninstall playsound
pip install playsound==1.2.2
```

### File Tidak Ditemukan

- Pastikan file PDF ada di folder `pdf_files/`
- Ucapkan nama file dengan jelas
- Sistem menggunakan fuzzy matching, jadi tidak perlu 100% tepat

## 📝 Requirements.txt

Buat file `requirements.txt` dengan isi:

```
SpeechRecognition==3.10.0
gTTS==2.3.2
playsound==1.2.2
rapidfuzz==3.5.2
PyAudio==0.2.13
```

## 🛠️ Teknologi yang Digunakan

- **Python 3.x**: Bahasa pemrograman utama
- **SpeechRecognition**: Google Speech API untuk voice recognition
- **gTTS**: Google Text-to-Speech untuk respon suara
- **RapidFuzz**: Fuzzy string matching untuk mencocokkan nama file
- **Tkinter**: GUI framework bawaan Python
- **PyAudio**: Audio I/O untuk mikrofon
- **Playsound**: Memutar audio TTS

## 📱 Screenshot

```
┌─────────────────────────────┐
│   Voice PDF Printer         │
├─────────────────────────────┤
│      [   ON   ]             │
│      [  OFF   ]             │
├─────────────────────────────┤
│  Log Area:                  │
│  [🤖] Listener aktif...     │
│  [🎤] Kamu bilang: halo ella│
│  [🖨️] Mencetak: surat.pdf  │
│                             │
└─────────────────────────────┘
```

## 🤝 Kontribusi

Kontribusi sangat diterima! Silakan:

1. Fork repository ini
2. Buat branch fitur (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📄 Lisensi

Distributed under the MIT License. See `LICENSE` for more information.

## 👨‍💻 Author

**Wildan MKH**
- GitHub: [@wildanmkhdev](https://github.com/wildanmkhdev)

## 🙏 Acknowledgments

- Google Speech Recognition API
- Google Text-to-Speech
- Python Community

---

⭐ Jangan lupa berikan star jika project ini membantu Anda!