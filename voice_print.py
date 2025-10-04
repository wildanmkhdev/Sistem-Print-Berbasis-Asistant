import os
import threading
import queue
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from rapidfuzz import process
import shutil
import subprocess
import tempfile
import webbrowser
import customtkinter as ctk
from tkinter import scrolledtext

# ------------------- QUEUE FOR THREAD-SAFE LOGGING -------------------
log_queue = queue.Queue()

# ------------------- TTS (Non-blocking) -------------------
def speak(text, blocking=False):
    def _speak():
        try:
            log_message(f"[🤖] {text}")
            tmp_file = os.path.join(tempfile.gettempdir(), f"voice_print_{threading.get_ident()}.mp3")
            tts = gTTS(text=text, lang="id")
            tts.save(tmp_file)
            playsound(tmp_file)
            try:
                os.remove(tmp_file)
            except:
                pass
        except Exception as e:
            log_message(f"[ERROR TTS] {e}")
    
    try:
        if blocking:
            _speak()
        else:
            threading.Thread(target=_speak, daemon=True).start()
    except:
        pass

# ------------------- PRINT -------------------
def print_pdf(file_path):
    try:
        # Cek apakah file ada
        if not os.path.exists(file_path):
            log_message(f"❌ File tidak ditemukan: {file_path}")
            speak("Maaf, file tidak ditemukan.")
            return
        
        # Konversi ke absolute path
        abs_path = os.path.abspath(file_path)
        log_message(f"[INFO] Mencoba mencetak: {abs_path}")
        
        # Cari printer executable yang tersedia
        adobe_paths = [
            shutil.which("AcroRd32.exe"),
            r"C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe",
            r"C:\Program Files\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe"
        ]
        
        sumatra_paths = [
            shutil.which("SumatraPDF.exe"),
            r"C:\Program Files\SumatraPDF\SumatraPDF.exe",
            r"C:\Program Files (x86)\SumatraPDF\SumatraPDF.exe"
        ]
        
        # Coba Adobe Reader
        for adobe_path in adobe_paths:
            if adobe_path and os.path.exists(adobe_path):
                try:
                    subprocess.Popen([adobe_path, "/p", "/h", abs_path], 
                                   stdout=subprocess.DEVNULL, 
                                   stderr=subprocess.DEVNULL)
                    log_message(f"🖨️ Mencetak dengan Adobe Reader: {os.path.basename(file_path)}")
                    speak("File sedang dicetak dengan Adobe Reader.")
                    return
                except:
                    continue
        
        # Coba SumatraPDF
        for sumatra_path in sumatra_paths:
            if sumatra_path and os.path.exists(sumatra_path):
                try:
                    subprocess.Popen([sumatra_path, "-print-to-default", abs_path],
                                   stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL)
                    log_message(f"🖨️ Mencetak dengan SumatraPDF: {os.path.basename(file_path)}")
                    speak("File sedang dicetak dengan Sumatra PDF.")
                    return
                except:
                    continue
        
        # Fallback: buka di browser
        log_message(f"[INFO] Tidak ada printer app terdeteksi. Membuka di browser...")
        import webbrowser
        file_url = f"file:///{abs_path.replace(os.sep, '/')}"
        webbrowser.open(file_url)
        log_message(f"🌐 File dibuka di browser: {os.path.basename(file_path)}")
        speak("File dibuka di browser. Silakan cetak dengan Control P.")
            
    except Exception as e:
        log_message(f"❌ Error: {str(e)}")
        speak("Maaf, terjadi kesalahan.")

# ------------------- LIST PDF -------------------
def list_pdfs(folder="pdf_files"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    return [f for f in os.listdir(folder) if f.lower().endswith(".pdf")]

# ------------------- GUI LOG (Thread-safe) -------------------
def log_message(msg):
    log_queue.put(msg)

def process_log_queue():
    try:
        while True:
            msg = log_queue.get_nowait()
            log_area.configure(state="normal")
            if "ERROR" in msg:
                log_area.insert("end", f"❌ {msg}\n", "error")
            elif "INFO" in msg:
                log_area.insert("end", f"ℹ️ {msg}\n", "info")
            elif "print" in msg or "Mencetak" in msg:
                log_area.insert("end", f"🖨️ {msg}\n", "print")
            else:
                log_area.insert("end", msg + "\n", "normal")
            log_area.see("end")
            log_area.configure(state="disabled")
    except queue.Empty:
        pass
    finally:
        root.after(100, process_log_queue)

# ------------------- VOICE LISTENER (Improved) -------------------
def voice_listener():
    global listening
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8
    recognizer.non_speaking_duration = 0.5

    speak("Listener aktif. Katakan 'Halo Ella' untuk memulai atau 'Hentikan sistem' untuk mematikan.")
    
    while listening:
        try:
            with sr.Microphone() as source:
                log_message("[INFO] Mendengarkan...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                
            # Proses speech recognition di thread terpisah agar tidak blocking
            text = recognizer.recognize_google(audio, language="id-ID").lower()
            log_message(f"[🎤] Kamu bilang: {text}")
            
            if "halo ella" in text or "hello ella" in text:
                speak("Siap! Sebutkan nama file PDF yang ingin kamu cetak.", blocking=True)
                
                try:
                    with sr.Microphone() as source2:
                        recognizer.adjust_for_ambient_noise(source2, duration=0.5)
                        audio2 = recognizer.listen(source2, timeout=8, phrase_time_limit=5)
                    
                    file_name = recognizer.recognize_google(audio2, language="id-ID").lower()
                    log_message(f"[🎤] Nama file: {file_name}")
                    
                    pdfs = list_pdfs()
                    if not pdfs:
                        speak("Maaf, tidak ada file PDF di folder.")
                        continue
                    
                    result = process.extractOne(file_name, pdfs, score_cutoff=40)
                    
                    if result:
                        best_match = result[0]
                        score = result[1]
                        file_path = os.path.join("pdf_files", best_match)
                        
                        log_message(f"[INFO] File ditemukan: {best_match} (confidence: {score}%)")
                        speak(f"File {best_match} ditemukan. Apakah kamu yakin ingin mencetak? Jawab ya atau tidak.", blocking=True)
                        
                        try:
                            with sr.Microphone() as source3:
                                recognizer.adjust_for_ambient_noise(source3, duration=0.5)
                                audio3 = recognizer.listen(source3, timeout=8, phrase_time_limit=3)
                            
                            confirm = recognizer.recognize_google(audio3, language="id-ID").lower()
                            log_message(f"[🎤] Jawaban konfirmasi: {confirm}")
                            
                            if any(word in confirm for word in ["ya", "iya", "boleh", "lanjut", "cetak", "oke", "ok"]):
                                speak("Baik, file akan segera dicetak.")
                                threading.Thread(target=print_pdf, args=(file_path,), daemon=True).start()
                            else:
                                speak("Oke, proses dibatalkan.")
                                log_message("[INFO] Print dibatalkan oleh pengguna.")
                        except sr.WaitTimeoutError:
                            speak("Tidak ada jawaban. Proses dibatalkan.")
                        except sr.UnknownValueError:
                            speak("Maaf, jawabanmu tidak terdengar. Proses dibatalkan.")
                    else:
                        speak("Maaf, file tidak ditemukan di folder PDF.")
                        log_message(f"[INFO] File '{file_name}' tidak cocok dengan file manapun.")
                        
                except sr.WaitTimeoutError:
                    speak("Tidak ada suara terdeteksi. Silakan coba lagi.")
                except sr.UnknownValueError:
                    speak("Maaf, aku tidak mendengar dengan jelas. Silakan ulangi.")
                    
            elif "hentikan sistem" in text or "matikan sistem" in text or "stop sistem" in text:
                speak("Baik, sistem akan dimatikan sekarang. Sampai jumpa.", blocking=True)
                stop_listener()
                break

        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
            log_message("[INFO] Suara tidak dikenali.")
        except sr.RequestError as e:
            log_message(f"[ERROR] Layanan suara error: {e}")
            speak("Terjadi kesalahan koneksi. Cek koneksi internetmu.")
        except Exception as e:
            log_message(f"[ERROR] Error tidak terduga: {e}")

    log_message("[INFO] Listener berhenti.")

# ------------------- GUI CONTROL -------------------
def start_listener():
    global listening
    if not listening:
        listening = True
        threading.Thread(target=voice_listener, daemon=True).start()
        log_message("[INFO] Listener dimulai.")
        start_btn.configure(state="disabled")
        stop_btn.configure(state="normal")
    else:
        log_message("[INFO] Listener sudah aktif.")

def stop_listener():
    global listening
    listening = False
    log_message("[INFO] Listener dihentikan.")
    start_btn.configure(state="normal")
    stop_btn.configure(state="disabled")

# ------------------- MAIN GUI -------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Ella Voice Printer")
root.geometry("700x650")

title_label = ctk.CTkLabel(root, text="🎙️ Ella Voice Printer", font=ctk.CTkFont(size=28, weight="bold"))
title_label.pack(pady=15)

desc_label = ctk.CTkLabel(
    root,
    text="Katakan 'Halo Ella' untuk mulai print.\nKatakan 'Hentikan sistem' untuk mematikan.",
    font=ctk.CTkFont(size=16),
    text_color="#A0AEC0"
)
desc_label.pack()

button_frame = ctk.CTkFrame(root, fg_color="transparent")
button_frame.pack(pady=15)

start_btn = ctk.CTkButton(button_frame, text="🟢 Mulai Listener", width=240, height=45, 
                          font=ctk.CTkFont(size=15, weight="bold"), command=start_listener)
start_btn.grid(row=0, column=0, padx=10)

stop_btn = ctk.CTkButton(button_frame, text="🔴 Hentikan", width=240, height=45,
                         font=ctk.CTkFont(size=15, weight="bold"), command=stop_listener, state="disabled")
stop_btn.grid(row=0, column=1, padx=10)

log_label = ctk.CTkLabel(root, text="Log Aktivitas", font=ctk.CTkFont(size=18, weight="bold"))
log_label.pack(pady=(15, 5))

log_area = scrolledtext.ScrolledText(
    root, width=68, height=18, state="disabled",
    bg="#0f172a", fg="#e2e8f0", font=("Cascadia Code", 12), bd=0, relief="flat",
    wrap="word"
)
log_area.pack(padx=15, pady=10, fill="both", expand=True)
log_area.tag_configure("error", foreground="#F87171", font=("Cascadia Code", 12, "bold"))
log_area.tag_configure("info", foreground="#60A5FA", font=("Cascadia Code", 12))
log_area.tag_configure("print", foreground="#34D399", font=("Cascadia Code", 12, "bold"))
log_area.tag_configure("normal", foreground="#E2E8F0", font=("Cascadia Code", 12))

listening = False

# Start log queue processing
root.after(100, process_log_queue)

speak("Selamat datang di Ella Voice Printer versi stabil.")
root.mainloop()