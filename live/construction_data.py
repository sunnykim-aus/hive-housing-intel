"""
Construction cost index, global events timeline, and housing condition data.
Sources:
  - ABS Cat. 6427.0 — Producer Price Indexes, House Construction (Series ID A2330813K)
  - Rawlinsons Australian Construction Handbook 2020–2025
  - AIHW — Housing Assistance in Australia 2023
  - UNSW City Futures — Social Housing Futures 2023
  - Australian Institute of Project Management — Construction Insolvency Report 2024
"""

# ── Construction cost index (ABS PPI House Construction, Q4 2019 = 100) ─────
# Quarterly: year, quarter (1–4), index value, and annotation if major event
COST_INDEX = [
    {"year": 2019, "q": 4, "index": 100.0, "label": None},
    {"year": 2020, "q": 1, "index": 100.4, "label": "COVID-19 shutdowns begin (Mar 2020)"},
    {"year": 2020, "q": 2, "index": 100.1, "label": None},
    {"year": 2020, "q": 3, "index": 101.8, "label": "HomeBuilder scheme launches — demand surge"},
    {"year": 2020, "q": 4, "index": 103.2, "label": None},
    {"year": 2021, "q": 1, "index": 106.1, "label": "Timber shortage: framing lumber +130% globally"},
    {"year": 2021, "q": 2, "index": 109.8, "label": "Suez Canal blocked — shipping containers crisis"},
    {"year": 2021, "q": 3, "index": 113.5, "label": None},
    {"year": 2021, "q": 4, "index": 118.2, "label": "HomeBuilder completions backlog peaks"},
    {"year": 2022, "q": 1, "index": 125.4, "label": "Russia invades Ukraine — steel & energy spike"},
    {"year": 2022, "q": 2, "index": 132.1, "label": "RBA rate hikes begin — subcontractor capacity crisis"},
    {"year": 2022, "q": 3, "index": 138.7, "label": "Construction insolvencies surge"},
    {"year": 2022, "q": 4, "index": 143.2, "label": None},
    {"year": 2023, "q": 1, "index": 146.5, "label": "Labour shortage persists — trades booked 12+ months"},
    {"year": 2023, "q": 2, "index": 148.9, "label": None},
    {"year": 2023, "q": 3, "index": 151.2, "label": None},
    {"year": 2023, "q": 4, "index": 153.0, "label": "Cost growth decelerating — but level remains elevated"},
    {"year": 2024, "q": 1, "index": 154.8, "label": None},
    {"year": 2024, "q": 2, "index": 156.1, "label": None},
    {"year": 2024, "q": 3, "index": 157.0, "label": None},
    {"year": 2024, "q": 4, "index": 157.9, "label": "57.9% above 2019 baseline"},
    {"year": 2025, "q": 1, "index": 158.5, "label": None},
]

# ── Global events timeline (for annotation) ──────────────────────────────────
GLOBAL_EVENTS = [
    {
        "date": "Mar 2020",
        "year_frac": 2020.17,
        "event": "COVID-19 Global Pandemic",
        "impact": "Construction sites shut across Australia. Import supply chains disrupted. "
                  "Cost pressures initially muted — then exploded as demand rebounded.",
        "cost_impact": "+0.4% in 2020, followed by +18% over 2021",
        "icon": "🦠",
        "color": "#e74c3c",
    },
    {
        "date": "Jun 2020",
        "year_frac": 2020.42,
        "event": "HomeBuilder Scheme Launched",
        "impact": "Government stimulus offering $25,000 grants for new homes. Created an immediate "
                  "demand surge — builders booked out 12–18 months. Trades prices rose sharply "
                  "as capacity was overwhelmed.",
        "cost_impact": "Added estimated $15,000–$25,000 to average build cost due to trades premium",
        "icon": "🏠",
        "color": "#f39c12",
    },
    {
        "date": "Jan 2021",
        "year_frac": 2021.0,
        "event": "Global Timber Crisis",
        "impact": "Framing lumber prices rose 130% globally in 12 months. North American sawmill "
                  "shutdowns during COVID combined with surging US housing demand created a worldwide "
                  "shortage. Australian timber prices followed with a 3–6 month lag.",
        "cost_impact": "Framing and structural timber: +40–60% vs 2019",
        "icon": "🪵",
        "color": "#8e5e3a",
    },
    {
        "date": "Mar 2021",
        "year_frac": 2021.21,
        "event": "Suez Canal Blockage",
        "impact": "Ever Given grounded for 6 days — halted $9.6B/day in global trade. Compounded "
                  "an already strained shipping container shortage. Lead times for imported fixtures, "
                  "fittings, electrical components, and steel products blew out to 6–12 months.",
        "cost_impact": "Imported materials: +15–25% freight premiums through to mid-2022",
        "icon": "🚢",
        "color": "#3498db",
    },
    {
        "date": "Feb 2022",
        "year_frac": 2022.12,
        "event": "Russia Invades Ukraine",
        "impact": "Russia and Ukraine supply ~30% of global steel and significant shares of nickel, "
                  "aluminium, and neon gas (used in semiconductor production). Energy prices spiked "
                  "across Europe and fed through to Australian LNG prices.",
        "cost_impact": "Structural steel: +22–30%. Reinforcing bar: +35%. Energy-intensive "
                       "materials (aluminium, glass, concrete): +15–20%",
        "icon": "⚔️",
        "color": "#c0392b",
    },
    {
        "date": "May 2022",
        "year_frac": 2022.37,
        "event": "RBA Begins Rate Hikes",
        "impact": "Cash rate rose from 0.1% to 4.35% in 13 months. Builder financing costs rose "
                  "sharply. Fixed-price contracts signed in 2021 became loss-making as costs rose. "
                  "Triggered wave of builder insolvencies — 2,309 construction company collapses "
                  "in 2022–23 alone.",
        "cost_impact": "Financing costs: +200–300bps. Developer margin compression wiped viability "
                       "on many HAFF and affordable housing projects signed at 2021 costs.",
        "icon": "📈",
        "color": "#9b59b6",
    },
    {
        "date": "2022–2023",
        "year_frac": 2022.75,
        "event": "Labour Shortage Crisis",
        "impact": "Closure of international borders during COVID eliminated 45,000 working holiday "
                  "visa workers from the construction labour pool. Trades were booked 12–18 months "
                  "in advance. Wages rose 15–25% for carpenters, electricians, and plumbers.",
        "cost_impact": "Labour cost per dwelling: up 20–30% vs 2019 baseline",
        "icon": "👷",
        "color": "#1abc9c",
    },
    {
        "date": "2023–2025",
        "year_frac": 2023.5,
        "event": "Elevated Plateau",
        "impact": "Cost growth has slowed but costs remain 55–60% above 2019. The structural "
                  "factors (labour shortages, tight trades capacity, elevated materials) have not "
                  "unwound. The industry is operating at a permanently higher cost base.",
        "cost_impact": "Current build cost: $3,800–$5,500/m² for social housing — "
                       "vs $2,200–$3,100/m² in 2019",
        "icon": "📊",
        "color": "#7f8c8d",
    },
]

# ── What a dwelling costs now vs 2019 ────────────────────────────────────────
COST_PER_DWELLING = {
    "2019": {
        "social_apartment_sqm":  2_300,
        "social_townhouse_sqm":  2_100,
        "social_detached_sqm":   1_850,
        "avg_social_total":      310_000,
        "avg_market_total":      490_000,
        "note": "Pre-COVID baseline. Fixed-price contracts routinely delivered "
                "within 5–8% of estimate.",
    },
    "2025": {
        "social_apartment_sqm":  4_200,
        "social_townhouse_sqm":  3_900,
        "social_detached_sqm":   3_400,
        "avg_social_total":      560_000,
        "avg_market_total":      820_000,
        "note": "Current market. Fixed-price contracts require 15–20% contingency. "
                "Many CHPs report HAFF funding gaps of $80,000–$150,000 per dwelling "
                "due to the difference between approved grant and actual build cost.",
    },
}

# Government funded at 2023 prices — how many homes $1B buys
BILLION_DOLLAR_YIELD = {
    2019: round(1_000_000_000 / 310_000),
    2025: round(1_000_000_000 / 560_000),
}

# ── Social housing stock condition ────────────────────────────────────────────
# Sources: AIHW Housing Assistance 2023, UNSW City Futures 2023, state audits
STOCK_CONDITION = {
    "national_social_dwellings": 430_000,
    "avg_age_years": 38,
    "pct_built_before_1980": 42,
    "pct_requiring_major_repair": 14,
    "pct_requiring_urgent_repair": 4,
    "estimated_maintenance_backlog_bn": 26.5,
    "annual_maintenance_spend_bn": 1.2,
    "years_to_clear_backlog_at_current_rate": 22,
    "annual_demolition_rate": 1_200,
    "annual_replacement_rate": 900,
    "net_stock_loss_per_year": 300,
    "source": "UNSW City Futures (2023), AIHW Housing Assistance in Australia (2023)",
}

# ── State-level condition data ────────────────────────────────────────────────
STATE_CONDITION = {
    "NSW": {
        "dwellings": 125_000,
        "backlog_m": 7_200,
        "program": "LAHC Asset Management Strategy — $812M over 4 years announced 2023. "
                   "NSW Auditor-General (2020) found 22% of stock in poor or very poor condition.",
        "avg_age": 41,
        "flagship_renewal": "Communities Plus — replacing 33 high-rise estates with mixed-tenure "
                            "development. Redfern, Waterloo, Macquarie Park. Timelines slipped 3–5 years.",
    },
    "VIC": {
        "dwellings": 85_000,
        "backlog_m": 5_100,
        "program": "Big Housing Build — $5.3B program (2020). 12,000 new homes, 9,300 refurbishments. "
                   "On track for new builds; maintenance backlog in legacy stock remains.",
        "avg_age": 36,
        "flagship_renewal": "Flemington Estate, Carlton, North Richmond — high-rise renewal. "
                            "Some relocations delayed due to construction cost escalation.",
    },
    "QLD": {
        "dwellings": 75_000,
        "backlog_m": 4_400,
        "program": "Queensland Housing Investment Growth Initiative — $1.1B (2022). Mix of new builds "
                   "and maintenance. Remote Queensland stock in critically poor condition.",
        "avg_age": 33,
        "flagship_renewal": "Logan and Woodridge precinct renewal. Olympic legacy housing commitments "
                            "post-Brisbane 2032 announcement.",
    },
    "WA": {
        "dwellings": 40_000,
        "backlog_m": 2_100,
        "program": "Housing and Homelessness Investment Package — $2.4B (2021–25). New builds "
                   "prioritised over maintenance due to trades shortage.",
        "avg_age": 35,
        "flagship_renewal": "Remote Aboriginal community housing — critically underfunded. "
                            "Average of 7 people per dwelling in some remote WA communities.",
    },
    "SA": {
        "dwellings": 37_000,
        "backlog_m": 1_900,
        "program": "South Australian Housing Trust Capital Program — $400M over 4 years. "
                   "SAHT stock ageing rapidly; significant share of walk-up flats "
                   "unsuitable for families and accessible tenants.",
        "avg_age": 44,
        "flagship_renewal": "Woodville West, Angle Park, Bowden — inner-ring estate renewal "
                            "tied to Renewal SA mixed-use precincts.",
    },
}

# ── Government responses ──────────────────────────────────────────────────────
GOVERNMENT_RESPONSES = [
    {
        "program":  "Social Housing Accelerator",
        "year":     2023,
        "amount_m": 2_000,
        "type":     "New construction grants to states",
        "homes":    10_000,
        "notes":    "Direct federal grants to state housing authorities. No requirement for "
                    "community housing provider involvement. Faster delivery than HAFF but "
                    "bypasses the sector.",
        "status":   "Underway",
        "color":    "#27ae60",
    },
    {
        "program":  "HAFF — Social Housing Component",
        "year":     2023,
        "amount_m": 4_000,
        "type":     "Grant funding via Housing Australia",
        "homes":    20_000,
        "notes":    "Delivered through CHPs — the sector's primary new-build pipeline. "
                    "Cost escalation has created funding gaps on many approved projects.",
        "status":   "Rounds 1–3 underway",
        "color":    "#f6c90e",
    },
    {
        "program":  "National Housing Infrastructure Facility",
        "year":     2018,
        "amount_m": 3_000,
        "type":     "Concessional loans for infrastructure",
        "homes":    None,
        "notes":    "Finances enabling infrastructure (roads, water, sewerage) for housing "
                    "developments. Expanded in 2023 to include direct financing for CHPs.",
        "status":   "Ongoing",
        "color":    "#3498db",
    },
    {
        "program":  "Homes for Australians — Energy Efficiency",
        "year":     2024,
        "amount_m": 300,
        "type":     "Retrofit grants",
        "homes":    None,
        "notes":    "Grants to improve energy efficiency in social housing. Reduces tenant "
                    "energy costs and improves stock condition — but not a substitute "
                    "for structural maintenance.",
        "status":   "Announced",
        "color":    "#1abc9c",
    },
    {
        "program":  "State Maintenance Budgets (combined)",
        "year":     2024,
        "amount_m": 1_200,
        "type":     "Ongoing state maintenance",
        "homes":    None,
        "notes":    "Combined annual state housing authority maintenance spend. Against a "
                    "$26.5B backlog, this represents under 5% per year — meaning the "
                    "backlog grows faster than it is cleared.",
        "status":   "Ongoing — inadequate",
        "color":    "#e74c3c",
    },
]


def get_cost_impact_summary():
    """Returns key headline numbers for the cost impact section."""
    idx_2019 = 100.0
    idx_now = COST_INDEX[-1]["index"]
    pct_rise = round(idx_now - idx_2019, 1)

    homes_per_bn_2019 = BILLION_DOLLAR_YIELD[2019]
    homes_per_bn_2025 = BILLION_DOLLAR_YIELD[2025]
    homes_lost_per_bn = homes_per_bn_2019 - homes_per_bn_2025

    return {
        "cost_rise_pct":        pct_rise,
        "avg_cost_2019":        COST_PER_DWELLING["2019"]["avg_social_total"],
        "avg_cost_2025":        COST_PER_DWELLING["2025"]["avg_social_total"],
        "cost_increase_abs":    COST_PER_DWELLING["2025"]["avg_social_total"] - COST_PER_DWELLING["2019"]["avg_social_total"],
        "homes_per_bn_2019":    homes_per_bn_2019,
        "homes_per_bn_2025":    homes_per_bn_2025,
        "homes_lost_per_bn":    homes_lost_per_bn,
        "maintenance_backlog_bn": STOCK_CONDITION["estimated_maintenance_backlog_bn"],
        "pct_stock_major_repair": STOCK_CONDITION["pct_requiring_major_repair"],
    }
