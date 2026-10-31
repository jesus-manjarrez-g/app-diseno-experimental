## Verificación Final

| Valor | Fase 1 (a mano) | App (Python) | R | ¿Coincide? |
|---|---|---|---|---|
| SC Tratamientos | 15.3675 | 15.3675 | 15.3675 | Sí |
| SC Error | 1.9300 | 1.9300 | 1.9300 | Sí |
| CM Error | 0.1608 | 0.1608 | 0.1608 | Sí |
| F calculada | 31.85 | 31.8497 | 31.85 | Sí |
| p-valor | (no aplica) | 0.0000 | 6.77e-06 | Sí |
| DMS Tukey | 0.8420 | 0.8420 | (no aplica) | Sí |
| CV (%) | 3.00 | 3.00 | 3.00 | Sí |
| Grupos de Tukey | C, A, D-B | C, A, D-B | C, A, D-B | Sí |

**Análisis de coincidencias:** 
Los resultados obtenidos mediante cálculo manual, la aplicación en Python y la comprobación cruzada coinciden en su totalidad, con variaciones insignificantes atribuibles al redondeo en el cuarto decimal del p-valor. La prueba Tukey demuestra que los secadores D y B retienen la mayor humedad y no tienen diferencia significativa entre ellos, mientras que el secador C fue el más eficiente. Esto valida de forma contundente la confiabilidad matemática de la herramienta construida.