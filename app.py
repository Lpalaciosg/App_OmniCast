import streamlit as st
import pandas as pd
from datetime import date, timedelta
import urllib.parse
import html
from supabase import create_client, Client

# ==========================================
# 1. CONFIGURACIÓN GENERAL DE LA PÁGINA
# ==========================================
st.set_page_config(
    page_title="OmniCast AI | Neural Streaming Core",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. SISTEMA DE LOGIN FUTURISTA CON CONTRASEÑA
# ==========================================
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if "menu_activo" not in st.session_state:
    st.session_state.menu_activo = "📲 Registros y Central IA"

def pantalla_login():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800&family=Inter:wght@400;600;700&display=swap');
        .login-box {
            max-width: 440px;
            margin: 50px auto 20px auto;
            padding: 38px 30px;
            border-radius: 20px;
            background: radial-gradient(circle at top right, rgba(0, 240, 255, 0.15), rgba(15, 23, 42, 0.95));
            border: 1px solid rgba(0, 240, 255, 0.4);
            box-shadow: 0 0 35px rgba(0, 240, 255, 0.18);
            text-align: center;
            color: white;
            backdrop-filter: blur(12px);
        }
        .login-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 28px;
            font-weight: 800;
            background: linear-gradient(90deg, #00F0FF, #A855F7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }
        .login-sub { font-size: 13px; color: #94A3B8; letter-spacing: 1px; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.3, 1])
    with col2:
        st.markdown('<div class="login-box"><div class="login-title">🤖 OMNICAST AI</div><div class="login-sub">Neural Subscription Core v6.0</div></div>', unsafe_allow_html=True)
        with st.form("login_form"):
            usuario = st.text_input("👤 Operador IA", placeholder="Ingresa tu usuario")
            clave = st.text_input("🔑 Clave de Acceso", type="password", placeholder="Ingresa tu contraseña")
            ingresar = st.form_submit_button("⚡ INICIAR CONEXIÓN NEURAL", use_container_width=True)
            
            if ingresar:
                if usuario.strip() == "lewis123" and clave.strip() == "201334":
                    st.session_state.autenticado = True
                    st.rerun()
                else:
                    st.error("❌ Credenciales no autorizadas.")

if not st.session_state.autenticado:
    pantalla_login()
    st.stop()

# ==========================================
# 3. CONEXIÓN A SUPABASE
# ==========================================
if "SUPABASE_URL" not in st.secrets or "SUPABASE_KEY" not in st.secrets:
    st.error("⚠️ Falta configurar SUPABASE_URL y SUPABASE_KEY en los 'Secrets' de Streamlit Cloud.")
    st.stop()

URL_LIMPIA = st.secrets["SUPABASE_URL"].strip().split("/rest/v1")[0].rstrip("/")
KEY_LIMPIA = st.secrets["SUPABASE_KEY"].strip()

@st.cache_resource
def conectar_supabase_v6(url: str, key: str) -> Client:
    return create_client(url, key)

supabase = conectar_supabase_v6(URL_LIMPIA, KEY_LIMPIA)

def precargar_datos_supabase():
    try:
        res_m = supabase.table("cuentas_madre").select("id").limit(1).execute()
        if len(res_m.data) == 0:
            madres_iniciales = [
                {"codigo_mad": "MAD-001", "plataforma": "Netflix", "correo_madre": "hussainrazamonthly1@gmail.com", "clave_actual": "sszzxx", "proveedor": "Proveedor Mayorista 1", "fecha_corte": "2026-11-30", "capacidad_cupos": 1, "costo_madre": 7.00, "notas_recuperacion": "https://taikhoan24h.vn"},
                {"codigo_mad": "MAD-002", "plataforma": "Netflix", "correo_madre": "hussainrazamonthly2@gmail.com", "clave_actual": "sszzxx", "proveedor": "Proveedor Mayorista 1", "fecha_corte": "2026-11-30", "capacidad_cupos": 1, "costo_madre": 7.00, "notas_recuperacion": "https://taikhoan24h.vn"},
                {"codigo_mad": "MAD-003", "plataforma": "Netflix", "correo_madre": "hussainrazamonthly3@gmail.com", "clave_actual": "sszzxx", "proveedor": "Proveedor Mayorista 1", "fecha_corte": "2026-11-30", "capacidad_cupos": 1, "costo_madre": 7.00, "notas_recuperacion": "https://taikhoan24h.vn"},
                {"codigo_mad": "MAD-004", "plataforma": "Netflix", "correo_madre": "QGXWL84PTN@gmail.com", "clave_actual": "https://www.netflix.com/unsupported", "proveedor": "Proveedor Mayorista 2", "fecha_corte": "2026-11-30", "capacidad_cupos": 1, "costo_madre": 7.00, "notas_recuperacion": "https://cheapnetf.pages.dev/"},
                {"codigo_mad": "MAD-005", "plataforma": "Netflix", "correo_madre": "taikhoanflix0+29@gmail.com", "clave_actual": "1niemvui", "proveedor": "Proveedor Mayorista 1", "fecha_corte": "2026-12-01", "capacidad_cupos": 1, "costo_madre": 7.00, "notas_recuperacion": "https://taikhoan24h.vn"},
                {"codigo_mad": "MAD-006", "plataforma": "Netflix", "correo_madre": "hussainrazamonthly150@gmail.com", "clave_actual": "1minhem", "proveedor": "Proveedor Mayorista 1", "fecha_corte": "2026-12-02", "capacidad_cupos": 1, "costo_madre": 7.00, "notas_recuperacion": "https://taikhoan24h.vn"},
                {"codigo_mad": "MAD-007", "plataforma": "Netflix", "correo_madre": "Q2CH3KC279@gmail.com", "clave_actual": "https://www.netflix.com/unsupported?nft", "proveedor": "Proveedor Mayorista 2", "fecha_corte": "2026-12-03", "capacidad_cupos": 1, "costo_madre": 7.00, "notas_recuperacion": "https://cheapnetf.pages.dev/"},
                {"codigo_mad": "MAD-008", "plataforma": "Netflix", "correo_madre": "FQBDW6QLJ5@gmail.com", "clave_actual": "https://www.netflix.com/tv2?nftoken=Bgi", "proveedor": "Proveedor Mayorista 2", "fecha_corte": "2026-12-03", "capacidad_cupos": 1, "costo_madre": 7.00, "notas_recuperacion": "https://cheapnetf.pages.dev/"},
                {"codigo_mad": "MAD-009", "plataforma": "Disney+", "correo_madre": "dsntrapflix002@seiyafuzyom.com", "clave_actual": "azulito113", "proveedor": "Panel", "fecha_corte": "2026-12-06", "capacidad_cupos": 5, "costo_madre": 10.00, "notas_recuperacion": ""}
            ]
            supabase.table("cuentas_madre").insert(madres_iniciales).execute()

        res_v = supabase.table("ventas").select("id").limit(1).execute()
        if len(res_v.data) == 0:
            ventas_iniciales = [
                {"codigo_vta": "VTA-001", "cliente": "YOJANY", "whatsapp": "51952529351", "plataforma": "Netflix", "correo_cuenta": "hussainrazamonthly1@gmail.com", "clave_acceso": "sszzxx", "perfil": "Perfil 5 - ######", "pin": "1122", "dispositivo": "Smart TV", "fecha_venta": "2026-10-31", "fecha_vencimiento": "2026-11-30", "precio_venta": 12.00, "costo_prop": 7.00, "metodo_pago": "Yape", "estado_pago": "Pagado", "notas_2fa": "Cliente Nuevo"},
                {"codigo_vta": "VTA-002", "cliente": "RICARDO", "whatsapp": "51959538866", "plataforma": "Netflix", "correo_cuenta": "hussainrazamonthly2@gmail.com", "clave_acceso": "sszzxx", "perfil": "Perfil 5 - ######", "pin": "-", "dispositivo": "Celular / Laptop", "fecha_venta": "2026-10-31", "fecha_vencimiento": "2026-11-30", "precio_venta": 13.00, "costo_prop": 7.00, "metodo_pago": "Plin", "estado_pago": "Pagado", "notas_2fa": "Cliente Nuevo"},
                {"codigo_vta": "VTA-003", "cliente": "LIZ - RIC", "whatsapp": "51928268758", "plataforma": "Netflix", "correo_cuenta": "hussainrazamonthly3@gmail.com", "clave_acceso": "sszzxx", "perfil": "Perfil 1 - Liz", "pin": "1122", "dispositivo": "Tablet", "fecha_venta": "2026-10-31", "fecha_vencimiento": "2026-11-30", "precio_venta": 12.00, "costo_prop": 7.00, "metodo_pago": "Yape", "estado_pago": "Pagado", "notas_2fa": "Cliente Nuevo"},
                {"codigo_vta": "VTA-004", "cliente": "JAVIER", "whatsapp": "51972174896", "plataforma": "Netflix", "correo_cuenta": "QGXWL84PTN@gmail.com", "clave_acceso": "https://www.netflix.com/unsupported", "perfil": "Perfil 4 - Javi", "pin": "-", "dispositivo": "Celular", "fecha_venta": "2026-10-31", "fecha_vencimiento": "2026-11-30", "precio_venta": 13.00, "costo_prop": 6.70, "metodo_pago": "Yape", "estado_pago": "Pagado", "notas_2fa": "Cliente Nuevo | QGXWL84PTN - https://www.netflix"},
                {"codigo_vta": "VTA-005", "cliente": "ENZO", "whatsapp": "51918664028", "plataforma": "Netflix", "correo_cuenta": "taikhoanflix0+29@gmail.com", "clave_acceso": "1niemvui", "perfil": "Perfil 1 - ######", "pin": "-", "dispositivo": "Celular", "fecha_venta": "2026-11-01", "fecha_vencimiento": "2026-12-01", "precio_venta": 13.00, "costo_prop": 7.00, "metodo_pago": "Yape", "estado_pago": "Pagado", "notas_2fa": "Cliente Nuevo"},
                {"codigo_vta": "VTA-006", "cliente": "BRISSA", "whatsapp": "51993464296", "plataforma": "Netflix", "correo_cuenta": "hussainrazamonthly150@gmail.com", "clave_acceso": "1minhem", "perfil": "Perfil 1 - ######", "pin": "1122", "dispositivo": "Celular", "fecha_venta": "2026-11-02", "fecha_vencimiento": "2026-12-02", "precio_venta": 13.00, "costo_prop": 7.00, "metodo_pago": "Yape", "estado_pago": "Pagado", "notas_2fa": "Cliente Nuevo"},
                {"codigo_vta": "VTA-007", "cliente": "ROGER", "whatsapp": "51983645735", "plataforma": "Netflix", "correo_cuenta": "Q2CH3KC279@gmail.com", "clave_acceso": "https://www.netflix.com/unsupported?nft", "perfil": "Perfil 1 - ######", "pin": "-", "dispositivo": "Tablet", "fecha_venta": "2026-11-03", "fecha_vencimiento": "2026-12-03", "precio_venta": 13.00, "costo_prop": 6.70, "metodo_pago": "Yape", "estado_pago": "Pagado", "notas_2fa": "Cliente Nuevo | QGXWL84PTN - https://www.netflix"},
                {"codigo_vta": "VTA-008", "cliente": "JUNIOR", "whatsapp": "51917838120", "plataforma": "Netflix", "correo_cuenta": "FQBDW6QLJ5@gmail.com", "clave_acceso": "https://www.netflix.com/tv2?nftoken=Bgi", "perfil": "Perfil 2 - ######", "pin": "-", "dispositivo": "TV", "fecha_venta": "2026-11-03", "fecha_vencimiento": "2026-12-03", "precio_venta": 13.00, "costo_prop": 6.70, "metodo_pago": "Yape", "estado_pago": "Pagado", "notas_2fa": "Cliente Nuevo | QGXWL84PTN - https://www.netflix"},
                {"codigo_vta": "VTA-009", "cliente": "JUNIOR", "whatsapp": "51917838120", "plataforma": "Disney+", "correo_cuenta": "dsntrapflix002@seiyafuzyom.com", "clave_acceso": "azulito113", "perfil": "Perfil 2 - Junior", "pin": "2233", "dispositivo": "TV", "fecha_venta": "2026-11-06", "fecha_vencimiento": "2026-12-06", "precio_venta": 10.00, "costo_prop": 10.00, "metodo_pago": "Yape", "estado_pago": "Pagado", "notas_2fa": "Cliente Nuevo"}
            ]
            supabase.table("ventas").insert(ventas_iniciales).execute()
    except Exception as e:
        st.error(f"⚠️ Error al inicializar tablas en Supabase: {e}")
        st.stop()

precargar_datos_supabase()

# ==========================================
# 4. ESTÉTICA FUTURISTA IA Y MENÚ LATERAL
# ==========================================
st.sidebar.markdown("## 🤖 **OMNICAST AI**")
st.sidebar.caption("🟢 Neural Cloud Activo | Operador: **lewis123**")

modo_tema = st.sidebar.toggle("☀️ Modo Claro Ejecutivo", value=False)

if modo_tema:
    bg_card = "linear-gradient(135deg, #ffffff, #f1f5f9)"
    bg_hud = "linear-gradient(135deg, #f8fafc, #e2e8f0)"
    text_card = "#0F172A"
    sub_card = "#475569"
    border_hud = "rgba(14, 165, 233, 0.4)"
    creds_bg = "#e2e8f0"
    creds_text = "#0f172a"
else:
    bg_card = "linear-gradient(135deg, rgba(15, 23, 42, 0.92), rgba(9, 13, 22, 0.96))"
    bg_hud = "radial-gradient(circle at top right, rgba(0, 240, 255, 0.12), rgba(15, 23, 42, 0.95))"
    text_card = "#F8FAFC"
    sub_card = "#94A3B8"
    border_hud = "rgba(0, 240, 255, 0.32)"
    creds_bg = "rgba(6, 10, 18, 0.85)"
    creds_text = "#38BDF8"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800&family=JetBrains+Mono:wght@400;600&family=Inter:wght@400;600;700&display=swap');

    .ai-banner {{
        background: {bg_hud};
        border: 1px solid {border_hud};
        border-left: 5px solid #00F0FF;
        border-radius: 16px;
        padding: 18px 22px;
        margin-bottom: 20px;
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.12);
        color: {text_card};
    }}
    .ai-banner-title {{
        font-family: 'Orbitron', sans-serif;
        font-size: 14px;
        color: #00F0FF;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        font-weight: 800;
        margin-bottom: 6px;
    }}
    .ai-banner-text {{
        font-size: 14.5px;
        color: {text_card};
        line-height: 1.5;
    }}
    .metric-card {{
        background: {bg_card};
        border: 1px solid {border_hud};
        border-left: 4px solid #00F0FF;
        padding: 16px 18px;
        border-radius: 14px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
        color: {text_card};
        margin-bottom: 12px;
    }}
    .metric-title {{
        font-size: 11.5px;
        color: {sub_card};
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
    }}
    .metric-value {{
        font-family: 'Orbitron', sans-serif;
        font-size: 24px;
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
    .card-blue {{ border-left-color: #00F0FF !important; }}
    .card-yellow {{ border-left-color: #F59E0B !important; }}
    .card-purple {{ border-left-color: #A855F7 !important; }}

    /* TARJETAS HOLOGRÁFICAS IA PARA CADA REGISTRO */
    .holo-card {{
        background: {bg_card};
        border: 1px solid {border_hud};
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 18px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3), inset 0 0 15px rgba(0, 240, 255, 0.04);
        transition: all 0.25s ease;
        color: {text_card};
    }}
    .holo-card:hover {{
        transform: translateY(-3px);
        border-color: #00F0FF;
        box-shadow: 0 10px 28px rgba(0, 240, 255, 0.18);
    }}
    .holo-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
    }}
    .holo-client {{
        font-family: 'Orbitron', sans-serif;
        font-size: 17px;
        font-weight: 800;
        color: {text_card};
    }}
    .holo-id {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        padding: 3px 8px;
        border-radius: 6px;
        background: rgba(168, 85, 247, 0.2);
        color: #C084FC;
        border: 1px solid rgba(168, 85, 247, 0.4);
    }}
    .holo-plat {{
        display: inline-block;
        font-size: 12.5px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 8px;
        background: rgba(0, 240, 255, 0.14);
        color: #00F0FF;
        border: 1px solid rgba(0, 240, 255, 0.3);
        margin-bottom: 10px;
    }}
    .holo-creds {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        background: {creds_bg};
        color: {creds_text};
        padding: 10px 12px;
        border-radius: 10px;
        border: 1px solid rgba(56, 189, 248, 0.2);
        margin: 8px 0;
        line-height: 1.55;
        word-break: break-all;
    }}
    .energy-bar-bg {{
        width: 100%;
        height: 7px;
        background: rgba(148, 163, 184, 0.2);
        border-radius: 99px;
        overflow: hidden;
        margin: 8px 0 4px 0;
    }}
    .wa-btn-row {{
        display: flex;
        gap: 6px;
        margin-top: 12px;
    }}
    .wa-btn {{
        flex: 1;
        text-align: center;
        padding: 8px 6px;
        border-radius: 9px;
        font-size: 12px;
        font-weight: 700;
        text-decoration: none !important;
        transition: all 0.2s ease;
        border: 1px solid rgba(255,255,255,0.15);
    }}
    .wa-accesos {{
        background: linear-gradient(135deg, #0284C7, #0369A1);
        color: #FFFFFF !important;
    }}
    .wa-cobrar {{
        background: linear-gradient(135deg, #059669, #047857);
        color: #FFFFFF !important;
    }}
    .wa-clave {{
        background: linear-gradient(135deg, #7C3AED, #6D28D9);
        color: #FFFFFF !important;
    }}
    .wa-btn:hover {{
        filter: brightness(1.2);
        transform: scale(1.03);
    }}

    /* BOTONES GRANDES DE NAVEGACIÓN LATERAL */
    section[data-testid="stSidebar"] div.stButton > button {{
        width: 100%;
        min-height: 54px !important;
        padding: 12px 16px !important;
        font-size: 16.5px !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        margin-bottom: 7px !important;
        display: flex !important;
        justify-content: flex-start !important;
        text-align: left !important;
        transition: all 0.2s ease-in-out !important;
    }}
    section[data-testid="stSidebar"] div.stButton > button p {{
        font-size: 16px !important;
        font-weight: 700 !important;
    }}
</style>
""", unsafe_allow_html=True)

st.sidebar.divider()
st.sidebar.markdown("### 🧭 Módulos del Sistema")

OPCIONES_MENU = [
    "📲 Registros y Central IA",
    "📊 Dashboard y Ganancias",
    "➕ Registrar Venta / Perfil",
    "🏦 Cuentas Madre y Cupos",
    "🔐 Editar / Renovar / Claves",
    "⚙️ Respaldo en Excel"
]

for item in OPCIONES_MENU:
    es_activo = (st.session_state.menu_activo == item)
    if st.sidebar.button(
        item,
        key=f"nav_{item}",
        type="primary" if es_activo else "secondary",
        use_container_width=True
    ):
        st.session_state.menu_activo = item
        st.rerun()

menu = st.session_state.menu_activo

st.sidebar.divider()
if st.sidebar.button("🔒 Cerrar Sesión", use_container_width=True):
    st.session_state.autenticado = False
    st.rerun()

PLATAFORMAS = ["Netflix", "Disney+", "Prime Video", "HBO Max", "Crunchyroll", "Spotify", "YouTube Premium", "Canva Pro", "ChatGPT Plus", "Paramount+", "Vix+", "Apple TV+"]

MESES_ES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

# ==========================================
# 5. FUNCIONES DE DATOS Y GENERADOR WHATSAPP SIN ERROR DE EMOJIS
# ==========================================
def generar_link_whatsapp(telefono_raw: str, mensaje: str) -> str:
    """
    Usa api.whatsapp.com/send con codificación UTF-8 estricta e iconografía
    universal BMP para que NUNCA aparezcan rombos '' en WhatsApp Web, PC ni móvil.
    """
    tel = ''.join(filter(str.isdigit, str(telefono_raw)))
    texto_codificado = urllib.parse.quote(mensaje.encode('utf-8'), safe='')
    return f"https://api.whatsapp.com/send?phone={tel}&text={texto_codificado}"

def construir_mensajes_cliente(r) -> tuple:
    # Usamos símbolos Unicode universales (BMP: ⚡, ✨, ✉️, ❖, ▸, ✅, ⚠️) que jamás se rompen en Windows/Web
    msg_accesos = (
        f"⚡ *OMNICAST AI | DATOS DE ACCESO* ⚡\n\n"
        f"Hola *{r['cliente']}* ✨, aquí tienes los datos de acceso de tu cuenta *{r['plataforma']}*:\n\n"
        f"❖ *Correo:* {r['correo_cuenta']}\n"
        f"❖ *Clave:* {r['clave_acceso']}\n"
        f"❖ *Perfil:* {r['perfil']}\n"
        f"❖ *PIN:* {r['pin']}\n"
        f"❖ *Dispositivo:* {r['dispositivo']}\n"
        f"❖ *Vencimiento:* {r['fecha_vencimiento']}\n\n"
        f"✅ *¡Que lo disfrutes!*"
    )

    msg_cobro = (
        f"⚡ *OMNICAST AI | AVISO DE VENCIMIENTO* ⚡\n\n"
        f"Hola *{r['cliente']}* ✨, te recordamos que tu suscripción de *{r['plataforma']}* ({r['perfil']}) "
        f"vence el *{r['fecha_vencimiento']}* ({r['estado_texto']}).\n\n"
        f"▸ *Monto de renovación:* S/ {r['precio_venta']:.2f}\n"
        f"▸ *Medios de pago:* Yape / Plin\n\n"
        f"✅ Confírmanos por aquí para mantener activo tu perfil. ¡Gracias!"
    )

    msg_actualizar = (
        f"⚡ *OMNICAST AI | ACTUALIZACIÓN DE ACCESO* ⚡\n\n"
        f"Hola *{r['cliente']}* ✨, hemos actualizado las credenciales de tu cuenta *{r['plataforma']}*:\n\n"
        f"❖ *Correo:* {r['correo_cuenta']}\n"
        f"❖ *Nueva Clave:* {r['clave_acceso']}\n"
        f"❖ *Perfil:* {r['perfil']} (PIN: {r['pin']})\n\n"
        f"✅ Cualquier consulta estamos atentos."
    )

    return (
        generar_link_whatsapp(r['whatsapp'], msg_accesos),
        generar_link_whatsapp(r['whatsapp'], msg_cobro),
        generar_link_whatsapp(r['whatsapp'], msg_actualizar),
        msg_accesos
    )

def cargar_ventas():
    try:
        res = supabase.table("ventas").select("*").execute()
        df = pd.DataFrame(res.data)
    except Exception:
        df = pd.DataFrame()

    if not df.empty:
        hoy = pd.to_datetime(date.today())
        df['precio_venta'] = pd.to_numeric(df['precio_venta'], errors='coerce').fillna(0.0)
        df['costo_prop'] = pd.to_numeric(df['costo_prop'], errors='coerce').fillna(0.0)
        df['fecha_venta_dt'] = pd.to_datetime(df['fecha_venta'])
        df['fecha_vencimiento_dt'] = pd.to_datetime(df['fecha_vencimiento'])
        df['dias_restantes'] = (df['fecha_vencimiento_dt'] - hoy).dt.days
        df['ganancia_neta'] = df['precio_venta'] - df['costo_prop']
        
        df['mes_anio'] = df['fecha_venta_dt'].dt.strftime('%Y-%m')
        df['mes_nombre'] = df['fecha_venta_dt'].apply(lambda d: f"{MESES_ES[d.month]} {d.year}")
        
        def semaforo(dias):
            if dias < 0:
                return f"🔴 VENCIDO ({dias}d)"
            elif dias <= 5:
                return f"🟡 POR VENCER ({dias}d)"
            else:
                return f"🟢 ACTIVO ({dias}d)"

        def texto_limpio(dias):
            if dias < 0:
                return f"Vencido hace {abs(dias)} días"
            elif dias == 0:
                return "Vence Hoy"
            else:
                return f"Quedan {dias} días"
        
        df['alerta'] = df['dias_restantes'].apply(semaforo)
        df['estado_texto'] = df['dias_restantes'].apply(texto_limpio)
        df = df.sort_values(by='dias_restantes', ascending=True)
    return df

def cargar_madres():
    try:
        res_m = supabase.table("cuentas_madre").select("*").execute()
        res_v = supabase.table("ventas").select("*").execute()
        df_m = pd.DataFrame(res_m.data)
        df_v = pd.DataFrame(res_v.data)
    except Exception:
        df_m = pd.DataFrame()
        df_v = pd.DataFrame()
    
    if not df_m.empty:
        hoy = pd.to_datetime(date.today())
        df_m['capacidad_cupos'] = pd.to_numeric(df_m['capacidad_cupos'], errors='coerce').fillna(1).astype(int)
        df_m['costo_madre'] = pd.to_numeric(df_m['costo_madre'], errors='coerce').fillna(0.0)
        df_m['dias_corte'] = (pd.to_datetime(df_m['fecha_corte']) - hoy).dt.days
        
        ocupados_list = []
        ingresos_list = []
        for _, row in df_m.iterrows():
            if not df_v.empty:
                df_v['precio_venta'] = pd.to_numeric(df_v['precio_venta'], errors='coerce').fillna(0.0)
                ventas_cuenta = df_v[df_v['correo_cuenta'].astype(str).str.lower() == str(row['correo_madre']).lower()]
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
        df_m = df_m.sort_values(by='id', ascending=True)
    return df_m

# ==========================================
# MÓDULO 1: REGISTROS Y CENTRAL IA (INTERFAZ FUTURISTA)
# ==========================================
if menu == "📲 Registros y Central IA":
    st.title("🤖 Central Neural de Suscripciones y WhatsApp IA")
    df = cargar_ventas()
    
    if not df.empty:
        # 1. ASISTENTE IA DE DIAGNÓSTICO EN TIEMPO REAL
        total_cli = len(df)
        activos_cli = len(df[df['dias_restantes'] > 5])
        por_vencer_cli = len(df[(df['dias_restantes'] >= 0) & (df['dias_restantes'] <= 5)])
        vencidos_cli = len(df[df['dias_restantes'] < 0])
        utilidad_total = df['ganancia_neta'].sum()

        if vencidos_cli > 0 or por_vencer_cli > 0:
            nombres_urgentes = ", ".join(df[df['dias_restantes'] <= 5]['cliente'].head(4).tolist())
            recomendacion_ia = f"⚠️ <b>Prioridad IA:</b> Tienes <b>{vencidos_cli} vencidos</b> y <b>{por_vencer_cli} por vencer</b>. Se sugiere enviar aviso de cobro hoy a: <b>{nombres_urgentes}</b>."
        else:
            recomendacion_ia = "✅ <b>Diagnóstico IA Óptimo:</b> El 100% de tu cartera se encuentra con vigencia saludable superior a 5 días."

        st.markdown(f"""
        <div class="ai-banner">
            <div class="ai-banner-title">⚡ OMNICAST NEURAL ASSISTANT // ANÁLISIS EN TIEMPO REAL</div>
            <div class="ai-banner-text">
                Monitoreando <b>{total_cli} suscripciones registradas</b> ({activos_cli} activas) con una utilidad neta acumulada de <b>S/ {utilidad_total:.2f}</b>.<br>
                {recomendacion_ia}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2. PANEL DE FILTROS FUTURISTA
        f1, f2, f3, f4, f5 = st.columns([1.1, 1.2, 1, 1.4, 1.3])
        with f1:
            filtro_plat = st.selectbox("📺 Plataforma:", ["Todas"] + PLATAFORMAS)
        with f2:
            filtro_estado = st.selectbox("🚦 Estado Neural:", ["Todos", "🟢 Activos (>5d)", "🟡 Por Vencer (0-5d)", "🔴 Vencidos (<0d)"])
        with f3:
            filtro_mes = st.selectbox("📅 Mes Venta:", ["Todos"] + sorted(df['mes_anio'].unique().tolist(), reverse=True))
        with f4:
            buscar_txt = st.text_input("🔍 Escáner IA (Cliente / Correo / Perfil):")
        with f5:
            modo_vista = st.selectbox("👁️ Modo Visualización:", ["🎴 Tarjetas IA + Matriz", "🎴 Solo Tarjetas Holográficas", "📋 Solo Matriz Cuántica"])
            
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
                df['cliente'].astype(str).str.contains(buscar_txt, case=False, na=False) |
                df['correo_cuenta'].astype(str).str.contains(buscar_txt, case=False, na=False) |
                df['perfil'].astype(str).str.contains(buscar_txt, case=False, na=False)
            ]

        btn_accesos, btn_cobrar, btn_actualizar, textos_copia = [], [], [], []
        for _, r in df.iterrows():
            l_acc, l_cob, l_act, txt_c = construir_mensajes_cliente(r)
            btn_accesos.append(l_acc)
            btn_cobrar.append(l_cob)
            btn_actualizar.append(l_act)
            textos_copia.append(txt_c)

        df['btn_accesos'] = btn_accesos
        df['btn_cobrar'] = btn_cobrar
        df['btn_actualizar'] = btn_actualizar
        df['texto_copia'] = textos_copia
        df['energia_vida'] = df['dias_restantes'].clip(lower=0, upper=30)

        # 3. VISTA DE TARJETAS HOLOGRÁFICAS IA
        if "🎴" in modo_vista:
            st.subheader(f"🎴 Nodos de Clientes Activos ({len(df)} registros)")
            cols = st.columns(3)
            for idx, (_, r) in enumerate(df.iterrows()):
                dias = int(r['dias_restantes'])
                porc_barra = max(0, min(100, int((dias / 30) * 100)))
                if dias < 0:
                    color_estado = "#EF4444"
                elif dias <= 5:
                    color_estado = "#F59E0B"
                else:
                    color_estado = "#10B981"

                cliente_safe = html.escape(str(r['cliente']))
                cod_safe = html.escape(str(r['codigo_vta']))
                plat_safe = html.escape(str(r['plataforma']))
                disp_safe = html.escape(str(r['dispositivo']))
                correo_safe = html.escape(str(r['correo_cuenta']))
                clave_safe = html.escape(str(r['clave_acceso']))
                perfil_safe = html.escape(str(r['perfil']))
                pin_safe = html.escape(str(r['pin']))

                with cols[idx % 3]:
                    st.markdown(f"""
                    <div class="holo-card" style="border-top: 3px solid {color_estado};">
                        <div class="holo-header">
                            <span class="holo-client">{cliente_safe}</span>
                            <span class="holo-id">{cod_safe}</span>
                        </div>
                        <div>
                            <span class="holo-plat">📺 {plat_safe} • {disp_safe}</span>
                            <span style="float:right; font-size:12px; font-weight:700; color:{color_estado};">{r['alerta']}</span>
                        </div>
                        <div class="holo-creds">
                            📧 <b>Correo:</b> {correo_safe}<br>
                            🔑 <b>Clave:</b> {clave_safe}<br>
                            👤 <b>Perfil:</b> {perfil_safe} &nbsp;|&nbsp; 📌 <b>PIN:</b> {pin_safe}
                        </div>
                        <div style="display:flex; justify-content:space-between; font-size:11.5px; color:#94A3B8; margin-top:4px;">
                            <span>📅 Vence: <b>{r['fecha_vencimiento']}</b></span>
                            <span>💵 Ganancia: <b style="color:#10B981;">S/ {r['ganancia_neta']:.2f}</b></span>
                        </div>
                        <div class="energy-bar-bg">
                            <div style="width:{porc_barra}%; height:100%; background:{color_estado};"></div>
                        </div>
                        <div class="wa-btn-row">
                            <a href="{r['btn_accesos']}" target="_blank" class="wa-btn wa-accesos">⚡ Accesos</a>
                            <a href="{r['btn_cobrar']}" target="_blank" class="wa-btn wa-cobrar">💰 Cobrar</a>
                            <a href="{r['btn_actualizar']}" target="_blank" class="wa-btn wa-clave">🔄 Clave</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        # 4. VISTA DE MATRIZ CUÁNTICA (TABLA INTERACTIVA CON BARRA DE ENERGÍA)
        if "Matriz" in modo_vista:
            st.divider()
            st.subheader("📋 Matriz Cuántica de Registros (Vista Tabular)")
            st.dataframe(
                df[['codigo_vta', 'cliente', 'whatsapp', 'plataforma', 'correo_cuenta', 'clave_acceso', 'perfil', 'pin', 'dispositivo', 'fecha_vencimiento', 'alerta', 'energia_vida', 'precio_venta', 'ganancia_neta', 'btn_accesos', 'btn_cobrar', 'btn_actualizar']],
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
                    "alerta": "Semáforo IA",
                    "energia_vida": st.column_config.ProgressColumn("Nivel Vigencia", min_value=0, max_value=30, format="%d días"),
                    "precio_venta": st.column_config.NumberColumn("Precio", format="S/ %.2f"),
                    "ganancia_neta": st.column_config.NumberColumn("Ganancia", format="S/ %.2f"),
                    "btn_accesos": st.column_config.LinkColumn("Accesos", display_text="⚡ Enviar Datos"),
                    "btn_cobrar": st.column_config.LinkColumn("Cobranza", display_text="💰 Cobrar"),
                    "btn_actualizar": st.column_config.LinkColumn("Soporte", display_text="🔄 Actualizar")
                },
                hide_index=True,
                use_container_width=True
            )

        with st.expander("📋 Copiar Mensaje Manualmente (Con botón de copiado en 1 clic)"):
            sel_copia = st.selectbox("Selecciona el cliente:", df['codigo_vta'] + " - " + df['cliente'] + " (" + df['plataforma'] + ")")
            cod_c = sel_copia.split(" - ")[0]
            fila_c = df[df['codigo_vta'] == cod_c].iloc[0]
            st.code(fila_c['texto_copia'], language="markdown")
    else:
        st.info("No hay registros disponibles.")

# ==========================================
# MÓDULO 2: DASHBOARD Y GANANCIAS MENSUALES
# ==========================================
elif menu == "📊 Dashboard y Ganancias":
    st.title("📊 Panel de Control Financiero y Ganancias Mensuales")
    df_v = cargar_ventas()
    df_m = cargar_madres()
    
    if not df_v.empty:
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
# MÓDULO 3: REGISTRAR NUEVA VENTA EN SUPABASE
# ==========================================
elif menu == "➕ Registrar Venta / Perfil":
    st.title("➕ Registrar Nueva Venta en Supabase")
    df_m = cargar_madres()
    df_v = cargar_ventas()
    
    sig_num = len(df_v) + 1
    cod_sugerido = f"VTA-{sig_num:03d}"
    
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

    with st.form("form_nueva_venta_cloud"):
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
            
        guardar = st.form_submit_button("✅ Guardar Venta en la Nube (Supabase)", use_container_width=True)
        
        if guardar:
            if cliente and whatsapp and len(whatsapp.strip()) >= 9:
                f_venc = f_venta + timedelta(days=int(duracion_dias))
                nuevo_reg = {
                    "codigo_vta": codigo_vta,
                    "cliente": cliente.upper().strip(),
                    "whatsapp": whatsapp.strip(),
                    "plataforma": plataforma,
                    "correo_cuenta": correo_cuenta.strip(),
                    "clave_acceso": clave_acceso.strip(),
                    "perfil": perfil,
                    "pin": pin,
                    "dispositivo": dispositivo,
                    "fecha_venta": str(f_venta),
                    "fecha_vencimiento": str(f_venc),
                    "precio_venta": float(precio_venta),
                    "costo_prop": float(costo_prop),
                    "metodo_pago": metodo_pago,
                    "estado_pago": "Pagado",
                    "notas_2fa": notas_2fa
                }
                supabase.table("ventas").insert(nuevo_reg).execute()
                st.success(f"🎉 ¡Venta **{codigo_vta}** guardada en Supabase para **{cliente.upper()}**! Ganancia neta: **S/ {precio_venta - costo_prop:.2f}**")
            else:
                st.error("⚠️ Ingresa el nombre del cliente y un número de WhatsApp válido.")

# ==========================================
# MÓDULO 4: INVENTARIO DE CUENTAS MADRE
# ==========================================
elif menu == "🏦 Cuentas Madre y Cupos":
    st.title("🏦 Inventario de Cuentas Madre en Supabase")
    df_m = cargar_madres()
    
    with st.expander("➕ Agregar Nueva Cuenta Madre al Inventario", expanded=False):
        sig_mad = f"MAD-{(len(df_m) + 1):03d}"
        with st.form("form_madre_cloud"):
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
                
            if st.form_submit_button("💾 Guardar Cuenta Madre en Supabase", use_container_width=True):
                if m_correo:
                    try:
                        nueva_madre = {
                            "codigo_mad": m_cod,
                            "plataforma": m_plat,
                            "correo_madre": m_correo.strip(),
                            "clave_actual": m_clave.strip(),
                            "proveedor": m_prov,
                            "fecha_corte": str(m_corte),
                            "capacidad_cupos": int(m_cupos),
                            "costo_madre": float(m_costo),
                            "notas_recuperacion": m_notas
                        }
                        supabase.table("cuentas_madre").insert(nueva_madre).execute()
                        st.success("✅ Cuenta Madre guardada en Supabase.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"⚠️ Error al guardar: {e}")

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
    st.title("🔐 Modificar Accesos o Renovar Suscripción en Supabase")
    df = cargar_ventas()
    
    if not df.empty:
        opciones = df['id'].astype(str) + " | " + df['codigo_vta'].fillna('') + " - " + df['cliente'] + " (" + df['plataforma'] + " - " + df['correo_cuenta'] + ")"
        seleccion = st.selectbox("Selecciona el cliente a gestionar:", opciones)
        
        id_sel = int(seleccion.split(" | ")[0])
        row = df[df['id'] == id_sel].iloc[0]
        
        col_r1, col_r2, col_r3 = st.columns([1, 1, 2])
        with col_r1:
            if st.button("🔄 Renovar +30 Días (1 Clic)", use_container_width=True):
                nueva_fecha = pd.to_datetime(row['fecha_vencimiento']).date() + timedelta(days=30)
                supabase.table("ventas").update({
                    "fecha_vencimiento": str(nueva_fecha),
                    "fecha_venta": str(date.today())
                }).eq("id", id_sel).execute()
                st.success(f"✅ Suscripción renovada hasta el {nueva_fecha}!")
                st.rerun()
        with col_r2:
            if st.button("🗑️ Eliminar Registro", type="primary", use_container_width=True):
                supabase.table("ventas").delete().eq("id", id_sel).execute()
                st.warning("Registro eliminado de Supabase.")
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
                
            if st.form_submit_button("💾 Guardar Cambios en Supabase", use_container_width=True):
                datos_act = {
                    "codigo_vta": e_cod,
                    "cliente": e_cliente.upper().strip(),
                    "whatsapp": e_wa.strip(),
                    "plataforma": e_plat,
                    "correo_cuenta": e_correo.strip(),
                    "clave_acceso": e_clave.strip(),
                    "perfil": e_perfil,
                    "pin": e_pin,
                    "dispositivo": e_disp,
                    "fecha_venta": str(e_fventa),
                    "fecha_vencimiento": str(e_fvenc),
                    "precio_venta": float(e_precio),
                    "costo_prop": float(e_costo),
                    "metodo_pago": e_metodo,
                    "notas_2fa": e_notas
                }
                supabase.table("ventas").update(datos_act).eq("id", id_sel).execute()
                st.success("✅ ¡Datos actualizados en Supabase en tiempo real!")
                st.rerun()

# ==========================================
# MÓDULO 6: RESPALDO EN EXCEL / HERRAMIENTAS
# ==========================================
elif menu == "⚙️ Respaldo en Excel":
    st.title("⚙️ Exportar a Excel desde Supabase")
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
