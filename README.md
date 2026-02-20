# 📊 Dashboard de Empleos en Data Science

## 📌 Descripción del Proyecto

Este proyecto consiste en el desarrollo de un dashboard interactivo en Python utilizando Dash y Plotly, para analizar empleos en el área de Data Science.

El objetivo es explorar cómo varían los salarios según:

- 🌍 País
- 💼 Nivel de experiencia
- 🏢 Tamaño de empresa
- 🏠 Modalidad de trabajo (Remoto, Presencial, Híbrido)
- 📍 Procedencia del empleado

El dashboard permite aplicar filtros dinámicos para analizar los datos de forma interactiva.

## 🛠️ Tecnologías Utilizadas

- Python
- Pandas
- Plotly Express
- Dash

## Dash Bootstrap Components

### Jupyter Notebook

#### 📂 Dataset

Se utilizó el dataset Data Science Job Salaries, que incluye información como:

- salary_in_usd
- experience_level
- employee_residence
- company_location
- remote_ratio
- company_size

Los códigos de país están en formato ISO Alpha-2 (ej: US, DE, CO).

#### 🔄 Transformaciones Realizadas

Durante el proceso de limpieza y preparación de datos se realizaron:

- Eliminación de columnas innecesarias
- Conversión de salario a formato numérico
- Eliminación de valores nulos
- Traducción de niveles de experiencia:
 - EN → Nivel inicial
 - MI → Intermedio
 - SE → Senior
 - EX → Ejecutivo
- Conversión de remote_ratio a modalidad:
 - 0 → Presencial
 - 50 → Híbrido
 - 100 → Remoto
- Conversión de códigos de país a nombres completos

## 📊 Funcionalidades del Dashboard
### 🎛️ Filtros Interactivos

- Filtrar por modalidad de trabajo
- Filtrar por país

## 📈 Visualizaciones

- Salario promedio por país
- Salario promedio por nivel de experiencia
- Salario promedio por tamaño de empresa
- Procedencia de empleados según modalidad

## ▶️ Cómo Ejecutarlo

### Clonar el repositorio:

git clone https://github.com/vivianagonzalez203/Dashboard-Proyecto.git

### Instalar dependencias:

pip install dash plotly pandas dash-bootstrap-components pycountry

### Ejecutar el archivo principal:

python dashboard.py

### Si se ejecuta desde Jupyter Notebook:

app.run(jupyter_mode="inline")

## 📸 Vista del Proyecto

Link: https://dashboard-proyecto-vivianagonzalez.onrender.com

## 🎯 Objetivo Académico

Este proyecto fue desarrollado como parte de una actividad académica para aplicar:

- Limpieza de datos
- Transformación de variables
- Visualización interactiva
- Desarrollo de aplicaciones con Dash

👩‍💻 Autor

Viviana Gonzalez

Proyecto académico – Análisis de datos con Python
