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
        df = df.sort_values(by='dias_restantes', ascending=True)
    return df

def cargar_madres():
    df_m = pd.read_sql_query("SELECT * FROM cuentas_madre", conn)
    df_v = pd.read_sql_query("SELECT * FROM ventas", conn)
    if not df_m.empty:
        hoy = pd.to_datetime(date.today())
        df_m['dias_corte'] = (pd.to_datetime(df_m['fecha_corte']) - hoy).dt.days
        
        ocupados_list = []
        ingresos_list = []
        for _, row in df_m.iterrows():
            if not df_v.empty:
                ventas_cuenta = df_v[df_v['correo_cuenta'].str.lower() == str(row['correo_madre']).lower()]
                ocupados = len(ventas_cuenta)
                ingresos = ventas_cuenta['precio_venta'].sum()
            else:
                ocupados = 0
                ingresos = 0.0
            ocupados_list.append(ocupados)
            ingresos_list.append(ingresos)
            
        df_m['cupos_ocupados'] = ocupados_list
        df_m['cupos_libres'] = df_m['capacidad_cupos'] - df_m['cupos_ocupados']
        df_m['ingresos_activos'] = ingresos_list
        df_m['utilidad_real'] = df_m['ingresos_activos'] - df_m['costo_madre']
        df_m['disponibilidad'] = df_m['cupos_libres'].apply(
            lambda x: f"🟢 DISPONIBLE ({x} libres)" if x > 0 else "🔴 LLENA (SIN CUPOS)"
        )
    return df_m

# 5. MENÚ LATERAL
st.sidebar.markdown("## 🚀 **OmniCast PRO**")
st.sidebar.caption("Control de Suscripciones, Perfiles y Finanzas")
st.sidebar.divider()

menu = st.sidebar.radio(
    "Módulos del Sistema:",
    [
        "📊 Dashboard y Finanzas",
        "➕ Registrar Venta / Perfil",
        "📲 Control y Botones WhatsApp",
        "🏦 Inventario Cuentas Madre",
        "🔐 Editar / Eliminar Accesos"
    ]
)

PLATAFORMAS = ["Netflix", "Disney+", "Prime Video", "HBO Max", "Crunchyroll", "Spotify", "YouTube Premium", "Canva Pro", "ChatGPT Plus"]

# ==========================================
# MÓDULO 1: DASHBOARD Y FINANZAS
# ==========================================
if menu == "📊 Dashboard y Finanzas":
    st.title("📊 Panel de Control Financiero y Operativo")
    df_v = cargar_ventas()
    df_m = cargar_madres()
    
    ingresos_tot = df_v['precio_venta'].sum() if not df_v.empty else 0.0
    costos_tot = df_v['costo_prop'].sum() if not df_v.empty else 0.0
    ganancia_tot = df_v['ganancia_neta'].sum() if not df_v.empty else 0.0
    por_vencer = len(df_v[df_v['dias_restantes'] <= 5]) if not df_v.empty else 0
    
    # Tarjetas Financieras superiores (Estilo Excel Netflix)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card card-blue"><div class="metric-title">💰 Ingresos (Ventas)</div><div class="metric-value">S/ {ingresos_tot:.2f}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card card-yellow"><div class="metric-title">📉 Costo Proveedor</div><div class="metric-value">S/ {costos_tot:.2f}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card card-green"><div class="metric-title">📈 Ganancia Neta</div><div class="metric-value">S/ {ganancia_tot:.2f}</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><div class="metric-title">⚠️ Alertas (≤ 5 días)</div><div class="metric-value">{por_vencer} Clientes</div></div>', unsafe_allow_html=True)

    st.divider()
    
    if not df_v.empty:
        col_g1, col_g2 = st.columns([1.2, 1])
        with col_g1:
            st.subheader("🚨 Próximos Vencimientos Urgentes")
            urgentes = df_v[df_v['dias_restantes'] <= 5][['cliente', 'plataforma', 'perfil', 'fecha_vencimiento', 'alerta']]
            if not urgentes.empty:
                st.dataframe(urgentes, hide_index=True, use_container_width=True)
            else:
                st.success("🎉 ¡Todo al día! No tienes cuentas vencidas ni por vencer en los próximos 5 días.")
                
        with col_g2:
            st.subheader("📺 Ingresos por Plataforma (S/)")
            resumen_plat = df_v.groupby('plataforma')[['precio_venta', 'ganancia_neta']].sum()
            st.bar_chart(resumen_plat)
    else:
        st.info("Aún no hay ventas registradas. Dirígete a '➕ Registrar Venta / Perfil' en el menú izquierdo para empezar.")

# ==========================================
# MÓDULO 2: REGISTRAR VENTA / CLIENTE
# ==========================================
elif menu == "➕ Registrar Venta / Perfil":
    st.title("➕ Registrar Nueva Venta de Suscripción")
    df_m = cargar_madres()
    
    with st.form("form_nueva_venta"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("👤 1. Cliente")
            cliente = st.text_input("Nombre del Cliente *")
            whatsapp = st.text_input("WhatsApp (Con código 51) *", value="51")
            plataforma = st.selectbox("Plataforma / Servicio", PLATAFORMAS)
            dispositivo = st.selectbox("Dispositivo / Regla", ["Smart TV", "Celular / Laptop", "Tablet", "TV", "Cuenta Completa"])
            
        with col2:
            st.subheader("🔐 2. Cuenta y Perfil")
            if not df_m.empty:
                correos_disp = ["Escribir manualmente..."] + df_m['correo_madre'].tolist()
                correo_sel = st.selectbox("Seleccionar Cuenta Madre (Opcional)", correos_disp)
            else:
                correo_sel = "Escribir manualmente..."
                
            correo_manual = st.text_input("Correo de la Cuenta (Si no elegiste arriba)")
            clave_acceso = st.text_input("Contraseña de Acceso")
            perfil = st.text_input("Perfil Asignado (Ej: Perfil 1 - Liz)")
            pin = st.text_input("PIN del Perfil (Ej: 1122)")
            
        with col3:
            st.subheader("💵 3. Finanzas y Fechas")
            f_venta = st.date_input("Fecha de Venta", value=date.today())
            duracion_dias = st.number_input("Días de Vigencia", min_value=1, max_value=365, value=30)
            precio_venta = st.number_input("Precio de Venta (S/)", min_value=0.0, value=12.0, step=0.5)
            costo_prop = st.number_input("Costo Proporcional Perfil (S/)", min_value=0.0, value=7.0, step=0.5)
            metodo_pago = st.selectbox("Método de Pago", ["Yape", "Plin", "BCP", "Ligo", "Efectivo", "Transferencia"])
            notas_2fa = st.text_input("Link 2FA / Garantía / Observaciones")
            
        guardar = st.form_submit_button("✅ Guardar Venta y Generar Accesos", use_container_width=True)
        
        if guardar:
            correo_final = correo_manual if correo_sel == "Escribir manualmente..." else correo_sel
            if cliente and whatsapp and len(whatsapp) >= 9:
                f_venc = f_venta + timedelta(days=int(duracion_dias))
                c.execute('''INSERT INTO ventas 
                    (cliente, whatsapp, plataforma, correo_cuenta, clave_acceso, perfil, pin, dispositivo, fecha_venta, fecha_vencimiento, precio_venta, costo_prop, metodo_pago, notas_2fa)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (cliente, whatsapp.strip(), plataforma, correo_final, clave_acceso, perfil, pin, dispositivo, str(f_venta), str(f_venc), precio_venta, costo_prop, metodo_pago, notas_2fa))
                conn.commit()
                st.success(f"✅ ¡Venta registrada para **{cliente}**! Vence el {f_venc.strftime('%d/%m/%Y')}. Ganancia Neta: **S/ {precio_venta - costo_prop:.2f}**")
            else:
                st.error("⚠️ Por favor completa el Nombre del Cliente y un número de WhatsApp válido.")

# ==========================================
# MÓDULO 3: CONTROL Y 3 BOTONES WHATSAPP
# ==========================================
elif menu == "📲 Control y Botones WhatsApp":
    st.title("📲 Control de Vencimientos y Mensajería Rápida")
    st.caption("Incluye Semáforo de Vigencia y los 3 botones directos de WhatsApp (Accesos, Cobranza y Cambio de Clave).")
    
    df = cargar_ventas()
    
    if not df.empty:
        # Filtros rápidos en línea
        f1, f2, f3 = st.columns(3)
        with f1:
            filtro_plat = st.selectbox("Filtrar por Plataforma:", ["Todas"] + PLATAFORMAS)
        with f2:
            filtro_estado = st.selectbox("Filtrar por Semáforo:", ["Todos", "🟢 Activos (>5 días)", "🟡 Por Vencer (0 a 5 días)", "🔴 Vencidos (<0 días)"])
        with f3:
            buscar_txt = st.text_input("🔍 Buscar por Cliente o Correo:")
            
        if filtro_plat != "Todas":
            df = df[df['plataforma'] == filtro_plat]
        if "🟢" in filtro_estado:
            df = df[df['dias_restantes'] > 5]
        elif "🟡" in filtro_estado:
            df = df[(df['dias_restantes'] >= 0) & (df['dias_restantes'] <= 5)]
        elif "🔴" in filtro_estado:
            df = df[df['dias_restantes'] < 0]
        if buscar_txt:
            df = df[df['cliente'].str.contains(buscar_txt, case=False, na=False) | df['correo_cuenta'].str.contains(buscar_txt, case=False, na=False)]

        # Generación de los 3 Botones de WhatsApp inspirados en el Excel de Netflix
        btn_cobrar = []
        btn_accesos = []
        btn_actualizar = []
        
        for _, r in df.iterrows():
            tel = ''.join(filter(str.isdigit, str(r['whatsapp'])))
            
            # 1. Mensaje Cobrar / Renovar
            msg_cobro = (
                f"Hola *{r['cliente']}* 👋, te saluda *OmniCast*. "
                f"Te recordamos que tu suscripción de *{r['plataforma']}* ({r['perfil']}) vence el *{r['fecha_vencimiento']}* ({r['alerta']}). "
                f"Para renovar por *S/ {r['precio_venta']:.2f}* vía Yape o Plin, confírmanos por aquí. ¡Gracias!"
            )
            btn_cobrar.append(f"https://wa.me/{tel}?text={urllib.parse.quote(msg_cobro)}")
            
            # 2. Mensaje Enviar Datos de Perfil y PIN
            msg_perf = (
                f"Hola *{r['cliente']}* 🎬, aquí tienes los accesos de tu cuenta *{r['plataforma']}* - *OmniCast*:\n"
                f"📧 *Correo:* {r['correo_cuenta']}\n"
                f"🔑 *Clave:* {r['clave_acceso']}\n"
                f"👤 *Perfil:* {r['perfil']}\n"
                f"📌 *PIN:* {r['pin']}\n"
                f"📅 *Vencimiento:* {r['fecha_vencimiento']}\n"
                f"¡Que lo disfrutes!"
            )
            btn_accesos.append(f"https://wa.me/{tel}?text={urllib.parse.quote(msg_perf)}")
            
            # 3. Mensaje Actualizar Clave / Soporte
            msg_act = (
                f"Hola *{r['cliente']}* 🔄, te escribimos de *OmniCast*. "
                f"Hemos actualizado la contraseña de tu cuenta *{r['plataforma']}* por mantenimiento.\n"
                f"🔑 *Nueva Clave:* {r['clave_acceso']}\n"
                f"👤 *Tu Perfil:* {r['perfil']} (PIN: {r['pin']})"
            )
            btn_actualizar.append(f"https://wa.me/{tel}?text={urllib.parse.quote(msg_act)}")
            
        df['btn_cobrar'] = btn_cobrar
        df['btn_accesos'] = btn_accesos
        df['btn_actualizar'] = btn_actualizar
        
        st.dataframe(
            df[['cliente', 'plataforma', 'perfil', 'pin', 'correo_cuenta', 'clave_acceso', 'fecha_vencimiento', 'alerta', 'ganancia_neta', 'btn_accesos', 'btn_cobrar', 'btn_actualizar']],
            column_config={
                "cliente": "Cliente",
                "plataforma": "Servicio",
                "perfil": "Perfil",
                "pin": "PIN",
                "correo_cuenta": "Correo Cuenta",
                "clave_acceso": "Clave",
                "fecha_vencimiento": "Expiración",
                "alerta": "Semáforo / Días",
                "ganancia_neta": st.column_config.NumberColumn("Ganancia", format="S/ %.2f"),
                "btn_accesos": st.column_config.LinkColumn("Enviar Accesos", display_text="💻 Perfiles"),
                "btn_cobrar": st.column_config.LinkColumn("Cobranza", display_text="💰 Cobrar"),
                "btn_actualizar": st.column_config.LinkColumn("Soporte", display_text="🔑 Actualizar")
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("No hay clientes registrados todavía.")

# ==========================================
# MÓDULO 4: INVENTARIO DE CUENTAS MADRE
# ==========================================
elif menu == "🏦 Inventario Cuentas Madre":
    st.title("🏦 Inventario de Cuentas Madre y Cupos Libres")
    st.caption("Se sincroniza automáticamente con tus ventas: calcula cuántos perfiles están ocupados y cuántos quedan libres para vender.")
    
    with st.expander("➕ Registrar Nueva Cuenta Madre (Proveedor)", expanded=False):
        with st.form("form_madre"):
            c1, c2, c3 = st.columns(3)
            with c1:
                m_plat = st.selectbox("Plataforma", PLATAFORMAS)
                m_correo = st.text_input("Correo de Cuenta Madre *")
                m_clave = st.text_input("Contraseña Actual *")
            with c2:
                m_prov = st.text_input("Proveedor / Origen (Ej: Mayorista 1)")
                m_corte = st.date_input("Fecha de Corte Proveedor", value=date.today() + timedelta(days=30))
                m_cupos = st.number_input("Capacidad Total (Perfiles/Cupos)", min_value=1, max_value=10, value=5)
            with c3:
                m_costo = st.number_input("Costo Cuenta Madre (S/)", min_value=0.0, value=10.0, step=0.5)
                m_notas = st.text_input("Link 2FA / Correo Recuperación / Notas")
                
            if st.form_submit_button("💾 Guardar Cuenta Madre", use_container_width=True):
                if m_correo:
                    try:
                        c.execute('''INSERT INTO cuentas_madre 
                            (plataforma, correo_madre, clave_actual, proveedor, fecha_corte, capacidad_cupos, costo_madre, notas_recuperacion)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                            (m_plat, m_correo.strip(), m_clave, m_prov, str(m_corte), m_cupos, m_costo, m_notas))
                        conn.commit()
                        st.success("✅ Cuenta Madre añadida al inventario.")
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("⚠️ Este correo de cuenta madre ya existe en tu inventario.")
                else:
                    st.error("El correo de la cuenta madre es obligatorio.")

    df_m = cargar_madres()
    if not df_m.empty:
        st.dataframe(
            df_m[['plataforma', 'correo_madre', 'clave_actual', 'proveedor', 'fecha_corte', 'dias_corte', 'capacidad_cupos', 'cupos_ocupados', 'cupos_libres', 'disponibilidad', 'costo_madre', 'ingresos_activos', 'utilidad_real', 'notas_recuperacion']],
            column_config={
                "plataforma": "Plataforma",
                "correo_madre": "Correo Cuenta Madre",
                "clave_actual": "Clave",
                "proveedor": "Proveedor",
                "fecha_corte": "Fecha Corte",
                "dias_corte": "Días Corte",
                "capacidad_cupos": "Total Cupos",
                "cupos_ocupados": "Ocupados",
                "cupos_libres": "Libres",
                "disponibilidad": "Disponibilidad",
                "costo_madre": st.column_config.NumberColumn("Costo (S/)", format="S/ %.2f"),
                "ingresos_activos": st.column_config.NumberColumn("Ingresos (S/)", format="S/ %.2f"),
                "utilidad_real": st.column_config.NumberColumn("Utilidad Real", format="S/ %.2f"),
                "notas_recuperacion": "2FA / Notas"
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("No has registrado Cuentas Madre aún. Abre el desplegable de arriba para registrar tus cuentas completas.")

# ==========================================
# MÓDULO 5: EDITAR / ELIMINAR EN TIEMPO REAL
# ==========================================
elif menu == "🔐 Editar / Eliminar Accesos":
    st.title("🔐 Modificar Datos, Claves o Renovar Cliente")
    df = cargar_ventas()
    
    if not df.empty:
        opciones = df['id'].astype(str) + " | " + df['cliente'] + " - " + df['plataforma'] + " (" + df['perfil'].fillna('') + ")"
        seleccion = st.selectbox("Selecciona el registro que deseas editar:", opciones)
        
        id_sel = int(seleccion.split(" | ")[0])
        row = df[df['id'] == id_sel].iloc[0]
        
        st.divider()
        with st.form(f"edit_venta_{id_sel}"):
            c1, c2, c3 = st.columns(3)
            with c1:
                e_cliente = st.text_input("Cliente", value=row['cliente'])
                e_wa = st.text_input("WhatsApp", value=row['whatsapp'])
                e_plat = st.selectbox("Plataforma", PLATAFORMAS, index=PLATAFORMAS.index(row['plataforma']) if row['plataforma'] in PLATAFORMAS else 0)
                e_disp = st.text_input("Dispositivo", value=row['dispositivo'] if pd.notna(row['dispositivo']) else "")
            with c2:
                e_correo = st.text_input("Correo Cuenta", value=row['correo_cuenta'] if pd.notna(row['correo_cuenta']) else "")
                e_clave = st.text_input("Contraseña", value=row['clave_acceso'] if pd.notna(row['clave_acceso']) else "")
                e_perfil = st.text_input("Perfil Asignado", value=row['perfil'] if pd.notna(row['perfil']) else "")
                e_pin = st.text_input("PIN", value=row['pin'] if pd.notna(row['pin']) else "")
            with c3:
                e_fvenc = st.date_input("Fecha de Vencimiento", value=pd.to_datetime(row['fecha_vencimiento']).date())
                e_precio = st.number_input("Precio Venta (S/)", value=float(row['precio_venta']), step=0.5)
                e_costo = st.number_input("Costo Prop. (S/)", value=float(row['costo_prop']), step=0.5)
                e_notas = st.text_input("Notas / 2FA", value=row['notas_2fa'] if pd.notna(row['notas_2fa']) else "")
                
            if st.form_submit_button("💾 Guardar Cambios en Tiempo Real", use_container_width=True):
                c.execute('''UPDATE ventas SET 
                    cliente=?, whatsapp=?, plataforma=?, correo_cuenta=?, clave_acceso=?, perfil=?, pin=?, dispositivo=?, fecha_vencimiento=?, precio_venta=?, costo_prop=?, notas_2fa=?
                    WHERE id=?''',
                    (e_cliente, e_wa, e_plat, e_correo, e_clave, e_perfil, e_pin, e_disp, str(e_fvenc), e_precio, e_costo, e_notas, id_sel))
                conn.commit()
                st.success("✅ ¡Registro actualizado exitosamente!")
                st.rerun()
                
        if st.button("🗑️ Eliminar este cliente permanentemente", type="primary"):
            c.execute("DELETE FROM ventas WHERE id=?", (id_sel,))
            conn.commit()
            st.warning("Cliente eliminado.")
            st.rerun()
    else:
        st.info("No hay clientes registrados para editar.")
