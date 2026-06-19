# Detector de Batidas com Arduino

Sistema que integra **Python + Arduino** pensado para jogos de ritmo. Captura o áudio do computador em tempo real, detecta batidas e aciona um motor físico via comunicação serial com resposta tátil rápida e precisa.

### ⭐ Sugestões de Jogos

Este projeto foi calibrado e otimizado para jogos de ritmo acelerados, onde a precisão do feedback tátil e o tempo de resposta fazem toda a diferença. Experimente testar a manopla com:

* **Friday Night Funkin' (FNF):** Excelente para testar a detecção de transientes rápidos e notas agudas nos vocais isolados dos personagens (como o Boyfriend).
* **Muse Dash:** Perfeito para testar o tempo de resposta (*cooldown*) do motor e o impacto seco nos graves a cada batida frenética.

---

## 📂 Estrutura do Projeto

```text
manopla-do-ritmo/
├── artefato/
│   └── controle_motor.ino    # Código do Arduino
├── .gitignore
├── main.py                   # Script Python principal
├── README.md
└── requirements.txt          # Dependências do Python
```

---

## 🛠️ Requisitos e Instalação (Python)

### 1. Dependências
Certifique-se de ter o Python 3.9+ instalado. Instale as bibliotecas necessárias rodando no terminal:

```bash
pip install -r requirements.txt
```

### 2. Executando o Script
Com o Arduino já conectado ao computador, inicie a captura rodando:

```bash
python main.py
```

O script identificará automaticamente a saída de áudio padrão do sistema e iniciará o envio de dados via Serial.

---

## 🔌 Hardware e Circuito

<center><small>Link para o Tinkercad...</small></center>
 <p align="center">
<a href="https://www.tinkercad.com/things/0RpFRD87ChT-vibration-motor">
  <img src="https://csg.us-east-1.prd.tinkercad.com/things/0RpFRD87ChT/t725.png?rev=1588776824634000000&s=&v=1&type=circuits" width="400" alt="Simulação do Circuito no Tinkercad">
</a>
</p>

### Lógica de Funcionamento
O circuito baseia-se no controle do motor via **PWM (Modulação por Largura de Pulso)**:

* **Controle de Potência:** O Arduino recebe a intensidade gerada pelo Python (100 a 255) e ajusta o pulso no pino PWM, variando a velocidade e a força do motor.
* **Fechamento (GND):** O terminal negativo do motor é ligado ao GND da placa, garantindo o retorno seguro da corrente.
* **Alimentação USB:** Todo o sistema (Arduino e motor) é energizado diretamente pelo cabo USB do computador, sem necessidade de fontes externas.

### Componentes Utilizados
* Placa compatível com Arduino (Ex: Uno, Nano)
* Motor de vibração
* Transistor/BC548 ou N2222A *(invertido)* para acionamento do motor
* Diodo de proteção (Ex: 1N4001)
* Protoboard e Jumpers

### ⭐ Código do Arduino

Dentro da pasta `artefato/`, você encontrará o arquivo **`controle_motor.ino`**, que contém toda a lógica de controle físico do motor. 

### Como Carregar via Arduino IDE:
1. Abra o software **Arduino IDE** em seu computador.
2. Vá em `Arquivo > Abrir` e selecione o arquivo `artefato/controle_motor.ino`.
3. Conecte a sua placa Arduino ao computador utilizando o cabo USB.
4. No menu superior da IDE, certifique-se de selecionar o modelo correto da sua placa (Ex: *Arduino Uno*, *Nano*, etc.) e a porta COM ativa.
5. Clique no botão **Carregar** (ícone de seta para a direita) para compilar e transferir o código para o hardware.

> ⚠️ **Importante:** Se você abrir o *Monitor Serial* da Arduino IDE para testar, lembre-se de **fechá-lo** antes de executar o script Python (`main.py`). Duas aplicações não podem usar a mesma porta Serial simultaneamente, e isso causará erro de conexão no Python.

<!-- ### Lógica de Ligação Elétrica
* **Pino PWM do Arduino:** Conectado à base/gate do componente de acionamento (transistor/MOSFET).
* **Alimentação do motor:** O motor é ligado diretamente ao Arduino, dispensando o uso de fonte externa.
* **GND Comum:** O GND do Arduino deve obrigatoriamente estar conectado ao GND da fonte externa. -->

---

## 🚀 Como Funciona o Sistema

1. **Captura e Filtro (Python):** O `main.py` captura o áudio tocado no sistema e aplica um filtro Passa-Faixa amplo (40Hz a 6000Hz) para escutar toda a faixa musical (dos graves profundos aos agudos secos). Ele calcula o ataque da batida baseando-se em picos reais de energia (RMS) com sensibilidade dinâmica.
2. **Envio de Dados:** Quando uma batida ou nota aguda do jogo ultrapassa o limiar, o Python envia o valor da intensidade mapeada via comunicação serial para a porta do Arduino.
3. **Atuação (Arduino):** O código `controle_motor.ino` lê a serial, converte o valor em sinal PWM e aciona o motor aplicando uma lógica de corte seco por tempo (ex: 40ms). Isso garante que o motor responda a notas rápidas sem embolar a vibração.

---

## ⚙️ Configurações Avançadas

Se você deseja customizar a sensibilidade ou o comportamento físico da manopla, pode alterar as seguintes variáveis diretamente no código:

* **No Python (`main.py`):**
  * `fator`: Multiplicador mestre (ex: `1.5`). Aumente para deixar a vibração geral mais intensa ou diminua para suavizar.
  * `cooldown_batida`: Tempo de espera entre os disparos (ex: `0.06s`). Ideal para ajustar o tempo de resposta em músicas frenéticas.
* **No Arduino (`controle_motor.ino`):**
  * `duracaoSoco`: Tempo em milissegundos (ex: `40`) que o motor fica ativo. Altere para tornar o feedback tátil mais seco ou mais arrastado.