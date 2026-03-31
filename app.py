import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# --- CONEXIÓN A FIREBASE (Plan Maestro) ---
if not firebase_admin._apps:
    try:
        # 1. Cargamos los secretos
        fb_creds = dict(st.secrets["firebase"])
        
        # 2. Reparación quirúrgica de la llave PEM
        # Esto quita cualquier error de pegado y restaura los saltos de línea
        fixed_key = fb_creds["private_key"].replace("\\n", "\n")
        fb_creds["private_key"] = fixed_key
        
        # 3. Inicializar con la llave reparada
        creds = credentials.Certificate(fb_creds)
        firebase_admin.initialize_app(creds)
        st.success("✅ ¡CONECTADO POR FIN!")
    except Exception as e:
        st.error(f"Error de conexión: {e}")

db = firestore.client()
