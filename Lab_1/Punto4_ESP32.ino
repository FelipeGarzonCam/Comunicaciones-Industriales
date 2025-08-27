#include <Wire.h>

#define POT_PIN 36        
#define I2C_ADDRESS 0x08

int valorPotenciometro = 0;

void setup() {
  Serial.begin(115200);
  
  Wire.begin((uint8_t)I2C_ADDRESS);
  Wire.onRequest(enviarDatos);   
}

void loop() {
  // Leer directamente del ADC
  valorPotenciometro = analogRead(POT_PIN);
  
  Serial.print("ADC Raw: ");
  Serial.print(valorPotenciometro);
  Serial.print(" -> Mapeado: ");
  Serial.println(map(valorPotenciometro, 0, 4095, 0, 255));
  
  delay(500);
}

void enviarDatos() {
  byte valorMapeado = map(valorPotenciometro, 0, 4095, 0, 255);
  Wire.write(valorMapeado);
  Serial.print("Enviado I2C: ");
  Serial.println(valorMapeado);
}
