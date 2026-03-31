import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- 1. CONFIGURACIÓN DE PÁGINA Y ESTILO PREMIUM ---
st.set_page_config(page_title="Misión 3 | Gestión Estratégica", layout="wide")

st.markdown("""
    <style>
    /* Fondo General y Texto */
    .main { background-color: #F8FAFC; color: #1E293B; }
    
    /* Títulos con tipografía limpia */
    h1, h2, h3 { color: #0F172A; font-family: 'Inter', sans-serif; font-weight: 700; }
    
    /* Tarjetas de métricas (KPIs) */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Botones Premium */
    .stButton>button { 
        background-color: #2563EB; /* Azul Corporativo */
        color: white; 
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1D4ED8;
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3);
    }

    /* Inputs y Selectores */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>select {
        background-color: #FFFFFF;
        color: #1E293B;
        border: 1px solid #CBD5E1;
        border-radius: 6px;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #F1F5F9;
        border-right: 1px solid #E2E8F0;
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
st.sidebar.markdown("<h2 style='text-align: left; color: #1E3A8A;'>MISIÓN 3</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='font-size: 0.8rem; color: #64748B;'>PLATAFORMA DE GESTIÓN V1.0</p>", unsafe_allow_html=True)
area = st.sidebar.selectbox("Módulos", 
    ["Dashboard Estratégico", "Emprendimiento", "Vinculación", "Plataformas", "Comunicaciones", "Gestión Administrativa"])

# --- 4. FUNCIÓN PARA GUARDAR ---
def guardar_datos(coleccion, data):
    try:
        data["timestamp"] = datetime.now()
        db.collection(coleccion).add(data)
        st.toast("✅ Datos sincronizados con éxito", icon='🚀')
    except Exception as e:
        st.error(f"Error al guardar: {e}")

# --- 5. LÓGICA DE MÓDULOS (FORMULARIOS) ---

if area == "Dashboard Estratégico":
    st.title("📊 Dashboard Estratégico Misión 3")
    
    # KPIs Superiores con colores Azul/Gris
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Registrados", "1,850", "+15%", delta_color="normal")
    m2.metric("Aceleración", "12", "En curso")
    m3.metric("Presupuesto", "72%", "Ejecutado")
    m4.metric("Aliados", "45", "+3")

    st.markdown("---")
    
    # Gráficos con paleta Azul/Gris
    c1, c2 = st.columns(2)
    
    # Gráfico 1: Barras Azules
    df_progs = pd.DataFrame({'Prog': ['Pre-Inc', 'Inc', 'Acel'], 'Cant': [80, 50, 20]})
    fig1 = px.bar(df_progs, x='Prog', y='Cant', title="Evolución de Programas", 
                 template="plotly_white", color_discrete_sequence=['#3B82F6'])
    fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    c1.plotly_chart(fig1, use_container_width=True)
    
    # Gráfico 2: Pie en Azules y Grises
    df_aliados = pd.DataFrame({'Tipo': ['Univ', 'Gob', 'Priv'], 'Cant': [15, 10, 8]})
    fig2 = px.pie(df_aliados, values='Cant', names='Tipo', title="Distribución de Aliados", 
                 hole=.4, template="plotly_white", color_discrete_sequence=['#1E3A8A', '#64748B', '#94A3B8'])
    c2.plotly_chart(fig2, use_container_width=True)

# [Los demás módulos (Emprendimiento, Vinculación, etc.) se mantienen con la misma lógica pero heredan el estilo visual Premium]
elif area == "Emprendimiento":
    st.header("🚀 Programas de Emprendimiento")
    with st.form("form_emp"):
        prog = st.selectbox("Programa", ["Pre-incubación", "Incubación", "Aceleración", "Mentores"])
        c1, c2 = st.columns(2)
        reg = c1.number_input("Total Registrados", min_value=0)
        comp = c2.number_input("Completados", min_value=0)
        city = st.text_input("Ciudad(es)")
        if st.form_submit_button("Sincronizar Datos"):
            guardar_datos("emprendimiento", {"programa": prog, "registrados": reg, "completados": comp, "ciudades": city})

# (He omitido el resto de los módulos por brevedad, pero conservan su estructura original)
