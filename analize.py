import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D

df = pd.read_csv("3_inputs.csv")

# Print basic statistics
print("Data overview:")
print(df.describe())

# Set visual style
sns.set(style="whitegrid")

# Chart 1 – Score over generations
plt.figure()
sns.lineplot(x="generation", y="score", data=df, marker="o")
plt.title("Score per Generation")
plt.xlabel("Generation")
plt.ylabel("Score")
plt.tight_layout()
plt.savefig("chart_score_per_generation.png")

# Chart 2 – Number of surviving birds over generations
plt.figure()
sns.lineplot(x="generation", y="living_birds", data=df, marker="o", color="green")
plt.title("Surviving Birds per Generation")
plt.xlabel("Generation")
plt.ylabel("Number of Surviving Birds")
plt.tight_layout()
plt.savefig("chart_living_birds_per_generation.png")

# Chart 3 – Score vs Distance to Pipe
plt.figure()
sns.scatterplot(x="distance_to_pipe", y="score", data=df)
plt.title("Score vs Distance to Pipe")
plt.xlabel("Distance to Pipe")
plt.ylabel("Score")
plt.tight_layout()
plt.savefig("chart_score_vs_distance.png")

# Chart 4 – 3D Plot: Score based on Y and Distance to Pipe
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(
    df["y"],
    df["distance_to_pipe"],
    df["score"],
    c=df["score"],
    cmap="viridis",
    s=50
)
ax.set_title("3D: Score by Y Position and Pipe Distance")
ax.set_xlabel("Y Position")
ax.set_ylabel("Distance to Pipe")
ax.set_zlabel("Score")
plt.tight_layout()
plt.savefig("chart_3d_score_y_distance.png")

# Chart 5 – Score distribution per generation (Boxplot)
plt.figure(figsize=(12, 6))
sns.boxplot(x="generation", y="score", data=df, palette="Set3")
plt.title("Score Distribution per Generation")
plt.xlabel("Generation")
plt.ylabel("Score")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("chart_boxplot_score_per_generation.png")
