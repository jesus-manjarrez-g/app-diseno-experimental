import pandas as pd
import numpy as np
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd

def cargar_datos(archivo) -> pd.DataFrame:
    nombre = archivo.name.lower()
    if nombre.endswith('.csv'):
        try:
            return pd.read_csv(archivo, sep=',')
        except:
            return pd.read_csv(archivo, sep=';')
    elif nombre.endswith(('.xls', '.xlsx')):
        return pd.read_excel(archivo)
    else:
        raise ValueError("Formato no soportado.")

def validar_dca(df: pd.DataFrame, col_trat: str, col_resp: str) -> list[str]:
    errores = []
    if col_trat not in df.columns or col_resp not in df.columns:
        return ["Faltan las columnas seleccionadas."]
    if not pd.api.types.is_numeric_dtype(df[col_resp]):
        errores.append("La respuesta debe ser numérica.")
    if df[col_resp].isnull().any() or df[col_trat].isnull().any():
        errores.append("Hay datos faltantes.")
    if len(df[col_trat].unique()) < 2:
        errores.append("Se necesitan al menos 2 tratamientos.")
    if (df.groupby(col_trat).size() < 2).any():
        errores.append("Cada tratamiento requiere al menos 2 réplicas.")
    return errores

def ajustar_dca(df: pd.DataFrame, col_trat: str, col_resp: str):
    return ols(f'Q("{col_resp}") ~ C(Q("{col_trat}"))', data=df).fit()

def tabla_anova(modelo) -> pd.DataFrame:
    anova = anova_lm(modelo, typ=2)
    anova.columns = ['SC', 'gl', 'F', 'p-valor']
    anova.index = ['Tratamientos', 'Error']
    anova['CM'] = anova['SC'] / anova['gl']
    anova = anova[['gl', 'SC', 'CM', 'F', 'p-valor']]
    fila_total = pd.DataFrame({'gl': [anova['gl'].sum()], 'SC': [anova['SC'].sum()], 'CM': [np.nan], 'F': [np.nan], 'p-valor': [np.nan]}, index=['Total'])
    return pd.concat([anova, fila_total])

def resumen_tratamientos(df: pd.DataFrame, col_trat: str, col_resp: str) -> pd.DataFrame:
    resumen = df.groupby(col_trat)[col_resp].agg(n='count', Total='sum', Media='mean', Desviación='std').reset_index()
    resumen.rename(columns={col_trat: 'Tratamiento'}, inplace=True)
    return resumen

def coeficiente_variacion(modelo, df: pd.DataFrame, col_resp: str) -> float:
    return (np.sqrt(modelo.mse_resid) / df[col_resp].mean()) * 100

def tukey(df: pd.DataFrame, col_trat: str, col_resp: str, alfa=0.05):
    res = pairwise_tukeyhsd(endog=df[col_resp], groups=df[col_trat], alpha=alfa)
    df_tukey = pd.DataFrame(data=res._results_table.data[1:], columns=res._results_table.data[0])
    df_tukey.columns = ['Grupo 1', 'Grupo 2', 'Diferencia', 'p-valor', 'LI', 'LS', 'Rechazar H0']
    
    t = len(df[col_trat].unique())
    gl_error = len(df) - t
    cme = ols(f'Q("{col_resp}") ~ C(Q("{col_trat}"))', data=df).fit().mse_resid
    conteos = df.groupby(col_trat).size()
    balanceado = conteos.nunique() == 1
    r = conteos.iloc[0] if balanceado else len(df) / t
    
    dms = stats.studentized_range.ppf(1 - alfa, t, gl_error) * np.sqrt(cme / r)
    return df_tukey, dms, balanceado

def interpretar_dca(tabla, alfa=0.05) -> str:
    p = tabla.loc['Tratamientos', 'p-valor']
    if p < alfa: return f"Se rechaza H0 (p = {p:.4f} < {alfa}). Hay evidencia estadística de diferencias."
    return f"No se rechaza H0 (p = {p:.4f} >= {alfa}). Las medias se consideran iguales."