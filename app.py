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
st.sidebar.markdown(f"**Autor:** {AUTOR}\n**Curso:** Diseño Experimental\n**Semestre:** 2026-2")