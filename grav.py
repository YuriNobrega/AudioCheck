import schedule
import time
from datetime import datetime
from pydub import AudioSegment
from pydub.utils import make_chunks
import numpy as np
import os
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext

def check_audio_modulation(folder_path, chunk_duration_ms=1000, silence_threshold=-50.0, max_duration_ms=60000):
    """
    Verifica se os 3 arquivos de áudio mais recentes em uma pasta estão modulando corretamente e se há som,
    limitando a análise a 1 minuto de cada arquivo.
    """
    logs.insert(tk.END, f'Iniciando análise em {folder_path}\n')
    
    # Listar todos os arquivos de áudio no diretório, junto com suas datas de modificação
    audio_files = [
        (filename, os.path.getmtime(os.path.join(folder_path, filename)))
        for filename in os.listdir(folder_path)
        if filename.endswith('.mp3') or filename.endswith('.ogg')  # Adicione mais formatos se necessário
    ]
    
    # Ordenar os arquivos pela data de modificação, do mais recente para o mais antigo
    audio_files.sort(key=lambda x: x[1], reverse=True)
    
    # Pegar apenas os 3 arquivos mais recentes
    audio_files = audio_files[:3]
    
    for filename, _ in audio_files:
        audio_path = os.path.join(folder_path, filename)
        audio = AudioSegment.from_file(audio_path)
        
        # Limitar o áudio a 1 minuto
        audio = audio[:max_duration_ms]
        
        logs.insert(tk.END, f'Analisando {filename} até {max_duration_ms / 1000} segundos...\n')
        
        # Dividir o áudio em chunks de duração especificada
        chunks = make_chunks(audio, chunk_duration_ms)
        silence_count = 0
        modulation_count = 0

        for chunk in chunks:
            rms = chunk.rms
            dBFS = 20 * np.log10(rms / 32767.0) if rms > 0 else float('-inf')
            
            # Verificar se o chunk é considerado silencioso
            if dBFS < silence_threshold:
                silence_count += 1
            else:
                modulation_count += 1

        if silence_count == len(chunks):
            logs.insert(tk.END, f'{filename}: Nenhum som detectado.\n')
        elif modulation_count > 0:
            logs.insert(tk.END, f'{filename}: Áudio modulando corretamente.\n')
        else:
            logs.insert(tk.END, f'{filename}: Som constante sem modulação detectada.\n')


def run_daily_checks():
    # Obter a data atual no formato DD-MM-YY
    current_date = datetime.now().strftime('%d%m%y')
    # Construir o nome do diretório do dia atual
    folder_name = f"Dia{current_date}"
    # Construir o caminho para o diretório do dia atual
    folder_path = os.path.join(base_folder.get(), folder_name)
    
    if os.path.exists(folder_path):
        logs.insert(tk.END, f'Executando verificações para o diretório: {folder_path}\n')
        check_audio_modulation(folder_path)
    else:
        logs.insert(tk.END, f'Diretório {folder_path} não encontrado.\n')
    logs.yview(tk.END)  # Atualizar a visualização dos logs

def start_schedule():
    schedule.every().day.at("07:00").do(run_daily_checks)
    schedule.every().day.at("12:00").do(run_daily_checks)
    schedule.every().day.at("18:00").do(run_daily_checks)
    threading.Thread(target=run_scheduler).start()
    logs.insert(tk.END, 'Agendamento iniciado para 7:00, 12:00 e 18:00.\n')

def stop_schedule():
    schedule.clear()
    logs.insert(tk.END, 'Agendamento parado.\n')

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)  # Verifica a cada minuto se há tarefas agendadas para executar

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        base_folder.set(folder_selected)
        logs.insert(tk.END, f'Pasta base selecionada: {folder_selected}\n')

# Criar a janela principal
root = tk.Tk()
root.title("Verificador de Áudio Automático")

base_folder = tk.StringVar()

tk.Label(root, text="Pasta base:").pack()
tk.Entry(root, textvariable=base_folder, width=50).pack()
tk.Button(root, text="Selecionar Pasta", command=select_folder).pack()
tk.Button(root, text="Iniciar Agendamento", command=start_schedule).pack()
tk.Button(root, text="Parar Agendamento", command=stop_schedule).pack()

logs = scrolledtext.ScrolledText(root, width=60, height=20)
logs.pack()

root.mainloop()
