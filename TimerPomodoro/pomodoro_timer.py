import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from datetime import timedelta
import winsound
import sys

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer Pro")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        
        # Variabili
        self.running = False
        self.paused = False
        self.current_session = "Studio"
        self.sessions_completed = 0
        self.remaining_time = 0
        self.timer_thread = None
        
        # Configurazione colori
        self.bg_color = "#2C3E50"
        self.fg_color = "#ECF0F1"
        self.accent_color = "#3498DB"
        self.study_color = "#E74C3C"
        self.break_color = "#2ECC71"
        
        self.root.configure(bg=self.bg_color)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Titolo
        title_frame = tk.Frame(self.root, bg=self.bg_color)
        title_frame.pack(pady=20)
        
        tk.Label(title_frame, text="🍅 Pomodoro Timer Pro", 
                font=("Arial", 24, "bold"), bg=self.bg_color, 
                fg=self.fg_color).pack()
        
        # Display tempo
        self.time_frame = tk.Frame(self.root, bg=self.study_color, 
                                   relief=tk.RAISED, borderwidth=3)
        self.time_frame.pack(pady=20, padx=40, fill=tk.BOTH)
        
        self.session_label = tk.Label(self.time_frame, text="Studio", 
                                     font=("Arial", 16, "bold"), 
                                     bg=self.study_color, fg="white")
        self.session_label.pack(pady=10)
        
        self.time_label = tk.Label(self.time_frame, text="25:00", 
                                   font=("Arial", 48, "bold"), 
                                   bg=self.study_color, fg="white")
        self.time_label.pack(pady=20)
        
        # Contatore sessioni
        self.sessions_label = tk.Label(self.root, 
                                       text="Sessioni completate: 0", 
                                       font=("Arial", 12), 
                                       bg=self.bg_color, fg=self.fg_color)
        self.sessions_label.pack(pady=5)
        
        # Frame impostazioni
        settings_frame = tk.LabelFrame(self.root, text="Impostazioni Timer", 
                                       font=("Arial", 12, "bold"),
                                       bg=self.bg_color, fg=self.fg_color,
                                       relief=tk.GROOVE, borderwidth=2)
        settings_frame.pack(pady=20, padx=40, fill=tk.BOTH)
        
        # Tempo studio
        study_frame = tk.Frame(settings_frame, bg=self.bg_color)
        study_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(study_frame, text="Tempo Studio (min):", 
                font=("Arial", 11), bg=self.bg_color, 
                fg=self.fg_color).pack(side=tk.LEFT, padx=5)
        
        self.study_time = tk.Spinbox(study_frame, from_=1, to=120, 
                                     width=10, font=("Arial", 11))
        self.study_time.delete(0, tk.END)
        self.study_time.insert(0, "25")
        self.study_time.pack(side=tk.LEFT, padx=5)
        
        # Tempo riposo breve
        short_break_frame = tk.Frame(settings_frame, bg=self.bg_color)
        short_break_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(short_break_frame, text="Riposo Breve (min):", 
                font=("Arial", 11), bg=self.bg_color, 
                fg=self.fg_color).pack(side=tk.LEFT, padx=5)
        
        self.short_break_time = tk.Spinbox(short_break_frame, from_=1, to=60, 
                                           width=10, font=("Arial", 11))
        self.short_break_time.delete(0, tk.END)
        self.short_break_time.insert(0, "5")
        self.short_break_time.pack(side=tk.LEFT, padx=5)
        
        # Tempo riposo lungo
        long_break_frame = tk.Frame(settings_frame, bg=self.bg_color)
        long_break_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(long_break_frame, text="Riposo Lungo (min):", 
                font=("Arial", 11), bg=self.bg_color, 
                fg=self.fg_color).pack(side=tk.LEFT, padx=5)
        
        self.long_break_time = tk.Spinbox(long_break_frame, from_=1, to=120, 
                                          width=10, font=("Arial", 11))
        self.long_break_time.delete(0, tk.END)
        self.long_break_time.insert(0, "15")
        self.long_break_time.pack(side=tk.LEFT, padx=5)
        
        # Sessioni prima del riposo lungo
        sessions_frame = tk.Frame(settings_frame, bg=self.bg_color)
        sessions_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(sessions_frame, text="Sessioni prima riposo lungo:", 
                font=("Arial", 11), bg=self.bg_color, 
                fg=self.fg_color).pack(side=tk.LEFT, padx=5)
        
        self.sessions_before_long = tk.Spinbox(sessions_frame, from_=1, to=10, 
                                               width=10, font=("Arial", 11))
        self.sessions_before_long.delete(0, tk.END)
        self.sessions_before_long.insert(0, "4")
        self.sessions_before_long.pack(side=tk.LEFT, padx=5)
        
        # Pulsanti controllo
        buttons_frame = tk.Frame(self.root, bg=self.bg_color)
        buttons_frame.pack(pady=20)
        
        self.start_button = tk.Button(buttons_frame, text="▶ Avvia", 
                                      command=self.start_timer,
                                      font=("Arial", 12, "bold"),
                                      bg=self.accent_color, fg="white",
                                      width=12, height=2, cursor="hand2")
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.pause_button = tk.Button(buttons_frame, text="⏸ Pausa", 
                                      command=self.pause_timer,
                                      font=("Arial", 12, "bold"),
                                      bg="#F39C12", fg="white",
                                      width=12, height=2, cursor="hand2",
                                      state=tk.DISABLED)
        self.pause_button.grid(row=0, column=1, padx=5)
        
        self.stop_button = tk.Button(buttons_frame, text="⏹ Stop", 
                                     command=self.stop_timer,
                                     font=("Arial", 12, "bold"),
                                     bg="#95A5A6", fg="white",
                                     width=12, height=2, cursor="hand2",
                                     state=tk.DISABLED)
        self.stop_button.grid(row=0, column=2, padx=5)
        
        # Reset contatore
        reset_button = tk.Button(self.root, text="Reset Contatore Sessioni", 
                                command=self.reset_sessions,
                                font=("Arial", 10),
                                bg=self.bg_color, fg=self.fg_color,
                                cursor="hand2")
        reset_button.pack(pady=10)
        
    def start_timer(self):
        if not self.running:
            if not self.paused:
                # Nuovo timer
                self.remaining_time = int(self.study_time.get()) * 60
                self.current_session = "Studio"
                self.update_session_display()
            
            self.running = True
            self.paused = False
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
            
            # Avvia thread timer
            self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
            self.timer_thread.start()
    
    def pause_timer(self):
        if self.running:
            self.running = False
            self.paused = True
            self.start_button.config(text="▶ Riprendi", state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
    
    def stop_timer(self):
        self.running = False
        self.paused = False
        self.remaining_time = 0
        
        self.start_button.config(text="▶ Avvia", state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)
        
        # Reset display
        self.update_time_display(int(self.study_time.get()) * 60)
    
    def reset_sessions(self):
        self.sessions_completed = 0
        self.sessions_label.config(text="Sessioni completate: 0")
    
    def run_timer(self):
        while self.running and self.remaining_time > 0:
            self.update_time_display(self.remaining_time)
            time.sleep(1)
            self.remaining_time -= 1
        
        if self.remaining_time <= 0 and self.running:
            # Timer completato
            self.play_sound()
            self.handle_session_complete()
    
    def handle_session_complete(self):
        if self.current_session == "Studio":
            self.sessions_completed += 1
            self.sessions_label.config(text=f"Sessioni completate: {self.sessions_completed}")
            
            # Determina tipo di pausa
            sessions_threshold = int(self.sessions_before_long.get())
            if self.sessions_completed % sessions_threshold == 0:
                self.current_session = "Riposo Lungo"
                self.remaining_time = int(self.long_break_time.get()) * 60
                message = f"🎉 Sessione completata!\n\nInizio Riposo Lungo di {self.long_break_time.get()} minuti"
            else:
                self.current_session = "Riposo Breve"
                self.remaining_time = int(self.short_break_time.get()) * 60
                message = f"✅ Sessione completata!\n\nInizio Riposo Breve di {self.short_break_time.get()} minuti"
        else:
            # Fine pausa
            self.current_session = "Studio"
            self.remaining_time = int(self.study_time.get()) * 60
            message = f"🔔 Pausa terminata!\n\nInizio sessione di Studio di {self.study_time.get()} minuti"
        
        self.update_session_display()
        
        # Mostra notifica
        self.root.after(0, lambda: messagebox.showinfo("Timer Completato", message))
        
        # Continua automaticamente con la prossima sessione
        if self.running:
            self.run_timer()
    
    def update_time_display(self, seconds):
        minutes, secs = divmod(seconds, 60)
        time_string = f"{minutes:02d}:{secs:02d}"
        self.root.after(0, lambda: self.time_label.config(text=time_string))
    
    def update_session_display(self):
        if self.current_session == "Studio":
            color = self.study_color
            label = "📚 Studio"
        elif self.current_session == "Riposo Breve":
            color = self.break_color
            label = "☕ Riposo Breve"
        else:
            color = self.break_color
            label = "🌴 Riposo Lungo"
        
        self.root.after(0, lambda: self.time_frame.config(bg=color))
        self.root.after(0, lambda: self.session_label.config(text=label, bg=color))
        self.root.after(0, lambda: self.time_label.config(bg=color))
    
    def play_sound(self):
        # Suona un beep di sistema
        try:
            # Suono di notifica Windows
            for _ in range(3):
                winsound.Beep(1000, 300)
                time.sleep(0.1)
        except:
            # Fallback se winsound non funziona
            print('\a')

def main():
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()

if __name__ == "__main__":
    main()