"""
Weekly Housing Intelligence Digest.
Uses Claude to synthesise new reports + live data into a readable email brief.
Covers: national supply/demand, state-level demand & supply, HAFF investment tracker,
SHS homelessness indicators, and newly indexed research.
"""
import os
import json
from datetime import date, timedelta
from pathlib import Path
import anthropic

from config import META_FILE, CLAUDE_MODEL, DATA_DIR
from live.abs_feed import fetch_housing_indicators
from live.shs_feed import get_shs_summary
from live.state_analysis import get_state_summary, get_all_states_latest
from live.haff_data import get_haff_summary, HAFF_ROUNDS

_client = None


def get_client():
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    return _client


def get_new_reports(days=7):
    """Find reports added to the index in the last N days."""
    if not META_FILE.exists():
        return []
    new = []
    for line in META_FILE.read_text().splitlines():
        try:
            r = json.loads(line)
            if r.get("title") and r.get("source"):
                new.append(r)
        except Exception:
            pass
    return new[:10]


def get_digest_stats():
    """Compile all current housing stats for the digest."""
    stats = {}

    try:
        stats["building_approvals"] = fetch_housing_indicators()
    except Exception as e:
        stats["building_approvals"] = {"error": str(e)}

    try:
        stats["shs"] = get_shs_summary()
    except Exception as e:
        stats["shs"] = {"error": str(e)}

    try:
        # WA as focus state — most relevant for user's org
        stats["wa"] = get_state_summary("WA")
        stats["all_states"] = get_all_states_latest()
    except Exception as e:
        stats["wa"] = {"error": str(e)}

    try:
        stats["haff"] = get_haff_summary()
        stats["haff_r1"] = HAFF_ROUNDS["Round 1"]
        stats["haff_r2"] = HAFF_ROUNDS["Round 2"]
        stats["haff_r3"] = HAFF_ROUNDS["Round 3"]
    except Exception as e:
        stats["haff"] = {"error": str(e)}

    return stats


def generate_digest_text(stats, new_reports):
    """Use Claude to write the digest narrative."""
    ba = stats.get("building_approvals", {})
    shs = stats.get("shs", {})
    wa = stats.get("wa", {})
    haff = stats.get("haff", {})

    def _n(v, fmt=","):
        """Format a number safely, returning N/A for None/missing."""
        if v is None or v == "":
            return "N/A"
        try:
            return format(v, fmt)
        except (TypeError, ValueError):
            return str(v)

    r3 = HAFF_ROUNDS.get("Round 3", {})
    context = f"""
Current Housing Data (as of {date.today().strftime('%d %B %Y')}):

NATIONAL SUPPLY (ABS Building Approvals):
- Latest month: {ba.get('latest_month', 'N/A')}
- Monthly approvals: {_n(ba.get('latest_total'))} dwellings
- Annual run rate: {_n(ba.get('annual_run_rate'))} dwellings/year
- National Housing Accord target: 240,000/year
- Gap to accord target: {_n(ba.get('gap_to_accord_target'))} dwellings/year
- Year-on-year change: {ba.get('yoy_change_pct', 'N/A')}%

SPECIALIST HOMELESSNESS SERVICES (AIHW):
- Latest year: {shs.get('latest_year', 'N/A')}
- Total clients: {_n(shs.get('total_clients'))}
- Unassisted requests: {_n(shs.get('unassisted_requests'))}
- Housing success rate: {shs.get('housing_success_rate', 'N/A')}%
- Unmet need rate: {shs.get('unmet_need_rate', 'N/A')}%
- Client change YoY: {shs.get('client_change_yoy', 'N/A')}%

WESTERN AUSTRALIA — STATE DEMAND & SUPPLY:
- Current waitlist: {_n(wa.get('latest_waitlist'))} approved applicants
- Waitlist change YoY: {wa.get('wl_change_yoy', 'N/A')}%
- Total building approvals (latest yr): {_n(wa.get('latest_approvals_total'))}
- Social/affordable housing delivered: {_n(wa.get('accessible_total'))} ({wa.get('accessible_pct_of_approvals', 'N/A')}% of all approvals)
- Years to clear waitlist at current rate: {wa.get('years_to_clear_waitlist', 'N/A')}
- Key insight: {wa.get('insight', '')[:200]}

HAFF INVESTMENT (all rounds to date):
- Total homes announced: {_n(haff.get('total_homes'))} of 30,000 target
- Total grants committed: ${_n(haff.get('total_grants_m'), ',.0f')}M
- Progress to target: {haff.get('pct_of_5yr_target', 'N/A')}%
- Total projects: {_n(haff.get('total_projects'))}
- Round 3 (latest): {_n(r3.get('total_homes'))} homes, ${r3.get('grants_total_m', 'N/A')}M, status: {r3.get('status', 'N/A')}

New reports indexed this week: {len(new_reports)}
{chr(10).join(f'- {r.get("title","")[:80]} ({r.get("source","")}, {r.get("year","")})' for r in new_reports[:5])}
"""

    prompt = f"""You are writing a weekly Housing Intelligence Digest for a community housing professional in Australia.
Write a concise, insightful brief (plain text, no markdown) covering these 5 sections:

1. SUPPLY PULSE (2-3 sentences on national building approvals vs accord target)
2. DEMAND SIGNAL (2-3 sentences on SHS data and what it means for the sector)
3. STATE SPOTLIGHT — WA (2-3 sentences on WA waitlist, the supply/demand mismatch, and the accessible housing gap)
4. HAFF WATCH (2-3 sentences on HAFF delivery progress across rounds, what's on track, what to watch)
5. WHAT TO WATCH THIS WEEK (2 key things for sector leaders to monitor)

Be specific with numbers. Be direct. Write for a sector leader, not a general audience.
No fluff. No hedging. If numbers are bad, say so plainly.

Data:
{context}"""

    client = get_client()
    r = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}],
    )
    return r.content[0].text


def build_html_digest(stats, new_reports, narrative):
    """Build HTML email body with all updated data sections."""
    ba = stats.get("building_approvals", {})
    shs = stats.get("shs", {})
    wa = stats.get("wa", {})
    haff = stats.get("haff", {})
    today = date.today().strftime("%d %B %Y")

    gap = ba.get("gap_to_accord_target", 0) or 0
    gap_color = "#e74c3c" if gap < -20000 else "#f39c12" if gap < 0 else "#27ae60"
    run_rate = ba.get("annual_run_rate", 0) or 0
    target = 240000
    pct_of_target = round((run_rate / target) * 100) if target else 0

    wa_waitlist = wa.get("latest_waitlist", 0) or 0
    wa_accessible = wa.get("accessible_total", 0) or 0
    wa_acc_pct = wa.get("accessible_pct_of_approvals", 0) or 0
    wa_ytc = wa.get("years_to_clear_waitlist", "—")

    haff_homes = haff.get("total_homes", 0) or 0
    haff_pct = haff.get("pct_of_5yr_target", 0) or 0
    haff_grants = haff.get("total_grants_m", 0) or 0

    new_reports_html = "".join(
        f'<li><strong>{r.get("source","")}</strong> — {r.get("title","")[:70]} ({r.get("year","")})</li>'
        for r in new_reports[:5]
    ) or "<li>No new reports this week</li>"

    narrative_html = narrative.replace("\n\n", "</p><p>").replace("\n", "<br>")

    all_states = stats.get("all_states", [])
    states_rows = "".join(
        f'<tr style="border-bottom:1px solid #2a2a4e;">'
        f'<td style="padding:6px 10px;">{s["state"]}</td>'
        f'<td style="padding:6px 10px;text-align:right;">{s["waitlist"]:,}</td>'
        f'<td style="padding:6px 10px;text-align:right;">{s["approvals_total"]:,}</td>'
        f'<td style="padding:6px 10px;text-align:right;">{round(s["approvals_total"]/s["waitlist"]*100) if s["waitlist"] else "—"}%</td>'
        f'</tr>'
        for s in all_states
    )

    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
         color: #1a1a2e; background: #f5f5f5; margin: 0; padding: 20px; }}
  .container {{ max-width: 680px; margin: 0 auto; background: white;
                border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
  .header {{ background: #1a1a2e; color: white; padding: 24px 32px; }}
  .header h1 {{ margin: 0; font-size: 20px; }}
  .header p {{ margin: 4px 0 0; color: #aaa; font-size: 13px; }}
  .body {{ padding: 24px 32px; }}
  .kpi-row {{ display: flex; gap: 10px; margin: 14px 0; flex-wrap: wrap; }}
  .kpi {{ flex: 1; min-width: 120px; background: #f8f9fa; border-radius: 6px;
          padding: 10px 14px; border-left: 4px solid #1a1a2e; }}
  .kpi .label {{ font-size: 10px; color: #666; text-transform: uppercase;
                 letter-spacing: 0.5px; margin-bottom: 2px; }}
  .kpi .value {{ font-size: 20px; font-weight: bold; color: #1a1a2e; line-height: 1.1; }}
  .kpi .sub {{ font-size: 10px; color: #888; margin-top: 2px; }}
  .section {{ margin: 20px 0; }}
  .section h2 {{ font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px;
                 color: #666; border-bottom: 1px solid #eee; padding-bottom: 6px;
                 margin-bottom: 12px; }}
  .narrative {{ line-height: 1.7; color: #333; font-size: 14px; }}
  .new-reports {{ background: #eef7ff; border-radius: 6px; padding: 14px 18px; }}
  .new-reports ul {{ margin: 6px 0; padding-left: 18px; }}
  .new-reports li {{ margin: 4px 0; font-size: 13px; color: #333; }}
  .footer {{ background: #f8f9fa; padding: 14px 32px; font-size: 11px; color: #999;
             border-top: 1px solid #eee; }}
  .state-table {{ width:100%; border-collapse:collapse; font-size:12px; }}
  .state-table th {{ background:#f8f9fa; padding:6px 10px; text-align:left;
                     color:#666; font-weight:500; border-bottom:2px solid #eee; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>HIVE — Housing Intelligence Digest</h1>
    <p>Week of {today} &nbsp;·&nbsp; Australian Community Housing Sector</p>
  </div>
  <div class="body">

    <div class="section">
      <h2>National Supply &amp; Demand</h2>
      <div class="kpi-row">
        <div class="kpi" style="border-left-color:#3498db;">
          <div class="label">Monthly Approvals</div>
          <div class="value">{ba.get('latest_total') and f"{ba['latest_total']:,}" or '—'}</div>
          <div class="sub">{ba.get('latest_month','')} · {ba.get('yoy_change_pct','—')}% YoY</div>
        </div>
        <div class="kpi" style="border-left-color:{gap_color};">
          <div class="label">Accord Gap</div>
          <div class="value">{abs(gap):,}</div>
          <div class="sub">dwellings/yr below 240k target ({pct_of_target}%)</div>
        </div>
        <div class="kpi" style="border-left-color:#e74c3c;">
          <div class="label">SHS Unassisted</div>
          <div class="value">{shs.get('unassisted_requests') and f"{shs['unassisted_requests']:,}" or '—'}</div>
          <div class="sub">{shs.get('latest_year','')} · {shs.get('unassisted_change_yoy','—')}% YoY</div>
        </div>
        <div class="kpi" style="border-left-color:#f39c12;">
          <div class="label">Housing Success Rate</div>
          <div class="value">{shs.get('housing_success_rate','—')}%</div>
          <div class="sub">of those needing housing who received it</div>
        </div>
      </div>
    </div>

    <div class="section">
      <h2>WA State Spotlight — Demand vs Accessible Supply</h2>
      <div class="kpi-row">
        <div class="kpi" style="border-left-color:#f6c90e;">
          <div class="label">WA Waitlist</div>
          <div class="value">{wa_waitlist:,}</div>
          <div class="sub">{wa.get('wl_change_yoy','—')}% YoY change</div>
        </div>
        <div class="kpi" style="border-left-color:#e74c3c;">
          <div class="label">Accessible Homes Built</div>
          <div class="value">{wa_accessible:,}</div>
          <div class="sub">{wa_acc_pct}% of all approvals in WA</div>
        </div>
        <div class="kpi" style="border-left-color:#9b59b6;">
          <div class="label">Yrs to Clear Waitlist</div>
          <div class="value">{wa_ytc}</div>
          <div class="sub">at current social housing delivery rate</div>
        </div>
      </div>
      {'<table class="state-table"><thead><tr><th>State</th><th style="text-align:right;">Waitlist</th><th style="text-align:right;">Total Approvals</th><th style="text-align:right;">Approvals per waitlist applicant</th></tr></thead><tbody>' + states_rows + '</tbody></table>' if states_rows else ''}
    </div>

    <div class="section">
      <h2>HAFF Investment Tracker — All Rounds</h2>
      <div class="kpi-row">
        <div class="kpi" style="border-left-color:#27ae60;">
          <div class="label">Homes Announced</div>
          <div class="value">{haff_homes:,}</div>
          <div class="sub">{haff_pct}% of 30,000 target</div>
        </div>
        <div class="kpi" style="border-left-color:#3498db;">
          <div class="label">Grants Committed</div>
          <div class="value">${haff_grants:,.0f}M</div>
          <div class="sub">Rounds 1–3 combined</div>
        </div>
        <div class="kpi" style="border-left-color:#f39c12;">
          <div class="label">Round 3 Status</div>
          <div class="value">{HAFF_ROUNDS['Round 3']['total_homes']:,} homes</div>
          <div class="sub">{HAFF_ROUNDS['Round 3']['status']}</div>
        </div>
      </div>
    </div>

    <div class="section">
      <h2>This Week's Analysis</h2>
      <div class="narrative"><p>{narrative_html}</p></div>
    </div>

    <div class="section">
      <h2>New Reports Indexed</h2>
      <div class="new-reports">
        <ul>{new_reports_html}</ul>
      </div>
    </div>

    <div class="section">
      <h2>Key Indicators Summary</h2>
      <table style="width:100%;border-collapse:collapse;font-size:12px;">
        <tr style="background:#f8f9fa;">
          <td style="padding:7px 10px;"><strong>SHS clients seeking help</strong></td>
          <td style="padding:7px 10px;text-align:right;">{shs.get('total_clients','—'):,}</td>
        </tr>
        <tr>
          <td style="padding:7px 10px;"><strong>Annual build run rate</strong></td>
          <td style="padding:7px 10px;text-align:right;">{run_rate:,} dwellings/year</td>
        </tr>
        <tr style="background:#f8f9fa;">
          <td style="padding:7px 10px;"><strong>National Accord target</strong></td>
          <td style="padding:7px 10px;text-align:right;">240,000 dwellings/year</td>
        </tr>
        <tr>
          <td style="padding:7px 10px;"><strong>HAFF homes announced (all rounds)</strong></td>
          <td style="padding:7px 10px;text-align:right;">{haff_homes:,} of 30,000</td>
        </tr>
        <tr style="background:#f8f9fa;">
          <td style="padding:7px 10px;"><strong>WA social housing accessible</strong></td>
          <td style="padding:7px 10px;text-align:right;">{wa_acc_pct}% of all WA approvals</td>
        </tr>
      </table>
    </div>

  </div>
  <div class="footer">
    Generated by HIVE — Housing Intelligence &amp; Evidence &nbsp;·&nbsp; {today}<br>
    Built by <a href="https://www.linkedin.com/in/sunny-kim-58a780100/" style="color:#f6c90e;">Sunny Kim</a>
    &nbsp;·&nbsp; Data: ABS, AIHW, Housing Australia, State housing authorities<br>
    For internal use only — verify before external publication.
  </div>
</div>
</body>
</html>
"""


def generate_digest():
    """Full digest generation pipeline. Returns (html, plain_text, stats)."""
    stats = get_digest_stats()
    new_reports = get_new_reports(days=7)
    narrative = generate_digest_text(stats, new_reports)
    html = build_html_digest(stats, new_reports, narrative)
    return html, narrative, stats
