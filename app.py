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
    .main { background-color: #0F172A; color: #E2E8F0; font-family: 'Inter', sans-serif; }
    h1, h2, h3 { color: #F8FAFC !important; border-bottom: 2px solid #334155; padding-bottom: 10px; }
    [data-testid="stMetric"] { background-color: #1E293B; border: 1px solid #334155; padding: 20px; border-radius: 8px; }
    .stButton>button { background-color: #2563EB; color: white; border-radius: 6px; font-weight: 600; width: 100%; }
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>select {
        background-color: #1E293B !important; color: #F8FAFC !important; border: 1px solid #475569 !important;
    }
    [data-testid="stSidebar"] { background-color: #020617; border-right: 1px solid #1E293B; }
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

# --- 3. FUNCIONES DE APOYO ---
def obtener_datos(coleccion):
    try:
        docs = db.collection(coleccion).stream()
        data = [doc.to_dict() for doc in docs]
        return pd.DataFrame(data)
    except:
        return pd.DataFrame()

def guardar(coleccion, data):
    data["timestamp"] = datetime.now()
    db.collection(coleccion).add(data)
    st.toast(f"Datos sincronizados en {coleccion}", icon="✅")

# --- 4. NAVEGACIÓN ---
area = st.sidebar.selectbox("Panel de Control", 
    ["Dashboard Ejecutivo", "Emprendimiento", "Vinculación", "Plataformas", "Comunicaciones", "Gestión Administrativa"])

# --- 5. DASHBOARD EJECUTIVO ---
if area == "Dashboard Ejecutivo":
    st.title("📈 Inteligencia de Gestión Misión 3")
    
    df_emp = obtener_datos("emprendimiento")
    df_vin = obtener_datos("vinculacion")
    df_com = obtener_datos("comunicaciones")
    df_ges = obtener_datos("gestion")

    # KPIs Superiores
    k1, k2, k3, k4 = st.columns(4)
    total_reg = df_emp['registrados'].sum() if not df_emp.empty else 0
    total_ali = len(df_vin) if not df_vin.empty else 0
    total_pau = df_com['pauta'].sum() if not df_com.empty else 0
    ejecucion = df_ges['presupuesto'].mean() if not df_ges.empty else 0

    k1.metric("REGISTRADOS TOTALES", f"{total_reg:,}")
    k2.metric("ALIADOS ESTRATÉGICOS", f"{total_ali}")
    k3.metric("INVERSIÓN PAUTA", f"S/. {total_pau:,.2f}")
    k4.metric("EJECUCIÓN PROM.", f"{ejecucion:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🚀 Emprendimiento: Programas")
        if not df_emp.empty:
            fig1 = px.bar(df_emp, x='programa', y='registrados', color='programa', template="plotly_dark", color_discrete_sequence=['#3B82F6', '#60A5FA'])
            fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig1, use_container_width=True)
    
    with c2:
        st.subheader("🤝 Vinculación: Aliados")
        if not df_vin.empty:
            fig2 = px.pie(df_vin, names='tipo_aliado', hole=.5, template="plotly_dark", color_discrete_sequence=['#1E3A8A', '#475569', '#94A3B8'])
            st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.subheader("📱 Comunicaciones: Crecimiento")
        if not df_com.empty:
            fig3 = px.scatter(df_com, x='pauta', y='seguidores', template="plotly_dark", color_discrete_sequence=['#3B82F6'])
            st.plotly_chart(fig3, use_container_width=True)
            
    with c4:
        st.subheader("⚙️ Gestión: Presupuesto")
        if not df_ges.empty:
            fig4 = px.line(df_ges, y='presupuesto', template="plotly_dark")
            fig4.update_traces(line_color='#60A5FA')
            st.plotly_chart(fig4, use_container_width=True)

# --- 6. MÓDULOS DE CAPTURA ---
elif area == "Emprendimiento":
    st.header("Gestión de Programas")
    with st.form("f_emp"):
        prog = st.selectbox("Programa", ["Pre-incubación", "Incubación", "Aceleración", "Mentores"])
        reg = st.number_input("Registrados", min_value=0)
        if st.form_submit_button("Sincronizar"):
            guardar("emprendimiento", {"programa": prog, "registrados": reg})

elif area == "Vinculación":
    st.header("Alianzas Estratégicas")
    with st.form("f_vin"):
        tipo = st.selectbox("Tipo de Aliado", ["Universidad", "Gobierno", "Cámara", "DER"])
        nombre = st.text_input("Nombre Institución")
        if st.form_submit_button("Guardar Aliado"):
            guardar("vinculacion", {"tipo_aliado": tipo, "nombre": nombre})

elif area == "Plataformas":
    st.header("Infraestructura Digital")
    with st.form("f_plat"):
        plat = st.selectbox("Plataforma", ["web", "accelerator", "ChatGPT", "Make.com", "Hashi"])
        estado = st.radio("Estatus", ["Operativo", "Incidencia"])
        if st.form_submit_button("Actualizar"):
            guardar("plataformas", {"nombre": plat, "estado": estado})

elif area == "Comunicaciones":
    st.header("Métricas de Difusión")
    with st.form("f_com"):
        seg = st.number_input("Nuevos Seguidores", min_value=0)
        pau = st.number_input("Pauta (S/.)", min_value=0.0)
        if st.form_submit_button("Guardar"):
            guardar("comunicaciones", {"seguidores": seg, "pauta": pau})

elif area == "Gestión Administrativa":
    st.header("Control de Gestión")
    with st.form("f_ges"):
        pre = st.slider("Presupuesto %", 0, 100)
        if st.form_submit_button("Reportar"):
            guardar("gestion", {"presupuesto": pre})
