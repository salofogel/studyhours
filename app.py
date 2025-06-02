import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import zipfile

# Configuración de la página
st.set_page_config(page_title="Student Exam Analysis", layout="wide")
st.title("📊 Student Exam Performance Dashboard")

# Sidebar con navegación
st.sidebar.title("Navegación")
section = st.sidebar.radio(
    "Selecciona una sección:",
    [
        "📁 Cargar Datos",
        "🔍 Vista Previa del Dataset",
        "📈 Histogramas",
        "💼 Trabajo de Medio Tiempo vs Nota",
        "📱 Tiempo de Pantalla vs Nota",
        "📚 Estudio vs Nota"
    ]
)

# Cargar archivo ZIP
@st.cache_data
def load_data(uploaded_file):
    with zipfile.ZipFile(uploaded_file) as z:
        csv_files = [f for f in z.namelist() if f.endswith('.csv')]
        if not csv_files:
            return None
        with z.open(csv_files[0]) as f:
            df = pd.read_csv(f)
            df.columns = df.columns.str.strip()
            df["total_screen_time"] = df["social_media_hours"] + df["netflix_hours"]
            return df

uploaded_file = st.sidebar.file_uploader("Sube tu archivo ZIP con el dataset", type="zip")
df = load_data(uploaded_file) if uploaded_file else None

# Secciones según el botón seleccionado
if section == "📁 Cargar Datos":
    st.header("📁 Cargar Datos")
    st.markdown("""
    Sube un archivo `.zip` que contenga un archivo `.csv` con información de estudiantes, como horas de estudio, sueño, trabajo, salud mental, etc.
    El análisis se centrará en cómo estos factores influyen en las **notas de los exámenes**.
    """)
    if uploaded_file:
        st.success("✅ Archivo cargado correctamente.")
        st.write("Puedes continuar navegando por el menú para ver los análisis.")
    else:
        st.warning("Por favor sube un archivo para continuar.")

elif section == "🔍 Vista Previa del Dataset":
    if df is not None:
        st.header("🔍 Vista Previa del Dataset")
        st.markdown("Aquí puedes ver las primeras filas del dataset que has cargado:")
        st.dataframe(df.head())
    else:
        st.error("Por favor sube un archivo ZIP válido primero.")

elif section == "📈 Histogramas":
    if df is not None:
        st.header("📈 Histogramas de Variables Numéricas")
        st.markdown("""
        Estos histogramas muestran la distribución de variables numéricas como edad, horas de sueño, ejercicio y nota del examen.
        Las curvas KDE (en azul claro) ayudan a entender la forma de la distribución.
        """)
        num_cols = df.select_dtypes("number").columns
        cols = 3
        rows = -(-len(num_cols) // cols)

        fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 3))
        axes = axes.flatten()

        for ax, col in zip(axes, num_cols):
            sns.histplot(data=df, x=col, kde=True, ax=ax, color="#6699CC")
            ax.set_title(col.replace("_", " ").title())

        for i in range(len(num_cols), len(axes)):
            axes[i].set_visible(False)

        st.pyplot(fig)
    else:
        st.error("Por favor sube un archivo ZIP válido primero.")

elif section == "💼 Trabajo de Medio Tiempo vs Nota":
    if df is not None:
        st.header("💼 Promedio de Nota según Trabajo de Medio Tiempo")
        st.markdown("""
        Este gráfico compara las notas promedio de los estudiantes que **tienen** y **no tienen** trabajo de medio tiempo.
        Puede revelar si trabajar afecta el rendimiento académico.
        """)
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.barplot(data=df, x="part_time_job", y="exam_score", ci="sd", palette="pastel", ax=ax)
        ax.set_title("Average Exam Score by Part-Time Job Status")
        ax.set_xlabel("Part-Time Job")
        ax.set_ylabel("Average Exam Score")
        st.pyplot(fig)
    else:
        st.error("Por favor sube un archivo ZIP válido primero.")

elif section == "📱 Tiempo de Pantalla vs Nota":
    if df is not None:
        st.header("📱 Tiempo Total de Pantalla vs Nota de Examen")
        st.markdown("""
        Esta regresión muestra la relación entre **el tiempo en redes sociales y Netflix** (combinado como tiempo total de pantalla)
        y la nota del examen. La línea roja indica una tendencia general: ¿más pantalla = peores notas?
        """)
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.regplot(data=df, x="total_screen_time", y="exam_score",
                    scatter_kws={"alpha": 0.3}, line_kws={"color": "red"}, ax=ax)
        ax.set_title("Effect of Total Screen Time on Exam Score")
        ax.set_xlabel("Total Screen Time (hours per day)")
        ax.set_ylabel("Exam Score")
        st.pyplot(fig)
    else:
        st.error("Por favor sube un archivo ZIP válido primero.")

elif section == "📚 Estudio vs Nota":
    if df is not None:
        st.header("📚 Horas de Estudio vs Nota de Examen")
        st.markdown("""
        Este gráfico muestra cómo las **horas diarias de estudio** se relacionan con la nota del examen.
        Se espera ver una relación positiva (más estudio = mejores resultados), aunque con variabilidad.
        """)
        df_clean = df.dropna(subset=["study_hours_per_day", "exam_score"])
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=df_clean, x="study_hours_per_day", y="exam_score", alpha=0.6, ax=ax)
        ax.set_title("Study Time vs. Exam Score")
        ax.set_xlabel("Study Hours per Day")
        ax.set_ylabel("Exam Score")
        ax.grid(True)
        st.pyplot(fig)
    else:
        st.error("Por favor sube un archivo ZIP válido primero.")
