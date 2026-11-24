# C3 · Integrated BI Study: Lag-Safe & Nowcasted Respiratory Emergency Forecasting in Chile

**Course:** Business Intelligence · IIB423T-1 (Universidad del Desarrollo)  
**Instructor:** Tomás Fontecilla  
**Assessed Version:** `v1.0 — Final C3 Submission`  
**Team:** Group 02 — **Benjamín Pinto** & **Sebastián Herrera**

---

## 1. Study Question & Operational Decision

> **Operational Question:** On **Monday morning** after calendar week $t$ closes, how accurately can Chile's public emergency network (`MINSAL / Servicios de Salud`) forecast **facility-level weekly respiratory emergency visits (`IdCausa = 2`) two weeks ahead ($t+2$)** across `633` public emergency facilities—respecting real DEIS publication lag—to guide shift reinforcement and surge monitoring?

* **Simulated External Audience:** MINSAL and Servicio de Salud **Emergency Network Operations Managers** running the Monday-morning staffing and surge-readiness meeting.
* **Key Result:** Starting from a lag-safe naive baseline (`same as week t-1`, **Test 2024 MAE = `51.32` visits/facility-week**, `WAPE = 29.31%`):
  * **C2 Frozen Poisson GLM (`<= t-1`)** reduced MAE to **`46.98`** (`-8.5%`, `WAPE = 26.83%`, `Bias = -0.56%`), but peaked **3 weeks late** (`2 Jun` vs. `12 May 2024`).
  * **Top-Down SARIMAX(1,1,1) + Fourier (`<= t-1`)** scored **`48.29`** (`-5.9%` vs. baseline), underperforming global panel models due to `d=1` overshoot after early-season bumps.
  * **Lag-Safe XGBoost Poisson (`<= t-1`, engineered features)** reduced MAE to **`36.17`** (`-29.5%` vs. baseline, `WAPE = 20.66%`, `0-week` peak lag) without any nowcasting.
  * **XGBoost Poisson + Simulated Monday Chain-Ladder Nowcast** (recovering 94.3%-complete partial week $t$ under independent day-level gaps) reached **`30.57`** (`-40.4%` vs. baseline, `WAPE = 17.46%`, `Bias = +1.79%`, flat May plateau `182.0k` on `12 May` vs. `183.7k` on `26 May`).

---

## 2. Repository Structure & Reading Order

**No installation, code execution, or data download is required to assess this repository.** Every notebook in `notebooks/` is saved **fully executed** with all explanations, compact summary tables, metrics, assertions, and inline high-resolution plots visible directly alongside the code that produced them.

**Recommended reading order:**

| Order | File | Role in the Pipeline |
|---:|---|---|
| **1** | [`notebooks/01_data_eda_and_preparation.ipynb`](notebooks/01_data_eda_and_preparation.ipynb) | **Data Provenance, EDA, Quality Audit, DEIS Lag Probe & Chronological Split.** Documents exact DEIS sources, unit of analysis, distributions, quality checks (duplicates, missing weeks, spikes), empirical Monday publication-lag audit (`4 Nov 2026`), row/feature impact of every cleaning step, and the strict chronological out-of-time split (`2020–2022` / `2023` / `2024`). |
| **2** | [`notebooks/02_modeling_nowcasting_and_eval.ipynb`](notebooks/02_modeling_nowcasting_and_eval.ipynb) | **Model Benchmark, Simulated Monday Nowcasting & Out-of-Time Evaluation.** Evaluates the post-pandemic training window choice on Validation 2023 (`2022-only` vs. `2020–2022`), quantifies the cost of publication lag, and benchmarks **14 models** on Test 2024 (`n = 31,121` rows): Naive Baseline, C2 Poisson GLM, Top-Down SARIMAX+Fourier, Lag-Safe XGBoost, Simulated Monday Nowcasting (`Sun–Thu` & `Chain-Ladder`), and the unattainable Complete-Week-$t$ Oracle ceiling. Includes care-setting breakdown, peak timing, and honest limitations. |
| **3** | [`notebooks/03_visual_system_and_redesigns.ipynb`](notebooks/03_visual_system_and_redesigns.ipynb) | **Applied Visual System & Before-and-After Redesigns (W3 Integration).** Imports [`src/visual_system.py`](src/visual_system.py) to generate and display all **3 final W3 v2 views** and all **3 Before-and-After pairs** inline, documents Audience/Tasks (Class 09 verbs), shared visual rules (palette, non-color redundancy, top-bar legend, zero-based scales), and the 4-part **Limitation → Possible Misunderstanding → Reason to Keep → Next Improvement** audit for each view. |
| — | [`src/visual_system.py`](src/visual_system.py) | Shared Python design-system module (`PALETTE`, `SERIES_STYLE` + `series_line()`/`series_marker()`/`series_handle()`, `apply_system_rc()`, `style_axes()`, `add_header_footer()`, `add_top_legend()`) used by Notebook 03 so all final charts enforce identical visual semantics. |
| — | `figures/` | Final exported 300-dpi PNGs and editable vector SVGs generated directly by Notebook 03 (exact visual match to notebook inline outputs and presentation slides). |
| **4** | [`presentation/GROUP_02_C3_Presentations.pdf`](presentation/GROUP_02_C3_Presentations.pdf) (+ `.pptx` with speaker notes) | **Both presentations in one file, two clearly marked parts.** Part 1, slides 1–7: **Presentation 1 · Audience**, a Monday staffing brief for MINSAL / Servicio de Salud Emergency Network Operations Managers (Situation → Complication → Resolution, answer first, ≈3.5 min). Slide 8: divider. Part 2, slides 9–15: **Presentation 2 · Internal Review** for the instructor (decision chain with notebook § citations, W3 fix, limits, learning, next steps, AI statement, ≈4 min). |
| — | [`presentation/build_presentations.py`](presentation/build_presentations.py), [`presentation/slide_kit.py`](presentation/slide_kit.py) | Editable source of the presentation file. Slides are drawn with matplotlib on top of `src/visual_system.py` (same palette, `SERIES_STYLE`, typography) and embed the three final `figures/`; run `python presentation/build_presentations.py` to rebuild the PDF and PPTX. |

---

## 3. Data Provenance & No-Data-Files Policy

Per C3 rubric policy, **no raw datasets, curated datasets, or CSV data extracts are included in this repository**. All results are preserved via compact summary tables and embedded figures inside the executed notebooks.

* **Primary Official Source:** Departamento de Estadísticas e Información de Salud (DEIS), Ministerio de Salud de Chile (MINSAL) — *Atenciones de Urgencia* (daily emergency visits by facility and cause, `IdCausa = 1` total visits, `IdCausa = 2` total respiratory visits):
  * Portal: `https://deis.minsal.cl/#datosabiertos` (Atenciones de Urgencia 2020–2026 archives).
* **Scope & Snapshot Dates:**
  * Modeling panel (`2020–2024`): downloaded `24 Sep 2026` (SHA-256 verified unchanged on `4 Nov 2026`); `260` complete Sunday–Saturday weeks across `663` public emergency facilities (`149,997` eligible facility-week modeling rows after strict lag-safe filtering).
  * Empirical publication-lag probe: live `2026` DEIS archive downloaded on `Wed 4 Nov 2026` (last reporting date `2026-11-03`), compared against the `2025` same-weekday baseline (`n ≈ 626` facilities/day).

---

## 4. Traceable Decisions & Instructor Feedback Log (Criterion D)

| Stage | Instructor Feedback / Empirical Finding | Decision Made & Evidence in Repository |
|---|---|---|
| **W1 / C1** | Do not infer causal effects of lockdowns/reopenings; primary/hospital correlation reflects shared seasonality; panel stability does not prove epidemiological causation. | Reframed study strictly as **predictive operational forecasting** (no causal claims on coefficients or care-setting shares; explicit non-causal caveats in NB02 & NB03). |
| **W2** | Features dated at week $t$ are **not operationally complete on Monday morning** due to DEIS reporting delay. | Conducted live DEIS archive probe (`4 Nov 2026`, NB01 §4): Age 1 = `17%`, Age 2 (Sat of week $t$) = `82%`, Week $t$ avg = `94.3%`, Week $t-1$ avg = `99.1%`. Shifted all strict lag-safe features to `<= t-1` (cost on Val 2023 = `+9.75` MAE, NB02 §3). |
| **C2** | Pandemic years (`2020–2021`) distort post-pandemic respiratory levels; keep evaluation leak-free. | Selected **post-pandemic training window (`2022-only`)** on Validation 2023 (`MAE 47.45` vs. `48.49`; `Bias -2.46%` vs. `-7.13%`), froze spec, refitted on `2022–2023` (`62,635` rows), and scored Test 2024 (`31,121` rows) once (`MAE 46.98` vs. `51.32`). |
| **C2 Feedback** | Test additional model families (**SARIMA** and **XGBoost**) and explore **nowcasting** to recover the DEIS lag penalty. | Benchmarked **14 models** on the exact same chronological split (NB02 §4–§5): Top-Down SARIMAX+Fourier (`48.29`), Lag-Safe XGBoost (`36.17`, `0-wk` peak lag), and **XGBoost Poisson + Simulated Monday Chain-Ladder Nowcast (`30.57`, `-40.4%`)**, clearly separating XGBoost's gain from simulated nowcasting's gain. |
| **W3 → C3** | Unify separate charts into one colorblind-safe visual system with transparent caveats; avoid overstating simulated nowcast or unproven causal causes of the Oct overshoot. | Implemented [`src/visual_system.py`](src/visual_system.py) with 5-role semantic palette, non-color redundancy (`X`, `D`, `o`, `s`, `^`, hatching), uniform frameless top-bar legends across all 3 views, neutral slate vs. red residual shading, factual `6 Oct` overshoot label (`+28.4k`), and explicit May plateau (`182.0k` vs. `183.7k`) & Wednesday-to-Monday probe re-mapping notes (NB03). |
| **W3 Feedback (C, −7.5)** | System explicit, but in View 2 *Observed* and *Model* shared a solid line and a filled circle, weakening non-color redundancy despite labels. Suggestion: use different line types (solid vs. dotted). | Added a shared `SERIES_STYLE` role table and helpers (`series_line`, `series_marker`, `series_handle`) to [`src/visual_system.py`](src/visual_system.py): **Observed = solid + `●`**, **Model = dotted + `◆`**, **Baseline = dashed + `□`**. View 2 uses these roles in both panels, at the peak markers, in the legend and in the direct end labels. View 3 reuses the model diamond so Views 2–3 share one series encoding. Rule table and fix note are in NB03 §1 and §3; figures were regenerated in `figures/`. |

---

## 5. Team Contributions & Software

* **Benjamín Pinto:** Led C3 model-expansion & nowcasting experiments (`XGBoost`, `SARIMAX+Fourier`, `Sun–Thu` & `Chain-Ladder` Monday nowcasting), initial W3 visual system design & PDF automation, C2/C3 pipeline verification, and C3 notebook integration.
* **Sebastián Herrera:** Led C1/W2/C2 data engineering, DEIS publication-lag probe & lag-safe panel construction, W3 methodological & visual audit (separating XGBoost vs. simulated nowcast gains, removing causal overclaims on the Oct overshoot, uniform top-bar legend, portable relative-path refactoring), and C3 validation.
* **Shared:** Study framing, operational audience & narrative design, visual system review, and full-study defense preparation.
* **Software & Main Libraries:** `Python 3.14` (`numpy`, `pandas`, `scikit-learn`, `xgboost`, `statsmodels`, `matplotlib`, `nbformat`, `nbclient`, `python-pptx` for the slide export). See [`requirements.txt`](requirements.txt).

---

## 6. AI Usage Statement

Generative AI tools (Gemini / Antigravity and Claude) were used to assist in drafting Python code for the modeling benchmark, visual system module, notebook assembly, and the slide-building script for both presentations, checking alignment with the course rubrics (Classes 01–14), and proofreading English prose. All empirical numbers, chronological split assertions, lag-safety checks, model comparisons, visual design rules, and analytical limitations were programmatically verified and approved by both authors.
