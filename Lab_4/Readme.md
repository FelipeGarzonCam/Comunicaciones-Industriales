

# Punto 1 – Router, Switch, PC y Raspberry Pi

#### Luis Garzon C.
#### David Quinchanegua

## 1. Configuración de Equipos

### **Router Cisco 4321**

```

enable
configure terminal
interface GigabitEthernet0/0/0
description Conexion Switch VLAN1
ip address 192.168.1.1 255.255.255.0
no shutdown
exit
ip dhcp pool VLAN1
network 192.168.1.0 255.255.255.0
default-router 192.168.1.1
lease 7
exit
end

```

---

### **Switch Cisco WS-C2960**

```

enable
configure terminal
vlan 1
name VLAN1
exit
interface range FastEthernet0/1-24
switchport mode access
switchport access vlan 1
no shutdown
exit
end

```

---

### **PC y Raspberry Pi**

- Configuración de red: **DHCP automático** (por defecto en Windows y Raspberry Pi OS).
- Conectar ambos equipos a puertos del switch. Verifica IP obtenida vía DHCP con:
    - En PC (cmd): `ipconfig /all`
    - En Raspberry Pi (terminal): `ifconfig`

---

## 2. Evidencias y Pruebas

### 2.1 Ping entre PC y Raspberry Pi (conectividad)
- Verificar que ambos equipos se comunican correctamente.

<img width="572" height="267" alt="Ping pc a pi 3" src="https://github.com/user-attachments/assets/7d5942c9-cdfa-4fd3-94ac-e67025c76391" />


![Ping pi a pc](https://github.com/user-attachments/assets/59e07cfd-c7e3-463d-bad4-54ba164ad1b2)

---

### 2.2 Tabla ARP en el router y switch
- Confirmar que los dispositivos han aprendido las IP y MAC.

<img width="694" height="95" alt="show arp Router" src="https://github.com/user-attachments/assets/aa0a2172-1cc6-48c6-a4bd-762a2d7ee972" />

<img width="604" height="82" alt="show arp" src="https://github.com/user-attachments/assets/9ca243f3-7e91-4582-a30c-f85491af76b3" />

---

### 2.3 Estado de interfaces del switch
- Visualizar puertos conectados y su estado.
<img width="664" height="499" alt="show interface status" src="https://github.com/user-attachments/assets/305b2cd2-0159-421f-82f5-990cd4f17df9" />

---

### 2.4 Asignación DHCP en el router
- Comprobar que el router está entregando direcciones IP correctamente.

<img width="659" height="182" alt="show ip dhcp binding" src="https://github.com/user-attachments/assets/e0f8b287-db9f-4641-b2ec-dd803aec2c64" />

<img width="714" height="206" alt="show ip dhcp pool" src="https://github.com/user-attachments/assets/de7e2989-e4aa-47d6-a6c9-24a4e060bcab" />


---

### 2.5 Estado de interfaces en el router
- Verificar IP y status de interfaces.
  
<img width="735" height="160" alt="show ip interface brief" src="https://github.com/user-attachments/assets/0817edd1-c5cd-4d66-9e25-c786bb18536f" />



---

### 2.6 Tabla MAC del switch
- Validar qué dispositivos están conectados.
<img width="393" height="538" alt="show mac address-table" src="https://github.com/user-attachments/assets/3cc30f8f-2c5b-436b-bb29-b3d24e6b003b" />


---

### 2.7 Resumen de VLANs en el switch
- Mostrar que la configuración está limpia y estándar.
<img width="664" height="257" alt="show vlan brief" src="https://github.com/user-attachments/assets/de907ce4-79dd-491f-a553-2e82564b10a5" />

---

## 3. Comandos de Verificación

### **En el Switch**
```

show vlan brief
show mac address-table
show arp
show interface status

```

### **En el Router**
```

show ip dhcp binding
show ip dhcp pool
show arp
show ip interface brief

```

### **En PC y Raspberry**
```

ipconfig /all   # PC (Windows)
ip addr         # Raspberry Pi
arp -a          # Ambos equipos

```

---

## 4. Observaciones

- La topología está completamente basada en configuración automática por DHCP.
- Las asignaciones de IP y la tabla MAC/ARP se limpian tras reiniciar los equipos si no se guarda la configuración.
- Todas las pruebas corresponden a la evidencia de correcta integración y funcionamiento de la red de laboratorio.

---
---

# Punto 2: Comunicación RS485 Simplex y Full Duplex
Implementar y comparar comunicación RS485 en modos Simplex (unidireccional) y Full Duplex (bidireccional simultánea) entre Raspberry Pi como maestro y Raspberry Pi Pico como esclavo, analizando el rendimiento de cada modo y visualizando los datos en tiempo real.

## Arquitectura del Sistema

### Modo Simplex (Unidireccional)
Raspberry Pi (TX) → MAX485 → Bus RS485 → MAX485 → Raspberry Pi Pico (RX)

*Conexiones:**
- RPi TX (GPIO 14) → DI del MAX485 maestro
- DE/RE del MAX485 maestro → 3.3V (siempre en transmisión)
- Bus A/B conectado entre ambos MAX485
- RO del MAX485 esclavo → RX (GPIO 1) del Pico
- DE/RE del MAX485 esclavo → GND (siempre en recepción)
  
 ### Modo Full Duplex (Bidireccional)

Raspberry Pi ↔ Bus 1 ↔ Raspberry Pi Pico 1 (RX)
Raspberry Pi ↔ Bus 2 ↔ Raspberry Pi Pico 2 (TX)

### Comunicación Simplex

**Transmisión desde el Maestro:**

<img width="815" height="341" alt="Maestro simple" src="https://github.com/user-attachments/assets/67b255e4-fd2a-4aba-bec2-5d53708b113e" />


**Recepción en el Esclavo:**

<img width="411" height="325" alt="Esclavo simplex" src="https://github.com/user-attachments/assets/5c46e79a-177e-4a3a-9372-821092d7eee3" />

**Observaciones:**
- Se transmitieron 15 paquetes correctamente
- Todos los datos fueron recibidos sin errores
- Coincidencia exacta entre datos transmitidos y recibidos
- Tasa de error: 0%
- Data rate promedio: 2.8 bytes/s

 ---

### Comunicación Full Duplex

**Maestro (TX/RX simultáneos):**

<img width="1096" height="579" alt="maestro_full_duplex" src="https://github.com/user-attachments/assets/e0efe5b4-1a30-49cb-ba77-7461bb537d34" />

**Observaciones:**
- Transmisión y recepción funcionan simultáneamente
- Se detectaron 2 errores en 61 paquetes (tasa de error: 3.3%)
- Throughput bidireccional: 5.0 bytes/s (TX) + 5.0 bytes/s (RX)
- Mayor complejidad pero doble capacidad de comunicación

---

### Visualización en Streamlit

**Modo Simplex:**
<img width="1632" height="914" alt="Streamlit SImplex" src="https://github.com/user-attachments/assets/de1f2a90-75a1-4563-bb84-176afedf0aa5" />

**Modo Full Duplex:**
<img width="1627" height="761" alt="Streamlit Duplex" src="https://github.com/user-attachments/assets/66a02b0a-74ad-46ff-8f1f-0fe2fd89f79c" />

El dashboard permite observar en tiempo real los datos transmitidos (TX) en azul y los recibidos (RX) en rojo para el modo Full Duplex.

---

## Análisis Comparativo

| Característica | Simplex | Full Duplex |
|----------------|---------|-------------|
| Dirección | Unidireccional | Bidireccional |
| Buses requeridos | 1 | 2 |
| Complejidad | Baja | Media-Alta |
| Throughput total | ~2.8 bytes/s | ~10 bytes/s |
| Tasa de error | 0% | 3.3% |
| Uso de recursos | Bajo | Alto |

---
## Conclusiones

1. La comunicación Simplex es más confiable (0% de errores) pero limitada a transmisión unidireccional.

2. El modo Full Duplex permite comunicación bidireccional simultánea con mayor throughput total, aunque presenta una tasa de error ligeramente superior debido a la mayor complejidad.

3. RS485 es un protocolo robusto adecuado para comunicaciones industriales de mediana distancia.

4. La visualización en tiempo real mediante Streamlit facilita el monitoreo y análisis del comportamiento del sistema.

5. Para aplicaciones donde solo se requiere transmisión de datos en una dirección, el modo Simplex es más eficiente. Para sistemas que requieren intercambio bidireccional de información, el modo Full Duplex es la mejor opción a pesar de su mayor complejidad.

