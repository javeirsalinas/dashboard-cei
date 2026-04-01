import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# --- 1. ESTILO BASADO EN MISION3.COM (DARK MODE) ---
st.set_page_config(page_title="Misión 3 | Management System", layout="wide")

st.markdown("""
    <style>
    /* Fondo Negro Mate y Fuente Inter */
    .main { 
        background-color: #0A0A0A; 
        color: #F8FAFC; 
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Estilo Minimal */
    [data-testid="stSidebar"] {
        background-color: #111111;
        border-right: 1px solid #262626;
    }

    /* Títulos con el Azul Misión 3 */
    h1, h2, h3 { 
        color: #FFFFFF !important; 
        font-weight: 800 !important;
        letter-spacing: -0.05em;
    }
    
    /* Tarjetas de Métricas - Executive Grey */
    [data-testid="stMetric"] {
        background-color: #171717;
        border: 1px solid #262626;
        padding: 20px;
        border-radius: 10px;
        transition: transform 0.2s;
    }
    [data-testid="stMetric"]:hover {
        border: 1px solid #3B82F6; /* Brillo azul al pasar el mouse */
    }

    /* Botones con el Azul Oficial */
    .stButton>button { 
        background-color: #0056FF; 
        color: white; 
        border-radius: 4px;
        border: none;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        background-color: #0041C2;
        box-shadow: 0px 0px 15px rgba(0, 86, 255, 0.4);
    }

    /* Inputs Modernos */
    input, select, textarea {
        background-color: #171717 !important;
        color: #FFFFFF !important;
        border: 1px solid #262626 !important;
    }
    
    /* Estilo para los divisores */
    hr { border: 0; border-top: 1px solid #262626; }
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
        st.error(f"Error: {e}")

db = firestore.client()

# --- 3. FUNCIONES DE DATOS ---
def obtener_datos(coleccion, dias=3650):
    try:
        docs = db.collection(coleccion).stream()
        data = [doc.to_dict() for doc in docs]
        if not data: return pd.DataFrame()
        df = pd.DataFrame(data)
        if 'timestamp' in df.columns:
            df['fecha'] = pd.to_datetime(df['timestamp']).dt.tz_localize(None)
        else:
            df['fecha'] = datetime.now()
        limite = datetime.now() - timedelta(days=dias)
        return df[df['fecha'] >= limite]
    except: return pd.DataFrame()

def guardar_datos(coll, data):
    data["timestamp"] = datetime.now()
    db.collection(coll).add(data)
    st.toast(f"Sincronizado con Misión 3", icon="🔵")

# --- 4. NAVEGACIÓN ---
st.sidebar.image("https://www.mision3.com/wp-content/uploads/2023/11/logo-mision-3.png", width=150) # Intento de cargar logo si la URL es directa
st.sidebar.markdown("<br>", unsafe_allow_html=True)
area = st.sidebar.selectbox("NAVEGACIÓN", 
    ["Dashboard Ejecutivo", "Emprendimiento", "Vinculación", "Plataformas", "Comunicaciones", "Gestión", "Mantenimiento"])

# --- 5. LÓGICA DE MÓDULOS ---

if area == "Dashboard Ejecutivo":
    st.title("Misión 3 | Dashboard Estratégico")
    st.markdown("---")
    
    df_emp = obtener_datos("emprendimiento")
    df_vin = obtener_datos("vinculacion")
    df_com = obtener_datos("comunicaciones")
    df_ges = obtener_datos("gestion")

    # KPIs con estilo minimalista
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("REGISTRADOS", f"{df_emp['registrados'].sum() if not df_emp.empty else 0:,}")
    m2.metric("ALIADOS", f"{len(df_vin) if not df_vin.empty else 0}")
    m3.metric("INVERSIÓN PAUTA", f"S/. {df_com['pauta'].sum() if not df_com.empty else 0:,.0f}")
    m4.metric("EJECUCIÓN", f"{df_ges['presupuesto'].mean() if not df_ges.empty else 0:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Evolución de Programas")
        if not df_emp.empty:
            fig1 = px.bar(df_emp, x='programa', y='registrados', template="plotly_dark", color_discrete_sequence=['#0056FF'])
            fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig1, use_container_width=True)
    
    with c2:
        st.subheader("Distribución de Ecosistema")
        if not df_vin.empty:
            fig2 = px.pie(df_vin, names='tipo_aliado', hole=.6, template="plotly_dark", color_discrete_sequence=['#0056FF', '#475569', '#94A3B8'])
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig2, use_container_width=True)

# [Los módulos de carga siguen la misma lógica con el nuevo CSS aplicado]
elif area == "Emprendimiento":
    st.header("Gestión de Programas")
    with st.form("f_emp"):
        p = st.selectbox("Programa", ["Pre-incubación", "Incubación", "Aceleración", "Mentores"])
        r = st.number_input("Registrados", min_value=0)
        if st.form_submit_button("GUARDAR REGISTRO"):
            guardar_datos("emprendimiento", {"programa": p, "registrados": r})

elif area == "Mantenimiento":
    st.header("Limpieza de Base de Datos")
    col = st.selectbox("Colección", ["emprendimiento", "vinculacion", "plataformas", "comunicaciones", "gestion"])
    pwd = st.text_input("Palabra clave", type="password")
    if st.button("LIMPIAR"):
        if pwd == "BORRAR":
            docs = db.collection(col).stream()
            for doc in docs: doc.reference.delete()
            st.success("Limpieza completada")
