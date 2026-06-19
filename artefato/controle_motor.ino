const int pinoMotor = 3;
int forcaAtual = 0;
unsigned long tempoInicioBatida = 0;
const unsigned long duracaoSoco = 40; // Tempo máximo de soco (40ms) para a nota ficar seca

void setup() {
  pinMode(pinoMotor, OUTPUT);
  Serial.begin(115200);
}

void loop() {
  // 1. RECEBE O COMANDO DO PYTHON
  if (Serial.available() > 0) {
    int comandoRecebido = Serial.parseInt();
    
    while (Serial.available() > 0 && (Serial.peek() == '\n' || Serial.peek() == '\r')) {
      Serial.read();
    }

   
    if (comandoRecebido >= 100) {
      forcaAtual = comandoRecebido; 
      tempoInicioBatida = millis(); 
    }
  }

  // 2. CONTROLE DEFINIDO DA VIBRAÇÃO
  if (forcaAtual > 0) {
    
    if (millis() - tempoInicioBatida > duracaoSoco) {
      forcaAtual = 0;
      analogWrite(pinoMotor, 0);
    } else {
      analogWrite(pinoMotor, forcaAtual);
    }
  } else {
    analogWrite(pinoMotor, 0);
  }
}