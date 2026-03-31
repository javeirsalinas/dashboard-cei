# --- CONEXIÓN A FIREBASE (Versión Ultra-Compatible) ---
if not firebase_admin._apps:
    try:
        # 1. Extraemos el diccionario de los secretos
        fb_dict = dict(st.secrets["firebase"])
        
        # 2. LIMPIEZA PROFUNDA: 
        # Forzamos que los saltos de línea sean exactamente los que Firebase espera
        raw_key = fb_dict["private_key"]
        # Primero quitamos posibles escapes de texto y luego normalizamos
        clean_key = raw_key.replace("\\n", "\n").replace("\n\n", "\n")
        fb_dict["private_key"] = clean_key
        
        # 3. Intentamos la conexión
        creds = credentials.Certificate(fb_dict)
        firebase_admin.initialize_app(creds)
    except Exception as e:
        st.error(f"Error crítico de credenciales: {e}")
        st.info("Revisa que la private_key en Secrets empiece con -----BEGIN... y termine con -----END...")

db = firestore.client()
