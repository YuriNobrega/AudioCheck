import os
import datetime
import schedule
import time
from pydub import AudioSegment
from pydub.utils import make_chunks
import numpy as np
import tkinter as tk
from tkinter import scrolledtext

def check_audio_modulation(folder_path, chunk_duration_ms=1000, silence_threshold=-50.0, max_duration_ms=60000):
    """
    Verifica se os arquivos de áudio em uma pasta estão modulando corretamente e se há som,
    limitando a análise a 1 minuto de cada arquivo.
    """
    logs.insert(tk.END, f'Iniciando análise em {folder_path}\n')
    for filename in os.listdir(folder_path):
        if filename.endswith('.mp3') or filename.endswith('.wav'):  # Adicione mais formatos se necessário
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
                
                # Verificar se o chunk é considerado silêncio
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
            logs.yview(tk.END)  # Atualizar a visualização dos logs

def find_folder():
    today = datetime.datetime.now().strftime('%d-%m-%y')
    folder_name = f"Dia {today}"
    base_folder = os.path.join(os.getcwd(), folder_name)
    if os.path.exists(base_folder):
        check_audio_modulation(base_folder)
    else:
        logs.insert(tk.END, f'Pasta {folder_name} não encontrada.\n')
        logs.yview(tk.END)

# Configuração da Interface Gráfica
root = tk.Tk()
root.title("Verificação de Modulação de Áudio")
root.geometry("600x400")

logs = scrolledtext.ScrolledText(root, width=80, height=20)
logs.pack(pady=20)

# Agendamento para horários específicos
schedule.every().day.at("07:00").do(find_folder)
schedule.every().day.at("12:00").do(find_folder)
schedule.every().day.at("18:00").do(find_folder)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Executar o agendamento em um thread separado
import threading
t = threading.Thread(target=run_schedule)
t.daemon = True
t.start()

root.mainloop()
