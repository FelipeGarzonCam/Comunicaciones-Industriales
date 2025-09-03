# Taller 1 - Comunicaciones Industriales

## 1. Detectores de errores
Durante el taller se revisaron y describieron los principales métodos de detección de errores en comunicaciones digitales:  

- **Paridad:** sencillo de implementar, usado en transmisiones básicas ⚡.  
- **Checksum:** permite validar bloques de datos, muy útil en protocolos de red.  
- **CRC (Cyclic Redundancy Check):** el más robusto, ampliamente utilizado en entornos industriales (ej. Modbus, CAN).  
- **Código Hamming:** detecta y corrige errores de un bit.  
- **ARQ (Automatic Repeat reQuest):** asegura la retransmisión de tramas dañadas.  

✔️ Se comprendió que cada método tiene ventajas y limitaciones, siendo CRC y Hamming los más confiables en aplicaciones críticas.  

---

## 2. Tecnologías actuales basadas en RS232
Se exploraron patentes y aplicaciones modernas que mantienen vigente al estándar RS232 en la industria:  

1. **Conversores USB–RS232 (ejemplo: FT232R de FTDI).**  
   Facilitan la conexión de equipos industriales antiguos a PCs modernas.  

2. **Módulos RS232–Bluetooth.**  
   Permiten la comunicación inalámbrica con máquinas y dispositivos en mantenimiento remoto 📡.  

3. **Gateways RS232–IoT.**  
   Integran equipos clásicos con plataformas modernas de supervisión mediante protocolos como MQTT o Modbus TCP.  

👉 Con estas tecnologías se comprobó que RS232 sigue siendo útil cuando se combina con soluciones actuales.  

---

## 3. Raspberry Pi + Dashboards

### 📊 Grafana
En la Raspberry Pi se instaló **Grafana** y se conectó con una base de datos InfluxDB simulando registros de temperatura.  

- **Resultado obtenido:**  
  Un dashboard con un **gráfico de líneas en tiempo real** mostrando la evolución de la temperatura entre **23°C y 28°C**.  
  - Eje X: Tiempo (segundos)  
  - Eje Y: Temperatura (°C)  
  - Panel con título *“Temperatura del Sensor en Tiempo Real”*  

La interfaz permitió observar cómo variaban los datos a lo largo de la práctica.  

---

### 🌐 Streamlit
Se desarrolló una aplicación en Python con Streamlit para graficar datos simulados.  

- **Código usado:**
  ```python
  import streamlit as st
  import random

  st.title("Ejemplo sencillo con Streamlit")
  data = [random.randint(20, 30) for _ in range(10)]
  st.line_chart(data)
