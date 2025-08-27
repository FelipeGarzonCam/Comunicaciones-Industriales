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

## 🎬 Demostración

### Consola
<img width="2216" height="1594" alt="pruebas" src="https://github.com/user-attachments/assets/b4d889ca-1a1d-436a-9d3c-a9d88ba8f751" />

### LEDs
![Punto2](https://github.com/user-attachments/assets/bc288129-3394-48a3-95bb-c6b21b500605)


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


# PUNTO 4📡 Comunicación I2C entre ESP32 y Raspberry Pi Pico

## 📋 Descripción

Sistema de comunicación **I2C** donde la **Raspberry Pi Pico** (maestro) lee valores de un potenciómetro conectado al **ESP32** (esclavo) y los visualiza mediante 3 LEDs en representación binaria. Proyecto del Laboratorio 1, Punto 4: I2C con Múltiples Dispositivos - Comunicaciones Industriales.

## ✨ Funcionamiento

1. **ESP32** lee continuamente un potenciómetro (0-4095) via **ADC**
2. **Mapea** el valor a rango de 1 byte (0-255)  
3. **Raspberry Pi Pico** solicita datos via **I2C** cada 500ms
4. **3 LEDs** muestran los **3 bits más significativos** del valor:
   - `000` = Potenciómetro 0-31 (LEDs apagados)
   - `001` = Potenciómetro 32-63 (LED1 encendido)
   - `111` = Potenciómetro 224-255 (todos encendidos)


## 🔌 Conexiones

### Bus I2C
| Raspberry Pi Pico | ESP32 | Función |
|------------------|--------|---------|
| **GPIO 4 (SDA)** | **GPIO 21 (SDA)** | 📡 Datos I2C |
| **GPIO 5 (SCL)** | **GPIO 22 (SCL)** | ⏰ Reloj I2C |
| **GND** | **GND** | ⚡ Tierra común |

### Potenciómetro (ESP32)
| Terminal | Conexión |
|----------|----------|
| **Terminal A** | **3.3V** |
| **Terminal Central** | **GPIO 36** (ADC1_CH0) |
| **Terminal B** | **GND** |

### LEDs (Raspberry Pi Pico)
| LED | GPIO | Conexión |
|-----|------|----------|
| **LED 1 (Bit 0)** | **GPIO 16** | 220Ω → LED → GND |
| **LED 2 (Bit 1)** | **GPIO 17** | 220Ω → LED → GND |
| **LED 3 (Bit 2)** | **GPIO 18** | 220Ω → LED → GND |

## 🎯 Configuración

- **Velocidad I2C:** 100kHz
- **Dirección Esclavo:** 0x08
- **Resolución ADC:** 12 bits (0-4095)
- **Frecuencia de lectura:** 500ms
- **Mapeo:** ADC → 8 bits (0-255)
- 
## 🎬 Demostración
![punto4](https://github.com/user-attachments/assets/20a26ce9-6309-42ca-8c40-f22c67a10868)



