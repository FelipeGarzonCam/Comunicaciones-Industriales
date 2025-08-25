# PUNTO 2🔌 Comunicación UART ESP32 ↔ Raspberry Pi Pico

## 📋 Descripción
Comunicación serial bidireccional entre ESP32 y Raspberry Pi Pico con LEDs de estado visual.

## ⚡ Conexiones

### UART

ESP32 ←→ Raspberry Pi Pico
GPIO17 (TX) ←→ GP1 (RX)
GPIO16 (RX) ←→ GP0 (TX)
GND ←→ GND


### LEDs (Raspberry Pi Pico)
GP2 → LED Verde + 220Ω → GND (Comunicación OK)
GP3 → LED Azul + 220Ω → GND (Sin Comunicación)

## 🚀 Funcionamiento

- **ESP32**: Envía mensajes cada 3 segundos
- **Pico**: Responde automáticamente y controla LEDs
- **Verde ON**: Comunicación activa ✅
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
![Salida de Consola](images/console_output.png)

### Demo LEDs
![Funcionamiento](images/led_demo.gif)

## 📊 Especificaciones
- **Protocolo**: UART 8N1
- **Baudrate**: 9600 bps
- **Voltaje**: 3.3V compatible
- **Timeout**: 8 segundos



# PUNTO 3🔌 Comunicación SPI entre ESP32 y Raspberry Pi Pico

[![ESP32](https://img.shields.io/badge/ESP32-Dev%20Module-red?style=flat&logo=espressif)](https://www.espressif.com/en/products/socs/esp32)
[![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-Pico-green?style=flat&logo=raspberry-pi)](https://www.raspberrypi.org/products/raspberry-pi-pico/)
[![Arduino](https://img.shields.io/badge/Arduino-IDE-blue?style=flat&logo=arduino)](https://www.arduino.cc/en/software)
[![MicroPython](https://img.shields.io/badge/MicroPython-v1.20-yellow?style=flat&logo=micropython)](https://micropython.org/)

## 📋 Descripción

Implementación de comunicación **SPI síncrona** entre ESP32 (esclavo) y Raspberry Pi Pico (maestro) para control remoto de LED. Proyecto del Laboratorio 1, Punto 3: SPI Sincrónico - Comunicaciones Industriales.

## ✨ Características

- 🎯 Comunicación SPI bidireccional a 100kHz
- 💡 Control remoto de LED desde Raspberry Pi Pico
- 🔄 Protocolo de comandos simple (0x01=ON, 0x00=OFF)
- 📡 Detección de errores con timeouts
- 🖥️ Monitoreo serial en tiempo real

## 🧰 Materiales

| Componente | Cantidad |
|------------|----------|
| ESP32 Dev Module | 1 |
| Raspberry Pi Pico | 1 |
| LED + Resistencia 220Ω | 1 |
| Protoboard | 1 |
| Cables Jumper | 8 |
| Cables USB | 2 |

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

## 🚀 Instalación

### ESP32 (Arduino IDE)
1. Instalar ESP32 en Arduino IDE
2. Cargar `spi_esclavo_esp32.ino`
3. Seleccionar "ESP32 Dev Module"
4. Subir código (115200 baud)

### Raspberry Pi Pico (Thonny)
1. Instalar Thonny IDE
2. Configurar MicroPython (Raspberry Pi Pico)
3. Cargar `spi_maestro_pico.py`
4. Ejecutar programa

## 🏃‍♂️ Ejecución

1. Conectar hardware según diagrama
2. Programar ESP32 primero
3. Programar Raspberry Pi Pico
4. Observar LED encender/apagar cada 2 segundos

## 📊 Resultado Esperado

## 🎬 Demostración

![SPI Communication Demo](./demo/spi_funcionamiento.gif)

*Comunicación SPI en tiempo real: LED controlado remotamente desde Raspberry Pi Pico*

