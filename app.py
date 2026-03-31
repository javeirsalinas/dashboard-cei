import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- 1. CONFIGURACIÓN Y ESTILO EXECUTIVE ---
st.set_page_config(page_title="Misión 3 | Inteligencia Estratégica", layout="wide")

st.markdown("""
    <style>
    /* Fondo Azul Grisáceo Muy Oscuro */
    .main { 
        background-color: #0F172A; 
        color: #E2E8F0; 
        font-family: 'Inter', sans-serif;
    }
    
    /* Títulos Ejecutivos en Azul Acero */
    h1, h2 { 
        color: #F8FAFC !important; 
        font-weight: 700 !important;
        letter-spacing: -0.025em;
        text-align: left;
        border-bottom: 2px solid #334155;
        padding-bottom: 10px;
    }
    
    /* Tarjetas de KPIs Modernas */
    [data-testid="stMetric"] {
        background-color: #1E293B;
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Botones en Azul Real */
    .stButton>button { 
        background-color: #2563EB; 
        color: white; 
        border-radius: 6px;
        border: none;
        font-weight: 600;
        padding: 0.6rem 2rem;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #3B82F6;
        transform: translateY(-1px);
    }

    /* Inputs Estilo Dark Mode Premium */
    input, select, textarea {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
        border: 1px solid #475569 !important;
        border-radius: 4px !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #020617;
        border-right: 1px solid #1E293B;
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

# --- 3. NAVEGACIÓN ---
st.sidebar.markdown("<h2 style='color: #3B82F6; border:none;'>MISIÓN 3</h2>", unsafe_allow_html=True)
area = st.sidebar.selectbox("Panel de Control", 
    ["Dashboard Ejecutivo", "Emprendimiento", "Vinculación", "Plataformas", "Comunicaciones", "Gestión Administrativa"])

# --- 4. FUNCIÓN GUARDAR ---
def enviar_datos(coll, data):
    data["timestamp"] = datetime.now()
    db.collection(coll).add(data)
    st.toast("Transmisión exitosa a base de datos central.", icon="🏦")

# --- 5. MÓDULOS DE CARGA ---

if area == "Plataformas":
    st.header("Infraestructura Digital")
    with st.form("f_plat"):
        p_opcion = st.selectbox("Sistemas Críticos", ["Web Institucional", "Accelerator App", "ChatGPT Enterprise", "Make.com", "Hashicorp/Hashi", "Sistemas Externos"])
        c1, c2 = st.columns(2)
        p_estado = c1.select_slider("Estado de Salud", options=["Crítico", "Alerta", "Estable"])
        p_users = c2.number_input("Usuarios / Licencias Activas", min_value=0)
        p_notas = st.text_area("Informe de Incidencias")
        if st.form_submit_button("Actualizar Estatus"):
            enviar_datos("plataformas", {"nombre": p_opcion, "estado": p_estado, "usuarios": p_users, "notas": p_notas})

elif area == "Emprendimiento":
    st.header("Gestión de Programas")
    with st.form("f_emp"):
        prog = st.selectbox("Programa", ["Pre-incubación", "Incubación", "Aceleración", "Mentores"])
        c1, c2 = st.columns(2)
        reg = c1.number_input("Total Registrados", min_value=0)
        com = c2.number_input("Aplicaciones Completas", min_value=0)
        if st.form_submit_button("Sincronizar Datos"):
            enviar_datos("emprendimiento", {"programa": prog, "registrados": reg, "completados": com})

elif area == "Comunicaciones":
    st.header("Métricas de Impacto")
    with st.form("f_com"):
        c1, c2 = st.columns(2)
        foll = c1.number_input("Nuevos Seguidores", min_value=0)
        pau = c2.number_input("Gasto Pauta Mensual (S/.)", min_value=0.0)
        prod = st.number_input("Producción Audiovisual (Unidades)", min_value=0)
        if st.form_submit_button("Guardar Reporte"):
            enviar_datos("comunicaciones", {"seguidores": foll, "pauta": pau, "produccion": prod})

# --- 6. DASHBOARD ESTRATÉGICO EJECUTIVO ---
elif area == "Dashboard Ejecutivo":
    st.title("Inteligencia de Gestión Misión 3")
    
    # KPIs en Azules y Grises
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("REGISTRADOS", "1,850", "+12%", delta_color="normal")
    k2.metric("ALIADOS", "45", "+3")
    k3.metric("GASTO COMMS", "S/. 4,200", "-5%")
    k4.metric("EJECUCIÓN", "72%", "Vía Libre")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Gráficos con Paleta de Azules Ejecutivos
    c1, c2 = st.columns(2)
    
    # Gráfico 1: Azul Medianoche a Azul Acero
    df_emp = pd.DataFrame({'Prog': ['Pre-Inc', 'Inc', 'Acel'], 'Val': [80, 45, 20]})
    fig1 = px.bar(df_emp, x='Prog', y='Val', title="Consolidado de Programas", 
                 template="plotly_dark", color_discrete_sequence=['#3B82F6'])
    fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_family="Inter")
    c1.plotly_chart(fig1, use_container_width=True)

    # Gráfico 2: Gradiente de Grises y Azules
    df_vin = pd.DataFrame({'Tipo': ['Univ', 'Gob', 'Cámaras'], 'Cant': [15, 10, 20]})
    fig2 = px.pie(df_vin, values='Cant', names='Tipo', title="Distribución de Aliados", 
                 hole=.5, template="plotly_dark", 
                 color_discrete_sequence=['#1E3A8A', '#475569', '#94A3B8'])
    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)')
    c2.plotly_chart(fig2, use_container_width=True)
