"""Build both C3 presentations (Group 02) from the shared visual system.

Output (in this folder), one file with two clearly marked parts:
  GROUP_02_C3_Presentations.pdf / .pptx
    Part 1 (slides 1–7)   -> Presentation 1 · Audience (Monday staffing brief)
    slide 8               -> divider
    Part 2 (slides 9–15)  -> Presentation 2 · Internal Review

Every number shown is copied from the executed notebooks (NB01–NB03) and README;
the three charts are the final figures exported by Notebook 03 (`figures/`).
New slide charts (P1-S4, P2-S3, P2-S5) are drawn here with `src/visual_system.py`
(PALETTE + SERIES_STYLE), so they follow the same rules as the notebook views.

Run:  python presentation/build_presentations.py   (needs matplotlib, python-pptx)
"""
from __future__ import annotations

from pathlib import Path

from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.lines import Line2D

from slide_kit import (DARK_MUTED, INK, MARGIN, PALETTE, PAPER, PAPER_ALT, REPO_ROOT, RULE,
                       SERIES_STYLE, H, W, Slide, export_pptx, series_kw)

OUT = Path(__file__).resolve().parent
FIG = REPO_ROOT / "figures"
RENDER = OUT / "_render"            # per-slide PNGs used to assemble the PPTX
RENDER.mkdir(exist_ok=True)

BLUE, GREEN, GRAY, RED = PALETTE["model"], PALETTE["nowcast"], PALETTE["baseline"], PALETTE["alert"]
MUTED = PALETTE["muted"]
SRC_TEST = "Source: DEIS MINSAL, Atenciones de Urgencia (IdCausa = 2) · Test year 2024 · 31,121 facility-weeks · 633 facilities"

# Crop fractions (left, top, right, bottom) that remove each figure's own title line,
# so the slide headline is the only title (no double headers). Subtitle + footer kept.
CROP = {
    "view1": (0.0, 0.070, 0.0, 0.0),
    "view2": (0.0, 0.072, 0.0, 0.0),
    "view3": (0.0, 0.070, 0.0, 0.0),
}


def deck_footer(s, deck, page, total, source=SRC_TEST):
    s.footer(source, page=f"{page}/{total}", right=deck)


# ======================================================================================
# PRESENTATION 1 · AUDIENCE  (SCR, answer first) — striking but sober
# ======================================================================================
P1 = "Part 1: Monday Staffing Brief"
P1_TOTAL = 7


def p1_cover(pdf, notes, pngs):
    s = Slide(dark=True)
    s.rect(0, H - 0.09, W * 0.62, 0.09, BLUE)
    s.rect(W * 0.62, H - 0.09, W * 0.38, 0.09, GREEN)
    s.text(MARGIN, H - 0.75, "MONDAY STAFFING BRIEF   |   MINSAL / SERVICIOS DE SALUD", size=11.5, color=DARK_MUTED, weight="bold")
    s.text(MARGIN, H - 1.75, "See the respiratory wave\ncoming, two weeks ahead", size=48, weight="bold", ls=1.08)
    s.text(MARGIN, H - 4.0,
           "A forecast built only from data DEIS has already published by Monday cuts\n"
           "the average miss per facility by 30%, and up to 40% with a simulated nowcast.",
           size=17, color="#D1D5DB", ls=1.35)
    s.hline(MARGIN, W - MARGIN, 1.55, color="#374151", lw=1.0)
    s.text(MARGIN, 1.35, "633 public emergency facilities      Forecast horizon: week t+2      Decision: Monday morning",
           size=12.5, color="#D1D5DB")
    s.text(MARGIN, 0.55, "Benjamín Pinto and Sebastián Herrera   |   Group 02, IIB423T-1 Business Intelligence, C3, Presentation 1 of 2",
           size=10, color=DARK_MUTED, va="bottom")
    s.text(W - MARGIN, 0.55, "SEBASTIÁN", size=9.5, color=DARK_MUTED, weight="bold", ha="right", va="bottom")
    png = RENDER / "p1_01.png"; s.save(pdf, png); pngs.append(png)
    notes.append("SEBASTIÁN (~15 s). Good morning. Every Monday you set respiratory emergency staffing two weeks out for "
                 "633 public facilities. We built a forecast that only uses what DEIS has already published by Monday, and "
                 "we will show how much error it removes and where a manual check is still needed.")


def p1_situation(pdf, notes, pngs):
    s = Slide()
    s.kicker("Current planning", color=MUTED); s.speaker("Sebastián")
    s.headline("Today's rule, \"same as last week\", saw the\n2024 winter peak three weeks late", size=27)
    figs = [
        ("633", "public emergency facilities\nplanned every Monday", INK, "4.4M–5.5M respiratory visits a year (2022–2024)", False),
        ("51 visits", "average miss per facility-week\nwith today's rule in 2024", INK, "29.3% of total weekly volume", False),
        ("3 weeks late", "on the 12 May 2024 peak\n(201.7k visits nationally)", RED, "The rule only peaked on 2 Jun.", True),
    ]
    x, cw = MARGIN, 3.85
    for big, lab, col, foot, alert in figs:
        s.hline(x, x + cw - 0.3, 5.42, color=col if alert else INK, lw=1.6)
        s.text(x, 5.25, big, size=36, weight="bold", color=col)
        s.text(x, 4.38, lab, size=13, color=INK, ls=1.3)
        s.text(x, 3.55, foot, size=10.5, color=RED if alert else MUTED, weight="bold" if alert else "normal")
        x += cw + 0.27
    y = 1.55
    s.text(MARGIN, 2.6, "On Monday morning", size=12, color=MUTED, weight="bold")
    boxes = [("Week t−1", "99.1% reported\n(settled)", BLUE, PAPER_ALT),
             ("Week t", "94.3% reported\non Monday", GREEN, PAPER_ALT),
             ("Monday 08:00", "staffing decision", INK, INK),
             ("Week t+1", "shifts already\nscheduled", GRAY, PAPER),
             ("Week t+2", "the week being\nstaffed now", RED, PAPER_ALT)]
    bx, bw = MARGIN, 2.18
    for i, (lab, sub, col, fc) in enumerate(boxes):
        dark = fc == INK
        s.card(bx, y - 0.62, bw, 1.0, fc=fc, ec=(col if not dark else INK), lw=1.2)
        s.text(bx + bw / 2, y + 0.24, lab, size=12.5, weight="bold", ha="center", color=PAPER if dark else col if col != GRAY else MUTED)
        s.text(bx + bw / 2, y - 0.08, sub, size=9.5, ha="center", color=DARK_MUTED if dark else MUTED, ls=1.2)
        if i < len(boxes) - 1:
            s.ax.annotate("", xy=(bx + bw + 0.30, y - 0.12), xytext=(bx + bw + 0.04, y - 0.12),
                          arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.2))
        bx += bw + 0.34
    deck_footer(s, P1, 2, P1_TOTAL)
    png = RENDER / "p1_02.png"; s.save(pdf, png); pngs.append(png)
    notes.append("SEBASTIÁN (~25 s). Right now the meeting takes last week's count and assumes the same two weeks later. "
                 "In 2024 that missed by 51 visits per facility-week on average, and it only reached the 12 May peak three "
                 "weeks late. On Monday morning week t−1 is settled, week t is about 94% in, and shifts are already being "
                 "set for week t+2.")


def p1_complication(pdf, notes, pngs):
    s = Slide()
    s.kicker("DEIS reporting lag", color=MUTED); s.speaker("Sebastián")
    s.headline("On Monday, this week's data is only 94% complete", size=27)
    s.image(FIG / "view1_after_publication_lag.png", MARGIN - 0.1, 1.2, w=8.7, crop=CROP["view1"])
    rx, rw = 9.4, W - MARGIN - 9.4
    items = [
        ("17%", RED, "of facilities have reported\nyesterday.", "Excluded from the model."),
        ("94.3%", GREEN, "of week t is reported by\nMonday. A nowcast can\nfill in the rest.", None),
        ("≈ 10 visits", BLUE, "of extra miss per facility-week\nif week t is dropped\n(2023 check: 37.7 → 47.5).", None),
    ]
    yy = 5.45
    for k, (big, col, txt, alert) in enumerate(items):
        if k:
            s.hline(rx, rx + rw, yy + 0.2, color=RULE, lw=1.0)
        s.text(rx, yy, big, size=26, weight="bold", color=col)
        s.text(rx, yy - 0.55, txt, size=11, color=INK, ls=1.25)
        if alert:
            s.text(rx, yy - 1.12, alert, size=11, color=RED, weight="bold")
        yy -= 1.65
    deck_footer(s, P1, 3, P1_TOTAL, source="Source: live DEIS MINSAL archive, downloaded Wed 4 Nov 2026 (n ≈ 626 facilities/day); ages re-mapped to a Monday decision")
    png = RENDER / "p1_03.png"; s.save(pdf, png); pngs.append(png)
    notes.append("SEBASTIÁN (~30 s). Why not just use this week's numbers? We checked the live DEIS archive. Only 17% of "
                 "facilities have reported yesterday, so we leave that day out. The rest of the week is already about 94% "
                 "complete, and dropping it costs around ten extra visits of error per facility-week. Benjamín will show "
                 "what we get back with settled data alone and with a Monday nowcast.")


def p1_resolution(pdf, notes, pngs):
    s = Slide()
    s.kicker("Forecast accuracy", color=MUTED); s.speaker("Benjamín")
    s.headline("A lag-safe forecast cuts the average miss by 30%,\nand a Monday nowcast could reach 40%", size=25)
    ax = s.inset(MARGIN + 5.55, 1.3, 6.55, 3.95)
    rows = [("Today's rule\n(same as last week)", 51.32, "baseline", "51.3  visits"),
            ("Lag-safe forecast\n(settled data only)", 36.17, "model_open", "36.2  (−29.5%)"),
            ("+ Monday nowcast\n(simulated)", 30.57, "model", "30.6  (−40.4%)")]
    ys = [2, 1, 0]
    ax.axvspan(30.57, 36.17, ymin=0.0, ymax=0.62, facecolor=BLUE, alpha=0.14, hatch="///", edgecolor=BLUE, lw=0.6)
    ax.text(33.37, -0.62, "Expected live range\n30.6 to 36.2", ha="center", va="top", fontsize=10, color=BLUE, fontweight="bold")
    for (lab, v, role, txt), yy in zip(rows, ys):
        st = SERIES_STYLE["baseline" if role == "baseline" else "model"]
        ax.plot([0, v], [yy, yy], color=st["color"], ls=st["ls"], lw=3.2 if role != "baseline" else 2.4, dash_capstyle="round", zorder=3)
        mfc = "white" if role in ("baseline", "model_open") else st["mfc"]
        ax.plot([v], [yy], marker=st["marker"], ms=15, mfc=mfc, mec=st["color"], mew=2.2, ls="none", zorder=5)
        ax.text(v + 1.6, yy, txt, va="center", fontsize=14, fontweight="bold", color=st["color"] if role != "baseline" else INK)
    ax.set_yticks(ys); ax.set_yticklabels([r[0] for r in rows], fontsize=12, color=INK)
    ax.set_xlim(0, 65); ax.set_ylim(-1.25, 2.55)
    ax.set_xticks([0, 10, 20, 30, 40, 50, 60]); ax.tick_params(axis="x", labelsize=10)
    ax.set_xlabel("Average miss per facility-week (visits), 2024 test year, lower is better", fontsize=10.5, color=MUTED)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(PALETTE["spine"]); ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color=RULE, lw=0.8); ax.set_axisbelow(True)
    # left: two short operational notes (no repeated KPI cards)
    s.hline(MARGIN, MARGIN + 2.9, 5.1, color=BLUE, lw=1.6)
    s.text(MARGIN, 4.95, "Ready now", size=14, weight="bold", color=BLUE)
    s.text(MARGIN, 4.55, "Uses settled DEIS data only\n(up to week t−1). No delay\non the 2024 peak.", size=11, color=INK, ls=1.3)
    s.hline(MARGIN, MARGIN + 2.9, 3.05, color=BLUE, lw=1.6, ls=":")
    s.text(MARGIN, 2.9, "With a Monday nowcast", size=14, weight="bold", color=BLUE)
    s.text(MARGIN, 2.5, "Fills in the 94% of week t\nthat is already reported.", size=11, color=INK, ls=1.3)
    s.text(MARGIN, 1.72, "Simulated only, not yet\ntested on live Mondays.", size=11, color=RED, weight="bold", ls=1.3)
    deck_footer(s, P1, 4, P1_TOTAL)
    png = RENDER / "p1_04.png"; s.save(pdf, png); pngs.append(png)
    notes.append("BENJAMÍN (~35 s). We tested on 2024, a year the model never saw. Using only settled data, the average "
                 "miss drops from 51 to 36 visits, about 30% less, and the forecast no longer arrives late to the peak. "
                 "If we also fill in this week's 94% with a nowcast, it drops to 31, about 40% less. That part is simulated, "
                 "though. If real reporting delays come in blocks, the live number should land in the shaded range, between 31 and 36.")


def p1_national(pdf, notes, pngs):
    s = Slide()
    s.kicker("National picture, 2024", color=MUTED); s.speaker("Benjamín")
    s.headline("In 2024 the forecast climbed with the winter wave,\nnot three weeks after it", size=25)
    s.image(FIG / "view2_after_national_forecast.png", MARGIN - 0.12, 0.66, w=8.65, crop=CROP["view2"])
    rx, rw = 9.25, W - MARGIN - 9.25
    s.text(rx, 5.55, "OBSERVED IN 2024", size=10, weight="bold", color=MUTED)
    s.hline(rx, rx + rw, 5.3, color=INK, lw=1.0)
    s.text(rx, 5.15, "Peak of 201.7k visits on 12 May.\nForecast for that week: 182.0k.\nToday's rule: 142.2k.\nOn 6 Oct the forecast was\n28.4k above the real count.",
           size=11, color=INK, ls=1.3)
    s.text(rx, 3.2, "WHAT IT MEANS FOR STAFFING", size=10, weight="bold", color=MUTED)
    s.hline(rx, rx + rw, 2.95, color=BLUE, lw=1.0)
    s.text(rx, 2.8, "The surge shows up in time, but\nthe forecast flattens near the\ntop (9–10% under the peak).",
           size=11, color=INK, ls=1.3)
    s.text(rx, 1.75, "Keep a human check on\npeaks and sudden jumps.", size=11, color=RED, weight="bold", ls=1.3)
    deck_footer(s, P1, 5, P1_TOTAL, source="Source: DEIS MINSAL (IdCausa = 2), 633 facilities, test year 2024. Forecast shown includes the simulated nowcast.")
    png = RENDER / "p1_05.png"; s.save(pdf, png); pngs.append(png)
    notes.append("BENJAMÍN (~35 s). Black solid is what happened, blue dotted is our forecast, grey dashed is today's rule. "
                 "Visits peaked at 201.7 thousand on 12 May. For that week our forecast already said 182 thousand; today's "
                 "rule said 142. Near the top the forecast flattens and stays about 10% short. In October it overshot one week "
                 "by 28 thousand, and we don't know why yet. So peaks and sudden jumps still need someone looking at them.")


def p1_settings(pdf, notes, pngs):
    s = Slide()
    s.kicker("By care setting", color=MUTED); s.speaker("Sebastián")
    s.headline("Misses drop 36–42% across the four main care\nsettings; CEAR is the exception", size=25)
    s.image(FIG / "view3_after_care_setting_mae.png", MARGIN - 0.12, 1.2, w=8.65, crop=CROP["view3"])
    rx, rw = 9.35, W - MARGIN - 9.35
    s.hline(rx, rx + rw, 5.55, color=BLUE, lw=1.6)
    s.text(rx, 5.4, "Where it pays off most", size=14, weight="bold", color=BLUE)
    s.text(rx, 4.98, "SAR (≈297 visits/wk) and SAPU\n(≈210/wk) carry the heaviest load;\ntheir miss falls about 42%.\nHospitals −38%, rural SUR −36%.",
           size=11, color=INK, ls=1.3)
    s.text(rx, 3.48, "Chart: forecast with simulated\nnowcast (settled data only:\n−30% overall).", size=9.5, color=MUTED, ls=1.25)
    s.hline(rx, rx + rw, 2.55, color=RED, lw=1.6)
    s.text(rx, 2.4, "Keep CEAR manual", size=14, weight="bold", color=RED)
    s.text(rx, 1.98, "Only 31 facility-weeks at about\n5 visits a week; the miss rises\nfrom 3.0 to 5.3 visits.", size=11, color=INK, ls=1.3)
    deck_footer(s, P1, 6, P1_TOTAL, source="Source: DEIS MINSAL (IdCausa = 2), 633 facilities, test year 2024")
    png = RENDER / "p1_06.png"; s.save(pdf, png); pngs.append(png)
    notes.append("SEBASTIÁN (~30 s). Staffing is planned by type of facility, so we checked each one. SAR and SAPU are the "
                 "busiest, and there the miss falls by about 42%; hospitals improve 38% and rural SUR 36%. These numbers "
                 "include the simulated nowcast; with settled data only, the overall gain is 30%. CEAR is the exception: "
                 "very little data and about five visits a week, and the forecast does worse there, so CEAR stays manual.")


def p1_action(pdf, notes, pngs):
    s = Slide()
    s.kicker("Recommendation", color=MUTED); s.speaker("Benjamín")
    s.headline("Start with the lag-safe forecast now, and test the\nMonday nowcast live next winter", size=25)
    colw = (W - 2 * MARGIN - 0.6) / 2
    x0 = MARGIN
    s.text(x0, 5.4, "RECOMMENDED ROLLOUT", size=11, weight="bold", color=BLUE)
    s.hline(x0, x0 + colw, 5.12, color=BLUE, lw=1.6)
    steps = [("1", "Use the lag-safe forecast for SAR, SAPU,\nHospital and SUR staffing (−30%, settled data)."),
             ("2", "Run the nowcast in parallel next winter and\nsave each Monday's DEIS download."),
             ("3", "Switch to the nowcast only if its live miss\nclearly beats 36 visits. Keep CEAR manual.")]
    yy = 4.75
    for n, txt in steps:
        s.text(x0, yy, n, size=26, weight="bold", color=BLUE)
        s.text(x0 + 0.6, yy - 0.05, txt, size=12.5, color=INK, ls=1.3)
        yy -= 1.15
    x1 = MARGIN + colw + 0.6
    s.text(x1, 5.4, "WHAT TO KEEP IN MIND", size=11, weight="bold", color=RED)
    s.hline(x1, x1 + colw, 5.12, color=RED, lw=1.6)
    lims = ["The 40% gain is simulated; live, it may be\ncloser to 30%.",
            "One number per facility and no range yet,\nso keep buffers around peaks and jumps.",
            "The national line is smoother than any\nsingle facility.",
            "It forecasts visit volume. It does not explain\nwhat causes an outbreak."]
    yy = 4.75
    for t in lims:
        s.text(x1, yy, "–", size=12.5, color=RED, weight="bold")
        s.text(x1 + 0.35, yy, t, size=12.5, color=INK, ls=1.3)
        yy -= 0.88
    deck_footer(s, P1, 7, P1_TOTAL, source="Source: DEIS MINSAL, test year 2024. Predictive study; it does not establish causes.")
    png = RENDER / "p1_07.png"; s.save(pdf, png); pngs.append(png)
    notes.append("BENJAMÍN (~35 s). We suggest doing this in two steps. Use the lag-safe forecast now for SAR, SAPU, "
                 "hospitals and SUR; it only needs settled data and cut the miss by 30% in 2024. Next winter, run the nowcast "
                 "alongside it and save every Monday download, and switch only if its live miss clearly beats 36 visits. "
                 "CEAR stays manual. Four caveats: the 40% is simulated, there are no uncertainty ranges yet, single "
                 "facilities move more than the national line, and the model predicts demand without explaining it.")


# ======================================================================================
# PRESENTATION 2 · INTERNAL REVIEW  (decision chain) — academic-forward
# ======================================================================================
P2 = "Part 2: Internal Review"
P2_TOTAL = 7


def p2_frame(s, page, ref, speaker, headline, sub=None):
    """Academic header strip: deck tag · notebook citation badge · speaker."""
    s.rect(0, H - 0.42, W, 0.42, PAPER_ALT)
    s.rect(0, H - 0.05, W, 0.05, INK)
    s.text(MARGIN, H - 0.15, "P2: INTERNAL REVIEW   |   GROUP 02, C3", size=9, weight="bold", color=MUTED)
    s.text(W - MARGIN, H - 0.15, f"{speaker.upper()}   |   EVIDENCE: {ref}", size=9, weight="bold", color=MUTED, ha="right",
           family="DejaVu Sans Mono")
    s.text(MARGIN, H - 0.68, headline, size=19.5, weight="bold", ls=1.15)
    if sub:
        s.text(MARGIN, H - 1.62, sub, size=11.5, color=MUTED)


def table(s, x, y, colw, rows, header, size=10, row_h=None, header_size=9.5, colors=None):
    """Tufte-style table: header band + horizontal rules only. rows: list of tuples of str."""
    tw = sum(colw)
    s.rect(x, y - 0.36, tw, 0.36, "#F3F4F6")
    cx = x
    for c, hd in zip(colw, header):
        s.text(cx + 0.1, y - 0.09, hd, size=header_size, weight="bold", color=MUTED)
        cx += c
    yy = y - 0.36
    for ri, r in enumerate(rows):
        n_lines = max(cell.count("\n") + 1 for cell in r)
        rh = row_h or (0.2 + 0.19 * n_lines * size / 10)
        cx = x
        for ci, (c, cell) in enumerate(zip(colw, r)):
            col = (colors[ri][ci] if colors and colors[ri] and colors[ri][ci] else INK)
            s.text(cx + 0.1, yy - 0.09, cell, size=size, color=col, ls=1.22, weight="bold" if ci == 0 else "normal")
            cx += c
        yy -= rh
        s.hline(x, x + tw, yy, color=RULE, lw=0.9)
    return yy


def p2_bridge(pdf, notes, pngs):
    s = Slide()
    p2_frame(s, 1, "README §2, §5", "Sebastián",
             "Two presentations, one study: answer-first SCR for managers,\na decision chain for the review",
             "Big Idea: a Monday forecast restricted to published data cuts the two-week miss by 29.5% (lag-safe)\nto 40.4% (simulated nowcast), with clear operational limits.")
    rows = [("P1 Audience", "MINSAL / Servicio de Salud\noperations managers", "Situation → Complication →\nResolution, answer first",
             "Short Monday meeting: decision and limits\nfirst; method only where it affects trust."),
            ("P2 Internal\nReview", "Instructor as\nreviewer", "Decision chain: evidence or\nfeedback → decision → effect",
             "Reviewer checks traceability: each step cites\nits notebook section, its MAE effect, and\nwhat stayed unchanged.")]
    table(s, MARGIN, 5.2, [1.75, 2.75, 3.1, 4.5], rows, ["Deck", "Audience", "Structure (classes 13–14)", "Why it fits"], size=10.5)
    # pipeline flow
    s.text(MARGIN, 3.05, "PIPELINE AND READING ORDER", size=9.5, weight="bold", color=MUTED)
    flow = [("NB01", "Data, EDA, lag probe,\nchronological split"), ("NB02", "14-model benchmark,\nnowcast, evaluation"),
            ("NB03", "Visual system,\nbefore → after views"), ("src/visual_system.py", "shared rules:\nPALETTE, SERIES_STYLE"),
            ("figures/, slides", "PNG + SVG outputs,\nboth presentations")]
    bx, bw = MARGIN, 2.15
    for i, (a, b) in enumerate(flow):
        s.card(bx, 1.55, bw, 1.2, fc=PAPER, ec=RULE, lw=1.0)
        s.text(bx + 0.15, 2.6, a, size=10.5, weight="bold", family="DejaVu Sans Mono", color=BLUE if i < 3 else INK)
        s.text(bx + 0.15, 2.22, b, size=9.5, color=MUTED, ls=1.2)
        if i < len(flow) - 1:
            s.ax.annotate("", xy=(bx + bw + 0.27, 2.15), xytext=(bx + bw + 0.03, 2.15),
                          arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.1))
        bx += bw + 0.3
    s.text(MARGIN, 1.2, "Contributions. Benjamín: model expansion and nowcasting (XGBoost, SARIMAX, Chain-Ladder), first W3 visual system, notebook integration.\n"
           "Sebastián: data engineering C1–C2, DEIS lag probe and lag-safe panel, W3 method and visual audit, C3 validation. Shared: framing, narrative, defense.",
           size=9.5, color=INK, ls=1.3)
    deck_footer(s, P2, 1, P2_TOTAL, source="Repository: GROUP_02_C3, README.md (reading order, roles, AI statement)")
    png = RENDER / "p2_01.png"; s.save(pdf, png); pngs.append(png)
    notes.append("SEBASTIÁN (~25 s). Both decks defend one Big Idea with one visual system. For managers we used "
                 "Situation-Complication-Resolution, answer first, because their meeting is short and they need the decision "
                 "and its limits. For you as reviewer we use a decision chain: evidence or feedback, the decision it caused, "
                 "and the effect, each tied to a notebook section. Underneath is the order in which to read the repository.")


def p2_data(pdf, notes, pngs):
    s = Slide()
    p2_frame(s, 2, "NB01 §1–§4 · NB02 §1", "Sebastián",
             "EDA and the live lag probe set our 2022–23 window,\nthe Poisson model and the ≤ t−1 feature rule")
    # funnel strip
    steps = [("2,169,824", "raw DEIS rows\n673 facility IDs"), ("149,997", "facility-weeks\n663 fac. · 260 wks"),
             ("87,937 · 30,939", "train 2020–22 ·\nvalidation 2023"), ("62,635", "final refit rows\n2022–2023"),
             ("31,121", "test 2024, scored once\n633 facilities")]
    bx, bw = MARGIN, 2.25
    for i, (a, b) in enumerate(steps):
        s.text(bx, 6.0, a, size=15, weight="bold", color=INK if i != 4 else BLUE)
        s.text(bx, 5.6, b, size=9.5, color=MUTED, ls=1.2)
        if i < len(steps) - 1:
            s.text(bx + bw + 0.02, 5.95, "→", size=15, color=MUTED)
        bx += bw + 0.3
    rows = [("W1 / C1 feedback", "No causal reading of\nlockdowns or care-setting shares", "Predictive, operational framing:\nfacility-week t+2, IdCausa = 2",
             "Kept through C3; non-causal\ncaveats in NB02 §4, NB03 §5"),
            ("EDA (NB01 §2)", "2020–21 suppressed winters; 2022–24\n4.4M–5.5M resp. visits/yr; volume\n≈5/wk (CEAR) to ≈297/wk (SAR)",
             "Poisson count objective;\ntest a post-pandemic window", "Val 2023 MAE 47.45 vs 48.49;\nbias −2.46% vs −7.13%"),
            ("W2 feedback", "Week-t features are not\ncomplete on Monday", "Live DEIS probe (4 Nov 2026);\nall strict features ≤ t−1",
             "Age 1 = 17%, week t = 94.3%,\nweek t−1 = 99.1%; cost +9.75 MAE\n(37.70 → 47.45) → C3 nowcast")]
    cols = [[None, None, None, None], [None, None, None, BLUE], [None, None, None, RED]]
    yend = table(s, MARGIN, 4.85, [2.0, 3.65, 3.25, 3.2], rows, ["Trigger", "Evidence", "Decision", "Measured effect"],
          size=11, colors=cols)
    s.rect(MARGIN, 0.8, W - 2 * MARGIN, 1.0, PAPER_ALT)
    s.text(MARGIN + 0.25, 1.62, "PANEL DEFINITION AND CLEANING RULES (NB01 §1, §4)", size=9.5, weight="bold", color=MUTED)
    s.text(MARGIN + 0.25, 1.3, "One row is one public facility in one Sunday–Saturday week t; the target is respiratory visits (IdCausa = 2) in week t+2.\n"
           "Weeks with no report stay missing (never 0). Rows need 7 reported days in the target week. Split by target year; 2 duplicates removed.",
           size=10, color=INK, ls=1.3)
    deck_footer(s, P2, 2, P2_TOTAL, source="DEIS MINSAL Atenciones de Urgencia 2020–2024 (downloaded 24 Sep 2026, SHA-256 re-checked 4 Nov 2026) · no data files in repo")
    png = RENDER / "p2_02.png"; s.save(pdf, png); pngs.append(png)
    notes.append("SEBASTIÁN (~35 s). Three early decisions shaped the dataset. W1–C1 feedback removed causal claims, so the study is purely "
                 "predictive. EDA showed the pandemic regime shift and a 60-fold volume spread across care settings, which "
                 "justified a Poisson objective and testing a post-pandemic window: on Validation 2023 it lowered MAE and cut "
                 "bias from −7.1% to −2.5%. W2 feedback led to the live DEIS probe, which set the ≤ t−1 rule and measured its "
                 "cost, 9.75 MAE, which became the reason to try nowcasting in C3.")


def p2_benchmark(pdf, notes, pngs):
    s = Slide()
    p2_frame(s, 3, "NB02 §2–§3", "Benjamín",
             "A 14-model benchmark on one holdout separates the model-family gain\n(46.98 → 36.17) from the simulated nowcast gain (36.17 → 30.57)")
    ax = s.inset(MARGIN + 2.95, 1.45, 5.0, 4.6)
    rows = [("Baseline · same as week t−1", 51.32, "baseline", "51.32"),
            ("SARIMAX(1,1,1)+Fourier, top-down", 48.29, "ref", "48.29"),
            ("C2 Poisson GLM · ≤ t−1", 46.98, "ref", "46.98"),
            ("GLM oracle · complete week t*", 38.76, "oracle", "38.76"),
            ("Lag-safe XGBoost Poisson · ≤ t−1", 36.17, "model_open", "36.17"),
            ("XGB L1 oracle · complete week t*", 31.55, "oracle", "31.55"),
            ("XGBoost + sim. Chain-Ladder nowcast", 30.57, "model", "30.57")]
    n = len(rows)
    for i, (lab, v, role, txt) in enumerate(rows):
        yy = n - 1 - i
        if role == "oracle":
            ax.plot([0, v], [yy, yy], color=PALETTE["spine"], lw=1.2, ls=(0, (1, 2.5)))
            ax.plot([v], [yy], marker="|", ms=14, mew=2, color=GRAY, ls="none")
        elif role == "ref":
            ax.plot([0, v], [yy, yy], color=GRAY, lw=1.8)
            ax.plot([v], [yy], marker="o", ms=7, mfc="white", mec=GRAY, mew=1.6, ls="none")
        else:
            st = SERIES_STYLE["baseline" if role == "baseline" else "model"]
            ax.plot([0, v], [yy, yy], color=st["color"], ls=st["ls"], lw=2.6, dash_capstyle="round")
            ax.plot([v], [yy], marker=st["marker"], ms=10, mfc="white" if role != "model" else st["mfc"],
                    mec=st["color"], mew=1.9, ls="none")
        ax.text(v + 2.0, yy, txt, va="center", fontsize=10, fontweight="bold" if role in ("model", "model_open", "baseline") else "normal",
                color=BLUE if role.startswith("model") else INK)
    ax.set_yticks(range(n)); ax.set_yticklabels([r[0] for r in rows][::-1], fontsize=10)
    for t in ax.get_yticklabels():
        if "oracle" in t.get_text():
            t.set_color(GRAY); t.set_fontstyle("italic")
    ax.set_xlim(0, 60); ax.set_ylim(-0.6, n - 0.4)
    ax.set_xticks([0, 10, 20, 30, 40, 50])
    ax.set_xlabel("Test 2024 MAE (visits per facility-week) · n = 31,121", fontsize=9.5, color=MUTED)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(axis="y", length=0); ax.grid(axis="x", color=RULE); ax.set_axisbelow(True)
    # gain brackets (right side)
    def bracket(y0, y1, label, color):
        xb = 55.5
        ax.plot([xb, xb], [y0, y1], color=color, lw=1.4, clip_on=False)
        ax.plot([xb - 0.7, xb], [y0, y0], color=color, lw=1.4, clip_on=False)
        ax.plot([xb - 0.7, xb], [y1, y1], color=color, lw=1.4, clip_on=False)
        ax.text(xb + 0.9, (y0 + y1) / 2, label, va="center", fontsize=9.3, color=color, fontweight="bold", clip_on=False)
    bracket(4, 2, "model family\n−10.81 MAE", BLUE)
    bracket(2, 0, "sim. nowcast\n−5.60 MAE", BLUE)
    # right explanations
    rx = 10.35
    blocks = [("Why XGBoost > GLM", "One annual sin/cos wave cannot bend to\nthe steep May rise and June drop; trees\nlearn the shape and facility-size\ninteractions. With C2 features alone:\n38.16 (Poisson) / 37.29 (L1)."),
              ("Why SARIMAX lagged", "~2 post-pandemic cycles; d = 1 carried\na March bump into an April overshoot\nand kept the 3-week peak lag."),
              ("Why separate the two gains", "36.17 is reachable with settled data;\n30.57 depends on a simulated nowcast.\nRealistic live MAE: 30.57 to 36.17.")]
    yy = 6.0
    for t, b in blocks:
        s.text(rx, yy, t, size=11, weight="bold", color=INK)
        s.text(rx, yy - 0.33, b, size=9.2, color=INK, ls=1.25)
        yy -= 1.62
    s.text(MARGIN, 0.72, "* Oracle = complete week t, not available on Monday (upper reference, not a candidate). 7 of the 14 benchmarked models shown.",
           size=8.8, color=MUTED, style="italic")
    deck_footer(s, P2, 3, P2_TOTAL, source="Same 2022–23 refit (62,635 rows) and Test 2024 holdout for all; panel models tuned on Val 2023, SARIMAX fit directly · NB02 §2")
    png = RENDER / "p2_03.png"; s.save(pdf, png); pngs.append(png)
    notes.append("BENJAMÍN (~40 s). After the C2 feedback we added SARIMA, XGBoost and nowcasting, all on the same split "
                 "and scored once on 2024. The chart separates two effects: changing model family, GLM to XGBoost, removes "
                 "10.8 MAE with lag-safe data only; the simulated nowcast removes another 5.6. SARIMAX lost because two "
                 "post-pandemic seasons are too short and differencing amplified a March bump. We report the gains apart so the "
                 "achievable 36.17 is never confused with the simulated 30.57.")


def p2_limits(pdf, notes, pngs):
    s = Slide()
    p2_frame(s, 4, "NB02 §4, NB03 §5", "Benjamín",
             "Out-of-time testing showed four limits, and each one\nconstrains the Part 1 recommendation")
    rows = [("Simulated nowcast", "Day-level gaps were masked independently (sim. week-t WAPE 1.58%).\nBlock-correlated winter delays would push live Monday MAE\ninto 30.57 to 36.17.",
             "Use lag-safe now; pilot the\nnowcast live first."),
            ("May plateau and\nOctober overshoot", "Observed: model 182.0k (12 May) vs 183.7k (26 May), a flat plateau with a\nnominal 2-week lag; 6 Oct 147.9k vs 119.5k (+28.4k).\nInterpretation: Fourier seasonality as the cause is a hypothesis (ablation pending).",
             "Human check on peaks\nand sudden jumps."),
            ("Small care setting", "SAR, SAPU, Hospital, SUR: −36.4% to −42.4% MAE (n = 31,083).\nCEAR: n = 31 rows, about 5 visits/wk, MAE 3.0 → 5.3 (+76.9%).",
             "CEAR stays under\nmanual planning."),
            ("Scope and\nuncertainty", "Point forecasts only (no prediction intervals); the national sum hides\nfacility-level variance; one test year; predictive, not causal.",
             "Keep staffing buffers;\nno causal claims.")]
    cols = [[RED, None, BLUE], [RED, None, BLUE], [RED, None, BLUE], [INK, None, BLUE]]
    table(s, MARGIN, 5.55, [2.35, 6.75, 3.0], rows, ["Limit", "Test 2024 evidence", "Effect on Part 1"], size=11, colors=cols)
    deck_footer(s, P2, 4, P2_TOTAL, source="Test 2024 holdout (31,121 rows); observed values and interpretation kept apart; NB02 Tables 2A–2B")
    png = RENDER / "p2_04.png"; s.save(pdf, png); pngs.append(png)
    notes.append("BENJAMÍN (~30 s). Every limit here turned into a check in Part 1. The nowcast assumed independent day gaps, "
                 "which is optimistic, so we expect live error between 30.57 and 36.17. The May plateau and the October "
                 "overshoot are what we observed; blaming the Fourier terms is still only a hypothesis. CEAR is too small to "
                 "trust, and we have no prediction intervals yet. Sebastián takes the visual system.")


def p2_visual(pdf, notes, pngs):
    s = Slide()
    p2_frame(s, 5, "src/visual_system.py · NB03 §1–§4", "Sebastián",
             "One shared visual module fixed the W3 deduction by encoding\neach series with its own line style and marker")
    rows = [("Observed", "     #111827", "solid  —", "filled circle  ●"),
            ("Model", "     #0072B2", "dotted  ···", "filled diamond  ◆"),
            ("Baseline", "     #6B7280", "dashed  – –", "hollow square  □")]
    yend = table(s, MARGIN, 5.5, [1.55, 1.35, 1.55, 1.95], rows, ["SERIES_STYLE role", "Color", "Line", "Marker"], size=10.5)
    for k, col in enumerate([INK, BLUE, GRAY]):   # color swatches next to the hex codes
        s.rect(MARGIN + 1.67, 5.5 - 0.36 - 0.27 - k * 0.3995, 0.17, 0.17, col, z=3)
    s.text(MARGIN, yend - 0.2,
           "Shared rules applied in all views:\n"
           "• 5-role palette: observed, model, nowcast, baseline, alert\n"
           "• red reserved for risk: excluded data, under-forecast, CEAR\n"
           "• zero-based magnitude axes (0–100%, 0–235k, 0–100 MAE)\n"
           "• one-row legend above the plot, plus direct end labels\n"
           "• title states the finding; subtitle gives n and period; footer the caveat",
           size=10.3, color=INK, ls=1.38)
    # right: W3 fix with grayscale proof
    rx = 7.35; rw = W - MARGIN - rx
    s.card(rx, 0.95, rw, 4.6, fc=PAPER, ec=RULE, lw=1.0)
    s.text(rx + 0.25, 5.3, "W3 feedback, criterion C (−7.5)", size=12, weight="bold", color=RED)
    s.text(rx + 0.25, 4.92, "\"Observed and model share a solid circle and a solid line in V2.\"\nSuggested: different line types (solid and dotted).",
           size=9.6, color=INK, ls=1.3, style="italic")
    # before/after grayscale proof
    import numpy as np
    xs = np.linspace(0, 1, 40)
    obs = 0.5 + 0.35 * np.exp(-((xs - 0.45) / 0.12) ** 2)
    mod = 0.5 + 0.30 * np.exp(-((xs - 0.50) / 0.14) ** 2)
    for j, (lab, fixed) in enumerate([("W3 v2 (before)", False), ("C3 (after), shown in grayscale", True)]):
        ax = s.inset(rx + 0.3 + j * (rw - 0.4) / 2, 1.78, (rw - 0.8) / 2, 2.1)
        ax.set_xlim(-0.02, 1.02); ax.set_ylim(0.3, 1.0); ax.axis("off")
        if fixed:
            ax.plot(xs, obs, color="#222222", ls="-", lw=2.4)
            ax.plot(xs, mod, color="#555555", ls=":", lw=2.6, dash_capstyle="round")
            ax.plot([0.45], [0.85], marker="o", ms=8, color="#222222", ls="none")
            ax.plot([0.50], [0.80], marker="D", ms=8, color="#555555", mec="white", ls="none")
        else:
            ax.plot(xs, obs, color=INK, ls="-", lw=2.4)
            ax.plot(xs, mod, color=BLUE, ls="-", lw=2.2)
            ax.plot([0.45], [0.85], marker="o", ms=8, color=INK, ls="none")
            ax.plot([0.50], [0.80], marker="o", ms=8, color=BLUE, mec="white", ls="none")
        ax.text(0.0, 0.33, lab, fontsize=9.3, fontweight="bold", color=RED if not fixed else BLUE)
    s.text(rx + 0.25, 1.62, "Fix: SERIES_STYLE with series_line, series_marker and series_handle,\n"
           "used in both View 2 panels, the peak markers, legend and end labels.\n"
           "View 3 reuses the model diamond.", size=9.0, color=INK, ls=1.3)
    deck_footer(s, P2, 5, P2_TOTAL, source="Editable sources: src/visual_system.py, notebooks/03_visual_system_and_redesigns.ipynb, presentation/build_presentations.py")
    png = RENDER / "p2_05.png"; s.save(pdf, png); pngs.append(png)
    notes.append("SEBASTIÁN (~35 s). Every chart in the notebooks and in these slides comes from one module. In W3 we lost 7.5 points here: in View 2 "
                 "observed and model were both solid lines with circles, so only color separated them. We now define each "
                 "series once in SERIES_STYLE: observed solid with circles, model dotted with diamonds, baseline dashed with "
                 "hollow squares. On the right, the fixed version still reads in pure grayscale.")


def p2_evolution(pdf, notes, pngs):
    s = Slide()
    p2_frame(s, 6, "README §4", "Sebastián",
             "How course feedback shaped the study, and which\ndesign choices held up")
    colw = (W - 2 * MARGIN - 0.5) / 2
    s.text(MARGIN, 5.75, "CHANGED AFTER FEEDBACK", size=10.5, weight="bold", color=BLUE)
    s.hline(MARGIN, MARGIN + colw, 5.5, color=BLUE, lw=1.4)
    changed = [("W1/C1", "Dropped causal claims; scoped to operational forecasting."),
               ("W2", "Probed the live DEIS lag; strict features only up to t−1."),
               ("C2", "Chose the post-pandemic window on Val 2023; refit 2022–23."),
               ("C2→C3", "Added SARIMA, XGBoost and nowcasting (14 models),\nreporting the two gains separately."),
               ("W3", "Kept the W3 v2 views (final model) and added the\nsolid / dotted / dashed encoding for the −7.5 fix.")]
    yy = 5.25
    for tag, txt in changed:
        s.text(MARGIN, yy, tag, size=10.5, weight="bold", family="DejaVu Sans Mono", color=BLUE)
        s.text(MARGIN + 1.05, yy, txt, size=10.8, color=INK, ls=1.25)
        yy -= 0.8 if "\n" in txt else 0.55
    x1 = MARGIN + colw + 0.5
    s.text(x1, 5.75, "KEPT, BECAUSE THE EVIDENCE HELD", size=10.5, weight="bold", color=INK)
    s.hline(x1, x1 + colw, 5.5, color=INK, lw=1.4)
    kept = [("Unit", "Facility-week, t+2 respiratory visits, Monday decision."),
            ("Split", "Chronological 2020–22 / 2023 / 2024; test scored once."),
            ("Objective", "Poisson count loss for skewed volumes (≈5 to ≈297/wk)."),
            ("Baseline", "\"Same as week t−1\" as the fair, lag-safe reference."),
            ("Visuals", "5-role palette, zero-based axes, top legends in all views.")]
    yy = 5.25
    for tag, txt in kept:
        s.text(x1, yy, tag, size=10.5, weight="bold", color=INK)
        s.text(x1 + 1.15, yy, txt, size=10.8, color=INK, ls=1.25)
        yy -= 0.62
    s.rect(MARGIN, 0.85, W - 2 * MARGIN, 0.95, PAPER_ALT)
    s.text(MARGIN + 0.25, 1.6, "How the headline result moved (Test 2024 MAE)", size=10, weight="bold", color=MUTED)
    s.text(MARGIN + 0.25, 1.22, "51.32 baseline  →  46.98 C2 GLM (−8.5%)  →  36.17 lag-safe XGBoost (−29.5%)  →  30.57 with simulated nowcast (−40.4%)",
           size=11.3, weight="bold", color=INK)
    deck_footer(s, P2, 6, P2_TOTAL, source="Feedback log: README §4; each row links to NB01–NB03 sections")
    png = RENDER / "p2_06.png"; s.save(pdf, png); pngs.append(png)
    notes.append("SEBASTIÁN (~30 s). Feedback changed our claims, the input cutoff, the training window, the model set and the "
                 "chart encoding. For W3 we kept the v2 views, which use the final model, and fixed the line styles. Other "
                 "choices held up under the evidence: the facility-week unit, the chronological split, the Poisson loss and the "
                 "lag-safe baseline. The headline number went from 51.32 to 36.17 with settled data, and 30.57 with the simulated nowcast.")


def p2_learning(pdf, notes, pngs):
    s = Slide()
    p2_frame(s, 7, "NB03 §5 · README §6", "Benjamín",
             "Reporting lag mattered as much as model choice.\nNext: test the nowcast on real Monday data.")
    colw = (W - 2 * MARGIN - 0.4) / 2
    s.text(MARGIN, 5.75, "WHAT WE LEARNED", size=10.5, weight="bold", color=INK)
    s.hline(MARGIN, MARGIN + colw, 5.5, color=INK, lw=1.4)
    learned = [("Check what data exists on Monday first.", "Using week t as if it were complete hid a\n+9.75 MAE gap (Val 2023)."),
               ("Report the two gains separately.", "XGBoost (−10.81 MAE) is achievable now;\nthe extra −5.60 is still simulated."),
               ("Put visual rules in shared code.", "One module kept 3 views and both\npresentations consistent, so the W3 fix reached every chart.")]
    yy = 5.25
    for t, b in learned:
        s.text(MARGIN, yy, t, size=12, weight="bold", color=INK)
        s.text(MARGIN, yy - 0.35, b, size=10.8, color=INK, ls=1.25)
        yy -= 1.18
    x1 = MARGIN + colw + 0.4
    s.text(x1, 5.75, "NEXT IMPROVEMENTS", size=10.5, weight="bold", color=BLUE)
    s.hline(x1, x1 + colw, 5.5, color=BLUE, lw=1.4)
    nxt = [("1  Live Monday archive", "Save each Monday DEIS download for one\nwinter and measure the real nowcast error."),
           ("2  Intervals and an ablation", "Quantile intervals (80/95%); ablate Fourier\nterms to test the 6 Oct overshoot."),
           ("3  Relative error by setting", "Add WAPE % next to MAE so SAR and SUR\nare compared fairly.")]
    yy = 5.25
    for t, b in nxt:
        s.text(x1, yy, t, size=12, weight="bold", color=BLUE)
        s.text(x1 + 0.3, yy - 0.35, b, size=10.8, color=INK, ls=1.25)
        yy -= 1.18
    s.card(MARGIN, 0.8, W - 2 * MARGIN, 1.15, fc=PAPER_ALT, ec=RULE, lw=1.0)
    s.text(MARGIN + 0.25, 1.75, "AI USE (COURSE POLICY)", size=9.5, weight="bold", color=MUTED)
    s.text(MARGIN + 0.25, 1.45,
           "Gemini (Antigravity) and Claude helped draft Python code (benchmark, visual system, notebooks, these slides), check rubric alignment and\n"
           "proofread English. Both authors verified every number, split, lag check, design rule and limitation, and approved the final content.",
           size=9.8, color=INK, ls=1.3)
    deck_footer(s, P2, 7, P2_TOTAL, source="Group 02: Benjamín Pinto and Sebastián Herrera, IIB423T-1 Business Intelligence, C3")
    png = RENDER / "p2_07.png"; s.save(pdf, png); pngs.append(png)
    notes.append("BENJAMÍN (~35 s). The biggest lesson was that checking what data actually exists on Monday mattered as "
                 "much as picking the model. We also learned to keep simulated gains apart from real ones, and to put visual "
                 "rules in shared code. The most practical next step is saving real Monday DEIS downloads for one winter, "
                 "then adding prediction intervals and testing the Fourier terms behind the October overshoot. On AI: Gemini "
                 "and Claude helped draft code, check the rubric and proofread; Sebastián and I verified every number and "
                 "limitation. Happy to take your questions.")


def p2_divider(pdf, notes, pngs):
    """Section break between the two presentations (same file, two clearly marked parts)."""
    s = Slide(dark=True)
    s.rect(0, H - 0.09, W, 0.09, PAPER)
    s.text(MARGIN, H - 0.75, "PART 2 OF 2", size=11.5, color=DARK_MUTED, weight="bold")
    s.text(MARGIN, H - 2.1, "Presentation 2\nInternal Review", size=46, weight="bold", ls=1.08)
    s.text(MARGIN, H - 4.35,
           "Audience: the instructor as reviewer. The same study, traced back through\n"
           "the data, the models, the evaluation and the visual decisions behind Part 1.",
           size=17, color="#D1D5DB", ls=1.35)
    s.text(MARGIN, 0.55, "Group 02, IIB423T-1 Business Intelligence, C3", size=10, color=DARK_MUTED, va="bottom")
    s.text(W - MARGIN, 0.55, "SEBASTIÁN", size=9.5, color=DARK_MUTED, weight="bold", ha="right", va="bottom")
    png = RENDER / "p2_00.png"; s.save(pdf, png); pngs.append(png)
    notes.append("SEBASTIÁN (~5 s). That was the brief for the operations team. For the review, here is how the data, "
                 "the models and the visual choices produced those numbers.")


def build(slides, stem):
    notes, pngs = [], []
    pdf_path = OUT / f"{stem}.pdf"
    with PdfPages(pdf_path) as pdf:
        for fn in slides:
            fn(pdf, notes, pngs)
        d = pdf.infodict()
        d["Title"] = "Group 02 · C3 · Presentation 1 (Audience) and Presentation 2 (Internal Review)"
        d["Author"] = "Group 02 · Benjamín Pinto & Sebastián Herrera"
    export_pptx(pngs, notes, OUT / f"{stem}.pptx")
    return pdf_path, pngs


if __name__ == "__main__":
    # One file, two clearly marked parts: Part 1 = Presentation 1 (Audience), Part 2 = Presentation 2 (Internal Review)
    out, _ = build([p1_cover, p1_situation, p1_complication, p1_resolution, p1_national, p1_settings, p1_action,
                    p2_divider,
                    p2_bridge, p2_data, p2_benchmark, p2_limits, p2_visual, p2_evolution, p2_learning],
                   "GROUP_02_C3_Presentations")
    print("Built:", out.name)
