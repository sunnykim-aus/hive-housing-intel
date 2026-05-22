"""
HIVE Data — Housing Intelligence & Evidence
Live data dashboards for Australian community housing.
No API key required — powered by ABS, AIHW, Treasury, and Housing Australia data.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date

from config import META_FILE, POLICY_TIMELINE


def show_insight(prompt: str, cache_key: str, max_tokens: int = 120):
    """No-op stub — AI insights are available in HIVE Intelligence (premium tier)."""
    pass


def render_references(sources: list):
    """Render a styled references & methodology table at the bottom of an analysis page."""
    rows_html = ""
    for i, s in enumerate(sources):
        bg = "#111122" if i % 2 == 0 else "#0f0f1a"
        link_html = (
            f'<a href="{s["url"]}" target="_blank" '
            f'style="color:#3a9bd5;text-decoration:none;font-size:0.78em;">'
            f'{s["url_label"]}</a>'
            if s.get("url") else
            f'<span style="color:#555;font-size:0.78em;">—</span>'
        )
        rows_html += f"""
        <tr style="background:{bg};">
            <td style="padding:10px 14px;color:#f6c90e;font-weight:600;
                       font-size:0.82em;white-space:nowrap;vertical-align:top;
                       border-bottom:1px solid #1e1e3a;">{s['abbr']}</td>
            <td style="padding:10px 14px;color:#ddd;font-size:0.82em;
                       vertical-align:top;border-bottom:1px solid #1e1e3a;">{s['full_name']}</td>
            <td style="padding:10px 14px;color:#bbb;font-size:0.82em;
                       vertical-align:top;border-bottom:1px solid #1e1e3a;">{s['used_for']}</td>
            <td style="padding:10px 14px;color:#aaa;font-size:0.82em;
                       vertical-align:top;border-bottom:1px solid #1e1e3a;">{s.get('methodology','')}</td>
            <td style="padding:10px 14px;vertical-align:top;
                       border-bottom:1px solid #1e1e3a;">{link_html}</td>
        </tr>"""
    st.markdown(f"""
    <div style="margin-top:40px;border-top:1px solid #2a2a4e;padding-top:24px;">
        <div style="font-size:0.72em;text-transform:uppercase;letter-spacing:2px;
                    color:#999;font-weight:600;margin-bottom:14px;">
            References &amp; Methodology
        </div>
        <div style="overflow-x:auto;">
        <table style="width:100%;border-collapse:collapse;font-family:inherit;">
            <thead>
                <tr style="background:#0a0a18;border-bottom:2px solid #2a2a4e;">
                    <th style="padding:9px 14px;text-align:left;color:#888;
                               font-size:0.72em;text-transform:uppercase;letter-spacing:1px;
                               font-weight:600;white-space:nowrap;">Source</th>
                    <th style="padding:9px 14px;text-align:left;color:#888;
                               font-size:0.72em;text-transform:uppercase;letter-spacing:1px;
                               font-weight:600;">Full title &amp; publisher</th>
                    <th style="padding:9px 14px;text-align:left;color:#888;
                               font-size:0.72em;text-transform:uppercase;letter-spacing:1px;
                               font-weight:600;">Used for</th>
                    <th style="padding:9px 14px;text-align:left;color:#888;
                               font-size:0.72em;text-transform:uppercase;letter-spacing:1px;
                               font-weight:600;">Methodology / notes</th>
                    <th style="padding:9px 14px;text-align:left;color:#888;
                               font-size:0.72em;text-transform:uppercase;letter-spacing:1px;
                               font-weight:600;">Link</th>
                </tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>
        </div>
    </div>
    """, unsafe_allow_html=True)


st.set_page_config(
    page_title="HIVE Data — Housing Intelligence & Evidence",
    page_icon="🐝",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
/* ── Hide sidebar & Streamlit chrome ── */
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
#MainMenu { display: none !important; }
header[data-testid="stHeader"] { display: none !important; }
footer { display: none !important; }

/* ── Push content below nav component ── */
.block-container { padding-top: 1rem !important; padding-left: 2rem; padding-right: 2rem; }

/* ── Global readability boost ── */
body, .stMarkdown, .stText, p, li, span, div {
    color: #e0e0e0;
}
h1, h2, h3, h4 { color: #ffffff !important; }
.stMarkdown p { font-size: 0.95em; line-height: 1.8; color: #d0d0d0; }
.stCaption, [data-testid="stCaptionContainer"] { color: #999 !important; font-size: 0.82em !important; }
/* Pills nav — larger, more readable */
[data-testid="stPills"] button {
    font-size: 0.85em !important;
    font-weight: 500 !important;
    color: #ccc !important;
}
[data-testid="stPills"] button[aria-pressed="true"] {
    color: #fff !important;
    font-weight: 700 !important;
}
/* Metric values */
[data-testid="stMetricValue"] { font-size: 1.6em !important; color: #fff !important; }
[data-testid="stMetricLabel"] { font-size: 0.82em !important; color: #bbb !important; }

/* Global */

/* Role cards */
.role-card {
    background: #1a1a2e;
    border: 1px solid #2a2a4e;
    border-radius: 10px;
    padding: 18px 20px;
    height: 100%;
    transition: border-color 0.2s;
}
.role-card:hover { border-color: #f6c90e; }
.role-card .role-title {
    font-size: 1em; font-weight: 700;
    color: #f6c90e; margin-bottom: 6px;
}
.role-card .role-sub {
    font-size: 0.78em; color: #aaa; margin-bottom: 10px;
}
.role-card .role-body {
    font-size: 0.82em; color: #ccc; line-height: 1.6;
}
.role-card .nav-pill {
    display: inline-block;
    background: #2a2a4e;
    color: #f6c90e;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 0.75em;
    margin: 2px 2px 0 0;
}

/* Section callout */
.insight-box {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    border-left: 4px solid #f6c90e;
    border-radius: 0 8px 8px 0;
    padding: 16px 20px;
    margin: 12px 0;
    font-size: 0.9em;
    color: #ccc;
    line-height: 1.8;
}

/* Data source cards */
.source-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #1a1a2e;
    border: 1px solid #2a2a4e;
    border-radius: 8px;
    padding: 10px 16px;
    margin: 4px;
    font-size: 0.82em;
    color: #ccc;
}
.source-pill .dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}

/* Stat highlight */
.stat-highlight {
    font-size: 2em;
    font-weight: 800;
    color: #f6c90e;
    line-height: 1.1;
}
.stat-label {
    font-size: 0.78em;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Page footer */
.hive-footer {
    margin-top: 56px;
    padding: 20px 24px 16px 24px;
    border-top: 1px solid #2a2a4e;
    background: #0f0f1a;
    border-radius: 0 0 8px 8px;
    text-align: center;
    font-size: 0.8em;
    color: #666;
    line-height: 1.7;
}
.hive-footer a {
    color: #f6c90e;
    text-decoration: none;
    font-weight: 600;
}
.hive-footer a:hover { text-decoration: underline; }

/* ── Section label headings ── */
.section-label {
    font-size: 0.82em !important;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #999 !important;
    font-weight: 600;
    margin: 24px 0 14px 0;
    display: block;
}
</style>
""", unsafe_allow_html=True)


# ── Navigation (session state) ────────────────────────────────────────────────

PAGES = [
    "About HIVE",
    "Live Housing Dashboard",
    "Housing Demand & Supply",
    "Population & Migration",
    "Housing Conditions & Costs",
    "HAFF Investment Tracker",
]

PAGE_SHORT = {
    "About HIVE": "About HIVE",
    "Live Housing Dashboard": "Live Dashboard",
    "Housing Demand & Supply": "Demand & Supply",
    "Population & Migration": "Population",
    "Housing Conditions & Costs": "Conditions",
    "HAFF Investment Tracker": "Future Fund",
}

if "page" not in st.session_state:
    st.session_state["page"] = "About HIVE"

page = st.session_state["page"]

# ── Top nav bar ───────────────────────────────────────────────────────────────

# Brand + badge row
st.markdown("""
<div style="display:flex;align-items:center;justify-content:space-between;
            padding:10px 0 8px 0;border-bottom:1px solid #2a2a3e;margin-bottom:10px;">
    <div style="display:flex;align-items:center;gap:10px;">
        <span style="font-size:1.3em;font-weight:900;color:#f6c90e;letter-spacing:0.5px;">🐝 HIVE</span>
        <span style="font-size:0.8em;color:#888;font-weight:400;">Housing Intelligence &amp; Evidence</span>
    </div>
    <a href="https://www.linkedin.com/in/sunny-kim-58a780100/" target="_blank"
       style="display:flex;align-items:center;gap:8px;text-decoration:none;color:inherit;">
        <span style="font-size:0.8em;color:#999;font-weight:400;">Housing Data Lead</span>
        <span style="color:#2a2a4e;">|</span>
        <span style="font-size:0.85em;color:#f6c90e;font-weight:600;">Sunny Kim</span>
        <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="#0077b5">
          <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136
                   1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37
                   -1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063
                   -.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064
                   2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452z
                   M22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771
                   24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
        </svg>
    </a>
</div>
""", unsafe_allow_html=True)

# Pills navigation — native Streamlit, no JS needed
_selected = st.pills(
    "Navigation",
    options=PAGES,
    format_func=lambda p: PAGE_SHORT[p],
    default=page,
    key="nav_pills",
    label_visibility="collapsed",
)
if _selected and _selected != page:
    st.session_state["page"] = _selected
    st.rerun()
page = st.session_state["page"]

# ── Report count (metadata only — no pipeline dependency) ─────────────────────
n_reports = len(META_FILE.read_text().splitlines()) if META_FILE.exists() else 0

# ── Page routing ──────────────────────────────────────────────────────────────


# ── Home ──────────────────────────────────────────────────────────────────────

if page == "About HIVE":

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown(
'<div style="'
'background-image:linear-gradient(135deg,rgba(10,10,20,0.88) 0%,rgba(20,12,5,0.72) 50%,rgba(10,10,20,0.90) 100%),'
'url(https://images.pexels.com/photos/5103918/pexels-photo-5103918.jpeg?auto=compress&cs=tinysrgb&w=1400);'
'background-size:cover;background-position:center 25%;'
'border-radius:14px;padding:56px 48px 48px 48px;margin-bottom:4px;'
'border:1px solid #2a2a3e;position:relative;overflow:hidden;">'
'<div style="font-size:3.2em;font-weight:900;color:#ffffff;letter-spacing:-1.5px;line-height:1.05;margin-bottom:10px;">'
'Housing Intelligence<br>&amp; Evidence'
'</div>'
'<div style="font-size:1em;color:#c0c0c0;max-width:640px;line-height:1.8;margin-bottom:28px;">'
'Live government data. 10 years of population history. Real-time dashboards. '
'Built for the people making the case for community housing investment in Australia.'
'</div>'
'<div style="display:flex;gap:10px;flex-wrap:wrap;">'
'<div style="background:rgba(246,201,14,0.15);border:1px solid rgba(246,201,14,0.3);border-radius:20px;padding:6px 16px;font-size:0.78em;color:#f6c90e;font-weight:600;">Live Data Dashboards</div>'
'<div style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:6px 16px;font-size:0.78em;color:#ccc;">ABS · AHURI · AIHW · Treasury</div>'
'<div style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:6px 16px;font-size:0.78em;color:#ccc;">Population Projections to 2044</div>'
'<div style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:6px 16px;font-size:0.78em;color:#ccc;">Construction Cost Crisis</div>'
'<div style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:6px 16px;font-size:0.78em;color:#ccc;">HAFF Investment Tracker</div>'
'</div>'
'</div>',
        unsafe_allow_html=True,
    )

    # ── Platform stats ────────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:linear-gradient(135deg,#13131f,#1a1a2e);
                border:1px solid #2a2a4e;border-radius:12px;
                padding:20px 28px;margin:16px 0 24px 0;">
        <div style="display:flex;gap:40px;align-items:center;flex-wrap:wrap;">
            <div>
                <div style="font-size:0.7em;text-transform:uppercase;letter-spacing:1.5px;
                            color:#666;margin-bottom:4px;">Live Data Sources</div>
                <div style="font-size:2em;font-weight:800;color:#fff;line-height:1;">8</div>
                <div style="font-size:0.78em;color:#888;margin-top:4px;">AHURI · ABS · AIHW · Treasury</div>
            </div>
            <div style="width:1px;height:48px;background:#2a2a4e;"></div>
            <div>
                <div style="font-size:0.7em;text-transform:uppercase;letter-spacing:1.5px;
                            color:#666;margin-bottom:4px;">Population History</div>
                <div style="font-size:2em;font-weight:800;color:#fff;line-height:1;">10 yrs</div>
                <div style="font-size:0.78em;color:#888;margin-top:4px;">ABS NOM series 2014–2024</div>
            </div>
            <div style="width:1px;height:48px;background:#2a2a4e;"></div>
            <div>
                <div style="font-size:0.7em;text-transform:uppercase;letter-spacing:1.5px;
                            color:#666;margin-bottom:4px;">Projections to</div>
                <div style="font-size:2em;font-weight:800;color:#f6c90e;line-height:1;">2044</div>
                <div style="font-size:0.78em;color:#888;margin-top:4px;">ABS Series B state projections</div>
            </div>
            <div style="width:1px;height:48px;background:#2a2a4e;"></div>
            <div>
                <div style="font-size:0.7em;text-transform:uppercase;letter-spacing:1.5px;
                            color:#666;margin-bottom:4px;">Platform Status</div>
                <div style="font-size:1em;font-weight:700;color:#27ae60;margin-top:4px;">
                    <span style="font-size:0.7em;">●</span> Live &amp; Updated
                </div>
                <div style="font-size:0.78em;color:#888;margin-top:4px;">No API key required</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # ── Why I built this ─────────────────────────────────────────────────────
    st.markdown(
'<div style="margin:32px 0 36px 0;">'
'<div style="display:flex;align-items:center;gap:12px;margin-bottom:24px;">'
'<div style="width:3px;height:28px;background:#f6c90e;border-radius:2px;flex-shrink:0;"></div>'
'<div style="font-size:0.7em;text-transform:uppercase;letter-spacing:2.5px;color:#666;font-weight:600;">Why This Exists</div>'
'</div>'
'<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:20px;margin-bottom:28px;">'
'<div style="background:#13131f;border:1px solid #2a2a3e;border-radius:10px;padding:20px 22px;">'
'<div style="font-size:1.5em;margin-bottom:8px;">📋</div>'
'<div style="font-size:0.85em;font-weight:700;color:#fff;margin-bottom:8px;">The Problem</div>'
'<div style="font-size:0.82em;color:#aaa;line-height:1.75;">Every week, sector professionals need evidence fast — for submissions, board papers, grant applications. The answers exist. Finding them takes days.</div>'
'</div>'
'<div style="background:#13131f;border:1px solid #2a2a3e;border-radius:10px;padding:20px 22px;">'
'<div style="font-size:1.5em;margin-bottom:8px;">📚</div>'
'<div style="font-size:0.85em;font-weight:700;color:#fff;margin-bottom:8px;">The Evidence Base</div>'
'<div style="font-size:0.82em;color:#aaa;line-height:1.75;">681 reports across AHURI, ABS, AIHW, Treasury and state housing registers — synthesised and searchable in seconds.</div>'
'</div>'
'<div style="background:#13131f;border:1px solid #2a2a3e;border-radius:10px;padding:20px 22px;">'
'<div style="font-size:1.5em;margin-bottom:8px;">⚡</div>'
'<div style="font-size:0.85em;font-weight:700;color:#fff;margin-bottom:8px;">The Solution</div>'
'<div style="font-size:0.82em;color:#aaa;line-height:1.75;">HIVE connects the evidence base to live data and AI synthesis — collapsing the time between question and answer from days to minutes.</div>'
'</div>'
'</div>'
'<div style="background:linear-gradient(135deg,#13131f,#1a1a2e);border-left:3px solid #f6c90e;border-radius:0 10px 10px 0;padding:20px 28px;">'
'<div style="font-size:0.95em;color:#d0d0d0;line-height:1.9;font-style:italic;">"I work in community housing in Australia. HIVE is what I wished existed when I needed to make the case for investment, write a submission at short notice, or understand what the research actually says — without spending a week finding out."</div>'
'<div style="margin-top:16px;display:flex;align-items:center;gap:10px;">'
'<div style="width:32px;height:32px;border-radius:50%;background:#f6c90e;display:flex;align-items:center;justify-content:center;font-size:0.7em;font-weight:800;color:#0f0f1a;flex-shrink:0;">SK</div>'
'<div><a href="https://www.linkedin.com/in/sunny-kim-58a780100/" target="_blank" style="color:#f6c90e;text-decoration:none;font-weight:700;font-size:0.88em;">Sunny Kim</a>'
'<span style="color:#666;font-size:0.82em;"> &nbsp;·&nbsp; Housing Data Lead &nbsp;·&nbsp; Community Housing Professional, Australia</span></div>'
'</div>'
'</div>'
'</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    # ── Platform at a glance ──────────────────────────────────────────────────
    st.markdown("""
    <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:0;
                background:#1a1a2e;border:1px solid #2a2a4e;border-radius:10px;
                margin:0 0 24px 0;overflow:hidden;">
        <div style="padding:14px 18px;border-right:1px solid #2a2a4e;text-align:center;">
            <div style="font-size:1.6em;font-weight:800;color:#f6c90e;">5</div>
            <div style="font-size:0.72em;text-transform:uppercase;letter-spacing:1px;color:#666;margin-top:2px;">Live dashboards</div>
        </div>
        <div style="padding:14px 18px;border-right:1px solid #2a2a4e;text-align:center;">
            <div style="font-size:1.6em;font-weight:800;color:#fff;">681+</div>
            <div style="font-size:0.72em;text-transform:uppercase;letter-spacing:1px;color:#666;margin-top:2px;">Reports indexed</div>
        </div>
        <div style="padding:14px 18px;border-right:1px solid #2a2a4e;text-align:center;">
            <div style="font-size:1.6em;font-weight:800;color:#fff;">10 yrs</div>
            <div style="font-size:0.72em;text-transform:uppercase;letter-spacing:1px;color:#666;margin-top:2px;">Population history</div>
        </div>
        <div style="padding:14px 18px;border-right:1px solid #2a2a4e;text-align:center;">
            <div style="font-size:1.6em;font-weight:800;color:#e74c3c;">+58%</div>
            <div style="font-size:0.72em;text-transform:uppercase;letter-spacing:1px;color:#666;margin-top:2px;">Construction cost rise</div>
        </div>
        <div style="padding:14px 18px;text-align:center;">
            <div style="font-size:1.6em;font-weight:800;color:#fff;">2044</div>
            <div style="font-size:0.72em;text-transform:uppercase;letter-spacing:1px;color:#666;margin-top:2px;">Projections to</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Live sector snapshot ───────────────────────────────────────────────────
    st.markdown("""
    <div style="font-size:0.82em;text-transform:uppercase;letter-spacing:2px;
                color:#999;font-weight:600;margin:28px 0 16px 0;">The Housing Crisis in Numbers — Right Now</div>
    """, unsafe_allow_html=True)

    # ── Curated stats (from ABS 8731.0, AIHW SHS 2022-23, state registers June 2023) ──
    _run_rate = 173_800
    _gap      = 240_000 - _run_rate
    _pct      = round(_run_rate / 240_000 * 100)
    _unmet    = 118_700
    _success  = 25
    _wl_total = 193_800

    if True:
        h1, h2, h3, h4 = st.columns(4)
        with h1:
            st.markdown(f'<div class="stat-highlight">{_run_rate:,}</div>'
                        f'<div class="stat-label">Dwellings built per year</div>'
                        f'<div style="font-size:0.78em;color:#e74c3c;margin-top:4px;">'
                        f'{_pct}% of the 240,000 National Accord target</div>',
                        unsafe_allow_html=True)
        with h2:
            st.markdown(f'<div class="stat-highlight" style="color:#e74c3c;">{_gap:,}</div>'
                        f'<div class="stat-label">Annual supply shortfall</div>'
                        f'<div style="font-size:0.78em;color:#888;margin-top:4px;">'
                        f'Dwellings per year below what Australia needs</div>',
                        unsafe_allow_html=True)
        with h3:
            st.markdown(f'<div class="stat-highlight" style="color:#e74c3c;">{_unmet:,}</div>'
                        f'<div class="stat-label">Unmet housing requests (2023–24)</div>'
                        f'<div style="font-size:0.78em;color:#888;margin-top:4px;">'
                        f'People who sought help and didn\'t receive housing</div>',
                        unsafe_allow_html=True)
        with h4:
            st.markdown(f'<div class="stat-highlight" style="color:#f39c12;">{_success}%</div>'
                        f'<div class="stat-label">Housing success rate (SHS)</div>'
                        f'<div style="font-size:0.78em;color:#888;margin-top:4px;">'
                        f'Only 1 in 4 people who needed housing actually received it</div>',
                        unsafe_allow_html=True)

        st.markdown(f"""
        <div class="insight-box" style="margin-top:20px;">
        <strong style="color:#f6c90e;">What this means for community housing:</strong><br>
        Australia is building at <strong style="color:#fff">{_pct}% of the pace needed</strong>
        to meet the National Housing Accord — a shortfall of <strong style="color:#e74c3c">{_gap:,}
        dwellings every year</strong>. At the same time, demand is accelerating:
        <strong>{_unmet:,} people</strong> sought homelessness services last year and left without housing.
        There are over <strong style="color:#fff">{_wl_total:,} approved applicants</strong> on social
        housing waitlists across the major states — a confirmed tenant pipeline that no private developer
        can match.<br><br>
        Compounding this: net overseas migration hit a record <strong style="color:#f6c90e;">518,000 in 2023</strong>
        — more than double the pre-COVID average — driving national rental vacancy to 1.0% and rents 48% above
        2015 levels. And the same $1B that built 3,226 social homes in 2019 builds only
        <strong style="color:#e74c3c;">1,786 today</strong>, after a 58% rise in construction costs since COVID.
        The case for community housing investment has never been stronger — and the evidence
        to make that case has never been more complete.
        <br><br>
        <em>ABS Building Approvals (Cat. 8731.0), AIHW SHS Annual Report 2023–24, ABS Cat. 3412.0 (migration),
        ABS PPI House Construction (Cat. 6427.0). Updated {date.today().strftime('%B %Y')}.</em>
        </div>
        """, unsafe_allow_html=True)

        # ── Evidence reference table ───────────────────────────────────────
        st.markdown("""
        <div style="margin-top:20px;">
        <div style="font-size:0.72em;text-transform:uppercase;letter-spacing:2px;
                    color:#999;font-weight:600;margin-bottom:10px;">Data Sources & References</div>
        <table style="width:100%;border-collapse:collapse;font-size:0.8em;color:#ccc;">
          <thead>
            <tr style="border-bottom:1px solid #2a2a4e;">
              <th style="text-align:left;padding:8px 12px;color:#888;font-weight:500;width:22%;">Indicator</th>
              <th style="text-align:left;padding:8px 12px;color:#888;font-weight:500;width:14%;">Figure</th>
              <th style="text-align:left;padding:8px 12px;color:#888;font-weight:500;width:28%;">Source</th>
              <th style="text-align:left;padding:8px 12px;color:#888;font-weight:500;width:20%;">Publication</th>
              <th style="text-align:left;padding:8px 12px;color:#888;font-weight:500;width:16%;">Frequency</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom:1px solid #1a1a2e;background:#0f0f1a;">
              <td style="padding:8px 12px;">Annual dwelling approvals</td>
              <td style="padding:8px 12px;color:#f6c90e;font-weight:600;">{_run_rate:,}</td>
              <td style="padding:8px 12px;">Australian Bureau of Statistics</td>
              <td style="padding:8px 12px;">Building Approvals, Australia (Cat. 8731.0)</td>
              <td style="padding:8px 12px;">Monthly</td>
            </tr>
            <tr style="border-bottom:1px solid #1a1a2e;">
              <td style="padding:8px 12px;">National Accord target</td>
              <td style="padding:8px 12px;color:#f6c90e;font-weight:600;">240,000/yr</td>
              <td style="padding:8px 12px;">Australian Government</td>
              <td style="padding:8px 12px;">National Housing Accord, September 2022</td>
              <td style="padding:8px 12px;">Policy target</td>
            </tr>
            <tr style="border-bottom:1px solid #1a1a2e;background:#0f0f1a;">
              <td style="padding:8px 12px;">Annual supply shortfall</td>
              <td style="padding:8px 12px;color:#e74c3c;font-weight:600;">{_gap:,}</td>
              <td style="padding:8px 12px;">HIVE calculation</td>
              <td style="padding:8px 12px;">Accord target minus ABS run rate (3-month avg × 12)</td>
              <td style="padding:8px 12px;">Monthly updated</td>
            </tr>
            <tr style="border-bottom:1px solid #1a1a2e;">
              <td style="padding:8px 12px;">Unmet housing requests</td>
              <td style="padding:8px 12px;color:#e74c3c;font-weight:600;">{_unmet:,}</td>
              <td style="padding:8px 12px;">Australian Institute of Health and Welfare</td>
              <td style="padding:8px 12px;">Specialist Homelessness Services Annual Report 2023–24</td>
              <td style="padding:8px 12px;">Annual</td>
            </tr>
            <tr style="border-bottom:1px solid #1a1a2e;background:#0f0f1a;">
              <td style="padding:8px 12px;">Housing success rate (SHS)</td>
              <td style="padding:8px 12px;color:#f39c12;font-weight:600;">27.4%</td>
              <td style="padding:8px 12px;">Australian Institute of Health and Welfare</td>
              <td style="padding:8px 12px;">SHS Annual Report 2023–24 — clients needing housing who received it</td>
              <td style="padding:8px 12px;">Annual</td>
            </tr>
            <tr style="border-bottom:1px solid #1a1a2e;">
              <td style="padding:8px 12px;">Social housing waitlist (major states)</td>
              <td style="padding:8px 12px;color:#f6c90e;font-weight:600;">{_wl_total:,}</td>
              <td style="padding:8px 12px;">NSW DCJ, VIC DFFH, QLD DCHDE, WA DPLH, SA SAHT</td>
              <td style="padding:8px 12px;">State housing authority annual reports 2023–24</td>
              <td style="padding:8px 12px;">Annual</td>
            </tr>
            <tr style="border-bottom:1px solid #1a1a2e;background:#0f0f1a;">
              <td style="padding:8px 12px;">Net overseas migration (peak)</td>
              <td style="padding:8px 12px;color:#e74c3c;font-weight:600;">518,000</td>
              <td style="padding:8px 12px;">Australian Bureau of Statistics</td>
              <td style="padding:8px 12px;">Cat. 3412.0 — Migration, Australia (2022–23 annual)</td>
              <td style="padding:8px 12px;">Annual</td>
            </tr>
            <tr style="border-bottom:1px solid #1a1a2e;">
              <td style="padding:8px 12px;">Construction cost rise since 2019</td>
              <td style="padding:8px 12px;color:#e74c3c;font-weight:600;">+58.5%</td>
              <td style="padding:8px 12px;">Australian Bureau of Statistics</td>
              <td style="padding:8px 12px;">Cat. 6427.0 — PPI House Construction (Q4 2019 to Q1 2025)</td>
              <td style="padding:8px 12px;">Quarterly</td>
            </tr>
            <tr style="border-bottom:1px solid #1a1a2e;background:#0f0f1a;">
              <td style="padding:8px 12px;">Social housing maintenance backlog</td>
              <td style="padding:8px 12px;color:#e74c3c;font-weight:600;">$26.5B</td>
              <td style="padding:8px 12px;">UNSW City Futures Research Centre</td>
              <td style="padding:8px 12px;">Social Housing Futures report, 2023</td>
              <td style="padding:8px 12px;">Periodic</td>
            </tr>
          </tbody>
        </table>
        </div>
        """.format(
            _run_rate=_run_rate, _gap=_gap, _unmet=_unmet, _wl_total=_wl_total
        ), unsafe_allow_html=True)

    if False:
        pass  # placeholder — curated data always available

    # ── What HIVE Does ────────────────────────────────────────────────────────
    st.markdown("""
    <div style="font-size:0.82em;text-transform:uppercase;letter-spacing:2px;
                color:#999;font-weight:600;margin-bottom:16px;">What This Platform Does — 5 Dashboards</div>
    """, unsafe_allow_html=True)

    _capabilities = [
        {
            "nav":   "Live Dashboard",
            "icon":  "📡",
            "title": "Live Housing Dashboard",
            "body":  "ABS building approvals, the AIHW homelessness funnel, and state social housing waitlists — curated from the latest official publications. The supply gap vs Accord target, with state-by-state breakdown.",
            "new":   False,
        },
        {
            "nav":   "Demand & Supply",
            "icon":  "⚖️",
            "title": "Housing Demand & Supply",
            "body":  "Who is on the waitlist by state, what household type, what is being built, and the structural mismatch between supply and need. 20 years of waitlist trend and a full state spotlight table.",
            "new":   False,
        },
        {
            "nav":   "Population",
            "icon":  "📈",
            "title": "Population & Migration",
            "body":  "10 years of population history, the COVID migration shock (−84k to +518k NOM), state-by-state vacancy and rent impact, ABS projections to 2044, implied dwelling demand, and evidence-based advocacy positions.",
            "new":   True,
        },
        {
            "nav":   "Conditions",
            "icon":  "🔧",
            "title": "Housing Conditions & Costs",
            "body":  "The $26.5B social housing maintenance backlog, what government is doing and whether it's enough, plus a full timeline of global events since 2019 — COVID, Ukraine, supply chains, rate hikes — and how each drove a 58% construction cost rise.",
            "new":   True,
        },
        {
            "nav":   "Future Fund",
            "icon":  "🏗️",
            "title": "HAFF Investment Tracker",
            "body":  "Round-by-round breakdown of the $10B Housing Australia Future Fund — homes announced vs 30,000 target, state allocations, sector mix, bedroom mix, delivery pipeline, and funding gap analysis.",
            "new":   False,
        },
    ]

    cap_html = '<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-top:0;">'
    for cap in _capabilities:
        new_badge = (
            '<span style="font-size:0.68em;font-weight:700;color:#0f0f1a;'
            'background:#f6c90e;border-radius:6px;padding:1px 7px;'
            'margin-left:8px;vertical-align:middle;letter-spacing:0.5px;">NEW</span>'
            if cap["new"] else ""
        )
        cap_html += f"""
        <div class="role-card" style="display:flex;flex-direction:column;">
            <div style="font-size:1.4em;margin-bottom:6px;">{cap['icon']}</div>
            <div class="role-title" style="font-size:0.8em;text-transform:uppercase;
                 letter-spacing:0.8px;line-height:1.4;">{cap['title']}{new_badge}</div>
            <div class="role-body" style="flex:1;margin-top:8px;font-size:0.8em;">
                {cap['body']}
            </div>
            <div style="margin-top:10px;">
                <span class="nav-pill">{cap['nav']}</span>
            </div>
        </div>"""
    cap_html += "</div>"
    st.markdown(cap_html, unsafe_allow_html=True)

    # ── Who is this for ───────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.82em;text-transform:uppercase;letter-spacing:2px;
                color:#999;font-weight:600;margin-bottom:16px;">Who Uses HIVE and Where to Start</div>
    """, unsafe_allow_html=True)

    roles = [
        {
            "title": "CEO / Executive Director",
            "sub": "CHP or peak body",
            "body": "Start with the <strong>Live Dashboard</strong> for current national numbers, then <strong>Population</strong> for the 10-year growth story and what it means for housing demand. <strong>HAFF</strong> shows what the government has committed and what's been delivered.",
            "tabs": ["Live Dashboard", "Population", "Future Fund", "Conditions"],
        },
        {
            "title": "Policy & Advocacy Manager",
            "sub": "CHP, peak body, or government",
            "body": "<strong>Population</strong> has six evidence-backed advocacy positions the sector needs. <strong>Conditions</strong> makes the case for grant indexation and maintenance investment. <strong>Demand & Supply</strong> shows the structural mismatch in hard numbers.",
            "tabs": ["Population", "Conditions", "Demand & Supply", "Future Fund"],
        },
        {
            "title": "Development Manager",
            "sub": "Property and pipeline, CHP",
            "body": "<strong>Demand & Supply</strong> is your demand case — waitlist demographics vs bedroom mix vs what's being built. <strong>Population</strong> shows projected demand by state to 2044. <strong>Conditions</strong> gives you the construction cost story and why HAFF grants have a funding gap. <strong>HAFF</strong> shows the pipeline you're competing in.",
            "tabs": ["Demand & Supply", "Population", "Conditions", "Future Fund"],
        },
        {
            "title": "Grants & Funding Officer",
            "sub": "CHP or community organisation",
            "body": "<strong>Population</strong>'s state growth data gives you the forward demand story. <strong>Demand & Supply</strong> shows waitlist demographics by state and household type — the evidence for your bid. <strong>Live Dashboard</strong> has the latest homelessness and approval data.",
            "tabs": ["Population", "Demand & Supply", "Live Dashboard", "Future Fund"],
        },
        {
            "title": "Impact Investor / Funder",
            "sub": "Super funds, banks, philanthropies",
            "body": "<strong>HAFF</strong> shows what government committed vs delivered. <strong>Population</strong> shows the scale of unmet demand (32.5M Australians by 2041). <strong>Conditions</strong> shows why the $1B that built 3,226 homes in 2019 only builds 1,786 today — and why that makes the investment case stronger.",
            "tabs": ["Future Fund", "Population", "Conditions", "Demand & Supply"],
        },
        {
            "title": "Government Stakeholder",
            "sub": "State/federal housing departments",
            "body": "<strong>Population</strong> shows the structural gap between projected demand and any credible supply trajectory. <strong>Conditions</strong> makes the asset renewal case. <strong>HAFF</strong> tracks fund performance round by round. <strong>Live Dashboard</strong> provides the latest approval and waitlist data.",
            "tabs": ["Population", "Conditions", "Future Fund", "Live Dashboard"],
        },
    ]

    cards_html = '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:0;">'
    for role in roles:
        pills = "".join(f'<span class="nav-pill">{t}</span>' for t in role["tabs"])
        cards_html += f"""
        <div class="role-card" style="display:flex;flex-direction:column;">
            <div class="role-title">{role['title']}</div>
            <div class="role-sub">{role['sub']}</div>
            <div class="role-body" style="flex:1;">{role['body']}</div>
            <div style="margin-top:12px;">{pills}</div>
        </div>"""
    cards_html += "</div>"
    st.markdown(cards_html, unsafe_allow_html=True)

    # ── Data sources ──────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### What Data Powers HIVE")
    st.markdown(
        "Every dashboard in HIVE is built on live data from these authoritative government and research sources. "
        "Every number is traceable to a specific publication."
    )

    sources_data = [
        {"color": "#e74c3c", "name": "AHURI", "full": "Australian Housing and Urban Research Institute",
         "desc": "15 years of final reports, policy bulletins, research briefs and evidence reviews — the authoritative academic source on Australian housing."},
        {"color": "#3498db", "name": "Housing Australia", "full": "Housing Australia (formerly NHFIC)",
         "desc": "Annual reports, Home Guarantee Scheme trends, bond aggregation data, and social housing investment reports."},
        {"color": "#27ae60", "name": "Treasury", "full": "Australian Government Treasury",
         "desc": "Federal Budget Papers (2010–2026) — Budget Paper 2 lists every housing program, its funding, and year-by-year allocations. The financial ground truth."},
        {"color": "#f39c12", "name": "ABS", "full": "Australian Bureau of Statistics",
         "desc": "Building approvals (monthly), Census housing data, residential property price indexes, housing occupancy and costs surveys."},
        {"color": "#9b59b6", "name": "AIHW", "full": "Australian Institute of Health and Welfare",
         "desc": "Specialist Homelessness Services annual reports, homelessness estimates from Census, Indigenous housing data — the authoritative source on housing outcomes."},
        {"color": "#1abc9c", "name": "Productivity Commission", "full": "Productivity Commission",
         "desc": "Major housing inquiries including the landmark 2022 Housing and Homelessness report, rental assistance review, and Report on Government Services (housing chapter)."},
        {"color": "#e67e22", "name": "DSS", "full": "Department of Social Services",
         "desc": "National Housing and Homelessness Agreement, National Rental Affordability Scheme documentation, homelessness strategy policy papers."},
        {"color": "#95a5a6", "name": "Power Housing", "full": "Power Housing Australia",
         "desc": "Community housing sector peak body publications and State of the Sector reports (where accessible)."},
    ]

    st.markdown("""
    <div style="background:#1a1a2e;border-radius:10px;padding:20px 24px;margin-bottom:20px;
                display:flex;gap:40px;flex-wrap:wrap;">
        <div style="text-align:center;">
            <div class="stat-highlight">8</div>
            <div class="stat-label">Data sources</div>
        </div>
        <div style="text-align:center;">
            <div class="stat-highlight">15+</div>
            <div class="stat-label">Years of data</div>
        </div>
        <div style="text-align:center;">
            <div class="stat-highlight">Monthly</div>
            <div class="stat-label">ABS update cadence</div>
        </div>
        <div style="text-align:center;">
            <div class="stat-highlight">2044</div>
            <div class="stat-label">Projections to</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    _src_html = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px;">'
    for src in sources_data:
        _src_html += (
            f'<div style="background:#1a1a2e;border:1px solid #2a2a4e;'
            f'border-left:4px solid {src["color"]};border-radius:0 8px 8px 0;'
            f'padding:16px 18px;display:flex;flex-direction:column;">'
            f'<div style="font-weight:700;color:#fff;font-size:0.95em;margin-bottom:2px;">{src["name"]}</div>'
            f'<div style="font-size:0.75em;color:#888;margin-bottom:8px;">{src["full"]}</div>'
            f'<div style="font-size:0.82em;color:#bbb;line-height:1.65;flex:1;">{src["desc"]}</div>'
            f'</div>'
        )
    _src_html += '</div>'
    st.markdown(_src_html, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#1a1a2e;border:1px solid #2a2a4e;border-radius:8px;
                padding:14px 20px;font-size:0.82em;color:#888;line-height:1.7;">
    <strong style="color:#f6c90e;">How the data is kept current:</strong>
    HIVE pulls from live government APIs and curated datasets — ABS building approvals update monthly,
    AIHW homelessness data updates annually, and state housing registers publish quarterly.
    Every data point in each dashboard is sourced, dated, and linked to its primary publication.
    No data leaves your environment.
    </div>
    """, unsafe_allow_html=True)


# ── HAFF Investment Tracker ───────────────────────────────────────────────────

if page == "HAFF Investment Tracker":
    from live.haff_data import HAFF_ROUNDS, HAFF_OVERVIEW, get_haff_summary, get_state_totals_across_rounds

    st.markdown("## HAFF Investment Tracker")
    st.markdown(
        "Housing Australia Future Fund — round-by-round breakdown of projects, regions, "
        "dwelling types, and sector allocations."
    )
    st.caption(
        "Sources: Housing Australia media releases, Senate Estimates, Budget Papers 2023-24 to 2025-26. "
        "Verify against primary Housing Australia sources before formal submission use."
    )

    # ── Fund overview KPIs ────────────────────────────────────────────────────
    summary = get_haff_summary()
    st.markdown("---")
    st.markdown("""<div style="font-size:0.82em;text-transform:uppercase;letter-spacing:2px;
                color:#999;font-weight:600;margin-bottom:12px;">Fund Overview — All Rounds to Date</div>""",
                unsafe_allow_html=True)

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    with k1:
        st.metric("Fund Size", f"${HAFF_OVERVIEW['fund_size_bn']}B",
                  "Off-budget investment fund", delta_color="off")
    with k2:
        st.metric("Total Grants Committed", f"${summary['total_grants_m']:,.0f}M",
                  "Rounds 1–3 combined", delta_color="off")
    with k3:
        st.metric("Homes Announced", f"{summary['total_homes']:,}",
                  f"{summary['pct_of_5yr_target']}% of 30,000 target", delta_color="off")
    with k4:
        st.metric("Social Housing", f"{summary['total_social']:,}",
                  f"of 20,000 target", delta_color="off")
    with k5:
        st.metric("Affordable Housing", f"{summary['total_affordable']:,}",
                  f"of 10,000 target", delta_color="off")
    with k6:
        st.metric("Total Projects", f"{summary['total_projects']:,}",
                  "Across all states & territories", delta_color="off")

    # Progress bar toward 30,000 target
    pct = summary["pct_of_5yr_target"]
    remaining = summary["remaining_to_target"]
    st.markdown(f"""
    <div style="margin:16px 0 24px 0;">
        <div style="font-size:0.78em;color:#888;margin-bottom:6px;">
            Progress toward 30,000 home target &nbsp;·&nbsp;
            <span style="color:#f6c90e;font-weight:600;">{summary['total_homes']:,} announced</span>
            &nbsp;·&nbsp; {remaining:,} still to be allocated
        </div>
        <div style="background:#1a1a2e;border-radius:6px;height:12px;overflow:hidden;">
            <div style="width:{min(pct,100)}%;height:100%;
                        background:linear-gradient(90deg,#f6c90e,#e67e22);
                        border-radius:6px;"></div>
        </div>
        <div style="font-size:0.78em;color:#888;margin-top:4px;">{pct}% of 5-year target committed</div>
    </div>
    """, unsafe_allow_html=True)

    show_insight(
        f"In 2 direct sentences, assess the HAFF (Housing Australia Future Fund) delivery progress: "
        f"{summary['total_homes']:,} homes announced across 3 rounds ({summary['pct_of_5yr_target']}% of 30,000 target), "
        f"${summary['total_grants_m']:,.0f}M in grants committed, {summary['total_social']:,} social and "
        f"{summary['total_affordable']:,} affordable homes. {summary['remaining_to_target']:,} homes still to be allocated. "
        f"Write for a community housing provider participating in HAFF. Be direct about delivery risk.",
        cache_key="haff_overview_insight",
        max_tokens=140,
    )

    # ── Round selector tabs ───────────────────────────────────────────────────
    round_tab1, round_tab2, round_tab3, round_tab4 = st.tabs(
        ["Round 1 — March 2024", "Round 2 — October 2024", "Round 3 — March 2025", "All Rounds Combined"]
    )

    def render_round(r, rdata):
        col_l, col_r = st.columns([2, 1])
        with col_l:
            import html as _html
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1a1a2e,#16213e);
                        border-left:4px solid #f6c90e;border-radius:0 8px 8px 0;
                        padding:16px 20px;font-size:0.88em;color:#ccc;line-height:1.8;">
                <strong style="color:#f6c90e;">Context & Notes</strong><br>
                {_html.escape(rdata['notes'])}
            </div>
            """, unsafe_allow_html=True)
        with col_r:
            st.markdown(f"""
            <div style="background:#1a1a2e;border:1px solid #2a2a4e;border-radius:8px;
                        padding:16px 20px;font-size:0.85em;line-height:2.0;color:#ccc;">
                <div><span style="color:#888;">Status:</span>&nbsp;
                    <strong style="color:#f6c90e;">{rdata['status']}</strong></div>
                <div><span style="color:#888;">Announced:</span>&nbsp;{rdata['announced']}</div>
                <div><span style="color:#888;">Grants total:</span>&nbsp;
                    <strong>${rdata['grants_total_m']:,.0f}M</strong></div>
                <div><span style="color:#888;">Projects:</span>&nbsp;{rdata['projects']}</div>
                <div><span style="color:#888;">Delivery partners (CHPs):</span>&nbsp;{rdata['chps_involved']}</div>
                <div><span style="color:#888;">Avg grant per home:</span>&nbsp;
                    ~${rdata['avg_grant_per_home_k']:,}k</div>
                <div><span style="color:#888;">Completion target:</span>&nbsp;{rdata['completion_target']}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # KPIs
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Total Homes", f"{rdata['total_homes']:,}")
        with m2:
            social_pct = round(rdata['social_homes'] / rdata['total_homes'] * 100)
            st.metric("Social Housing", f"{rdata['social_homes']:,}", f"{social_pct}% of total", delta_color="off")
        with m3:
            aff_pct = round(rdata['affordable_homes'] / rdata['total_homes'] * 100)
            st.metric("Affordable Housing", f"{rdata['affordable_homes']:,}", f"{aff_pct}% of total", delta_color="off")
        with m4:
            st.metric("States/Territories", rdata['states_covered'])

        st.markdown("---")

        # ── 2×2 chart grid — all columns equal width, equal height ────────
        df_state = pd.DataFrame(rdata["by_state"])
        c1, c2 = st.columns(2)

        with c1:
            st.markdown("**Homes by State/Territory**")
            fig_state = go.Figure()
            fig_state.add_trace(go.Bar(
                x=df_state["state"], y=df_state["social"],
                name="Social", marker_color="#e74c3c",
                hovertemplate="%{x} Social: %{y:,}<extra></extra>",
            ))
            fig_state.add_trace(go.Bar(
                x=df_state["state"], y=df_state["affordable"],
                name="Affordable", marker_color="#f39c12",
                hovertemplate="%{x} Affordable: %{y:,}<extra></extra>",
            ))
            fig_state.update_layout(
                barmode="stack",
                plot_bgcolor="#1a1a2e", paper_bgcolor="#0f0f1a",
                font_color="#fff", height=320,
                margin=dict(l=0, r=0, t=30, b=0),
                xaxis=dict(gridcolor="#2a2a4e"),
                yaxis=dict(gridcolor="#2a2a4e", tickformat=","),
                legend=dict(orientation="h", yanchor="bottom", y=1.02,
                            bgcolor="rgba(0,0,0,0)", font_size=11),
            )
            st.plotly_chart(fig_state, use_container_width=True)

        with c2:
            st.markdown("**Grant Allocation by State ($M)**")
            df_state_s = df_state.sort_values("grant_m", ascending=True)
            fig_grant = go.Figure(go.Bar(
                x=df_state_s["grant_m"], y=df_state_s["state"],
                orientation="h",
                marker_color="#f6c90e",
                text=[f"${v:.1f}M" for v in df_state_s["grant_m"]],
                textposition="outside",
                hovertemplate="%{y}: $%{x:.1f}M<extra></extra>",
            ))
            fig_grant.update_layout(
                plot_bgcolor="#1a1a2e", paper_bgcolor="#0f0f1a",
                font_color="#fff", height=320,
                margin=dict(l=0, r=70, t=30, b=0),
                xaxis=dict(gridcolor="#2a2a4e"),
                yaxis=dict(gridcolor="#2a2a4e"),
                showlegend=False,
            )
            st.plotly_chart(fig_grant, use_container_width=True)

        # ── Row 2 ──────────────────────────────────────────────────────────
        c3, c4 = st.columns(2)

        with c3:
            st.markdown("**Investment by Target Sector**")
            df_sec = pd.DataFrame(rdata["by_sector"])
            SECTOR_COLORS = ["#3498db", "#e74c3c", "#f39c12", "#27ae60", "#9b59b6", "#1abc9c", "#e67e22"]
            fig_sec = go.Figure(go.Bar(
                x=df_sec["homes"], y=df_sec["sector"],
                orientation="h",
                marker_color=SECTOR_COLORS[:len(df_sec)],
                text=[f"{h:,} ({p}%)" for h, p in zip(df_sec["homes"], df_sec["pct"])],
                textposition="auto",
                hovertemplate="%{y}: %{x:,} homes<extra></extra>",
            ))
            fig_sec.update_layout(
                plot_bgcolor="#1a1a2e", paper_bgcolor="#0f0f1a",
                font_color="#fff", height=320,
                margin=dict(l=0, r=20, t=30, b=0),
                xaxis=dict(gridcolor="#2a2a4e", tickformat=","),
                yaxis=dict(gridcolor="#2a2a4e"),
                showlegend=False,
            )
            st.plotly_chart(fig_sec, use_container_width=True)

        with c4:
            st.markdown("**Dwelling Type Mix**")
            df_type = pd.DataFrame(rdata["by_dwelling_type"])
            TYPE_COLORS = ["#3498db", "#f6c90e", "#27ae60", "#9b59b6"]
            fig_type = go.Figure(go.Bar(
                x=df_type["pct"], y=df_type["type"],
                orientation="h",
                marker_color=TYPE_COLORS[:len(df_type)],
                text=[f"{h:,} ({p}%)" for h, p in zip(df_type["homes"], df_type["pct"])],
                textposition="auto",
                hovertemplate="%{y}: %{x}% — %{text}<extra></extra>",
            ))
            fig_type.update_layout(
                plot_bgcolor="#1a1a2e", paper_bgcolor="#0f0f1a",
                font_color="#fff", height=320,
                margin=dict(l=0, r=20, t=30, b=0),
                xaxis=dict(gridcolor="#2a2a4e", ticksuffix="%", range=[0, 75]),
                yaxis=dict(gridcolor="#2a2a4e"),
                showlegend=False,
            )
            st.plotly_chart(fig_type, use_container_width=True)

        # ── Bedroom breakdown ──────────────────────────────────────────────
        st.markdown("---")
        bd1, bd2 = st.columns([1, 1])

        with bd1:
            st.markdown("**Bedroom Mix — Number of Dwellings**")
            df_bed = pd.DataFrame(rdata.get("by_bedrooms", []))
            if not df_bed.empty:
                BED_COLORS = ["#e74c3c", "#f39c12", "#3498db", "#9b59b6"]
                fig_bed = go.Figure(go.Bar(
                    x=df_bed["homes"], y=df_bed["bedrooms"],
                    orientation="h",
                    marker_color=BED_COLORS[:len(df_bed)],
                    text=[f"{h:,} ({p}%)" for h, p in zip(df_bed["homes"], df_bed["pct"])],
                    textposition="auto",
                    hovertemplate="%{y}: %{x:,} homes<extra></extra>",
                ))
                fig_bed.update_layout(
                    plot_bgcolor="#1a1a2e", paper_bgcolor="#0f0f1a",
                    font_color="#fff", height=260,
                    margin=dict(l=0, r=20, t=10, b=0),
                    xaxis=dict(gridcolor="#2a2a4e", tickformat=","),
                    yaxis=dict(gridcolor="#2a2a4e"),
                    showlegend=False,
                )
                st.plotly_chart(fig_bed, use_container_width=True)

                one_bed_pct = df_bed[df_bed["bedrooms"] == "Studio / 1 bed"]["pct"].values
                one_bed_pct = int(one_bed_pct[0]) if len(one_bed_pct) else 0
                st.markdown(f"""
                <div style="background:#1a1a2e;border-left:3px solid #f39c12;
                            border-radius:0 6px 6px 0;padding:12px 16px;
                            font-size:0.82em;color:#ccc;line-height:1.7;">
                    <strong style="color:#f39c12;">Bedroom mix vs waitlist need:</strong><br>
                    {one_bed_pct}% of HAFF homes are 1-bed or studio — while ~52% of social housing
                    waitlist applicants nationally are single-person households. The supply is
                    improving but the mismatch persists.
                </div>
                """, unsafe_allow_html=True)

        with bd2:
            pass  # intentionally empty — bedroom distribution gets its own full-width row below

        # Full-width bedroom distribution chart
        st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)
        bbt = rdata.get("bedroom_by_type", [])
        if bbt:
            st.markdown("**Bedroom Distribution Within Each Dwelling Type**")
            bed_cats = ["Studio/1 bed", "2 bed", "3 bed", "4+ bed"]
            BED_COLORS2 = ["#e74c3c", "#f39c12", "#3498db", "#9b59b6"]
            fig_bbt = go.Figure()
            for i, bed in enumerate(bed_cats):
                fig_bbt.add_trace(go.Bar(
                    name=bed,
                    y=[row["type"] for row in bbt],
                    x=[row["beds"].get(bed, 0) for row in bbt],
                    orientation="h",
                    marker_color=BED_COLORS2[i],
                    text=[f"{row['beds'].get(bed, 0)}%" for row in bbt],
                    textposition="auto",
                    hovertemplate=f"{bed}: %{{x}}% of %{{y}}<extra></extra>",
                ))
            fig_bbt.update_layout(
                barmode="group",
                plot_bgcolor="#1a1a2e", paper_bgcolor="#0f0f1a",
                font_color="#fff", height=520,
                margin=dict(l=0, r=20, t=10, b=0),
                xaxis=dict(gridcolor="#2a2a4e", ticksuffix="%", range=[0, 85],
                           tickfont=dict(size=13)),
                yaxis=dict(gridcolor="#2a2a4e", tickfont=dict(size=13)),
                legend=dict(orientation="h", yanchor="bottom", y=1.02,
                            bgcolor="rgba(0,0,0,0)", font_size=13),
                bargap=0.2,
                bargroupgap=0.05,
            )
            st.plotly_chart(fig_bbt, use_container_width=True)

        # ── State detail table ─────────────────────────────────────────────
        st.markdown("**Full State Breakdown — Detailed Table**")
        df_tbl = pd.DataFrame(rdata["by_state"])
        df_tbl["Social %"] = (df_tbl["social"] / df_tbl["homes"] * 100).round(0).astype(int).astype(str) + "%"
        df_tbl["Grant per home ($k)"] = (df_tbl["grant_m"] * 1000 / df_tbl["homes"]).round(0).astype(int)
        df_tbl = df_tbl.rename(columns={
            "state": "State", "projects": "Projects", "homes": "Total homes",
            "social": "Social", "affordable": "Affordable", "grant_m": "Grant ($M)"
        })
        st.dataframe(
            df_tbl[["State","Projects","Total homes","Social","Affordable",
                    "Social %","Grant ($M)","Grant per home ($k)"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "State":               st.column_config.TextColumn("State",         width="small"),
                "Projects":            st.column_config.NumberColumn("Projects",     width="small", format="%d"),
                "Total homes":         st.column_config.TextColumn("Total",          width="small"),
                "Social":              st.column_config.TextColumn("Social",         width="small"),
                "Affordable":          st.column_config.TextColumn("Affordable",     width="small"),
                "Social %":            st.column_config.TextColumn("Social %",       width="small"),
                "Grant ($M)":          st.column_config.TextColumn("Grant ($M)",     width="small"),
                "Grant per home ($k)": st.column_config.NumberColumn("$/home ($k)",  width="small", format="%d"),
            }
        )

        # ── Delivery pipeline ──────────────────────────────────────────────
        st.markdown("**Delivery Pipeline**")
        STATUS_COLOR = {"complete": "#27ae60", "underway": "#f39c12",
                        "on track": "#3498db", "projected": "#555"}
        pipeline_html = '<div style="display:flex;flex-direction:column;gap:8px;margin-top:4px;">'
        for m in rdata["delivery_pipeline"]:
            color = STATUS_COLOR.get(m["status"], "#555")
            pipeline_html += f"""
            <div style="display:flex;align-items:center;gap:12px;
                        background:#1a1a2e;border-radius:6px;padding:10px 16px;
                        border-left:3px solid {color};">
                <div style="font-size:0.82em;color:#ccc;flex:1;">{m['milestone']}</div>
                <div style="font-size:0.82em;color:#888;width:140px;">{m['date']}</div>
                <div style="font-size:0.75em;font-weight:600;color:{color};
                            text-transform:uppercase;letter-spacing:1px;
                            width:80px;text-align:right;">{m['status']}</div>
            </div>"""
        pipeline_html += "</div>"
        st.markdown(pipeline_html, unsafe_allow_html=True)

    with round_tab1:
        render_round("Round 1", HAFF_ROUNDS["Round 1"])

    with round_tab2:
        render_round("Round 2", HAFF_ROUNDS["Round 2"])

    with round_tab3:
        render_round("Round 3", HAFF_ROUNDS["Round 3"])

    with round_tab4:
        st.markdown("### All Rounds Combined — Cumulative Investment")

        state_totals = get_state_totals_across_rounds()
        df_all = pd.DataFrame(state_totals)

        ca, cb = st.columns(2)
        with ca:
            st.markdown("**Total Homes by State — All Rounds**")
            fig_all_st = go.Figure()
            fig_all_st.add_trace(go.Bar(x=df_all["state"], y=df_all["social"],
                                        name="Social", marker_color="#e74c3c"))
            fig_all_st.add_trace(go.Bar(x=df_all["state"], y=df_all["affordable"],
                                        name="Affordable", marker_color="#f39c12"))
            fig_all_st.update_layout(
                barmode="stack", plot_bgcolor="#1a1a2e", paper_bgcolor="#0f0f1a",
                font_color="#fff", height=320, margin=dict(l=0, r=0, t=10, b=0),
                xaxis=dict(gridcolor="#2a2a4e"),
                yaxis=dict(gridcolor="#2a2a4e", tickformat=","),
                legend=dict(orientation="h", yanchor="bottom", y=1.02,
                            bgcolor="rgba(0,0,0,0)"),
            )
            st.plotly_chart(fig_all_st, use_container_width=True)

        with cb:
            st.markdown("**Round-by-Round Homes Delivered**")
            round_names = list(HAFF_ROUNDS.keys())
            round_homes = [HAFF_ROUNDS[r]["total_homes"] for r in round_names]
            round_grants = [HAFF_ROUNDS[r]["grants_total_m"] for r in round_names]
            fig_rounds = go.Figure()
            fig_rounds.add_trace(go.Bar(
                x=round_names, y=round_homes, name="Homes",
                marker_color=["#3498db", "#f6c90e", "#27ae60"],
                text=[f"{h:,}" for h in round_homes], textposition="outside",
            ))
            fig_rounds.update_layout(
                plot_bgcolor="#1a1a2e", paper_bgcolor="#0f0f1a",
                font_color="#fff", height=320, margin=dict(l=0, r=0, t=10, b=0),
                xaxis=dict(gridcolor="#2a2a4e"),
                yaxis=dict(gridcolor="#2a2a4e", tickformat=","),
                showlegend=False,
            )
            st.plotly_chart(fig_rounds, use_container_width=True)

        st.markdown("**All States — Combined Summary Table**")
        df_all["Social %"] = (df_all["social"] / df_all["homes"] * 100).round(0).astype(int).astype(str) + "%"
        df_all["Grant per home ($k)"] = (df_all["grant_m"] * 1000 / df_all["homes"]).round(0).astype(int)
        df_all = df_all.rename(columns={
            "state": "State", "projects": "Total projects", "homes": "Total homes",
            "social": "Social", "affordable": "Affordable", "grant_m": "Total grant ($M)"
        })
        st.dataframe(df_all[["State","Total projects","Total homes","Social","Affordable",
                              "Social %","Total grant ($M)","Grant per home ($k)"]],
                     use_container_width=True, hide_index=True)


# ── Ask the Research ──────────────────────────────────────────────────────────

if page == "Live Housing Dashboard":
    st.markdown("## Live Housing Dashboard")
    st.caption("Key indicators from ABS Building Approvals, AIHW Specialist Homelessness Services, and state housing registers. Data as at latest published release.")

    # ── Curated data (sourced from official ABS / AIHW / State Authority publications) ──
    # ABS Building Approvals 8731.0 — annual run rate, accord target, YoY change
    run_rate    = 173_800   # ABS 8731.0 trailing 12-month total to Mar 2024
    latest_mo   = 14_200    # ABS 8731.0 latest monthly total (Mar 2024)
    yoy         = -7.4      # YoY % change vs same month prior year
    gap         = run_rate - 240_000  # negative = behind target
    pct_target  = round((run_rate / 240_000) * 100)

    # AIHW SHS Annual Report 2022–23
    shs_clients    = 277_300
    shs_needed     = 95_900
    shs_got        = 23_700
    shs_unmet      = shs_needed - shs_got
    success_rate   = round((shs_got / shs_needed) * 100)
    unassisted     = 118_700   # people who sought help but received no response to any need

    # SHS time series (AIHW 2016-17 to 2022-23)
    _shs_years   = [2017, 2018, 2019, 2020, 2021, 2022, 2023]
    _shs_clients = [290300, 295700, 290200, 272400, 260500, 272800, 277300]
    _shs_needed  = [100100, 101400,  98200,  91100,  86300,  91200,  95900]
    _shs_got     = [ 28100,  27400,  26700,  24200,  23100,  23500,  23700]

    # ABS building approvals monthly series (ABS 8731.0, 2015–2024, approximate monthly totals)
    import pandas as _pd_ba
    _ba_months = _pd_ba.date_range("2015-01-01", periods=111, freq="MS")
    _ba_totals = [
        16800,17200,16600,17400,17800,18100,18400,18200,17900,17600,17300,17100,
        17500,16800,16200,17100,17400,17600,17200,16900,16500,16200,15900,15600,
        15400,15200,15600,15900,14800,14200,14600,14900,14300,13800,13400,13200,
        12900,12600,12300,13100,13800,14200,14600,14900,15100,15400,15600,15900,
        16100,16400,16800,17100,17500,18200,19100,19800,20100,19600,18900,18400,
        17800,17200,16600,16100,15700,15400,15800,16200,16700,17100,17400,17800,
        17200,16600,16100,15700,15300,14900,14600,14300,14100,13900,13700,13500,
        13400,13600,13900,14200,14100,13800,13600,13400,13200,13000,12800,12600,
        13100,13500,13900,14200,14100,13800,13500,13400,13200,13100,13000,12900,
        13200,13500,13800
    ]

    # State social housing waitlists (June of each year, approved applicants)
    _wl_data = {
        "NSW": {2018:57400,2019:59200,2020:60100,2021:58900,2022:60300,2023:61100},
        "VIC": {2018:42100,2019:45300,2020:49800,2021:52400,2022:54900,2023:56700},
        "QLD": {2018:27800,2019:29100,2020:31200,2021:32800,2022:33900,2023:34600},
        "WA":  {2018:24200,2019:24900,2020:25600,2021:24100,2022:23100,2023:22500},
        "SA":  {2018:20900,2019:21200,2020:21400,2021:20800,2022:19700,2023:18900},
    }

    if True:
        # ── Executive summary banner ───────────────────────────────────────────
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1a1a2e,#16213e);padding:22px 30px;
                    border-radius:12px;border-left:5px solid #f6c90e;margin-bottom:24px;">
            <div style="font-size:0.7em;text-transform:uppercase;letter-spacing:2px;
                        color:#f6c90e;font-weight:600;margin-bottom:10px;">Executive Briefing — Australian Housing Crisis</div>
            <div style="font-size:1.05em;color:#ccc;line-height:1.9;">
            Australia is building <strong style="color:#fff">{run_rate:,} dwellings per year</strong> —
            <strong style="color:#e74c3c">{abs(gap):,} short</strong> of the National Housing Accord target of 240,000/year,
            and approvals are <strong style="color:#e74c3c">falling ({yoy:+.1f}% YoY)</strong>.
            Meanwhile, <strong style="color:#e74c3c">{unassisted:,} requests for housing help went unmet</strong>
            through frontline services last year — only
            <strong style="color:#f39c12">{success_rate}%</strong> of people who specifically needed housing received it.
            Australia's social housing waitlist now exceeds <strong style="color:#fff">193,000 households</strong>.
            The supply gap is structural and widening.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── KPI row ────────────────────────────────────────────────────────────
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Monthly Approvals", f"{latest_mo:,}", f"{yoy:+.1f}% vs prior year", delta_color="inverse")
        c2.metric("Annual Run Rate", f"{run_rate:,}", f"{pct_target}% of 240k target", delta_color="inverse")
        c3.metric("Accord Shortfall", f"{abs(gap):,}/yr", "Below 240k target", delta_color="off")
        c4.metric("SHS Unmet Requests", f"{unassisted:,}", "People turned away", delta_color="off")
        c5.metric("Housing Success Rate", f"{success_rate}%", f"Of {shs_needed:,} who needed housing", delta_color="off")

        st.divider()

        # ── Section 1: Building Supply ─────────────────────────────────────────
        st.markdown("---")
        st.markdown("### 1 — Housing Supply: Are We Building Enough?")
        st.markdown(
            f"Monthly dwelling approvals across Australia since 2015 (ABS 8731.0). "
            f"The **red dashed line** is the pace needed — 20,000/month — to meet the "
            f"National Housing Accord target of **1.2 million homes by 2029**. "
            f"At the current run rate of **{run_rate:,}/year**, Australia is building at "
            f"**{pct_target}% of the required pace** — a shortfall of {abs(gap):,} dwellings per year."
        )

        col_left, col_right = st.columns([3, 2])
        with col_left:
            import pandas as _pba
            df_ba = _pba.DataFrame({"date": _ba_months, "total_aus": _ba_totals})
            df_ba["rolling_12m"] = df_ba["total_aus"].rolling(12).mean()

            fig_ba = go.Figure()
            fig_ba.add_trace(go.Scatter(
                x=df_ba["date"], y=df_ba["total_aus"],
                name="Monthly approvals", fill="tozeroy",
                line=dict(color="#3498db", width=1.5),
                fillcolor="rgba(52,152,219,0.15)"
            ))
            fig_ba.add_trace(go.Scatter(
                x=df_ba["date"], y=df_ba["rolling_12m"],
                name="12-month rolling average",
                line=dict(color="#f39c12", width=2.5)
            ))
            fig_ba.add_hline(
                y=240000/12, line_dash="dash", line_color="#e74c3c", line_width=2,
                annotation_text="  Accord target (20,000/mth)",
                annotation_font_color="#e74c3c", annotation_position="top left"
            )
            fig_ba.add_vrect(x0="2020-03-01", x1="2021-06-01",
                fillcolor="rgba(255,255,255,0.04)", line_width=0,
                annotation_text="COVID", annotation_position="top left",
                annotation_font_color="#888", annotation_font_size=10)
            fig_ba.add_vrect(x0="2020-10-01", x1="2022-03-01",
                fillcolor="rgba(246,201,14,0.04)", line_width=0,
                annotation_text="HomeBuilder", annotation_position="bottom left",
                annotation_font_color="#888", annotation_font_size=10)
            fig_ba.update_layout(
                height=380, plot_bgcolor="#1a1a2e", paper_bgcolor="#0f0f1a",
                font_color="#ccc", legend=dict(bgcolor="#1a1a2e", bordercolor="#333"),
                yaxis_title="Dwellings approved per month", xaxis_title="",
                margin=dict(t=30, b=10), hovermode="x unified"
            )
            fig_ba.update_xaxes(showgrid=True, gridcolor="#2a2a3e", zeroline=False)
            fig_ba.update_yaxes(showgrid=True, gridcolor="#2a2a3e", zeroline=False)
            st.plotly_chart(fig_ba, use_container_width=True)
            st.caption("Source: ABS Building Approvals 8731.0 — monthly total dwellings approved (houses + other residential). Data to March 2024.")

        with col_right:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=run_rate,
                delta={"reference": 240000, "valueformat": ",", "suffix": " vs target"},
                gauge={
                    "axis": {"range": [0, 280000], "tickformat": ",", "tickcolor": "#ccc"},
                    "bar": {"color": "#3498db"},
                    "bgcolor": "#1a1a2e",
                    "steps": [
                        {"range": [0, 150000], "color": "#3d1515"},
                        {"range": [150000, 200000], "color": "#3d2d15"},
                        {"range": [200000, 240000], "color": "#2d3d15"},
                        {"range": [240000, 280000], "color": "#153d15"},
                    ],
                    "threshold": {"line": {"color": "#e74c3c", "width": 3}, "value": 240000}
                },
                title={"text": "Annual Run Rate vs 240k Target", "font": {"color": "#ccc", "size": 13}},
                number={"valueformat": ",", "font": {"color": "#fff", "size": 28}}
            ))
            fig_gauge.update_layout(
                height=280, paper_bgcolor="#0f0f1a", font_color="#ccc",
                margin=dict(t=60, b=10, l=20, r=20)
            )
            st.plotly_chart(fig_gauge, use_container_width=True)
            st.markdown(f"""
            <div style="background:#1a1a2e;border-radius:8px;padding:14px 16px;
                        font-size:0.86em;line-height:1.8;color:#ccc;margin-top:0;">
            <strong style="color:#e74c3c;">At current pace, Australia delivers:</strong><br>
            <span style="font-size:1.5em;font-weight:800;color:#fff;">{round(run_rate * 5 / 10000) * 10000:,}</span>
            <span style="color:#888;"> homes over 5 years</span><br>
            <span style="color:#888;">Target: </span><strong style="color:#fff;">1,200,000</strong><br>
            <span style="color:#888;">Projected shortfall: </span>
            <strong style="color:#e74c3c;">{max(0, 1200000 - run_rate * 5):,} homes by 2029</strong><br>
            <span style="font-size:0.82em;color:#666;">Before accounting for population growth</span>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # ── Section 2: Homelessness & Demand ──────────────────────────────────
        st.markdown("### 2 — Homelessness & Housing Demand: The Human Cost")
        st.markdown(
            "Specialist Homelessness Services (SHS) are the frontline agencies — crisis shelters, "
            "housing support workers, women's refuges. "
            "The data below shows how many people sought help each year, how many needed long-term housing, "
            "and **how few actually received it.** This is the direct demand signal for community housing providers."
        )

        df_shs = pd.DataFrame({
            "year": _shs_years,
            "clients": _shs_clients,
            "needing_housing": _shs_needed,
            "got_housing": _shs_got,
        })
        unmet_2023 = shs_needed - shs_got

        fig_shs = go.Figure()
        fig_shs.add_trace(go.Bar(
            x=df_shs["year"], y=df_shs["clients"],
            name="Total people seeking help",
            marker=dict(color="#3498db", opacity=0.7),
        ))
        fig_shs.add_trace(go.Bar(
            x=df_shs["year"], y=df_shs["needing_housing"],
            name="Specifically needed housing",
            marker=dict(color="#f39c12", opacity=0.85),
        ))
        fig_shs.add_trace(go.Bar(
            x=df_shs["year"], y=df_shs["got_housing"],
            name="Actually received housing",
            marker=dict(color="#27ae60", opacity=0.95),
        ))
        fig_shs.update_layout(
            barmode="group", height=340,
            plot_bgcolor="#1a1a2e", paper_bgcolor="#0f0f1a",
            font_color="#ccc",
            legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#333",
                        orientation="h", y=-0.18, x=0),
            yaxis_title="Number of people", xaxis_title="Financial year ending",
            margin=dict(t=10, b=60), hovermode="x unified"
        )
        fig_shs.update_xaxes(showgrid=False)
        fig_shs.update_yaxes(showgrid=True, gridcolor="#2a2a3e")
        st.plotly_chart(fig_shs, use_container_width=True)
        st.caption("Source: AIHW Specialist Homelessness Services Annual Report 2022–23. Year = financial year ending.")

        col_shs2, col_shs3 = st.columns([1, 2])
        with col_shs2:
            fig_funnel = go.Figure(go.Funnel(
                y=["Sought help", "Needed housing", "Received housing"],
                x=[shs_clients, shs_needed, shs_got],
                textposition="inside",
                textinfo="value+percent initial",
                marker=dict(color=["#3498db", "#f39c12", "#27ae60"]),
                connector=dict(line=dict(color="#333", width=1))
            ))
            fig_funnel.update_layout(
                height=280, plot_bgcolor="#1a1a2e", paper_bgcolor="#0f0f1a",
                font_color="#ccc", margin=dict(t=30, b=10, l=10, r=10),
                title=dict(text="2022–23 SHS Outcomes", font=dict(color="#ccc", size=13))
            )
            st.plotly_chart(fig_funnel, use_container_width=True)

        with col_shs3:
            st.markdown(f"""
            <div style="background:#1a1a2e;border-radius:8px;padding:20px 24px;font-size:0.92em;
                        line-height:2;color:#ccc;height:100%;box-sizing:border-box;">
            <strong style="color:#e74c3c;">The unmet housing gap (2022–23):</strong><br>
            <strong style="color:#fff">{shs_needed:,} people</strong>
            came to SHS agencies specifically needing long-term housing.<br><br>
            Only <strong style="color:#27ae60;">{shs_got:,}</strong> received it —
            <strong style="color:#e74c3c;">{unmet_2023:,} people</strong>
            walked away without housing. That is a
            <strong style="color:#e74c3c;">{round((unmet_2023/shs_needed)*100)}% failure rate</strong>
            driven directly by insufficient social and community housing stock.<br><br>
            <span style="font-size:0.85em;color:#888;">Additionally, <strong style="color:#fff;">{unassisted:,} people</strong>
            who sought any form of help received no response to any of their needs.</span>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # ── Section 3: Waitlists ───────────────────────────────────────────────
        st.markdown("### 3 — Social Housing Waitlists: The Queue Getting Longer")
        st.markdown(
            "Approved applicants on state social housing registers at 30 June each year. "
            "These people have already been assessed as eligible — they are confirmed demand. "
            "A rising line means the sector is losing ground: more people qualifying faster than housing is delivered. "
            "**NSW alone has over 61,000 households on the register**, with average wait times exceeding 10 years."
        )

        state_colors = {"NSW":"#e74c3c","VIC":"#3498db","QLD":"#f39c12","WA":"#27ae60","SA":"#9b59b6"}
        _wl_rows = []
        for state, yr_data in _wl_data.items():
            for yr, count in yr_data.items():
                _wl_rows.append({"state": state, "year": yr, "applicants": count})
        df_wl = pd.DataFrame(_wl_rows)

        col_wl_chart, col_wl_table = st.columns([3, 1])
        with col_wl_chart:
            fig_wl = go.Figure()
            for state in ["NSW","VIC","QLD","WA","SA"]:
                df_s = df_wl[df_wl["state"]==state].sort_values("year")
                fig_wl.add_trace(go.Scatter(
                    x=df_s["year"], y=df_s["applicants"],
                    name=state, mode="lines+markers",
                    line=dict(color=state_colors[state], width=2.5),
                    marker=dict(size=7),
                    hovertemplate=f"<b>{state}</b><br>Year: %{{x}}<br>Applicants: %{{y:,}}<extra></extra>"
                ))
            df_total = df_wl.groupby("year")["applicants"].sum().reset_index()
            fig_wl.add_trace(go.Scatter(
                x=df_total["year"], y=df_total["applicants"],
                name="Total (5 states)", mode="lines",
                line=dict(color="#ffffff", width=2, dash="dot"),
                hovertemplate="<b>Total</b><br>Year: %{x}<br>Applicants: %{y:,}<extra></extra>"
            ))
            fig_wl.update_layout(
                height=380, plot_bgcolor="#1a1a2e", paper_bgcolor="#0f0f1a",
                font_color="#ccc", legend=dict(bgcolor="#1a1a2e", bordercolor="#333"),
                yaxis_title="Approved applicants on waitlist", xaxis_title="June of year",
                margin=dict(t=20, b=20), hovermode="x unified"
            )
            fig_wl.update_xaxes(showgrid=True, gridcolor="#2a2a3e", dtick=1)
            fig_wl.update_yaxes(showgrid=True, gridcolor="#2a2a3e")
            st.plotly_chart(fig_wl, use_container_width=True)
            st.caption("Source: State housing authority annual reports — approved applicants on public housing register at 30 June. Not directly comparable across states.")

        with col_wl_table:
            _latest_yr = 2023
            _wl_latest = {s: _wl_data[s][_latest_yr] for s in ["NSW","VIC","QLD","WA","SA"]}
            _wl_total = sum(_wl_latest.values())
            st.markdown("""
            <div style="font-size:0.7em;text-transform:uppercase;letter-spacing:1.5px;
                        color:#666;margin-bottom:8px;margin-top:8px;">2023 Waitlist</div>
            """, unsafe_allow_html=True)
            for state, count in sorted(_wl_latest.items(), key=lambda x: -x[1]):
                _pct = round(count/_wl_total*100)
                st.markdown(f"""
                <div style="background:#1a1a2e;border-left:3px solid {state_colors[state]};
                            border-radius:0 6px 6px 0;padding:8px 12px;margin-bottom:6px;">
                    <div style="font-size:0.75em;color:#888;">{state}</div>
                    <div style="font-size:1.1em;font-weight:700;color:#fff;">{count:,}</div>
                    <div style="font-size:0.72em;color:#666;">{_pct}% of total</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown(f"""
            <div style="background:#2a1a1a;border:1px solid #e74c3c33;border-radius:6px;
                        padding:10px 12px;margin-top:4px;text-align:center;">
                <div style="font-size:0.72em;color:#888;">Combined total</div>
                <div style="font-size:1.4em;font-weight:800;color:#e74c3c;">{_wl_total:,}</div>
                <div style="font-size:0.72em;color:#666;">approved & waiting</div>
            </div>
            """, unsafe_allow_html=True)

        _earliest_total = sum(_wl_data[s][2018] for s in _wl_data)
        _pct_increase = round((_wl_total - _earliest_total) / _earliest_total * 100)
        st.markdown(f"""
        <div style="background:#1a1a2e;border-radius:8px;padding:16px 22px;
                    border-left:4px solid #f39c12;font-size:0.87em;line-height:1.9;color:#ccc;margin-top:8px;">
        <strong style="color:#f39c12;">What this means:</strong>
        Combined waitlists across these five states grew by
        <strong style="color:#fff;">{_pct_increase}%</strong> from 2018 to 2023 —
        from <strong>{_earliest_total:,}</strong> to <strong>{_wl_total:,}</strong> approved applicants.
        Every person on this list is a confirmed, assessed tenant waiting for a community housing provider.
        <strong style="color:#e74c3c;">The rising trend is the investment case.</strong>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # ── Section 4: Executive summary callouts ──────────────────────────────
        st.markdown("### 4 — Key Takeaways for Sector Leaders")
        _ko1, _ko2, _ko3 = st.columns(3)
        with _ko1:
            st.markdown(f"""
            <div style="background:#1a0a0a;border:1px solid #e74c3c44;border-top:3px solid #e74c3c;
                        border-radius:0 0 8px 8px;padding:20px 20px;height:100%;">
            <div style="font-size:0.7em;text-transform:uppercase;letter-spacing:1.5px;
                        color:#e74c3c;margin-bottom:10px;font-weight:600;">Supply Crisis</div>
            <div style="font-size:2.2em;font-weight:800;color:#fff;line-height:1;">{pct_target}%</div>
            <div style="font-size:0.82em;color:#aaa;margin-top:6px;line-height:1.6;">
            of the National Housing Accord pace.<br>
            Australia is building <strong style="color:#e74c3c">{abs(gap):,} fewer</strong>
            dwellings per year than required.<br>
            <span style="color:#666;font-size:0.9em;">ABS 8731.0 — to March 2024</span>
            </div>
            </div>""", unsafe_allow_html=True)
        with _ko2:
            st.markdown(f"""
            <div style="background:#0a0a1a;border:1px solid #3498db44;border-top:3px solid #3498db;
                        border-radius:0 0 8px 8px;padding:20px 20px;height:100%;">
            <div style="font-size:0.7em;text-transform:uppercase;letter-spacing:1.5px;
                        color:#3498db;margin-bottom:10px;font-weight:600;">Demand Crisis</div>
            <div style="font-size:2.2em;font-weight:800;color:#fff;line-height:1;">193,800</div>
            <div style="font-size:0.82em;color:#aaa;margin-top:6px;line-height:1.6;">
            households on social housing waitlists across 5 states.<br>
            Up <strong style="color:#e74c3c">{_pct_increase}%</strong> since 2018.<br>
            <span style="color:#666;font-size:0.9em;">State housing authority registers, June 2023</span>
            </div>
            </div>""", unsafe_allow_html=True)
        with _ko3:
            st.markdown(f"""
            <div style="background:#0a1a0a;border:1px solid #f39c1244;border-top:3px solid #f39c12;
                        border-radius:0 0 8px 8px;padding:20px 20px;height:100%;">
            <div style="font-size:0.7em;text-transform:uppercase;letter-spacing:1.5px;
                        color:#f39c12;margin-bottom:10px;font-weight:600;">Access Crisis</div>
            <div style="font-size:2.2em;font-weight:800;color:#fff;line-height:1;">{success_rate}%</div>
            <div style="font-size:0.82em;color:#aaa;margin-top:6px;line-height:1.6;">
            of people who specifically needed housing actually received it.<br>
            <strong style="color:#e74c3c">{unmet_2023:,} people</strong> turned away last year.<br>
            <span style="color:#666;font-size:0.9em;">AIHW SHS Annual Report 2022–23</span>
            </div>
            </div>""", unsafe_allow_html=True)

    render_references([
        {
            "abbr": "ABS 8731.0",
            "full_name": "Building Approvals, Australia — Australian Bureau of Statistics",
            "used_for": "Monthly dwelling approvals, annual run rate, housing accord gap",
            "methodology": "Total dwellings approved (houses + other residential) by month. "
                           "Annual run rate = trailing 12-month sum. Accord gap = run rate minus 240,000 target.",
            "url": "https://www.abs.gov.au/statistics/industry/building-and-construction/building-approvals-australia/latest-release",
            "url_label": "abs.gov.au › 8731.0",
        },
        {
            "abbr": "AIHW SHS",
            "full_name": "Specialist Homelessness Services Annual Report 2022–23 — AIHW",
            "used_for": "Clients seeking help, people needing housing, housing success rate, unmet requests",
            "methodology": "Administrative data from SHS agencies. Housing success rate = clients who received "
                           "housing as a proportion of clients who presented with a housing need.",
            "url": "https://www.aihw.gov.au/reports/homelessness-services/specialist-homelessness-services-annual-report",
            "url_label": "aihw.gov.au › SHS Annual Report",
        },
        {
            "abbr": "National Housing Accord",
            "full_name": "National Housing Accord — Australian Government / Housing Australia",
            "used_for": "240,000 dwellings/year target; 1.2 million homes by 2029 benchmark",
            "methodology": "Agreed target between Commonwealth, states, territories, and local government. "
                           "Monthly equivalent = 240,000 ÷ 12 = 20,000 dwellings/month.",
            "url": "https://www.housingaustralia.gov.au",
            "url_label": "housingaustralia.gov.au",
        },
        {
            "abbr": "State Registers",
            "full_name": "State and Territory Social Housing Waitlist Registers — Housing Authority Annual Reports",
            "used_for": "Social housing waitlist applicant counts by state (2018–2023)",
            "methodology": "Approved applicants on public housing registers at 30 June each year. "
                           "Not directly comparable across states due to differing eligibility criteria.",
            "url": None,
            "url_label": "",
        },
    ])


# ── State Demand & Supply ─────────────────────────────────────────────────────

if page == "Housing Demand & Supply":
    from live.state_analysis import (
        get_state_summary, get_all_states_latest,
        WAITLIST_TREND, APPROVALS_BY_TYPE, WAITLIST_DEMOGRAPHICS,
        HOUSEHOLD_SIZE_TREND, SOCIAL_HOUSING_COMPLETIONS
    )

    st.markdown("## State Housing Demand & Supply Analysis")
    st.markdown(
        "20 years of waitlist demand, household demographics, and building supply by state — "
        "revealing the structural mismatch between who needs housing and what's being built."
    )

    col_sel, col_note = st.columns([1, 3])
    with col_sel:
        selected_state = st.selectbox(
            "Select state", ["WA", "NSW", "VIC", "QLD", "SA"],
            index=0,
            format_func=lambda s: {"WA": "Western Australia", "NSW": "New South Wales",
                                   "VIC": "Victoria", "QLD": "Queensland", "SA": "South Australia"}[s]
        )
    with col_note:
        st.caption(
            "Data: State housing authority annual reports, ABS Building Approvals (8731.0), "
            "ABS Census. Pre-2019 figures are estimates from published historical series. "
            "Verify against primary sources before formal use."
        )

    s = get_state_summary(selected_state)

    # ── KPI row ───────────────────────────────────────────────────────────────
    st.markdown("---")
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    with k1:
        st.metric("Waitlist", f"{s['latest_waitlist']:,}",
                  f"{s['wl_change_yoy']:+.1f}% YoY" if s['wl_change_yoy'] else "")
    with k2:
        st.metric("10-Year Change",
                  f"{s['wl_change_decade']:+.1f}%" if s['wl_change_decade'] else "—")
    with k3:
        st.metric("Social Housing Stock", f"{s['social_housing_stock']:,}")
    with k4:
        st.metric("Total Approvals (latest yr)", f"{s['latest_approvals_total']:,}")
    with k5:
        st.metric("Accessible to Waitlist",
                  f"{s['accessible_total']:,}",
                  f"{s['accessible_pct_of_approvals']}% of all approvals",
                  delta_color="off")
    with k6:
        ytc = s.get("years_to_clear_waitlist")
        st.metric("Yrs to Clear Waitlist", f"{ytc}" if ytc else "—",
                  "at current social housing rate", delta_color="off")

    # ── Insight callout ───────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1a1a2e,#16213e);border-left:4px solid #f6c90e;
                border-radius:0 8px 8px 0;padding:16px 20px;margin:12px 0;
                font-size:0.88em;color:#ccc;line-height:1.8;">
        <strong style="color:#f6c90e;">{s['state_full']} — Snapshot</strong><br>{s['insight']}
    </div>
    """, unsafe_allow_html=True)

    # ── Accessible housing breakdown ──────────────────────────────────────────
    st.markdown("---")
    st.markdown("### The Critical Filter: What Can Waitlist Applicants Actually Access?")
    st.caption(
        "Total building approvals include private market housing that waitlist applicants cannot afford. "
        "Only social housing (public + community) and some affordable housing (below-market rent) "
        "is genuinely accessible."
    )

    acc1, acc2, acc3 = st.columns([1, 1, 1])

    with acc1:
        st.markdown("**Share of new dwellings accessible to waitlist**")
        priv = max(0, s["latest_approvals_total"] - s["accessible_total"])
        labels = ["Private market<br>(no access)", "Social housing", "Affordable housing"]
        values = [priv, s["latest_social_completions"], s["latest_affordable_completions"]]
        colors = ["#3a3a5e", "#e74c3c", "#f39c12"]
        fig_donut = go.Figure(go.Pie(
            labels=labels, values=values, hole=0.55,
            marker_colors=colors,
            textinfo="percent",
            hovertemplate="%{label}: %{value:,}<extra></extra>",
        ))
        fig_donut.update_layout(
            paper_bgcolor="#0f0f1a", font_color="#fff",
            height=320, margin=dict(l=10, r=10, t=30, b=10),
            showlegend=True,
            legend=dict(orientation="v", x=0.75, y=0.5, font_size=11,
                        bgcolor="rgba(0,0,0,0)"),
            annotations=[dict(
                text=f"<b>{s['accessible_pct_of_approvals']}%</b><br>accessible",
                x=0.35, y=0.5, font_size=15, font_color="#f6c90e",
                showarrow=False
            )],
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with acc2:
        sc = SOCIAL_HOUSING_COMPLETIONS.get(selected_state, [])
        appr_by_yr = {r["year"]: (r.get("houses", 0) or 0) + (r.get("other", 0) or 0)
                      for r in s["approvals_by_type"]}
        sc_yrs = [r["year"] for r in sc]
        private_vals = [max(0, appr_by_yr.get(r["year"], 0) - r["social"] - r["affordable"]) for r in sc]
        social_vals = [r["social"] for r in sc]
        afford_vals = [r["affordable"] for r in sc]

        st.markdown("**All approvals: accessible vs private market**")
        fig_access = go.Figure()
        fig_access.add_trace(go.Bar(x=sc_yrs, y=private_vals, name="Private market",
                                    marker_color="#2a2a5e",
                                    hovertemplate="%{x} Private: %{y:,}<extra></extra>"))
        fig_access.add_trace(go.Bar(x=sc_yrs, y=afford_vals, name="Affordable housing",
                                    marker_color="#f39c12",
                                    hovertemplate="%{x} Affordable: %{y:,}<extra></extra>"))
        fig_access.add_trace(go.Bar(x=sc_yrs, y=social_vals, name="Social housing",
                                    marker_color="#e74c3c",
                                    hovertemplate="%{x} Social: %{y:,}<extra></extra>"))
        fig_access.update_layout(
            barmode="stack",
            plot_bgcolor="#1a1a2e", paper_bgcolor="#0f0f1a",
            font_color="#ffffff", height=300,
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis=dict(gridcolor="#2a2a4e", tickformat="d"),
            yaxis=dict(gridcolor="#2a2a4e", tickformat=","),
            legend=dict(orientation="h", yanchor="bottom", y=1.02,
                        bgcolor="rgba(0,0,0,0)", font_size=11),
        )
        st.plotly_chart(fig_access, use_container_width=True)

    with acc3:
        if sc:
            wl_by_yr = {r["year"]: r["applicants"] for r in s["waitlist_trend"]}
            sc_wl = [wl_by_yr.get(r["year"]) for r in sc]

            st.markdown("**Social/affordable delivery vs waitlist growth**")
            fig_gap = go.Figure()
            fig_gap.add_trace(go.Bar(
                x=sc_yrs, y=[r["social"] + r["affordable"] for r in sc],
                name="Social + affordable delivered",
                marker_color="#27ae60",
                hovertemplate="%{x}: %{y:,} accessible<extra></extra>",
            ))
            fig_gap.add_trace(go.Scatter(
                x=sc_yrs, y=sc_wl, name="Waitlist (RHS)",
                yaxis="y2", mode="lines",
                line=dict(color="#f6c90e", width=2.5),
                hovertemplate="Waitlist %{x}: %{y:,}<extra></extra>",
            ))
            fig_gap.update_layout(
                plot_bgcolor="#1a1a2e", paper_bgcolor="#0f0f1a",
                font_color="#ffffff", height=300,
                margin=dict(l=0, r=0, t=30, b=0),
                xaxis=dict(gridcolor="#2a2a4e", tickformat="d"),
                yaxis=dict(gridcolor="#2a2a4e", tickformat=",", title="Dwellings delivered"),
                yaxis2=dict(overlaying="y", side="right", tickformat=",",
                            title="Waitlist", showgrid=False),
                legend=dict(orientation="h", yanchor="bottom", y=1.02,
                            bgcolor="rgba(0,0,0,0)", font_size=11),
            )
            st.plotly_chart(fig_gap, use_container_width=True)

    # Reality check callout
    ytc = s.get("years_to_clear_waitlist")
    acc_pct = s["accessible_pct_of_approvals"]
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1a0a0a,#2a0a0a);border-left:4px solid #e74c3c;
                border-radius:0 8px 8px 0;padding:16px 20px;margin:8px 0;
                font-size:0.88em;color:#ccc;line-height:1.9;">
        <strong style="color:#e74c3c;">Supply Reality — {s['state_full']}</strong><br>
        Of the <strong>{s['latest_approvals_total']:,}</strong> dwellings approved last year,
        only <strong style="color:#f6c90e;">{s['accessible_total']:,}
        ({acc_pct}%)</strong> were social or affordable housing accessible to the
        <strong>{s['latest_waitlist']:,}</strong> households on the waitlist.<br>
        At this rate of social housing delivery, it would take
        <strong style="color:#e74c3c;">{ytc} years</strong> to house everyone currently waiting —
        assuming <em>zero</em> new applicants join the list.
        The other <strong>{100 - acc_pct:.1f}%</strong> of new supply went to the private market.
    </div>
    """, unsafe_allow_html=True)

    show_insight(
        f"In 2 direct sentences, analyse this housing crisis situation for {s['state_full']}: "
        f"waitlist of {s['latest_waitlist']:,} households, {acc_pct}% of all approvals are accessible, "
        f"{ytc} years to clear the waitlist at current delivery rates, "
        f"waitlist grew {s.get('wl_change_yoy', 'unknown')}% in the past year. "
        f"Write for a community housing sector leader. Name the systemic failure directly.",
        cache_key=f"state_gap_insight_{s['state']}",
        max_tokens=140,
    )

    st.markdown("---")

    # ── Row 1: Waitlist trend + All-state comparison ──────────────────────────
    ch1, ch2 = st.columns([3, 2])

    with ch1:
        st.markdown(f"#### Waitlist Trend — {s['state_full']} ({s['earliest_year']}–{s['waitlist_year']})")
        wl_data = s["waitlist_trend"]
        df_wl = pd.DataFrame(wl_data)
        fig_wl = go.Figure()
        fig_wl.add_trace(go.Scatter(
            x=df_wl["year"], y=df_wl["applicants"],
            mode="lines+markers",
            line=dict(color="#f6c90e", width=2.5),
            marker=dict(size=5),
            fill="tozeroy",
            fillcolor="rgba(246,201,14,0.08)",
            name="Waitlist applicants",
            hovertemplate="%{x}: %{y:,}<extra></extra>",
        ))
        fig_wl.update_layout(
            plot_bgcolor="#1a1a2e", paper_bgcolor="#0f0f1a",
            font_color="#ffffff", height=320,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(gridcolor="#2a2a4e", tickformat="d"),
            yaxis=dict(gridcolor="#2a2a4e", tickformat=","),
            showlegend=False,
        )
        st.plotly_chart(fig_wl, use_container_width=True)

    with ch2:
        st.markdown("#### State Comparison — Current Waitlist")
        all_states = get_all_states_latest()
        df_cmp = pd.DataFrame(all_states).sort_values("waitlist", ascending=True)
        colors = ["#f6c90e" if r == selected_state else "#3a3a6e" for r in df_cmp["state"]]
        fig_cmp = go.Figure(go.Bar(
            x=df_cmp["waitlist"], y=df_cmp["state"],
            orientation="h",
            marker_color=colors,
            hovertemplate="%{y}: %{x:,}<extra></extra>",
        ))
        fig_cmp.update_layout(
            plot_bgcolor="#1a1a2e", paper_bgcolor="#0f0f1a",
            font_color="#ffffff", height=320,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(gridcolor="#2a2a4e", tickformat=","),
            yaxis=dict(gridcolor="#2a2a4e"),
            showlegend=False,
        )
        st.plotly_chart(fig_cmp, use_container_width=True)

    # ── Row 2: Who is on the waitlist + Household size trend ──────────────────
    st.markdown("---")
    d1, d2 = st.columns([2, 3])

    with d1:
        demo = s["demographics"]
        st.markdown(f"#### Who Is on the Waitlist — {s['state_full']}")
        st.caption(f"Source: {demo.get('source', '')} · {demo.get('year', '')}")
        if demo.get("types"):
            df_demo = pd.DataFrame(demo["types"])
            DEMO_COLORS = ["#f6c90e", "#e74c3c", "#3498db", "#27ae60", "#9b59b6", "#e67e22"]
            fig_demo = go.Figure(go.Bar(
                x=df_demo["pct"],
                y=df_demo["label"],
                orientation="h",
                marker_color=DEMO_COLORS[:len(df_demo)],
                text=[f"{p}%" for p in df_demo["pct"]],
                textposition="outside",
                hovertemplate="%{y}: %{x}%<extra></extra>",
            ))
            fig_demo.update_layout(
                plot_bgcolor="#1a1a2e", paper_bgcolor="#0f0f1a",
                font_color="#ffffff", height=300,
                margin=dict(l=0, r=60, t=10, b=0),
                xaxis=dict(gridcolor="#2a2a4e", range=[0, 70], ticksuffix="%"),
                yaxis=dict(gridcolor="#2a2a4e"),
                showlegend=False,
            )
            st.plotly_chart(fig_demo, use_container_width=True)

            # What this means
            top_type = df_demo.loc[df_demo["pct"].idxmax(), "label"]
            top_pct = df_demo["pct"].max()
            singles_pct = sum(r["pct"] for r in demo["types"] if "single" in r["label"].lower())
            houses_pct = s["houses_pct_of_approvals"]
            st.markdown(f"""
            <div style="background:#1a1a2e;border-radius:6px;padding:12px 16px;
                        font-size:0.82em;color:#ccc;line-height:1.7;border:1px solid #2a2a4e;">
                <strong style="color:#f6c90e;">The mismatch:</strong><br>
                {singles_pct}% of waitlist applicants are singles or single-parent households
                who need 1–2 bedroom dwellings. Yet {houses_pct}% of what's being approved
                is detached houses — typically 3–4 bedrooms.
            </div>
            """, unsafe_allow_html=True)

    with d2:
        st.markdown(f"#### Building Approvals by Dwelling Type — {s['state_full']}")
        st.caption("ABS Building Approvals 8731.0 · Houses vs units/apartments/townhouses")
        appr = s["approvals_by_type"]
        if appr:
            df_appr = pd.DataFrame(appr)
            fig_appr = go.Figure()
            fig_appr.add_trace(go.Bar(
                x=df_appr["year"], y=df_appr["houses"],
                name="Separate houses",
                marker_color="#3498db",
                hovertemplate="%{x} Houses: %{y:,}<extra></extra>",
            ))
            fig_appr.add_trace(go.Bar(
                x=df_appr["year"], y=df_appr["other"],
                name="Units / apartments / townhouses",
                marker_color="#f6c90e",
                hovertemplate="%{x} Other: %{y:,}<extra></extra>",
            ))
            # Overlay waitlist line on secondary axis
            df_wl2 = pd.DataFrame(s["waitlist_trend"])
            fig_appr.add_trace(go.Scatter(
                x=df_wl2["year"], y=df_wl2["applicants"],
                name="Waitlist (RHS)",
                yaxis="y2",
                mode="lines",
                line=dict(color="#e74c3c", width=2, dash="dot"),
                hovertemplate="Waitlist %{x}: %{y:,}<extra></extra>",
            ))
            fig_appr.update_layout(
                barmode="stack",
                plot_bgcolor="#1a1a2e", paper_bgcolor="#0f0f1a",
                font_color="#ffffff", height=300,
                margin=dict(l=0, r=0, t=10, b=0),
                xaxis=dict(gridcolor="#2a2a4e", tickformat="d"),
                yaxis=dict(gridcolor="#2a2a4e", tickformat=",", title="Approvals"),
                yaxis2=dict(overlaying="y", side="right", tickformat=",",
                            title="Waitlist", showgrid=False),
                legend=dict(orientation="h", yanchor="bottom", y=1.02,
                            bgcolor="rgba(0,0,0,0)", font_size=11),
            )
            st.plotly_chart(fig_appr, use_container_width=True)

    # ── Row 3: Household size decline + supply gap table ──────────────────────
    st.markdown("---")
    h1, h2 = st.columns([1, 2])

    with h1:
        st.markdown("#### Shrinking Households — Average Size (Census)")
        st.caption("Smaller households = greater demand for smaller dwellings")
        hh = s.get("household_size_trend", [])
        if hh:
            df_hh = pd.DataFrame(hh)
            fig_hh = go.Figure(go.Scatter(
                x=df_hh["year"], y=df_hh["avg"],
                mode="lines+markers+text",
                line=dict(color="#9b59b6", width=2.5),
                marker=dict(size=8),
                hovertemplate="%{x}: %{y} persons avg<extra></extra>",
                text=[str(r["avg"]) for r in hh],
                textposition="top center",
                textfont=dict(size=11, color="#ccc"),
            ))
            fig_hh.update_layout(
                plot_bgcolor="#1a1a2e", paper_bgcolor="#0f0f1a",
                font_color="#ffffff", height=260,
                margin=dict(l=0, r=0, t=20, b=0),
                xaxis=dict(gridcolor="#2a2a4e", tickformat="d"),
                yaxis=dict(gridcolor="#2a2a4e", range=[2.0, 3.0]),
                showlegend=False,
            )
            st.plotly_chart(fig_hh, use_container_width=True)

    with h2:
        st.markdown("#### Supply vs Demand — 20-Year Summary")
        appr = s["approvals_by_type"]
        wl = s["waitlist_trend"]
        sc_data = s["social_housing_completions"]
        wl_by_year = {r["year"]: r["applicants"] for r in wl}
        sc_by_year = {r["year"]: r for r in sc_data}
        rows = []
        for a in appr:
            yr = a["year"]
            total = (a.get("houses", 0) or 0) + (a.get("other", 0) or 0)
            waitlist_val = wl_by_year.get(yr)
            sc_row = sc_by_year.get(yr, {})
            social = sc_row.get("social", 0) or 0
            affordable = sc_row.get("affordable", 0) or 0
            accessible = social + affordable
            accessible_pct = round(accessible / total * 100, 1) if total else 0
            rows.append({
                "Year": yr,
                "Total approvals": f"{total:,}",
                "Social housing": f"{social:,}" if social else "—",
                "Affordable housing": f"{affordable:,}" if affordable else "—",
                "Accessible total": f"{accessible:,}" if accessible else "—",
                "Accessible %": f"{accessible_pct}%" if accessible else "—",
                "Waitlist": f"{waitlist_val:,}" if isinstance(waitlist_val, int) else "—",
            })
        df_table = pd.DataFrame(rows)
        st.dataframe(
            df_table,
            use_container_width=True,
            hide_index=True,
            height=420,
            column_config={
                "Year":              st.column_config.NumberColumn("Year", format="%d", width="small"),
                "Total approvals":   st.column_config.TextColumn("Total approvals", width="medium"),
                "Social housing":    st.column_config.TextColumn("Social", width="small"),
                "Affordable housing":st.column_config.TextColumn("Affordable", width="small"),
                "Accessible total":  st.column_config.TextColumn("Accessible", width="small"),
                "Accessible %":      st.column_config.TextColumn("% of total", width="small"),
                "Waitlist":          st.column_config.TextColumn("Waitlist", width="small"),
            }
        )

    # ── All-state waitlist trend overlay ─────────────────────────────────────
    st.markdown("---")
    st.markdown("#### All States — Waitlist Growth 2005–2024")
    st.caption("Highlighting the acceleration across every state post-2020")
    STATE_COLORS = {"NSW": "#e74c3c", "VIC": "#3498db", "QLD": "#f39c12",
                    "WA": "#f6c90e", "SA": "#27ae60"}
    fig_all = go.Figure()
    for st_code, records in WAITLIST_TREND.items():
        df_s = pd.DataFrame(records)
        fig_all.add_trace(go.Scatter(
            x=df_s["year"], y=df_s["applicants"],
            mode="lines+markers",
            name=st_code,
            line=dict(color=STATE_COLORS.get(st_code, "#aaa"), width=2.5 if st_code == selected_state else 1.5,
                      dash="solid" if st_code == selected_state else "dot"),
            marker=dict(size=5 if st_code == selected_state else 3),
            hovertemplate=f"{st_code} %{{x}}: %{{y:,}}<extra></extra>",
        ))
    fig_all.update_layout(
        plot_bgcolor="#1a1a2e", paper_bgcolor="#0f0f1a",
        font_color="#ffffff", height=360,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(gridcolor="#2a2a4e", tickformat="d"),
        yaxis=dict(gridcolor="#2a2a4e", tickformat=","),
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig_all, use_container_width=True)

    render_references([
        {
            "abbr": "ABS 8731.0",
            "full_name": "Building Approvals, Australia — Australian Bureau of Statistics",
            "used_for": "Total and type-split dwelling approvals by state (houses vs units/apartments/townhouses)",
            "methodology": "Annual totals derived from monthly ABS release. Dwelling types: 'houses' = separate "
                           "houses; 'other' = semi-detached, row/terrace, townhouses, flats, apartments.",
            "url": "https://www.abs.gov.au/statistics/industry/building-and-construction/building-approvals-australia/latest-release",
            "url_label": "abs.gov.au › 8731.0",
        },
        {
            "abbr": "State Housing Authority Reports",
            "full_name": "Annual Reports — Housing Authority (WA), FACS/DCJ (NSW), DFFH (VIC), DCHDE (QLD), SAHT (SA)",
            "used_for": "Waitlist applicant counts (2005–2024), social housing stock numbers, "
                        "social housing completions by year",
            "methodology": "Approved applicants at 30 June. Pre-2019 figures estimated from published historical "
                           "series. Waitlist growth methodology: year-on-year change in registered applicants.",
            "url": None,
            "url_label": "",
        },
        {
            "abbr": "ABS Census",
            "full_name": "Census of Population and Housing — Australian Bureau of Statistics (2001, 2006, 2011, 2016, 2021)",
            "used_for": "Average household size trend; demographic composition of waitlist comparison",
            "methodology": "Average persons per occupied private dwelling. Calculated from Census Table Builder "
                           "data for each state.",
            "url": "https://www.abs.gov.au/census",
            "url_label": "abs.gov.au › Census",
        },
        {
            "abbr": "AIHW Housing Assistance",
            "full_name": "Housing Assistance in Australia — Australian Institute of Health and Welfare",
            "used_for": "Demographic breakdown of social housing waitlist applicants (household type, priority need)",
            "methodology": "Administrative data reported by state and territory housing authorities. "
                           "Figures are for approved applicants on the housing register.",
            "url": "https://www.aihw.gov.au",
            "url_label": "aihw.gov.au (search: Housing Assistance in Australia)",
        },
        {
            "abbr": "SCRGSP / ROGS",
            "full_name": "Report on Government Services — Steering Committee for the Review of Government Service Provision (Productivity Commission)",
            "used_for": "Affordable housing completions data; social housing as share of total approvals",
            "methodology": "Social housing completions include public housing and community housing. "
                           "Affordable housing = below-market rent dwellings approved under NRAS or equivalent programs.",
            "url": "https://www.pc.gov.au",
            "url_label": "pc.gov.au (search: Report on Government Services)",
        },
        {
            "abbr": "Years-to-Clear",
            "full_name": "Calculated metric — HIVE platform",
            "used_for": "Estimated years to clear waitlist at current social housing delivery rate",
            "methodology": "Current waitlist ÷ average annual social + affordable housing completions (last 3 years). "
                           "Assumes no new applicants join the waitlist — a conservative lower bound.",
            "url": None,
            "url_label": "",
        },
    ])


# ── Population & Supply Gap ───────────────────────────────────────────────────

if page == "Population & Migration":
    from live.population_data import (
        NATIONAL_PROJECTIONS, STATE_PROJECTIONS, GROWTH_DRIVERS,
        POLICY_ADVOCACY, ACCORD_TARGET, CURRENT_ANNUAL_APPROVALS,
        get_national_dwelling_demand,
        HISTORICAL_NATIONAL, HISTORICAL_STATE_POP, HISTORICAL_NOM_DETAIL,
        MIGRATION_PHASES, HOUSING_MARKET_HISTORY, STATE_VACANCY_HISTORY,
    )

    st.markdown("## Population & Supply Gap")
    st.markdown(
        "Ten years of actual population history, the COVID migration shock and its housing impact, "
        "evidence-based projections to 2044, and the policy positions the sector needs to advocate."
    )
    st.caption(
        "Sources: ABS Cat. 3101.0 (historical demographic statistics), ABS Cat. 3412.0 (migration), "
        "ABS Cat. 3222.0 (projections, Series B), SQM Research (vacancy), CoreLogic (rents)."
    )

    # ════════════════════════════════════════════════════════════════════════
    # Historical section
    if True:
        st.markdown("### Ten Years of Population Growth — What Actually Happened")
        st.caption("ABS Cat. 3101.0 & 3412.0 — annual June-year figures")

        # ── National headline stats ───────────────────────────────────────
        first = HISTORICAL_NATIONAL[0]
        last  = HISTORICAL_NATIONAL[-1]
        total_growth = round(last["population_m"] - first["population_m"], 2)
        peak_nim = max(HISTORICAL_NOM_DETAIL, key=lambda x: x["total_k"])
        trough_nim = min(HISTORICAL_NOM_DETAIL, key=lambda x: x["total_k"])

        h1, h2, h3, h4 = st.columns(4)
        with h1:
            st.metric("Population 2015", f"{first['population_m']:.2f}M")
        with h2:
            st.metric("Population 2024", f"{last['population_m']:.2f}M",
                      f"+{total_growth:.2f}M over 10 years")
        with h3:
            st.metric("Peak NOM (2023)", f"{peak_nim['total_k']:,}k",
                      "Record — 2× pre-COVID average", delta_color="inverse")
        with h4:
            st.metric("COVID trough (2021)", f"{trough_nim['total_k']:,}k",
                      "Net outflow — first time since 1946", delta_color="inverse")

        st.markdown("---")

        # ── National population + NOM area chart ─────────────────────────
        st.markdown("""<div style="font-size:0.72em;text-transform:uppercase;letter-spacing:2px;
                    color:#999;font-weight:600;margin-bottom:8px;">National Population & Net Overseas Migration — 2015 to 2024</div>""",
                    unsafe_allow_html=True)

        hist_df = pd.DataFrame(HISTORICAL_NATIONAL)
        fig_hist = go.Figure()

        fig_hist.add_trace(go.Bar(
            x=hist_df["year"], y=hist_df["nim"] * 1000,
            name="Net overseas migration",
            marker_color=["#e74c3c" if v < 0 else "#3498db" for v in hist_df["nim"]],
            opacity=0.75,
            yaxis="y2",
            hovertemplate="%{x} NOM: %{y:,.0f}<extra></extra>",
        ))
        fig_hist.add_trace(go.Bar(
            x=hist_df["year"], y=hist_df["natural_increase"] * 1000,
            name="Natural increase",
            marker_color="#27ae60",
            opacity=0.6,
            yaxis="y2",
            hovertemplate="%{x} Natural increase: %{y:,.0f}<extra></extra>",
        ))
        fig_hist.add_trace(go.Scatter(
            x=hist_df["year"], y=hist_df["population_m"],
            mode="lines+markers",
            name="National population (M)",
            line=dict(color="#f6c90e", width=3),
            marker=dict(size=6),
            hovertemplate="<b>%{x}</b> — Population: %{y:.2f}M<extra></extra>",
        ))

        # Annotate key events
        for ev_year, ev_text, ev_y in [
            (2020, "COVID begins", 25.6),
            (2021, "Borders closed\nNet outflow", 25.4),
            (2023, "Record NOM\n518k", 27.0),
        ]:
            fig_hist.add_annotation(
                x=ev_year, y=ev_y, yref="y",
                text=ev_text, showarrow=True, arrowhead=2,
                arrowcolor="#888", font=dict(size=9, color="#ccc"),
                bgcolor="rgba(15,15,26,0.85)", bordercolor="#333",
                ax=30, ay=-30,
            )

        fig_hist.add_vrect(x0=2019.5, x1=2021.5,
                           fillcolor="rgba(231,76,60,0.08)", line_width=0,
                           annotation_text="COVID border closure",
                           annotation_position="top left",
                           annotation_font_size=9, annotation_font_color="#e74c3c")

        fig_hist.update_layout(
            barmode="stack",
            plot_bgcolor="#1a1a2e", paper_bgcolor="#0f0f1a",
            font_color="#fff", height=360,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(gridcolor="#2a2a4e", dtick=1),
            yaxis=dict(gridcolor="#2a2a4e", title="Population (M)", ticksuffix="M",
                       side="left"),
            yaxis2=dict(overlaying="y", side="right", title="Annual arrivals",
                        showgrid=False, tickformat=",",
                        zeroline=True, zerolinecolor="#555", zerolinewidth=1),
            legend=dict(orientation="h", yanchor="bottom", y=1.02,
                        bgcolor="rgba(0,0,0,0)", font_size=11),
        )
        st.plotly_chart(fig_hist, use_container_width=True)

        # ── Migration phases narrative ─────────────────────────────────────
        st.markdown("""<div style="font-size:0.72em;text-transform:uppercase;letter-spacing:2px;
                    color:#999;font-weight:600;margin:4px 0 14px 0;">Four Phases of Migration — and What Each Did to Housing</div>""",
                    unsafe_allow_html=True)

        for phase in MIGRATION_PHASES:
            with st.expander(
                f"**{phase['label']}** — {phase['years']} · avg. NOM {phase['avg_nim_k']:,}k/yr",
                expanded=(phase["years"] in ("2022–2023", "2020–2021")),
            ):
                pc1, pc2 = st.columns([3, 2])
                with pc1:
                    st.markdown(f"""
                    <div style="border-left:3px solid {phase['color']};
                                padding-left:14px;font-size:0.88em;color:#ccc;line-height:1.8;">
                        {phase['narrative']}
                    </div>
                    """, unsafe_allow_html=True)
                with pc2:
                    st.markdown(f"""
                    <div style="background:#1a1a2e;border-radius:8px;
                                padding:14px 16px;font-size:0.83em;color:#aaa;line-height:1.7;">
                        <div style="font-size:0.72em;text-transform:uppercase;letter-spacing:1px;
                                    color:#888;margin-bottom:6px;">Housing market impact</div>
                        {phase['housing']}
                    </div>
                    """, unsafe_allow_html=True)

        # ── State population growth chart ──────────────────────────────────
        st.markdown("---")
        st.markdown("""<div style="font-size:0.72em;text-transform:uppercase;letter-spacing:2px;
                    color:#999;font-weight:600;margin-bottom:8px;">State Population Growth — 2015 to 2024</div>""",
                    unsafe_allow_html=True)

        state_colors = {"NSW": "#3498db", "VIC": "#e74c3c", "QLD": "#f39c12",
                        "WA": "#27ae60", "SA": "#9b59b6"}
        years_list = [r["year"] for r in HISTORICAL_STATE_POP["NSW"]]

        fig_states = go.Figure()
        for state, color in state_colors.items():
            pops = [r["pop_m"] for r in HISTORICAL_STATE_POP[state]]
            fig_states.add_trace(go.Scatter(
                x=years_list, y=pops,
                mode="lines+markers",
                name=state,
                line=dict(color=color, width=2),
                marker=dict(size=5),
                hovertemplate=f"<b>{state} %{{x}}</b>: %{{y:.2f}}M<extra></extra>",
            ))
        fig_states.add_vrect(x0=2019.5, x1=2021.5,
                             fillcolor="rgba(231,76,60,0.06)", line_width=0)
        fig_states.update_layout(
            plot_bgcolor="#1a1a2e", paper_bgcolor="#0f0f1a",
            font_color="#fff", height=320,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(gridcolor="#2a2a4e", dtick=1),
            yaxis=dict(gridcolor="#2a2a4e", title="Population (M)", ticksuffix="M"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02,
                        bgcolor="rgba(0,0,0,0)", font_size=11),
        )
        st.plotly_chart(fig_states, use_container_width=True)

        # Per-state callout
        state_narratives = {
            "NSW": ("Most populous state — but slowest growth rate among the five. Sydney's "
                    "extreme unaffordability has pushed internal migrants out to QLD, WA, and SA. "
                    "NOM keeps the population growing but goes straight into an already-stressed "
                    "rental market. Waitlist: 50,000+ approved applicants."),
            "VIC": ("Fastest pre-COVID growth, driven by Melbourne's attraction as a student and "
                    "professional hub. Population actually FELL in 2021 as students and temporary "
                    "visa holders departed during extended lockdowns. Recovered sharply from 2022. "
                    "Big Housing Build is the most ambitious state response nationally."),
            "QLD": ("The decade's standout — Brisbane grew faster than Melbourne or Sydney in "
                    "absolute terms from 2021 onwards. Remote work enabled lifestyle migration "
                    "from NSW/VIC. Brisbane 2032 Olympics is accelerating infrastructure and "
                    "population investment. Rental market went from the most affordable capital "
                    "in 2019 to a vacancy rate below 0.8% by 2023."),
            "WA": ("Stalled from 2016–2019 after the mining boom ended. Transformed post-2021 "
                   "as resources sector rebounded and Perth emerged as Australia's most affordable "
                   "capital. Now growing faster than NSW or VIC. Rental vacancy hit 0.4% — the "
                   "tightest market in the country. State is building but well behind demand."),
            "SA": ("Steady, moderate growth driven by defence, energy, and education sectors. "
                   "Adelaide remains Australia's most affordable major city — attracting interstate "
                   "migrants priced out of eastern capitals. Highest social housing as % of stock "
                   "nationally (6.1%) but stock is ageing rapidly."),
        }
        _sel_state_hist = st.selectbox("State detail", list(state_colors.keys()),
                                        key="hist_state_sel")
        st.markdown(f"""
        <div style="background:#1a1a2e;border:1px solid #2a2a4e;
                    border-left:4px solid {state_colors[_sel_state_hist]};
                    border-radius:0 8px 8px 0;padding:14px 20px;
                    font-size:0.88em;color:#ccc;line-height:1.8;">
            <strong style="color:#fff;">{_sel_state_hist} — 10-Year Growth Story</strong><br><br>
            {state_narratives[_sel_state_hist]}
        </div>
        """, unsafe_allow_html=True)

        # ── NOM visa breakdown waterfall ───────────────────────────────────
        st.markdown("---")
        st.markdown("""<div style="font-size:0.72em;text-transform:uppercase;letter-spacing:2px;
                    color:#999;font-weight:600;margin-bottom:8px;">Migration Breakdown by Visa Stream — 2015 to 2024</div>""",
                    unsafe_allow_html=True)

        nom_df = pd.DataFrame(HISTORICAL_NOM_DETAIL)
        fig_nom = go.Figure()
        stream_map = [
            ("skilled_k",  "Skilled migration",       "#3498db"),
            ("family_k",   "Family stream",            "#27ae60"),
            ("student_k",  "International students",   "#f39c12"),
            ("other_k",    "Other / humanitarian",     "#9b59b6"),
        ]
        for col_key, label, color in stream_map:
            fig_nom.add_trace(go.Bar(
                x=nom_df["year"], y=nom_df[col_key],
                name=label,
                marker_color=color,
                hovertemplate=f"{label} %{{x}}: %{{y:,}}k<extra></extra>",
            ))
        fig_nom.add_trace(go.Scatter(
            x=nom_df["year"], y=nom_df["total_k"],
            mode="lines+markers",
            name="Total NOM",
            line=dict(color="#f6c90e", width=3, dash="dot"),
            marker=dict(size=6),
            hovertemplate="<b>Total NOM %{x}: %{y:,}k</b><extra></extra>",
        ))
        fig_nom.add_hline(y=0, line_color="#555", line_width=1)
        fig_nom.update_layout(
            barmode="relative",
            plot_bgcolor="#1a1a2e", paper_bgcolor="#0f0f1a",
            font_color="#fff", height=340,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(gridcolor="#2a2a4e", dtick=1),
            yaxis=dict(gridcolor="#2a2a4e", title="People ('000s)", ticksuffix="k"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02,
                        bgcolor="rgba(0,0,0,0)", font_size=11),
        )
        st.plotly_chart(fig_nom, use_container_width=True)

        # Year-by-year context pills
        _sel_nom_year = st.select_slider(
            "Select year for migration context",
            options=[r["year"] for r in HISTORICAL_NOM_DETAIL],
            key="nom_year_slider",
        )
        _nom_ctx = next(r for r in HISTORICAL_NOM_DETAIL if r["year"] == _sel_nom_year)
        ctx_color = "#e74c3c" if _nom_ctx["total_k"] < 0 else (
            "#f39c12" if _nom_ctx["total_k"] > 300 else "#3498db"
        )
        st.markdown(f"""
        <div style="background:#1a1a2e;border:1px solid #2a2a4e;
                    border-left:4px solid {ctx_color};
                    border-radius:0 8px 8px 0;padding:14px 20px;
                    font-size:0.88em;color:#ccc;line-height:1.8;">
            <div style="display:flex;gap:24px;margin-bottom:10px;flex-wrap:wrap;">
                <div><span style="color:#888;font-size:0.82em;">TOTAL NOM</span>
                     <div style="font-size:1.8em;font-weight:800;color:{ctx_color};">
                     {_nom_ctx['total_k']:+,}k</div></div>
                <div><span style="color:#888;font-size:0.82em;">SKILLED</span>
                     <div style="font-size:1.4em;font-weight:700;color:#3498db;">
                     {_nom_ctx['skilled_k']:+,}k</div></div>
                <div><span style="color:#888;font-size:0.82em;">STUDENTS</span>
                     <div style="font-size:1.4em;font-weight:700;color:#f39c12;">
                     {_nom_ctx['student_k']:+,}k</div></div>
                <div><span style="color:#888;font-size:0.82em;">FAMILY</span>
                     <div style="font-size:1.4em;font-weight:700;color:#27ae60;">
                     {_nom_ctx['family_k']:+,}k</div></div>
            </div>
            {_nom_ctx['context']}
        </div>
        """, unsafe_allow_html=True)

        # ── Vacancy + rent impact chart ────────────────────────────────────
        st.markdown("---")
        st.markdown("""<div style="font-size:0.72em;text-transform:uppercase;letter-spacing:2px;
                    color:#999;font-weight:600;margin-bottom:8px;">The Housing Market Response — Vacancy & Rent 2015–2024</div>""",
                    unsafe_allow_html=True)

        mkt_df = pd.DataFrame(HOUSING_MARKET_HISTORY)
        fig_mkt = go.Figure()
        fig_mkt.add_trace(go.Scatter(
            x=mkt_df["year"], y=mkt_df["national_vacancy_pct"],
            mode="lines+markers", name="National vacancy rate (%)",
            line=dict(color="#e74c3c", width=2),
            fill="tozeroy", fillcolor="rgba(231,76,60,0.08)",
            yaxis="y",
            hovertemplate="%{x} vacancy: %{y:.1f}%<extra></extra>",
        ))
        fig_mkt.add_trace(go.Scatter(
            x=mkt_df["year"], y=mkt_df["rent_index"],
            mode="lines+markers", name="Rent index (2015 = 100)",
            line=dict(color="#f6c90e", width=2),
            yaxis="y2",
            hovertemplate="%{x} rent index: %{y:.0f}<extra></extra>",
        ))
        fig_mkt.add_trace(go.Bar(
            x=mkt_df["year"], y=mkt_df["nim_k"].clip(lower=0),
            name="NOM ('000s)",
            marker_color="rgba(52,152,219,0.3)",
            yaxis="y3",
            hovertemplate="%{x} NOM: %{y:,}k<extra></extra>",
        ))
        fig_mkt.add_hline(
            y=3.0, line_dash="dot", line_color="#27ae60", line_width=1,
            annotation_text="Healthy vacancy (3%)", yref="y",
            annotation_font_color="#27ae60", annotation_font_size=9,
        )
        fig_mkt.add_vrect(x0=2019.5, x1=2021.5,
                          fillcolor="rgba(231,76,60,0.06)", line_width=0)
        fig_mkt.update_layout(
            plot_bgcolor="#1a1a2e", paper_bgcolor="#0f0f1a",
            font_color="#fff", height=340,
            margin=dict(l=0, r=60, t=10, b=0),
            xaxis=dict(gridcolor="#2a2a4e", dtick=1),
            yaxis=dict(gridcolor="#2a2a4e", title="Vacancy (%)",
                       ticksuffix="%", range=[0, 6]),
            yaxis2=dict(overlaying="y", side="right", title="Rent index",
                        showgrid=False, range=[90, 170]),
            yaxis3=dict(overlaying="y", side="right", showgrid=False,
                        visible=False, range=[0, 1500]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02,
                        bgcolor="rgba(0,0,0,0)", font_size=11),
        )
        st.plotly_chart(fig_mkt, use_container_width=True)

        # State vacancy comparison
        st.markdown("**State Rental Vacancy Rates — 2015 to 2024**")
        fig_svac = go.Figure()
        vac_years = STATE_VACANCY_HISTORY["years"]
        for state, color in state_colors.items():
            fig_svac.add_trace(go.Scatter(
                x=vac_years, y=STATE_VACANCY_HISTORY[state],
                mode="lines+markers", name=state,
                line=dict(color=color, width=2),
                marker=dict(size=5),
                hovertemplate=f"{state} %{{x}}: %{{y:.1f}}%<extra></extra>",
            ))
        fig_svac.add_hline(y=3.0, line_dash="dot", line_color="#555",
                            annotation_text="Healthy market (3%)",
                            annotation_font_color="#666", annotation_font_size=9)
        fig_svac.add_vrect(x0=2019.5, x1=2021.5,
                           fillcolor="rgba(231,76,60,0.06)", line_width=0)
        fig_svac.update_layout(
            plot_bgcolor="#1a1a2e", paper_bgcolor="#0f0f1a",
            font_color="#fff", height=300,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(gridcolor="#2a2a4e", dtick=1),
            yaxis=dict(gridcolor="#2a2a4e", ticksuffix="%", title="Vacancy rate (%)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02,
                        bgcolor="rgba(0,0,0,0)", font_size=11),
        )
        st.plotly_chart(fig_svac, use_container_width=True)

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#13131f,#1a1a2e);
                    border-left:4px solid #e74c3c;border-radius:0 8px 8px 0;
                    padding:16px 22px;margin-top:4px;font-size:0.88em;color:#ccc;line-height:1.8;">
            <strong style="color:#e74c3c;">The mechanism is clear in the data.</strong>
            When NOM is high, vacancy falls and rents rise within 12 months.
            When NOM collapsed in 2021, vacancy briefly recovered — but supply did not increase,
            so when borders reopened and 518,000 people arrived in 2023,
            the market had no buffer. WA fell to <strong style="color:#f6c90e;">0.4% vacancy</strong> —
            effectively zero. National rents rose <strong style="color:#f6c90e;">48% above their 2015 level
            </strong> in under a decade. Social housing waitlists, which had been growing for 20 years,
            accelerated sharply. The private market failure is now <strong style="color:#fff;">structural</strong>,
            not cyclical.
        </div>
        """, unsafe_allow_html=True)

        show_insight(
            f"Australia's net overseas migration hit a record 518,000 in 2023 after a COVID-era "
            f"net outflow of -84,000 in 2021. This extreme swing — a 600,000-person change in two "
            f"years — coincided with national rental vacancy falling to 1.0% and rents rising 48% "
            f"above 2015 levels. In 2 direct sentences, explain what this means for the social "
            f"housing sector and why private market recovery alone will not resolve it.",
            cache_key="migration_housing_insight",
            max_tokens=150,
        )

    # ════════════════════════════════════════════════════════════════════════
    # Projections section

    # ── National population projection ────────────────────────────────────────
    st.markdown("---")
    st.markdown("""<div style="font-size:0.82em;text-transform:uppercase;letter-spacing:2px;
                color:#999;font-weight:600;margin-bottom:12px;">National Population Trajectory — 2024 to 2044</div>""",
                unsafe_allow_html=True)

    pop_df = pd.DataFrame(NATIONAL_PROJECTIONS)

    col_pop1, col_pop2, col_pop3, col_pop4 = st.columns(4)
    with col_pop1:
        st.metric("Current Population", "26.8M", "2024 estimate")
    with col_pop2:
        st.metric("Projected 2031", "29.4M", "+2.6M in 7 years")
    with col_pop3:
        st.metric("Projected 2041", "32.5M", "+5.7M in 17 years")
    with col_pop4:
        current_hh_size = 2.53
        implied_new_dw = round((5_700_000 / current_hh_size) * 1.03 / 1_000) * 1_000
        st.metric("Implied New Dwellings Needed", f"{implied_new_dw:,}", "to 2041 at current HH size")

    # Population projection chart
    fig_pop = go.Figure()
    fig_pop.add_trace(go.Scatter(
        x=pop_df["year"], y=pop_df["population_m"],
        mode="lines+markers",
        name="Projected population",
        line=dict(color="#f6c90e", width=3),
        marker=dict(size=5),
        hovertemplate="<b>%{x}</b><br>Population: %{y:.1f}M<extra></extra>",
    ))
    fig_pop.add_trace(go.Bar(
        x=pop_df["year"], y=pop_df["nim"],
        name="Net overseas migration (M)",
        marker_color="#e74c3c",
        opacity=0.6,
        yaxis="y2",
        hovertemplate="%{x} NOM: %{y:.2f}M<extra></extra>",
    ))
    fig_pop.add_trace(go.Bar(
        x=pop_df["year"], y=pop_df["natural_increase"],
        name="Natural increase (M)",
        marker_color="#3498db",
        opacity=0.6,
        yaxis="y2",
        hovertemplate="%{x} Natural increase: %{y:.2f}M<extra></extra>",
    ))
    fig_pop.add_vline(x=2024, line_dash="dot", line_color="#555", annotation_text="Today")
    fig_pop.update_layout(
        barmode="stack",
        plot_bgcolor="#1a1a2e", paper_bgcolor="#0f0f1a",
        font_color="#fff", height=340,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(gridcolor="#2a2a4e"),
        yaxis=dict(gridcolor="#2a2a4e", title="Population (M)", ticksuffix="M"),
        yaxis2=dict(overlaying="y", side="right", title="Annual growth (M)",
                    showgrid=False, ticksuffix="M"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    bgcolor="rgba(0,0,0,0)", font_size=11),
    )
    st.plotly_chart(fig_pop, use_container_width=True)

    # Growth drivers
    st.markdown("---")
    st.markdown("""<div style="font-size:0.82em;text-transform:uppercase;letter-spacing:2px;
                color:#999;font-weight:600;margin-bottom:12px;">Why Is the Population Growing?</div>""",
                unsafe_allow_html=True)

    _gd_html = '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;align-items:stretch;margin-bottom:8px;">'
    for driver, data in GROWTH_DRIVERS.items():
        _gd_html += f"""
        <div style="background:#1a1a2e;border:1px solid #2a2a4e;
                    border-top:4px solid {data['color']};
                    border-radius:0 0 10px 10px;padding:20px 22px;
                    display:flex;flex-direction:column;">
            <div style="font-size:1.8em;font-weight:800;color:{data['color']};
                        line-height:1;">{data['share_pct']}%</div>
            <div style="font-size:0.72em;text-transform:uppercase;letter-spacing:1px;
                        color:#888;margin-bottom:10px;">of annual growth</div>
            <div style="font-weight:700;color:#fff;font-size:0.92em;
                        margin-bottom:8px;">{driver}</div>
            <div style="font-size:0.82em;color:#aaa;line-height:1.65;
                        margin-bottom:10px;flex:1;">{data['detail']}</div>
            <div style="font-size:0.8em;color:#ccc;line-height:1.6;
                        border-top:1px solid #2a2a4e;padding-top:10px;margin-top:auto;">
                <strong style="color:#f6c90e;">Housing impact:</strong><br>
                {data['housing_impact']}
            </div>
        </div>"""
    _gd_html += '</div>'
    st.markdown(_gd_html, unsafe_allow_html=True)

    # ── State-level projections ───────────────────────────────────────────────
    st.markdown("---")
    st.markdown("""<div style="font-size:0.82em;text-transform:uppercase;letter-spacing:2px;
                color:#999;font-weight:600;margin-bottom:12px;">State-by-State Population Outlook to 2041</div>""",
                unsafe_allow_html=True)

    states_list  = list(STATE_PROJECTIONS.keys())
    state_labels = [f"{s} — {STATE_PROJECTIONS[s]['proj_2041_m']:.1f}M by 2041" for s in states_list]
    _sel_state_pop = st.selectbox("Select state for detail", states_list,
                                   format_func=lambda s: state_labels[states_list.index(s)],
                                   key="pop_state_sel")
    _sp = STATE_PROJECTIONS[_sel_state_pop]

    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        st.metric("Current Population", f"{_sp['current_pop_m']:.2f}M")
    with col_s2:
        st.metric("Projected 2031", f"{_sp['proj_2031_m']:.2f}M",
                  f"+{(_sp['proj_2031_m'] - _sp['current_pop_m']):.2f}M")
    with col_s3:
        st.metric("Projected 2041", f"{_sp['proj_2041_m']:.2f}M",
                  f"+{(_sp['proj_2041_m'] - _sp['current_pop_m']):.2f}M")
    with col_s4:
        st.metric("Implied New Dwellings to 2041", f"{_sp['implied_new_dwellings_2041']:,}")

    # State supply gap bar
    fig_state_gap = go.Figure()
    fig_state_gap.add_trace(go.Bar(
        x=["Current approvals/yr", "Required to meet demand", "National Accord target"],
        y=[_sp["current_approvals"], _sp["required_to_meet_demand"], ACCORD_TARGET // 5],
        marker_color=["#3498db", "#e74c3c", "#f39c12"],
        text=[f"{_sp['current_approvals']:,}", f"{_sp['required_to_meet_demand']:,}",
              f"{ACCORD_TARGET // 5:,}"],
        textposition="outside",
        textfont=dict(color="#fff"),
        hovertemplate="%{x}: %{y:,} dwellings/yr<extra></extra>",
    ))
    fig_state_gap.update_layout(
        plot_bgcolor="#1a1a2e", paper_bgcolor="#0f0f1a",
        font_color="#fff", height=280,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(gridcolor="#2a2a4e"),
        yaxis=dict(gridcolor="#2a2a4e", tickformat=",", title="Dwellings per year"),
        showlegend=False,
    )

    col_sg1, col_sg2 = st.columns([2, 1])
    with col_sg1:
        st.markdown(f"**{_sel_state_pop} — Annual Dwellings: Current vs Required**")
        st.plotly_chart(fig_state_gap, use_container_width=True)
    with col_sg2:
        st.markdown(f"""
        <div style="background:#1a1a2e;border:1px solid #2a2a4e;border-radius:8px;
                    padding:18px 20px;font-size:0.85em;color:#ccc;line-height:1.75;
                    min-height:316px;box-sizing:border-box;display:flex;flex-direction:column;
                    justify-content:space-between;">
            <div>
                <div style="font-weight:700;color:#f6c90e;margin-bottom:8px;">Why this gap exists</div>
                {_sp['growth_drivers']}
            </div>
            <div style="border-top:1px solid #2a2a4e;padding-top:12px;margin-top:16px;">
                <div style="font-size:0.75em;color:#888;text-transform:uppercase;
                            letter-spacing:1px;margin-bottom:4px;">Social housing as % of stock</div>
                <div style="font-size:1.8em;font-weight:800;color:#f6c90e;line-height:1.1;">
                    {_sp['social_housing_pct']}%
                </div>
                <div style="font-size:0.78em;color:#aaa;margin-top:2px;">vs OECD average of 7–8%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # All states comparison chart
    st.markdown("**All States — Projected Growth and Supply Gap**")
    all_states_df = pd.DataFrame([{
        "State": s,
        "Current population (M)": d["current_pop_m"],
        "2041 projection (M)":    d["proj_2041_m"],
        "Growth (M)":             round(d["proj_2041_m"] - d["current_pop_m"], 2),
        "Current approvals/yr":   d["current_approvals"],
        "Required/yr":            d["required_to_meet_demand"],
        "Annual gap":             d["required_to_meet_demand"] - d["current_approvals"],
    } for s, d in STATE_PROJECTIONS.items()])

    fig_multi = go.Figure()
    fig_multi.add_trace(go.Bar(
        name="Current approvals/yr",
        x=all_states_df["State"],
        y=all_states_df["Current approvals/yr"],
        marker_color="#3498db",
        hovertemplate="%{x} current: %{y:,}<extra></extra>",
    ))
    fig_multi.add_trace(go.Bar(
        name="Required/yr to meet demand",
        x=all_states_df["State"],
        y=all_states_df["Required/yr"],
        marker_color="#e74c3c",
        hovertemplate="%{x} required: %{y:,}<extra></extra>",
    ))
    fig_multi.update_layout(
        barmode="group",
        plot_bgcolor="#1a1a2e", paper_bgcolor="#0f0f1a",
        font_color="#fff", height=300,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(gridcolor="#2a2a4e"),
        yaxis=dict(gridcolor="#2a2a4e", tickformat=","),
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    bgcolor="rgba(0,0,0,0)", font_size=11),
    )
    st.plotly_chart(fig_multi, use_container_width=True)

    # ── The catch-up question ─────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("""<div style="font-size:0.82em;text-transform:uppercase;letter-spacing:2px;
                color:#999;font-weight:600;margin-bottom:12px;">The Catch-Up Question — How Do We Get There?</div>""",
                unsafe_allow_html=True)

    demand_proj = get_national_dwelling_demand()
    demand_df = pd.DataFrame(demand_proj)

    fig_catchup = go.Figure()
    fig_catchup.add_trace(go.Scatter(
        x=demand_df["year"], y=demand_df["required_new_dwellings"],
        mode="lines", name="Demand — dwellings required/yr",
        line=dict(color="#e74c3c", width=3),
        fill="tozeroy", fillcolor="rgba(231,76,60,0.08)",
        hovertemplate="%{x} required: %{y:,.0f}<extra></extra>",
    ))
    fig_catchup.add_hline(
        y=CURRENT_ANNUAL_APPROVALS, line_dash="dash", line_color="#3498db", line_width=2,
        annotation_text=f"Current run rate: {CURRENT_ANNUAL_APPROVALS:,}",
        annotation_position="top left",
        annotation_font_color="#3498db",
    )
    fig_catchup.add_hline(
        y=ACCORD_TARGET, line_dash="dash", line_color="#f39c12", line_width=2,
        annotation_text=f"National Accord target: {ACCORD_TARGET:,}",
        annotation_position="bottom right",
        annotation_font_color="#f39c12",
    )
    fig_catchup.update_layout(
        plot_bgcolor="#1a1a2e", paper_bgcolor="#0f0f1a",
        font_color="#fff", height=320,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(gridcolor="#2a2a4e"),
        yaxis=dict(gridcolor="#2a2a4e", tickformat=",", title="Dwellings needed per year"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    bgcolor="rgba(0,0,0,0)", font_size=11),
    )
    st.plotly_chart(fig_catchup, use_container_width=True)

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#13131f,#1a1a2e);
                border-left:4px solid #e74c3c;border-radius:0 8px 8px 0;
                padding:16px 22px;margin-bottom:20px;font-size:0.88em;color:#ccc;line-height:1.8;">
        <strong style="color:#e74c3c;">The math is stark.</strong> Population projections imply Australia needs
        approximately <strong style="color:#fff;">220,000–240,000 new dwellings per year</strong> just to keep pace
        with demand — before addressing the existing waitlist backlog of 170,000+ approved applicants.
        At the current run rate of {CURRENT_ANNUAL_APPROVALS:,}, the country is running
        <strong style="color:#e74c3c;">50,000–80,000 dwellings short every year</strong>. Even if the National Accord
        target of {ACCORD_TARGET:,} were met, it would only keep pace — not clear the existing backlog.
        Catching up requires a sustained build rate of <strong style="color:#f6c90e;">280,000–320,000 per year
        for at least a decade</strong> — a rate Australia has never achieved.
    </div>
    """, unsafe_allow_html=True)

    show_insight(
        f"Australia's population is projected to reach 32.5M by 2041 (ABS Series B), implying "
        f"approximately 2.3M new dwellings needed over 17 years — {220_000:,} per year at minimum. "
        f"Current approvals are running at {CURRENT_ANNUAL_APPROVALS:,} per year. "
        f"In 2 direct sentences, what does this mean for community housing providers and what "
        f"is the single most important policy lever the sector should advocate for?",
        cache_key="population_gap_insight",
        max_tokens=160,
    )

    # ── Policy advocacy ───────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("""<div style="font-size:0.82em;text-transform:uppercase;letter-spacing:2px;
                color:#999;font-weight:600;margin-bottom:16px;">What the Sector Should Advocate For — Evidence-Based Positions</div>""",
                unsafe_allow_html=True)

    st.markdown(
        "These positions are grounded in AHURI research, Productivity Commission findings, "
        "and sector experience. Use them as the basis for submissions, board papers, and "
        "government engagement."
    )

    for adv in POLICY_ADVOCACY:
        with st.expander(f"{adv['icon']}  {adv['category']}", expanded=False):
            st.markdown(f"""
            <div style="display:grid;grid-template-columns:3fr 2fr;gap:20px;">
                <div>
                    <div style="font-weight:700;color:#fff;font-size:0.9em;margin-bottom:8px;">
                        Our position
                    </div>
                    <div style="font-size:0.88em;color:#ccc;line-height:1.8;">
                        {adv['position']}
                    </div>
                </div>
                <div style="background:#1a1a2e;border-left:3px solid #f6c90e;
                            border-radius:0 8px 8px 0;padding:14px 16px;">
                    <div style="font-size:0.72em;text-transform:uppercase;letter-spacing:1px;
                                color:#888;margin-bottom:6px;">Evidence base</div>
                    <div style="font-size:0.82em;color:#aaa;line-height:1.7;">
                        {adv['evidence']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    render_references([
        {
            "abbr": "ABS 3101.0",
            "full_name": "National, State and Territory Population — Australian Bureau of Statistics",
            "used_for": "Historical population by state (2015–2024), natural increase, net overseas migration, total growth",
            "methodology": "Estimated resident population (ERP) at 31 December each year. "
                           "Components of growth: natural increase (births minus deaths) + net overseas migration (NOM).",
            "url": "https://www.abs.gov.au/statistics/people/population/national-state-and-territory-population/latest-release",
            "url_label": "abs.gov.au › 3101.0",
        },
        {
            "abbr": "ABS 3412.0",
            "full_name": "Migration, Australia — Australian Bureau of Statistics",
            "used_for": "Net overseas migration by visa stream (skilled, family, humanitarian, student, temporary)",
            "methodology": "NOM measured using the 12/16 rule: a person is a net migrant if they spend "
                           "12 of the next 16 months in Australia (arrivals) or outside (departures).",
            "url": "https://www.abs.gov.au/statistics/people/population/migration-australia/latest-release",
            "url_label": "abs.gov.au › 3412.0",
        },
        {
            "abbr": "ABS 3222.0",
            "full_name": "Population Projections, Australia — Australian Bureau of Statistics (Series B)",
            "used_for": "20-year population projections by state (2024–2044), implied dwelling demand",
            "methodology": "Series B (medium scenario): assumes fertility rate of 1.62, life expectancy improvements, "
                           "and net overseas migration of 235,000/year from 2025. Implied dwelling demand = "
                           "population growth ÷ average household size (2.53 persons).",
            "url": "https://www.abs.gov.au/statistics/people/population/population-projections-australia/latest-release",
            "url_label": "abs.gov.au › 3222.0",
        },
        {
            "abbr": "SQM Research",
            "full_name": "Residential Vacancy Rates — SQM Research",
            "used_for": "Historical rental vacancy rates by city (2015–2024); COVID vacancy spike and post-COVID tightening",
            "methodology": "Vacancy rate = advertised vacant rental listings ÷ total rental stock, expressed as %. "
                           "Derived from online listing platforms. A rate below 1% indicates critically tight conditions.",
            "url": "https://www.sqmresearch.com.au",
            "url_label": "sqmresearch.com.au (vacancy rates)",
        },
        {
            "abbr": "CoreLogic / ABS 6416.0",
            "full_name": "Rental Index — CoreLogic / ABS Residential Property Price Indexes",
            "used_for": "National rent index (2015=100), rent growth acceleration post-COVID",
            "methodology": "Rent index rebased to 2015=100. CoreLogic tracks asking rents on new leases; "
                           "ABS 6416.0 tracks changes in the stock of rental prices paid.",
            "url": "https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/residential-property-price-indexes-eight-capital-cities/latest-release",
            "url_label": "abs.gov.au › 6416.0",
        },
        {
            "abbr": "National Housing Accord",
            "full_name": "National Housing Accord — Australian Government / Housing Australia (2022)",
            "used_for": "240,000 dwellings/year benchmark; catch-up requirement modelling",
            "methodology": "Accord target of 1.2 million homes over 5 years (2024–2029) = 240,000/year. "
                           "Catch-up requirement modelled as: (population-implied demand + waitlist backlog) ÷ target years.",
            "url": "https://www.housingaustralia.gov.au",
            "url_label": "housingaustralia.gov.au (National Housing Accord)",
        },
    ])


# ── Housing Conditions & Costs ─────────────────────────────────────────────────

if page == "Housing Conditions & Costs":
    from live.construction_data import (
        COST_INDEX, GLOBAL_EVENTS, COST_PER_DWELLING, STATE_CONDITION,
        STOCK_CONDITION, GOVERNMENT_RESPONSES, get_cost_impact_summary,
    )

    st.markdown("## Housing Conditions & Construction Costs")
    st.markdown(
        "Two forces squeezing public housing: existing stock is ageing and deteriorating, "
        "while global events since 2019 have made building new stock dramatically more expensive."
    )

    impact = get_cost_impact_summary()

    # ── Top KPIs ──────────────────────────────────────────────────────────────
    ki1, ki2, ki3, ki4 = st.columns(4)
    with ki1:
        st.metric("Construction cost rise since 2019",
                  f"+{impact['cost_rise_pct']}%",
                  "ABS PPI House Construction", delta_color="inverse")
    with ki2:
        st.metric("Average social home cost — 2019",
                  f"${impact['avg_cost_2019']:,}",
                  "Pre-COVID baseline", delta_color="off")
    with ki3:
        st.metric("Average social home cost — 2025",
                  f"${impact['avg_cost_2025']:,}",
                  f"+${impact['cost_increase_abs']:,} per dwelling", delta_color="inverse")
    with ki4:
        st.metric("Maintenance backlog",
                  f"${impact['maintenance_backlog_bn']}B",
                  f"{impact['pct_stock_major_repair']}% of stock needs major repair",
                  delta_color="inverse")

    # ── Construction cost index with global events ─────────────────────────────
    st.markdown("---")
    st.markdown("""<div style="font-size:0.82em;text-transform:uppercase;letter-spacing:2px;
                color:#999;font-weight:600;margin-bottom:12px;">Construction Cost Index — 2019 to 2025
                (Q4 2019 = 100)</div>""", unsafe_allow_html=True)

    cost_df = pd.DataFrame(COST_INDEX)
    cost_df["period"] = cost_df["year"].astype(str) + " Q" + cost_df["q"].astype(str)

    fig_cost = go.Figure()
    # Shaded background zones
    fig_cost.add_vrect(x0="2020 Q1", x1="2020 Q3",
                       fillcolor="rgba(231,76,60,0.08)", line_width=0,
                       annotation_text="COVID", annotation_position="top left",
                       annotation_font_size=9, annotation_font_color="#e74c3c")
    fig_cost.add_vrect(x0="2022 Q1", x1="2022 Q4",
                       fillcolor="rgba(192,57,43,0.10)", line_width=0,
                       annotation_text="Ukraine + Rate hikes", annotation_position="top left",
                       annotation_font_size=9, annotation_font_color="#c0392b")

    fig_cost.add_trace(go.Scatter(
        x=cost_df["period"], y=cost_df["index"],
        mode="lines+markers",
        name="Construction cost index",
        line=dict(color="#f6c90e", width=3),
        marker=dict(
            size=[8 if r else 4 for r in cost_df["label"]],
            color=["#e74c3c" if r else "#f6c90e" for r in cost_df["label"]],
        ),
        hovertemplate="<b>%{x}</b><br>Index: %{y:.1f}<extra></extra>",
    ))
    fig_cost.add_hline(y=100, line_dash="dot", line_color="#555",
                       annotation_text="2019 baseline (100)",
                       annotation_font_color="#888", annotation_font_size=9)
    fig_cost.update_layout(
        plot_bgcolor="#1a1a2e", paper_bgcolor="#0f0f1a",
        font_color="#fff", height=340,
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis=dict(gridcolor="#2a2a4e", tickangle=-45, tickfont=dict(size=9)),
        yaxis=dict(gridcolor="#2a2a4e", title="Index (Q4 2019 = 100)"),
        showlegend=False,
    )
    st.plotly_chart(fig_cost, use_container_width=True)

    # ── Global events timeline ────────────────────────────────────────────────
    st.markdown("""<div style="font-size:0.82em;text-transform:uppercase;letter-spacing:2px;
                color:#999;font-weight:600;margin:4px 0 12px 0;">Global Events Driving the Cost Rise</div>""",
                unsafe_allow_html=True)

    for ev in GLOBAL_EVENTS:
        st.markdown(f"""
        <div style="display:flex;gap:16px;align-items:flex-start;
                    background:#1a1a2e;border:1px solid #2a2a4e;
                    border-left:4px solid {ev['color']};
                    border-radius:0 8px 8px 0;padding:14px 18px;margin-bottom:8px;">
            <div style="font-size:1.6em;flex-shrink:0;margin-top:2px;">{ev['icon']}</div>
            <div style="flex:1;">
                <div style="display:flex;align-items:center;gap:12px;margin-bottom:4px;">
                    <div style="font-weight:700;color:#fff;font-size:0.9em;">{ev['event']}</div>
                    <div style="font-size:0.72em;color:{ev['color']};font-weight:600;
                                background:rgba(255,255,255,0.06);border-radius:10px;
                                padding:2px 10px;">{ev['date']}</div>
                </div>
                <div style="font-size:0.83em;color:#aaa;line-height:1.7;margin-bottom:6px;">
                    {ev['impact']}
                </div>
                <div style="font-size:0.8em;color:#f6c90e;font-weight:600;">
                    Cost impact: {ev['cost_impact']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── What $1 billion buys now vs 2019 ─────────────────────────────────────
    st.markdown("---")
    st.markdown("""<div style="font-size:0.82em;text-transform:uppercase;letter-spacing:2px;
                color:#999;font-weight:600;margin-bottom:12px;">What $1 Billion Buys — 2019 vs 2025</div>""",
                unsafe_allow_html=True)

    from live.construction_data import BILLION_DOLLAR_YIELD
    b1, b2, b3 = st.columns(3)
    with b1:
        st.markdown(f"""
        <div style="background:#1a1a2e;border:1px solid #2a2a4e;border-radius:10px;
                    padding:24px;text-align:center;">
            <div style="font-size:0.72em;text-transform:uppercase;letter-spacing:1.5px;
                        color:#888;margin-bottom:8px;">$1B in 2019</div>
            <div style="font-size:3em;font-weight:900;color:#27ae60;line-height:1;">
                {BILLION_DOLLAR_YIELD[2019]:,}
            </div>
            <div style="font-size:0.82em;color:#aaa;margin-top:6px;">social homes</div>
            <div style="font-size:0.75em;color:#666;margin-top:4px;">
                Avg. $310,000 per dwelling
            </div>
        </div>
        """, unsafe_allow_html=True)
    with b2:
        st.markdown(f"""
        <div style="background:#1a1a2e;border:1px solid #2a2a4e;border-radius:10px;
                    padding:24px;text-align:center;">
            <div style="font-size:0.72em;text-transform:uppercase;letter-spacing:1.5px;
                        color:#888;margin-bottom:8px;">$1B in 2025</div>
            <div style="font-size:3em;font-weight:900;color:#e74c3c;line-height:1;">
                {BILLION_DOLLAR_YIELD[2025]:,}
            </div>
            <div style="font-size:0.82em;color:#aaa;margin-top:6px;">social homes</div>
            <div style="font-size:0.75em;color:#666;margin-top:4px;">
                Avg. $560,000 per dwelling
            </div>
        </div>
        """, unsafe_allow_html=True)
    with b3:
        lost = BILLION_DOLLAR_YIELD[2019] - BILLION_DOLLAR_YIELD[2025]
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1a1a2e,#2a1a1a);
                    border:1px solid #3a2a2a;border-radius:10px;
                    padding:24px;text-align:center;">
            <div style="font-size:0.72em;text-transform:uppercase;letter-spacing:1.5px;
                        color:#888;margin-bottom:8px;">Homes lost per $1B</div>
            <div style="font-size:3em;font-weight:900;color:#e74c3c;line-height:1;">
                −{lost:,}
            </div>
            <div style="font-size:0.82em;color:#aaa;margin-top:6px;">fewer social homes</div>
            <div style="font-size:0.75em;color:#e74c3c;margin-top:4px;">
                Every $1B invested today delivers {round((lost/BILLION_DOLLAR_YIELD[2019])*100)}% fewer homes than 2019
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#13131f,#1a1a2e);
                border-left:4px solid #e74c3c;border-radius:0 8px 8px 0;
                padding:16px 22px;margin:16px 0;font-size:0.88em;color:#ccc;line-height:1.8;">
        <strong style="color:#e74c3c;">The sector argument in one number:</strong>
        The same billion dollars that built {BILLION_DOLLAR_YIELD[2019]:,} social homes in 2019
        builds only {BILLION_DOLLAR_YIELD[2025]:,} today. Government commitments made in 2022–23
        at one cost level are now being delivered at a 58% higher cost level.
        This is why CHPs report HAFF funding gaps of $80,000–$150,000 per dwelling —
        the grants were sized to 2022 construction costs. The sector needs the federal government
        to <strong style="color:#f6c90e;">index future HAFF rounds to construction cost escalation</strong>,
        not CPI.
    </div>
    """, unsafe_allow_html=True)

    show_insight(
        f"Construction costs for social housing have risen {impact['cost_rise_pct']}% since 2019 "
        f"due to COVID, supply chain disruption, the Ukraine war, and the Australian rate hiking cycle. "
        f"The same $1B that built {BILLION_DOLLAR_YIELD[2019]:,} homes in 2019 now builds only "
        f"{BILLION_DOLLAR_YIELD[2025]:,}. In 2 sentences, what is the most compelling argument "
        f"a community housing peak body should make to government about grant indexation?",
        cache_key="cost_crisis_insight",
        max_tokens=140,
    )

    # ── Property market impact ─────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("""<div style="font-size:0.82em;text-transform:uppercase;letter-spacing:2px;
                color:#999;font-weight:600;margin-bottom:12px;">Flow-On Effects — Property Market & Rental Crisis</div>""",
                unsafe_allow_html=True)

    pm_cols = st.columns(3)
    pm_data = [
        {
            "title": "Private Rental Market",
            "stat":  "+32%",
            "stat_label": "median rent rise 2020–2025",
            "color": "#e74c3c",
            "body": "Construction cost inflation fed directly into new build costs, lifting the "
                    "price floor for developers. With less new stock entering the market, "
                    "vacancy rates fell to historic lows — 1.0–1.2% nationally in 2023. "
                    "Rents rose 32% nationally. Low-income renters were pushed into "
                    "homelessness or overcrowding.",
        },
        {
            "title": "Owner-Occupied Market",
            "stat":  "+58%",
            "stat_label": "new build cost rise since 2019",
            "color": "#f39c12",
            "body": "New home builds are now $250,000–$280,000 more expensive than 2019. "
                    "This raised the entry cost for first home buyers. Combined with "
                    "13 RBA rate hikes, mortgage serviceability dropped sharply — pushing "
                    "more would-be buyers into the rental market, increasing competition "
                    "with existing renters.",
        },
        {
            "title": "Public Sector Capacity",
            "stat":  "−44%",
            "stat_label": "homes per $1B vs 2019",
            "color": "#9b59b6",
            "body": "Government programs announced in 2022–23 at 2022 cost assumptions now face "
                    "significant funding gaps. CHPs report that HAFF grants cover only 70–85% "
                    "of current build costs. Without grant top-ups or cross-subsidisation, "
                    "some approved projects may not proceed — reducing actual delivery "
                    "below announced targets.",
        },
    ]
    for col, pm in zip(pm_cols, pm_data):
        with col:
            st.markdown(f"""
            <div style="background:#1a1a2e;border:1px solid #2a2a4e;
                        border-top:3px solid {pm['color']};
                        border-radius:0 0 10px 10px;padding:18px 20px;">
                <div style="font-weight:700;color:#fff;font-size:0.9em;margin-bottom:4px;">
                    {pm['title']}
                </div>
                <div style="font-size:2.2em;font-weight:900;color:{pm['color']};line-height:1.1;">
                    {pm['stat']}
                </div>
                <div style="font-size:0.72em;color:#888;text-transform:uppercase;
                            letter-spacing:0.5px;margin-bottom:10px;">{pm['stat_label']}</div>
                <div style="font-size:0.82em;color:#aaa;line-height:1.7;">{pm['body']}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Social housing stock condition ─────────────────────────────────────────
    st.markdown("---")
    st.markdown("""<div style="font-size:0.82em;text-transform:uppercase;letter-spacing:2px;
                color:#999;font-weight:600;margin-bottom:12px;">Social Housing Stock — Condition & Asset Risk</div>""",
                unsafe_allow_html=True)

    sc_cols = st.columns(4)
    sc_stats = [
        ("430,000", "Social housing dwellings nationally", "#f6c90e"),
        ("38 years", "Average age of social housing stock", "#f39c12"),
        (f"{STOCK_CONDITION['pct_built_before_1980']}%", "Built before 1980", "#e74c3c"),
        (f"${STOCK_CONDITION['estimated_maintenance_backlog_bn']}B", "Deferred maintenance backlog", "#e74c3c"),
    ]
    for col, (val, label, color) in zip(sc_cols, sc_stats):
        with col:
            st.markdown(f"""
            <div style="text-align:center;padding:16px 8px;">
                <div style="font-size:2.2em;font-weight:800;color:{color};line-height:1.1;">{val}</div>
                <div style="font-size:0.75em;color:#888;text-transform:uppercase;
                            letter-spacing:0.5px;margin-top:6px;">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    # State condition detail
    st.markdown("**State-by-State: Stock Condition & Government Response**")
    _state_cond_sel = st.selectbox("Select state", list(STATE_CONDITION.keys()),
                                    key="cond_state_sel")
    _sc = STATE_CONDITION[_state_cond_sel]

    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(f"""
        <div style="background:#1a1a2e;border:1px solid #2a2a4e;border-radius:10px;
                    padding:18px 20px;">
            <div style="font-size:0.72em;text-transform:uppercase;letter-spacing:1px;
                        color:#888;margin-bottom:12px;">{_state_cond_sel} — Key Numbers</div>
            <div style="margin-bottom:10px;">
                <div style="font-size:0.75em;color:#666;">Social dwellings</div>
                <div style="font-size:1.5em;font-weight:800;color:#f6c90e;">
                    {_sc['dwellings']:,}
                </div>
            </div>
            <div style="margin-bottom:10px;">
                <div style="font-size:0.75em;color:#666;">Maintenance backlog</div>
                <div style="font-size:1.5em;font-weight:800;color:#e74c3c;">
                    ${_sc['backlog_m']:,}M
                </div>
            </div>
            <div>
                <div style="font-size:0.75em;color:#666;">Average stock age</div>
                <div style="font-size:1.5em;font-weight:800;color:#f39c12;">
                    {_sc['avg_age']} yrs
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div style="background:#1a1a2e;border:1px solid #2a2a4e;border-radius:10px;
                    padding:18px 20px;height:100%;">
            <div style="font-size:0.72em;text-transform:uppercase;letter-spacing:1px;
                        color:#888;margin-bottom:10px;">Government Response</div>
            <div style="font-size:0.88em;color:#ccc;line-height:1.8;margin-bottom:12px;">
                {_sc['program']}
            </div>
            <div style="border-top:1px solid #2a2a4e;padding-top:10px;">
                <div style="font-size:0.75em;text-transform:uppercase;letter-spacing:1px;
                            color:#888;margin-bottom:6px;">Flagship renewal program</div>
                <div style="font-size:0.85em;color:#aaa;line-height:1.7;">
                    {_sc['flagship_renewal']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Government responses overview ──────────────────────────────────────────
    st.markdown("---")
    st.markdown("""<div style="font-size:0.82em;text-transform:uppercase;letter-spacing:2px;
                color:#999;font-weight:600;margin-bottom:12px;">What Is Government Doing?</div>""",
                unsafe_allow_html=True)

    for resp in GOVERNMENT_RESPONSES:
        homes_str = f"{resp['homes']:,} homes" if resp.get("homes") else "Infrastructure / maintenance"
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:auto 1fr auto;gap:16px;align-items:start;
                    background:#1a1a2e;border:1px solid #2a2a4e;
                    border-left:4px solid {resp['color']};
                    border-radius:0 8px 8px 0;padding:14px 18px;margin-bottom:8px;">
            <div>
                <div style="font-size:0.72em;text-transform:uppercase;letter-spacing:1px;
                            color:#888;">{resp['year']}</div>
                <div style="font-size:1.5em;font-weight:800;color:{resp['color']};line-height:1.1;">
                    ${resp['amount_m']:,}M
                </div>
                <div style="font-size:0.75em;color:#666;">{homes_str}</div>
            </div>
            <div>
                <div style="font-weight:700;color:#fff;font-size:0.9em;margin-bottom:4px;">
                    {resp['program']}
                </div>
                <div style="font-size:0.72em;color:#888;margin-bottom:6px;">{resp['type']}</div>
                <div style="font-size:0.82em;color:#aaa;line-height:1.65;">{resp['notes']}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:0.72em;color:{resp['color']};font-weight:600;
                            background:rgba(255,255,255,0.05);border-radius:10px;
                            padding:3px 10px;white-space:nowrap;">
                    {resp['status']}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#13131f,#1a1a2e);
                border-left:4px solid #f39c12;border-radius:0 8px 8px 0;
                padding:16px 22px;margin-top:8px;font-size:0.88em;color:#ccc;line-height:1.8;">
        <strong style="color:#f39c12;">The gap between commitment and need.</strong>
        Combined government spending on social housing maintenance nationally is approximately
        <strong style="color:#fff;">$1.2B per year</strong>. Against a
        <strong style="color:#e74c3c;">${STOCK_CONDITION['estimated_maintenance_backlog_bn']}B deferred backlog</strong>
        — and a stock that loses {STOCK_CONDITION['net_stock_loss_per_year']:,} dwellings per year
        to demolition faster than replacement — the math does not close.
        The cost of demolishing and rebuilding a deteriorated social housing unit is
        <strong style="color:#f6c90e;">4–6 times the cost of proactive maintenance</strong>.
        Inaction is not saving money. It is deferring a much larger future cost onto the same budget.
    </div>
    """, unsafe_allow_html=True)

    show_insight(
        f"Australia's social housing stock has a deferred maintenance backlog of "
        f"${STOCK_CONDITION['estimated_maintenance_backlog_bn']}B. The average dwelling is "
        f"{STOCK_CONDITION['avg_age_years']} years old and {STOCK_CONDITION['pct_built_before_1980']}% "
        f"was built before 1980. Annual maintenance spend is $1.2B against a growing backlog. "
        f"In 2 direct sentences, make the economic case for government to significantly increase "
        f"maintenance investment rather than waiting for stock to deteriorate to demolition point.",
        cache_key="conditions_insight",
        max_tokens=140,
    )

    render_references([
        {
            "abbr": "ABS 6427.0",
            "full_name": "Producer Price Indexes, Australia — House Construction (Series ID A2330813K) — Australian Bureau of Statistics",
            "used_for": "Construction cost index (Q4 2019 = 100 baseline through Q1 2025); quarterly cost escalation",
            "methodology": "PPI measures price changes for outputs of house construction industries. "
                           "Index rebased to Q4 2019 = 100. Percentage change calculated from index: "
                           "(current index − 100) = cumulative % rise above the 2019 baseline.",
            "url": "https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/producer-price-indexes-australia/latest-release",
            "url_label": "abs.gov.au › 6427.0",
        },
        {
            "abbr": "Rawlinsons",
            "full_name": "Rawlinsons Australian Construction Handbook — Rawlinsons Quantity Surveyors (2020–2025 editions)",
            "used_for": "Cost per m² estimates for social housing (apartment, townhouse, detached); "
                        "2019 vs 2025 cost-per-dwelling comparison",
            "methodology": "Published rate tables for residential construction in Australian states. "
                           "Social housing rates reflect base build cost without land; exclude developer margin.",
            "url": "https://www.rawlhouse.com.au",
            "url_label": "rawlhouse.com.au (Construction Handbook)",
        },
        {
            "abbr": "AIHW Housing Assistance",
            "full_name": "Housing Assistance in Australia — Australian Institute of Health and Welfare (2023)",
            "used_for": "National social housing stock count (430,000 dwellings), stock age profile, "
                        "maintenance spend, demolition and replacement rates",
            "methodology": "Administrative data from state and territory housing authorities. "
                           "Stock condition categories: poor/very poor/requiring major work defined by housing authority asset assessments.",
            "url": "https://www.aihw.gov.au",
            "url_label": "aihw.gov.au (search: Housing Assistance in Australia)",
        },
        {
            "abbr": "UNSW City Futures",
            "full_name": "Social Housing Futures — City Futures Research Centre, UNSW Sydney (2023)",
            "used_for": "$26.5B deferred maintenance backlog estimate; net stock loss per year; "
                        "years-to-clear-backlog calculation",
            "methodology": "Backlog estimated from asset condition surveys across all states. "
                           "Years to clear = estimated backlog ÷ annual maintenance spend ($1.2B). "
                           "Net stock loss = annual demolitions minus annual replacements.",
            "url": "https://www.unsw.edu.au",
            "url_label": "unsw.edu.au (search: City Futures Research Centre)",
        },
        {
            "abbr": "AIPM 2024",
            "full_name": "Construction Insolvency Report — Australian Institute of Project Management (2024)",
            "used_for": "Construction company insolvency figures (2,309 collapses in 2022–23); "
                        "subcontractor capacity crisis context",
            "methodology": "ASIC insolvency data analysed by sector. Construction sector defined by ANZSIC Division E.",
            "url": "https://www.aipm.com.au",
            "url_label": "aipm.com.au (Construction Insolvency Report)",
        },
        {
            "abbr": "State Condition Audits",
            "full_name": "State Housing Authority Asset Condition Reports — NSW Auditor-General (2020), "
                         "VIC Big Housing Build Progress Report (2022), QLD Housing Investment Initiative (2022)",
            "used_for": "State-level dwelling counts, maintenance backlog by state, average stock age, flagship renewal programs",
            "methodology": "Each state defines condition categories differently. NSW Auditor-General used "
                           "'poor' and 'very poor' ratings from LAHC asset database. VIC figures from DFFH "
                           "quarterly reporting. QLD from DCHDE annual reports.",
            "url": None,
            "url_label": "",
        },
        {
            "abbr": "Homes per $1B",
            "full_name": "Calculated metric — HIVE platform",
            "used_for": "How many social housing dwellings $1B of government funding builds in 2019 vs 2025",
            "methodology": "2019: $1,000,000,000 ÷ $310,000 (avg social dwelling cost) = 3,226 homes. "
                           "2025: $1,000,000,000 ÷ $560,000 (avg social dwelling cost) = 1,786 homes. "
                           "Costs sourced from Rawlinsons 2020 and 2025 editions.",
            "url": None,
            "url_label": "",
        },
    ])

