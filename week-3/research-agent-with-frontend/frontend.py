import streamlit as st
from agent import run_agent, agent

# ─────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Autonomous Research Agent",
    page_icon="[R]",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# Design tokens — light theme
# PRIMARY      #cc785c
# SUBTLE       #fdf1f1
# BG           #faf8f6
# SURFACE      #ffffff
# BORDER       #ddd6cf
# TEXT         #1a1410
# MUTED        #7a6a60
# DIM          #b5a89e
# ─────────────────────────────────────────────

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

  /* ── Global reset ── */
  *, *::before, *::after {
    border-radius: 0 !important;
    box-shadow: none !important;
  }

  /* ── Base typography & background ── */
  html, body, [class*="css"],
  .stApp, .main, .block-container {
    font-family: 'Space Grotesk', system-ui, sans-serif !important;
    color: #1a1410 !important;
    background-color: #faf8f6 !important;
  }

  .stApp {
    background: #faf8f6 !important;
  }

  /* ── Force ALL text in markdown/write elements to be dark ── */
  .stMarkdown, .stMarkdown p, .stMarkdown li,
  .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
  .stMarkdown h4, .stMarkdown h5, .stMarkdown h6,
  .stMarkdown strong, .stMarkdown em, .stMarkdown span,
  [data-testid="stMarkdownContainer"],
  [data-testid="stMarkdownContainer"] p,
  [data-testid="stMarkdownContainer"] li,
  [data-testid="stMarkdownContainer"] h1,
  [data-testid="stMarkdownContainer"] h2,
  [data-testid="stMarkdownContainer"] h3,
  [data-testid="stMarkdownContainer"] strong {
    color: #1a1410 !important;
    background: transparent !important;
  }

  /* ── Header ── */
  .site-header {
    border-bottom: 1px solid #ddd6cf;
    padding: 2rem 0 1.2rem;
    margin-bottom: 1.6rem;
  }
  .site-wordmark {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #cc785c;
    display: block;
    margin-bottom: 0.35rem;
  }
  .site-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #1a1410;
    line-height: 1.1;
    margin: 0 0 1.1rem;
  }

  /* ── Pipeline strip ── */
  .pipeline-strip {
    display: flex;
    align-items: center;
    gap: 0;
    margin: 0;
    border: 1px solid #ddd6cf;
    width: fit-content;
  }
  .pipe-step {
    padding: 5px 16px;
    font-size: 0.73rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #7a6a60;
    border-right: 1px solid #ddd6cf;
  }
  .pipe-step:last-child { border-right: none; }

  /* ── Section label ── */
  .section-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #cc785c;
    display: block;
    margin-bottom: 0.5rem;
  }

  /* ── Button column alignment ── */
  [data-testid="column"]:last-child .stButton {
    margin-top: 0 !important;
  }
  [data-testid="column"]:last-child .stButton > button {
    height: 42px !important;
    margin-top: 0 !important;
  }

  /* ── Text input ── */
  .stTextInput > div > div > input {
    background: #fdf1f1 !important;
    border: 1px solid #ddd6cf !important;
    border-radius: 0 !important;
    color: #1a1410 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.92rem !important;
    padding: 0.7rem 0.9rem !important;
  }
  .stTextInput > div > div > input:focus {
    border-color: #cc785c !important;
    box-shadow: none !important;
    outline: none !important;
  }
  .stTextInput > div > div > input::placeholder {
    color: #b5a89e !important;
  }
  .stTextInput > label {
    color: #7a6a60 !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
  }
  .stTextInput > div { border-radius: 0 !important; }

  /* ── Button ── */
  .stButton > button {
    background: #cc785c !important;
    color: #ffffff !important;
    border: 1px solid #cc785c !important;
    border-radius: 0 !important;
    padding: 0.65rem 1.6rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    width: 100% !important;
    transition: background 0.15s !important;
    cursor: pointer !important;
  }
  .stButton > button:hover {
    background: #b8674d !important;
    border-color: #b8674d !important;
  }
  .stButton > button:active {
    background: #a35840 !important;
  }

  /* ── Status panel ── */
  .status-panel {
    background: #ffffff;
    border: 1px solid #ddd6cf;
    border-left: 3px solid #cc785c;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1.6rem;
  }
  .status-title {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #7a6a60;
    margin-bottom: 1rem;
  }
  .step-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 5px 0;
    border-bottom: 1px solid #ede8e4;
    font-size: 0.85rem;
  }
  .step-row:last-child { border-bottom: none; }
  .step-row.done   { color: #cc785c !important; }
  .step-row.active { color: #1a1410 !important; }
  .step-row.idle   { color: #b5a89e !important; }
  .step-indicator {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    width: 20px;
    text-align: center;
    flex-shrink: 0;
  }

  /* ── Report header card ── */
  .report-wrap {
    border: 1px solid #ddd6cf;
    border-top: 3px solid #cc785c;
    margin-top: 1rem;
    background: #ffffff;
  }
  .report-header {
    padding: 0.8rem 1.4rem;
    border-bottom: 1px solid #ddd6cf;
    display: flex;
    align-items: center;
    gap: 1rem;
  }
  .report-badge {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #cc785c;
  }
  .report-topic {
    font-size: 0.82rem;
    color: #7a6a60;
    font-family: 'JetBrains Mono', monospace;
  }

  /* ── Report body — Streamlit renders markdown into its own divs ── */
  /* Target the container that sits directly after the report-wrap header */
  .report-body-container {
    border: 1px solid #ddd6cf;
    border-top: none;
    background: #ffffff;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
  }
  .report-body-container p,
  .report-body-container li {
    color: #2e2520 !important;
    font-size: 0.94rem !important;
    line-height: 1.65 !important;
    margin-bottom: 0.25rem !important;
  }
  .report-body-container h1,
  .report-body-container h2,
  .report-body-container h3 {
    color: #1a1410 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    margin-top: 1rem !important;
    margin-bottom: 0.3rem !important;
    line-height: 1.2 !important;
    border: none !important;
    background: transparent !important;
  }
  .report-body-container h1 { font-size: 1.2rem !important; }
  .report-body-container h2 { font-size: 1.05rem !important; }
  .report-body-container h3 { font-size: 0.96rem !important; }
  .report-body-container strong { color: #1a1410 !important; font-weight: 700 !important; }
  .report-body-container ul,
  .report-body-container ol {
    padding-left: 1.4rem !important;
    margin: 0.2rem 0 0.5rem !important;
  }
  .report-body-container a { color: #cc785c !important; text-decoration: underline !important; }
  .report-body-container hr {
    border: none !important;
    border-top: 1px solid #ddd6cf !important;
    margin: 0.8rem 0 !important;
  }
  /* Ensure no dark background bleeds in */
  .report-body-container,
  .report-body-container * {
    background-color: transparent !important;
  }
  .report-body-container .stMarkdown,
  .report-body-container [data-testid="stMarkdownContainer"] {
    color: #2e2520 !important;
  }

  /* ── Error block ── */
  .error-block {
    background: #fff5f5;
    border: 1px solid #e8c0c0;
    border-left: 3px solid #cc4444;
    padding: 0.9rem 1.2rem;
    color: #8b2020 !important;
    font-size: 0.88rem;
    font-family: 'JetBrains Mono', monospace;
    margin-top: 1rem;
  }

  /* ── Expanders ── */
  [data-testid="stExpander"] {
    border: 1px solid #ddd6cf !important;
    border-radius: 0 !important;
    background: #fdf1f1 !important;
    margin-top: 0.6rem !important;
  }
  [data-testid="stExpander"] summary {
    background: #fdf1f1 !important;
    color: #1a1410 !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    padding: 0.65rem 1rem !important;
  }
  [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    background: #ffffff !important;
    border-top: 1px solid #ddd6cf !important;
    padding: 0.8rem 1rem !important;
    color: #1a1410 !important;
  }
  [data-testid="stExpander"] [data-testid="stExpanderDetails"] p,
  [data-testid="stExpander"] [data-testid="stExpanderDetails"] li,
  [data-testid="stExpander"] [data-testid="stExpanderDetails"] a,
  [data-testid="stExpander"] [data-testid="stExpanderDetails"] code {
    color: #1a1410 !important;
    background: transparent !important;
  }
  /* st.code inside expanders */
  [data-testid="stExpander"] pre,
  [data-testid="stExpander"] code {
    background: #f4ede8 !important;
    color: #2e2520 !important;
    border: 1px solid #ddd6cf !important;
    padding: 0.4rem 0.7rem !important;
  }

  /* ── Divider ── */
  hr {
    border: none !important;
    border-top: 1px solid #ddd6cf !important;
    margin: 2rem 0 1rem !important;
  }

  /* ── Hide Streamlit chrome ── */
  #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────

st.markdown("""
<div class="site-header">
  <span class="site-wordmark">Autonomous Research Agent</span>
  <div class="site-title">Research. Verified.</div>
  <div class="pipeline-strip">
    <div class="pipe-step">01 &colon; Plan</div>
    <div class="pipe-step">02 &colon; Search</div>
    <div class="pipe-step">03 &colon; Read</div>
    <div class="pipe-step">04 &colon; Synthesise</div>
    <div class="pipe-step">05 &colon; Review</div>
  </div>
</div>
<div class="section-label">Research Query</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Input row
# ─────────────────────────────────────────────

col_input, col_btn = st.columns([5, 1])

with col_input:
    topic = st.text_input(
        "Topic",
        placeholder="e.g. How is AI being used in Pakistani universities?",
        label_visibility="collapsed",
        key="topic_input",
    )

with col_btn:
    run = st.button("Run Agent", key="run_btn")

# ─────────────────────────────────────────────
# Pipeline step definitions
# ─────────────────────────────────────────────

STEPS = [
    ("plan",       "Plan",       "Generating search queries"),
    ("search",     "Search",     "Querying Tavily"),
    ("read",       "Read",       "Extracting article text"),
    ("synthesise", "Synthesise", "Drafting report"),
    ("review",     "Review",     "Fact-checking and finalizing"),
]

# ─────────────────────────────────────────────
# Execution
# ─────────────────────────────────────────────

if run:
    if not topic.strip():
        st.markdown(
            '<div class="error-block">ERROR — No query provided. Enter a research topic above.</div>',
            unsafe_allow_html=True,
        )
    else:
        status_placeholder = st.empty()

        def render_status(current_idx: int, done: bool = False):
            rows_html = ""
            for i, (_, short, desc) in enumerate(STEPS):
                if done or i < current_idx:
                    cls = "done";   ind = "+"
                elif i == current_idx:
                    cls = "active"; ind = ">"
                else:
                    cls = "idle";   ind = "-"
                rows_html += (
                    f'<div class="step-row {cls}">'
                    f'<span class="step-indicator">{ind}</span>'
                    f'<span><strong>{short}</strong> &colon; {desc}</span>'
                    f'</div>'
                )
            status_placeholder.markdown(f"""
<div class="status-panel">
  <div class="status-title">Pipeline Progress</div>
  {rows_html}
</div>
""", unsafe_allow_html=True)

        render_status(0)
        result_placeholder = st.empty()

        try:
            step_map = {name: i for i, (name, _, _) in enumerate(STEPS)}

            for chunk in agent.stream({"topic": topic.strip()}):
                node_name = list(chunk.keys())[0]
                if node_name in step_map:
                    finished_idx = step_map[node_name]
                    next_idx = finished_idx + 1
                    render_status(
                        next_idx if next_idx < len(STEPS) else len(STEPS),
                        done=(next_idx >= len(STEPS)),
                    )

            render_status(0, done=True)

            final_result = run_agent(topic.strip())

            # Report header (HTML card top bar)
            result_placeholder.markdown(f"""
<div class="report-wrap">
  <div class="report-header">
    <span class="report-badge">Final Report</span>
    <span class="report-topic">{topic.strip()}</span>
  </div>
</div>
""", unsafe_allow_html=True)

            # Report body — rendered via st.markdown inside a styled container div
            # The container div is opened as HTML, content goes through Streamlit's
            # markdown renderer (handles **bold**, ## headings, - lists), then closed.
            st.markdown('<div class="report-body-container">', unsafe_allow_html=True)
            st.markdown(final_result["final_report"])
            st.markdown('</div>', unsafe_allow_html=True)

            # Expandable extras
            with st.expander("Sources and URLs", expanded=False):
                for item in final_result.get("search_results", []):
                    st.markdown(f"- [{item['title']}]({item['url']})")

            with st.expander("Search Queries Generated", expanded=False):
                for q in final_result.get("search_queries", []):
                    st.code(q, language=None)

        except Exception as e:
            render_status(0, done=False)
            st.markdown(
                f'<div class="error-block">ERROR — {str(e)}</div>',
                unsafe_allow_html=True,
            )
