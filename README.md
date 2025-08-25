# PUNTO 2🔌 Comunicación UART ESP32 ↔ Raspberry Pi Pico
[![ESP32](https://img.shields.io/badge/ESP32-Dev%20Module-red?style=flat&logo=espressif)](https://www.espressif.com/en/products/socs/esp32)
[![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-Pico-green?style=flat&logo=raspberry-pi)](https://www.raspberrypi.org/products/raspberry-pi-pico/)
[![Arduino](https://img.shields.io/badge/Arduino-IDE-blue?style=flat&logo=arduino)](https://www.arduino.cc/en/software)
[![MicroPython](https://img.shields.io/badge/MicroPython-v1.20-yellow?style=flat&logo=micropython)](https://micropython.org/)
## 📋 Descripción
Comunicación serial bidireccional entre ESP32 y Raspberry Pi Pico con LEDs de estado visual.

## ⚡ Conexiones

### UART

| Raspberry Pi Pico | ESP32 | 
|------------------|--------|
| **GPIO1 (Rx)** | **GPIO17 (TX)** | 
| **GP0 (TX)** | **GPIO16 (RX)** |
| **GND** | **GND** | GND |


### LEDs (Raspberry Pi Pico)
GP2 → LED Azul + 220Ω → GND (Comunicación OK)
GP3 → LED Azul + 220Ω → GND (Sin Comunicación)

## 🚀 Funcionamiento

- **ESP32**: Envía mensajes cada 3 segundos
- **Pico**: Responde automáticamente y controla LEDs
- **Azul ON**: Comunicación activa ✅
- **Rojo ON**: Sin comunicación ❌
- **Timeout**: 8 segundos

## 💻 Configuración

**ESP32 (Arduino IDE):**
- UART: 9600 baudios
- Monitor: 115200

**Pico (Thonny):**  
- UART: 9600 baudios
- MicroPython

## 📺 Capturas

### Consola
![Salida de Consola](<img width="2216" height="2405" alt="pruebas" src="https://github.com/user-attachments/assets/bacfdb74-eab5-429d-a98b-018d78f8da69" />
)

### LEDs
![Funcionamiento](![Punto2](https://github.com/user-attachments/assets/9c63f598-a797-4902-98b7-cf035351350c)
)

## 📊 Especificaciones
- **Protocolo**: UART 8N1
- **Baudrate**: 9600 bps
- **Voltaje**: 3.3V compatible
- **Timeout**: 8 segundos



# PUNTO 3🔌 Comunicación SPI entre ESP32 y Raspberry Pi Pico

## 📋 Descripción

Implementación de comunicación **SPI síncrona** entre ESP32 (esclavo) y Raspberry Pi Pico (maestro) para control remoto de LED. Proyecto del Laboratorio 1, Punto 3: SPI Sincrónico - Comunicaciones Industriales.

## ✨ Características

- 🎯 Comunicación SPI bidireccional a 100kHz
- 💡 Control remoto de LED desde Raspberry Pi Pico
- 🔄 Protocolo de comandos simple (0x01=ON, 0x00=OFF)
- 📡 Detección de errores con timeouts
- 🖥️ Monitoreo serial en tiempo real

## 🔌 Conexiones

| Raspberry Pi Pico | ESP32 | Señal |
|------------------|--------|-------|
| **GPIO 17** | **GPIO 5** | CS |
| **GPIO 18** | **GPIO 18** | SCK |
| **GPIO 19** | **GPIO 23** | MOSI |
| **GPIO 16** | **GPIO 19** | MISO |
| **GND** | **GND** | GND |

### LED en ESP32

GPIO 2 → Resistencia 220Ω → LED(+)
GND → LED(-)



## 🎬 Demostración

![SPI](![Punto2 gif](https://github.com/user-attachments/assets/c8a9939a-a87a-4952-a82e-f0be97dc9d7a)
)

*Comunicación SPI en tiempo real: LED controlado remotamente desde Raspberry Pi Pico*

