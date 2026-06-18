# Detector de Batidas com Arduino

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Arduino](https://img.shields.io/badge/Arduino-Compatible-00979D?style=for-the-badge&logo=arduino&logoColor=white)](https://www.arduino.cc/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

Sistema em **Python + Arduino** para detectar batidas musicais em tempo real e controlar um motor via PWM com resposta suave.

O projeto foi pensado para aplicações como:

- jogos de ritmo
- feedback tátil
- automação reativa ao áudio
- efeitos musicais interativos

---

## Preview

Este projeto captura o áudio do computador, detecta batidas e envia a intensidade para o Arduino, que controla o motor com resposta rápida e desaceleração suave.

---

## Índice

- [Visão geral](#visão-geral)
- [Como funciona](#como-funciona)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Como usar](#como-usar)
- [Ligação do motor](#ligação-do-motor)
- [Configurações importantes](#configurações-importantes)
- [Problemas comuns](#problemas-comuns)
- [Estrutura dos valores enviados](#estrutura-dos-valores-enviados)
- [Melhorias futuras](#melhorias-futuras)
- [Licença](#licença)
- [Autor](#autor)

---

## Visão geral

O projeto é dividido em duas partes principais:

### Python
Responsável pela inteligência do sistema:

- captura o áudio do sistema em tempo real
- filtra frequências relevantes para destacar a batida
- detecta batidas com base em energia e variação do sinal
- envia a intensidade da batida para o Arduino via serial

### Arduino
Responsável pela atuação física:

- recebe os valores enviados pelo Python
- converte a intensidade em PWM
- controla um motor com subida rápida e desaceleração suave

---

## Como funciona

O fluxo do sistema é o seguinte:

1. O Python captura o áudio da saída do computador.
2. O áudio passa por um filtro para destacar graves e médio-graves.
3. O algoritmo identifica o "ataque" da batida.
4. A intensidade detectada é convertida em um valor serial.
5. O Arduino recebe esse valor.
6. O motor é acionado proporcionalmente, com suavização no tempo.

---

## Estrutura do projeto

```text
seu-projeto/
├── detector_batida.py
├── controle_motor.ino
├── LICENSE
├── README.md
└── requirements.txt
```

### Arquivos principais

- `detector_batida.py`  
  Código Python responsável pela análise de áudio e envio dos dados ao Arduino.

- `controle_motor.ino`  
  Sketch do Arduino responsável por receber os dados e acionar o motor.

- `requirements.txt`  
  Lista de dependências Python do projeto.

- `LICENSE`  
  Licença do projeto.

---

## Requisitos

### No computador
- Python **3.9+** (para usar o código) **OU** Windows 10+ (para usar o executável)
- Bibliotecas Python:
  - `numpy`
  - `soundcard`
  - `pyserial`
  - `scipy`

### No Arduino
- Placa compatível com Arduino
- Motor DC ou motor de vibração
- Circuito de acionamento adequado:
  - MOSFET ou transistor
  - diodo de proteção
  - fonte externa para o motor
  - GND comum entre Arduino e fonte

---

## Instalação

### Opção 1: Usar o código Python

#### 1. Clonar o repositório

```bash
git clone https://github.com/SEU_USUARIO_GITHUB/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
```

#### 2. Criar ambiente virtual opcional

```bash
python -m venv venv
```

#### 3. Ativar o ambiente virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

#### 4. Instalar as bibliotecas Python

```bash
pip install numpy soundcard pyserial scipy
```

#### 5. Ou usar `requirements.txt`

```bash
pip install -r requirements.txt
```

### Opção 2: Usar o executável (em breve)

Quando o executável estiver disponível:

1. Baixe o arquivo `.exe` da seção de [Releases](https://github.com/SEU_USUARIO_GITHUB/SEU_REPOSITORIO/releases)
2. Coloque em uma pasta de sua preferência
3. Clique duas vezes para executar
4. **Não há necessidade de instalar Python ou qualquer dependência**

---

## Como usar

### 1. Gravar o código no Arduino

- Abra o arquivo `controle_motor.ino` na Arduino IDE
- Selecione a placa correta
- Selecione a porta correta
- Faça o upload do sketch

### 2. Conectar o Arduino ao computador

- Conecte o Arduino via USB
- Feche o **Serial Monitor** da Arduino IDE, caso esteja aberto

### 3. Executar o script Python

#### Se estiver usando o **código Python**:

```bash
python detector_batida.py
```

#### Se estiver usando o **executável**:

- Clique duas vezes no arquivo `detector_batida.exe`
- A janela do programa abrirá automaticamente

### 4. Iniciar a reprodução de áudio

- Dê play em uma música no computador
- O script/executável vai analisar o áudio da saída padrão
- Quando uma batida for detectada, o Arduino receberá o valor e acionará o motor

---

## Ligação do motor

**Importante:** nunca ligue o motor diretamente ao pino do Arduino.

### Recomendado
- Pino PWM do Arduino → gate/base do transistor ou MOSFET
- Motor alimentado por fonte externa
- Diodo em paralelo com o motor para proteção
- GND comum entre Arduino e a fonte do motor

### Exemplo de pino usado
```cpp
const int pinoMotor = 3;
```

---

## Configurações importantes

### No Python
Você pode ajustar:

- `taxa_amostra`
- `janela`
- `cooldown_batida`
- `limiar_minimo`
- `fator_detecao_pico`
- faixa do filtro

### No Arduino
Você pode ajustar:

- `taxaDesaceleracao`
- `forcaMinimaMotor`
- faixa de mapeamento entre intensidade recebida e PWM

---

## Problemas comuns

### Arduino não é encontrado
- Verifique o cabo USB
- Verifique os drivers
- Feche o Serial Monitor
- Confirme se a porta correta está disponível

### Nenhum áudio é detectado
- Verifique se o dispositivo de saída de áudio está ativo
- Confirme se o loopback está disponível
- Teste com uma música tocando no sistema

### Motor não gira
- Verifique a ligação elétrica
- Confirme a alimentação externa do motor
- Verifique o transistor/MOSFET
- Verifique se o pino PWM está correto

### Muitas detecções falsas
- Aumente o limiar mínimo
- Aumente o cooldown
- Ajuste a faixa do filtro

### Resposta lenta
- Reduza a janela de captura no Python
- Reduza o cooldown
- Ajuste a desaceleração no Arduino

---

## Estrutura dos valores enviados

### Python envia
- `0` → nenhuma batida
- `150 a 600` → batida detectada com intensidade variável

### Arduino interpreta
- `150` → intensidade mínima útil
- `600` → intensidade máxima
- converte esse valor em saída PWM para o motor

---

## Melhorias futuras

- Detecção ainda mais precisa de batidas
- Ajuste automático de limiar
- Interface gráfica para calibração
- Salvamento de configurações em arquivo
- ✅ Exportação para executável `.exe` (em desenvolvimento)
- Suporte a mais tipos de motor e resposta tátil

---

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

Projeto desenvolvido para detecção de batidas musicais com controle de motor via Arduino.