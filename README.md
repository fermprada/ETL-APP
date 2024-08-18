# ETL-APP

# Aplicación ETL con Streamlit

Esta es una aplicación de **Extracción, Transformación y Carga (ETL)** desarrollada con **Streamlit**. Permite cargar archivos CSV o Excel, realizar varias transformaciones y análisis en los datos, y descargar el archivo transformado.

## Características

- **Cargar Archivos:** Selecciona archivos en formato CSV o Excel para su análisis.
- **Transformaciones de Datos:** 
  - Reemplazar valores nulos.
  - Reemplazar valores cero.
  - Normalización de datos.
  - Agregaciones (media, mediana, moda).
- **Análisis Estadístico:** Estadísticas descriptivas avanzadas para columnas numéricas.
- **Descargar Archivo Transformado:** Descarga el archivo procesado en el mismo formato que se cargó.

## Tecnologías Utilizadas

- **Streamlit:** Para crear la interfaz de usuario interactiva.
- **Pandas:** Para el manejo y análisis de datos.
- **Numpy:** Para operaciones numéricas y manejo de arrays.
- **Openpyxl:** Para leer y escribir archivos Excel.

## Instalación

1. **Clona el repositorio:**

    ```bash
    git clone https://github.com/tu_usuario/nombre_del_repositorio.git
    cd nombre_del_repositorio
    ```

2. **Crea un entorno virtual e instálalo:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

## Ejecución de la Aplicación

Para ejecutar la aplicación localmente, usa el siguiente comando:

```bash
streamlit run etlapp.py
```


## Uso

- **Cargar un Archivo:** Usa el botón "Seleccionar archivo" para cargar un archivo CSV o Excel.
- **Realizar Transformaciones:** Selecciona las opciones de transformación que desees aplicar.
- **Ver Análisis Estadístico:** La aplicación mostrará estadísticas descriptivas y distribuciones de los datos.
- **Descargar el Archivo Transformado:** Una vez realizadas las transformaciones, puedes descargar el archivo procesado.

## Contribuciones

Si deseas contribuir a este proyecto, por favor, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una rama para tus cambios:

    ```bash
    git checkout -b mi-nueva-funcionalidad
    ```

3. Realiza tus cambios y haz commit:

    ```bash
    git commit -am 'Añadida nueva funcionalidad'
    ```

4. Haz push a la rama:

    ```bash
    git push origin mi-nueva-funcionalidad
    ```

5. Crea un Pull Request en GitHub.

## Enlace Directo

Puedes acceder a la aplicación ETL en el siguiente enlace:

[https://etl-app-dg6hbteatzs4lp7gp9hcvp.streamlit.app/](https://etl-app-dg6hbteatzs4lp7gp9hcvp.streamlit.app/)


## Autor

Creado por María Fernanda Mosquera - Data Scientist.
