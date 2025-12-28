"""Logica del timer Pomodoro"""
import threading
import time


class PomodoroLogic:
    def __init__(self, on_tick, on_complete):
        self.on_tick = on_tick  # Callback per aggiornamento tempo
        self.on_complete = on_complete  # Callback per completamento
        
        self.running = False
        self.paused = False
        self.current_session = "Studio"
        self.sessions_completed = 0
        self.remaining_time = 0
        self.total_time = 0
        self.timer_thread = None
        
        # Impostazioni (verranno sovrascritte da config)
        self.study_time = 25
        self.short_break = 5
        self.long_break = 15
        self.sessions_before_long = 4
    
    def set_times(self, study, short_break, long_break, sessions):
        """Imposta i tempi"""
        self.study_time = study
        self.short_break = short_break
        self.long_break = long_break
        self.sessions_before_long = sessions
    
    def start(self):
        """Avvia timer"""
        if not self.running:
            if not self.paused:
                # Nuovo timer
                self.remaining_time = self.study_time * 60
                self.total_time = self.remaining_time
                self.current_session = "Studio"
            
            self.running = True
            self.paused = False
            self.timer_thread = threading.Thread(target=self._run, daemon=True)
            self.timer_thread.start()
            return True
        return False
    
    def pause(self):
        """Mette in pausa"""
        if self.running:
            self.running = False
            self.paused = True
            return True
        return False
    
    def stop(self):
        """Ferma timer"""
        self.running = False
        self.paused = False
        self.remaining_time = 0
        return True
    
    def reset_sessions(self):
        """Resetta contatore sessioni"""
        self.sessions_completed = 0
    
    def _run(self):
        """Loop principale timer"""
        while self.running and self.remaining_time > 0:
            self.on_tick(self.remaining_time, self.total_time)
            time.sleep(1)
            self.remaining_time -= 1
        
        if self.remaining_time <= 0 and self.running:
            self._complete_session()
    
    def _complete_session(self):
        """Gestisce completamento sessione"""
        if self.current_session == "Studio":
            self.sessions_completed += 1
            
            # Determina tipo pausa
            if self.sessions_completed % self.sessions_before_long == 0:
                self.current_session = "Riposo Lungo"
                self.remaining_time = self.long_break * 60
                msg_type = "long_break"
            else:
                self.current_session = "Riposo Breve"
                self.remaining_time = self.short_break * 60
                msg_type = "short_break"
        else:
            # Fine pausa
            self.current_session = "Studio"
            self.remaining_time = self.study_time * 60
            msg_type = "study"
        
        self.total_time = self.remaining_time
        self.on_complete(msg_type, self.current_session, self.sessions_completed)
        
        # Continua automaticamente
        if self.running:
            self._run()
    
    def get_progress(self):
        """Restituisce progresso 0-100"""
        if self.total_time > 0:
            return ((self.total_time - self.remaining_time) / self.total_time) * 100
        return 0
    
    def get_next_break_type(self):
        """Restituisce tipo prossima pausa"""
        remaining = self.sessions_before_long - (self.sessions_completed % self.sessions_before_long)
        return "Lunga" if remaining == self.sessions_before_long else "Breve"