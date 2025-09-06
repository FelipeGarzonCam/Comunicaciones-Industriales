

# 📡 Taller: Detección de Errores, RS232 y Raspberry Pi

## 📖 Descripción del Proyecto

Este repositorio contiene el desarrollo completo del taller académico enfocado en **detección de errores en comunicaciones**, **tecnologías RS232** y **configuración de Raspberry Pi** para aplicaciones de monitoreo con **Grafana** y **Streamlit**. El proyecto está diseñado como recurso educativo para estudiantes de ingeniería en telecomunicaciones y sistemas embebidos.

## 🔍 Ítem 1: Detectores de Errores

### Tipos Principales de Detectores

#### 1. **Código de Paridad**

- **Función**: Detección de errores simples mediante bit adicional
- **Tipos**: Par, Impar, Marca, Espacio
- **Eficiencia**: Detecta errores de 1 bit (50% de efectividad)
- **Aplicación**: Comunicaciones seriales básicas


#### 2. **Suma de Comprobación (Checksum)**

- **Algoritmos**: Simple sum, Fletcher, Adler-32
- **Ventajas**: Implementación sencilla, bajo costo computacional
- **Limitaciones**: No detecta todos los errores de transposición
- **Uso**: Protocolos de red, verificación de archivos


#### 3. **CRC (Cyclic Redundancy Check)**

- **Polinomios estándar**: CRC-16, CRC-32, CRC-CCITT
- **Capacidades**: Detecta errores en ráfaga hasta el grado del polinomio
- **Eficiencia**: 99.99% de detección para errores aleatorios
- **Implementación**: Hardware y software


#### 4. **Códigos de Hamming**

- **Propósito**: Detección Y corrección de errores
- **Distancia mínima**: 3 (detecta 2 errores, corrige 1)
- **Redundancia**: log₂(n) bits para n bits de datos
- **Aplicaciones**: Memoria RAM ECC, almacenamiento crítico


#### 5. **Códigos Reed-Solomon**

- **Especialidad**: Corrección de errores en ráfaga
- **Aplicación**: CDs, DVDs, comunicaciones espaciales
- **Capacidad**: Corrige hasta t errores con 2t símbolos de redundancia


### Comparación de Eficiencia

| Método | Detección | Corrección | Overhead | Complejidad |
| :-- | :-- | :-- | :-- | :-- |
| Paridad | Limitada | No | 1 bit | Muy Baja |
| Checksum | Moderada | No | Variable | Baja |
| CRC | Alta | No | Variable | Media |
| Hamming | Alta | Limitada | log₂(n) | Media-Alta |
| Reed-Solomon | Muy Alta | Excelente | Alto | Alta |

## 📡 Ítem 2: Tecnologías RS232

### Características del Estándar RS232

**RS232** (Recommended Standard 232) es un estándar de comunicación serial punto a punto desarrollado en 1960 y actualizado hasta RS232-E en 1991.[^10]

#### Especificaciones Técnicas

- **Velocidad**: Hasta 20 kbps (115.2 kbps no estándar)
- **Distancia**: Máximo 15 metros
- **Niveles de voltaje**: ±3V a ±15V
- **Conectores**: DB25, DB9, RJ45 (variantes)
- **Modo**: Full-duplex, asíncrono


### Tres Tecnologías Actuales Basadas en RS232

#### 1. **Convertidores USB-RS232 Inteligentes**

- **Description**: Circuitos integrados que mantienen compatibilidad total con RS232 mientras permiten conexión USB
- **Ventajas**:
    - Plug-and-play en sistemas modernos
    - Aislamiento galvánico opcional
    - Soporte para múltiples sistemas operativos
- **Fabricantes líderes**: FTDI (FT232), Silicon Labs (CP210x), Prolific (PL2303)
- **Aplicaciones**: Programación de microcontroladores, equipos industriales legacy


#### 2. **Gateways IoT Ethernet-RS232**

- **Funcionalidad**: Dispositivos que encapsulan comunicación RS232 en protocolos TCP/IP
- **Características**:
    - Configuración web integrada
    - Soporte MQTT, HTTP, Modbus TCP
    - Alimentación PoE opcional
- **Beneficios**: Integración de equipos legacy a redes modernas sin modificación de firmware
- **Casos de uso**: Automatización industrial, monitoreo remoto, Industry 4.0


#### 3. **Servidores de Puerto Serial Virtual**

- **Concepto**: Software/hardware que virtualiza puertos RS232 accesibles por red
- **Implementaciones**:
    - **Hardware**: Dispositivos dedicados con múltiples puertos RS232
    - **Software**: Aplicaciones que crean puertos COM virtuales
- **Protocolos soportados**: RFC2217, Telnet, Raw TCP
- **Aplicaciones**: Laboratorios remotos, centros de datos, acceso concurrente a equipos


### Comparativa de Protocolos de Comunicación Serial

| Característica | RS232 | RS422 | RS485 |
| :-- | :-- | :-- | :-- |
| **Modo** | Punto a punto | Punto a punto | Multipunto |
| **Velocidad máx** | 20 kbps | 10 Mbps | 35 Mbps |
| **Distancia máx** | 15 m | 1200 m | 1200 m |
| **Nodos** | 2 | 2 | 32-256 |
| **Señalización** | Single-ended | Diferencial | Diferencial |
| **Aplicaciones** | Consolas, modems | Comunicaciones industriales | Redes industriales |

## 🖥️ Ítem 3: Raspberry Pi 3 Model B

### Especificaciones Técnicas

La **Raspberry Pi 3 Model B:** 

#### Hardware Principal

- **CPU**: Broadcom BCM2837 Quad-core ARM Cortex-A53 64-bit @ 1.2 GHz
- **RAM**: 1 GB LPDDR2 SDRAM
- **Almacenamiento**: Slot microSD (clase 10 recomendada, mínimo 8 GB)
- **GPU**: VideoCore IV 3D graphics


#### Conectividad

- **Ethernet**: Puerto 10/100 Mbps
- **Wi-Fi**: 802.11n wireless LAN integrada
- **Bluetooth**: 4.1 Low Energy (BLE)
- **USB**: 4 puertos USB 2.0
- **GPIO**: 40 pines (26 GPIO + alimentación + tierra)


#### Puertos de Salida

- **HDMI**: Full size, resolución hasta 1080p
- **Audio**: Jack 3.5mm estéreo + salida HDMI
- **Cámara**: Conector CSI para cámara oficial RPi
- **Display**: Conector DSI para pantalla táctil oficial


### Aplicaciones en el Laboratorio

#### Casos de Uso Académicos

1. **Servidor web local** para prácticas de programación
2. **Nodo IoT** para sensores ambientales
3. **Centro multimedia** para presentaciones
4. **Plataforma de desarrollo** para sistemas embebidos
5. **Gateway de comunicaciones** RS232/Ethernet


## 🛠️ Instalación y Configuración

### Prerrequisitos

- Raspberry Pi 3 Model B
- MicroSD Card (16 GB+ recomendada, Clase 10)
- Fuente de alimentación 5V/2.5A
- Cable HDMI y teclado/mouse USB
- Conexión a internet (Ethernet o Wi-Fi)


### 1. Instalación de Raspbian OS

```bash
# 1. Descargar Raspberry Pi Imager
wget https://downloads.raspberrypi.org/imager/imager_latest_amd64.deb
sudo dpkg -i imager_latest_amd64.deb

# 2. Escribir imagen a SD (usar GUI de Imager)
# Seleccionar Raspberry Pi OS (Legacy, 32-bit) para mejor compatibilidad
# Configurar SSH, usuario y Wi-Fi antes de escribir

# 3. Primer arranque y actualización
sudo apt update && sudo apt upgrade -y
sudo reboot
```


### 2. Configuración Inicial del Sistema

```bash
# Activar SSH y configurar interfaz
sudo systemctl enable ssh
sudo systemctl start ssh

# Configurar GPIO y interfaces
sudo raspi-config
# Seleccionar: Interface Options → SSH, SPI, I2C (Enable)
# Advanced Options → Memory Split → 128

# Instalar dependencias básicas
sudo apt install -y git curl wget vim htop
```


### 3. Instalación de Grafana

```bash
#!/bin/bash
# Script: install-grafana.sh

# Agregar repositorio oficial de Grafana
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee /etc/apt/sources.list.d/grafana.list

# Actualizar e instalar
sudo apt update
sudo apt install -y grafana

# Configurar servicio
sudo systemctl daemon-reload
sudo systemctl enable grafana-server
sudo systemctl start grafana-server

# Verificar estado
sudo systemctl status grafana-server

# Configurar firewall (opcional)
sudo ufw allow 3000
```


### 4. Configuración de Grafana

```bash
# Acceso web inicial
echo "Grafana disponible en: http://$(hostname -I | cut -d' ' -f1):3000"
echo "Usuario inicial: admin"
echo "Contraseña inicial: admin"

# Configuración de base de datos (SQLite por defecto)
sudo nano /etc/grafana/grafana.ini
# [database]
# type = sqlite3
# host = 127.0.0.1:3306
# name = grafana
# user = root
# password =

# Reiniciar servicio después de cambios
sudo systemctl restart grafana-server
```


### 5. Instalación de Streamlit

```bash
#!/bin/bash
# Script: setup-streamlit.sh

# Instalar Python pip si no está disponible
sudo apt install -y python3-pip python3-venv

# Crear entorno virtual
python3 -m venv streamlit-env
source streamlit-env/bin/activate

# Actualizar pip
pip install --upgrade pip

# Instalar Streamlit y dependencias
pip install streamlit pandas numpy matplotlib plotly

# Verificar instalación
streamlit --version
```




### 6. Ejecución de la Aplicación

```bash
# Activar entorno virtual
source streamlit-env/bin/activate

# Ejecutar aplicación Streamlit
streamlit run src/examples/streamlit-demo.py --server.port 8501 --server.address 0.0.0.0

# La aplicación estará disponible en:
# http://IP_RASPBERRY:8501
```


### 7. Integración Grafana-Streamlit

```bash
# Configurar reverse proxy con nginx (opcional)
sudo apt install -y nginx

# Configuración básica nginx
sudo nano /etc/nginx/sites-available/dashboard

# server {
#     listen 80;
#     server_name raspberry-dashboard.local;
#     
#     location /grafana/ {
#         proxy_pass http://localhost:3000/;
#     }
#     
#     location /streamlit/ {
#         proxy_pass http://localhost:8501/;
#     }
# }
```

### Configuración de Data Sources en Grafana

```bash
# Para datos locales, instalar InfluxDB
sudo apt install -y influxdb influxdb-client
sudo systemctl enable influxdb
sudo systemctl start influxdb

# Crear base de datos
influx
> CREATE DATABASE raspberry_sensors
> exit
```


### Monitoreo del Sistema

```bash
# Verificar servicios activos
sudo systemctl status grafana-server
sudo systemctl status nginx
ps aux | grep streamlit

# Verificar puertos abiertos
sudo netstat -tlnp | grep -E ':(3000|8501|80)'

# Logs de Grafana
sudo journalctl -u grafana-server -f
```


