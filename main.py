import os
import numpy as np
import soundcard as sc
import serial
import time
import warnings
import serial.tools.list_ports
from scipy.signal import butter, lfilter

warnings.filterwarnings("ignore", category=sc.SoundcardRuntimeWarning)
os.system('cls' if os.name == 'nt' else 'clear')

# ==========================================================
# 1. FUNÇÃO DE AUTODETECÇÃO DO ARDUINO
# ==========================================================
def descobrir_porta_arduino():
    portas = serial.tools.list_ports.comports()
    for porta in portas:
        desc = porta.description.upper()
        if "ARDUINO" in desc or "CH340" in desc or "USB SERIAL" in desc or "CP210" in desc:
            return porta.device
    return portas[-1].device if portas else None

print("🔍 Buscando Arduino...")
porta_automatica = descobrir_porta_arduino()

if not porta_automatica:
    print("❌ Nenhum Arduino encontrado!")
    exit()

try:
    arduino = serial.Serial(porta_automatica, 115200, timeout=0.1)
    time.sleep(2)
    print(f"✅ Conectado automaticamente na porta: {porta_automatica}!\n") 
except Exception as e:
    print(f"❌ Erro ao conectar: {e}\nFeche o Serial Monitor da IDE do Arduino e tente de novo.")
    exit()

# ==========================================================
# 2. PREPARANDO O FILTRO E O ÁUDIO
# ==========================================================
taxa_amostra = 48000
b, a = butter(5, 150 / (taxa_amostra * 0.5), btype='low') # Filtro de Graves

historico_graves = [0.0] * 12  # Memória curta do som de fundo

# --- O SEGREDO DO ENCAIXE MUSICAL ---
tempo_ultima_batida = 0
cooldown_batida = 0.1  # Segundos que o motor "descansa" entre um soco e outro (0.1 = 100ms)

caixa_som = sc.default_speaker()
print(f"🔊 Escutando os graves de: {caixa_som.name}...")
print("Pressione CTRL+C no terminal para encerrar.\n")

# ==========================================================
# 3. O LOOP PRINCIPAL (TEMPO REAL)
# ==========================================================
volume_max_detectado = 0.5
try:
    with sc.get_microphone(id=str(caixa_som.id), include_loopback=True).recorder(samplerate=taxa_amostra) as mic:
        while True:
            
            audio_bruto = mic.record(numframes=1024)
            audio_filtrado = lfilter(b, a, audio_bruto[:, 0])
            forca_atual = np.max(np.abs(audio_filtrado))

            media_recente = sum(historico_graves) / len(historico_graves)
            tempo_atual = time.time()

            # A BATIDA ACONTECE SE:
            # 1. É 35% mais alta que o fundo (pico)
            # 2. Não é só ruído estático (> 0.05)
            # 3. Já passou o tempo do cooldown
            if forca_atual > (media_recente * 1.35) and forca_atual > 0.05 and (tempo_atual - tempo_ultima_batida > cooldown_batida):
                
                # Ajuste dinâmico: Se a música for muito alta, ele recalibra o pico
                if forca_atual > volume_max_detectado:
                    volume_max_detectado = forca_atual
                
                # Mapeia a força atual baseada no que foi o volume máximo até agora
                # Isso faz com que batidas fracas virem vibrações fracas, e batidas fortes virem vibrações máximas
                valor_motor = int(np.interp(forca_atual, [0.05, volume_max_detectado], [80, 255]))
                valor_motor = max(80, min(255, valor_motor)) 
                
                tempo_ultima_batida = tempo_atual
                print(f"💥 BATIDA VARIÁVEL! Força: {valor_motor:03d}")
            else:
                valor_motor = 0

            historico_graves.pop(0)
            historico_graves.append(forca_atual)

            arduino.write(f"{valor_motor}\n".encode())

except KeyboardInterrupt:
    print("\n⏹ Instrução de parada recebida.")
finally:
    if 'arduino' in locals() and arduino.is_open:
        arduino.write(b"0\n")
        arduino.close()
        print("🔌 Conexão com o Arduino encerrada.")