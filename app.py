import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- 1. CONFIGURACIÓN DE PÁGINA Y ESTILO NEÓN ---
st.set_page_config(page_title="Misión 3 - Gestión Estratégica", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0E1117; color: #00FFC8; }
    h1, h2, h3 { color: #FF00E6; text-shadow: 0 0 15px #FF00E6; text-align: center; }
    .stMetric { background-color: #161B22; border: 1px solid #00FFC8; padding: 15px; border-radius: 10px; box-shadow: 0 0 5px #00FFC8; }
    [data-testid="stMetricValue"] { color: #00FFC8; text-shadow: 0 0 5px #00FFC8; }
    .stButton>button { 
        background-color: #FF00E6; color: white; 
        border-radius: 20px; border: none; box-shadow: 0 0 10px #FF00E6; font-weight: bold;
    }
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>select {
        background-color: #161B22; color: #00FFC8; border: 1px solid #00FFC8;
    }
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
st.sidebar.markdown("<h2 style='text-align: left; color: #00FFC8;'>MISIÓN 3</h2>", unsafe_allow_html=True)
area = st.sidebar.selectbox("Módulos de Gestión", 
    ["Dashboard Estratégico", "Emprendimiento", "Vinculación", "Plataformas", "Comunicaciones", "Gestión Administrativa"])

# --- 4. FUNCIONES DE APOYO ---
def guardar_datos(coleccion, data):
    try:
        data["timestamp"] = datetime.now()
        db.collection(coleccion).add(data)
        st.success("✅ Datos enviados a Misión 3 correctamente.")
    except Exception as e:
        st.error(f"Error al guardar: {e}")

# --- 5. MÓDULOS POR ÁREA ---

if area == "Emprendimiento":
    st.header("🚀 Programas de Emprendimiento e Innovación")
    with st.form("form_emp"):
        prog = st.selectbox("Programa", ["Pre-incubación", "Incubación", "Aceleración", "Mentores"])
        c1, c2 = st.columns(2)
        reg = c1.number_input("Total Registrados", min_value=0)
        comp = c2.number_input("Completados (Aplicación)", min_value=0)
        city = st.text_input("Origen por ciudades")
        if st.form_submit_button("Guardar Reporte"):
            guardar_datos("emprendimiento", {"programa": prog, "registrados": reg, "completados": comp, "ciudades": city})

elif area == "Vinculación":
    st.header("🤝 Vinculación y Concurso ATIPAQ")
    with st.form("form_vin"):
        atipaq = st.number_input("Registrados en ATIPAQ", min_value=0)
        st.subheader("Nuevos Aliados Estratégicos")
        c1, c2 = st.columns(2)
        tipo = c1.selectbox("Tipo de Aliado", ["Universidad", "Cámara de Comercio", "Incubadora", "Municipio", "Gobierno Regional", "DER"])
        nombre = c2.text_input("Nombre de la Organización")
        if st.form_submit_button("Registrar Vinculación"):
            guardar_datos("vinculacion", {"atipaq": atipaq, "tipo_aliado": tipo, "nombre_aliado": nombre})

elif area == "Plataformas":
    st.header("💻 Infraestructura Digital y Soporte")
    with st.form("form_plat"):
        plat = st.selectbox("Plataforma", ["Web", "CRM", "Aula Virtual", "App"])
        estado = st.select_slider("Estado", options=["Incidencia", "Mantenimiento", "Operativo"])
        users = st.number_input("Usuarios Activos", min_value=0)
        notas = st.text_area("Detalles técnicos")
        if st.form_submit_button("Actualizar Estado"):
            guardar_datos("plataformas", {"plataforma": plat, "estado": estado, "usuarios": users, "notas": notas})

elif area == "Comunicaciones":
    st.header("📱 Redes Sociales y Audiovisuales")
    with st.form("form_com"):
        red = st.selectbox("Red Social", ["Facebook", "Instagram", "LinkedIn", "TikTok"])
        followers = st.number_input("Nuevos Seguidores", min_value=0)
        pauta = st.number_input("Gasto en Pauta (S/.)", min_value=0.0)
        prod = st.number_input("Producción Audiovisual/Diseño (Piezas)", min_value=0)
        if st.form_submit_button("Guardar Métricas"):
            guardar_datos("comunicaciones", {"red": red, "seguidores": followers, "pauta": pauta, "produccion": prod})

elif area == "Gestión Administrativa":
    st.header("⚙️ Gestión y Presupuesto")
    with st.form("form_ges"):
        presupuesto = st.number_input("Uso del Presupuesto (%)", min_value=0, max_value=100)
        logistica = st.number_input("Solicitudes a Logística", min_value=0)
        viajes = st.number_input("Viajes y Viáticos", min_value=0)
        if st.form_submit_button("Reportar Gestión"):
            guardar_datos("gestion", {"presupuesto": presupuesto, "logistica": logistica, "viajes": viajes})

# --- 6. DASHBOARD ESTRATÉGICO MISIÓN 3 ---
elif area == "Dashboard Estratégico":
    st.title("💡 Dashboard Estratégico Misión 3")
    
    # KPIs Superiores
    m1, m2, m3 = st.columns(3)
    m1.metric("Registrados Totales", "1,850", "+15%")
    m2.metric("Proyectos en Aceleración", "12", "Activos")
    m3.metric("Ejecución Presupuestal", "72%", "En Meta")

    st.markdown("---")
    
    # Gráfico de ejemplo Neon
    c1, c2 = st.columns(2)
    
    df_progs = pd.DataFrame({'Prog': ['Pre-Inc', 'Inc', 'Acel'], 'Cant': [80, 50, 20]})
    fig1 = px.bar(df_progs, x='Prog', y='Cant', title="Evolución de Programas", template="plotly_dark")
    fig1.update_traces(marker_color='#FF00E6') # Rosa Neon
    c1.plotly_chart(fig1, use_container_width=True)
    
    df_aliados = pd.DataFrame({'Tipo': ['Univ', 'Gob', 'Priv'], 'Cant': [15, 10, 8]})
    fig2 = px.pie(df_aliados, values='Cant', names='Tipo', title="Distribución de Aliados", hole=.4, template="plotly_dark")
    fig2.update_traces(marker=dict(colors=['#00FFC8', '#FF00E6', '#00D4FF']))
    c2.plotly_chart(fig2, use_container_width=True)
