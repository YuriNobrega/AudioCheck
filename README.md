
![project-img3 9727d0d3](https://github.com/user-attachments/assets/79ed15bf-ac9c-4749-83a4-117859fae35c)

# AudioCheck

A Python tool for automatically checking the RMS modulation of audio files in a folder, designed for scheduled use in a work environment.  
_Uma ferramenta em Python para checar automaticamente a modulação RMS de arquivos de áudio em uma pasta, projetada para uso agendado no ambiente de trabalho._

---

## 🎯 What This App Does / O que este app faz

**EN:**  
- Scans a folder for audio files named by date (e.g., `audio_20250728.wav`)
- Splits each audio into chunks and checks RMS modulation
- Logs if modulation is normal, absent, or too high
- Designed for pre-scheduled, automated use (e.g., Windows Task Scheduler)
- Output is shown in the front-end as a log

**PT:**  
- Varre uma pasta por arquivos de áudio nomeados pela data (ex: `audio_20250728.wav`)
- Divide cada áudio em pedaços e verifica a modulação RMS
- Registra se a modulação está normal, ausente ou muito alta
- Feito para uso automatizado e agendado (ex: Agendador de Tarefas do Windows)
- Saída exibida no front-end como um log

---

## 🏗️ Architecture Overview / Visão Geral da Arquitetura

```text
Audio Folder         AudioCheck (Python)         ffmpeg (System)
┌──────────────┐     ┌────────────────────┐     ┌───────────────┐
│  audio_*.wav │ →→  │ grav.py            │ →→  │ ffmpeg.exe    │
│  (by date)   │     │ (RMS Analysis)     │     │ (audio decode)│
└──────────────┘     └────────────────────┘     └───────────────┘
         │                    │                        │
         ▼                    ▼                        ▼
┌──────────────┐     ┌────────────────────┐     ┌───────────────┐
│  Newest file │     │  Chunk splitting   │     │  Audio chunks │
│  selection   │     │  RMS calculation   │     │  Processing   │
└──────────────┘     └────────────────────┘     └───────────────┘
```

---

## 📁 Project Structure / Estrutura do Projeto

```text
AudioCheck/
├── build/grav/           # Build artifacts
├── dist/                 # Distribution files
├── ffmpeg/               # ffmpeg binaries (if included)
├── grav.py               # Main script for audio checking
├── grav.spec             # PyInstaller spec file
├── .gitattributes        # Git settings
└── README.md             # This file
```

---

## 🚀 Setup Instructions / Instruções de Instalação

### Prerequisites / Pré-requisitos

**EN:**  
- Python 3.x  
- [pydub](https://github.com/jiaaro/pydub)  
- [ffmpeg](https://ffmpeg.org/) (must be installed and added to the PATH)  
- Tested on Windows

**PT:**  
- Python 3.x  
- [pydub](https://github.com/jiaaro/pydub)  
- [ffmpeg](https://ffmpeg.org/) (deve estar instalado e no PATH)  
- Testado no Windows

---

### Installation / Instalação

**EN:**  
1. Install Python 3.x from [python.org](https://www.python.org/downloads/)
2. Install pydub:
   ```sh
   pip install pydub
   ```
3. Download and install ffmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
4. Add ffmpeg to your system PATH

**PT:**  
1. Instale o Python 3.x em [python.org](https://www.python.org/downloads/)
2. Instale o pydub:
   ```sh
   pip install pydub
   ```
3. Baixe e instale o ffmpeg em [ffmpeg.org](https://ffmpeg.org/download.html)
4. Adicione o ffmpeg ao PATH do sistema

---

## 🏃 Usage / Uso

**EN:**  
- Place your audio files in the target folder, named by date (e.g., `audio_20250728.wav`)
- Schedule the script to run automatically (e.g., with Windows Task Scheduler)
- When run, it will:
  1. Find the most recent audio file(s)
  2. Split each into chunks
  3. Analyze RMS modulation for each chunk
  4. Log the results in the front-end

**PT:**  
- Coloque os arquivos de áudio na pasta alvo, nomeados pela data (ex: `audio_20250728.wav`)
- Agende o script para rodar automaticamente (ex: Agendador de Tarefas do Windows)
- Ao rodar, ele irá:
  1. Encontrar o(s) arquivo(s) de áudio mais recente(s)
  2. Dividir cada um em pedaços
  3. Analisar a modulação RMS de cada pedaço
  4. Registrar os resultados no front-end

---

## 📝 Output & Log / Saída & Log

**EN:**  
- The log will indicate:
  - **Normal**: Controlled modulation detected
  - **Error**: No modulation detected
  - **Warning**: High modulation detected

**PT:**  
- O log irá indicar:
  - **Normal**: Modulação controlada detectada
  - **Erro**: Nenhuma modulação detectada
  - **Aviso**: Modulação alta detectada

---

## 🐛 Troubleshooting / Dicas

**EN:**  
- If you get errors about ffmpeg, make sure it’s installed and the path is set in your environment variables.
- Only tested on Windows; behavior on other OS may vary.

**PT:**  
- Se aparecer erro sobre ffmpeg, confira se está instalado e se o caminho está no PATH do sistema.
- Testado apenas no Windows; o comportamento em outros sistemas pode variar.

---

## 👨‍💻 Credits / Créditos

**EN:**  
Developed by Yuri Nobrega for internal use.

**PT:**  
Desenvolvido por Yuri Nobrega para uso interno.
