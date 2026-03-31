import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- 1. CONFIGURACIÓN DE PÁGINA Y ESTILO NEÓN EXTREMO ---
st.set_page_config(page_title="Misión 3 | Dashboard Estratégico", layout="wide")

st.markdown("""
    <style>
    /* Fondo Negro Profundo */
    .main { 
        background-color: #000000; 
        color: #00FFC8; 
    }
    
    /* Títulos Neón con Resplandor (Glow) */
    h1, h2, h3 { 
        color: #FF00E6 !important; 
        text-shadow: 0 0 15px #FF00E6, 0 0 5px #FF00E6; 
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Tarjetas de KPIs Estilo Cyber */
    [data-testid="stMetric"] {
        background-color: #0A0A0A;
        border: 1px solid #00FFC8;
        padding: 15px;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0, 255, 200, 0.2);
    }
    
    /* Colores de las métricas */
    [data-testid="stMetricLabel"] { color: #00FFC8 !important; }
    [data-testid="stMetricValue"] { 
        color: #00FFC8 !important; 
        text-shadow: 0 0 8px #00FFC8; 
        font-weight: bold;
    }

    /* Botones Rosa Neón */
    .stButton>button { 
        background-color: transparent; 
        color: #FF00E6; 
        border: 2px solid #FF00E6;
        border-radius: 0px;
        font-weight: bold;
        text-transform: uppercase;
        box-shadow: 0 0 10px #FF00E6;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #FF00E6;
        color: black;
        box-shadow: 0 0 20px #FF00E6;
    }

    /* Inputs y Selectores Dark */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>select {
        background-color: #111111;
        color: #00FFC8;
        border: 1px solid #00FFC8;
    }
    
    /* Sidebar Dark */
    [data-testid="stSidebar"] {
        background-color: #050505;
        border-right: 1px solid #FF00E6;
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
st.sidebar.markdown("<h1 style='font-size: 25px; color: #FF00E6;'>MISIÓN 3</h1>", unsafe_allow_html=True)
area = st.sidebar.selectbox("Módulos", 
    ["Dashboard Estratégico", "Emprendimiento", "Vinculación", "Plataformas", "Comunicaciones", "Gestión"])

# --- 4. FUNCIÓN PARA GUARDAR ---
def guardar_datos(coleccion, data):
    try:
        data["timestamp"] = datetime.now()
        db.collection(coleccion).add(data)
        st.balloons()
        st.success("✅ DATOS TRANSMITIDOS A MISIÓN 3")
    except Exception as e:
        st.error(f"ERROR EN LA TRANSMISIÓN: {e}")

# --- 5. LÓGICA DE MÓDULOS ---

if area == "Dashboard Estratégico":
    st.title("⚡ DASHBOARD ESTRATÉGICO")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("REGISTRADOS", "1,850", "+15%")
    col2.metric("ACELERACIÓN", "12", "ACTIVOS")
    col3.metric("PRESUPUESTO", "72%", "EJECUTADO")
    col4.metric("ALIADOS", "45", "NUEVOS")

    st.markdown("<hr style='border: 1px solid #FF00E6;'>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    
    # Gráfico 1: Barras Verde Neón
    df_progs = pd.DataFrame({'Prog': ['Pre-Inc', 'Inc', 'Acel'], 'Cant': [80, 50, 20]})
    fig1 = px.bar(df_progs, x='Prog', y='Cant', title="EVOLUCIÓN DE PROGRAMAS", 
                 template="plotly_dark", color_discrete_sequence=['#00FFC8'])
    fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#00FFC8")
    c1.plotly_chart(fig1, use_container_width=True)
    
    # Gráfico 2: Pie Rosa Neón
    df_aliados = pd.DataFrame({'Tipo': ['Univ', 'Gob', 'Priv'], 'Cant': [15, 10, 8]})
    fig2 = px.pie(df_aliados, values='Cant', names='Tipo', title="DISTRIBUCIÓN DE ALIADOS", 
                 hole=.4, template="plotly_dark", color_discrete_sequence=['#FF00E6', '#00FFC8', '#00D4FF'])
    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="#00FFC8")
    c2.plotly_chart(fig2, use_container_width=True)

elif area == "Emprendimiento":
    st.header("🚀 MÓDULO EMPRENDIMIENTO")
    with st.form("form_emp"):
        prog = st.selectbox("Programa", ["Pre-incubación", "Incubación", "Aceleración", "Mentores"])
        c1, c2 = st.columns(2)
        reg = c1.number_input("Total Registrados", min_value=0)
        comp = c2.number_input("Completados", min_value=0)
        city = st.text_input("Ciudad(es)")
        if st.form_submit_button("SINCRONIZAR"):
            guardar_datos("emprendimiento", {"programa": prog, "registrados": reg, "completados": comp, "ciudades": city})

elif area == "Vinculación":
    st.header("🤝 MÓDULO VINCULACIÓN")
    with st.form("form_vin"):
        atipaq = st.number_input("Registrados ATIPAQ", min_value=0)
        tipo = st.selectbox("Tipo de Aliado", ["Universidad", "Cámara", "Municipio", "Gobierno", "DER"])
        nombre = st.text_input("Nombre de la Organización")
        if st.form_submit_button("GUARDAR ALIANZA"):
            guardar_datos("vinculacion", {"atipaq": atipaq, "tipo": tipo, "nombre": nombre})

# Los demás módulos se pueden agregar siguiendo este mismo patrón estético.
