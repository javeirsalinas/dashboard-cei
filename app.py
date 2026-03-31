import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- 1. CONFIGURACIÓN DE PÁGINA Y ESTILO NEÓN ---
st.set_page_config(page_title="CEI Management System", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0E1117; color: #00FFC8; }
    h1, h2, h3 { color: #FF00E6; text-shadow: 0 0 10px #FF00E6; }
    .stButton>button { 
        background-color: #FF00E6; color: white; 
        border-radius: 20px; border: none; box-shadow: 0 0 10px #FF00E6;
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
st.sidebar.title("🚀 Panel de Control CEI")
area = st.sidebar.selectbox("Seleccione su Área", 
    ["Dashboard Ejecutivo", "Emprendimiento", "Vinculación", "Plataformas", "Comunicaciones", "Gestión"])

# --- 4. FUNCIONES DE APOYO ---
def guardar_datos(coleccion, data):
    try:
        data["timestamp"] = datetime.now()
        db.collection(coleccion).add(data)
        st.success("✅ Datos guardados correctamente en la nube.")
    except Exception as e:
        st.error(f"Error al guardar: {e}")

# --- 5. MÓDULOS POR ÁREA ---

if area == "Emprendimiento":
    st.header("📊 Reporte de Programas")
    with st.form("form_emp"):
        prog = st.selectbox("Programa", ["Pre-incubación", "Incubación", "Aceleración", "Mentores"])
        c1, c2 = st.columns(2)
        reg = c1.number_input("Total Registrados", min_value=0)
        comp = c2.number_input("Registros Completados (Aplicación)", min_value=0)
        city = st.text_input("Origen por ciudades (ej: Lima, Arequipa, Trujillo)")
        if st.form_submit_button("Enviar Reporte"):
            guardar_datos("emprendimiento", {"programa": prog, "registrados": reg, "completados": comp, "ciudades": city})

elif area == "Vinculación":
    st.header("🤝 Alianzas y Concursos")
    with st.form("form_vin"):
        atipaq = st.number_input("Registrados en Concurso ATIPAQ", min_value=0)
        st.subheader("Nuevos Aliados")
        c1, c2 = st.columns(2)
        tipo = c1.selectbox("Tipo de Aliado", ["Universidad", "Cámara de Comercio", "Incubadora", "Municipio", "Gobierno Regional", "DER"])
        nombre = c2.text_input("Nombre de la Organización")
        if st.form_submit_button("Registrar Vinculación"):
            guardar_datos("vinculacion", {"atipaq": atipaq, "tipo_aliado": tipo, "nombre_aliado": nombre})

elif area == "Plataformas":
    st.header("💻 Estado de Infraestructura Digital")
    with st.form("form_plat"):
        plat = st.selectbox("Plataforma", ["Web Institucional", "CRM", "Aula Virtual", "App Emprendedor"])
        estado = st.select_slider("Estado Actual", options=["Incidencia Crítica", "Mantenimiento", "Operativo"])
        users = st.number_input("Usuarios Activos esta semana", min_value=0)
        notas = st.text_area("Detalle de incidencias o licencias")
        if st.form_submit_button("Actualizar Plataforma"):
            guardar_datos("plataformas", {"plataforma": plat, "estado": estado, "usuarios": users, "observaciones": notas})

elif area == "Comunicaciones":
    st.header("📱 Métricas de Redes y Prensa")
    with st.form("form_com"):
        red = st.selectbox("Red Social Principal", ["Facebook", "Instagram", "LinkedIn", "TikTok"])
        followers = st.number_input("Seguidores Ganados", min_value=0)
        pauta = st.number_input("Gasto en Pauta (S/.)", min_value=0.0)
        prod = st.number_input("Piezas de diseño/audiovisuales producidas", min_value=0)
        if st.form_submit_button("Guardar Comunicaciones"):
            guardar_datos("comunicaciones", {"red": red, "seguidores_nuevos": followers, "gasto_pauta": pauta, "produccion": prod})

elif area == "Gestión":
    st.header("⚙️ Gestión Administrativa e Interna")
    with st.form("form_ges"):
        presupuesto = st.number_input("Uso del Presupuesto (%)", min_value=0, max_value=100)
        logistica = st.number_input("Número de solicitudes a logística", min_value=0)
        viajes = st.number_input("Comunicaciones por viajes/viáticos", min_value=0)
        areas_rel = st.number_input("N° de áreas con relación interna", min_value=0)
        if st.form_submit_button("Reportar Gestión"):
            guardar_datos("gestion", {"presupuesto_uso": presupuesto, "solicitudes": logistica, "viajes": viajes, "relaciones_internas": areas_rel})

# --- 6. DASHBOARD EJECUTIVO (VISUALIZACIÓN) ---
elif area == "Dashboard Ejecutivo":
    st.title("💡 Dashboard Estratégico CEI")
    st.write("Visualización de indicadores en tiempo real para la Alta Dirección.")
    
    # Simulación de extracción de datos para visualización
    # En el futuro, aquí leeremos con db.collection('emprendimiento').get()
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Registrados", "1,240", "+12%")
    col2.metric("Aliados Activos", "45", "+3")
    col3.metric("Uso Presupuesto", "68%", "Estable")

    st.divider()
    
    # Gráfico de ejemplo Neón
    df_chart = pd.DataFrame({
        'Área': ['Pre-inc', 'Inc', 'Acel'],
        'Completados': [450, 320, 150]
    })
    
    fig = px.bar(df_chart, x='Área', y='Completados', title="Evolución de Programas",
                 template="plotly_dark", color_discrete_sequence=['#00FFC8'])
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color="#00FFC8"
    )
    
    st.plotly_chart(fig, use_container_width=True)
