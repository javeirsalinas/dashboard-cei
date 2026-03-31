import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
    # Cargamos directamente el diccionario de Secrets
    fb_credentials = dict(st.secrets["firebase"])
    creds = credentials.Certificate(fb_credentials)
    firebase_admin.initialize_app(creds)

db = firestore.client()
st.success("¡Conexión Exitosa!")
