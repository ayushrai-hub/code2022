import matplotlib.pyplot as plt

# Step 1: Determine the count of occurrences for each label in the `golden_label` column
label_counts = items_new['golden_label'].value_counts()

# Step 2: Compute precision metrics for each tag
precision_metrics = {
    'neither': precision_neither,
    'fully_supported': precision_fully_supported,
    'factual_dispute': precision_factual_dispute,
    'minor_dispute': precision_minor_dispute
}

# Step 3: Calculate recall metrics for each tag
recall_metrics = {
    'neither': recall_neither,
    'fully_supported': recall_fully_supported,
    'factual_dispute': recall_factual_dispute,
    'minor_dispute': recall_minor_dispute
}

# Enlarge the plot size
fig, ax1 = plt.subplots(figsize=(10, 6))

# Create bars for the count of occurrences for each label
bars = ax1.bar(label_counts.index, label_counts.values, color='cyan', alpha=0.5)

# Embed numerical values for the counts of each bar
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width() / 2, height, str(height), ha='center', va='bottom')

# Assign labels and a title
ax1.set_xlabel('Golden Label', fontweight='bold')
ax1.set_ylabel('Count', fontweight='bold')
ax1.set_title('Count of Entries for Each Golden Label', fontweight='bold', fontsize=16)

# Incorporate a second y-axis to illustrate precision metrics
ax2 = ax1.twinx()

# Get the x-positions from the bars to ensure proper positioning
x_positions = {label: i for i, label in enumerate(label_counts.index)}

# Plot precision metrics with labels
for label, precision in precision_metrics.items():
    if label in x_positions:
        x_pos = x_positions[label]
        ax2.plot(x_pos, precision, marker='o', color='blue')
        ax2.text(x_pos, precision + 0.02, f'P: {precision:.2f}', 
                ha='center', va='bottom', color='blue', fontsize=9)

# Plot recall metrics with labels
for label, recall in recall_metrics.items():
    if label in x_positions:
        x_pos = x_positions[label]
        ax2.plot(x_pos, recall, marker='o', color='green')
        ax2.text(x_pos, recall - 0.05, f'R: {recall:.2f}', 
                ha='center', va='top', color='green', fontsize=9)

# Set the x-axis labels to match the original bars
ax2.set_xticks(range(len(label_counts.index)))
ax2.set_xticklabels(label_counts.index)

# Embed labels for the second y-axis
ax2.set_ylabel('Precision & Recall', fontweight='bold')
ax2.tick_params(axis='y')

plt.tight_layout()
plt.show()
