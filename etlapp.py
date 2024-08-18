import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

# Título de la aplicación
st.title("Aplicación de ETL (Extracción, Transformación y Carga)")

# Descripción de la aplicación
st.write("""
## Instrucciones:
1. **Cargar archivo**: Selecciona un archivo en formato CSV o Excel.
2. **Realiza transformaciones**: Limpia valores nulos, normaliza datos o realiza agregaciones.
3. **Descargar archivo transformado**: Al finalizar, puedes descargar el archivo procesado.
""")

# Cargar archivo
uploaded_file = st.file_uploader("Selecciona un archivo CSV o Excel", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Detectar si es un archivo CSV o Excel
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)

    st.write("### Vista previa de los datos cargados:")
    st.dataframe(df.head())

    # Transformaciones básicas
    st.write("### Transformaciones disponibles:")

    # Eliminar filas con valores nulos
    if st.checkbox("Eliminar filas con valores nulos"):
        df = df.dropna()
        st.write("Filas con valores nulos eliminadas.")

    # Normalización de columnas numéricas
    if st.checkbox("Normalizar columnas numéricas"):
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        for col in numeric_cols:
            df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
        st.write("Columnas numéricas normalizadas.")

    # Reemplazar valores 0
    if st.checkbox("Reemplazar valores 0"):
        replacement_value = st.number_input("Introduce el valor de reemplazo para los 0", value=0)
        df.replace(0, replacement_value, inplace=True)
        st.write(f"Todos los valores 0 han sido reemplazados por {replacement_value}.")

    # Eliminar filas duplicadas
    if st.checkbox("Eliminar filas duplicadas"):
        df = df.drop_duplicates()
        st.write("Filas duplicadas eliminadas.")

    # Conversión de tipos de datos
    col_to_convert = st.selectbox("Selecciona una columna para convertir su tipo de datos", df.columns)
    new_type = st.selectbox("Selecciona el nuevo tipo de datos", ["int", "float", "str", "datetime"])
    if st.button("Convertir tipo de datos"):
        try:
            if new_type == "int":
                df[col_to_convert] = df[col_to_convert].astype(int)
            elif new_type == "float":
                df[col_to_convert] = df[col_to_convert].astype(float)
            elif new_type == "str":
                df[col_to_convert] = df[col_to_convert].astype(str)
            elif new_type == "datetime":
                df[col_to_convert] = pd.to_datetime(df[col_to_convert])
            st.write(f"Columna '{col_to_convert}' convertida a {new_type}.")
        except Exception as e:
            st.error(f"Error al convertir tipo de datos: {e}")

    # Filtrado de datos
    st.write("### Filtrar datos:")
    filter_col = st.selectbox("Selecciona una columna para filtrar", df.columns)
    filter_value = st.number_input("Introduce el valor de filtrado", value=0)
    filter_op = st.selectbox("Selecciona la condición", ["Mayor que", "Menor que", "Igual a"])
    
    if st.button("Aplicar filtro"):
        if filter_op == "Mayor que":
            df = df[df[filter_col] > filter_value]
        elif filter_op == "Menor que":
            df = df[df[filter_col] < filter_value]
        elif filter_op == "Igual a":
            df = df[df[filter_col] == filter_value]
        st.write(f"Datos filtrados donde {filter_col} {filter_op.lower()} {filter_value}.")

    # Manejo de valores atípicos
    st.write("### Manejo de valores atípicos:")
    col_outliers = st.selectbox("Selecciona una columna para manejar valores atípicos", df.select_dtypes(include=['float64', 'int64']).columns)
    threshold = st.number_input("Introduce el umbral para detectar valores atípicos", value=1.5)
    
    if st.button("Eliminar valores atípicos"):
        Q1 = df[col_outliers].quantile(0.25)
        Q3 = df[col_outliers].quantile(0.75)
        IQR = Q3 - Q1
        df = df[~((df[col_outliers] < (Q1 - threshold * IQR)) | (df[col_outliers] > (Q3 + threshold * IQR)))]
        st.write(f"Valores atípicos eliminados en la columna {col_outliers}.")

    # División de columnas
    st.write("### División de columnas:")
    split_col = st.selectbox("Selecciona una columna para dividir", df.select_dtypes(include=['object']).columns)
    delimiter = st.text_input("Introduce el delimitador para dividir la columna", value=",")
    
    if st.button("Dividir columna"):
        df[split_col] = df[split_col].astype(str)  # Asegurarse de que la columna es de tipo string
        new_cols = df[split_col].str.split(delimiter, expand=True)
        for i, new_col in enumerate(new_cols.columns):
            df[f"{split_col}_part_{i+1}"] = new_cols[new_col]
        st.write(f"Columna {split_col} dividida en nuevas columnas.")

    # Combinación de columnas
    st.write("### Combinación de columnas:")
    cols_to_combine = st.multiselect("Selecciona columnas para combinar", df.columns)
    separator = st.text_input("Introduce el separador para combinar las columnas", value="_")
    
    if st.button("Combinar columnas"):
        df[f"combined_column"] = df[cols_to_combine].astype(str).agg(separator.join, axis=1)
        st.write("Columnas combinadas.")

    # Creación de columnas calculadas
    st.write("### Creación de columnas calculadas:")
    col1 = st.selectbox("Selecciona la primera columna para la operación", df.columns)
    operation = st.selectbox("Selecciona la operación matemática", ["+", "-", "*", "/"])
    col2 = st.selectbox("Selecciona la segunda columna para la operación", df.columns)
    new_col_name = st.text_input("Introduce el nombre para la nueva columna", value="calculated_column")
    
    if st.button("Crear columna calculada"):
        try:
            if operation == "+":
                df[new_col_name] = df[col1] + df[col2]
            elif operation == "-":
                df[new_col_name] = df[col1] - df[col2]
            elif operation == "*":
                df[new_col_name] = df[col1] * df[col2]
            elif operation == "/":
                df[new_col_name] = df[col1] / df[col2]
            st.write(f"Columna calculada '{new_col_name}' creada.")
        except Exception as e:
            st.error(f"Error al crear columna calculada: {e}")

    # Ordenamiento de datos
    st.write("### Ordenamiento de datos:")
    sort_col = st.selectbox("Selecciona una columna para ordenar", df.columns)
    sort_order = st.selectbox("Selecciona el orden", ["Ascendente", "Descendente"])
    
    if st.button("Ordenar datos"):
        df = df.sort_values(by=sort_col, ascending=(sort_order == "Ascendente"))
        st.write(f"Datos ordenados por la columna {sort_col} en orden {sort_order.lower()}.")

    # Transformaciones de texto
    st.write("### Transformaciones de texto:")
    text_col = st.selectbox("Selecciona una columna de texto para transformar", df.select_dtypes(include=['object']).columns)
    text_transformation = st.selectbox("Selecciona la transformación de texto", ["Convertir a minúsculas", "Eliminar espacios en blanco", "Eliminar caracteres especiales"])
    
    if st.button("Aplicar transformación de texto"):
        if text_transformation == "Convertir a minúsculas":
            df[text_col] = df[text_col].str.lower()
        elif text_transformation == "Eliminar espacios en blanco":
            df[text_col] = df[text_col].str.strip()
        elif text_transformation == "Eliminar caracteres especiales":
            df[text_col] = df[text_col].str.replace(r'[^\w\s]', '', regex=True)
        st.write(f"Transformación de texto '{text_transformation}' aplicada a la columna {text_col}.")

    # Estadísticas avanzadas
    st.write("### Estadísticas avanzadas:")
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    stats_col = st.selectbox("Selecciona una columna para estadísticas avanzadas", numeric_cols)
    if st.button("Calcular estadísticas avanzadas"):
        mean = df[stats_col].mean()
        median = df[stats_col].median()
        mode = df[stats_col].mode().values
        std_dev = df[stats_col].std()
        st.write(f"**Media**: {mean}")
        st.write(f"**Mediana**: {median}")
        st.write(f"**Moda**: {mode}")
        st.write(f"**Desviación estándar**: {std_dev}")

    # Descargar archivo transformado
    st.write("### Descargar archivo transformado:")
    if st.button("Descargar archivo transformado"):
        output = BytesIO()
        if uploaded_file.name.endswith('.csv'):
            df.to_csv(output, index=False)
        elif uploaded_file.name.endswith('.xlsx'):
            df.to_excel(output, index=False)
        st.download_button(label="Descargar archivo", data=output.getvalue(), file_name="transformado_" + uploaded_file.name)

    # Mensaje final
    st.markdown("""
    ---
    <p style="text-align: center;">
        Creado por <a href="https://www.linkedin.com/in/fernandamosquera/" target="_blank">María Fernanda Mosquera - Data Scientist</a>
    </p>
    """, unsafe_allow_html=True)
