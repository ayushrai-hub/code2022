import matplotlib.pyplot as plt

# --- ruler geometry ----------------------------------------------------------
half_ruler_length_mm = 565.5 / 2          # half of the full ruler
ruler_width_mm       = 20
n_increments         = 180                # marks along the half‑ruler

# mm ➜ inch
half_len_in  = half_ruler_length_mm / 25.4
ruler_w_in   = ruler_width_mm       / 25.4

# --- page geometry -----------------------------------------------------------
page_w_in, page_h_in = 17, 11            # 11×17 landscape

# horizontal centring (same for both rulers)
left_margin = (page_w_in - half_len_in) / 2

# vertical stacking: ruler A, a gap equal to top_margin, ruler B, bottom_margin
total_rulers_h = 2 * ruler_w_in
top_margin  = (page_h_in - total_rulers_h) / 2      # = bottom margin
bottom_margin = top_margin

# --- figure ------------------------------------------------------------------
fig = plt.figure(figsize=(page_w_in, page_h_in))

def draw_half_ruler(ax, reverse=False):
    ax.set_xlim(0, half_len_in)
    ax.set_ylim(0, ruler_w_in)
    ax.axis('off')

    # border
    ax.add_patch(plt.Rectangle((0, 0), half_len_in, ruler_w_in,
                               fill=False, edgecolor='black', linewidth=1))

    # increments
    for i in range(n_increments + 1):
        x = i * half_len_in / n_increments
        if i % 10 == 0:                        # long tick every 10
            h = ruler_w_in * 0.5
            label = str(i) if not reverse else str(180 - i)
            ax.text(x, h + 0.1, label,
                    ha='center', va='bottom', fontsize=5)
        else:                                  # short tick
            h = ruler_w_in * 0.3
        ax.plot([x, x], [0, h], color='k')

# axes coordinates are given in *figure fraction* (0–1)
# width and height fractions of one half‑ruler
ax_w = half_len_in / page_w_in
ax_h = ruler_w_in   / page_h_in

# first (upper) ruler
ax1 = fig.add_axes([left_margin / page_w_in,
                    (bottom_margin + ruler_w_in) / page_h_in,  # y‑origin of top ruler
                    ax_w, ax_h])
draw_half_ruler(ax1)

# second (lower) ruler – inverted numbers
ax2 = fig.add_axes([left_margin / page_w_in,
                    bottom_margin / page_h_in,                # y‑origin of bottom ruler
                    ax_w, ax_h])
draw_half_ruler(ax2, reverse=True)

plt.savefig("centered_vertical_rulers_11x17.pdf")
