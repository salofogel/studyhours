import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import zipfile
import io

st.set_page_config(page_title="Student Exam Analysis", layout="wide")
st.title("📊 Student Exam Performance Dashboard")

# File upload
uploaded_file = st.file_uploader("Upload your ZIP file containing the dataset", type="zip")

if uploaded_file is not None:
    try:
        with zipfile.ZipFile(uploaded_file) as z:
            csv_files = [f for f in z.namelist() if f.endswith('.csv')]
            if len(csv_files) == 0:
                st.error("❌ No CSV file found inside the ZIP.")
            else:
                with z.open(csv_files[0]) as f:
                    df = pd.read_csv(f)
                    df.columns = df.columns.str.strip()  # clean column names

                    # Create total_screen_time column
                    df["total_screen_time"] = df["social_media_hours"] + df["netflix_hours"]

                    st.subheader("🔍 Dataset Preview")
                    st.dataframe(df.head())

                    # Histograms for numeric columns
                    st.subheader("📈 Histograms of Numeric Features")
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

                    # Barplot: Part-Time Job vs Exam Score
                    st.subheader("💼 Average Exam Score by Part-Time Job Status")
                    fig2, ax2 = plt.subplots(figsize=(6, 5))
                    sns.barplot(data=df, x="part_time_job", y="exam_score", ci="sd", palette="pastel", ax=ax2)
                    ax2.set_title("Average Exam Score by Part-Time Job Status")
                    ax2.set_xlabel("Part-Time Job")
                    ax2.set_ylabel("Average Exam Score")
                    st.pyplot(fig2)

                    # Regression: Total Screen Time vs Exam Score
                    st.subheader("📱 Total Screen Time vs Exam Score")
                    fig3, ax3 = plt.subplots(figsize=(8, 5))
                    sns.regplot(data=df, x="total_screen_time", y="exam_score",
                                scatter_kws={"alpha": 0.3}, line_kws={"color": "red"}, ax=ax3)
                    ax3.set_title("Effect of Total Screen Time on Exam Score")
                    ax3.set_xlabel("Total Screen Time (hours per day)")
                    ax3.set_ylabel("Exam Score")
                    st.pyplot(fig3)

                    # Scatterplot: Study Time vs Exam Score
                    st.subheader("📚 Study Hours vs Exam Score")
                    df_clean = df.dropna(subset=["study_hours_per_day", "exam_score"])
                    fig4, ax4 = plt.subplots(figsize=(10, 6))
                    sns.scatterplot(data=df_clean, x="study_hours_per_day", y="exam_score", alpha=0.6, ax=ax4)
                    ax4.set_title("Study Time vs. Exam Score")
                    ax4.set_xlabel("Study Hours per Day")
                    ax4.set_ylabel("Exam Score")
                    ax4.grid(True)
                    st.pyplot(fig4)

    except Exception as e:
        st.error(f"Something went wrong: {e}")
