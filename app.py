import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Inicialización limpia
if not firebase_admin._apps:
    # Cargamos el diccionario desde Secrets
    fb_credentials = dict(st.secrets["firebase"])
    
    # IMPORTANTE: Reemplazamos los saltos de línea literales por reales si existen
    if "\\n" in fb_credentials["private_key"]:
        fb_credentials["private_key"] = fb_credentials["private_key"].replace("\\n", "\n")
        
    creds = credentials.Certificate(fb_credentials)
    firebase_admin.initialize_app(creds)

db = firestore.client()

st.success("🚀 ¡Conexión establecida y segura!")
