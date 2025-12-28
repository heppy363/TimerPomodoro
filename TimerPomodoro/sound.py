"""Gestione suoni e notifiche"""
import threading

try:
    import winsound
    SOUND_AVAILABLE = True
except ImportError:
    SOUND_AVAILABLE = False


def play_notification():
    """Suona una melodia piacevole"""
    if not SOUND_AVAILABLE:
        print('\a')
        return
    
    def play():
        # Melodia piacevole (Do-Mi-Sol-Do alto)
        notes = [
            (523, 200),  # Do
            (659, 200),  # Mi
            (784, 200),  # Sol
            (1047, 400), # Do alto
        ]
        
        try:
            for freq, duration in notes:
                winsound.Beep(freq, duration)
        except:
            print('\a')
    
    # Esegui in thread separato per non bloccare UI
    thread = threading.Thread(target=play, daemon=True)
    thread.start()