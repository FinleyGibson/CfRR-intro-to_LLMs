import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as path_effects

# Create figure
fig, ax = plt.subplots(figsize=(10, 12))
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)
ax.axis('off')

# Define colors (accent colors)
colors = ['#4A90E2', '#7B68EE', '#50C878', '#FF6B6B', '#FFD93D']

# Box positions (x, y, width, height)
boxes = [
    (2.5, 10, 5, 1.2, 'User Request (LLM)', colors[0]),
    (1.5, 7.5, 7, 1.5, '1. Planning / Decomposition\n→ Ingredients\n→ Ordered Steps', colors[1]),
    (1.5, 5, 7, 1.5, '2. Step Executor Loop\n(LLM runs each step alone)', colors[2]),
    (1.5, 2.5, 7, 1.5, '3. Context Memory Update\n(previous steps accumulated)', colors[3]),
    (1.5, 0, 7, 1.5, 'Final Structured Recipe\n+ step-by-step instructions', colors[4]),
]

# Draw boxes
for x, y, w, h, text, color in boxes:
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                          edgecolor='black', facecolor=color, 
                          linewidth=2, alpha=0.8)
    ax.add_patch(box)
    
    # Add text
    ax.text(x + w/2, y + h/2, text, ha='center', va='center',
            fontsize=11, fontweight='bold', color='white',
            path_effects=[path_effects.withStroke(linewidth=3, foreground='black', alpha=0.3)])

# Draw arrows
arrows = [
    (5, 10, 5, 9),      # A -> B
    (5, 7.5, 5, 6.5),   # B -> C
    (5, 5, 5, 4),       # C -> D
    (5, 2.5, 5, 1.5),   # D -> E
]

for x1, y1, x2, y2 in arrows:
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                           arrowstyle='->', mutation_scale=30,
                           linewidth=3, color='black', alpha=0.7)
    ax.add_patch(arrow)

plt.tight_layout()
plt.savefig('documents/harnessing/workflow-diagram.png', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
print("Diagram saved to documents/harnessing/workflow-diagram.png")
