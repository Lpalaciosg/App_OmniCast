import streamlit as st
import pandas as pd
import sqlite3
from datetime import date, timedelta
import urllib.parse

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="OmniCast PRO | Gestión de Streaming", page_icon="🚀", layout="wide")

# 2. ESTILOS CSS PERSONALIZADOS (Tarjetas modernas y diseño vivo)
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, rgba(30,35,45,0.9), rgba(20,24,32,0.9));
        border-left: 5px solid #E50914;
        padding: 18px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        color: white;
        margin-bottom: 12px;
    }
    .metric-title {
        font-size: 13px;
        color: #A0AAB8;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 600;
    }
    .metric-value {
        font-size: 26px;
        font-weight: 800;
        margin-top: 6px;
        color: #FFFFFF;
    }
    .card-green { border-left-color: #10B981 !important; }
    .card-blue { border-left-color: #3B82F6 !important; }
    .card-yellow { border-left-color: #F59E0B !important; }
    .card-purple { border-left-color: #8B5CF6 !important; }
</style>
""", unsafe_allow_html=True)

# 3. BASE DE DATOS (Tablas sincronizadas para Ventas y Cuentas Madre)
conn = sqlite3.connect('omnicast_pro.db', check_same_thread=False)
c = conn.cursor()

# Tabla de Ventas / Clientes
c.execute('''CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente TEXT,
    whatsapp TEXT,
    plataforma TEXT,
    correo_cuenta TEXT,
    clave_acceso TEXT,
    perfil TEXT,
    pin TEXT,
    dispositivo TEXT,
    fecha_venta DATE,
    fecha_vencimiento DATE,
    precio_venta REAL,
    costo_prop REAL,
    metodo_pago TEXT,
    notas_2fa TEXT
)''')

# Tabla de Inventario de Cuentas Madre
c.execute('''CREATE TABLE IF NOT EXISTS cuentas_madre (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plataforma TEXT,
    correo_madre TEXT UNIQUE,
    clave_actual TEXT,
    proveedor TEXT,
    fecha_corte DATE,
    capacidad_cupos INTEGER,
    costo_madre REAL,
    notas_recuperacion TEXT
)''')
conn.commit()

# 4. FUNCIONES DE CÁLCULO Y PROCESAMIENTO (Error de página 3 corregido)
def cargar_ventas():
    df = pd.read_sql_query("SELECT * FROM ventas", conn)
    if not df.empty:
        hoy = pd.to_datetime(date.today())
        df['fecha_vencimiento_dt'] = pd.to_datetime(df['fecha_vencimiento'])
        # Cálculo seguro de días restantes sin error de atributo
        df['dias_restantes'] = (df['fecha_vencimiento_dt'] - hoy).dt.days
        df['ganancia_neta'] = df['precio_venta'] - df['costo_prop']
        
        def semaforo(dias):
            if dias < 0:
                return f"🔴 VENCIDO ({dias}d)"
            elif dias <= 5:
                return f"🟡 POR VENCER ({dias}d)"
            else:
                return f"🟢 ACTIVO ({dias}d)"
        
        df['alerta'] = df['dias_restantes'].apply(semaforo)
        df = df.sort_values(by
