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
    h1, h2 { color: #F8FAFC !important; border-bottom: 2px solid #334155; padding-bottom: 10px; }
    [data-testid="stMetric"] { background-color: #1E293B; border: 1px solid #334155; padding: 20px; border-radius: 8px; }
    .stButton>button { background-color: #2563EB; color: white; border-radius: 6px; font-weight: 600; }
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

# --- 3. FUNCIONES DE EXTRACCIÓN DE DATOS ---
def obtener_datos(coleccion):
    docs = db.collection(coleccion).stream()
    data = [doc.to_dict() for doc in docs]
    return pd.DataFrame(data)

# --- 4. NAVEGACIÓN ---
area = st.sidebar.selectbox("Panel de Control", 
    ["Dashboard Ejecutivo", "Emprendimiento", "Vinculación", "Plataformas", "Comunicaciones", "Gestión Administrativa"])

# --- 5. DASHBOARD EJECUTIVO (LOS 4 GRÁFICOS) ---
if area == "Dashboard Ejecutivo":
    st.title("📈 Inteligencia de Gestión Misión 3")
    
    # Intentamos cargar los datos de las 4 áreas
    df_emp = obtener_datos("emprendimiento")
    df_vin = obtener_datos("vinculacion")
    df_com = obtener_datos("comunicaciones")
    df_ges = obtener_datos("gestion")

    # KPIs Superiores (Totales acumulados reales)
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
    
    # --- FILA 1 DE GRÁFICOS ---
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("🚀 Emprendimiento: Por Programa")
        if not df_emp.empty:
            # Agrupamos por programa para el gráfico
            fig_emp = px.bar(df_emp, x='programa', y='registrados', 
                            color='programa', template="plotly_dark",
                            color_discrete_sequence=['#3B82F6', '#60A5FA', '#93C5FD'])
            fig_emp.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_emp, use_container_width=True)
        else:
            st.info("Esperando datos de Emprendimiento...")

    with c2:
        st.subheader("🤝 Vinculación: Tipos de Aliados")
        if not df_vin.empty:
            fig_vin = px.pie(df_vin, names='tipo_aliado', hole=.5, 
                            template="plotly_dark",
                            color_discrete_sequence=['#1E3A8A', '#334155', '#94A3B8', '#475569'])
            fig_vin.update_layout(paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_vin, use_container_width=True)
        else:
            st.info("Esperando datos de Vinculación...")

    # --- FILA 2 DE GRÁFICOS ---
    c3, c4 = st.columns(2)

    with c3:
        st.subheader("📱 Comunicaciones: Impacto y Pauta")
        if not df_com.empty:
            # Gráfico de dispersión para ver relación seguidores vs pauta
            fig_com = px.scatter(df_com, x='pauta', y='seguidores', size='produccion',
                                title="Seguidores vs Inversión", template="plotly_dark",
                                color_discrete_sequence=['#3B82F6'])
            fig_com.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_com, use_container_width=True)
        else:
            st.info("Esperando datos de Comunicaciones...")

    with c4:
        st.subheader("⚙️ Gestión: Eficiencia Presupuestal")
        if not df_ges.empty:
            # Histórico de ejecución
            fig_ges = px.line(df_ges, y='presupuesto', title="Tendencia de Gasto",
                             template="plotly_dark")
            fig_ges.update_traces(line_color='#60A5FA', mode='lines+markers')
            fig_ges.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_ges, use_container_width=True)
        else:
            st.info("Esperando datos de Gestión...")

# --- (RESTO DE LOS FORMULARIOS SE MANTIENEN IGUAL) ---
