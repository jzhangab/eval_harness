"""Generate a block diagram for the eval_harness notebook — max 800px wide."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

# 800 px wide @ 100 dpi = 8 inches
W, H = 8, 26
DPI  = 100

fig, ax = plt.subplots(figsize=(W, H))
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis("off")
fig.patch.set_facecolor("#F8F9FA")

# ── Palette ────────────────────────────────────────────────────────────────
C_HDR  = "#1A3A5C"
C_CFG  = "#2E6DA4"
C_M1   = "#1B7340"
C_M2   = "#8B4A00"
C_M3   = "#6B2D8B"
C_DAT  = "#C0392B"
C_ARR  = "#555555"
C_PAR  = "#E8F4E8"

# Usable x-range
LM, RM = 0.3, 7.7          # left / right margin
CW     = RM - LM           # 7.4  — full content width
MID    = LM + CW / 2       # 4.0  — horizontal centre

# Two-column split inside modules
COL1_W = 4.1               # main-flow column width
COL2_X = LM + COL1_W + 0.2  # dataset column start  (4.6)
COL2_W = RM - COL2_X        # 3.1


# ── Helpers ────────────────────────────────────────────────────────────────
def box(x, y, w, h, label, sublabel=None,
        fc="#FFF", ec="#333", lw=1.4,
        fs=10, sfs=8, bold=True, r=0.18, tc="#1A1A1A"):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.04,rounding_size={r}",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=3))
    cy = y + h/2 + (0.15 if sublabel else 0)
    ax.text(x + w/2, cy, label, ha="center", va="center",
            fontsize=fs, fontweight="bold" if bold else "normal",
            color=tc, zorder=4)
    if sublabel:
        ax.text(x + w/2, y + h/2 - 0.18, sublabel, ha="center", va="center",
                fontsize=sfs, style="italic", color=tc, zorder=4)


def hdr(x, y, w, h, text, fc):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.04,rounding_size=0.12",
        facecolor=fc, edgecolor=fc, linewidth=0, zorder=3))
    ax.text(x + w/2, y + h/2, text, ha="center", va="center",
            fontsize=11, fontweight="bold", color="white", zorder=4)


def arr(x1, y1, x2, y2, c=C_ARR, lw=1.6, label=None, style="-|>"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=c, lw=lw,
                                mutation_scale=14), zorder=5)
    if label:
        ax.text((x1+x2)/2 + 0.12, (y1+y2)/2, label,
                fontsize=7.5, color=c, zorder=6)


def darr(x1, y1, x2, y2, c):
    """Double-headed (bidirectional) arrow."""
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="<->", color=c, lw=1.5,
                                mutation_scale=14), zorder=5)


# ═══════════════════════════════════════════════════════════════════════════
# Title
# ═══════════════════════════════════════════════════════════════════════════
box(LM, 24.95, CW, 0.85,
    "eval_harness — Clinical Trial Protocol Evaluation Pipeline",
    sublabel="Dataiku DSS Notebook  ·  eval_harness.ipynb",
    fc=C_HDR, ec=C_HDR, tc="white", fs=12, sfs=8.5, r=0.25)

# ═══════════════════════════════════════════════════════════════════════════
# Section 0 — Configuration
# ═══════════════════════════════════════════════════════════════════════════
hdr(LM, 24.1, CW, 0.42, "Section 0 — Setup & Configuration", C_CFG)

for i, (lbl, sub) in enumerate([
    ("API_ENDPOINT / API_KEY",        "Custom parsing API credentials"),
    ("LLM_CONNECTION_ID",             "Dataiku LLM Mesh connection ID"),
    ("MAX_WORKERS  (M1=4, M2=4, M3=2)", "ThreadPoolExecutor concurrency"),
]):
    box(LM, 23.3 - i*0.72, CW, 0.6, lbl, sublabel=sub,
        fc="#EAF2FB", ec=C_CFG, fs=9, sfs=7.8)

# ═══════════════════════════════════════════════════════════════════════════
# Parallel swim-lane background
# ═══════════════════════════════════════════════════════════════════════════
SWIM_TOP = 21.55
SWIM_BOT =  9.55
ax.add_patch(FancyBboxPatch(
    (LM - 0.05, SWIM_BOT), CW + 0.1, SWIM_TOP - SWIM_BOT,
    boxstyle="round,pad=0.04,rounding_size=0.18",
    facecolor=C_PAR, edgecolor="#A8D5A2", linewidth=1.1, zorder=1))
ax.text(MID, SWIM_TOP - 0.18,
        "Parallel Execution  (concurrent.futures.ThreadPoolExecutor)",
        ha="center", va="center", fontsize=8, color="#1B7340",
        style="italic", zorder=2)

# ═══════════════════════════════════════════════════════════════════════════
# Module 1 — Protocol Ingestion
# ═══════════════════════════════════════════════════════════════════════════
hdr(LM, 21.0, CW, 0.42, "Module 1 — Protocol Ingestion", C_M1)

# Row 1: Input  →  parse_document()
box(LM,       20.05, 1.9,  0.75, "Input Files", sublabel=".pdf | .docx",
    fc="#E8F8EE", ec=C_M1, fs=8.5, sfs=7.5)
arr(LM+1.9,   20.42, LM+2.1, 20.42)
box(LM+2.1,   20.05, 5.3,  0.75, "parse_document(file_path)",
    sublabel="multipart POST  ·  Bearer token auth  ·  per-file error isolation",
    fc="#E8F8EE", ec=C_M1, fs=9, sfs=7.5)

# Row 2: run_module1  |  dataset
arr(LM+1.05, 20.05, LM+1.05, 19.7)   # input → run_module1
arr(LM+4.75, 20.05, LM+4.75, 19.7)   # parse_doc → run_module1

box(LM,       19.1, COL1_W, 0.65, "run_module1(file_paths)",
    sublabel="futures fan-out · aggregate results",
    fc="#C8EDD8", ec=C_M1, fs=9.5)
box(COL2_X,   19.1, COL2_W, 0.65, "protocol_parsed_json",
    sublabel="protocol_id · raw_json · status",
    fc="#FDECEA", ec=C_DAT, fs=8.5, sfs=7.5, bold=False, tc=C_DAT)
arr(LM+COL1_W, 19.42, COL2_X, 19.42, c=C_DAT, label="write")

# M1 → M2
arr(MID, 19.1, MID, 18.75, lw=2.0)

# ═══════════════════════════════════════════════════════════════════════════
# Module 2 — Section Content Generation
# ═══════════════════════════════════════════════════════════════════════════
hdr(LM, 18.3, CW, 0.42, "Module 2 — Section Content Generation", C_M2)

# Row 1: Input  →  generate_section()
box(LM,      17.3, 2.5, 0.8, "Input DataFrame",
    sublabel="protocol_id · indication\nage_group · section_id · prompt",
    fc="#FFF3E8", ec=C_M2, fs=8.5, sfs=7.5)
arr(LM+2.5,  17.7, LM+2.7, 17.7)
box(LM+2.7,  17.3, 4.7, 0.8, "generate_section(row, llm)",
    sublabel="build_generation_prompt()  →  LLM Mesh  →  HTML",
    fc="#FFF3E8", ec=C_M2, fs=9, sfs=7.5)

# LLM Mesh (below generate_section, bidirectional)
box(LM+2.7,  16.45, 3.1, 0.55, "Dataiku LLM Mesh",
    fc="#FFF0D0", ec="#CC8800", fs=8.5, bold=False)
darr(LM+4.25, 17.3, LM+4.25, 17.0, c="#CC8800")

# Row 2: run_module2  |  dataset
arr(LM+1.25, 17.3, LM+1.25, 16.25)   # input → run_module2
arr(LM+5.05, 17.3, LM+5.05, 16.25)   # gen_section → run_module2

box(LM,       15.85, COL1_W, 0.65, "run_module2(df)",
    sublabel="parallel generation · append generated_html",
    fc="#FFE0C0", ec=C_M2, fs=9.5)
box(COL2_X,   15.85, COL2_W, 0.65, "sections_generated",
    sublabel="+ generated_html column",
    fc="#FDECEA", ec=C_DAT, fs=8.5, sfs=7.5, bold=False, tc=C_DAT)
arr(LM+COL1_W, 16.17, COL2_X, 16.17, c=C_DAT, label="write")

# M2 → M3
arr(MID, 15.85, MID, 15.5, lw=2.0)

# ═══════════════════════════════════════════════════════════════════════════
# Module 3 — Evaluation Scoring
# ═══════════════════════════════════════════════════════════════════════════
hdr(LM, 15.05, CW, 0.42, "Module 3 — Evaluation Scoring  (LLM-as-Judge)", C_M3)

# Row 1: Input  →  score_section()
box(LM,      14.05, 2.5, 0.8, "Input DataFrame",
    sublabel="protocol_id · section_id\noriginal_text · generated_text",
    fc="#F5EEF8", ec=C_M3, fs=8.5, sfs=7.5)
arr(LM+2.5,  14.45, LM+2.7, 14.45)
box(LM+2.7,  14.05, 4.7, 0.8, "score_section(row, llm)",
    sublabel="build_scoring_prompt()  →  LLM Mesh  →  parse JSON",
    fc="#F5EEF8", ec=C_M3, fs=9, sfs=7.5)

# LLM Mesh
box(LM+2.7,  13.2, 3.1, 0.55, "Dataiku LLM Mesh",
    fc="#F0E8FB", ec="#7B3FA0", fs=8.5, bold=False)
darr(LM+4.25, 14.05, LM+4.25, 13.75, c="#7B3FA0")

# Row 2: run_module3  |  dataset
arr(LM+1.25, 14.05, LM+1.25, 13.0)
arr(LM+5.05, 14.05, LM+5.05, 13.0)

box(LM,       12.6, COL1_W, 0.65, "run_module3(df)",
    sublabel="JSON parse · regex fallback · expand score columns",
    fc="#E8D5F5", ec=C_M3, fs=9.5)
box(COL2_X,   12.6, COL2_W, 0.65, "eval_scores",
    sublabel="+ 7 score/rationale cols",
    fc="#FDECEA", ec=C_DAT, fs=8.5, sfs=7.5, bold=False, tc=C_DAT)
arr(LM+COL1_W, 12.92, COL2_X, 12.92, c=C_DAT, label="write")

# ═══════════════════════════════════════════════════════════════════════════
# Scoring Dimensions
# ═══════════════════════════════════════════════════════════════════════════
ax.add_patch(FancyBboxPatch(
    (LM, 8.85), CW, 3.5,
    boxstyle="round,pad=0.04,rounding_size=0.15",
    facecolor="#FAFAFA", edgecolor="#CCCCCC", linewidth=1.1, zorder=1))
ax.text(MID, 12.2, "Module 3 — Scoring Dimensions",
        ha="center", va="center", fontsize=10.5,
        fontweight="bold", color=C_M3, zorder=4)

for i, (title, desc) in enumerate([
    ("Content Accuracy  (1–10)",
     "Factual fidelity — does the generated text correctly represent\nclinical facts from the original?  (rubric: 1=poor · 5=acceptable · 10=excellent)"),
    ("Completeness  (1–10)",
     "Coverage — are all key criteria, endpoints, and statements\nfrom the original present in the generated text?"),
    ("Reading Grade Level  (Flesch-Kincaid)",
     "Estimated FK grade level for original vs generated text,\nplus delta and rationale column."),
]):
    box(LM, 11.55 - i*0.88, CW, 0.72, title, sublabel=desc,
        fc="#F3EAF8", ec=C_M3, fs=9, sfs=7.8)

# ═══════════════════════════════════════════════════════════════════════════
# Footer
# ═══════════════════════════════════════════════════════════════════════════
ax.text(MID, 8.5,
        "Aggregate summary: mean scores per protocol_id rendered as a styled HTML table",
        ha="center", va="center", fontsize=8, color="#555", style="italic")
ax.text(MID, 8.1,
        "github.com/jzhangab/eval_harness  ·  eval_harness.ipynb",
        ha="center", va="center", fontsize=7.5, color="#888")

# Legend
legend_items = [
    mpatches.Patch(facecolor=C_CFG, label="Configuration"),
    mpatches.Patch(facecolor=C_M1,  label="Module 1: Ingestion"),
    mpatches.Patch(facecolor=C_M2,  label="Module 2: Generation"),
    mpatches.Patch(facecolor=C_M3,  label="Module 3: Scoring"),
    mpatches.Patch(facecolor=C_DAT, label="Dataiku Datasets"),
    mpatches.Patch(facecolor=C_PAR, label="Parallel zone",
                   edgecolor="#A8D5A2", linewidth=1),
]
ax.legend(handles=legend_items, loc="lower center",
          bbox_to_anchor=(MID/W, 0.005),
          fontsize=8, framealpha=0.9, edgecolor="#CCC", ncol=3)

plt.savefig("eval_harness_diagram.pdf", format="pdf",
            dpi=DPI, facecolor=fig.get_facecolor())
plt.savefig("eval_harness_diagram.png", format="png",
            dpi=DPI, facecolor=fig.get_facecolor())
print("Saved PDF and PNG.")
