"""
Pomodoro Timer Pro
==================
Timer Pomodoro professionale con interfaccia grafica moderna e configurazione persistente.

Author: Pomodoro Timer Team
Version: 2.0
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import json
import os
from pathlib import Path
from datetime import datetime
import sys

# Gestione import condizionali per compatibilità cross-platform
try:
    import winsound
    SOUND_AVAILABLE = True
except ImportError:
    SOUND_AVAILABLE = False


class ConfigManager:
    """Gestisce il caricamento e salvataggio delle configurazioni"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".pomodoro_timer"
        self.config_file = self.config_dir / "config.json"
        self.default_config = {
            "study_time": 25,
            "short_break": 5,
            "long_break": 15,
            "sessions_before_long": 4,
            "sound_enabled": True,
            "auto_start_breaks": True,
            "auto_start_sessions": False
        }
        
    def load_config(self):
        """Carica la configurazione da file o restituisce i valori predefiniti"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Merge con default per aggiungere eventuali nuove chiavi
                    return {**self.default_config, **config}
            return self.default_config.copy()
        except Exception as e:
            print(f"Errore caricamento configurazione: {e}")
            return self.default_config.copy()
    
    def save_config(self, config):
        """Salva la configurazione su file"""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
            return True
        except Exception as e:
            print(f"Errore salvataggio configurazione: {e}")
            return False


class PomodoroTimer:
    """Timer Pomodoro con interfaccia grafica moderna"""
    
    # Palette colori moderna (nero/grigio/rosso)
    COLORS = {
        'bg_dark': '#1a1a1a',           # Nero profondo
        'bg_medium': '#2d2d2d',         # Grigio scuro
        'bg_light': '#3d3d3d',          # Grigio medio
        'fg_primary': '#ffffff',        # Bianco
        'fg_secondary': '#b0b0b0',      # Grigio chiaro
        'accent_red': '#e63946',        # Rosso accento
        'accent_red_dark': '#c72938',   # Rosso scuro
        'accent_green': '#06d6a0',      # Verde per pause
        'border': '#4d4d4d',            # Grigio per bordi
        'button_hover': '#4d4d4d'       # Hover pulsanti
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer Pro 2.0")
        self.root.geometry("600x750")
        self.root.resizable(False, False)
        self.root.configure(bg=self.COLORS['bg_dark'])
        
        # Configurazione
        self.config_manager = ConfigManager()
        self.config = self.config_manager.load_config()
        
        # Variabili di stato
        self.running = False
        self.paused = False
        self.current_session = "Studio"
        self.sessions_completed = 0
        self.remaining_time = 0
        self.timer_thread = None
        
        # Crea interfaccia
        self.create_ui()
        self.load_settings_from_config()
        self.update_timer_display()
        
        # Gestione chiusura finestra
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_ui(self):
        """Crea l'interfaccia grafica completa"""
        # Header con titolo
        self._create_header()
        
        # Display timer principale
        self._create_timer_display()
        
        # Statistiche sessioni
        self._create_stats_section()
        
        # Pannello impostazioni
        self._create_settings_panel()
        
        # Controlli timer
        self._create_controls()
        
        # Footer
        self._create_footer()
    
    def _create_header(self):
        """Crea l'header con il titolo"""
        header = tk.Frame(self.root, bg=self.COLORS['bg_dark'], height=80)
        header.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        title = tk.Label(
            header,
            text="🍅 POMODORO TIMER PRO",
            font=("Segoe UI", 28, "bold"),
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['accent_red']
        )
        title.pack()
        
        subtitle = tk.Label(
            header,
            text="Massimizza la tua produttività",
            font=("Segoe UI", 10),
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['fg_secondary']
        )
        subtitle.pack()
    
    def _create_timer_display(self):
        """Crea il display principale del timer"""
        # Frame con gradiente simulato
        display_frame = tk.Frame(
            self.root,
            bg=self.COLORS['bg_medium'],
            relief=tk.FLAT,
            borderwidth=0
        )
        display_frame.pack(pady=20, padx=30, fill=tk.BOTH)
        
        # Bordo superiore rosso
        top_border = tk.Frame(display_frame, bg=self.COLORS['accent_red'], height=4)
        top_border.pack(fill=tk.X)
        
        # Contenuto
        content = tk.Frame(display_frame, bg=self.COLORS['bg_medium'])
        content.pack(pady=30, padx=20)
        
        # Label sessione corrente
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
        
        # Barra progresso
        self.progress_bar = ttk.Progressbar(
            content,
            mode='determinate',
            length=400,
            style="Red.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(pady=(20, 0))
        
        # Configura stile barra progresso
        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            "Red.Horizontal.TProgressbar",
            background=self.COLORS['accent_red'],
            troughcolor=self.COLORS['bg_light'],
            borderwidth=0,
            thickness=8
        )
    
    def _create_stats_section(self):
        """Crea la sezione statistiche"""
        stats_frame = tk.Frame(self.root, bg=self.COLORS['bg_dark'])
        stats_frame.pack(pady=10, padx=30, fill=tk.X)
        
        # Sessioni completate
        sessions_box = tk.Frame(stats_frame, bg=self.COLORS['bg_medium'], relief=tk.FLAT)
        sessions_box.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)
        
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
        next_break_box = tk.Frame(stats_frame, bg=self.COLORS['bg_medium'], relief=tk.FLAT)
        next_break_box.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        tk.Label(
            next_break_box,
            text="Prossima Pausa",
            font=("Segoe UI", 10),
            bg=self.COLORS['bg_medium'],
            fg=self.COLORS['fg_secondary']
        ).pack(pady=(10, 0))
        
        self.next_break_label = tk.Label(
            next_break_box,
            text="Breve",
            font=("Segoe UI", 16, "bold"),
            bg=self.COLORS['bg_medium'],
            fg=self.COLORS['accent_green']
        )
        self.next_break_label.pack(pady=(5, 10))
    
    def _create_settings_panel(self):
        """Crea il pannello impostazioni migliorato"""
        settings_frame = tk.LabelFrame(
            self.root,
            text=" ⚙ IMPOSTAZIONI TIMER ",
            font=("Segoe UI", 12, "bold"),
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['fg_primary'],
            relief=tk.FLAT,
            borderwidth=2,
            highlightthickness=1,
            highlightbackground=self.COLORS['border']
        )
        settings_frame.pack(pady=15, padx=30, fill=tk.BOTH)
        
        # Contenitore interno
        inner = tk.Frame(settings_frame, bg=self.COLORS['bg_dark'])
        inner.pack(padx=15, pady=15, fill=tk.BOTH)
        
        # Grid per impostazioni timer
        settings_grid = tk.Frame(inner, bg=self.COLORS['bg_dark'])
        settings_grid.pack(fill=tk.BOTH)
        
        # Tempo Studio
        self._create_setting_row(
            settings_grid, 0,
            "⏱ Tempo Studio (min):",
            "study_time", 1, 120, self.config["study_time"]
        )
        
        # Riposo Breve
        self._create_setting_row(
            settings_grid, 1,
            "☕ Riposo Breve (min):",
            "short_break", 1, 60, self.config["short_break"]
        )
        
        # Riposo Lungo
        self._create_setting_row(
            settings_grid, 2,
            "🌴 Riposo Lungo (min):",
            "long_break", 1, 120, self.config["long_break"]
        )
        
        # Sessioni prima riposo lungo
        self._create_setting_row(
            settings_grid, 3,
            "🔄 Sessioni prima pausa lunga:",
            "sessions_before_long", 1, 10, self.config["sessions_before_long"]
        )
        
        # Opzioni aggiuntive
        options_frame = tk.Frame(inner, bg=self.COLORS['bg_dark'])
        options_frame.pack(pady=(15, 0), fill=tk.X)
        
        self.sound_var = tk.BooleanVar(value=self.config["sound_enabled"])
        sound_check = tk.Checkbutton(
            options_frame,
            text="🔊 Notifica sonora",
            variable=self.sound_var,
            font=("Segoe UI", 10),
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['fg_secondary'],
            selectcolor=self.COLORS['bg_medium'],
            activebackground=self.COLORS['bg_dark'],
            activeforeground=self.COLORS['fg_primary']
        )
        sound_check.pack(side=tk.LEFT, padx=5)
        
        # Pulsante salva impostazioni
        save_btn = tk.Button(
            inner,
            text="💾 Salva Impostazioni",
            command=self.save_settings,
            font=("Segoe UI", 10, "bold"),
            bg=self.COLORS['bg_light'],
            fg=self.COLORS['fg_primary'],
            activebackground=self.COLORS['button_hover'],
            relief=tk.FLAT,
            cursor="hand2",
            padx=15,
            pady=5
        )
        save_btn.pack(pady=(10, 0))
    
    def _create_setting_row(self, parent, row, label_text, attr_name, min_val, max_val, default):
        """Crea una riga di impostazione"""
        # Label
        label = tk.Label(
            parent,
            text=label_text,
            font=("Segoe UI", 11),
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['fg_secondary'],
            anchor='w'
        )
        label.grid(row=row, column=0, sticky='w', pady=8, padx=(0, 15))
        
        # Spinbox
        spinbox = tk.Spinbox(
            parent,
            from_=min_val,
            to=max_val,
            width=8,
            font=("Segoe UI", 11),
            bg=self.COLORS['bg_medium'],
            fg=self.COLORS['fg_primary'],
            buttonbackground=self.COLORS['bg_light'],
            relief=tk.FLAT,
            insertbackground=self.COLORS['fg_primary']
        )
        spinbox.delete(0, tk.END)
        spinbox.insert(0, str(default))
        spinbox.grid(row=row, column=1, sticky='ew', pady=8)
        
        # Salva riferimento
        setattr(self, f"{attr_name}_spin", spinbox)
        
        parent.columnconfigure(1, weight=1)
    
    def _create_controls(self):
        """Crea i controlli del timer"""
        controls_frame = tk.Frame(self.root, bg=self.COLORS['bg_dark'])
        controls_frame.pack(pady=20)
        
        # Stile pulsanti
        btn_config = {
            'font': ("Segoe UI", 12, "bold"),
            'relief': tk.FLAT,
            'cursor': "hand2",
            'width': 12,
            'height': 2,
            'borderwidth': 0
        }
        
        # Avvia
        self.start_button = tk.Button(
            controls_frame,
            text="▶ AVVIA",
            command=self.start_timer,
            bg=self.COLORS['accent_red'],
            fg=self.COLORS['fg_primary'],
            activebackground=self.COLORS['accent_red_dark'],
            **btn_config
        )
        self.start_button.grid(row=0, column=0, padx=8)
        
        # Pausa
        self.pause_button = tk.Button(
            controls_frame,
            text="⏸ PAUSA",
            command=self.pause_timer,
            bg=self.COLORS['bg_medium'],
            fg=self.COLORS['fg_secondary'],
            activebackground=self.COLORS['button_hover'],
            state=tk.DISABLED,
            **btn_config
        )
        self.pause_button.grid(row=0, column=1, padx=8)
        
        # Stop
        self.stop_button = tk.Button(
            controls_frame,
            text="⏹ STOP",
            command=self.stop_timer,
            bg=self.COLORS['bg_medium'],
            fg=self.COLORS['fg_secondary'],
            activebackground=self.COLORS['button_hover'],
            state=tk.DISABLED,
            **btn_config
        )
        self.stop_button.grid(row=0, column=2, padx=8)
        
        # Reset sessioni
        reset_btn = tk.Button(
            self.root,
            text="🔄 Reset Contatore",
            command=self.reset_sessions,
            font=("Segoe UI", 9),
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['fg_secondary'],
            activebackground=self.COLORS['bg_medium'],
            relief=tk.FLAT,
            cursor="hand2",
            borderwidth=0
        )
        reset_btn.pack(pady=5)
    
    def _create_footer(self):
        """Crea il footer"""
        footer = tk.Frame(self.root, bg=self.COLORS['bg_dark'])
        footer.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        tk.Label(
            footer,
            text="Pomodoro Timer Pro v2.0 | Creato con ❤ per la produttività",
            font=("Segoe UI", 8),
            bg=self.COLORS['bg_dark'],
            fg=self.COLORS['fg_secondary']
        ).pack()
    
    # === GESTIONE TIMER ===
    
    def start_timer(self):
        """Avvia il timer"""
        if not self.running:
            if not self.paused:
                # Nuovo timer
                try:
                    minutes = int(self.study_time_spin.get())
                    self.remaining_time = minutes * 60
                    self.total_time = self.remaining_time
                    self.current_session = "Studio"
                    self.update_session_display()
                except ValueError:
                    messagebox.showerror("Errore", "Inserire un valore numerico valido")
                    return
            
            self.running = True
            self.paused = False
            self.update_button_states(running=True)
            
            # Avvia thread timer
            self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
            self.timer_thread.start()
    
    def pause_timer(self):
        """Mette in pausa il timer"""
        if self.running:
            self.running = False
            self.paused = True
            self.start_button.config(text="▶ RIPRENDI")
            self.update_button_states(paused=True)
    
    def stop_timer(self):
        """Ferma il timer"""
        self.running = False
        self.paused = False
        self.remaining_time = 0
        
        self.start_button.config(text="▶ AVVIA")
        self.update_button_states(running=False)
        
        # Reset display
        try:
            minutes = int(self.study_time_spin.get())
            self.update_timer_display(minutes * 60)
        except ValueError:
            self.update_timer_display(1500)  # Default 25 min
    
    def run_timer(self):
        """Loop principale del timer"""
        while self.running and self.remaining_time > 0:
            self.update_timer_display(self.remaining_time)
            self.update_progress_bar()
            time.sleep(1)
            self.remaining_time -= 1
        
        if self.remaining_time <= 0 and self.running:
            self.play_notification_sound()
            self.handle_session_complete()
    
    def handle_session_complete(self):
        """Gestisce il completamento di una sessione"""
        try:
            if self.current_session == "Studio":
                self.sessions_completed += 1
                self.update_stats()
                
                # Determina tipo di pausa
                sessions_threshold = int(self.sessions_before_long_spin.get())
                if self.sessions_completed % sessions_threshold == 0:
                    self.current_session = "Riposo Lungo"
                    minutes = int(self.long_break_spin.get())
                    message = f"🎉 Ottimo lavoro!\n\nHai completato {sessions_threshold} sessioni.\nInizio Riposo Lungo di {minutes} minuti."
                else:
                    self.current_session = "Riposo Breve"
                    minutes = int(self.short_break_spin.get())
                    message = f"✅ Sessione completata!\n\nPrenditi una pausa breve di {minutes} minuti."
            else:
                # Fine pausa
                self.current_session = "Studio"
                minutes = int(self.study_time_spin.get())
                message = f"🔔 Pausa terminata!\n\nTorna al lavoro. Sessione di {minutes} minuti."
            
            self.remaining_time = minutes * 60
            self.total_time = self.remaining_time
            self.update_session_display()
            
            # Mostra notifica
            self.root.after(0, lambda: messagebox.showinfo("Timer Completato", message))
            
            # Continua automaticamente
            if self.running:
                self.run_timer()
                
        except Exception as e:
            print(f"Errore gestione sessione: {e}")
            self.stop_timer()
    
    # === AGGIORNAMENTO UI ===
    
    def update_timer_display(self, seconds=None):
        """Aggiorna il display del tempo"""
        if seconds is None:
            try:
                seconds = int(self.study_time_spin.get()) * 60
            except:
                seconds = 1500
        
        minutes, secs = divmod(seconds, 60)
        time_string = f"{minutes:02d}:{secs:02d}"
        self.root.after(0, lambda: self.time_label.config(text=time_string))
    
    def update_progress_bar(self):
        """Aggiorna la barra di progresso"""
        if hasattr(self, 'total_time') and self.total_time > 0:
            progress = ((self.total_time - self.remaining_time) / self.total_time) * 100
            self.root.after(0, lambda: self.progress_bar.config(value=progress))
    
    def update_session_display(self):
        """Aggiorna il display della sessione corrente"""
        if self.current_session == "Studio":
            label = "📚 STUDIO"
            color = self.COLORS['accent_red']
        elif self.current_session == "Riposo Breve":
            label = "☕ RIPOSO BREVE"
            color = self.COLORS['accent_green']
        else:
            label = "🌴 RIPOSO LUNGO"
            color = self.COLORS['accent_green']
        
        self.root.after(0, lambda: self.session_label.config(text=label))
        self.root.after(0, lambda: self.time_label.config(fg=color))
    
    def update_stats(self):
        """Aggiorna le statistiche"""
        self.root.after(0, lambda: self.sessions_label.config(text=str(self.sessions_completed)))
        
        # Calcola prossima pausa
        try:
            threshold = int(self.sessions_before_long_spin.get())
            remaining = threshold - (self.sessions_completed % threshold)
            if remaining == threshold:
                next_break = "Lunga"
            else:
                next_break = "Breve"
            self.root.after(0, lambda: self.next_break_label.config(text=next_break))
        except:
            pass
    
    def update_button_states(self, running=False, paused=False):
        """Aggiorna lo stato dei pulsanti"""
        if running and not paused:
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL, bg=self.COLORS['bg_light'], fg=self.COLORS['fg_primary'])
            self.stop_button.config(state=tk.NORMAL, bg=self.COLORS['bg_light'], fg=self.COLORS['fg_primary'])
        elif paused:
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED, bg=self.COLORS['bg_medium'], fg=self.COLORS['fg_secondary'])
            self.stop_button.config(state=tk.NORMAL, bg=self.COLORS['bg_light'], fg=self.COLORS['fg_primary'])
        else:
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED, bg=self.COLORS['bg_medium'], fg=self.COLORS['fg_secondary'])
            self.stop_button.config(state=tk.DISABLED, bg=self.COLORS['bg_medium'], fg=self.COLORS['fg_secondary'])
    
    # === UTILITÀ ===
    
    def reset_sessions(self):
        """Resetta il contatore delle sessioni"""
        if messagebox.askyesno("Conferma Reset", "Vuoi azzerare il contatore delle sessioni?"):
            self.sessions_completed = 0
            self.update_stats()
    
    def play_notification_sound(self):
        """Riproduce il suono di notifica"""
        if not self.sound_var.get():
            return
        
        try:
            if SOUND_AVAILABLE:
                # Suono Windows
                for _ in range(3):
                    winsound.Beep(1000, 300)
                    time.sleep(0.1)
            else:
                # Fallback beep sistema
                print('\a')
        except Exception as e:
            print(f"Errore riproduzione suono: {e}")
    
    def save_settings(self):
        """Salva le impostazioni correnti"""
        try:
            self.config = {
                "study_time": int(self.study_time_spin.get()),
                "short_break": int(self.short_break_spin.get()),
                "long_break": int(self.long_break_spin.get()),
                "sessions_before_long": int(self.sessions_before_long_spin.get()),
                "sound_enabled": self.sound_var.get(),
                "auto_start_breaks": True,
                "auto_start_sessions": False
            }
            
            if self.config_manager.save_config(self.config):
                messagebox.showinfo("Successo", "Impostazioni salvate correttamente!")
            else:
                messagebox.showerror("Errore", "Impossibile salvare le impostazioni")
                
        except ValueError as e:
            messagebox.showerror("Errore", "Inserire valori numerici validi")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore salvataggio: {str(e)}")
    
    def load_settings_from_config(self):
        """Carica le impostazioni dalla configurazione"""
        try:
            self.study_time_spin.delete(0, tk.END)
            self.study_time_spin.insert(0, str(self.config["study_time"]))
            
            self.short_break_spin.delete(0, tk.END)
            self.short_break_spin.insert(0, str(self.config["short_break"]))
            
            self.long_break_spin.delete(0, tk.END)
            self.long_break_spin.insert(0, str(self.config["long_break"]))
            
            self.sessions_before_long_spin.delete(0, tk.END)
            self.sessions_before_long_spin.insert(0, str(self.config["sessions_before_long"]))
            
            self.sound_var.set(self.config["sound_enabled"])
        except Exception as e:
            print(f"Errore caricamento impostazioni: {e}")
    
    def on_closing(self):
        """Gestisce la chiusura dell'applicazione"""
        if self.running:
            if messagebox.askokcancel("Conferma Uscita", "Il timer è in esecuzione. Vuoi uscire?"):
                self.running = False
                time.sleep(0.1)
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    """Entry point dell'applicazione"""
    try:
        root = tk.Tk()
        app = PomodoroTimer(root)
        root.mainloop()
    except Exception as e:
        print(f"Errore critico: {e}")
        messagebox.showerror("Errore Critico", f"Si è verificato un errore:\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
