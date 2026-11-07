import streamlit as st
import pandas as pd
import sqlite3
from datetime import date, timedelta
import urllib.parse

# ==========================================
# 1. CONFIGURACIÓN GENERAL DE LA PÁGINA
# ==========================================
st.set_page_config(
    page_title="OmniCast PRO V4 | Gestión Total",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. SISTEMA DE LOGIN CON CONTRASEÑA
# ==========================================
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

def pantalla_login():
    st.markdown("""
    <style>
        .login-box {
            max-width: 420px;
            margin: 60px auto;
            padding: 35px;
            border-radius: 16px;
            background: linear-gradient(145deg, #161b22, #0d1117);
            border: 1px solid #30363d;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            text-align: center;
            color: white;
        }
        .login-title { font-size: 28px; font-weight: 800; margin-bottom: 5px; color: #FFFFFF; }
        .login-sub { font-size: 14px; color: #8b949e; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.3, 1])
    with col2:
        st.markdown('<div class="login-box"><div class="login-title">🚀 OmniCast PRO</div><div class="login-sub">Panel Privado de Administración</div></div>', unsafe_allow_html=True)
        with st.form("login_form"):
            usuario = st.text_input("👤 Usuario", placeholder="Ingresa tu usuario")
            clave = st.text_input("🔑 Contraseña", type="password", placeholder="Ingresa tu contraseña")
            ingresar = st.form_submit_button("🔓 Iniciar Sesión", use_container_width=True)
            
            if ingresar:
                if usuario.strip() == "lewis123" and clave.strip() == "201334":
                    st.session_state.autenticado = True
                    st.rerun()
                else:
                    st.error("❌ Usuario o contraseña incorrectos.")

if not st.session_state.autenticado:
    pantalla_login()
    st.stop()

# ==========================================
# 3. BASE DE DATOS Y PRECARGA DE TUS DATOS ACTUALES
# ==========================================
conn = sqlite3.connect('omnicast_v4_master.db', check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_vta TEXT,
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
    estado_pago TEXT,
    notas_2fa TEXT
)''')

c.execute('''CREATE TABLE IF NOT EXISTS cuentas_madre (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_mad TEXT,
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

def precargar_datos_actuales():
    # Precargar Cuentas Madre si la tabla está vacía
    c.execute("SELECT COUNT(*) FROM cuentas_madre")
    if c.fetchone()[0] == 0:
        madres_iniciales = [
            ("MAD-001", "Netflix", "hussainrazamonthly1@gmail.com", "sszzxx", "Proveedor Mayorista 1", "2026-11-30", 1, 7.00, "https://taikhoan24h.vn"),
            ("MAD-002", "Netflix", "hussainrazamonthly2@gmail.com", "sszzxx", "Proveedor Mayorista 1", "2026-11-30", 1, 7.00, "https://taikhoan24h.vn"),
            ("MAD-003", "Netflix", "hussainrazamonthly3@gmail.com", "sszzxx", "Proveedor Mayorista 1", "2026-11-30", 1, 7.00, "https://taikhoan24h.vn"),
            ("MAD-004", "Netflix", "QGXWL84PTN@gmail.com", "https://www.netflix.com/unsupported", "Proveedor Mayorista 2", "2026-11-30", 1, 7.00, "https://cheapnetf.pages.dev/"),
            ("MAD-005", "Netflix", "taikhoanflix0+29@gmail.com", "1niemvui", "Proveedor Mayorista 1", "2026-12-01", 1, 7.00, "https://taikhoan24h.vn"),
            ("MAD-006", "Netflix", "hussainrazamonthly150@gmail.com", "1minhem", "Proveedor Mayorista 1", "2026-12-02", 1, 7.00, "https://taikhoan24h.vn"),
            ("MAD-007", "Netflix", "Q2CH3KC279@gmail.com", "https://www.netflix.com/unsupported?nft", "Proveedor Mayorista 2", "2026-12-03", 1, 7.00, "https://cheapnetf.pages.dev/"),
            ("MAD-008", "Netflix", "FQBDW6QLJ5@gmail.com", "https://www.netflix.com/tv2?nftoken=Bgi", "Proveedor Mayorista 2", "2026-12-03", 1, 7.00, "https://cheapnetf.pages.dev/"),
            ("MAD-009", "Disney+", "dsntrapflix002@seiyafuzyom.com", "azulito113", "Panel", "2026-12-06", 5, 10.00, "")
        ]
        c.executemany('''INSERT INTO cuentas_madre 
            (codigo_mad, plataforma, correo_madre, clave_actual, proveedor, fecha_corte, capacidad_cupos, costo_madre, notas_recuperacion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', madres_iniciales)
        conn.commit()

    # Precargar Ventas si la tabla está vacía
    c.execute("SELECT COUNT(*) FROM ventas")
    if c.fetchone()[0] == 0:
        ventas_iniciales = [
            ("VTA-001", "YOJANY", "51952529351", "Netflix", "hussainrazamonthly1@gmail.com", "sszzxx", "Perfil 5 - ######", "1122", "Smart TV", "2026-10-31", "2026-11-30", 12.00, 7.00, "Yape", "Pagado", "Cliente Nuevo"),
            ("VTA-002", "RICARDO", "51959538866", "Netflix", "hussainrazamonthly2@gmail.com", "sszzxx", "Perfil 5 - ######", "-", "Celular / Laptop", "2026-10-31", "2026-11-30", 13.00, 7.00, "Plin", "Pagado", "Cliente Nuevo"),
            ("VTA-003", "LIZ - RIC", "51928268758", "Netflix", "hussainrazamonthly3@gmail.com", "sszzxx", "Perfil 1 - Liz", "1122", "Tablet", "2026-10-31", "2026-11-30", 12.00, 7.00, "Yape", "Pagado", "Cliente Nuevo"),
            ("VTA-004", "JAVIER", "51972174896", "Netflix", "QGXWL84PTN@gmail.com", "https://www.netflix.com/unsupported", "Perfil 4 - Javi", "-", "Celular", "2026-10-31", "2026-11-30", 13.00, 6.70, "Yape", "Pagado", "Cliente Nuevo | QGXWL84PTN - https://www.netflix"),
            ("VTA-005", "ENZO", "51918664028", "Netflix", "taikhoanflix0+29@gmail.com", "1niemvui", "Perfil 1 - ######", "-", "Celular", "2026-11-01", "2026-12-01", 13.00, 7.00, "Yape", "Pagado", "Cliente Nuevo"),
            ("VTA-006", "BRISSA", "51993464296", "Netflix", "hussainrazamonthly150@gmail.com", "1minhem", "Perfil 1 - ######", "1122", "Celular", "2026-11-02", "2026-12-02", 13.00, 7.00, "Yape", "Pagado", "Cliente Nuevo"),
            ("VTA-007", "ROGER", "51983645735", "Netflix", "Q2CH3KC279@gmail.com", "https://www.netflix.com/unsupported?nft", "Perfil 1 - ######", "-", "Tablet", "2026-11-03", "2026-12-03", 13.00, 6.70, "Yape", "Pagado", "Cliente Nuevo | QGXWL84PTN - https://www.netflix"),
            ("VTA-008", "JUNIOR", "51917838120", "Netflix", "FQBDW6QLJ5@gmail.com", "https://www.netflix.com/tv2?nftoken=Bgi", "Perfil 2 - ######", "-", "TV", "2026-11-03", "2026-12-03", 13.00, 6.70, "Yape", "Pagado", "Cliente Nuevo | QGXWL84PTN - https://www.netflix"),
            ("VTA-009", "JUNIOR", "51917838120", "Disney+", "dsntrapflix002@seiyafuzyom.com", "azulito113", "Perfil 2 - Junior", "2233", "TV", "2026-11-06", "2026-12-06", 10.00, 10.00, "Yape", "Pagado", "Cliente Nuevo")
        ]
        c.executemany('''INSERT INTO ventas 
            (codigo_vta, cliente, whatsapp, plataforma, correo_cuenta, clave_acceso, perfil, pin, dispositivo, fecha_venta, fecha_vencimiento, precio_venta, costo_prop, metodo_pago, estado_pago, notas_2fa)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', ventas_iniciales)
        conn.commit()

precargar_datos_actuales()

# ==========================================
# 4. MENÚ LATERAL Y SELECTOR DE MODO OSCURO / CLARO
# ==========================================
st.sidebar.markdown("## 🚀 **OmniCast PRO V4**")
st.sidebar.caption("Usuario activo: **lewis123**")

modo_tema = st.sidebar.toggle("☀️ Activar Modo Claro", value=False)

if modo_tema:
    bg_card = "linear-gradient(135deg, #ffffff, #f3f4f6)"
    text_card = "#111827"
    sub_card = "#4b5563"
    shadow_card = "0 4px 12px rgba(0,0,0,0.08)"
else:
    bg_card = "linear-gradient(135deg, rgba(30,35,45,0.95), rgba(18,22,30,0.95))"
    text_card = "#FFFFFF"
    sub_card = "#9CA3AF"
    shadow_card = "0 6px 16px rgba(0,0,0,0.35)"

st.markdown(f"""
<style>
    .metric-card {{
        background: {bg_card};
        border-left: 5px solid #E50914;
        padding: 18px 20px;
        border-radius: 12px;
        box-shadow: {shadow_card};
        color: {text_card};
        margin-bottom: 14px;
    }}
    .metric-title {{
        font-size: 12px;
        color: {sub_card};
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 700;
    }}
    .metric-value {{
        font-size: 26px;
        font-weight: 800;
        margin-top: 6px;
        color: {text_card};
    }}
    .metric-sub {{
        font-size: 12px;
        color: #10B981;
        margin-top: 4px;
        font-weight: 600;
    }}
    .card-green {{ border-left-color: #10B981 !important; }}
    .card-blue {{ border-left-color: #3B82F6 !important; }}
    .card-yellow {{ border-left-color: #F59E0B !important; }}
    .card-purple {{ border-left-color: #8B5CF6 !important; }}
</style>
""", unsafe_allow_html=True)

st.sidebar.divider()

menu = st.sidebar.radio(
    "Navegación Principal:",
    [
        "📊 Dashboard y Ganancias Mensuales",
        "📲 Control y Botones WhatsApp",
        "➕ Registrar Venta / Perfil",
        "🏦 Inventario Cuentas Madre",
        "🔐 Editar / Renovar / Claves",
        "⚙️ Respaldo y Herramientas"
    ]
)

st.sidebar.divider()
if st.sidebar.button("🔒 Cerrar Sesión", use_container_width=True):
    st.session_state.autenticado = False
    st.rerun()

PLATAFORMAS = ["Netflix", "Disney+", "Prime Video", "HBO Max", "Crunchyroll", "Spotify", "YouTube Premium", "Canva Pro", "ChatGPT Plus", "Paramount+", "Vix+", "Apple TV+"]

# ==========================================
# 5. FUNCIONES DE CÁLCULO
# ==========================================
MESES_ES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

def cargar_ventas():
    df = pd.read_sql_query("SELECT * FROM ventas", conn)
    if not df.empty:
        hoy = pd.to_datetime(date.today())
        df['fecha_venta_dt'] = pd.to_datetime(df['fecha_venta'])
        df['fecha_vencimiento_dt'] = pd.to_datetime(df['fecha_vencimiento'])
        df['dias_restantes'] = (df['fecha_vencimiento_dt'] - hoy).dt.days
        df['ganancia_neta'] = df['precio_venta'] - df['costo_prop']
        
        # Columna Mes-Año para Ganancias Mensuales
        df['mes_anio'] = df['fecha_venta_dt'].dt.strftime('%Y-%m')
        df['mes_nombre'] = df['fecha_venta_dt'].apply(lambda d: f"{MESES_ES[d.month]} {d.year}")
        
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

# ==========================================
# MÓDULO 1: DASHBOARD Y GANANCIAS MENSUALES
# ==========================================
if menu == "📊 Dashboard y Ganancias Mensuales":
    st.title("📊 Panel de Control Financiero y Ganancias Mensuales")
    df_v = cargar_ventas()
    df_m = cargar_madres()
    
    if not df_v.empty:
        # Filtro de Mes en la parte superior
        col_f1, col_f2 = st.columns([1.2, 2.8])
        with col_f1:
            meses_disponibles = ["🌎 Todos los Meses (Histórico)"] + sorted(df_v['mes_anio'].unique().tolist(), reverse=True)
            mes_sel = st.selectbox("📅 Filtrar métricas por Mes de Venta:", meses_disponibles)
            
        if mes_sel == "🌎 Todos los Meses (Histórico)":
            df_filtrado = df_v
            etiqueta_periodo = "Acumulado Total"
        else:
            df_filtrado = df_v[df_v['mes_anio'] == mes_sel]
            etiqueta_periodo = df_filtrado['mes_nombre'].iloc[0]

        ingresos_tot = df_filtrado['precio_venta'].sum()
        costos_tot = df_filtrado['costo_prop'].sum()
        ganancia_tot = df_filtrado['ganancia_neta'].sum()
        margen_porc = (ganancia_tot / ingresos_tot * 100) if ingresos_tot > 0 else 0.0
        por_vencer = len(df_v[df_v['dias_restantes'] <= 5])
        cupos_libres_tot = int(df_m['cupos_libres'].clip(lower=0).sum()) if not df_m.empty else 0

        # 5 Tarjetas de Alto Impacto
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            st.markdown(f'<div class="metric-card card-blue"><div class="metric-title">💰 Ingresos ({etiqueta_periodo})</div><div class="metric-value">S/ {ingresos_tot:.2f}</div><div class="metric-sub">{len(df_filtrado)} ventas registradas</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-card card-yellow"><div class="metric-title">📉 Costo Proveedor</div><div class="metric-value">S/ {costos_tot:.2f}</div><div class="metric-sub">Inversión en cuentas</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="metric-card card-green"><div class="metric-title">📈 Ganancia Neta</div><div class="metric-value">S/ {ganancia_tot:.2f}</div><div class="metric-sub">Margen: {margen_porc:.1f}%</div></div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div class="metric-card card-purple"><div class="metric-title">🟢 Perfiles Libres</div><div class="metric-value">{cupos_libres_tot} Cupos</div><div class="metric-sub">Listos para vender</div></div>', unsafe_allow_html=True)
        with c5:
            st.markdown(f'<div class="metric-card"><div class="metric-title">⚠️ Alertas (≤ 5 días)</div><div class="metric-value">{por_vencer} Clientes</div><div class="metric-sub">Requieren cobro pronto</div></div>', unsafe_allow_html=True)

        st.divider()

        # SECCIÓN ESTRELLA: TABLA Y GRÁFICO DE GANANCIAS MENSUALES
        st.subheader("📆 Consolidado de Ganancias Mensuales (Mes a Mes)")
        resumen_mensual = df_v.groupby(['mes_anio', 'mes_nombre'], as_index=False).agg(
            ventas_totales=('id', 'count'),
            ingresos_brutos=('precio_venta', 'sum'),
            costo_total=('costo_prop', 'sum'),
            ganancia_neta=('ganancia_neta', 'sum')
        ).sort_values(by='mes_anio', ascending=False)
        
        resumen_mensual['margen'] = (resumen_mensual['ganancia_neta'] / resumen_mensual['ingresos_brutos'] * 100).round(1).astype(str) + "%"

        col_m1, col_m2 = st.columns([1.4, 1])
        with col_m1:
            st.dataframe(
                resumen_mensual[['mes_nombre', 'ventas_totales', 'ingresos_brutos', 'costo_total', 'ganancia_neta', 'margen']],
                column_config={
                    "mes_nombre": "Mes y Año",
                    "ventas_totales": "Cant. Ventas",
                    "ingresos_brutos": st.column_config.NumberColumn("Ingresos (S/)", format="S/ %.2f"),
                    "costo_total": st.column_config.NumberColumn("Costos (S/)", format="S/ %.2f"),
                    "ganancia_neta": st.column_config.NumberColumn("Ganancia Neta (S/)", format="S/ %.2f"),
                    "margen": "Rentabilidad"
                },
                hide_index=True,
                use_container_width=True
            )
        with col_m2:
            st.caption("Comparativa Mensual: Ingresos vs Ganancia Neta (S/)")
            chart_mes = resumen_mensual.set_index('mes_nombre')[['ingresos_brutos', 'ganancia_neta']]
            st.bar_chart(chart_mes)

        st.divider()

        # Fila inferior: Vencimientos urgentes y desglose por Método de Pago
        col_b1, col_b2 = st.columns([1.4, 1])
        with col_b1:
            st.subheader("🚨 Próximos Vencimientos Urgentes (≤ 5 días)")
            urgentes = df_v[df_v['dias_restantes'] <= 5][['codigo_vta', 'cliente', 'plataforma', 'perfil', 'fecha_vencimiento', 'alerta']]
            if not urgentes.empty:
                st.dataframe(urgentes, hide_index=True, use_container_width=True)
            else:
                st.success("🎉 ¡Todo al día! Todos tus clientes tienen más de 5 días de vigencia activa.")
        with col_b2:
            st.subheader("💳 Recaudación por Método de Pago")
            pagos_df = df_filtrado.groupby('metodo_pago', as_index=False).agg(
                Operaciones=('id', 'count'),
                Total_Recaudado=('precio_venta', 'sum'),
                Ganancia=('ganancia_neta', 'sum')
            )
            st.dataframe(
                pagos_df,
                column_config={
                    "metodo_pago": "Método",
                    "Total_Recaudado": st.column_config.NumberColumn("Total (S/)", format="S/ %.2f"),
                    "Ganancia": st.column_config.NumberColumn("Ganancia (S/)", format="S/ %.2f")
                },
                hide_index=True,
                use_container_width=True
            )

# ==========================================
# MÓDULO 2: CONTROL Y 3 BOTONES WHATSAPP
# ==========================================
elif menu == "📲 Control y Botones WhatsApp":
    st.title("📲 Control General de Suscripciones y Botones WhatsApp")
    df = cargar_ventas()
    
    if not df.empty:
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            filtro_plat = st.selectbox("Plataforma:", ["Todas"] + PLATAFORMAS)
        with f2:
            filtro_estado = st.selectbox("Semáforo:", ["Todos", "🟢 Activos (>5 días)", "🟡 Por Vencer (0 a 5 días)", "🔴 Vencidos (<0 días)"])
        with f3:
            filtro_mes = st.selectbox("Mes de Venta:", ["Todos"] + sorted(df['mes_anio'].unique().tolist(), reverse=True))
        with f4:
            buscar_txt = st.text_input("🔍 Buscar Cliente / Correo / Perfil:")
            
        if filtro_plat != "Todas":
            df = df[df['plataforma'] == filtro_plat]
        if "🟢" in filtro_estado:
            df = df[df['dias_restantes'] > 5]
        elif "🟡" in filtro_estado:
            df = df[(df['dias_restantes'] >= 0) & (df['dias_restantes'] <= 5)]
        elif "🔴" in filtro_estado:
            df = df[df['dias_restantes'] < 0]
        if filtro_mes != "Todos":
            df = df[df['mes_anio'] == filtro_mes]
        if buscar_txt:
            df = df[
                df['cliente'].str.contains(buscar_txt, case=False, na=False) |
                df['correo_cuenta'].str.contains(buscar_txt, case=False, na=False) |
                df['perfil'].str.contains(buscar_txt, case=False, na=False)
            ]

        btn_cobrar = []
        btn_accesos = []
        btn_actualizar = []
        
        for _, r in df.iterrows():
            tel = ''.join(filter(str.isdigit, str(r['whatsapp'])))
            
            msg_cobro = (
                f"Hola *{r['cliente']}* 👋, te saluda *OmniCast*. "
                f"Te recordamos que tu servicio de *{r['plataforma']}* ({r['perfil']}) vence el *{r['fecha_vencimiento']}* ({r['alerta']}). "
                f"Para renovar por *S/ {r['precio_venta']:.2f}* vía Yape o Plin, confírmanos por aquí. ¡Gracias!"
            )
            btn_cobrar.append(f"https://wa.me/{tel}?text={urllib.parse.quote(msg_cobro)}")
            
            msg_perf = (
                f"Hola *{r['cliente']}* 🎬, aquí tienes los datos de acceso de tu cuenta *{r['plataforma']}* - *OmniCast*:\n"
                f"📧 *Correo:* {r['correo_cuenta']}\n"
                f"🔑 *Clave:* {r['clave_acceso']}\n"
                f"👤 *Perfil:* {r['perfil']}\n"
                f"📌 *PIN:* {r['pin']}\n"
                f"🖥️ *Dispositivo:* {r['dispositivo']}\n"
                f"📅 *Vencimiento:* {r['fecha_vencimiento']}\n"
                f"¡Que lo disfrutes!"
            )
            btn_accesos.append(f"https://wa.me/{tel}?text={urllib.parse.quote(msg_perf)}")
            
            msg_act = (
                f"Hola *{r['cliente']}* 🔄, te escribimos de *OmniCast*. "
                f"Actualizamos los datos de acceso de tu cuenta *{r['plataforma']}*:\n"
                f"📧 *Correo:* {r['correo_cuenta']}\n"
                f"🔑 *Nueva Clave:* {r['clave_acceso']}\n"
                f"👤 *Perfil:* {r['perfil']} (PIN: {r['pin']})"
            )
            btn_actualizar.append(f"https://wa.me/{tel}?text={urllib.parse.quote(msg_act)}")
            
        df['btn_accesos'] = btn_accesos
        df['btn_cobrar'] = btn_cobrar
        df['btn_actualizar'] = btn_actualizar
        
        st.dataframe(
            df[['codigo_vta', 'cliente', 'whatsapp', 'plataforma', 'correo_cuenta', 'clave_acceso', 'perfil', 'pin', 'dispositivo', 'fecha_vencimiento', 'alerta', 'precio_venta', 'ganancia_neta', 'metodo_pago', 'btn_accesos', 'btn_cobrar', 'btn_actualizar']],
            column_config={
                "codigo_vta": "ID",
                "cliente": "Cliente",
                "whatsapp": "WhatsApp",
                "plataforma": "Servicio",
                "correo_cuenta": "Correo Cuenta",
                "clave_acceso": "Contraseña / Link",
                "perfil": "Perfil",
                "pin": "PIN",
                "dispositivo": "Dispositivo",
                "fecha_vencimiento": "Vencimiento",
                "alerta": "Estado / Días",
                "precio_venta": st.column_config.NumberColumn("Precio", format="S/ %.2f"),
                "ganancia_neta": st.column_config.NumberColumn("Ganancia", format="S/ %.2f"),
                "metodo_pago": "Pago",
                "btn_accesos": st.column_config.LinkColumn("Accesos", display_text="📲 Enviar Datos"),
                "btn_cobrar": st.column_config.LinkColumn("Cobranza", display_text="💰 Cobrar"),
                "btn_actualizar": st.column_config.LinkColumn("Soporte", display_text="🔄 Actualizar")
            },
            hide_index=True,
            use_container_width=True
        )

        # Generador rápido de ficha copiable para WhatsApp Web
        with st.expander("📋 Copiar Ficha de Acceso en 1 Clic (Para pegar en WhatsApp Web)"):
            cli_sel = st.selectbox("Selecciona cliente para generar texto copiable:", df['codigo_vta'] + " - " + df['cliente'] + " (" + df['plataforma'] + ")")
            cod_sel = cli_sel.split(" - ")[0]
            r_copia = df[df['codigo_vta'] == cod_sel].iloc[0]
            texto_ficha = f"""🎬 *DATOS DE ACCESO - OMNICAST* 🎬
👤 *Cliente:* {r_copia['cliente']}
📺 *Servicio:* {r_copia['plataforma']}
📧 *Correo:* {r_copia['correo_cuenta']}
🔑 *Contraseña:* {r_copia['clave_acceso']}
🎭 *Perfil:* {r_copia['perfil']}
📌 *PIN:* {r_copia['pin']}
🖥️ *Dispositivo:* {r_copia['dispositivo']}
📅 *Fecha de Vencimiento:* {r_copia['fecha_vencimiento']}"""
            st.code(texto_ficha, language="markdown")

# ==========================================
# MÓDULO 3: REGISTRAR NUEVA VENTA
# ==========================================
elif menu == "➕ Registrar Venta / Perfil":
    st.title("➕ Registrar Nueva Venta de Suscripción")
    df_m = cargar_madres()
    df_v = cargar_ventas()
    
    sig_num = len(df_v) + 1
    cod_sugerido = f"VTA-{sig_num:03d}"
    
    # Selector inteligente fuera del form para autocompletar clave y plataforma
    if not df_m.empty:
        opciones_madre = ["✍️ Escribir cuenta manualmente..."] + [f"{r['correo_madre']} ({r['plataforma']} | Libres: {r['cupos_libres']})" for _, r in df_m.iterrows()]
        madre_elegida = st.selectbox("⚡ Autocompletar desde Inventario de Cuentas Madre (Opcional):", opciones_madre)
    else:
        madre_elegida = "✍️ Escribir cuenta manualmente..."

    correo_auto, clave_auto, plat_auto = "", "", "Netflix"
    if madre_elegida != "✍️ Escribir cuenta manualmente...":
        correo_extraido = madre_elegida.split(" (")[0]
        fila_m = df_m[df_m['correo_madre'] == correo_extraido].iloc[0]
        correo_auto = fila_m['correo_madre']
        clave_auto = fila_m['clave_actual']
        plat_auto = fila_m['plataforma'] if fila_m['plataforma'] in PLATAFORMAS else "Netflix"

    with st.form("form_nueva_venta_v4"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("👤 1. Datos del Cliente")
            codigo_vta = st.text_input("ID Venta", value=cod_sugerido)
            cliente = st.text_input("Nombre del Cliente *")
            whatsapp = st.text_input("WhatsApp (Con código 51) *", value="51")
            plataforma = st.selectbox("Plataforma / Servicio", PLATAFORMAS, index=PLATAFORMAS.index(plat_auto))
            dispositivo = st.selectbox("Dispositivo / Regla Uso", ["Smart TV", "Celular / Laptop", "Celular", "Tablet", "TV", "Cuenta Completa"])
            
        with col2:
            st.subheader("🔐 2. Cuenta y Perfil")
            correo_cuenta = st.text_input("Correo de la Cuenta (Login)", value=correo_auto)
            clave_acceso = st.text_input("Contraseña de Acceso / Link", value=clave_auto)
            perfil = st.text_input("Perfil Asignado", value="Perfil 1 - ")
            pin = st.text_input("PIN del Perfil", value="-")
            notas_2fa = st.text_input("Observaciones / Garantía / 2FA", value="Cliente Nuevo")
            
        with col3:
            st.subheader("💵 3. Fechas y Finanzas")
            f_venta = st.date_input("Fecha de Venta", value=date.today())
            duracion_dias = st.number_input("Días de Vigencia (+ Días Extra)", min_value=1, max_value=365, value=30)
            precio_venta = st.number_input("Precio de Venta (S/)", min_value=0.0, value=13.0, step=0.5)
            costo_prop = st.number_input("Costo Proporcional (S/)", min_value=0.0, value=7.0, step=0.1)
            metodo_pago = st.selectbox("Método de Pago", ["Yape", "Plin", "BCP", "Ligo", "Efectivo", "Transferencia"])
            
        guardar = st.form_submit_button("✅ Registrar Venta en el Sistema", use_container_width=True)
        
        if guardar:
            if cliente and whatsapp and len(whatsapp.strip()) >= 9:
                f_venc = f_venta + timedelta(days=int(duracion_dias))
                c.execute('''INSERT INTO ventas 
                    (codigo_vta, cliente, whatsapp, plataforma, correo_cuenta, clave_acceso, perfil, pin, dispositivo, fecha_venta, fecha_vencimiento, precio_venta, costo_prop, metodo_pago, estado_pago, notas_2fa)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (codigo_vta, cliente.upper().strip(), whatsapp.strip(), plataforma, correo_cuenta.strip(), clave_acceso.strip(), perfil, pin, dispositivo, str(f_venta), str(f_venc), precio_venta, costo_prop, metodo_pago, "Pagado", notas_2fa))
                conn.commit()
                st.success(f"🎉 ¡Venta **{codigo_vta}** registrada para **{cliente.upper()}**! Ganancia neta: **S/ {precio_venta - costo_prop:.2f}**")
            else:
                st.error("⚠️ Ingresa el nombre del cliente y un número de WhatsApp válido.")

# ==========================================
# MÓDULO 4: INVENTARIO DE CUENTAS MADRE
# ==========================================
elif menu == "🏦 Inventario Cuentas Madre":
    st.title("🏦 Inventario de Cuentas Madre, Perfiles Libres y Proveedores")
    df_m = cargar_madres()
    
    with st.expander("➕ Agregar Nueva Cuenta Madre al Inventario", expanded=False):
        sig_mad = f"MAD-{(len(df_m) + 1):03d}"
        with st.form("form_madre_v4"):
            c1, c2, c3 = st.columns(3)
            with c1:
                m_cod = st.text_input("ID Matriz", value=sig_mad)
                m_plat = st.selectbox("Plataforma", PLATAFORMAS)
                m_correo = st.text_input("Correo de Cuenta Madre *")
            with c2:
                m_clave = st.text_input("Contraseña Actual / Link *")
                m_prov = st.text_input("Proveedor / Origen", value="Proveedor Mayorista 1")
                m_corte = st.date_input("Fecha de Corte Proveedor", value=date.today() + timedelta(days=30))
            with c3:
                m_cupos = st.number_input("Capacidad Total (Cupos)", min_value=1, max_value=10, value=1)
                m_costo = st.number_input("Costo Cuenta Madre (S/)", min_value=0.0, value=7.0, step=0.5)
                m_notas = st.text_input("Web 2FA / Correo Recuperación", value="https://taikhoan24h.vn")
                
            if st.form_submit_button("💾 Guardar Cuenta Madre", use_container_width=True):
                if m_correo:
                    try:
                        c.execute('''INSERT INTO cuentas_madre 
                            (codigo_mad, plataforma, correo_madre, clave_actual, proveedor, fecha_corte, capacidad_cupos, costo_madre, notas_recuperacion)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                            (m_cod, m_plat, m_correo.strip(), m_clave.strip(), m_prov, str(m_corte), m_cupos, m_costo, m_notas))
                        conn.commit()
                        st.success("✅ Cuenta Madre registrada correctamente.")
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("⚠️ Ese correo de Cuenta Madre ya está registrado.")

    if not df_m.empty:
        st.dataframe(
            df_m[['codigo_mad', 'plataforma', 'correo_madre', 'clave_actual', 'proveedor', 'fecha_corte', 'dias_corte', 'capacidad_cupos', 'cupos_ocupados', 'cupos_libres', 'disponibilidad', 'costo_madre', 'ingresos_activos', 'utilidad_real', 'notas_recuperacion']],
            column_config={
                "codigo_mad": "ID Matriz",
                "plataforma": "Plataforma",
                "correo_madre": "Correo Cuenta Madre",
                "clave_actual": "Contraseña / Link",
                "proveedor": "Proveedor",
                "fecha_corte": "Fecha Corte",
                "dias_corte": "Días Corte",
                "capacidad_cupos": "Capacidad",
                "cupos_ocupados": "Ocupados",
                "cupos_libres": "Libres",
                "disponibilidad": "Disponibilidad",
                "costo_madre": st.column_config.NumberColumn("Costo (S/)", format="S/ %.2f"),
                "ingresos_activos": st.column_config.NumberColumn("Ingresos (S/)", format="S/ %.2f"),
                "utilidad_real": st.column_config.NumberColumn("Utilidad Real", format="S/ %.2f"),
                "notas_recuperacion": st.column_config.LinkColumn("Link 2FA / Notas")
            },
            hide_index=True,
            use_container_width=True
        )

# ==========================================
# MÓDULO 5: EDITAR, RENOVAR (+30 DÍAS) O ELIMINAR
# ==========================================
elif menu == "🔐 Editar / Renovar / Claves":
    st.title("🔐 Modificar Accesos o Renovar Suscripción en Tiempo Real")
    df = cargar_ventas()
    
    if not df.empty:
        opciones = df['id'].astype(str) + " | " + df['codigo_vta'].fillna('') + " - " + df['cliente'] + " (" + df['plataforma'] + " - " + df['correo_cuenta'] + ")"
        seleccion = st.selectbox("Selecciona el cliente a gestionar:", opciones)
        
        id_sel = int(seleccion.split(" | ")[0])
        row = df[df['id'] == id_sel].iloc[0]
        
        # Acciones rápidas en 1 clic
        col_r1, col_r2, col_r3 = st.columns([1, 1, 2])
        with col_r1:
            if st.button("🔄 Renovar +30 Días (1 Clic)", use_container_width=True):
                nueva_fecha = pd.to_datetime(row['fecha_vencimiento']).date() + timedelta(days=30)
                c.execute("UPDATE ventas SET fecha_vencimiento=?, fecha_venta=? WHERE id=?", (str(nueva_fecha), str(date.today()), id_sel))
                conn.commit()
                st.success(f"✅ Suscripción renovada hasta el {nueva_fecha}!")
                st.rerun()
        with col_r2:
            if st.button("🗑️ Eliminar Registro", type="primary", use_container_width=True):
                c.execute("DELETE FROM ventas WHERE id=?", (id_sel,))
                conn.commit()
                st.warning("Registro eliminado.")
                st.rerun()

        st.divider()
        with st.form(f"edit_venta_{id_sel}"):
            c1, c2, c3 = st.columns(3)
            with c1:
                e_cod = st.text_input("ID Venta", value=row['codigo_vta'] if pd.notna(row['codigo_vta']) else "")
                e_cliente = st.text_input("Cliente", value=row['cliente'])
                e_wa = st.text_input("WhatsApp", value=row['whatsapp'])
                e_plat = st.selectbox("Plataforma", PLATAFORMAS, index=PLATAFORMAS.index(row['plataforma']) if row['plataforma'] in PLATAFORMAS else 0)
                e_disp = st.text_input("Dispositivo", value=row['dispositivo'] if pd.notna(row['dispositivo']) else "")
            with c2:
                e_correo = st.text_input("Correo Cuenta", value=row['correo_cuenta'] if pd.notna(row['correo_cuenta']) else "")
                e_clave = st.text_input("Contraseña / Link", value=row['clave_acceso'] if pd.notna(row['clave_acceso']) else "")
                e_perfil = st.text_input("Perfil Asignado", value=row['perfil'] if pd.notna(row['perfil']) else "")
                e_pin = st.text_input("PIN", value=row['pin'] if pd.notna(row['pin']) else "")
                e_notas = st.text_input("Observaciones / 2FA", value=row['notas_2fa'] if pd.notna(row['notas_2fa']) else "")
            with c3:
                e_fventa = st.date_input("Fecha de Venta", value=pd.to_datetime(row['fecha_venta']).date())
                e_fvenc = st.date_input("Fecha de Vencimiento", value=pd.to_datetime(row['fecha_vencimiento']).date())
                e_precio = st.number_input("Precio Venta (S/)", value=float(row['precio_venta']), step=0.5)
                e_costo = st.number_input("Costo Prop. (S/)", value=float(row['costo_prop']), step=0.1)
                metodos = ["Yape", "Plin", "BCP", "Ligo", "Efectivo", "Transferencia"]
                e_metodo = st.selectbox("Método de Pago", metodos, index=metodos.index(row['metodo_pago']) if row['metodo_pago'] in metodos else 0)
                
            if st.form_submit_button("💾 Guardar Todos los Cambios", use_container_width=True):
                c.execute('''UPDATE ventas SET 
                    codigo_vta=?, cliente=?, whatsapp=?, plataforma=?, correo_cuenta=?, clave_acceso=?, perfil=?, pin=?, dispositivo=?, fecha_venta=?, fecha_vencimiento=?, precio_venta=?, costo_prop=?, metodo_pago=?, notas_2fa=?
                    WHERE id=?''',
                    (e_cod, e_cliente.upper().strip(), e_wa.strip(), e_plat, e_correo.strip(), e_clave.strip(), e_perfil, e_pin, e_disp, str(e_fventa), str(e_fvenc), e_precio, e_costo, e_metodo, e_notas, id_sel))
                conn.commit()
                st.success("✅ ¡Datos actualizados en tiempo real!")
                st.rerun()

# ==========================================
# MÓDULO 6: RESPALDO EN EXCEL / HERRAMIENTAS
# ==========================================
elif menu == "⚙️ Respaldo y Herramientas":
    st.title("⚙️ Exportar a Excel y Respaldo de Base de Datos")
    df_v = cargar_ventas()
    df_m = cargar_madres()
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📥 Descargar Reporte de Ventas (CSV / Excel)")
        if not df_v.empty:
            csv_ventas = df_v.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📊 Descargar Tabla de Clientes y Ventas (.csv)",
                data=csv_ventas,
                file_name=f"OmniCast_Ventas_{date.today()}.csv",
                mime="text/csv",
                use_container_width=True
            )
    with c2:
        st.subheader("📥 Descargar Inventario Cuentas Madre")
        if not df_m.empty:
            csv_madres = df_m.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="🏦 Descargar Inventario Cuentas Madre (.csv)",
                data=csv_madres,
                file_name=f"OmniCast_CuentasMadre_{date.today()}.csv",
                mime="text/csv",
                use_container_width=True
            )
