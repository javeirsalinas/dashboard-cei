import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# --- 1. CONFIGURACIÓN Y ESTILO ECO-DARK ---
st.set_page_config(page_title="Misión 3 | Reporte Mensual", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #020617; color: #F8FAFC; font-family: 'Inter', sans-serif; }
    h1, h2, h3 { color: #3B82F6 !important; border-bottom: 1px solid #1E293B; }
    [data-testid="stMetric"] { background-color: #0F172A; border: 1px solid #1E3A8A; padding: 20px; border-radius: 12px; }
    .stButton>button { background-color: #1E40AF; color: white; border-radius: 8px; border: none; }
    /* Estilo para el botón de descarga */
    .stDownloadButton>button { background-color: #059669 !important; color: white !important; width: 100%; }
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

# --- 3. FUNCIONES DE DATOS ---
def obtener_datos_periodo(coleccion, dias=30):
    try:
        docs = db.collection(coleccion).stream()
        data = []
        for doc in docs:
            d = doc.to_dict()
            # Convertir timestamp de Firebase a objeto datetime de Python
            if 'timestamp' in d:
                d['fecha'] = d['timestamp'].replace(tzinfo=None)
            data.append(d)
        
        df = pd.DataFrame(data)
        if not df.empty:
            # Filtrar por los últimos 'n' días
            limite = datetime.now() - timedelta(days=dias)
            df = df[df['fecha'] >= limite]
        return df
    except:
        return pd.DataFrame()

# --- 4. NAVEGACIÓN LATERAL ---
st.sidebar.title("💎 Misión 3")
periodo = st.sidebar.radio("Ver evolución de:", ["Última Semana", "Último Mes", "Histórico Total"])
dias_filtro = 7 if periodo == "Última Semana" else 30 if periodo == "Último Mes" else 365

area = st.sidebar.selectbox("Módulos", ["Dashboard Ejecutivo", "Emprendimiento", "Vinculación", "Plataformas", "Comunicaciones", "Gestión"])

# --- 5. DASHBOARD EJECUTIVO CON EVOLUCIÓN ---
if area == "Dashboard Ejecutivo":
    st.title(f"📊 Evolución Estratégica: {periodo}")
    
    # Carga de datos filtrados
    df_emp = obtener_datos_periodo("emprendimiento", dias_filtro)
    df_vin = obtener_datos_periodo("vinculacion", dias_filtro)
    df_com = obtener_datos_periodo("comunicaciones", dias_filtro)
    df_ges = obtener_datos_periodo("gestion", dias_filtro)

    # KPIs Dinámicos
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        val = df_emp['registrados'].sum() if not df_emp.empty else 0
        st.metric("REGISTRADOS", f"{val:,}")
    with k2:
        val = len(df_vin) if not df_vin.empty else 0
        st.metric("NUEVOS ALIADOS", f"{val}")
    with k3:
        val = df_com['pauta'].sum() if not df_com.empty else 0
        st.metric("INVERSIÓN", f"S/. {val:,.0f}")
    with k4:
        val = df_ges['presupuesto'].mean() if not df_ges.empty else 0
        st.metric("EJECUCIÓN", f"{val:.1f}%")

    st.markdown("---")

    # GRÁFICOS DE EVOLUCIÓN
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("📈 Crecimiento de Registros")
        if not df_emp.empty:
            fig1 = px.line(df_emp.sort_values('fecha'), x='fecha', y='registrados', 
                          title="Tendencia Temporal", template="plotly_dark", markers=True)
            fig1.update_traces(line_color='#3B82F6')
            st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        st.subheader("💰 Distribución de Inversión")
        if not df_com.empty:
            fig2 = px.area(df_com.sort_values('fecha'), x='fecha', y='pauta', 
                          template="plotly_dark", color_discrete_sequence=['#10B981'])
            st.plotly_chart(fig2, use_container_width=True)

    # BOTÓN DE DESCARGA (ECO-FRIENDLY)
    st.markdown("### 📥 Exportar Reporte Digital")
    if not df_emp.empty:
        csv = df_emp.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar Reporte Consolidado (CSV)",
            data=csv,
            file_name=f'Mision3_Reporte_{periodo}.csv',
            mime='text/csv',
        )
    st.caption("Evite imprimir este documento. El ahorro de papel contribuye a la sostenibilidad del planeta. 🌱")

# --- (RESTO DE FORMULARIOS SE MANTIENEN IGUAL QUE LA VERSIÓN ANTERIOR) ---
