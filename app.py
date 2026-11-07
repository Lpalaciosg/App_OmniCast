import streamlit as st
import pandas as pd
import sqlite3
from datetime import date
import urllib.parse

# Configuración de página
st.set_page_config(page_title="Gestión OmniCast V2", page_icon="📺", layout="wide")

# Conexión a Base de Datos (SQLite para pruebas, migrable a Supabase para producción)
conn = sqlite3.connect('clientes_streaming_v2.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS clientes 
             (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, telefono TEXT, 
             servicio TEXT, plan TEXT, fecha_pago DATE, estado TEXT, 
             correo TEXT, contrasena TEXT, pin TEXT)''')
conn.commit()

# Funciones de base de datos
def obtener_clientes():
    return pd.read_sql_query("SELECT * FROM clientes ORDER BY fecha_pago ASC", conn)

def actualizar_cliente(id, nombre, telefono, servicio, plan, fecha_pago, estado, correo, contrasena, pin):
    c.execute('''UPDATE clientes SET nombre=?, telefono=?, servicio=?, plan=?, 
                 fecha_pago=?, estado=?, correo=?, contrasena=?, pin=? WHERE id=?''', 
              (nombre, telefono, servicio, plan, fecha_pago, estado, correo, contrasena, pin, id))
    conn.commit()

def eliminar_cliente(id):
    c.execute("DELETE FROM clientes WHERE id=?", (id,))
    conn.commit()

# Menú lateral
st.sidebar.title("📺 OmniCast Panel")
opcion = st.sidebar.radio("Navegación", ["Inicio", "Registrar Nuevo", "Control de Pagos", "Gestión y Claves"])

# --- PÁGINA 1: INICIO ---
if opcion == "Inicio":
    st.title("Bienvenido a OmniCast")
    st.write("Sistema de control de suscripciones y accesos.")
    df = obtener_clientes()
    if not df.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Clientes Registrados", len(df))
        col2.metric("Suscripciones Activas", len(df[df['estado'] == 'Activo']))
        col3.metric("Por Vencer (≤ 3 días)", len(df[pd.to_datetime(df['fecha_pago']).dt.date <= date.today() + pd.Timedelta(days=3)]))

# --- PÁGINA 2: REGISTRAR ---
elif opcion == "Registrar Nuevo":
    st.title("➕ Registrar Venta/Cliente")
    with st.form("registro_form"):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre del Cliente")
            telefono = st.text_input("WhatsApp (Ej: 51987654321)")
            servicio = st.selectbox("Servicio", ["Netflix", "Disney+", "Prime Video", "HBO Max", "Crunchyroll", "Spotify"])
            plan = st.selectbox("Plan/Perfil", ["1 Pantalla", "2 Pantallas", "Cuenta Completa", "Plan Anual"])
            fecha_pago = st.date_input("Fecha de Vencimiento")
            estado = st.selectbox("Estado", ["Activo", "Vencido", "Suspendido"])
        with col2:
            st.markdown("### Datos de Acceso de la Cuenta")
            correo = st.text_input("Correo de la Cuenta")
            contrasena = st.text_input("Contraseña")
            pin = st.text_input("PIN del Perfil (Opcional)")
        
        if st.form_submit_button("Guardar Cliente"):
            if nombre and telefono:
                c.execute('''INSERT INTO clientes (nombre, telefono, servicio, plan, fecha_pago, estado, correo, contrasena, pin) 
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                          (nombre, telefono, servicio, plan, fecha_pago, estado, correo, contrasena, pin))
                conn.commit()
                st.success(f"Registrado exitosamente: {nombre} ({servicio})")
            else:
                st.error("Nombre y WhatsApp son obligatorios.")

# --- PÁGINA 3: CONTROL DE PAGOS Y DÍAS ---
elif opcion == "Control de Pagos":
    st.title("📅 Vencimientos y Avisos")
    df = obtener_clientes()
    
    if not df.empty:
        # Calcular días restantes
        hoy = date.today()
        df['fecha_pago'] = pd.to_datetime(df['fecha_pago']).dt.date
        df['Dias Restantes'] = (df['fecha_pago'] - hoy).dt.days
        
        # Formatear la columna de días para que sea más legible
        df['Estado Tiempo'] = df['Dias Restantes'].apply(
            lambda x: "🚨 Vencido" if x < 0 else ("⚠️ Vence Hoy" if x == 0 else f"Faltan {x} días")
        )
        
        # Enlaces de WhatsApp
        enlaces = []
        for index, row in df.iterrows():
            msg = f"Hola {row['nombre']}, tu plan {row['plan']} de {row['servicio']} vence el {row['fecha_pago']}. ¡Gracias por preferir OmniCast!"
            enlaces.append(f"https://wa.me/{row['telefono']}?text={urllib.parse.quote(msg)}")
        df['Notificar'] = enlaces
        
        # Mostrar tabla resumida
        st.dataframe(
            df[['nombre', 'servicio', 'plan', 'Estado Tiempo', 'estado', 'Notificar']],
            column_config={"Notificar": st.column_config.LinkColumn("WhatsApp", display_text="📲 Enviar Aviso")},
            hide_index=True, use_container_width=True
        )
    else:
        st.info("No hay datos.")

# --- PÁGINA 4: GESTIÓN DE CLAVES (Modificación en tiempo real) ---
elif opcion == "Gestión y Claves":
    st.title("🔐 Administrar Accesos y Clientes")
    st.warning("Zona de información confidencial. Aquí puedes ver y editar contraseñas.")
    df = obtener_clientes()
    
    if not df.empty:
        cliente_nombres = df['nombre'] + " - " + df['servicio'] + " (" + df['id'].astype(str) + ")"
        seleccion = st.selectbox("Selecciona un cliente para ver/editar sus datos:", cliente_nombres)
        
        if seleccion:
            # Extraer el ID del string seleccionado
            id_cliente = int(seleccion.split("(")[-1].replace(")", ""))
            datos = df[df['id'] == id_cliente].iloc[0]
            
            st.divider()
            
            with st.form(f"editar_form_{id_cliente}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Datos de Contacto")
                    e_nombre = st.text_input("Nombre", value=datos['nombre'])
                    e_telefono = st.text_input("WhatsApp", value=datos['telefono'])
                    e_servicio = st.selectbox("Servicio", ["Netflix", "Disney+", "Prime Video", "HBO Max", "Crunchyroll", "Spotify"], index=["Netflix", "Disney+", "Prime Video", "HBO Max", "Crunchyroll", "Spotify"].index(datos['servicio']) if datos['servicio'] in ["Netflix", "Disney+", "Prime Video", "HBO Max", "Crunchyroll", "Spotify"] else 0)
                    e_plan = st.text_input("Plan", value=datos['plan'])
                    e_fecha = st.date_input("Vencimiento", value=pd.to_datetime(datos['fecha_pago']).date())
                    e_estado = st.selectbox("Estado", ["Activo", "Vencido", "Suspendido"], index=["Activo", "Vencido", "Suspendido"].index(datos['estado']) if datos['estado'] in ["Activo", "Vencido", "Suspendido"] else 0)
                
                with col2:
                    st.subheader("Datos de Acceso")
                    e_correo = st.text_input("Correo de Cuenta", value=datos['correo'] if pd.notna(datos['correo']) else "")
                    e_contra = st.text_input("Contraseña", value=datos['contrasena'] if pd.notna(datos['contrasena']) else "")
                    e_pin = st.text_input("PIN", value=datos['pin'] if pd.notna(datos['pin']) else "")
                
                col_submit, col_delete = st.columns([1, 1])
                with col_submit:
                    if st.form_submit_button("Actualizar Cambios"):
                        actualizar_cliente(id_cliente, e_nombre, e_telefono, e_servicio, e_plan, e_fecha, e_estado, e_correo, e_contra, e_pin)
                        st.success("¡Datos actualizados exitosamente!")
                        st.rerun() # Recarga la página para mostrar los cambios
            
            # Botón de eliminar fuera del form para evitar clicks accidentales
            if st.button("❌ Eliminar Cliente Permanentemente", type="primary"):
                eliminar_cliente(id_cliente)
                st.success("Cliente eliminado.")
                st.rerun()
    else:
        st.info("Registra un cliente primero.")
