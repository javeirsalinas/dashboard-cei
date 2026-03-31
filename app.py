import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- 1. CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="Misión 3 | Dashboard Estratégico", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #000000; color: #00FFC8; }
    h1, h2, h3 { color: #FF00E6 !important; text-shadow: 0 0 15px #FF00E6; text-align: center; }
    [data-testid="stMetric"] { background-color: #0A0A0A; border: 1px solid #00FFC8; padding: 15px; border-radius: 5px; }
    .stButton>button { background-color: transparent; color: #FF00E6; border: 2px solid #FF00E6; box-shadow: 0 0 10px #FF00E6; }
    .stButton>button:hover { background-color: #FF00E6; color: black; }
    input, select, textarea { background-color: #111111 !important; color: #00FFC8 !important; border: 1px solid #00FFC8 !important; }
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

# --- 3. NAVEGACIÓN ---
st.sidebar.markdown("<h1 style='color: #FF00E6;'>MISIÓN 3</h1>", unsafe_allow_html=True)
area = st.sidebar.selectbox("Módulos", ["Dashboard Estratégico", "Emprendimiento", "Vinculación", "Plataformas", "Comunicaciones", "Gestión"])

# --- 4. FUNCIÓN GUARDAR ---
def enviar_datos(coll, data):
    data["timestamp"] = datetime.now()
    db.collection(coll).add(data)
    st.success("🚀 TRANSMISIÓN EXITOSA")

# --- 5. MÓDULOS DE CARGA ---

if area == "Plataformas":
    st.header("💻 INFRAESTRUCTURA DIGITAL")
    with st.form("f_plat"):
        # Opciones solicitadas: web, accelerator, ChatGPT, Make.com, Hashi
        p_opcion = st.selectbox("Plataforma", ["Web Institucional", "Accelerator App", "ChatGPT Enterprise", "Make.com", "Hashicorp/Hashi", "Otras"])
        p_estado = st.radio("Estado", ["Operativo", "Mantenimiento", "Incidente"])
        p_users = st.number_input("Usuarios/Licencias", min_value=0)
        p_notas = st.text_area("Observaciones")
        if st.form_submit_button("ACTUALIZAR"):
            enviar_datos("plataformas", {"nombre": p_opcion, "estado": p_estado, "usuarios": p_users, "notas": p_notas})

elif area == "Emprendimiento":
    st.header("🚀 EMPRENDIMIENTO")
    with st.form("f_emp"):
        prog = st.selectbox("Programa", ["Pre-incubación", "Incubación", "Aceleración", "Mentores"])
        reg = st.number_input("Registrados", min_value=0)
        if st.form_submit_button("GUARDAR"):
            enviar_datos("emprendimiento", {"programa": prog, "registrados": reg})

elif area == "Vinculación":
    st.header("🤝 VINCULACIÓN")
    with st.form("f_vin"):
        ati = st.number_input("ATIPAQ", min_value=0)
        ali = st.text_input("Nuevo Aliado")
        if st.form_submit_button("GUARDAR"):
            enviar_datos("vinculacion", {"atipaq": ati, "aliado": ali})

elif area == "Comunicaciones":
    st.header("📱 COMUNICACIONES")
    with st.form("f_com"):
        foll = st.number_input("Nuevos Seguidores", min_value=0)
        pau = st.number_input("Gasto Pauta (S/.)", min_value=0.0)
        if st.form_submit_button("GUARDAR"):
            enviar_datos("comunicaciones", {"seguidores": foll, "pauta": pau})

elif area == "Gestión":
    st.header("⚙️ GESTIÓN")
    with st.form("f_ges"):
        pre = st.slider("Presupuesto %", 0, 100)
        viaj = st.number_input("Viajes/Viáticos", min_value=0)
        if st.form_submit_button("GUARDAR"):
            enviar_datos("gestion", {"presupuesto": pre, "viajes": viaj})

# --- 6. DASHBOARD ESTRATÉGICO MULTI-ÁREA ---
elif area == "Dashboard Estratégico":
    st.title("💡 DASHBOARD ESTRATÉGICO MISIÓN 3")
    
    # KPIs Globales
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("REGISTRADOS", "1,850", "+12%")
    k2.metric("ALIADOS", "45", "+3")
    k3.metric("GASTO PAUTA", "S/. 4,200", "-5%")
    k4.metric("PRESUPUESTO", "72%", "EJECUTADO")

    st.markdown("---")

    # FILA 1 DE GRÁFICOS
    g1, g2 = st.columns(2)
    
    # Gráfico Emprendimiento (Barras Rosa)
    df_emp = pd.DataFrame({'Prog': ['Pre-Inc', 'Inc', 'Acel'], 'Val': [80, 45, 20]})
    fig1 = px.bar(df_emp, x='Prog', y='Val', title="EMPRENDIMIENTO: PROGRAMAS", template="plotly_dark", color_discrete_sequence=['#FF00E6'])
    g1.plotly_chart(fig1, use_container_width=True)

    # Gráfico Vinculación (Pie Verde)
    df_vin = pd.DataFrame({'Tipo': ['Univ', 'Gob', 'Cámaras'], 'Cant': [15, 10, 20]})
    fig2 = px.pie(df_vin, values='Cant', names='Tipo', title="VINCULACIÓN: ALIADOS", hole=.4, template="plotly_dark", color_discrete_sequence=['#00FFC8', '#00D4FF', '#FF00E6'])
    g2.plotly_chart(fig2, use_container_width=True)

    # FILA 2 DE GRÁFICOS
    g3, g4 = st.columns(2)

    # Gráfico Comunicaciones (Línea Neón)
    df_com = pd.DataFrame({'Semana': ['S1', 'S2', 'S3', 'S4'], 'Seguidores': [100, 250, 400, 600]})
    fig3 = px.line(df_com, x='Semana', y='Seguidores', title="COMS: CRECIMIENTO RRSS", template="plotly_dark", markers=True)
    fig3.update_traces(line_color='#00FFC8')
    g3.plotly_chart(fig3, use_container_width=True)

    # Gráfico Gestión (Presupuesto)
    df_ges = pd.DataFrame({'Cat': ['Ejecutado', 'Pendiente'], 'Monto': [72, 28]})
    fig4 = px.pie(df_ges, values='Monto', names='Cat', title="GESTIÓN: PRESUPUESTO", template="plotly_dark", color_discrete_sequence=['#FF00E6', '#333333'])
    g4.plotly_chart(fig4, use_container_width=True)
