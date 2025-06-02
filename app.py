import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import zipfile

# Page setup
st.set_page_config(page_title="Student Exam Analysis", layout="wide")
st.title("📊 Student Exam Performance Dashboard")

# Sidebar navigation menu
st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Select a section:",
    [
        "📁 Upload Data",
        "🔍 Dataset Preview",
        "📈 Histograms",
        "💼 Part-Time Job vs Exam Score",
        "📱 Screen Time vs Exam Score",
        "📚 Study Time vs Exam Score"
    ]
)

# Function to load and process data
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

# Upload data
uploaded_file = st.sidebar.file_uploader("Upload your ZIP file with the dataset", type="zip")
df = load_data(uploaded_file) if uploaded_file else None

# Section logic
if section == "📁 Upload Data":
    st.header("📁 Upload Data")
    st.markdown("""
    Upload a `.zip` file that contains a `.csv` dataset about students (study hours, sleep, part-time job, mental health, etc.).
    This app will explore how those factors affect **exam performance**.
    """)
    if uploaded_file:
        st.success("✅ File uploaded successfully.")
        st.write("You can now explore the dashboard using the menu on the left.")
    else:
        st.warning("Please upload a file to continue.")

elif section == "🔍 Dataset Preview":
    if df is not None:
        st.header("🔍 Dataset Preview")
        st.markdown("Here’s a look at the first few rows of the uploaded dataset:")
        st.dataframe(df.head())
    else:
        st.error("Please upload a valid ZIP file first.")

elif section == "📈 Histograms":
    if df is not None:
        st.header("📈 Histograms of Numeric Features")
        st.markdown("""
        These histograms show the distribution of numeric variables like age, study hours, exercise, and exam scores.
        The KDE (blue curve) helps visualize the shape of the distribution more clearly.
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
        st.error("Please upload a valid ZIP file first.")

elif section == "💼 Part-Time Job vs Exam Score":
    if df is not None:
        st.header("💼 Average Exam Score by Part-Time Job Status")
        st.markdown("""
        This bar chart compares the average exam scores between students who **do** and **do not** have a part-time job.
        It helps analyze if working impacts academic performance.
        """)
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.barplot(data=df, x="part_time_job", y="exam_score", ci="sd", palette="pastel", ax=ax)
        ax.set_title("Average Exam Score by Part-Time Job Status")
        ax.set_xlabel("Part-Time Job")
        ax.set_ylabel("Average Exam Score")
        st.pyplot(fig)
    else:
        st.error("Please upload a valid ZIP file first.")

elif section == "📱 Screen Time vs Exam Score":
    if df is not None:
        st.header("📱 Total Screen Time vs Exam Score")
        st.markdown("""
        This regression plot shows the relationship between total screen time (sum of social media and Netflix hours)
        and exam scores. The red line shows the general trend: is more screen time linked to lower scores?
        """)
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.regplot(data=df, x="total_screen_time", y="exam_score",
                    scatter_kws={"alpha": 0.3}, line_kws={"color": "red"}, ax=ax)
        ax.set_title("Effect of Total Screen Time on Exam Score")
        ax.set_xlabel("Total Screen Time (hours per day)")
        ax.set_ylabel("Exam Score")
        st.pyplot(fig)
    else:
        st.error("Please upload a valid ZIP file first.")

elif section == "📚 Study Time vs Exam Score":
    if df is not None:
        st.header("📚 Study Hours vs Exam Score")
        st.markdown("""
        This scatter plot shows how daily study hours relate to exam scores.
        A positive correlation is expected — more study time could lead to better results, though with variability.
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
        st.error("Please upload a valid ZIP file first.")
