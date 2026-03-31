import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# --- 1. CONFIGURACIÓN Y ESTILO EXECUTIVE PREMIUM ---
st.set_page_config(page_title="Misión 3 | Inteligencia Estratégica", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0F172A; color: #E2E8F0; font-family: 'Inter', sans-serif; }
    h1, h2, h3 { color: #F8FAFC !important; border-bottom: 2px solid #334155; padding-bottom: 10px; }
    [data-testid="stMetric"] { 
        background-color: #1E293B; 
        border: 1px solid #334155; 
        padding: 20px; 
        border-radius: 12px; 
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .stButton>button { 
        background-color: #2563EB; color: white; 
        border-radius: 6px; border: none; font-weight: 600; width: 100%; 
    }
    .stDownloadButton>button { background-color: #059669 !important; color: white !important; }
    input, select, textarea { 
        background-color: #1E293B !important; color: #F8FAFC !important; 
        border: 1px solid #475569 !important; border-radius: 4px !important;
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
        st.error(f"Error de conexión crítica: {e}")

db = firestore.client()

# --- 3. FUNCIONES DE DATOS ---
def obtener_datos_periodo(coleccion, dias=30):
    try:
        docs = db.collection(coleccion).stream()
        data = []
        for doc in docs:
            d = doc.to_dict()
            if 'timestamp' in d and d['timestamp'] is not None:
                d['fecha'] = pd.to_datetime(d['timestamp']).replace(tzinfo=None)
            else:
                d['fecha'] = datetime.now()
            data.append(d)
        
        if not data:
            return pd.DataFrame()
            
        df = pd.DataFrame(data)
        limite = datetime.now() - timedelta(days=dias)
        return df[df['fecha'] >= limite]
    except Exception:
        return pd.DataFrame()

def guardar_mision3(coleccion, data):
    try:
        data["timestamp"] = datetime.now()
        db.collection(coleccion).add(data)
        st.toast(f"✅ Sincronizado en {coleccion.capitalize()}", icon="🚀")
    except Exception as e:
        st.error(f"Error al transmitir: {e}")

# --- 4. NAVEGACIÓN LATERAL (ORDEN CORREGIDO) ---
st.sidebar.markdown("<h2 style='color: #3B82F6; border:none;'>MISIÓN 3</h2>", unsafe_allow_html=True)
periodo_label = st.sidebar.radio("Rango de Evolución:", ["Última Semana", "Último Mes", "Histórico Total"])
dias_filtro = 7 if periodo_label == "Última Semana" else 30 if periodo_label == "Último Mes" else 3650

# Definimos 'area' ANTES de usarla en los condicionales
area = st.sidebar.selectbox("Panel de Control", 
    ["Dashboard Ejecutivo", "Emprendimiento", "Vinculación", "Plataformas", "Comunicaciones", "Gestión Administrativa"])

# --- 5. LÓGICA DE MÓDULOS ---

if area == "Dashboard Ejecutivo":
    st.title(f"📈 Dashboard de Inteligencia: {periodo_label}")
    
    df_emp = obtener_datos_periodo("emprendimiento", dias_filtro)
    df_vin = obtener_datos_periodo("vinculacion", dias_filtro)
    df_com = obtener_datos_periodo("comunicaciones", dias_filtro)
    df_ges = obtener_datos_periodo("gestion", dias_filtro)

    k1, k2, k3, k4 = st.columns(4)
    
    reg_sum = df_emp['registrados'].sum() if not df_emp.empty and 'registrados' in df_emp.columns else 0
    k1.metric("REGISTRADOS", f"{reg_sum:,}")
    
    ali_count = len(df_vin) if not df_vin.empty else 0
    k2.metric("ALIADOS", f"{ali_count}")
    
    pau_sum = df_com['pauta'].sum() if not df_com.empty and 'pauta' in df_com.columns else 0
    k3.metric("INVERSIÓN PAUTA", f"S/. {pau_sum:,.0f}")
    
    ejec_prom = df_ges['presupuesto'].mean() if not df_ges.empty and 'presupuesto' in df_ges.columns else 0
    k4.metric("EJECUCIÓN", f"{ejec_prom:.1f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if not df_emp.empty and 'programa' in df_emp.columns:
            st.subheader("🚀 Programas Activos")
            fig1 = px.bar(df_emp, x='programa', y='registrados', template="plotly_dark", color_discrete_sequence=['#3B82F6'])
            fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig1, use_container_width=True)
    
    with c2:
        if not df_vin.empty and 'tipo_aliado' in df_vin.columns:
            st.subheader("🤝 Distribución de Alianzas")
            fig2 = px.pie(df_vin, names='tipo_aliado', hole=.5, template="plotly_dark", color_discrete_sequence=['#1E3A8A', '#475569', '#94A3B8'])
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    if not df_emp.empty:
        st.download_button(label="📥 Descargar Reporte Semanal/Mensual (CSV)", 
                           data=df_emp.to_csv(index=False).encode('utf-8'),
                           file_name=f"Reporte_Mision3_{datetime.now().strftime('%Y%m%d')}.csv",
                           mime='text/csv')
        st.caption("🌱 Reporte digital optimizado para evitar impresiones innecesarias.")

elif area == "Emprendimiento":
    st.header("🚀 Reporte de Programas")
    with st.form("f_emp"):
        p = st.selectbox("Programa", ["Pre-incubación", "Incubación", "Aceleración", "Mentores"])
        r = st.number_input("Nuevos Registrados", min_value=0)
        c = st.text_input("Ciudades de impacto")
        if st.form_submit_button("Sincronizar"):
            guardar_mision3("emprendimiento", {"programa": p, "registrados": r, "ciudades": c})

elif area == "Vinculación":
    st.header("🤝 Alianzas y ATIPAQ")
    with st.form("f_vin"):
        ati = st.number_input("Registrados ATIPAQ", min_value=0)
        tipo = st.selectbox("Tipo de Aliado", ["Universidad", "Gobierno", "Cámara", "DER", "Otros"])
        nom = st.text_input("Nombre Institución")
        if st.form_submit_button("Registrar Alianza"):
            guardar_mision3("vinculacion", {"atipaq": ati, "tipo_aliado": tipo, "nombre": nom})

elif area == "Plataformas":
    st.header("💻 Estado de Sistemas")
    with st.form("f_plat"):
        sys = st.selectbox("Plataforma", ["web", "accelerator", "ChatGPT", "Make.com", "Hashi"])
        est = st.select_slider("Estatus Operativo", options=["Crítico", "Mantenimiento", "Operativo"])
        if st.form_submit_button("Actualizar Estatus"):
            guardar_mision3("plataformas", {"nombre": sys, "estado": est})

elif area == "Comunicaciones":
    st.header("📱 Impacto Digital")
    with st.form("f_com"):
        s = st.number_input("Nuevos Seguidores", min_value=0)
        p = st.number_input("Gasto Pauta (S/.)", min_value=0.0)
        if st.form_submit_button("Guardar Métricas"):
            guardar_mision3("comunicaciones", {"seguidores": s, "pauta": p})

elif area == "Gestión Administrativa":
    st.header("⚙️ Control Presupuestal")
    with st.form("f_ges"):
        pre = st.slider("Ejecución del Presupuesto %", 0, 100, 50)
        viajes = st.number_input("Viajes/Viáticos realizados", min_value=0)
        if st.form_submit_button("Cerrar Reporte Gestión"):
            guardar_mision3("gestion", {"presupuesto": pre, "viajes": viajes})
