#include <Arduino.h>

// recebe dados do python
int intensidadeBatida= 0;

// // led rgb (futuro teste)
// const int red = 1;
// const int green = 2;
// const int blue = 3;

// led normal
int azul = 8;
int verde = 9;
int amarelo = 10;
int laranja = 11;
int vermelho = 12;

void setup() {
  Serial.begin(115200);

  // leds
  pinMode(azul, OUTPUT);
  pinMode(verde, OUTPUT);
  pinMode(amarelo, OUTPUT);
  pinMode(laranja, OUTPUT);
  pinMode(vermelho, OUTPUT);
}


void loop() {
  // Serial.available verifica a quantidade de bytes que estão sendo recebidos -> pela porta USB
  // se está passando alguma informação então é maior que 0 
  if (Serial.available() > 0){

    // aqui pega o número certo que está sendo passado pela porta serial
    // >> batida
    intensidadeBatida = Serial.parseInt();
    // ## Python ##
    // valores = map(intensidadeBatida, 0, 1023)
    // ## ###### ##

    // filtro de ruído:
    if (intensidadeBatida > 0){
      
      if (intensidadeBatida > 350){
        digitalWrite(azul, LOW);
        digitalWrite(verde, LOW);
        digitalWrite(amarelo, LOW);
        digitalWrite(laranja, LOW);
        digitalWrite(vermelho, HIGH);
      } else if (intensidadeBatida > 250){
        digitalWrite(azul, LOW);
        digitalWrite(verde, LOW);
        digitalWrite(amarelo, LOW);
        digitalWrite(laranja, HIGH);
        digitalWrite(vermelho, LOW);
      } else if (intensidadeBatida > 150){
        digitalWrite(azul, LOW);
        digitalWrite(verde, LOW);
        digitalWrite(amarelo, HIGH);
        digitalWrite(laranja, LOW);
        digitalWrite(vermelho, LOW);
      }else if (intensidadeBatida > 100) {
        digitalWrite(azul, LOW);
        digitalWrite(verde, HIGH);
        digitalWrite(amarelo, LOW);
        digitalWrite(laranja, LOW);
        digitalWrite(vermelho, LOW);      
      }else if (intensidadeBatida < 50) {
        digitalWrite(azul, HIGH);
        digitalWrite(verde, LOW);
        digitalWrite(amarelo, LOW);
        digitalWrite(laranja, LOW);
        digitalWrite(vermelho, LOW);
        }
        else{
        digitalWrite(azul, LOW);
        digitalWrite(verde, LOW);
        digitalWrite(amarelo, LOW);
        digitalWrite(laranja, LOW);
        digitalWrite(vermelho, LOW);
      }
    }


  }
}