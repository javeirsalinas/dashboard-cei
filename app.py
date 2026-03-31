import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

# 1. Conexión a Firebase (Se ejecuta una sola vez)
if not firebase_admin._apps:
    firebase_secrets = dict(st.secrets["firebase"])
    creds = credentials.Certificate(firebase_secrets)
    firebase_admin.initialize_app(creds)

db = firestore.client()

# 2. Configuración estética "Neon"
st.set_page_config(page_title="Portal de Gestión CEI", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #0E1117; color: #00FFC8; }
    h1, h2, h3 { color: #FF00E6; text-shadow: 0 0 10px #FF00E6; }
    .stTextInput, .stNumberInput { color: #00FFC8; }
    </style>
    """, unsafe_allow_html=True)

# 3. Menú Lateral
st.sidebar.title("Navegación")
area = st.sidebar.selectbox("Seleccione su Área", 
    ["Inicio", "Emprendimiento", "Vinculación", "Plataformas", "Comunicaciones", "Gestión"])

# --- MÓDULO: INICIO ---
if area == "Inicio":
    st.title("🚀 Bienvenida al Sistema de Gestión CEI")
    st.write("Por favor, seleccione su área en el menú de la izquierda para ingresar los datos de la semana.")

# --- MÓDULO: EMPRENDIMIENTO ---
elif area == "Emprendimiento":
    st.title("📊 Área de Emprendimiento")
    
    with st.form("form_emprendimiento"):
        programa = st.selectbox("Programa", ["Pre-incubación", "Incubación", "Aceleración", "Mentores"])
        col1, col2 = st.columns(2)
        
        with col1:
            registrados = st.number_input("Número de Registrados", min_value=0, step=1)
            completados = st.number_input("Registros de Aplicación Completos", min_value=0, step=1)
        
        with col2:
            ciudad = st.text_input("Ciudad de Origen (Predominante)")
            fecha = st.date_input("Fecha de Reporte")

        submit = st.form_submit_button("Guardar Reporte")

        if submit:
            # Guardar en la colección 'reportes' de Firebase
            data = {
                "area": "Emprendimiento",
                "programa": programa,
                "registrados": registrados,
                "completados": completados,
                "ciudad": ciudad,
                "fecha": str(fecha)
            }
            db.collection("reportes_cei").add(data)
            st.success(f"✅ Datos de {programa} guardados con éxito.")
