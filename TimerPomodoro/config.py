"""Gestione configurazione persistente"""
import json
from pathlib import Path


class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / ".pomodoro_timer"
        self.config_file = self.config_dir / "config.json"
        self.defaults = {
            "study_time": 25,
            "short_break": 5,
            "long_break": 15,
            "sessions_before_long": 4,
            "sound_enabled": True
        }
    
    def load(self):
        """Carica configurazione o restituisce default"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return {**self.defaults, **config}
        except:
            pass
        return self.defaults.copy()
    
    def save(self, config):
        """Salva configurazione"""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            return True
        except:
            return False