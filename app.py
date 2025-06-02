import streamlit as st
import gdown
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import zipfile

st.set_page_config(page_title="Student Performance Dashboard", layout="wide")
st.title("📊 Student Performance Insights")
st.markdown("Analyze how different lifestyle and study habits affect students' exam performance.")

# Load dataset
@st.cache_data
def load_data():
    file_id = "16wVMAByC-TqBOKzybD2MRxEiZ41bzq5u"
    url = f"https://drive.google.com/uc?id={file_id}"
    output = "dataset.zip"
    gdown.download(url, output, quiet=False)

    with zipfile.ZipFile(output, 'r') as zip_ref:
        csv_file = zip_ref.namelist()[0]
        with zip_ref.open(csv_file) as f:
            df = pd.read_csv(f)
            df.columns = df.columns.str.strip()
            df["total_screen_time"] = df["social_media_hours"] + df["netflix_hours"]
            return df

df = load_data()
sns.set_theme(style="whitegrid")

# Sidebar menu as buttons
st.sidebar.title("Explore the Data")
show_hist = st.sidebar.button("📈 Histogram of Numeric Columns")
show_bar = st.sidebar.button("📊 Exam Score by Job")
show_reg = st.sidebar.button("📉 Screen Time vs Exam Score")
show_scatter = st.sidebar.button("📍 Study Hours vs Exam Score")

# Histogram Plot
if show_hist:
    st.subheader("Distribution of Numeric Features")
    st.markdown("This section shows how each numeric feature is distributed. It helps us understand the spread and common values of study habits, screen time, and scores.")

    num_cols = df.select_dtypes("number").columns
    n = len(num_cols)
    cols = 3
    rows = -(-n // cols)

    fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 3))
    axes = axes.flatten()

    for ax, col in zip(axes, num_cols):
        sns.histplot(data=df, x=col, kde=True, ax=ax, color="#6699CC")
        ax.set_title(col.replace("_", " ").title())

    for i in range(n, len(axes)):
        axes[i].set_visible(False)

    plt.tight_layout()
    st.pyplot(fig)

# Barplot
if show_bar:
    st.subheader("Average Exam Score Based on Part-Time Job Status")
    st.markdown("This barplot compares students with and without part-time jobs and their average exam performance.")

    fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(data=df, x="part_time_job", y="exam_score", ci="sd", palette="pastel", ax=ax)
    ax.set_title("Average Exam Score by Part-Time Job Status")
    ax.set_xlabel("Part-Time Job")
    ax.set_ylabel("Average Exam Score")
    st.pyplot(fig)

# Regression Plot
if show_reg:
    st.subheader("Impact of Total Screen Time on Exam Score")
    st.markdown("This regression plot shows whether spending more time on screens (social media and Netflix) is linked to lower or higher exam scores.")

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.regplot(data=df, x="total_screen_time", y="exam_score",
                scatter_kws={"alpha": 0.3}, line_kws={"color": "red"}, ax=ax)
    ax.set_title("Effect of Total Screen Time on Exam Score")
    ax.set_xlabel("Total Screen Time (hours per day)")
    ax.set_ylabel("Exam Score")
    st.pyplot(fig)

# Scatterplot
if show_scatter:
    st.subheader("Relationship Between Study Time and Exam Scores")
    st.markdown("This scatterplot explores whether students who study more daily tend to score higher in exams.")

    df_clean = df.dropna(subset=["study_hours_per_day", "exam_score"])
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df_clean, x="study_hours_per_day", y="exam_score", alpha=0.6, ax=ax)
    ax.set_title("Study Time vs. Exam Score")
    ax.set_xlabel("Study Hours per Day")
    ax.set_ylabel("Exam Score")
    ax.grid(True)
    st.pyplot(fig)

