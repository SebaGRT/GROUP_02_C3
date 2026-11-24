"""Slide kit for the C3 presentations (Group 02).

Builds 16:9 slides with matplotlib so the decks reuse the SAME visual system
as the notebooks and figures (`src/visual_system.py`): palette roles, series
line styles / markers, DejaVu Sans and the title -> subtitle -> footer order.

Coordinates are in slide inches (13.333 x 7.5), origin at the bottom left.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
from src.visual_system import PALETTE, SERIES_STYLE, apply_system_rc  # noqa: E402

W, H = 13.333, 7.5
MARGIN = 0.62

# Slide-level tokens derived from the shared palette (no new hues are introduced)
INK = PALETTE["observed"]        # near-black text / dark background
PAPER = "#FFFFFF"
PAPER_ALT = "#F6F7F9"            # light panel tint
RULE = PALETTE["grid"]
DARK_BG = PALETTE["observed"]    # cover / big-idea slides
DARK_MUTED = "#9CA3AF"


class Slide:
    def __init__(self, dark: bool = False, bg: str | None = None):
        apply_system_rc()
        self.dark = dark
        self.fig = plt.figure(figsize=(W, H), dpi=100)
        self.fig.patch.set_facecolor(bg or (DARK_BG if dark else PAPER))
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(0, W)
        self.ax.set_ylim(0, H)
        self.ax.axis("off")
        self.fg = PAPER if dark else INK
        self.muted = DARK_MUTED if dark else PALETTE["muted"]

    # ---- text -------------------------------------------------------------------------
    def text(self, x, y, s, size=16, color=None, weight="normal", ha="left", va="top",
             style="normal", ls=1.25, **kw):
        return self.ax.text(x, y, s, fontsize=size, color=color or self.fg, fontweight=weight,
                            ha=ha, va=va, fontstyle=style, linespacing=ls, **kw)

    def kicker(self, s, color=None, y=H - 0.55):
        """Small uppercase section label above the headline."""
        self.text(MARGIN, y, s.upper(), size=11, color=color or self.muted, weight="bold")

    def headline(self, s, y=H - 0.85, size=26, color=None, width_note=None):
        return self.text(MARGIN, y, s, size=size, weight="bold", color=color)

    def sub(self, s, y=H - 1.55, size=14, color=None):
        return self.text(MARGIN, y, s, size=size, color=color or self.muted)

    def footer(self, left, page=None, right=None):
        self.ax.plot([MARGIN, W - MARGIN], [0.52, 0.52], color=(DARK_MUTED if self.dark else RULE), lw=0.8)
        self.text(MARGIN, 0.40, left, size=8.5, color=self.muted)
        tail = " · ".join([p for p in [right, (f"{page}" if page is not None else None)] if p])
        if tail:
            self.text(W - MARGIN, 0.40, tail, size=8.5, color=self.muted, ha="right")

    def speaker(self, name):
        """Speaker tag top-right (shows which team member presents the slide)."""
        self.text(W - MARGIN, H - 0.55, name.upper(), size=9.5, color=self.muted, weight="bold", ha="right")

    # ---- shapes -----------------------------------------------------------------------
    def rect(self, x, y, w, h, fc, ec="none", lw=0, alpha=1.0, z=0, hatch=None):
        self.ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, lw=lw, alpha=alpha,
                                    zorder=z, hatch=hatch))

    def card(self, x, y, w, h, fc=PAPER_ALT, ec="none", lw=0, z=0, r=0.06):
        self.ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                         facecolor=fc, edgecolor=ec, lw=lw, zorder=z))

    def accent_bar(self, x, y, h, color, w=0.07):
        self.rect(x, y, w, h, color, z=2)

    def hline(self, x0, x1, y, color=None, lw=0.8, ls="-"):
        self.ax.plot([x0, x1], [y, y], color=color or RULE, lw=lw, ls=ls)

    # ---- images & insets --------------------------------------------------------------
    def image(self, path, x, y, w=None, h=None, crop=None):
        """Place a PNG keeping its aspect ratio. crop=(left, top, right, bottom) fractions."""
        img = mpimg.imread(path)
        if crop:
            hh, ww = img.shape[:2]
            l, t, r, b = crop
            img = img[int(t * hh): int(hh * (1 - b)), int(l * ww): int(ww * (1 - r))]
        ih, iw = img.shape[:2]
        if w is not None and h is None:
            h = w * ih / iw
        elif h is not None and w is None:
            w = h * iw / ih
        ax = self.fig.add_axes([x / W, y / H, w / W, h / H])
        ax.imshow(img, interpolation="lanczos")
        ax.axis("off")
        return (x, y, w, h)

    def inset(self, x, y, w, h):
        """New axes positioned in slide inches, for charts drawn directly on the slide."""
        return self.fig.add_axes([x / W, y / H, w / W, h / H])

    def save(self, pdf, png_path=None, dpi=200):
        fc = self.fig.get_facecolor()
        pdf.savefig(self.fig, facecolor=fc)
        if png_path is not None:
            self.fig.savefig(png_path, dpi=dpi, facecolor=fc)
        plt.close(self.fig)


def series_kw(role, **over):
    st = SERIES_STYLE[role]
    kw = dict(color=st["color"], ls=st["ls"], lw=st["lw"], dash_capstyle="round")
    kw.update(over)
    return kw


def export_pptx(png_paths, notes, out_path):
    """Wrap rendered slides (one full-bleed 16:9 image each) in a PPTX with speaker notes."""
    from pptx import Presentation
    from pptx.util import Inches

    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    blank = prs.slide_layouts[6]
    for png, note in zip(png_paths, notes):
        s = prs.slides.add_slide(blank)
        s.shapes.add_picture(str(png), 0, 0, width=prs.slide_width, height=prs.slide_height)
        s.notes_slide.notes_text_frame.text = note
    prs.save(out_path)
