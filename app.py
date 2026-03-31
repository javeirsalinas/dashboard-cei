# --- 3. FUNCIONES DE DATOS (REPARADA) ---
def obtener_datos_periodo(coleccion, dias=30):
    try:
        docs = db.collection(coleccion).stream()
        data = []
        for doc in docs:
            d = doc.to_dict()
            # Convertir timestamp de Firebase a datetime de Python
            if 'timestamp' in d and d['timestamp'] is not None:
                d['fecha'] = d['timestamp'].replace(tzinfo=None)
            else:
                # Si no tiene timestamp, le asignamos la fecha de hoy para que no de error
                d['fecha'] = datetime.now()
            data.append(d)
        
        if not data:
            return pd.DataFrame()
            
        df = pd.DataFrame(data)
        
        # Verificación de seguridad: Si la columna fecha no existe por algún motivo, la creamos
        if 'fecha' not in df.columns:
            df['fecha'] = datetime.now()

        # Filtrar por los últimos 'n' días
        limite = datetime.now() - timedelta(days=dias)
        df = df[df['fecha'] >= limite]
        return df
    except Exception as e:
        print(f"Error interno: {e}")
        return pd.DataFrame()

# --- 5. DASHBOARD EJECUTIVO ---
if area == "Dashboard Ejecutivo":
    st.title(f"📊 Evolución Estratégica: {periodo}")
    
    # Carga segura de datos
    df_emp = obtener_datos_periodo("emprendimiento", dias_filtro)
    df_vin = obtener_datos_periodo("vinculacion", dias_filtro)
    df_com = obtener_datos_periodo("comunicaciones", dias_filtro)
    df_ges = obtener_datos_periodo("gestion", dias_filtro)

    # Verificación de datos antes de calcular métricas
    k1, k2, k3, k4 = st.columns(4)
    
    # Métricas con validación de existencia de columnas
    reg_val = df_emp['registrados'].sum() if not df_emp.empty and 'registrados' in df_emp.columns else 0
    k1.metric("REGISTRADOS", f"{reg_val:,}")
    
    ali_val = len(df_vin) if not df_vin.empty else 0
    k2.metric("NUEVOS ALIADOS", f"{ali_val}")
    
    pau_val = df_com['pauta'].sum() if not df_com.empty and 'pauta' in df_com.columns else 0
    k3.metric("INVERSIÓN", f"S/. {pau_val:,.0f}")
    
    # En gestión el campo se llama 'presupuesto'
    ges_val = df_ges['presupuesto'].mean() if not df_ges.empty and 'presupuesto' in df_ges.columns else 0
    k4.metric("EJECUCIÓN", f"{ges_val:.1f}%")

    st.markdown("---")

    # Gráficos condicionales para evitar más KeyErrors
    col_a, col_b = st.columns(2)
    
    with col_a:
        if not df_emp.empty and 'fecha' in df_emp.columns and 'registrados' in df_emp.columns:
            st.subheader("📈 Crecimiento de Registros")
            fig1 = px.line(df_emp.sort_values('fecha'), x='fecha', y='registrados', 
                          template="plotly_dark", markers=True)
            fig1.update_traces(line_color='#3B82F6')
            fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("Sin datos suficientes para mostrar tendencia de registros.")

    with col_b:
        if not df_com.empty and 'fecha' in df_com.columns and 'pauta' in df_com.columns:
            st.subheader("💰 Distribución de Inversión")
            fig2 = px.area(df_com.sort_values('fecha'), x='fecha', y='pauta', 
                          template="plotly_dark", color_discrete_sequence=['#10B981'])
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Sin datos suficientes para mostrar inversión.")
