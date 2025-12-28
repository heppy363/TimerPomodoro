# 🍅 Pomodoro Timer Pro 2.0

![Version](https://img.shields.io/badge/version-2.0-red)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**Timer Pomodoro professionale con interfaccia grafica moderna** per massimizzare la tua produttività.

## ✨ Caratteristiche Principali

### 🎨 Interfaccia Moderna
- Design pulito con sfumature di **nero, grigio e rosso**
- Barra di progresso visuale
- Statistiche in tempo reale
- Effetti visivi per distinguere studio e pause

### ⚙️ Funzionalità Complete
- ✅ Timer completamente personalizzabile
- ✅ Modalità Pomodoro automatica (studio → pausa breve → studio → pausa lunga)
- ✅ **Salvataggio automatico delle impostazioni**
- ✅ Notifiche sonore configurabili
- ✅ Contatore sessioni completate
- ✅ Pausa e ripresa del timer
- ✅ Barra di progresso visiva
- ✅ Statistiche prossima pausa

### 🔧 Impostazioni Personalizzabili
- ⏱ Tempo sessione studio (1-120 min)
- ☕ Tempo pausa breve (1-60 min)
- 🌴 Tempo pausa lunga (1-120 min)
- 🔄 Numero sessioni prima della pausa lunga (1-10)
- 🔊 Notifiche sonore on/off

## 🚀 Installazione e Creazione Eseguibile

### Metodo 1: Automatico (CONSIGLIATO) ⚡

**Per utenti Windows:**

1. **Scarica tutto il progetto** in una cartella
2. **Doppio click** su `setup.bat` *(prima volta - configura tutto)*
3. **Doppio click** su `crea_exe.bat` *(crea l'eseguibile)*
4. **Trova l'exe** in `dist/PomodoroTimerPro.exe`

✨ **Fatto!** Non serve installare nulla manualmente.

### Metodo 2: Esecuzione Diretta Python 🐍

Se vuoi solo testare senza creare l'exe:

```bash
# Esegui setup
setup.bat

# Esegui l'app
.venv\Scripts\python.exe pomodoro_timer.py
```

### Metodo 3: Manuale (per sviluppatori) 🛠️

```bash
# 1. Installa UV (package manager veloce)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. Crea ambiente virtuale
uv venv

# 3. Attiva ambiente
.venv\Scripts\activate

# 4. Installa dipendenze
uv pip install -e .

# 5. Crea eseguibile
pyinstaller --onefile --windowed --name "PomodoroTimerPro" pomodoro_timer.py
```

## 📁 Struttura del Progetto

```
pomodoro-timer-pro/
├── pomodoro_timer.py     # Applicazione principale
├── pyproject.toml        # Configurazione dipendenze
├── setup.bat             # Script setup automatico
├── crea_exe.bat          # Script creazione exe
├── README.md             # Questa documentazione
├── .gitignore           # File da ignorare in Git
├── .venv/               # Ambiente virtuale (creato da setup)
└── dist/                # Eseguibile finale (creato da crea_exe)
    └── PomodoroTimerPro.exe
```

## 💾 Configurazione Automatica

Le impostazioni vengono salvate automaticamente in:
```
C:\Users\TuoNome\.pomodoro_timer\config.json
```

**Vantaggi:**
- ✅ Le tue impostazioni vengono ricordate
- ✅ Non devi riconfigurare ogni volta
- ✅ Backup e ripristino facile

## 🎯 Come Usare l'Applicazione

### Primo Avvio
1. **Personalizza** i timer nelle impostazioni
2. Clicca **"💾 Salva Impostazioni"** per ricordare le preferenze
3. Clicca **"▶ AVVIA"** per iniziare

### Durante l'Uso
- **⏸ PAUSA** → Mette in pausa il timer corrente
- **⏹ STOP** → Ferma e resetta il timer
- **🔄 Reset Contatore** → Azzera le sessioni completate

### Ciclo Pomodoro Automatico
L'app gestisce automaticamente il ciclo:
1. **Studio** (es. 25 min) → Notifica
2. **Pausa Breve** (es. 5 min) → Notifica
3. **Studio** → Pausa Breve → ...
4. Dopo N sessioni → **Pausa Lunga** (es. 15 min)

## 🐛 Risoluzione Problemi

### ❌ Errore: "pomodoro_timer.py non trovato"

**QUESTO È IL TUO PROBLEMA!**

**Causa:** Gli script `.bat` cercano il file Python nella cartella corrente, ma il file si trova altrove.

**Soluzione:**
1. Assicurati che **tutti i file** siano nella **stessa cartella**:
   ```
   MiaCartella/
   ├── pomodoro_timer.py    ← Deve essere qui!
   ├── setup.bat
   ├── crea_exe.bat
   └── pyproject.toml
   ```

2. Non mettere gli script in sottocartelle tipo `script/`

3. Verifica di essere nella cartella corretta:
   ```bash
   # Apri prompt comandi nella cartella
   # Controlla i file presenti
   dir
   
   # Dovresti vedere pomodoro_timer.py
   ```

### ❌ "UV non è riconosciuto"

**Soluzione:** Chiudi e **riapri** il Prompt dei Comandi dopo l'installazione di UV.

### ❌ L'antivirus blocca l'exe

**Causa:** È un **falso positivo** (normale per exe creati con PyInstaller)

**Soluzione:**
1. Aggiungi un'eccezione nell'antivirus per `dist/PomodoroTimerPro.exe`
2. Oppure carica l'exe su [VirusTotal](https://www.virustotal.com) per verificare

### ❌ Errore durante la creazione dell'exe

**Possibili cause:**
- Antivirus troppo aggressivo
- Spazio su disco insufficiente
- Permessi mancanti

**Soluzioni:**
1. Esegui il prompt comandi **come Amministratore**
2. Disattiva temporaneamente l'antivirus
3. Libera spazio su disco

## 🎨 Personalizzazione Avanzata

### Modifica Colori

Apri `pomodoro_timer.py` e cerca la sezione `COLORS`:

```python
COLORS = {
    'bg_dark': '#1a1a1a',        # Nero profondo
    'accent_red': '#e63946',     # Rosso accento
    # ... modifica come preferisci
}
```

### Modifica Valori Predefiniti

Nel file `pomodoro_timer.py`, cerca `default_config`:

```python
self.default_config = {
    "study_time": 25,              # Minuti studio
    "short_break": 5,              # Pausa breve
    "long_break": 15,              # Pausa lunga
    "sessions_before_long": 4,     # Sessioni prima pausa lunga
}
```

## 🆚 Perché UV invece di PIP?

**UV è 10-100x più veloce!**

| Caratteristica | UV | PIP |
|---------------|-----|-----|
| Velocità | ⚡⚡⚡ | ⚪ |
| Scritto in | Rust | Python |
| Gestione dipendenze | Intelligente | Basica |
| Cache globale | ✅ | ❌ |
| Lock file | Automatico | Manuale |

**Quando usare cosa:**
- ✅ **UV** → Migliore performance (CONSIGLIATO)
- ⚪ **PIP** → Se hai problemi con UV

## 📊 Requisiti di Sistema

- **OS:** Windows 10/11 (testato), Linux/Mac (dovrebbe funzionare)
- **Python:** 3.8 o superiore
- **RAM:** 512 MB minimo
- **Spazio:** ~50 MB per l'exe finale

## 🔐 Privacy e Sicurezza

- ✅ **Nessun dato inviato online**
- ✅ Configurazioni salvate solo localmente
- ✅ Nessuna telemetria
- ✅ Open source e modificabile

## 📝 Changelog

### v2.0 (Corrente)
- 🎨 Interfaccia completamente ridisegnata (nero/grigio/rosso)
- 💾 Salvataggio automatico impostazioni
- 📊 Barra di progresso visuale
- 📈 Statistiche prossima pausa
- 🔧 Gestione errori migliorata
- 🏗️ Struttura progetto riorganizzata
- ⚡ Supporto UV package manager

### v1.0
- Versione iniziale

## 🤝 Contribuire

Contributi, issues e feature requests sono benvenuti!

1. Fork il progetto
2. Crea un branch (`git checkout -b feature/AmazingFeature`)
3. Commit le modifiche (`git commit -m 'Add AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📜 Licenza

MIT License - Libero per uso personale e commerciale

## 🙏 Crediti

- Basato sulla [Tecnica Pomodoro](https://francescocirillo.com/pages/pomodoro-technique) di Francesco Cirillo
- Icone emoji di sistema
- Font Segoe UI (Windows) / San Francisco (Mac) / Roboto (Linux)

## 📧 Supporto

Hai problemi? Suggerimenti?

1. Controlla la sezione **Risoluzione Problemi** sopra
2. Apri una [Issue](https://github.com/tuousername/pomodoro-timer-pro/issues)
3. Leggi la documentazione completa

---

**Creato con ❤️ per migliorare la produttività**

*Ricorda: La tecnica Pomodoro funziona meglio quando la usi con costanza!*
