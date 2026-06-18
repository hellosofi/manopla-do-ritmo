#include <Arduino.h>

int pinoMotor = 3;
int forcaAtualMotor = 0;   // Guarda a força real do motor naquele exato momento
int taxaDesaceleracao = 5; // Velocidade com que o motor "freia" (ajuste a gosto)

void setup() {
    pinMode(pinoMotor, OUTPUT);
    Serial.begin(115200);
    
    // Configuração extra: Evita que o Arduino trave muito tempo lendo a porta
    Serial.setTimeout(10); 
}

void loop() {
    if (Serial.available() > 0) {
        int intensidadeBatida = Serial.parseInt();
        
        // Limpa o "Enter" (\n) que o Python manda junto com o número
        while (Serial.available() > 0 && Serial.peek() == '\n') {
            Serial.read();
        }

        int forcaAlvo = 0;

        // O seu threshold original: só passa daqui se for uma batida real
        if (intensidadeBatida >= 150) {
            forcaAlvo = map(intensidadeBatida, 150, 600, 100, 255);
            forcaAlvo = constrain(forcaAlvo, 0, 255);
        }

        // ==========================================
        // 🧠 A MÁGICA DA SUAVIZAÇÃO
        // ==========================================
        if (forcaAlvo > forcaAtualMotor) {
            // "PAM!": Se a batida alvo for mais forte que o estado atual, 
            // a força sobe instantaneamente para dar o impacto da quebra.
            forcaAtualMotor = forcaAlvo;
        } else {
            // Queda Suave: Se o som abaixou ou silenciou, nós NÃO zeramos de vez.
            // O motor vai diminuindo a força gradativamente, criando o efeito de suavidade.
            forcaAtualMotor -= taxaDesaceleracao;
            
            // Trava para impedir que a energia passe do zero para o negativo
            if (forcaAtualMotor < 0) {
                forcaAtualMotor = 0;
            }
        }

        // Aciona o motor com o valor recém-calculado (sem trancos bruscos)
        analogWrite(pinoMotor, forcaAtualMotor);
    }
}