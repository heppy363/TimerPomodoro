"""Interfaccia grafica Pomodoro Timer"""
import tkinter as tk
from tkinter import ttk, messagebox
from config import ConfigManager
from timerLogich import PomodoroLogic
from sound import play_notification


class PomodoroUI:
    COLORS = {
        'bg_dark': '#1a1a1a',
        'bg_medium': '#2d2d2d',
        'bg_light': '#3d3d3d',
        'fg_primary': '#ffffff',
        'fg_secondary': '#b0b0b0',
        'accent_red': '#e63946',
        'accent_red_dark': '#c72938',
        'accent_green': '#06d6a0',
        'border': '#4d4d4d'
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer Pro 2.0")
        self.root.geometry("600x750")
        self.root.resizable(False, False)
        self.root.configure(bg=self.COLORS['bg_dark'])
        
        # Config manager
        self.config_mgr = ConfigManager()
        self.config = self.config_mgr.load()
        
        # Timer logic
        self.timer = PomodoroLogic(
            on_tick=self._on_timer_tick,
            on_complete=self._on_timer_complete
        )
        self._apply_config_to_timer()
        
        # Crea UI
        self._create_ui()
        self._update_display()
        
        # Gestione chiusura
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _apply_config_to_timer(self):
        """Applica configurazione al timer"""
        self.timer.set_times(
            self.config["study_time"],
            self.config["short_break"],
            self.config["long_break"],
            self.config["sessions_before_long"]
        )
    
    def _create_ui(self):
        """Crea interfaccia"""
        # Header
        self._create_header()
        
        # Timer display
        self._create_timer_display()
        
        # Stats
        self._create_stats()
        
        # Settings
        self._create_settings()
        
        # Controls
        self._create_controls()
        
        # Footer
        self._create_footer()
    
    def _create_header(self):
        header = tk.Frame(self.root, bg=self.COLORS['bg_dark'])
        header.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        tk.Label(
            header,
            text="🍅 POMODORO TIMER PRO",
            font=("Segoe UI", 28, "bold"),
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['accent_red']
        ).pack()
        
        tk.Label(
            header,
            text="Massimizza la tua produttività",
            font=("Segoe UI", 10),
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['fg_secondary']
        ).pack()
    
    def _create_timer_display(self):
        display_frame = tk.Frame(self.root, bg=self.COLORS['bg_medium'])
        display_frame.pack(pady=20, padx=30, fill=tk.BOTH)
        
        # Bordo rosso
        tk.Frame(display_frame, bg=self.COLORS['accent_red'], height=4).pack(fill=tk.X)
        
        content = tk.Frame(display_frame, bg=self.COLORS['bg_medium'])
        content.pack(pady=30, padx=20)
        
        # Label sessione
        self.session_label = tk.Label(
            content,
            text="📚 STUDIO",
            font=("Segoe UI", 16, "bold"),
            bg=self.COLORS['bg_medium'],
            fg=self.COLORS['fg_primary']
        )
        self.session_label.pack(pady=(0, 15))
        
        # Timer
        self.time_label = tk.Label(
            content,
            text="25:00",
            font=("Consolas", 72, "bold"),
            bg=self.COLORS['bg_medium'],
            fg=self.COLORS['accent_red']
        )
        self.time_label.pack()
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            content,
            mode='determinate',
            length=400
        )
        self.progress_bar.pack(pady=(20, 0))
        
        # Style
        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            "TProgressbar",
            background=self.COLORS['accent_red'],
            troughcolor=self.COLORS['bg_light'],
            borderwidth=0,
            thickness=8
        )
    
    def _create_stats(self):
        stats_frame = tk.Frame(self.root, bg=self.COLORS['bg_dark'])
        stats_frame.pack(pady=10, padx=30, fill=tk.X)
        
        # Sessioni completate
        sessions_box = tk.Frame(stats_frame, bg=self.COLORS['bg_medium'])
        sessions_box.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
        
        tk.Label(
            sessions_box,
            text="Sessioni Completate",
            font=("Segoe UI", 10),
            bg=self.COLORS['bg_medium'],
            fg=self.COLORS['fg_secondary']
        ).pack(pady=(10, 0))
        
        self.sessions_label = tk.Label(
            sessions_box,
            text="0",
            font=("Segoe UI", 36, "bold"),
            bg=self.COLORS['bg_medium'],
            fg=self.COLORS['accent_red']
        )
        self.sessions_label.pack(pady=(0, 10))
        
        # Prossima pausa
        next_box = tk.Frame(stats_frame, bg=self.COLORS['bg_medium'])
        next_box.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5)
        
        tk.Label(
            next_box,
            text="Prossima Pausa",
            font=("Segoe UI", 10),
            bg=self.COLORS['bg_medium'],
            fg=self.COLORS['fg_secondary']
        ).pack(pady=(10, 0))
        
        self.next_break_label = tk.Label(
            next_box,
            text="Breve",
            font=("Segoe UI", 16, "bold"),
            bg=self.COLORS['bg_medium'],
            fg=self.COLORS['accent_green']
        )
        self.next_break_label.pack(pady=(5, 10))
    
    def _create_settings(self):
        settings_frame = tk.LabelFrame(
            self.root,
            text=" ⚙ IMPOSTAZIONI ",
            font=("Segoe UI", 12, "bold"),
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['fg_primary'],
            relief=tk.FLAT,
            borderwidth=2
        )
        settings_frame.pack(pady=15, padx=30, fill=tk.BOTH)
        
        inner = tk.Frame(settings_frame, bg=self.COLORS['bg_dark'])
        inner.pack(padx=15, pady=15)
        
        # Tempo studio
        self.study_spin = self._create_setting_row(
            inner, 0, "⏱ Tempo Studio (min):", 1, 120, self.config["study_time"]
        )
        
        # Riposo breve
        self.short_break_spin = self._create_setting_row(
            inner, 1, "☕ Riposo Breve (min):", 1, 60, self.config["short_break"]
        )
        
        # Riposo lungo
        self.long_break_spin = self._create_setting_row(
            inner, 2, "🌴 Riposo Lungo (min):", 1, 120, self.config["long_break"]
        )
        
        # Sessioni
        self.sessions_spin = self._create_setting_row(
            inner, 3, "🔄 Sessioni prima pausa lunga:", 1, 10, 
            self.config["sessions_before_long"]
        )
        
        # Suono
        options_frame = tk.Frame(inner, bg=self.COLORS['bg_dark'])
        options_frame.grid(row=4, column=0, columnspan=2, pady=(15, 0), sticky='w')
        
        self.sound_var = tk.BooleanVar(value=self.config["sound_enabled"])
        tk.Checkbutton(
            options_frame,
            text="🔊 Notifica sonora",
            variable=self.sound_var,
            font=("Segoe UI", 10),
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['fg_secondary'],
            selectcolor=self.COLORS['bg_medium'],
            activebackground=self.COLORS['bg_dark']
        ).pack(side=tk.LEFT)
        
        # Pulsante salva
        save_btn = tk.Button(
            inner,
            text="💾 SALVA IMPOSTAZIONI",
            command=self._save_settings,
            font=("Arial", 11, "bold"),
            bg="#3498DB",
            fg="white",
            relief=tk.RAISED,
            bd=3,
            width=20,
            height=2
        )
        save_btn.grid(row=5, column=0, columnspan=2, pady=(15, 0))
    
    def _create_setting_row(self, parent, row, label_text, min_val, max_val, default):
        tk.Label(
            parent,
            text=label_text,
            font=("Segoe UI", 11),
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['fg_secondary'],
            anchor='w'
        ).grid(row=row, column=0, sticky='w', pady=8, padx=(0, 15))
        
        spinbox = tk.Spinbox(
            parent,
            from_=min_val,
            to=max_val,
            width=8,
            font=("Segoe UI", 11),
            bg=self.COLORS['bg_medium'],
            fg=self.COLORS['fg_primary'],
            relief=tk.FLAT
        )
        spinbox.delete(0, tk.END)
        spinbox.insert(0, str(default))
        spinbox.grid(row=row, column=1, sticky='w', pady=8)
        
        parent.columnconfigure(1, weight=1)
        return spinbox
    
    def _create_controls(self):
        """Crea controlli timer"""
        controls = tk.Frame(self.root)
        controls.pack(pady=20)
        
        # AVVIA
        self.start_btn = tk.Button(
            controls,
            text="▶ AVVIA",
            command=self._start_timer,
            font=("Arial", 13, "bold"),
            bg="#E74C3C",
            fg="white",
            width=12,
            height=2,
            relief=tk.RAISED,
            bd=3
        )
        self.start_btn.grid(row=0, column=0, padx=8)
        
        # PAUSA
        self.pause_btn = tk.Button(
            controls,
            text="⏸ PAUSA",
            command=self._pause_timer,
            font=("Arial", 13, "bold"),
            bg="#F39C12",
            fg="white",
            width=12,
            height=2,
            relief=tk.RAISED,
            bd=3,
            state=tk.DISABLED
        )
        self.pause_btn.grid(row=0, column=1, padx=8)
        
        # STOP
        self.stop_btn = tk.Button(
            controls,
            text="⏹ STOP",
            command=self._stop_timer,
            font=("Arial", 13, "bold"),
            bg="#95A5A6",
            fg="white",
            width=12,
            height=2,
            relief=tk.RAISED,
            bd=3,
            state=tk.DISABLED
        )
        self.stop_btn.grid(row=0, column=2, padx=8)
        
        # RESET
        tk.Button(
            self.root,
            text="🔄 Reset Contatore Sessioni",
            command=self._reset_sessions,
            font=("Arial", 10),
            relief=tk.RAISED,
            bd=2,
            padx=10,
            pady=5
        ).pack(pady=5)
    
    def _create_footer(self):
        footer = tk.Frame(self.root, bg=self.COLORS['bg_dark'])
        footer.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        tk.Label(
            footer,
            text="Pomodoro Timer Pro v2.0 | Creato con ❤ per la produttività",
            font=("Segoe UI", 8),
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['fg_secondary']
        ).pack()
    
    # === CALLBACKS ===
    
    def _start_timer(self):
        if self.timer.start():
            self._update_button_states(running=True)
    
    def _pause_timer(self):
        if self.timer.pause():
            self.start_btn.config(text="▶ RIPRENDI")
            self._update_button_states(paused=True)
    
    def _stop_timer(self):
        self.timer.stop()
        self.start_btn.config(text="▶ AVVIA")
        self._update_button_states(running=False)
        self._update_display()
    
    def _reset_sessions(self):
        if messagebox.askyesno("Conferma", "Azzerare contatore sessioni?"):
            self.timer.reset_sessions()
            self._update_stats()
    
    def _save_settings(self):
        try:
            self.config = {
                "study_time": int(self.study_spin.get()),
                "short_break": int(self.short_break_spin.get()),
                "long_break": int(self.long_break_spin.get()),
                "sessions_before_long": int(self.sessions_spin.get()),
                "sound_enabled": self.sound_var.get()
            }
            
            self._apply_config_to_timer()
            
            if self.config_mgr.save(self.config):
                messagebox.showinfo("Successo", "Impostazioni salvate!")
            else:
                messagebox.showerror("Errore", "Impossibile salvare")
        except ValueError:
            messagebox.showerror("Errore", "Valori non validi")
    
    def _on_timer_tick(self, remaining, total):
        """Callback tick timer"""
        self.root.after(0, lambda: self._update_time_display(remaining))
        self.root.after(0, lambda: self._update_progress(remaining, total))
    
    def _on_timer_complete(self, msg_type, session, sessions_count):
        """Callback completamento"""
        # Suono
        if self.config["sound_enabled"]:
            play_notification()
        
        # Aggiorna UI
        self.root.after(0, self._update_session_display)
        self.root.after(0, self._update_stats)
        
        # Messaggio
        messages = {
            "short_break": f"✅ Sessione completata!\n\nPausa breve di {self.timer.short_break} minuti.",
            "long_break": f"🎉 Ottimo lavoro!\n\n{self.timer.sessions_before_long} sessioni completate.\nPausa lunga di {self.timer.long_break} minuti.",
            "study": f"🔔 Pausa terminata!\n\nTorna al lavoro.\nSessione di {self.timer.study_time} minuti."
        }
        self.root.after(0, lambda: messagebox.showinfo("Timer Completato", messages[msg_type]))
    
    # === AGGIORNAMENTI UI ===
    
    def _update_display(self):
        """Aggiorna display completo"""
        minutes = self.config["study_time"]
        self._update_time_display(minutes * 60)
        self._update_session_display()
        self._update_stats()
        self.progress_bar.config(value=0)
    
    def _update_time_display(self, seconds):
        minutes, secs = divmod(seconds, 60)
        self.time_label.config(text=f"{minutes:02d}:{secs:02d}")
    
    def _update_progress(self, remaining, total):
        if total > 0:
            progress = ((total - remaining) / total) * 100
            self.progress_bar.config(value=progress)
    
    def _update_session_display(self):
        labels = {
            "Studio": ("📚 STUDIO", self.COLORS['accent_red']),
            "Riposo Breve": ("☕ RIPOSO BREVE", self.COLORS['accent_green']),
            "Riposo Lungo": ("🌴 RIPOSO LUNGO", self.COLORS['accent_green'])
        }
        label, color = labels.get(self.timer.current_session, ("", self.COLORS['fg_primary']))
        self.session_label.config(text=label)
        self.time_label.config(fg=color)
    
    def _update_stats(self):
        self.sessions_label.config(text=str(self.timer.sessions_completed))
        next_break = self.timer.get_next_break_type()
        self.next_break_label.config(text=next_break)
    
    def _update_button_states(self, running=False, paused=False):
        """Aggiorna stati bottoni"""
        if running and not paused:
            self.start_btn.config(state=tk.DISABLED)
            self.pause_btn.config(state=tk.NORMAL, bg="#F39C12", fg="white")
            self.stop_btn.config(state=tk.NORMAL, bg="#95A5A6", fg="white")
        elif paused:
            self.start_btn.config(state=tk.NORMAL)
            self.pause_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL, bg="#95A5A6", fg="white")
        else:
            self.start_btn.config(state=tk.NORMAL)
            self.pause_btn.config(state=tk.DISABLED, bg="#cccccc", fg="#666666")
            self.stop_btn.config(state=tk.DISABLED, bg="#cccccc", fg="#666666")
    
    def _on_closing(self):
        """Gestione chiusura"""
        if self.timer.running:
            if messagebox.askokcancel("Uscita", "Timer in esecuzione. Uscire?"):
                self.timer.stop()
                self.root.destroy()
        else:
            self.root.destroy()