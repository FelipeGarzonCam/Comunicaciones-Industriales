## Conexión en Anillo (Token Ring)

### Descripción

Se implementó una topología en anillo con protocolo **Token Ring (IEEE 802.5)** utilizando comunicación UART serial entre 5 dispositivos: ESP32, 2 Raspberry Pi Pico (H y W), y 2 Arduino UNO. El token circula unidireccionalmente garantizando acceso ordenado sin colisiones.

<img width="1252" height="978" alt="Topologia" src="https://github.com/user-attachments/assets/c47ad6c8-0240-42f6-ad6a-77dc22ca3bae" />

**Arquitectura:**
- 5 nodos conectados en anillo cerrado UART
- Protocolo: Token Passing (paso de testigo)
- Velocidad: 9600 baud (Arduinos/Picos), 115200 baud (ESP32)
- Dirección: Unidireccional (horaria)

**Conexiones físicas:**
ESP32 (TX2/RX2) → Pi Pico H (TX/RX) → Pi Pico W (TX/RX) → Arduino1 (TX/RX) → Arduino2 (TX/RX) → ESP32

### Concepto de Token

El **token** es un paquete especial de 5 bytes `[0xAA][ID_high][ID_low][Seq][Checksum]` que circula continuamente. Solo quien lo posee puede transmitir:
- Acceso controlado
- 0% colisiones garantizado
- Orden determinístico
-  Recuperación ante fallas (ESP32 como monitor)

### Implementación por Dispositivo

**Node-1: ESP32** (Nodo_1.ino)
- Monitor del anillo (maestro)
- Regenera token si se pierde
- UART2 (GPIO16/17)
  
<img width="475" height="419" alt="Esp32 nodo 1" src="https://github.com/user-attachments/assets/bf0c88d4-108f-41a3-a9ca-70262094c337" />

**Node-2: Raspberry Pi Pico H** (Nodo_2.py)
- MicroPython en Thonny
- UART0 (GP0/GP1)
  
<img width="465" height="689" alt="Nodo 2" src="https://github.com/user-attachments/assets/2eaa1916-075e-4499-a313-9a9cb4b6a169" />

**Node-3: Raspberry Pi Pico W** (Nodo_3.py)
- MicroPython en Thonny
- UART0 (GP0/GP1)
  
<img width="423" height="693" alt="nodo 3" src="https://github.com/user-attachments/assets/e7b74c7b-ff22-46d0-a3ef-2bf8078dc36b" />

**Node-4: Arduino UNO 1** (Nodo_4.ino)
- Arduino IDE
- Serial Hardware (Pin 0/1)

<img width="536" height="427" alt="Arduino nodo 4" src="https://github.com/user-attachments/assets/13270592-6538-412b-98aa-dacaa26a5490" />

**Node-5: Arduino UNO 2** (Nodo_5.ino)
- Arduino IDE
- Serial Hardware (Pin 0/1)
- Cierra el anillo al ESP32
- 
<img width="383" height="321" alt="Arduino nodo 5" src="https://github.com/user-attachments/assets/342c194a-7761-4e39-a965-c8d556fd8fc8" />

### Protocolo Implementado

**Estructura del Token:**
| Byte | Campo | Descripción |
|------|-------|-------------|
| 0 | Header | 0xAA (identificador) |
| 1-2 | Token ID | ID incremental del token |
| 3 | Secuencia | Número de ronda |
| 4 | Checksum | Validación de integridad |

**Flujo de Operación:**
1. Nodo espera recibir token por UART
2. Valida header y checksum
3. Procesa token (100-120 ms)
4. Incrementa ID y secuencia
5. Envía token al siguiente nodo
6. Repite ciclo

