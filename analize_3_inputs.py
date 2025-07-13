import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D

df = pd.read_csv("4_inputs.csv")

# Summary stats
print("Data overview:")
print(df.describe())

sns.set(style="whitegrid")

# Chart 1 – Score per Generation
plt.figure()
sns.lineplot(x="generation", y="score", data=df, marker="o")
plt.title("Score per Generation")
plt.xlabel("Generation")
plt.ylabel("Score")
plt.tight_layout()
plt.savefig("4_inputs_score_per_generation.png")

# Chart 2 – Surviving birds per Generation
plt.figure()
sns.lineplot(x="generation", y="living_birds", data=df, marker="o", color="green")
plt.title("Surviving Birds per Generation")
plt.xlabel("Generation")
plt.ylabel("Number of Surviving Birds")
plt.tight_layout()
plt.savefig("4_inputs_living_birds_per_generation.png")

# Chart 3 – Score vs Distance to Pipe
plt.figure()
sns.scatterplot(x="distance_to_pipe", y="score", data=df)
plt.title("Score vs Distance to Pipe")
plt.xlabel("Distance to Pipe")
plt.ylabel("Score")
plt.tight_layout()
plt.savefig("4_inputs_score_vs_distance.png")

# Chart 4 – Score vs Bird Position vs Gap Center (3D)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
sc = ax.scatter(
    df["y"],
    df["gap_y_center"],
    df["score"],
    c=df["score"],
    cmap="plasma",
    s=50
)
ax.set_title("3D: Score by Bird Y and Gap Center")
ax.set_xlabel("Bird Y Position")
ax.set_ylabel("Gap Y Center")
ax.set_zlabel("Score")
plt.tight_layout()
plt.savefig("4_inputs_score_vs_y_and_gap_3d.png")

# Chart 5 – Boxplot of score per generation
plt.figure(figsize=(12, 6))
sns.boxplot(x="generation", y="score", data=df, palette="Set2")
plt.title("Score Distribution per Generation")
plt.xlabel("Generation")
plt.ylabel("Score")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("4_inputs_score_boxplot_per_generation.png")

# Chart 6 – Bird Position vs Gap Center (how well birds center themselves)
plt.figure()
sns.scatterplot(x="gap_y_center", y="y", data=df, hue="score", palette="viridis")
plt.title("Bird Position vs Gap Center (Colored by Score)")
plt.xlabel("Gap Y Center")
plt.ylabel("Bird Y Position")
plt.tight_layout()
plt.savefig("4_inputs_bird_vs_gap_position_colored_by_score.png")
