# Install and import necessary libraries
!pip install -q gdown
import gdown
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Download the dataset from Google Drive
file_id = "16wVMAByC-TqBOKzybD2MRxEiZ41bzq5u"
gdown.download(f"https://drive.google.com/uc?id={file_id}", "dataset.zip", quiet=False)

# 2. Extract the ZIP file
import zipfile
with zipfile.ZipFile("dataset.zip", 'r') as zip_ref:
    csv_file = zip_ref.namelist()[0]
    with zip_ref.open(csv_file) as f:
        df = pd.read_csv(f)

# 3. Prepare the data
df.columns = df.columns.str.strip()  # Remove whitespace from column names if any

# Create a "total_screen_time" column
df["total_screen_time"] = df["social_media_hours"] + df["netflix_hours"]

# Set general plot style
sns.set_theme(style="whitegrid")

# 4. Histogram of all numeric columns
num_cols = df.select_dtypes("number").columns
n = len(num_cols)
cols = 3
rows = -(-n // cols)  # Round up

fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 3))
axes = axes.flatten()

for ax, col in zip(axes, num_cols):
    sns.histplot(data=df, x=col, kde=True, ax=ax, color="#6699CC")
    ax.set_title(col.replace("_", " ").title())

# Hide any unused subplots
for i in range(n, len(axes)):
    axes[i].set_visible(False)

plt.tight_layout()
plt.show()

# 5. Barplot - Exam Score by Part-Time Job
plt.figure(figsize=(6, 5))
sns.barplot(data=df, x="part_time_job", y="exam_score", ci="sd", palette="pastel")
plt.title("Average Exam Score by Part-Time Job Status")
plt.xlabel("Part-Time Job")
plt.ylabel("Average Exam Score")
plt.tight_layout()
plt.show()

# 6. Regression - Total Screen Time vs Exam Score
plt.figure(figsize=(8, 5))
sns.regplot(data=df, x="total_screen_time", y="exam_score",
            scatter_kws={"alpha": 0.3}, line_kws={"color": "red"})
plt.title("Effect of Total Screen Time on Exam Score")
plt.xlabel("Total Screen Time (hours per day)")
plt.ylabel("Exam Score")
plt.tight_layout()
plt.show()

# 7. Scatterplot - Study Hours vs Exam Score
df_clean = df.dropna(subset=["study_hours_per_day", "exam_score"])
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_clean, x="study_hours_per_day", y="exam_score", alpha=0.6)
plt.title("Study Time vs. Exam Score")
plt.xlabel("Study Hours per Day")
plt.ylabel("Exam Score")
plt.grid(True)
plt.tight_layout()
plt.show()
