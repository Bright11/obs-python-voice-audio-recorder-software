import pyaudio
import wave
import numpy as np
import threading
import time
import keyboard
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# ==============================
# Configuration
# ==============================
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

class LiveVoiceProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bright C Web OBS Audio Link")
        self.root.geometry("400x500")
        
        self.audio = pyaudio.PyAudio()
        self.in_stream = None
        self.out_stream = None
        self.frames = []
        self.is_running = False
        self.is_paused = False
        self.current_volume = tk.DoubleVar(value=0)

        # --- UI ELEMENTS ---
        self.status_label = ttk.Label(root, text="STATUS: READY", font=("Arial", 14, "bold"))
        self.status_label.pack(pady=20)

        ttk.Label(root, text="Live Mic Meter:").pack()
        self.vu_meter = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate", variable=self.current_volume)
        self.vu_meter.pack(pady=10)

        # Buttons
        ttk.Button(root, text="Start (Ctrl+Shift+S)", command=self.start).pack(pady=5, fill='x', padx=60)
        ttk.Button(root, text="Pause (Ctrl+Shift+P)", command=self.pause).pack(pady=5, fill='x', padx=60)
        ttk.Button(root, text="Resume (Ctrl+Shift+R)", command=self.resume).pack(pady=5, fill='x', padx=60)
        ttk.Button(root, text="Stop (Ctrl+Shift+X)", command=self.stop).pack(pady=5, fill='x', padx=60)
        
        ttk.Separator(root, orient='horizontal').pack(fill='x', pady=20, padx=30)
        
        self.btn_save = ttk.Button(root, text="Save Audio to Location", command=self.save_to_location, state="disabled")
        self.btn_save.pack(pady=10)

        # --- GLOBAL HOTKEYS ---
        keyboard.add_hotkey('ctrl+shift+s', self.start)
        keyboard.add_hotkey('ctrl+shift+p', self.pause)
        keyboard.add_hotkey('ctrl+shift+r', self.resume)
        keyboard.add_hotkey('ctrl+shift+x', self.stop)

    def find_virtual_cable(self):
        for i in range(self.audio.get_device_count()):
            info = self.audio.get_device_info_by_index(i)
            if "CABLE Input" in info["name"]:
                return i
        return None

    def start(self):
        if self.is_running: return
        
        cable_index = self.find_virtual_cable()
        
        self.in_stream = self.audio.open(
            format=FORMAT, channels=CHANNELS, rate=RATE,
            input=True, frames_per_buffer=CHUNK
        )
        self.out_stream = self.audio.open(
            format=FORMAT, channels=CHANNELS, rate=RATE,
            output=True, output_device_index=cable_index,
            frames_per_buffer=CHUNK
        )

        self.is_running = True
        self.is_paused = False
        self.frames = []
        self.btn_save.config(state="disabled")
        self.status_label.config(text="STATUS: LIVE", foreground="red")
        
        threading.Thread(target=self.process_loop, daemon=True).start()

    def process_loop(self):
        """Your specific 'Best' High-Quality Loop"""
        while self.is_running:
            if not self.is_paused:
                try:
                    data = self.in_stream.read(CHUNK, exception_on_overflow=False)
                    audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32)
                    
                    # RMS for the VU Meter
                    rms = np.sqrt(np.mean(audio_data**2))
                    self.current_volume.set(min(100, (rms/5000)*100))

                    # 1. SOFT NOISE GATE
                    threshold = 50 
                    audio_data[np.abs(audio_data) < threshold] = 0
                    
                    # 2. AUTOMATIC GAIN / COMPRESSION
                    gain = 4.0
                    audio_data = audio_data * gain
                    
                    # Soft Clipping (Tanh)
                    audio_data = np.tanh(audio_data / 32768.0) * 32768.0
                    
                    # 3. CONVERT BACK TO BYTES
                    final_data = audio_data.astype(np.int16).tobytes()
                    
                    self.out_stream.write(final_data)
                    self.frames.append(data)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                self.current_volume.set(0)
                time.sleep(0.1)

    def pause(self):
        self.is_paused = True
        self.status_label.config(text="STATUS: PAUSED", foreground="orange")

    def resume(self):
        self.is_paused = False
        self.status_label.config(text="STATUS: LIVE", foreground="red")

    def stop(self):
        if not self.is_running: return
        self.is_running = False
        self.current_volume.set(0)
        time.sleep(0.2)
        
        if self.in_stream:
            self.in_stream.stop_stream()
            self.in_stream.close()
        if self.out_stream:
            self.out_stream.stop_stream()
            self.out_stream.close()
            
        self.status_label.config(text="STATUS: STOPPED", foreground="black")
        self.btn_save.config(state="normal")

    def save_to_location(self):
        if not self.frames: return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".wav",
            filetypes=[("WAV files", "*.wav")],
            title="Save Audio Recording"
        )
        if file_path:
            with wave.open(file_path, "wb") as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(self.audio.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b"".join(self.frames))
            messagebox.showinfo("Saved", f"Successfully saved to:\n{file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LiveVoiceProcessorGUI(root)
    root.mainloop()
