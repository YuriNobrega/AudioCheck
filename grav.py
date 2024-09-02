import schedule
import time
from datetime import datetime
from pydub import AudioSegment
from pydub.utils import make_chunks
import numpy as np
import os

def check_audio_modulation(folder_path, chunk_duration_ms=1000, silence_threshold=-50.0, max_duration_ms=60000):
    """
    Verifica se os arquivos de áudio em uma pasta estão modulando corretamente e se há som,
    limitando a análise a 1 minuto de cada arquivo.
    """
    for filename in os.listdir(folder_path):
        if filename.endswith('.mp3') or filename.endswith('.wav'):  # Adicione mais formatos se necessário
            audio_path = os.path.join(folder_path, filename)
            audio = AudioSegment.from_file(audio_path)
            
            # Limitar o áudio a 1 minuto
            audio = audio[:max_duration_ms]
            
            print(f'Analisando {filename} até {max_duration_ms / 1000} segundos...')
            
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
                print(f'{filename}: Nenhum som detectado.')
            elif modulation_count > 0:
                print(f'{filename}: Áudio modulando corretamente.')
            else:
                print(f'{filename}: Som constante sem modulação detectada.')

def run_daily_checks():
    # Obter a data atual no formato YYYY-MM-DD
    current_date = datetime.now().strftime('%Y-%m-%d')
    # Construir o caminho para o diretório do dia atual
    folder_path = os.path.join(r'', current_date)
    
    if os.path.exists(folder_path):
        print(f'Executando verificações para o diretório: {folder_path}')
        check_audio_modulation(folder_path)
    else:
        print(f'Diretório {folder_path} não encontrado.')

# Agendar as verificações para os horários especificados
schedule.every().day.at("07:00").do(run_daily_checks)
schedule.every().day.at("12:00").do(run_daily_checks)
schedule.every().day.at("18:00").do(run_daily_checks)

# Loop para manter o agendamento em execução
while True:
    schedule.run_pending()
    time.sleep(60)  # Verifica a cada minuto se há tarefas agendadas para executar
