import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página (Estética Dark/Neon)
st.set_page_config(page_title="Dashboard CEI", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
        color: #00FFC8; /* Verde Neon */
    }
    h1, h2, h3 {
        color: #FF00E6; /* Rosa Neon */
        text-shadow: 0 0 10px #FF00E6;
    }
    .stButton>button {
        background-color: #FF00E6;
        color: white;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Título de la Plataforma
st.title("🚀 Centro de Emprendimiento: Gestión 360")

# 3. Sidebar para Navegación de Áreas
menu = st.sidebar.selectbox(
    "Seleccione Área de Reporte",
    ["Dashboard Global", "Emprendimiento", "Vinculación", "Plataformas", "Comunicaciones", "Gestión"]
)

# 4. Lógica de Navegación
if menu == "Emprendimiento":
    st.header("📊 Área de Emprendimiento")
    col1, col2 = st.columns(2)
    
    with col1:
        registrados = st.number_input("Total Registrados", min_value=0)
        completados = st.number_input("Registros Completos", min_value=0)
        
    with col2:
        programa = st.selectbox("Programa", ["Pre-incubación", "Incubación", "Aceleración"])
        ciudad = st.text_input("Ciudad de Origen")

    if st.button("Guardar Datos"):
        # Aquí iría la lógica de: db.collection('emprendimiento').add({...})
        st.success(f"Datos de {programa} guardados correctamente en Firebase.")

elif menu == "Dashboard Global":
    st.header("🌐 Indicadores en Tiempo Real")
    
    # Ejemplo de gráfico Neon con Plotly
    df_ejemplo = pd.DataFrame({
        "Programa": ["Pre-inc", "Inc", "Acel"],
        "Registrados": [45, 30, 15]
    })
    
    fig = px.bar(df_ejemplo, x='Programa', y='Registrados', 
                 title="Evolución de Registros",
                 template="plotly_dark")
    fig.update_traces(marker_color='#00FFC8') # Color neon
    
    st.plotly_chart(fig, use_container_width=True)
