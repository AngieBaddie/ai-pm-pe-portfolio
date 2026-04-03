# app.py
# Streamlit dashboard — the main UI for the Copilot Readiness Analyzer.
# Run with: streamlit run app.py

import streamlit as st
from data.sample_connector import get_sample_reports
from scoring.engine import score_all_reports
from ai_layer.recommendations import get_recommendations, get_report_summary

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Copilot Readiness Analyzer",
    page_icon="⚡",
    layout="wide"
)

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown("""
    <style>
    .main { background-color: #f5f7fa; }
    .score-high { color: #1a7a4a; font-weight: bold; font-size: 1.4rem; }
    .score-mid  { color: #b45309; font-weight: bold; font-size: 1.4rem; }
    .score-low  { color: #b91c1c; font-weight: bold; font-size: 1.4rem; }
    .dim-label  { font-size: 0.85rem; color: #5a6478; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# ── Helper functions ──────────────────────────────────────────────────────────
def score_color(score):
    if score >= 70: return "score-high"
    if score >= 40: return "score-mid"
    return "score-low"

def score_emoji(score):
    if score >= 70: return "🟢"
    if score >= 40: return "🟡"
    return "🔴"

def score_label(score):
    if score >= 70: return "Copilot Ready"
    if score >= 40: return "Needs Work"
    return "Not Ready"

def format_dimension_name(name):
    return name.replace("_", " ").title()

# ── Load and score data ───────────────────────────────────────────────────────
@st.cache_data
def load_data():
    reports = get_sample_reports()
    return score_all_reports(reports)

results = load_data()

# ── Session state for navigation ─────────────────────────────────────────────
if "selected_report" not in st.session_state:
    st.session_state.selected_report = None

if "active_dimension" not in st.session_state:
    st.session_state.active_dimension = None

# ══════════════════════════════════════════════════════════════════════════════
# VIEW 1 — REPORT LIST
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.selected_report is None:

    # Header
    st.markdown("## ⚡ Copilot Readiness Analyzer")
    st.markdown("Power BI reports ranked by AI readiness — worst to best.")
    st.divider()

    # Summary stats
    avg_score = round(sum(r["final_score"] for r in results) / len(results))
    not_ready = sum(1 for r in results if r["final_score"] < 40)
    needs_work = sum(1 for r in results if 40 <= r["final_score"] < 70)
    ready = sum(1 for r in results if r["final_score"] >= 70)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Reports Scanned", len(results))
    col2.metric("🔴 Not Ready", not_ready)
    col3.metric("🟡 Needs Work", needs_work)
    col4.metric("🟢 Copilot Ready", ready)

    st.divider()

    # Report list
    st.markdown("### Reports — Ranked by Readiness")
    st.caption("Click any report to see its full audit and AI recommendations.")
    st.markdown(" ")

    for r in results:
        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])

        with col1:
            st.markdown(f"**{r['report_name']}**")
            st.caption(f"📁 {r['workspace']}")

        with col2:
            st.markdown(
                f"<span class='{score_color(r['final_score'])}'>"
                f"{score_emoji(r['final_score'])} {r['final_score']}/100</span>",
                unsafe_allow_html=True
            )

        with col3:
            st.caption(score_label(r['final_score']))

        with col4:
            total_issues = sum(
                len(d["issues"]) for d in r["dimensions"].values()
            )
            st.caption(f"⚠ {total_issues} issues")

        with col5:
            if st.button("Audit →", key=f"btn_{r['report_id']}"):
                st.session_state.selected_report = r
                st.rerun()

        st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# VIEW 2 — REPORT DRILL DOWN
# ══════════════════════════════════════════════════════════════════════════════
else:
    r = st.session_state.selected_report

    # Back button
    if st.button("← Back to all reports"):
        st.session_state.selected_report = None
        st.session_state.active_dimension = None
        st.rerun()

    st.markdown(f"## {r['report_name']}")
    st.caption(f"📁 {r['workspace']}")
    st.divider()

    # Score + summary side by side
    col1, col2 = st.columns([1, 3])

    with col1:
        st.markdown(
            f"<div style='text-align:center; padding: 20px; "
            f"background:#fff; border-radius:12px; border: 1px solid #e0e0e0;'>"
            f"<div style='font-size:0.85rem; color:#5a6478;'>AI READINESS SCORE</div>"
            f"<div class='{score_color(r['final_score'])}' style='font-size:2.5rem;'>"
            f"{r['final_score']}</div>"
            f"<div style='font-size:0.85rem; color:#5a6478;'>out of 100</div>"
            f"<div style='margin-top:8px;'>{score_emoji(r['final_score'])} "
            f"{score_label(r['final_score'])}</div>"
            f"</div>",
            unsafe_allow_html=True
        )

    with col2:
        with st.spinner("Generating executive summary..."):
            summary = get_report_summary(
                r['report_name'],
                r['final_score'],
                r['dimensions']
            )
        st.info(f"💡 {summary}")

    st.divider()

    # Dimension scores
    st.markdown("### Dimension Scores")
    cols = st.columns(4)
    for i, (dim, data) in enumerate(r['dimensions'].items()):
        with cols[i]:
            st.markdown(
                f"<div style='text-align:center; padding:16px; background:#fff; "
                f"border-radius:10px; border:1px solid #e0e0e0;'>"
                f"<div class='dim-label'>{format_dimension_name(dim)}</div>"
                f"<div class='{score_color(data['score'])}' style='font-size:1.8rem;'>"
                f"{data['score']}</div>"
                f"<div style='font-size:0.8rem; color:#5a6478;'>"
                f"{len(data['issues'])} issues</div>"
                f"</div>",
                unsafe_allow_html=True
            )

    st.divider()

    # Issues + AI recommendations per dimension
    st.markdown("### Issues &amp; AI Recommendations")

    for dim, data in r['dimensions'].items():
        dim_label = format_dimension_name(dim)
        issue_count = len(data['issues'])

        with st.expander(
            f"{score_emoji(data['score'])} {dim_label} — "
            f"{data['score']}/100 · {issue_count} issues"
        ):
            if not data['issues']:
                st.success("No issues found — this dimension is Copilot ready.")
            else:
                # Show raw issues
                st.markdown("**Issues detected:**")
                for issue in data['issues']:
                    st.markdown(f"- ⚠ {issue}")

                st.markdown(" ")

                # Get AI recommendations
                if st.button(
                    f"✨ Get AI Recommendations for {dim_label}",
                    key=f"ai_{r['report_id']}_{dim}"
                ):
                    with st.spinner("Asking Claude for recommendations..."):
                        recs = get_recommendations(
                            r['report_name'], dim, data['issues']
                        )
                    st.markdown("**Claude's Recommendations:**")
                    st.markdown(recs)