import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D

df = pd.read_csv("6_inputs.csv")

# Show quick summary
print("Data preview:")
print(df.describe())

# Apply consistent plot style
sns.set(style="whitegrid")

# Chart 1 – Score per Generation
plt.figure()
sns.lineplot(x="generation", y="score", data=df, marker="o")
plt.title("Score per Generation")
plt.xlabel("Generation")
plt.ylabel("Score")
plt.tight_layout()
plt.savefig("6_inputs_score_per_generation.png")

# Chart 2 – Surviving Birds per Generation
plt.figure()
sns.lineplot(x="generation", y="living_birds", data=df, marker="o", color="green")
plt.title("Surviving Birds per Generation")
plt.xlabel("Generation")
plt.ylabel("Number of Surviving Birds")
plt.tight_layout()
plt.savefig("6_inputs_living_birds_per_generation.png")

# Chart 3 – Score vs Velocity
plt.figure()
sns.scatterplot(x="velocity", y="score", data=df)
plt.title("Score vs Bird Velocity")
plt.xlabel("Velocity")
plt.ylabel("Score")
plt.tight_layout()
plt.savefig("6_inputs_score_vs_velocity.png")

# Chart 4 – Score vs Distance to Pipe (X only)
plt.figure()
sns.scatterplot(x="distance_to_pipe_only_x", y="score", data=df)
plt.title("Score vs Horizontal Distance to Pipe")
plt.xlabel("Distance to Pipe (X axis only)")
plt.ylabel("Score")
plt.tight_layout()
plt.savefig("6_inputs_score_vs_distance_x.png")

# Chart 5 – 3D: rel_y_to_gap vs Velocity vs Score
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
sc = ax.scatter(
    df["rel_y_to_gap"],
    df["velocity"],
    df["score"],
    c=df["score"],
    cmap="coolwarm",
    s=40
)
ax.set_title("3D: Score by Relative Y to Gap and Velocity")
ax.set_xlabel("Relative Y to Gap")
ax.set_ylabel("Velocity")
ax.set_zlabel("Score")
plt.tight_layout()
plt.savefig("6_inputs_3d_rel_y_velocity_score.png")

# Chart 6 – Boxplot of Score per Generation
plt.figure(figsize=(12, 6))
sns.boxplot(x="generation", y="score", data=df, palette="Set2")
plt.title("Score Distribution per Generation")
plt.xlabel("Generation")
plt.ylabel("Score")
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("6_inputs_boxplot_score_per_generation.png")

# Chart 7 – rel_y_to_gap vs Score (how aligned birds were with gap center)
plt.figure()
sns.scatterplot(x="rel_y_to_gap", y="score", data=df, hue="velocity", palette="viridis")
plt.title("Score vs Relative Y to Gap (Colored by Velocity)")
plt.xlabel("Relative Y to Gap")
plt.ylabel("Score")
plt.tight_layout()
plt.savefig("6_inputs_score_vs_rel_y_to_gap_colored_by_velocity.png")

