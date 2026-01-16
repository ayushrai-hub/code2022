import numpy as np
import matplotlib.pyplot as plt

# --- data (same as before) ----------------------------------------------------
label_counts = items_new['golden_label'].value_counts()

precision_metrics = {
    'neither': precision_neither,
    'fully_supported': precision_fully_supported,
    'factual_dispute': precision_factual_dispute,
    'minor_dispute': precision_minor_dispute
}

recall_metrics = {
    'neither': recall_neither,
    'fully_supported': recall_fully_supported,
    'factual_dispute': recall_factual_dispute,
    'minor_dispute': recall_minor_dispute
}

# --- numeric x positions ------------------------------------------------------
labels = label_counts.index.tolist()        # ['neither', 'fully_supported', ...]
x_pos  = np.arange(len(labels))             # [0, 1, 2, 3]

# --- plotting -----------------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(10, 6))

# bars -------------------------------------------------------------------------
bars = ax1.bar(x_pos, label_counts.values, color='cyan', alpha=0.5)
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, height,
             str(height), ha='center', va='bottom')

ax1.set_xlabel('Golden Label', fontweight='bold')
ax1.set_ylabel('Count', fontweight='bold')
ax1.set_title('Count of Entries for Each Golden Label',
              fontweight='bold', fontsize=16)

# make the ticks show the string labels
ax1.set_xticks(x_pos)
ax1.set_xticklabels(labels)

# second axis for precision/recall --------------------------------------------
ax2 = ax1.twinx()

for i, label in enumerate(labels):
    prec  = precision_metrics[label]
    rec   = recall_metrics[label]

    # precision point + annotation
    ax2.plot(i, prec, marker='o', color='blue')
    ax2.text(i, prec, f'P:{prec:.2f}', color='blue',
             ha='center', va='bottom')

    # recall point + annotation
    ax2.plot(i, rec, marker='o', color='green')
    ax2.text(i, rec, f'R:{rec:.2f}', color='green',
             ha='center', va='bottom')

ax2.set_ylabel('Precision / Recall', fontweight='bold')
ax2.tick_params(axis='y', labelcolor='blue')  # y‑axis will be blue; change if desired

plt.tight_layout()
plt.show()
