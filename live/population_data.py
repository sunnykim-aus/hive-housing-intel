"""
ABS Population Projections & Housing Demand data.
Sources:
  - ABS Cat. 3222.0 — Population Projections, Australia 2022–2071 (Series B)
  - ABS Cat. 3101.0 — Australian Demographic Statistics (historical, to Sep 2024)
  - ABS Cat. 3412.0 — Migration, Australia (Net Overseas Migration series)
  - ABS Cat. 6416.0 — Residential Property Price Indexes
  - SQM Research — National Residential Vacancy Rate series
  - CoreLogic Rental Review 2024
"""

# ── Historical national population (ABS 3101.0, annual, June year) ───────────
# natural_increase and nim are in millions (annual)
HISTORICAL_NATIONAL = [
    {"year": 2015, "population_m": 23.78, "nim": 0.183, "natural_increase": 0.155, "total_growth": 0.338},
    {"year": 2016, "population_m": 24.13, "nim": 0.183, "natural_increase": 0.152, "total_growth": 0.350},
    {"year": 2017, "population_m": 24.51, "nim": 0.231, "natural_increase": 0.149, "total_growth": 0.382},
    {"year": 2018, "population_m": 24.90, "nim": 0.240, "natural_increase": 0.149, "total_growth": 0.389},
    {"year": 2019, "population_m": 25.36, "nim": 0.239, "natural_increase": 0.148, "total_growth": 0.389},
    {"year": 2020, "population_m": 25.50, "nim": 0.194, "natural_increase": 0.147, "total_growth": 0.143},
    {"year": 2021, "population_m": 25.51, "nim": -0.084, "natural_increase": 0.143, "total_growth": 0.010},
    {"year": 2022, "population_m": 25.98, "nim": 0.170, "natural_increase": 0.148, "total_growth": 0.471},
    {"year": 2023, "population_m": 26.84, "nim": 0.518, "natural_increase": 0.150, "total_growth": 0.863},
    {"year": 2024, "population_m": 27.22, "nim": 0.395, "natural_increase": 0.151, "total_growth": 0.376},
]

# ── Historical state populations (ABS 3101.0, June year, millions) ────────────
HISTORICAL_STATE_POP = {
    "NSW": [
        {"year": 2015, "pop_m": 7.62}, {"year": 2016, "pop_m": 7.75},
        {"year": 2017, "pop_m": 7.89}, {"year": 2018, "pop_m": 8.03},
        {"year": 2019, "pop_m": 8.11}, {"year": 2020, "pop_m": 8.17},
        {"year": 2021, "pop_m": 8.18}, {"year": 2022, "pop_m": 8.20},
        {"year": 2023, "pop_m": 8.32}, {"year": 2024, "pop_m": 8.45},
    ],
    "VIC": [
        {"year": 2015, "pop_m": 5.94}, {"year": 2016, "pop_m": 6.07},
        {"year": 2017, "pop_m": 6.23}, {"year": 2018, "pop_m": 6.43},
        {"year": 2019, "pop_m": 6.63}, {"year": 2020, "pop_m": 6.65},
        {"year": 2021, "pop_m": 6.50}, {"year": 2022, "pop_m": 6.66},
        {"year": 2023, "pop_m": 6.91}, {"year": 2024, "pop_m": 7.10},
    ],
    "QLD": [
        {"year": 2015, "pop_m": 4.74}, {"year": 2016, "pop_m": 4.83},
        {"year": 2017, "pop_m": 4.93}, {"year": 2018, "pop_m": 5.01},
        {"year": 2019, "pop_m": 5.10}, {"year": 2020, "pop_m": 5.19},
        {"year": 2021, "pop_m": 5.26}, {"year": 2022, "pop_m": 5.46},
        {"year": 2023, "pop_m": 5.64}, {"year": 2024, "pop_m": 5.80},
    ],
    "WA": [
        {"year": 2015, "pop_m": 2.59}, {"year": 2016, "pop_m": 2.61},
        {"year": 2017, "pop_m": 2.62}, {"year": 2018, "pop_m": 2.62},
        {"year": 2019, "pop_m": 2.63}, {"year": 2020, "pop_m": 2.67},
        {"year": 2021, "pop_m": 2.71}, {"year": 2022, "pop_m": 2.81},
        {"year": 2023, "pop_m": 2.96}, {"year": 2024, "pop_m": 3.08},
    ],
    "SA": [
        {"year": 2015, "pop_m": 1.70}, {"year": 2016, "pop_m": 1.71},
        {"year": 2017, "pop_m": 1.72}, {"year": 2018, "pop_m": 1.74},
        {"year": 2019, "pop_m": 1.75}, {"year": 2020, "pop_m": 1.77},
        {"year": 2021, "pop_m": 1.78}, {"year": 2022, "pop_m": 1.81},
        {"year": 2023, "pop_m": 1.85}, {"year": 2024, "pop_m": 1.90},
    ],
}

# ── Net Overseas Migration — detailed breakdown by visa class (annual, '000s) ─
# Source: ABS 3412.0 and Department of Home Affairs migration program reports
HISTORICAL_NOM_DETAIL = [
    {
        "year": 2015,
        "total_k":    183,
        "skilled_k":  85,
        "family_k":   47,
        "student_k":  28,
        "other_k":    23,
        "context": "Pre-COVID steady state. Skilled and family streams dominating. "
                   "International student enrolments growing strongly.",
    },
    {
        "year": 2016,
        "total_k":    183,
        "skilled_k":  86,
        "family_k":   47,
        "student_k":  29,
        "other_k":    21,
        "context": "Stable migration year. 457 visa (temporary skills) contributing "
                   "significantly. Strong Asian student demand in Melbourne and Sydney.",
    },
    {
        "year": 2017,
        "total_k":    231,
        "skilled_k":  98,
        "family_k":   50,
        "student_k":  54,
        "other_k":    29,
        "context": "Surge in international students — particularly from China and India. "
                   "Student NOM often underestimated as students cycle in and out.",
    },
    {
        "year": 2018,
        "total_k":    240,
        "skilled_k":  100,
        "family_k":   52,
        "student_k":  56,
        "other_k":    32,
        "context": "Peak pre-COVID NOM. Federal government debates reducing migration "
                   "cap. Infrastructure strain becoming politically salient in Sydney and Melbourne.",
    },
    {
        "year": 2019,
        "total_k":    239,
        "skilled_k":  99,
        "family_k":   51,
        "student_k":  57,
        "other_k":    32,
        "context": "Last full pre-COVID year. Migration at near-record levels. "
                   "Housing markets tight. Rental vacancy in Sydney and Melbourne below 2%.",
    },
    {
        "year": 2020,
        "total_k":    194,
        "skilled_k":  72,
        "family_k":   45,
        "student_k":  42,
        "other_k":    35,
        "context": "COVID begins (March). International borders close from March 2020. "
                   "NOM drops but does not collapse — temporary visa holders returning home "
                   "partially offset by reduced outflows. Borders fully closed by June.",
    },
    {
        "year": 2021,
        "total_k":    -84,
        "skilled_k":  -18,
        "family_k":   10,
        "student_k":  -62,
        "other_k":    -14,
        "context": "Borders remain closed for the full year. Net OUTFLOW — more people "
                   "left Australia than arrived. Student visa holders departed in large numbers. "
                   "Temporary visa holders with no income left. Working holiday visa workers "
                   "departed — devastating for rural housing markets.",
    },
    {
        "year": 2022,
        "total_k":    170,
        "skilled_k":  70,
        "family_k":   42,
        "student_k":  38,
        "other_k":    20,
        "context": "Borders reopen July 2021 (partial) → November 2021 (international students) "
                   "→ February 2022 (all visitors). Pent-up demand begins. Skilled migration "
                   "fast-tracked. Ukraine humanitarian stream adds ~5,000.",
    },
    {
        "year": 2023,
        "total_k":    518,
        "skilled_k":  188,
        "family_k":   72,
        "student_k":  189,
        "other_k":    69,
        "context": "RECORD annual NOM — more than double the pre-COVID average. "
                   "International students returned en masse. Skilled migration surge to fill "
                   "post-COVID labour gaps. Afghan humanitarian program added ~15,000. "
                   "Rental markets collapsed: Sydney, Melbourne, Brisbane vacancy below 1%.",
    },
    {
        "year": 2024,
        "total_k":    395,
        "skilled_k":  155,
        "family_k":   68,
        "student_k":  128,
        "other_k":    44,
        "context": "Government targets reduction — student visa processing tightened, "
                   "university enrolment caps proposed. NOM falling but still far above "
                   "pre-COVID norm. Housing pressure remains acute in all capital cities.",
    },
]

# ── Migration phases — narrative framing ──────────────────────────────────────
MIGRATION_PHASES = [
    {
        "label":      "Pre-COVID steady state",
        "years":      "2015–2019",
        "avg_nim_k":  215,
        "color":      "#3498db",
        "narrative":  "Australia's NOM averaged 215,000 per year — high by historical standards "
                      "but absorbed into an economy and housing market growing in parallel. "
                      "Inner-city rental markets were tight but the system was in equilibrium.",
        "housing":    "Vacancy rates 2–3%. Rents rising moderately at CPI+2%. Social housing "
                      "waitlists growing slowly. Construction running at ~200,000/yr.",
    },
    {
        "label":      "COVID collapse",
        "years":      "2020–2021",
        "avg_nim_k":  55,
        "color":      "#e74c3c",
        "narrative":  "International borders slammed shut in March 2020. NOM crashed from "
                      "+239,000 to −84,000 over two years — a swing of 323,000 people. "
                      "Temporary visa holders left. International students departed. "
                      "Working holiday visa workers — a critical part of the rural rental market "
                      "— returned home en masse.",
        "housing":    "Paradoxically, some capital city vacancy rates rose as students and workers "
                      "departed (Melbourne CBD briefly hit 8% vacancy). Regional and coastal markets "
                      "boomed as Australians relocated with remote work. HomeBuilder inflated demand "
                      "for new construction while supply chains collapsed.",
    },
    {
        "label":      "Reopening surge",
        "years":      "2022–2023",
        "avg_nim_k":  344,
        "color":      "#f39c12",
        "narrative":  "Borders reopened in stages from mid-2021. By 2023, NOM hit a record "
                      "518,000 — more than double the pre-COVID average. Three factors compounded: "
                      "pent-up student demand (two years of deferred entry), accelerated skilled "
                      "migration to fill post-COVID labour shortages, and humanitarian programs "
                      "(Ukraine, Afghanistan). The housing system — already stressed by HomeBuilder, "
                      "construction cost blowouts, and record-low rental vacancy — absorbed "
                      "this surge without any matching supply increase.",
        "housing":    "National rental vacancy hit 1.0% in 2023 — the lowest since records began. "
                      "Perth vacancy: 0.4%. Brisbane: 0.7%. Median rents rose 10–15% in a single "
                      "year. Social housing waitlists spiked. SHS demand surged 18%. "
                      "Real wages went negative as rents outpaced income growth.",
    },
    {
        "label":      "Managed moderation",
        "years":      "2024–2025",
        "avg_nim_k":  340,
        "color":      "#27ae60",
        "narrative":  "Government has tightened student visa processing and proposed university "
                      "enrolment caps. NOM is declining but remains above the pre-COVID average. "
                      "The structural imbalance — population growing faster than housing supply — "
                      "has not resolved. It has moderated.",
        "housing":    "Vacancy recovering slowly toward 1.5–2.0%. Rent growth slowing but from "
                      "a 35% higher base than 2019. Social housing waitlists remain at "
                      "record levels. No state has added net social housing stock "
                      "in the past three years.",
    },
]

# ── Housing market impact (vacancy and rent, 2015–2024) ──────────────────────
# SQM Research vacancy data + CoreLogic median rent index
HOUSING_MARKET_HISTORY = [
    {"year": 2015, "national_vacancy_pct": 2.8, "rent_index": 100, "nim_k": 183},
    {"year": 2016, "national_vacancy_pct": 2.6, "rent_index": 102, "nim_k": 183},
    {"year": 2017, "national_vacancy_pct": 2.4, "rent_index": 105, "nim_k": 231},
    {"year": 2018, "national_vacancy_pct": 2.3, "rent_index": 108, "nim_k": 240},
    {"year": 2019, "national_vacancy_pct": 2.1, "rent_index": 110, "nim_k": 239},
    {"year": 2020, "national_vacancy_pct": 2.5, "rent_index": 109, "nim_k": 194},
    {"year": 2021, "national_vacancy_pct": 1.8, "rent_index": 112, "nim_k": -84},
    {"year": 2022, "national_vacancy_pct": 1.2, "rent_index": 122, "nim_k": 170},
    {"year": 2023, "national_vacancy_pct": 1.0, "rent_index": 140, "nim_k": 518},
    {"year": 2024, "national_vacancy_pct": 1.3, "rent_index": 148, "nim_k": 395},
]

# State vacancy rates (SQM Research, annual average)
STATE_VACANCY_HISTORY = {
    "NSW": [2.6, 2.5, 2.3, 2.1, 2.0, 2.8, 1.8, 1.1, 0.9, 1.1],
    "VIC": [2.7, 2.6, 2.3, 2.0, 1.9, 3.6, 2.9, 1.4, 1.1, 1.3],
    "QLD": [3.2, 3.0, 2.7, 2.4, 2.2, 1.9, 1.2, 0.9, 0.7, 0.9],
    "WA":  [4.8, 5.0, 4.2, 3.1, 2.4, 1.5, 0.9, 0.6, 0.4, 0.6],
    "SA":  [2.4, 2.3, 2.0, 1.7, 1.5, 1.2, 0.8, 0.6, 0.5, 0.7],
    "years": [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
}

# ── National population projections (Series B) ───────────────────────────────
# Year → projected national population (millions)
NATIONAL_PROJECTIONS = [
    {"year": 2024, "population_m": 26.8, "natural_increase": 0.15, "nim": 0.28},
    {"year": 2025, "population_m": 27.2, "natural_increase": 0.15, "nim": 0.25},
    {"year": 2026, "population_m": 27.6, "natural_increase": 0.15, "nim": 0.24},
    {"year": 2027, "population_m": 28.0, "natural_increase": 0.15, "nim": 0.23},
    {"year": 2028, "population_m": 28.4, "natural_increase": 0.15, "nim": 0.22},
    {"year": 2029, "population_m": 28.7, "natural_increase": 0.15, "nim": 0.21},
    {"year": 2030, "population_m": 29.1, "natural_increase": 0.15, "nim": 0.20},
    {"year": 2031, "population_m": 29.4, "natural_increase": 0.15, "nim": 0.20},
    {"year": 2032, "population_m": 29.8, "natural_increase": 0.14, "nim": 0.19},
    {"year": 2033, "population_m": 30.1, "natural_increase": 0.14, "nim": 0.19},
    {"year": 2034, "population_m": 30.4, "natural_increase": 0.14, "nim": 0.18},
    {"year": 2035, "population_m": 30.7, "natural_increase": 0.14, "nim": 0.18},
    {"year": 2036, "population_m": 31.1, "natural_increase": 0.13, "nim": 0.17},
    {"year": 2037, "population_m": 31.4, "natural_increase": 0.13, "nim": 0.17},
    {"year": 2038, "population_m": 31.7, "natural_increase": 0.13, "nim": 0.16},
    {"year": 2039, "population_m": 32.0, "natural_increase": 0.13, "nim": 0.16},
    {"year": 2040, "population_m": 32.3, "natural_increase": 0.12, "nim": 0.15},
    {"year": 2041, "population_m": 32.5, "natural_increase": 0.12, "nim": 0.15},
    {"year": 2042, "population_m": 32.8, "natural_increase": 0.12, "nim": 0.14},
    {"year": 2043, "population_m": 33.1, "natural_increase": 0.12, "nim": 0.14},
    {"year": 2044, "population_m": 33.4, "natural_increase": 0.11, "nim": 0.13},
]

# Average household size (persons per dwelling) — ABS Census 2021, projected decline
HOUSEHOLD_SIZE_BY_YEAR = {
    2024: 2.53, 2026: 2.52, 2028: 2.51, 2030: 2.50,
    2032: 2.49, 2034: 2.48, 2036: 2.47, 2038: 2.46,
    2040: 2.45, 2042: 2.44, 2044: 2.43,
}

# Current dwelling stock (2024 estimate, millions)
CURRENT_DWELLING_STOCK_M = 11.2

# Current annual approvals run rate (ABS, 12-month to Mar 2025)
CURRENT_ANNUAL_APPROVALS = 163_000

# National Accord target
ACCORD_TARGET = 240_000

# ── State-level projections ───────────────────────────────────────────────────
# ABS Series B state projections to 2041
# Source: ABS 3222.0 Table 1 — medium-growth scenario
STATE_PROJECTIONS = {
    "NSW": {
        "current_pop_m":   8.35,
        "proj_2031_m":     9.20,
        "proj_2041_m":     10.05,
        "growth_drivers":  "Strong net overseas migration, internal migration from VIC/QLD, "
                           "concentrated in Greater Sydney and Hunter Region.",
        "implied_new_dwellings_2041": 340_000,
        "social_housing_pct":  4.2,
        "current_approvals":   35_500,
        "required_to_meet_demand": 53_000,
        "color": "#3498db",
    },
    "VIC": {
        "current_pop_m":   7.05,
        "proj_2031_m":     7.85,
        "proj_2041_m":     8.60,
        "growth_drivers":  "Highest internal migration gain nationally, strong NOM recovery post-COVID. "
                           "Growth concentrated in Melbourne outer suburbs and Geelong.",
        "implied_new_dwellings_2041": 300_000,
        "social_housing_pct":  3.4,
        "current_approvals":   45_200,
        "required_to_meet_demand": 52_000,
        "color": "#e74c3c",
    },
    "QLD": {
        "current_pop_m":   5.72,
        "proj_2031_m":     6.45,
        "proj_2041_m":     7.20,
        "growth_drivers":  "Fastest-growing state by net internal migration. South East Queensland "
                           "absorbed 50,000+ interstate arrivals per year post-2020. Brisbane Olympics pipeline.",
        "implied_new_dwellings_2041": 255_000,
        "social_housing_pct":  3.8,
        "current_approvals":   31_000,
        "required_to_meet_demand": 44_000,
        "color": "#f39c12",
    },
    "WA": {
        "current_pop_m":   3.02,
        "proj_2031_m":     3.42,
        "proj_2041_m":     3.82,
        "growth_drivers":  "Resources sector driving NOM and skilled migration. Perth land release "
                           "constraints limiting outer-suburban supply. Rental vacancy below 1%.",
        "implied_new_dwellings_2041": 120_000,
        "social_housing_pct":  4.6,
        "current_approvals":   14_200,
        "required_to_meet_demand": 22_000,
        "color": "#27ae60",
    },
    "SA": {
        "current_pop_m":   1.86,
        "proj_2031_m":     2.00,
        "proj_2041_m":     2.12,
        "growth_drivers":  "Lower growth than eastern states. Defence and energy sector investment "
                           "driving skilled migration. Adelaide affordable by comparison.",
        "implied_new_dwellings_2041": 55_000,
        "social_housing_pct":  6.1,
        "current_approvals":   7_200,
        "required_to_meet_demand": 11_000,
        "color": "#9b59b6",
    },
}

# ── Why population is growing — breakdown ────────────────────────────────────
GROWTH_DRIVERS = {
    "Net Overseas Migration (NOM)":  {
        "share_pct": 65,
        "detail": "International students, skilled migrants, humanitarian entrants, and working holiday "
                  "makers. NOM averaged 400,000 per year in 2022–23, well above the pre-COVID average "
                  "of 240,000. Government is targeting a gradual return to ~260,000 by 2025–26.",
        "housing_impact": "New arrivals concentrate in major cities (Sydney, Melbourne, Brisbane) and "
                          "compete directly with existing renters. Average time to find housing for a "
                          "new arrival: 3–6 months in current market.",
        "color": "#e74c3c",
    },
    "Natural Increase": {
        "share_pct": 25,
        "detail": "Births minus deaths. Total fertility rate has declined to 1.63 per woman (2023), "
                  "below replacement level, but population momentum from a large working-age cohort "
                  "maintains positive natural increase for the next 20 years.",
        "housing_impact": "Family formation drives demand for 3+ bedroom homes. Household size is "
                          "shrinking as people live longer alone and family sizes reduce — meaning "
                          "each additional person requires a greater dwelling stock increase.",
        "color": "#3498db",
    },
    "Net Interstate Migration": {
        "share_pct": 10,
        "detail": "People moving between states — primarily from NSW/VIC to QLD/WA for affordability "
                  "and lifestyle. Post-COVID remote work enabled a structural shift that is "
                  "expected to persist.",
        "housing_impact": "Puts acute pressure on QLD and WA markets where supply pipelines were "
                          "not built for rapid population gain. Drove rental increases of 20–30% "
                          "in Brisbane and Perth in 2022–23.",
        "color": "#27ae60",
    },
}

# ── Policy advocacy positions ─────────────────────────────────────────────────
POLICY_ADVOCACY = [
    {
        "category": "Increase the National Housing Accord target",
        "position":  "The current 1.2M/5-year target (240,000/yr) is based on 2022 population assumptions. "
                     "With NOM running at 400,000+ per year, the required build rate is closer to "
                     "300,000–320,000 per year. The Accord target should be revised upward.",
        "evidence":  "ABS 3222.0 Series B projects 7.3M additional people to 2041 — requiring "
                     "approximately 3.0M additional dwellings at current household size. Current "
                     "trajectory delivers approximately 1.9M. The gap is structural.",
        "icon": "📈",
    },
    {
        "category": "Mandate inclusionary zoning at 15% minimum",
        "position":  "All new greenfield and medium-density developments above 50 dwellings should "
                     "include a minimum 15% social/affordable component as a condition of planning "
                     "approval. NSW, VIC, and QLD have all piloted versions of this — national "
                     "coordination through the NHAS would drive consistency.",
        "evidence":  "AHURI research (2022) found that inclusionary zoning of 10–15% would add "
                     "12,000–18,000 affordable dwellings annually at zero net public cost when "
                     "combined with density bonuses.",
        "icon": "🏗️",
    },
    {
        "category": "Accelerate Build-to-Rent for affordable tiers",
        "position":  "The managed investment trust (MIT) withholding tax concession for Build-to-Rent "
                     "should be extended to include a mandatory 20% affordable tier (at 75% of market "
                     "rent). Without an affordable requirement, BTR serves market renters, not the "
                     "people on the waitlist.",
        "evidence":  "The government's 2023 BTR tax changes were welcomed but AHURI modelling shows "
                     "they will add fewer than 5,000 dwellings at below-market rents over 10 years "
                     "without an affordability mandate.",
        "icon": "🏢",
    },
    {
        "category": "Fast-track planning reform for social housing",
        "position":  "State planning approvals for community housing provider developments should be "
                     "treated as State Significant Development with a 60-day determination target. "
                     "Current approval timelines average 18–24 months in NSW, 14–20 months in VIC — "
                     "adding $50,000–$80,000 per dwelling in holding costs.",
        "evidence":  "Power Housing Australia (2024): planning delays are the single largest "
                     "controllable cost driver in CHP development pipelines, accounting for "
                     "22% of total development costs in metropolitan areas.",
        "icon": "⚡",
    },
    {
        "category": "Establish a Social Housing Futures Fund",
        "position":  "A dedicated off-budget fund of $5B (modelled on HAFF but for existing stock "
                     "renewal) to address the $25B+ deferred maintenance backlog in social housing. "
                     "Framed as asset preservation — the cost of inaction (demolition and rebuilding) "
                     "is 4–6x the cost of proactive maintenance.",
        "evidence":  "UNSW City Futures (2023): the national social housing maintenance backlog is "
                     "estimated at $26.5B. At current state funding rates, it will take 40+ years "
                     "to clear — by which time much of the stock will be beyond repair.",
        "icon": "🔧",
    },
    {
        "category": "Tie Commonwealth Rent Assistance to housing CPI, not general CPI",
        "position":  "Commonwealth Rent Assistance has not kept pace with rental market increases. "
                     "Indexing CRA to a rental-specific CPI measure rather than the headline CPI "
                     "would prevent the effective reduction in support that has occurred since 2020.",
        "evidence":  "ACOSS (2024): the real value of CRA has fallen 20% relative to market rents "
                     "since 2019. Recipients face average rental stress of 67% — spending 2 in every "
                     "3 dollars of income on rent.",
        "icon": "💰",
    },
]


def get_national_dwelling_demand():
    """
    Returns projected annual dwelling demand implied by population growth.
    Compares against current approvals run rate and Accord target.
    """
    results = []
    prev_pop = NATIONAL_PROJECTIONS[0]["population_m"]
    prev_stock = CURRENT_DWELLING_STOCK_M

    for proj in NATIONAL_PROJECTIONS[1:]:
        year = proj["year"]
        pop = proj["population_m"]
        hh_size = HOUSEHOLD_SIZE_BY_YEAR.get(year, 2.50)

        pop_growth_m = pop - prev_pop
        implied_new_hh = (pop_growth_m * 1_000_000) / hh_size
        # Add 3% for vacancy/churn buffer
        required_dwellings = round(implied_new_hh * 1.03)

        # Cumulative stock if building at current rate
        cumulative_at_current = prev_stock + (CURRENT_ANNUAL_APPROVALS / 1_000_000)
        # Cumulative stock if building at Accord target
        cumulative_at_accord  = prev_stock + (ACCORD_TARGET / 1_000_000)

        required_stock = round((pop * 1_000_000) / hh_size * 1.03) / 1_000_000

        results.append({
            "year": year,
            "population_m": pop,
            "required_new_dwellings": required_dwellings,
            "current_run_rate": CURRENT_ANNUAL_APPROVALS,
            "accord_target": ACCORD_TARGET,
            "deficit_vs_current": required_dwellings - CURRENT_ANNUAL_APPROVALS,
            "deficit_vs_accord":  required_dwellings - ACCORD_TARGET,
        })
        prev_pop = pop
        prev_stock = cumulative_at_current

    return results
