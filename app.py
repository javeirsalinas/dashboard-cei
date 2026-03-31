import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Dashboard CEI Neon", layout="wide")

# --- ESTILO NEON ---
st.markdown("""
    <style>
    .main { background-color: #0E1117; color: #00FFC8; }
    h1, h2 { color: #FF00E6; text-shadow: 0 0 10px #FF00E6; text-align: center; }
    .stButton>button { background-color: #FF00E6; color: white; width: 100%; border: none; }
    .stSelectbox, .stTextInput, .stNumberInput { border: 1px solid #00FFC8; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXIÓN A FIREBASE ---
if not firebase_admin._apps:
    fb_dict = dict(st.secrets["firebase"])
    # Limpiamos la llave por si acaso quedaron saltos de línea de texto
    fb_dict["private_key"] = fb_dict["private_key"].replace("\\n", "\n")
    creds = credentials.Certificate(fb_dict)
    firebase_admin.initialize_app(creds)

db = firestore.client()

# --- MENÚ LATERAL ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/606/606112.png", width=100)
st.sidebar.title("Gestión CEI")
menu = st.sidebar.selectbox("Seleccione Área", 
    ["🏠 Inicio", "🚀 Emprendimiento", "🤝 Vinculación", "💻 Plataformas", "📈 Dashboard Real-Time"])

# --- LÓGICA DE MÓDULOS ---

if menu == "🏠 Inicio":
    st.title("BIENVENIDO AL PORTAL CEI")
    st.write("Selecciona un área para reportar los indicadores de esta semana.")

elif menu == "🚀 Emprendimiento":
    st.header("Reporte de Emprendimiento")
    with st.form("form_emp"):
        prog = st.selectbox("Programa", ["Pre-incubación", "Incubación", "Aceleración", "Mentores"])
        c1, c2 = st.columns(2)
        reg = c1.number_input("Registrados", min_value=0)
        comp = c2.number_input("Completados", min_value=0)
        city = st.text_input("Ciudad(es) de origen")
        if st.form_submit_button("Guardar"):
            db.collection("reportes").add({
                "area": "Emprendimiento", "programa": prog, "registrados": reg, 
                "completados": comp, "ciudad": city, "fecha": str(datetime.now())
            })
            st.success("Guardado en Firebase")

elif menu == "🤝 Vinculación":
    st.header("Reporte de Vinculación")
    with st.form("form_vin"):
        atipaq = st.number_input("Registrados ATIPAQ", min_value=0)
        aliado_tipo = st.selectbox("Nuevo Aliado", ["Universidad", "Cámara", "Gobierno", "Otros"])
        aliado_nom = st.text_input("Nombre del Aliado")
        if st.form_submit_button("Registrar Vinculación"):
            db.collection("reportes").add({
                "area": "Vinculación", "atipaq": atipaq, "tipo": aliado_tipo, 
                "nombre": aliado_nom, "fecha": str(datetime.now())
            })
            st.success("Vinculación actualizada")

elif menu == "💻 Plataformas":
    st.header("Estado de Plataformas")
    with st.form("form_plat"):
        plat = st.selectbox("Plataforma", ["CRM", "Web", "Aula Virtual", "App"])
        estado = st.radio("Estado", ["Activo", "Mantenimiento", "Incidencia"])
        user_count = st.number_input("Usuarios activos", min_value=0)
        obs = st.text_area("Incidencias/Notas")
        if st.form_submit_button("Reportar Estado"):
            db.collection("reportes").add({
                "area": "Plataformas", "nombre": plat, "estado": estado, 
                "usuarios": user_count, "notas": obs, "fecha": str(datetime.now())
            })
            st.success("Estado de plataforma enviado")
