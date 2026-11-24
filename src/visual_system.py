"""Shared Visual System for Group 02 (IIB423T-1 Business Intelligence · W3 & C3).

Enforces consistent semantic colors, grayscale-safe non-color redundancy,
left-aligned typographic hierarchy, frameless top-bar legends, and zero-based
magnitude scales across all final views.
"""
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# 5-role colorblind-safe semantic palette (consistent across all 3 views)
PALETTE = {
    'observed': '#111827',   # Near-black: actual observed DEIS visits & zero-error axis
    'model':    '#0072B2',   # Blue-teal: updated model (XGBoost + Sim. Nowcast) & settled week t-1
    'nowcast':  '#1B9E77',   # Emerald: partially complete week t (ages 2-8, simulated Chain-Ladder)
    'baseline': '#6B7280',   # Slate gray: naive t-1 baseline, 100% ref, all-settings MAE, + over-forecast
    'alert':    '#C0392B',   # Brick red: excluded Age 1, 2-wk lag, - under-forecast risk, Oct overshoot, CEAR n=31
    'text':     '#1F2937',
    'muted':    '#4B5563',
    'footnote': '#6B7280',
    'grid':     '#E5E7EB',
    'spine':    '#9CA3AF',
}


# Non-color redundancy for time-series roles (C3 fix of W3 feedback on View 2):
# every series that can appear on the same axes differs by LINE STYLE and
# MARKER SHAPE, not only by color, so it stays distinguishable in grayscale
# or for color-vision-deficient readers.
#   Observed  -> solid line   + filled circle  (o)
#   Model     -> dotted line  + filled diamond (D)
#   Baseline  -> dashed line  + hollow square  (s)
SERIES_STYLE = {
    'observed': dict(color=PALETTE['observed'], ls='-',  lw=2.4, marker='o', mfc=PALETTE['observed'], mec='white'),
    'model':    dict(color=PALETTE['model'],    ls=':',  lw=2.5, marker='D', mfc=PALETTE['model'],    mec='white'),
    'baseline': dict(color=PALETTE['baseline'], ls='--', lw=1.6, marker='s', mfc='white',             mec=PALETTE['baseline']),
}


def series_line(role, **overrides):
    """Line kwargs (color, linestyle, linewidth) for a series role; markers are added only at highlighted points."""
    st = SERIES_STYLE[role]
    kw = dict(color=st['color'], ls=st['ls'], lw=st['lw'], dash_capstyle='round')
    kw.update(overrides)
    return kw


def series_marker(role, size=7.0, **overrides):
    """Marker kwargs for ax.plot([x], [y], **series_marker(role)) at a highlighted point (e.g., a peak)."""
    st = SERIES_STYLE[role]
    kw = dict(ls='none', marker=st['marker'], ms=size, mfc=st['mfc'], mec=st['mec'], mew=1.4 if st['mfc'] == 'white' else 0.8)
    kw.update(overrides)
    return kw


def series_handle(role, label, ms=6.0):
    """Legend handle that repeats BOTH the line style and the marker shape of a series role."""
    st = SERIES_STYLE[role]
    return Line2D([0], [0], color=st['color'], ls=st['ls'], lw=st['lw'], dash_capstyle='round',
                  marker=st['marker'], ms=ms, mfc=st['mfc'], mec=st['mec'],
                  mew=1.4 if st['mfc'] == 'white' else 0.8, label=label)


def apply_system_rc():
    """Apply shared typography, spine, tick, and export defaults."""
    plt.rcParams.update({
        'font.family': 'DejaVu Sans',
        'font.size': 9.2,
        'axes.edgecolor': PALETTE['spine'],
        'axes.linewidth': 0.8,
        'axes.titlesize': 12.1,
        'axes.titleweight': 'bold',
        'axes.labelsize': 9.3,
        'axes.labelcolor': PALETTE['text'],
        'xtick.color': PALETTE['muted'],
        'ytick.color': PALETTE['muted'],
        'xtick.labelsize': 8.4,
        'ytick.labelsize': 8.4,
        'figure.facecolor': 'white',
        'axes.facecolor': 'white',
        'savefig.facecolor': 'white',
        'savefig.dpi': 300,
    })


def style_axes(ax, grid_axis='y'):
    """Remove top/right spines and add subtle gridlines on the quantitative axis only."""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis=grid_axis, color=PALETTE['grid'], linewidth=0.75, zorder=0)
    ax.set_axisbelow(True)


def add_header_footer(fig, title, subtitle, footer, title_y=0.965, sub_y=0.910, foot_y=0.015):
    """Apply left-aligned reading hierarchy: Qualified Title -> Context Subtitle -> Caveat Footer."""
    fig.text(0.06, title_y, title, fontsize=12.1, fontweight='bold', color=PALETTE['observed'], ha='left', va='top')
    fig.text(0.06, sub_y, subtitle, fontsize=8.7, color=PALETTE['muted'], ha='left', va='top')
    fig.text(0.06, foot_y, footer, fontsize=7.4, color=PALETTE['footnote'], ha='left', va='bottom')


def add_top_legend(ax, handles, ncol=3, y_offset=1.03, fontsize=7.8):
    """Shared frameless single-row top-bar legend above every plot (zero data overlap)."""
    ax.legend(
        handles=handles,
        loc='lower left',
        bbox_to_anchor=(-0.01, y_offset),
        ncol=ncol,
        frameon=False,
        fontsize=fontsize,
        columnspacing=1.1,
        handletextpad=0.4,
    )
