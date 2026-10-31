import streamlit as st

AUTOR = "Jesús Eduardo Manjarrez González"

st.set_page_config(page_title="App de Diseño Experimental", page_icon="🌱", layout="wide")
st.title("App de Diseño Experimental")
st.subheader("Ingeniería Agrícola – Universidad de Sucre")

st.markdown("""
| Módulo | Cuándo se usa | Estado |
|---|---|---|
| **DCA** | Unidades experimentales homogéneas | Disponible |
| **Otros** | DBCA, DCL, Parcelas, Factoriales | En construcción |
""")

st.warning("Esta app apoya el aprendizaje. El estudiante interpreta los resultados, verifica supuestos y compara con su cálculo manual.")

st.markdown("---")
st.header("📖 ¿Cómo utilizar esta aplicación?")

with st.expander("Haz clic aquí para ver los pasos detallados"):
    st.markdown("""
    **1. Prepara tus datos:** 
    Organiza tus datos en un archivo de Excel o CSV. Debes tener al menos una columna para los tratamientos (ej. *Secador*) y otra para la variable de respuesta (ej. *Humedad*). Recuerda usar el punto (`.`) para los decimales.
    
    **2. Selecciona el diseño:** 
    En el menú lateral izquierdo, elige el diseño estadístico que corresponde a tu experimento (actualmente disponible: DCA).
    
    **3. Sube tu archivo:** 
    Usa el botón *'Cargar datos'* en la parte superior del módulo para subir tu documento. Si no subes nada, la app cargará un set de datos de prueba por defecto.
    
    **4. Configura el análisis:** 
    Asegúrate de que las columnas seleccionadas en las listas desplegables coincidan con tus Tratamientos y tu Respuesta. Ajusta el nivel de significancia (Alfa) si requieres algo distinto a 0.05.
    
    **5. Interpreta los resultados:** 
    Navega por las 5 pestañas generadas para revisar los datos base, la tabla ANOVA, la prueba de Tukey (si hay diferencias significativas), los gráficos de distribución y la validación de supuestos (Normalidad y Homocedasticidad).
    """)

st.sidebar.markdown(f"**Autor:** {AUTOR}\n**Curso:** Diseño Experimental\n**Semestre:** 2026-2")