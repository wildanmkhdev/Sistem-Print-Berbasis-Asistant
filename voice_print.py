import os
import threading
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from rapidfuzz import process
import shutil
import subprocess
import tempfile
import tkinter as tk
from tkinter import scrolledtext

# ------------------- TTS -------------------
def speak(text):
    try:
        log_message(f"[🤖] {text}")
        tmp_file = os.path.join(tempfile.gettempdir(), "voice_print.mp3")
        tts = gTTS(text=text, lang="id")
        tts.save(tmp_file)
        playsound(tmp_file)
        os.remove(tmp_file)
    except Exception as e:
        log_message(f"[ERROR TTS] {e}")

# ------------------- PRINT -------------------
def print_pdf(file_path):
    adobe_path = shutil.which("AcroRd32.exe")       # Adobe Reader
    sumatra_path = shutil.which("SumatraPDF.exe")   # SumatraPDF

    try:
        if adobe_path:
            subprocess.run([adobe_path, "/p", file_path], check=True)
            log_message(f"🖨️ Mencetak dengan Adobe Reader: {file_path}")
        elif sumatra_path:
            subprocess.run([sumatra_path, "-print-to-default", file_path], check=True)
            log_message(f"🖨️ Mencetak dengan SumatraPDF: {file_path}")
        else:
            os.startfile(file_path)
            log_message(f"📂 Tidak ada aplikasi printer khusus, membuka: {file_path}")
    except Exception as e:
        log_message(f"❌ Error saat print: {e}")

# ------------------- LIST PDF -------------------
def list_pdfs(folder="pdf_files"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    return [f for f in os.listdir(folder) if f.lower().endswith(".pdf")]

# ------------------- GUI LOG -------------------
def log_message(msg):
    log_area.config(state="normal")
    log_area.insert(tk.END, msg + "\n")
    log_area.see(tk.END)
    log_area.config(state="disabled")

# ------------------- LISTENER -------------------
def voice_listener():
    global listening
    recognizer = sr.Recognizer()
    speak("Listener aktif. Silakan ucapkan 'Halo Ella' untuk mulai print.")
    while listening:
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                text = recognizer.recognize_google(audio, language="id-ID").lower()
                log_message(f"[🎤] Kamu bilang: {text}")
                
                if "halo ella" in text:
                    speak("Siap, sebutkan nama file PDF yang ingin dicetak.")
                    # Capture file name
                    with sr.Microphone() as source2:
                        audio2 = recognizer.listen(source2, timeout=5, phrase_time_limit=5)
                        file_name = recognizer.recognize_google(audio2, language="id-ID").lower()
                        log_message(f"[🎤] Nama file: {file_name}")
                        pdfs = list_pdfs()
                        best_match, score, _ = process.extractOne(file_name, pdfs, score_cutoff=40)
                        if best_match:
                            speak(f"Oke, saya print file {best_match}")
                            file_path = os.path.join("pdf_files", best_match)
                            print_pdf(file_path)
                        else:
                            speak("Maaf, file tidak ditemukan.")
                else:
                    log_message("[INFO] Tidak ada trigger 'Halo Ella'")
        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
            log_message("[INFO] Suara tidak dikenali.")
        except sr.RequestError as e:
            log_message(f"[ERROR] Layanan suara error: {e}")

# ------------------- GUI -------------------
def start_listener():
    global listening
    if not listening:
        listening = True
        threading.Thread(target=voice_listener, daemon=True).start()
        log_message("[INFO] Listener dimulai.")

def stop_listener():
    global listening
    listening = False
    log_message("[INFO] Listener dihentikan.")

# ------------------- MAIN -------------------
root = tk.Tk()
root.title("Voice PDF Printer")

start_btn = tk.Button(root, text="ON", width=15, command=start_listener)
start_btn.pack(pady=5)

stop_btn = tk.Button(root, text="OFF", width=15, command=stop_listener)
stop_btn.pack(pady=5)

log_area = scrolledtext.ScrolledText(root, width=60, height=20, state="disabled")
log_area.pack(padx=10, pady=10)

listening = False
speak("Selamat datang di program print otomatis versi GUI")
root.mainloop()
