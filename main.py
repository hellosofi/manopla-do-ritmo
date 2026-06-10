import os
os.system('cls' if os.name == 'nt' else 'clear')
##
import soundcard as sc
import numpy as np
import serial
import time
import warnings 
warnings.filterwarnings("ignore", category=sc.SoundcardRuntimeWarning)

# --- CONFIGURAÇÃO DO ARDUINO ---
PORTA_COM = 'COM3'  # Escolher porta: ('COM3', 'COM4', 'COM5', etc.)
BAUD_RATE = 115200

try:
    arduino = serial.Serial(PORTA_COM, BAUD_RATE, timeout=0.1)
    time.sleep(2)  # Tempo necessário para o Arduino reiniciar após conectar

    # emojis pro visual
    print(f"✅ Conectado com sucesso ao Arduino na porta {PORTA_COM}!")
except Exception as e:
    print(f"❌ Erro ao conectar no Arduino. Verifique se a porta {PORTA_COM} está correta ou se o Serial Monitor da IDE está aberto.")
    print(f"Detalhe do erro: {e}")
    exit()

# --- CAPTURA DE ÁUDIO ---
# Busca todas as caixas de som e escolhe a primeira da lista de forma segura
caixas_disponiveis = sc.all_speakers()

if not caixas_disponiveis:
    print("❌ Nenhuma caixa de som ou fone de ouvido foi encontrado no sistema!")
    arduino.close()
    exit()

# Seleciona a caixa de som padrão atual por índice, evitando o erro de ID
caixa_som = caixas_disponiveis[0] 

print(f"🔊 Dispositivo de áudio selecionado: {caixa_som.name}")
print("🎵 Capturando o áudio interno do PC...")
print("Abra o 'Serial Plotter' na IDE do Arduino para ver o gráfico das batidas!")
print("Pressione CTRL+C no terminal para encerrar.")

# 'include_loopback=True' para garantir que o Windows permita gravar o som interno
with sc.get_microphone(caixa_som.name, include_loopback=True).recorder(samplerate=44100) as mic:
    while True:
        try:
           
            dados_audio = mic.record(numframes=1024)
            canal_mono = dados_audio[:, 0]
            rms = np.sqrt(np.mean(canal_mono**2))
            amplitude_mapeada = rms * 2500 
            amplitude_final = int(max(0, min(500, amplitude_mapeada)))
            
            
            print(f"Batida: {amplitude_final}") 
            
            arduino.write(f"{amplitude_final}\n".encode())
            
            
        except KeyboardInterrupt:
            print("\nInstrução de parada recebida. Encerrando programa...")
            arduino.close()
            break
        except Exception as e:
            print(f"Ocorreu um erro durante a captura: {e}")
            break