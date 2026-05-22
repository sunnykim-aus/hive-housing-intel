# 🐝 HIVE — Housing Intelligence & Evidence

> The evidence base for Australian community housing.

HIVE is split into two products with separate deployment targets:

---

## HIVE Data — `app.py`

**Live data dashboards. No API key required.**

Deploy on [Streamlit Community Cloud](https://streamlit.io/cloud) → point to `app.py`.

### Dashboards (5)
| Page | Description |
|---|---|
| Home | Platform overview and data source summary |
| Live Dashboard | ABS building approvals, AIHW homelessness funnel, waitlist trends |
| State Demand & Supply | Waitlist vs supply mismatch by state, 20-year trend |
| Population & Supply Gap | ABS projections to 2044, COVID migration shock, implied dwelling demand |
| Housing Conditions & Costs | $26.5B maintenance backlog, 58% construction cost rise timeline |
| HAFF Investment Tracker | $10B Housing Australia Future Fund round-by-round breakdown |

### Deploy
```
Requirements: requirements.txt
Entry point:  app.py
Secrets:      none required
```

---

## HIVE Intelligence — `app_intelligence.py`

**AI-powered research synthesis + report pipeline. Requires Anthropic API key.**

Deploy on DigitalOcean App Platform or similar (not Streamlit Community Cloud — dependencies too heavy).

### Pages (12)
All HIVE Data dashboards, plus:
| Page | Description |
|---|---|
| Ask the Research | Semantic search across 681+ indexed reports — AI synthesised answer |
| Policy Impact | Evidence-based impact assessment for any major housing program |
| Outcome Ledger | Federal housing investment tracked: promised vs delivered |
| Policy Timeline | Housing policy history 2008–2025 |
| Browse Reports | Manage indexed reports, run ingest pipeline |
| Weekly Digest | AI-generated sector briefing |

### Deploy
```
Requirements: requirements_intelligence.txt
Entry point:  app_intelligence.py
Secrets:      ANTHROPIC_API_KEY (required)
Pipeline:     chromadb + sentence-transformers (local or cloud volume)
```

---

## Local development

```bash
# Clone and install
git clone https://github.com/sunnykim-aus/hive-housing-intel.git
cd hive-housing-intel

# Data app (no API key)
pip install -r requirements.txt
streamlit run app.py

# Intelligence app (needs API key + pipeline)
pip install -r requirements_intelligence.txt
cp .env.example .env          # add your ANTHROPIC_API_KEY
streamlit run app_intelligence.py
```

---

## Data sources

| Source | Used for |
|---|---|
| ABS | Building approvals, Census, population projections |
| AIHW | Homelessness SHS data, indigenous housing |
| AHURI | 15 years of housing research reports |
| Housing Australia | HAFF round data, bond aggregation |
| Treasury | Budget Papers 2010–2026, program allocations |
| Productivity Commission | Housing inquiries, Report on Government Services |
| DSS | NAHA, NRAS, homelessness strategy |
| State housing registers | Waitlist data by state |

---

Built by [Sunny Kim](https://www.linkedin.com/in/sunny-kim-58a780100/) — Housing Data Lead, Australian community housing sector.
