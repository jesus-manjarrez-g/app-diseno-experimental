import streamlit as st
import pandas as pd
import plotly.express as px
import scipy.stats as stats
from utils.anova_utils import cargar_datos, validar_dca, ajustar_dca, tabla_anova, resumen_tratamientos, coeficiente_variacion, tukey, interpretar_dca
from utils.diagnostico_utils import residuos_y_ajustados, prueba_shapiro, prueba_levene, grafico_residuos_vs_ajustados, grafico_qq

st.title("Diseño Completamente al Azar (DCA)")

archivo = st.file_uploader("Cargar datos (CSV/Excel)", type=["csv", "xlsx"])
df = cargar_datos(archivo) if archivo else pd.read_csv("data/dca_secadores.csv")
if archivo is None: st.caption("Usando datos de ejemplo. Sube tu archivo para evaluar tu variante.")

if not df.empty:
    col1, col2, col3 = st.columns(3)
    col_trat = col1.selectbox("Tratamientos", df.columns, index=0)
    col_resp = col2.selectbox("Respuesta", df.columns, index=len(df.columns)-1)
    alfa = col3.slider("Alfa", 0.01, 0.10, 0.05, 0.01)

    if errores := validar_dca(df, col_trat, col_resp):
        for e in errores: st.error(e)
        st.stop()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Datos", "ANOVA", "Tukey", "Gráficos", "Supuestos"])
    modelo = ajustar_dca(df, col_trat, col_resp)
    anova = tabla_anova(modelo)

    with tab1:
        st.dataframe(df)
        st.dataframe(resumen_tratamientos(df, col_trat, col_resp))

    with tab2:
        st.dataframe(anova.style.format(precision=4, na_rep="-"))
        st.write(f"**F crítica:** {stats.f.ppf(1-alfa, anova.loc['Tratamientos','gl'], anova.loc['Error','gl']):.4f} | **CV:** {coeficiente_variacion(modelo, df, col_resp):.2f}%")
        st.success(interpretar_dca(anova, alfa)) if anova.loc['Tratamientos','p-valor'] < alfa else st.info(interpretar_dca(anova, alfa))

    with tab3:
        if anova.loc['Tratamientos', 'p-valor'] < alfa:
            df_tukey, dms, bal = tukey(df, col_trat, col_resp, alfa)
            if not bal: st.warning("Diseño desbalanceado, DMS aproximada.")
            st.write(f"**DMS:** {dms:.4f}")
            st.dataframe(df_tukey)
        else: st.info("No aplica Tukey (no se rechazó H0).")

    with tab4:
        st.plotly_chart(px.box(df, x=col_trat, y=col_resp, points="all", title="Distribución"), use_container_width=True)

    with tab5:
        residuos, ajustados = residuos_y_ajustados(modelo)
        sh_stat, sh_p, sh_c = prueba_shapiro(residuos, alfa)
        lv_stat, lv_p, lv_c = prueba_levene(df, col_trat, col_resp, alfa)
        st.dataframe(pd.DataFrame({
            "Supuesto": ["Normalidad", "Homogeneidad"], "p-valor": [sh_p, lv_p], "Conclusión": [sh_c, lv_c]
        }).style.format({'p-valor': '{:.4f}'}))
        
        c1, c2 = st.columns(2)
        c1.plotly_chart(grafico_qq(residuos), use_container_width=True)
        c2.plotly_chart(grafico_residuos_vs_ajustados(ajustados, residuos), use_container_width=True)
        