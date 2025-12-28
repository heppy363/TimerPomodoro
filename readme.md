# 🍅 Pomodoro Timer Pro - Guida Completa

## Descrizione
Applicazione desktop Windows per gestire il tempo di studio con la tecnica Pomodoro completamente personalizzabile.

## Funzionalità
✅ Timer completamente personalizzabile
✅ Modalità Pomodoro con intervalli configurabili
✅ Notifica sonora allo scadere del tempo
✅ Contatore sessioni completate
✅ Riposo breve e lungo personalizzabili
✅ Pausa e ripresa del timer
✅ Interfaccia grafica intuitiva
✅ Gestione dipendenze con UV (velocissimo!)

## 🚀 Come Creare l'Eseguibile .EXE (METODO CONSIGLIATO CON UV)

### ⚡ Metodo Rapido - Automatico

1. **Scarica tutti i file** nella stessa cartella
2. **Fai doppio click** su `setup_uv.bat` (prima volta - installa tutto)
3. **Fai doppio click** su `crea_exe_uv.bat` (crea l'exe)
4. **Trova l'exe** in `dist/PomodoroTimer.exe`

Fatto! 🎉

### 📝 Cosa Succede Automaticamente

**setup_uv.bat** fa:
- Installa UV (package manager ultra-veloce)
- Crea ambiente virtuale Python isolato
- Installa tutte le dipendenze necessarie

**crea_exe_uv.bat** fa:
- Attiva l'ambiente virtuale
- Compila l'applicazione in .exe
- Apre la cartella con l'eseguibile

### 🔧 Metodo Manuale (se preferisci il controllo)

#### Passo 1: Installare UV
Apri PowerShell e digita:
```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

#### Passo 2: Creare Ambiente e Installare Dipendenze
```bash
# Crea ambiente virtuale
uv venv

# Attiva ambiente
.venv\Scripts\activate

# Installa dipendenze dal pyproject.toml
uv pip install -e .
```

#### Passo 3: Creare l'Eseguibile
```bash
pyinstaller --onefile --windowed --name "PomodoroTimer" pomodoro_timer.py
```

#### Passo 4: Trovare l'Eseguibile
L'exe si trova in:
```
dist/PomodoroTimer.exe
```

---

## 📦 Metodo Alternativo - Con PIP (vecchio metodo)

### Passo 1: Installare Python
1. Scarica Python da https://www.python.org/downloads/
2. Durante l'installazione, **seleziona "Add Python to PATH"**
3. Completa l'installazione

### Passo 2: Installare PyInstaller
```bash
pip install pyinstaller
```

### Passo 3: Creare l'Eseguibile
```bash
pyinstaller --onefile --windowed --name "PomodoroTimer" pomodoro_timer.py
```

## Risoluzione Problemi

### 🌟 Perché UV invece di PIP?

**UV è 10-100x più veloce!**
- ⚡ Scritto in Rust (super performante)
- 📦 Gestione dipendenze migliore
- 🔒 Lock file automatico
- 🎯 Risoluzione conflitti più intelligente
- 💾 Cache globale (risparmia spazio)

**Quando usare cosa:**
- ✅ **UV** - Se vuoi il meglio (consigliato!)
- ⚪ **PIP** - Se hai problemi con UV o preferisci il classico

### Problema: "uv non è riconosciuto"
**Soluzione:** Chiudi e riapri il Prompt dei Comandi dopo aver installato PyInstaller

### Problema: Errore durante la creazione dell'exe
**Soluzione:** Assicurati di essere nella cartella corretta con il comando:
```bash
cd C:\percorso\alla\cartella
```

### Problema: L'antivirus blocca l'eseguibile
**Soluzione:** Aggiungi un'eccezione nell'antivirus per il file .exe creato (è un falso positivo comune)

## Comandi Utili

### Verificare installazione Python:
```bash
python --version
```

### Verificare installazione PyInstaller:
```bash
pyinstaller --version
```

### Navigare in una cartella:
```bash
cd C:\Users\TuoNome\Desktop\MiaCartella
```

### Visualizzare file nella cartella corrente:
```bash
dir
```

## Personalizzazione

Puoi modificare i valori predefiniti nel codice:
- **Riga 91:** Tempo studio predefinito (default: 25 minuti)
- **Riga 103:** Tempo riposo breve (default: 5 minuti)
- **Riga 115:** Tempo riposo lungo (default: 15 minuti)
- **Riga 127:** Sessioni prima del riposo lungo (default: 4)

## Come Usare l'Applicazione

1. **Avvia** il timer con il pulsante ▶ Avvia
2. **Pausa** il timer con il pulsante ⏸ Pausa
3. **Ferma** il timer con il pulsante ⏹ Stop
4. **Personalizza** i tempi nelle impostazioni prima di avviare
5. **Reset** il contatore sessioni quando vuoi ricominciare

## Note Tecniche
- Sviluppato in Python 3
- Interfaccia grafica: Tkinter (incluso in Python)
- Audio: winsound (Windows nativo)
- Nessuna dipendenza esterna richiesta

## Licenza
Libero per uso personale

---
Creato con ❤️ per migliorare la produttività