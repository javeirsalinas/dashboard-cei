import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- 1. CONFIGURACIÓN DE PÁGINA Y ESTILO NEÓN ---
st.set_page_config(page_title="Misión 3 | Gestión Estratégica", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #000000; color: #00FFC8; }
    h1, h2, h3 { 
        color: #FF00E6 !important; 
        text-shadow: 0 0 15px #FF00E6; 
        font-family: 'Courier New', monospace;
        text-align: center;
    }
    [data-testid="stMetric"] {
        background-color: #0A0A0A;
        border: 1px solid #00FFC8;
        padding: 15px;
        border-radius: 5px;
    }
    .stButton>button { 
        background-color: transparent; color: #FF00E6; 
        border: 2px solid #FF00E6; border-radius: 0px;
        box-shadow: 0 0 10px #FF00E6; font-weight: bold;
    }
    .stButton>button:hover { background-color: #FF00E6; color: black; }
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>select, .stTextArea>div>div>textarea {
        background-color: #111111; color: #00FFC8; border: 1px solid #00FFC8;
    }
    [data-testid="stSidebar"] { background-color: #050505; border-right: 1px solid #FF00E6; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONEXIÓN A FIREBASE ---
if not firebase_admin._apps:
    try:
        fb_dict = dict(st.secrets["firebase"])
        fb_dict["private_key"] = fb_dict["private_key"].replace("\\n", "\n")
        creds = credentials.Certificate(fb_dict)
        firebase_admin.initialize_app(creds)
    except Exception as e:
        st.error(f"Error de conexión: {e}")

db = firestore.client()

# --- 3. NAVEGACIÓN LATERAL ---
st.sidebar.markdown("<h1 style='font-size: 25px; color: #FF00E6;'>MISIÓN 3</h1>", unsafe_allow_html=True)
area = st.sidebar.selectbox("Módulos de Reporte", 
    ["Dashboard Estratégico", "Emprendimiento", "Vinculación", "Plataformas", "Comunicaciones", "Gestión Administrativa"])

# --- 4. FUNCIÓN PARA GUARDAR ---
def enviar_a_mision3(coleccion, data):
    try:
        data["fecha_registro"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.collection(coleccion).add(data)
        st.balloons()
        st.success("🚀 DATOS TRANSMITIDOS A LA CENTRAL MISIÓN 3")
    except Exception as e:
        st.error(f"❌ ERROR EN LA TRANSMISIÓN: {e}")

# --- 5. MÓDULOS DE CAPTURA ---

if area == "Emprendimiento":
    st.header("🚀 PROGRAMAS DE EMPRENDIMIENTO")
    with st.form("form_emp"):
        prog = st.selectbox("Programa", ["Pre-incubación", "Incubación", "Aceleración", "Mentores"])
        c1, c2 = st.columns(2)
        reg = c1.number_input("Total Registrados", min_value=0)
        comp = c2.number_input("Registros Completos (Aplicación)", min_value=0)
        city = st.text_input("Ciudad(es) de Origen")
        if st.form_submit_button("SINCRONIZAR"):
            enviar_a_mision3("emprendimiento", {"programa": prog, "registrados": reg, "completados": comp, "ciudades": city})

elif area == "Vinculación":
    st.header("🤝 VINCULACIÓN Y ATIPAQ")
    with st.form("form_vin"):
        atipaq = st.number_input("Registrados en Concurso ATIPAQ", min_value=0)
        st.subheader("Aliados Estratégicos")
        tipo = st.selectbox("Tipo de Aliado", ["Universidad", "Cámara de Comercio", "Incubadora", "Aceleradora", "Municipio", "Gobierno Regional", "DER"])
        nombre = st.text_input("Nombre de la Institución")
        if st.form_submit_button("GUARDAR ALIANZA"):
            enviar_a_mision3("vinculacion", {"atipaq": atipaq, "tipo_aliado": tipo, "nombre_aliado": nombre})

elif area == "Plataformas":
    st.header("💻 ESTADO DE PLATAFORMAS")
    with st.form("form_plat"):
        plat = st.selectbox("Plataforma", ["Web", "CRM", "Aula Virtual", "App"])
        estado = st.radio("Estado de Operación", ["Operativo", "Mantenimiento", "Incidencia"])
        users = st.number_input("Usuarios Activos / Licencias", min_value=0)
        obs = st.text_area("Detalle de Incidencias")
        if st.form_submit_button("REPORTAR ESTADO"):
            enviar_a_mision3("plataformas", {"plataforma": plat, "estado": estado, "usuarios": users, "notas": obs})

elif area == "Comunicaciones":
    st.header("📱 COMUNICACIONES Y REDES")
    with st.form("form_com"):
        c1, c2 = st.columns(2)
        followers = c1.number_input("Seguidores Totales (Nuevos)", min_value=0)
        pauta = c2.number_input("Inversión en Pauta (S/.)", min_value=0.0)
        
        st.divider()
        c3, c4 = st.columns(2)
        prod = c3.number_input("Piezas de Diseño / Audiovisuales", min_value=0)
        articulos = c4.number_input("Artículos / Notas Publicadas", min_value=0)
        
        eventos = st.text_input("Eventos realizados / Cobertura")
        if st.form_submit_button("ENVIAR MÉTRICAS"):
            enviar_a_mision3("comunicaciones", {
                "seguidores": followers, "gasto_pauta": pauta, 
                "produccion_piezas": prod, "articulos": articulos, "eventos": eventos
            })

elif area == "Gestión Administrativa":
    st.header("⚙️ GESTIÓN Y PRESUPUESTO")
    with st.form("form_ges"):
        presu = st.slider("Uso de Presupuesto (%)", 0, 100, 50)
        c1, c2 = st.columns(2)
        logistica = c1.number_input("Solicitudes a Logística", min_value=0)
        viajes = c2.number_input("Viajes y Viáticos (N°)", min_value=0)
        
        relaciones = st.number_input("Iniciativas con otras Áreas (N°)", min_value=0)
        if st.form_submit_button("FINALIZAR REPORTE GESTIÓN"):
            enviar_a_mision3("gestion", {
                "uso_presupuesto": presu, "logistica": logistica, 
                "viajes_viaticos": viajes, "relaciones_internas": relaciones
            })

# --- 6. DASHBOARD ESTRATÉGICO ---
elif area == "Dashboard Estratégico":
    st.title("💡 DASHBOARD ESTRATÉGICO MISIÓN 3")
    
    # KPIs Rápidos
    m1, m2, m3 = st.columns(3)
    m1.metric("REGISTRADOS", "1,850", "+12%")
    m2.metric("ALIADOS", "45", "ACTIVOS")
    m3.metric("EJECUCIÓN", "72%", "EN META")

    st.markdown("---")
    
    # Gráficos de ejemplo
    c1, c2 = st.columns(2)
    df_chart = pd.DataFrame({'Área': ['Emprendimiento', 'Vinculación', 'Coms'], 'Valor': [40, 30, 20]})
    fig = px.bar(df_chart, x='Área', y='Valor', template="plotly_dark", color_discrete_sequence=['#00FFC8'])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    c1.plotly_chart(fig, use_container_width=True)
    
    st.info("ℹ️ Los gráficos muestran datos históricos una vez se consolide la primera semana de carga.")
