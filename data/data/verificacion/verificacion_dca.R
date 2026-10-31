# Leer los datos de la variante (se asume que el archivo está un nivel arriba, en data/)
datos <- read.csv("../data/dca_mi_variante.csv")

# Convertir la columna 'secador' a factor para el análisis de varianza
datos$secador <- as.factor(datos$secador)

# Ajustar el modelo ANOVA (humedad en función del secador)
modelo_anova <- aov(humedad ~ secador, data = datos)

# Imprimir la tabla ANOVA
cat("\n--- TABLA ANOVA ---\n")
print(summary(modelo_anova))

# Calcular e imprimir las medias por secador
cat("\n--- MEDIAS POR SECADOR ---\n")
medias <- tapply(datos$humedad, datos$secador, mean)
print(medias)

# Calcular el Cuadrado Medio del Error (CME) extrayéndolo del modelo
cme <- summary(modelo_anova)[[1]]["Residuals", "Mean Sq"]
media_general <- mean(datos$humedad)

# Calcular e imprimir el Coeficiente de Variación (CV)
cv <- (sqrt(cme) / media_general) * 100
cat("\n--- COEFICIENTE DE VARIACIÓN (CV) ---\n")
cat(sprintf("%.2f %%\n", cv))

# Realizar e imprimir la prueba de comparación de medias de Tukey
cat("\n--- PRUEBA DE TUKEY ---\n")
prueba_tukey <- TukeyHSD(modelo_anova)
print(prueba_tukey)