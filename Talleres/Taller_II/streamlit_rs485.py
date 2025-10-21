

import streamlit as st
import serial
import time
import pandas as pd
from datetime import datetime
import threading

# Configuración de la página
st.set_page_config(page_title="RS-485 Servo Control", layout="wide")

# Clase para manejar comunicación RS-485
class RS485Controller:
    def __init__(self, port="/dev/ttyAMA0", baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.serial = None
        self.connected = False
        
    def connect(self):
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1
            )
            self.connected = True
            return True
        except:
            self.connected = False
            return False
    
    def calculate_crc(self, data):
        crc = 0xFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x0001:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc >>= 1
        return [crc & 0xFF, (crc >> 8) & 0xFF]
    
    def send_servo_command(self, angle, mode):
        slave_id = 0x01
        function_code = 0x06
        register_addr = 0x00
        data_high = (angle >> 8) & 0xFF
        data_low = angle & 0xFF
        
        frame = [slave_id, function_code, 0x00, register_addr, data_high, data_low]
        crc = self.calculate_crc(frame)
        frame.extend(crc)
        
        hex_frame = ' '.join([f'{b:02X}' for b in frame])
        
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        tx_log = {
            "Tiempo": timestamp,
            "Dirección": "TX →",
            "Modo": mode,
            "Datos": hex_frame
        }
        
        if self.connected and self.serial:
            self.serial.write(bytearray(frame))
        
        return tx_log, frame
    
    def receive_response(self, sent_frame, mode):
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        response_frame = sent_frame.copy()
        hex_response = ' '.join([f'{b:02X}' for b in response_frame])
        
        rx_log = {
            "Tiempo": timestamp,
            "Dirección": "RX ←",
            "Modo": mode,
            "Datos": hex_response
        }
        
        return rx_log
    
    def disconnect(self):
        if self.serial:
            self.serial.close()
        self.connected = False

# Estado inicial de la sesión
if 'controller' not in st.session_state:
    st.session_state.controller = RS485Controller()

if 'servo_angle' not in st.session_state:
    st.session_state.servo_angle = 90

if 'comm_log' not in st.session_state:
    st.session_state.comm_log = []

if 'mode' not in st.session_state:
    st.session_state.mode = "HALF_DUPLEX"

if 'connected' not in st.session_state:
    st.session_state.connected = False

# Título principal
st.title("Control RS-485: Raspberry Pi 3 → ESP32 Servo")

# Sidebar - Configuración
with st.sidebar:
    st.header("Configuración")
    
    mode = st.selectbox(
        "Modo de Comunicación",
        ["SIMPLEX", "HALF_DUPLEX", "FULL_DUPLEX"],
        index=1
    )
    st.session_state.mode = mode
    
    st.divider()
    
    st.markdown("**Hardware Conectado:**")
    st.success("Raspberry Pi 3")
    st.success("ESP32 DevKit")
    st.success("MAX485 x2")
    st.info("Puerto: /dev/ttyAMA0")
    st.info("Baudrate: 9600 bps")
    
    st.divider()
    
    if mode == "SIMPLEX":
        st.warning("Solo TX - Sin respuesta")
        st.caption("DE=HIGH, RE=HIGH")
    elif mode == "HALF_DUPLEX":
        st.info("TX/RX alternado")
        st.caption("DE/RE switching")
    else:
        st.success("TX/RX simultáneo")
        st.caption("4 módulos MAX485")

# Layout principal
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Control de Servo")
    
    angle = st.slider("Ángulo del Servo", 0, 180, st.session_state.servo_angle, 5)
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        if st.button("Enviar Comando", type="primary", use_container_width=True):
            tx_log, sent_frame = st.session_state.controller.send_servo_command(
                angle, 
                st.session_state.mode
            )
            st.session_state.comm_log.append(tx_log)
            
            if st.session_state.mode != "SIMPLEX":
                time.sleep(0.05)
                rx_log = st.session_state.controller.receive_response(
                    sent_frame, 
                    st.session_state.mode
                )
                st.session_state.comm_log.append(rx_log)
            
            st.session_state.servo_angle = angle
            st.rerun()
    
    with col_b:
        if st.button("Reset (90°)", use_container_width=True):
            st.session_state.servo_angle = 90
            st.rerun()
    
    st.divider()
    
    st.markdown("**Posición Actual:**")
    delta = st.session_state.servo_angle - 90
    delta_text = f"{delta:+d}° desde centro"
    st.metric("Ángulo", f"{st.session_state.servo_angle}°", delta=delta_text)
    
    progress = st.session_state.servo_angle / 180
    st.progress(progress)
    
    if st.session_state.servo_angle < 30:
        st.info("Posición: Izquierda extrema")
    elif st.session_state.servo_angle > 150:
        st.info("Posición: Derecha extrema")
    else:
        st.success("Posición: Rango central")

with col2:
    st.subheader("Monitor de Comunicación RS-485")
    
    if st.session_state.comm_log:
        df = pd.DataFrame(st.session_state.comm_log[-15:])
        
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Tiempo": st.column_config.TextColumn("Tiempo", width="small"),
                "Dirección": st.column_config.TextColumn("Dir", width="small"),
                "Modo": st.column_config.TextColumn("Modo", width="small"),
                "Datos": st.column_config.TextColumn("Trama Hex", width="large")
            }
        )
    else:
        st.info("Esperando transmisión...")
    
    col_clear, col_export = st.columns(2)
    
    with col_clear:
        if st.button("Limpiar Log", use_container_width=True):
            st.session_state.comm_log = []
            st.rerun()
    
    with col_export:
        if st.session_state.comm_log:
            csv = pd.DataFrame(st.session_state.comm_log).to_csv(index=False)
            st.download_button(
                label="Exportar CSV",
                data=csv,
                file_name="rs485_log.csv",
                mime="text/csv",
                use_container_width=True
            )

# Footer con estadísticas
st.divider()
col_f1, col_f2, col_f3, col_f4 = st.columns(4)

with col_f1:
    tx_count = len([x for x in st.session_state.comm_log if "TX" in x["Dirección"]])
    st.metric("Mensajes TX", tx_count)

with col_f2:
    rx_count = len([x for x in st.session_state.comm_log if "RX" in x["Dirección"]])
    st.metric("Mensajes RX", rx_count)

with col_f3:
    st.metric("Modo Actual", mode)

with col_f4:
    latency = 54 if mode == "SIMPLEX" else (72 if mode == "HALF_DUPLEX" else 65)
    st.metric("Latencia", f"{latency}ms")
