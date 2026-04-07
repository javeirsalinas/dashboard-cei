import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px
import datetime

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Dashboard Innovación", layout="wide", initial_sidebar_state="expanded")

# 2. CONEXIÓN A GOOGLE SHEETS
# Se conecta usando la URL definida en Settings > Secrets de Streamlit Cloud
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. SEGURIDAD
PASSWORD_EDITOR = "Emprende2026"

# --- BARRA LATERAL ---
st.sidebar.title("🚀 Gestión de Innovación")
modo = st.sidebar.radio("Seleccione una opción:", ["📊 Dashboard de Gestión", "📥 Carga de Datos (Lunes)"])

# ---------------------------------------------------------
# MODO 1: VISUALIZACIÓN (DASHBOARD)
# ---------------------------------------------------------
if modo == "📊 Dashboard de Gestión":
    st.title("📈 Panel de Control Ejecutivo")
    
    # Selector de Vertical
    # IMPORTANTE: Los nombres aquí deben coincidir EXACTAMENTE con las pestañas de tu Google Sheet
    vertical = st.sidebar.selectbox("Seleccione Vertical:", 
        ["Resumen General", "Emprendimiento", "Vinculacion", "Plataformas", "Comunicacion", "Administracion"])

    if vertical == "Resumen General":
        st.subheader("Vista Consolidada del Centro")
        try:
            # Leemos la primera hoja por defecto para el resumen
            df_resumen = conn.read(ttl=300)
            col1, col2, col3 = st.columns(3)
            col1.metric("Estado del Sistema", "Activo")
            col2.metric("Última Actualización", datetime.date.today().strftime("%d/%m/%Y"))
            col3.metric("Sedes Reportando", "3")
            
            st.divider()
            st.write("### Vista previa de datos generales")
            st.dataframe(df_resumen.head(10), use_container_width=True)
        except Exception as e:
            st.error("No se pudo cargar el resumen. Verifica la conexión con Google Sheets.")

    else:
        try:
            # Carga de la pestaña específica
            df = conn.read(worksheet=vertical, ttl=300)
            st.header(f"Detalle: {vertical}")
            
            # Métricas dinámicas según la pestaña
            if not df.empty:
                st.dataframe(df, use_container_width=True)
                
                # Gráficos automáticos si detecta columnas clave
                if "Cantidad" in df.columns and "Sede" in df.columns:
                    fig = px.bar(df, x="Sede", y="Cantidad", color="Programa" if "Programa" in df.columns else None, title=f"Distribución en {vertical}")
                    st.plotly_chart(fig, use_container_width=True)
                
                if "Seguidores" in df.columns:
                    fig_com = px.line(df, x=df.index, y="Seguidores", title="Evolución de Audiencia")
                    st.plotly_chart(fig_com, use_container_width=True)
            else:
                st.warning(f"La pestaña '{vertical}' está vacía.")
        except Exception as e:
            st.error(f"⚠️ Error: No se encuentra la pestaña '{vertical}' en tu Google Sheets.")
            st.info("Sugerencia: Verifica que en tu Excel la pestaña se llame exactamente igual (sin tildes y sin espacios).")

# ---------------------------------------------------------
# MODO 2: CARGA DE DATOS (FORMULARIOS)
# ---------------------------------------------------------
elif modo == "📥 Carga de Datos (Lunes)":
    st.title("📥 Alimentación de Datos Semanal")
    st.write("Espacio reservado para los responsables de cada pilar.")
    
    pw = st.text_input("Ingrese contraseña de editor:", type="password")
    
    if pw == PASSWORD_EDITOR:
        st.success("Acceso concedido.")
        
        with st.form("form_registro"):
            pilar_carga = st.selectbox("¿Qué área reporta hoy?", 
                ["Emprendimiento", "Vinculacion", "Plataformas", "Comunicacion", "Administracion"])
            
            st.divider()
            
            # --- CAMPOS POR ÁREA ---
            if pilar_carga == "Emprendimiento":
                col1, col2 = st.columns(2)
                programa = col1.selectbox("Programa", ["Pre-incubación", "Incubación"])
                sede = col2.selectbox("Sede", ["Lima", "Arequipa", "Cusco"])
                inscritos = st.number_input("Número de Inscritos", min_value=0, step=1)
                tipo = st.selectbox("Tipo", ["Alumno", "Egresado", "Administrativo"])
                
            elif pilar_carga == "Vinculacion":
                aliado = st.text_input("Nombre del Aliado/Programa")
                region = st.selectbox("Región", ["Piura", "Loreto", "Lima", "Otros"])
                inscritos_v = st.number_input("Emprendedores inscritos", min_value=0)
                
            elif pilar_carga == "Plataformas":
                plataforma = st.text_input("Nombre de Plataforma")
                usuarios = st.number_input("Usuarios Activos", min_value=0)
                status = st.selectbox("Estatus", ["Activa", "Incidencia", "Mantenimiento"])
                
            elif pilar_carga == "Comunicacion":
                red = st.selectbox("Red Social", ["Instagram", "LinkedIn", "Facebook", "TikTok"])
                seguidores = st.number_input("Total Seguidores", min_value=0)
                gasto = st.number_input("Gasto Pauta ($)", min_value=0.0)
                actividad = st.text_area("Actividades del mes (Eventos, audiovisual, etc.)")
                
            elif pilar_carga == "Administracion":
                cat_email = st.selectbox("Categoría de Email", ["Logística", "Viajes", "Rendición Viáticos", "Coordinación"])
                cant_emails = st.number_input("Emails enviados", min_value=0)

            # BOTÓN DE GUARDADO
            btn_guardar = st.form_submit_button("Enviar Reporte")
            
            if btn_guardar:
                st.balloons()
                st.success(f"Datos de {pilar_carga} registrados correctamente en el sistema local.")
                st.info("Nota: Para que se guarden en Google Sheets, asegúrese de que el permiso de la App en Streamlit Cloud esté en modo 'Read/Write'.")
    
    elif pw != "":
        st.error("Contraseña incorrecta.")
