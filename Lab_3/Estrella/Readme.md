# Punto 2: Desarrollo de diferentes conexiones topologicas de red

## Conexion en estrella

Se implementó una red en topología estrella utilizando un smartphone Motorola Edge 50 Fusion como Access Point central. Todos los dispositivos cliente se conectan directamente al AP mediante WiFi 802.11n (2.4 GHz).

<img width="1452" height="1080" alt="Diagrama Conexion" src="https://github.com/user-attachments/assets/11db0570-2c62-451b-a4bd-e8248b7360a1" />


**Características de la red:**
- **SSID:** Edge50FusiondeFelipe
- **Seguridad:** WPA2-PSK
- **Red:** 10.102.14.0/24
- **Gateway:** 10.102.14.150 (Smartphone AP)
- **Asignación IP:** DHCP automático

### Dispositivos Conectados

### Dispositivos Conectados

| Dispositivo | IP Asignada | Dirección MAC | Sistema Operativo |
|-------------|-------------|---------------|-------------------|
| DESKTOP- (Portatil) | 10.102.14.15 | C8:F7:33:0C:B8:59 | Windows 11 |
| Redmi-Pad-2 | 10.102.14.1 | 3E:62:6C:42:5E:54 | Android  |
| esp32-DDCAE0 | 10.102.14.79 | 78:E3:6D:DD:CA:E0 | ESP-IDF |
| OPPO-Reno10-5G | 10.102.14.168 | 5A:08:9A:0F:73:2A | Android  |
| Edge 50 Fusion (AP) | 10.102.14.150 | XX:XX:XX:XX:XX:XX | Android |

<img width="1080" height="2400" alt="Pantallazo AP" src="https://github.com/user-attachments/assets/287011d6-6523-4640-b9f2-e0e7bdfdc2d1" />



## 2.2 Pruebas de Conectividad

Se realizaron pruebas ICMP (ping) desde todos los dispositivos para verificar conectividad. En dispositivos Android se utilizó **Termux** como emulador de terminal.


![Tablet](https://github.com/user-attachments/assets/5f431a00-725a-450c-b20f-62a48a894397)


### Sistema Implementado

Se programó un ESP32 (IP: **10.102.14.79**) para controlar remotamente su LED integrado (GPIO 2) mediante:
- **Servidor Web HTTP** (puerto 80)
- **Monitor Serial** (Arduino IDE)
- **Funcionalidad Ping** incorporada

<img width="977" height="585" alt="ESP32" src="https://github.com/user-attachments/assets/21f6bb43-ce10-4b42-9f51-9344e80e5417" />


*Control vía Wifi:**
- `http://10.102.14.79/on` → Enciende LED

![On](https://github.com/user-attachments/assets/bbf50e5e-6fd5-4740-bf49-8c1f6f8db3e0)


- `http://10.102.14.79/off` → Apaga LED

![OFF](https://github.com/user-attachments/assets/1897fe28-bf89-41cb-8806-7fbc876b440d)
