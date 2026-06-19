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
# 0. VARIÁVEIS DE INTENSIDADE
# ==========================================================
fator = 2 # porcentagem

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
    print("❌ Nenhum Arduino encontrado! Verifique o cabo USB.")
    exit()

try:
    arduino = serial.Serial(porta_automatica, 115200, timeout=0.1)
    time.sleep(2) 
    print(f"✅ Conectado com sucesso na porta: {porta_automatica}!\n") 
except Exception as e:
    print(f"❌ Erro ao conectar: {e}")
    exit()

# ==========================================================
# 2. FILTRO AMPLO (PEGA TUDO: 60Hz até 4000Hz)
# ==========================================================
taxa_amostra = 48000
nyq = 0.5 * taxa_amostra

# Filtro bem aberto para não ignorar absolutamente nenhum instrumento ou voz do jogo
limite_baixo = 40 / nyq # Graves
limite_alto = 6000 / nyq # Agudos
b, a = butter(3, [limite_baixo, limite_alto], btype='bandpass')

# Históricos para a Sensibilidade Inteligente
historico_curto = [0.0] * 5    # Segue o ritmo frenético das notas
historico_longo = [0.0] * 40   # Entende o volume geral da música de fundo
volume_max_detectado = 0.2

tempo_ultima_batida = 0
cooldown_batida = 0.06  # 60ms ideal para FNF e Muse Dash

caixa_som = sc.default_speaker()

print("=" * 60)
print(f"🎮 MODO TOTAL: GRAVES + AGUDOS REATIVOS")
print(f"🎧 Escutando: {caixa_som.name}")
print("=" * 60)
print("Pressione CTRL+C para encerrar.\n")

# ==========================================================
# 3. LOOP DE CAPTURA
# ==========================================================
try:
    with sc.get_microphone(id=str(caixa_som.id), include_loopback=True).recorder(samplerate=taxa_amostra) as mic:
        while True:
            audio_bruto = mic.record(numframes=1024)
            audio_filtrado = lfilter(b, a, audio_bruto[:, 0])
            
            # Voltamos para a energia real do som (RMS), que nunca falha
            forca_atual = np.sqrt(np.mean(audio_filtrado**2))

            media_curta = sum(historico_curto) / len(historico_curto)
            media_longa = sum(historico_longo) / len(historico_longo)
            tempo_atual = time.time()

            # AJUSTE AUTOMÁTICO DE BRINDE:
            # Se a música inteira estiver baixa, o limite mínimo cai para aceitar tons médios
            if media_longa < 0.015:
                fator_gatilho = 1.15      # Exige só 15% de aumento (super sensível)
                limite_silencio = 0.005   # Quase zero (pega qualquer barulhinho)
            else:
                fator_gatilho = 1.30      # Exige 30% de aumento no refrão barulhento
                limite_silencio = 0.02

            # LÓGICA DA BATIDA: O som atual precisa superar a média dos últimos milissegundos
            if forca_atual > (media_curta * fator_gatilho) and forca_atual > limite_silencio and (tempo_atual - tempo_ultima_batida > cooldown_batida):
                
                if forca_atual > volume_max_detectado:
                    volume_max_detectado = forca_atual
                
                # Transforma a força em sinal para o motor (100 a 255)
                valor_motor = int(np.interp(forca_atual, [limite_silencio, volume_max_detectado], [100, 255]))
                valor_motor = int(fator * valor_motor)
                valor_motor = max(100, min(255, valor_motor))
                
                tempo_ultima_batida = tempo_atual
                
                # Envia para o Arduino
                arduino.write(f"{valor_motor}\n".encode())
                
                # Gráfico do terminal
                tamanho_barra = int(np.interp(valor_motor, [100, 255], [5, 40]))
                print(f"💥 NOTA | {'█' * tamanho_barra}{' ' * (45 - tamanho_barra)} [Força: {valor_motor:03d}]")
            
            # Atualiza os históricos
            historico_curto.pop(0)
            historico_curto.append(forca_atual)
            
            historico_longo.pop(0)
            historico_longo.append(forca_atual)

except KeyboardInterrupt:
    print("\n⏹ Parado pelo usuário.")
finally:
    if 'arduino' in locals() and arduino.is_open:
        arduino.write(b"0\n")
        arduino.close()