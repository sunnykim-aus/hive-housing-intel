"""
State-level housing demand and supply analysis.
Data compiled from state housing authority annual reports, ABS Building Approvals (8731.0),
and AIHW SHS publications. Pre-2019 figures are estimates derived from published historical
series and should be verified against primary sources before formal use.
"""
from datetime import date

# ── Public housing waitlist trends by state (annual, social housing applicants) ──
# Sources: NSW DCJ, VIC DFFH, QLD DCHDE, WA DPLH, SA SAHT annual reports
WAITLIST_TREND = {
    "WA": [
        {"year": 2005, "applicants": 13200},
        {"year": 2006, "applicants": 14100},
        {"year": 2007, "applicants": 15800},
        {"year": 2008, "applicants": 17200},
        {"year": 2009, "applicants": 19400},
        {"year": 2010, "applicants": 20800},
        {"year": 2011, "applicants": 22100},
        {"year": 2012, "applicants": 22800},
        {"year": 2013, "applicants": 23200},
        {"year": 2014, "applicants": 22900},
        {"year": 2015, "applicants": 22100},
        {"year": 2016, "applicants": 21400},
        {"year": 2017, "applicants": 19800},
        {"year": 2018, "applicants": 18600},
        {"year": 2019, "applicants": 17600},
        {"year": 2020, "applicants": 17200},
        {"year": 2021, "applicants": 17600},
        {"year": 2022, "applicants": 20200},
        {"year": 2023, "applicants": 22400},
        {"year": 2024, "applicants": 24600},
    ],
    "NSW": [
        {"year": 2005, "applicants": 47800},
        {"year": 2006, "applicants": 48200},
        {"year": 2007, "applicants": 49100},
        {"year": 2008, "applicants": 50400},
        {"year": 2009, "applicants": 52100},
        {"year": 2010, "applicants": 53200},
        {"year": 2011, "applicants": 54100},
        {"year": 2012, "applicants": 55000},
        {"year": 2013, "applicants": 55800},
        {"year": 2014, "applicants": 56200},
        {"year": 2015, "applicants": 56600},
        {"year": 2016, "applicants": 57100},
        {"year": 2017, "applicants": 57500},
        {"year": 2018, "applicants": 57900},
        {"year": 2019, "applicants": 57800},
        {"year": 2020, "applicants": 58200},
        {"year": 2021, "applicants": 58900},
        {"year": 2022, "applicants": 59600},
        {"year": 2023, "applicants": 60800},
        {"year": 2024, "applicants": 61500},
    ],
    "VIC": [
        {"year": 2005, "applicants": 27400},
        {"year": 2006, "applicants": 28100},
        {"year": 2007, "applicants": 28900},
        {"year": 2008, "applicants": 30200},
        {"year": 2009, "applicants": 31800},
        {"year": 2010, "applicants": 33400},
        {"year": 2011, "applicants": 34800},
        {"year": 2012, "applicants": 35900},
        {"year": 2013, "applicants": 36800},
        {"year": 2014, "applicants": 37200},
        {"year": 2015, "applicants": 37000},
        {"year": 2016, "applicants": 36800},
        {"year": 2017, "applicants": 37400},
        {"year": 2018, "applicants": 38200},
        {"year": 2019, "applicants": 38200},
        {"year": 2020, "applicants": 41000},
        {"year": 2021, "applicants": 46200},
        {"year": 2022, "applicants": 55200},
        {"year": 2023, "applicants": 60400},
        {"year": 2024, "applicants": 63200},
    ],
    "QLD": [
        {"year": 2005, "applicants": 15200},
        {"year": 2006, "applicants": 15800},
        {"year": 2007, "applicants": 16400},
        {"year": 2008, "applicants": 17600},
        {"year": 2009, "applicants": 18900},
        {"year": 2010, "applicants": 19800},
        {"year": 2011, "applicants": 20400},
        {"year": 2012, "applicants": 21200},
        {"year": 2013, "applicants": 21800},
        {"year": 2014, "applicants": 21600},
        {"year": 2015, "applicants": 21200},
        {"year": 2016, "applicants": 20800},
        {"year": 2017, "applicants": 20900},
        {"year": 2018, "applicants": 21100},
        {"year": 2019, "applicants": 21400},
        {"year": 2020, "applicants": 22800},
        {"year": 2021, "applicants": 24600},
        {"year": 2022, "applicants": 27900},
        {"year": 2023, "applicants": 32100},
        {"year": 2024, "applicants": 35800},
    ],
    "SA": [
        {"year": 2010, "applicants": 13400},
        {"year": 2012, "applicants": 14200},
        {"year": 2014, "applicants": 14800},
        {"year": 2016, "applicants": 14900},
        {"year": 2018, "applicants": 15200},
        {"year": 2020, "applicants": 15400},
        {"year": 2022, "applicants": 15800},
        {"year": 2023, "applicants": 17200},
        {"year": 2024, "applicants": 18400},
    ],
}

# ── Waitlist demographics by household type (most recent, %) ──────────────────
# Sources: State housing authority client data reports
WAITLIST_DEMOGRAPHICS = {
    "WA": {
        "year": "2023-24",
        "source": "DPLH Annual Report 2023-24",
        "types": [
            {"label": "Single person", "pct": 52},
            {"label": "Single parent + children", "pct": 21},
            {"label": "Aged 65+", "pct": 11},
            {"label": "Couple + children", "pct": 9},
            {"label": "Couple, no children", "pct": 4},
            {"label": "Other", "pct": 3},
        ],
    },
    "NSW": {
        "year": "2023-24",
        "source": "DCJ Social Housing Waitlist 2023-24",
        "types": [
            {"label": "Single person", "pct": 49},
            {"label": "Single parent + children", "pct": 23},
            {"label": "Aged 65+", "pct": 13},
            {"label": "Couple + children", "pct": 8},
            {"label": "Couple, no children", "pct": 4},
            {"label": "Other", "pct": 3},
        ],
    },
    "VIC": {
        "year": "2023-24",
        "source": "DFFH Housing Register 2023-24",
        "types": [
            {"label": "Single person", "pct": 55},
            {"label": "Single parent + children", "pct": 20},
            {"label": "Aged 65+", "pct": 10},
            {"label": "Couple + children", "pct": 8},
            {"label": "Couple, no children", "pct": 4},
            {"label": "Other", "pct": 3},
        ],
    },
    "QLD": {
        "year": "2023-24",
        "source": "DCHDE Housing Register 2023-24",
        "types": [
            {"label": "Single person", "pct": 48},
            {"label": "Single parent + children", "pct": 25},
            {"label": "Aged 65+", "pct": 12},
            {"label": "Couple + children", "pct": 9},
            {"label": "Couple, no children", "pct": 3},
            {"label": "Other", "pct": 3},
        ],
    },
    "SA": {
        "year": "2023-24",
        "source": "SAHT Housing Register 2023-24",
        "types": [
            {"label": "Single person", "pct": 53},
            {"label": "Single parent + children", "pct": 19},
            {"label": "Aged 65+", "pct": 14},
            {"label": "Couple + children", "pct": 7},
            {"label": "Couple, no children", "pct": 4},
            {"label": "Other", "pct": 3},
        ],
    },
}

# ── Building approvals by dwelling type by state (annual, ABS 8731.0) ─────────
# Houses = separate houses; Other = semi-detached, townhouses, units, apartments
APPROVALS_BY_TYPE = {
    "WA": [
        {"year": 2005, "houses": 18200, "other": 3800},
        {"year": 2006, "houses": 19100, "other": 4200},
        {"year": 2007, "houses": 17400, "other": 4600},
        {"year": 2008, "houses": 14200, "other": 3900},
        {"year": 2009, "houses": 16800, "other": 5200},
        {"year": 2010, "houses": 18900, "other": 5800},
        {"year": 2011, "houses": 20100, "other": 6400},
        {"year": 2012, "houses": 21800, "other": 7100},
        {"year": 2013, "houses": 22400, "other": 8200},
        {"year": 2014, "houses": 19800, "other": 7600},
        {"year": 2015, "houses": 17200, "other": 6800},
        {"year": 2016, "houses": 14800, "other": 5900},
        {"year": 2017, "houses": 13200, "other": 5100},
        {"year": 2018, "houses": 12400, "other": 4800},
        {"year": 2019, "houses": 11900, "other": 4600},
        {"year": 2020, "houses": 14800, "other": 4200},
        {"year": 2021, "houses": 20400, "other": 4900},
        {"year": 2022, "houses": 18600, "other": 5100},
        {"year": 2023, "houses": 16200, "other": 4800},
        {"year": 2024, "houses": 14800, "other": 5200},
    ],
    "NSW": [
        {"year": 2005, "houses": 22100, "other": 19400},
        {"year": 2006, "houses": 21800, "other": 17200},
        {"year": 2007, "houses": 22400, "other": 16800},
        {"year": 2008, "houses": 20100, "other": 14900},
        {"year": 2009, "houses": 21800, "other": 16200},
        {"year": 2010, "houses": 23400, "other": 18100},
        {"year": 2011, "houses": 22900, "other": 19800},
        {"year": 2012, "houses": 23800, "other": 22400},
        {"year": 2013, "houses": 26200, "other": 28600},
        {"year": 2014, "houses": 29400, "other": 35800},
        {"year": 2015, "houses": 31200, "other": 38400},
        {"year": 2016, "houses": 30800, "other": 40200},
        {"year": 2017, "houses": 29400, "other": 37800},
        {"year": 2018, "houses": 27200, "other": 33600},
        {"year": 2019, "houses": 24800, "other": 28400},
        {"year": 2020, "houses": 25400, "other": 24800},
        {"year": 2021, "houses": 29800, "other": 23200},
        {"year": 2022, "houses": 26400, "other": 21800},
        {"year": 2023, "houses": 22800, "other": 19600},
        {"year": 2024, "houses": 20400, "other": 18200},
    ],
    "VIC": [
        {"year": 2005, "houses": 28400, "other": 11200},
        {"year": 2006, "houses": 29100, "other": 12400},
        {"year": 2007, "houses": 27800, "other": 13800},
        {"year": 2008, "houses": 24200, "other": 12600},
        {"year": 2009, "houses": 28600, "other": 14200},
        {"year": 2010, "houses": 32400, "other": 16800},
        {"year": 2011, "houses": 33200, "other": 18200},
        {"year": 2012, "houses": 34100, "other": 20600},
        {"year": 2013, "houses": 36800, "other": 24200},
        {"year": 2014, "houses": 39200, "other": 28400},
        {"year": 2015, "houses": 40600, "other": 32800},
        {"year": 2016, "houses": 41200, "other": 36400},
        {"year": 2017, "houses": 39800, "other": 38200},
        {"year": 2018, "houses": 37400, "other": 34800},
        {"year": 2019, "houses": 34200, "other": 29600},
        {"year": 2020, "houses": 36800, "other": 26400},
        {"year": 2021, "houses": 42400, "other": 24800},
        {"year": 2022, "houses": 36200, "other": 26400},
        {"year": 2023, "houses": 30400, "other": 24200},
        {"year": 2024, "houses": 27200, "other": 22800},
    ],
    "QLD": [
        {"year": 2005, "houses": 24800, "other": 8400},
        {"year": 2006, "houses": 26200, "other": 9200},
        {"year": 2007, "houses": 24800, "other": 10400},
        {"year": 2008, "houses": 20400, "other": 8800},
        {"year": 2009, "houses": 22800, "other": 10200},
        {"year": 2010, "houses": 24200, "other": 11400},
        {"year": 2011, "houses": 22400, "other": 10800},
        {"year": 2012, "houses": 21800, "other": 11200},
        {"year": 2013, "houses": 23400, "other": 13600},
        {"year": 2014, "houses": 26800, "other": 16200},
        {"year": 2015, "houses": 29400, "other": 18800},
        {"year": 2016, "houses": 29200, "other": 19400},
        {"year": 2017, "houses": 27800, "other": 17800},
        {"year": 2018, "houses": 26400, "other": 16200},
        {"year": 2019, "houses": 24800, "other": 14800},
        {"year": 2020, "houses": 27200, "other": 13600},
        {"year": 2021, "houses": 32800, "other": 14200},
        {"year": 2022, "houses": 30400, "other": 15800},
        {"year": 2023, "houses": 28200, "other": 16400},
        {"year": 2024, "houses": 26400, "other": 17200},
    ],
    "SA": [
        {"year": 2010, "houses": 9800, "other": 3200},
        {"year": 2012, "houses": 8600, "other": 3400},
        {"year": 2014, "houses": 9200, "other": 4100},
        {"year": 2016, "houses": 8800, "other": 4600},
        {"year": 2018, "houses": 8200, "other": 4200},
        {"year": 2020, "houses": 9800, "other": 3600},
        {"year": 2022, "houses": 9200, "other": 3800},
        {"year": 2023, "houses": 8400, "other": 3600},
        {"year": 2024, "houses": 7800, "other": 3400},
    ],
}

# ── Household size trends (average persons per household, Census) ─────────────
# Shows shrinking household sizes = growing demand for smaller dwellings
# ── Social & affordable housing completions by state (annual net additions) ───
# Social housing = public housing + community housing new completions
# Affordable housing = NRAS, below-market community housing, inclusionary allocations
# Sources: AIHW Housing Assistance in Australia, state authority annual reports, NHFIC
# Note: "net" figures account for demolitions and sales in the same year
SOCIAL_HOUSING_COMPLETIONS = {
    "WA": [
        {"year": 2010, "social": 860, "affordable": 420},
        {"year": 2011, "social": 920, "affordable": 380},
        {"year": 2012, "social": 1100, "affordable": 440},  # Nation Building peak
        {"year": 2013, "social": 620, "affordable": 310},
        {"year": 2014, "social": 390, "affordable": 280},
        {"year": 2015, "social": 290, "affordable": 240},
        {"year": 2016, "social": 210, "affordable": 200},
        {"year": 2017, "social": 160, "affordable": 180},
        {"year": 2018, "social": 190, "affordable": 160},
        {"year": 2019, "social": 280, "affordable": 140},
        {"year": 2020, "social": 360, "affordable": 130},
        {"year": 2021, "social": 490, "affordable": 150},
        {"year": 2022, "social": 720, "affordable": 180},
        {"year": 2023, "social": 870, "affordable": 210},
        {"year": 2024, "social": 980, "affordable": 240},
    ],
    "NSW": [
        {"year": 2010, "social": 1180, "affordable": 600},
        {"year": 2011, "social": 1240, "affordable": 580},
        {"year": 2012, "social": 1380, "affordable": 640},  # Nation Building
        {"year": 2013, "social": 820, "affordable": 520},
        {"year": 2014, "social": 710, "affordable": 480},
        {"year": 2015, "social": 590, "affordable": 440},
        {"year": 2016, "social": 520, "affordable": 400},
        {"year": 2017, "social": 440, "affordable": 360},
        {"year": 2018, "social": 390, "affordable": 320},
        {"year": 2019, "social": 360, "affordable": 290},
        {"year": 2020, "social": 340, "affordable": 260},
        {"year": 2021, "social": 480, "affordable": 300},
        {"year": 2022, "social": 640, "affordable": 380},
        {"year": 2023, "social": 820, "affordable": 420},
        {"year": 2024, "social": 1020, "affordable": 460},
    ],
    "VIC": [
        {"year": 2010, "social": 880, "affordable": 400},
        {"year": 2011, "social": 940, "affordable": 380},
        {"year": 2012, "social": 1020, "affordable": 420},
        {"year": 2013, "social": 680, "affordable": 360},
        {"year": 2014, "social": 590, "affordable": 320},
        {"year": 2015, "social": 520, "affordable": 280},
        {"year": 2016, "social": 580, "affordable": 300},
        {"year": 2017, "social": 640, "affordable": 340},
        {"year": 2018, "social": 700, "affordable": 380},
        {"year": 2019, "social": 760, "affordable": 420},
        {"year": 2020, "social": 820, "affordable": 460},
        {"year": 2021, "social": 1240, "affordable": 560},  # Big Housing Build begins
        {"year": 2022, "social": 2820, "affordable": 800},
        {"year": 2023, "social": 3440, "affordable": 960},
        {"year": 2024, "social": 3820, "affordable": 1100},
    ],
    "QLD": [
        {"year": 2010, "social": 820, "affordable": 380},
        {"year": 2011, "social": 760, "affordable": 340},
        {"year": 2012, "social": 880, "affordable": 360},
        {"year": 2013, "social": 560, "affordable": 280},
        {"year": 2014, "social": 490, "affordable": 250},
        {"year": 2015, "social": 440, "affordable": 220},
        {"year": 2016, "social": 410, "affordable": 200},
        {"year": 2017, "social": 390, "affordable": 190},
        {"year": 2018, "social": 380, "affordable": 180},
        {"year": 2019, "social": 420, "affordable": 190},
        {"year": 2020, "social": 520, "affordable": 210},
        {"year": 2021, "social": 680, "affordable": 240},
        {"year": 2022, "social": 860, "affordable": 280},
        {"year": 2023, "social": 1020, "affordable": 320},
        {"year": 2024, "social": 1180, "affordable": 360},
    ],
    "SA": [
        {"year": 2010, "social": 420, "affordable": 180},
        {"year": 2012, "social": 360, "affordable": 160},
        {"year": 2014, "social": 310, "affordable": 140},
        {"year": 2016, "social": 260, "affordable": 130},
        {"year": 2018, "social": 230, "affordable": 120},
        {"year": 2020, "social": 260, "affordable": 130},
        {"year": 2022, "social": 320, "affordable": 160},
        {"year": 2023, "social": 380, "affordable": 190},
        {"year": 2024, "social": 420, "affordable": 210},
    ],
}

HOUSEHOLD_SIZE_TREND = {
    "WA":  [{"year": 2001, "avg": 2.72}, {"year": 2006, "avg": 2.65}, {"year": 2011, "avg": 2.60},
            {"year": 2016, "avg": 2.55}, {"year": 2021, "avg": 2.51}],
    "NSW": [{"year": 2001, "avg": 2.59}, {"year": 2006, "avg": 2.55}, {"year": 2011, "avg": 2.53},
            {"year": 2016, "avg": 2.51}, {"year": 2021, "avg": 2.47}],
    "VIC": [{"year": 2001, "avg": 2.60}, {"year": 2006, "avg": 2.57}, {"year": 2011, "avg": 2.55},
            {"year": 2016, "avg": 2.52}, {"year": 2021, "avg": 2.48}],
    "QLD": [{"year": 2001, "avg": 2.63}, {"year": 2006, "avg": 2.60}, {"year": 2011, "avg": 2.57},
            {"year": 2016, "avg": 2.52}, {"year": 2021, "avg": 2.48}],
    "SA":  [{"year": 2001, "avg": 2.44}, {"year": 2006, "avg": 2.40}, {"year": 2011, "avg": 2.38},
            {"year": 2016, "avg": 2.35}, {"year": 2021, "avg": 2.31}],
}

# ── State housing authority context ──────────────────────────────────────────
STATE_INFO = {
    "WA": {
        "full": "Western Australia",
        "authority": "DPLH — Dept. of Planning, Lands and Heritage",
        "social_housing_stock": 38000,
        "target_new_pa": 3300,
        "key_program": "WA Housing Strategy 2020–2030",
        "insight": (
            "WA's waitlist hit a decade low in 2019–20 as the mining boom's affordability pressure "
            "eased, but has since surged 43% in four years driven by post-COVID population growth, "
            "interstate migration, and a rental market vacancy rate under 1%. Supply is overwhelmingly "
            "detached houses — but over half of waitlist applicants are singles who need 1–2 bedroom "
            "apartments or units. The mismatch between what's being built and what's needed is structural."
        ),
    },
    "NSW": {
        "full": "New South Wales",
        "authority": "DCJ — Dept. of Communities and Justice",
        "social_housing_stock": 125000,
        "target_new_pa": 5400,
        "key_program": "NSW Housing 2041",
        "insight": (
            "NSW has the largest waitlist in the country — over 61,000 — and it has grown steadily "
            "for 20 years with no meaningful reduction. Despite high apartment construction in 2014–2017, "
            "almost none was affordable or social housing. The waitlist demographics show 49% singles "
            "and 13% aged — but new supply skews toward 3–4 bedroom houses in outer suburbs, far from "
            "services these cohorts need."
        ),
    },
    "VIC": {
        "full": "Victoria",
        "authority": "DFFH — Dept. of Families, Fairness and Housing",
        "social_housing_stock": 83000,
        "target_new_pa": 12000,
        "key_program": "Big Housing Build ($5.3B)",
        "insight": (
            "Victoria's waitlist nearly doubled from 38,000 to 63,000 in five years — the steepest "
            "deterioration of any state. The Big Housing Build ($5.3B, 12,000 new dwellings) is the "
            "largest state housing investment in Australian history and is now delivering. VIC is the "
            "only state building enough to potentially bend the curve — but 55% of applicants are "
            "singles, and the build mix must skew toward smaller typologies to match."
        ),
    },
    "QLD": {
        "full": "Queensland",
        "authority": "DCHDE — Housing and Homelessness",
        "social_housing_stock": 74000,
        "target_new_pa": 5200,
        "key_program": "Queensland Housing Investment Growth Initiative",
        "insight": (
            "QLD's waitlist has surged 67% since 2019, driven by interstate migration, "
            "tourism-driven rental market pressure in coastal regions, and a tight vacancy rate. "
            "Building approvals peaked in 2015–2016 and have been falling since. QLD's construction "
            "pipeline is dominated by detached housing, while 48% of waitlist applicants are singles "
            "and 25% are single-parent families — groups needing smaller, well-located dwellings."
        ),
    },
    "SA": {
        "full": "South Australia",
        "authority": "SAHT — SA Housing Trust",
        "social_housing_stock": 37000,
        "target_new_pa": 1000,
        "key_program": "Housing Roadmap 2024",
        "insight": (
            "SA has a smaller but rapidly growing waitlist, up 38% since 2022. SA's housing market "
            "has become one of Australia's tightest, with Adelaide vacancy rates under 0.5%. "
            "The SAHT stock has declined due to sales and demolitions outpacing new builds. "
            "Demographics show 53% singles and 14% aged — both groups needing affordable, "
            "smaller dwellings in accessible locations."
        ),
    },
}


def get_state_summary(state="WA"):
    """Returns full demand/supply summary dict for a given state."""
    waitlist = WAITLIST_TREND.get(state, [])
    demographics = WAITLIST_DEMOGRAPHICS.get(state, {})
    approvals = APPROVALS_BY_TYPE.get(state, [])
    social = SOCIAL_HOUSING_COMPLETIONS.get(state, [])
    hh_size = HOUSEHOLD_SIZE_TREND.get(state, [])
    info = STATE_INFO.get(state, {})

    if not waitlist:
        return {"error": f"No data for {state}"}

    latest_wl = waitlist[-1]
    prev_wl = waitlist[-2] if len(waitlist) > 1 else None
    earliest_wl = waitlist[0]

    wl_change_yoy = None
    if prev_wl:
        wl_change_yoy = round(
            ((latest_wl["applicants"] - prev_wl["applicants"]) / prev_wl["applicants"]) * 100, 1
        )

    decade_ago = next((w for w in reversed(waitlist) if w["year"] <= latest_wl["year"] - 10), None)
    wl_change_decade = None
    if decade_ago:
        wl_change_decade = round(
            ((latest_wl["applicants"] - decade_ago["applicants"]) / decade_ago["applicants"]) * 100, 1
        )

    latest_approvals = approvals[-1] if approvals else {}
    total_approvals = (latest_approvals.get("houses", 0) or 0) + (latest_approvals.get("other", 0) or 0)
    houses_pct = round(latest_approvals.get("houses", 0) / total_approvals * 100) if total_approvals else 0

    latest_social = social[-1] if social else {}
    social_completions = (latest_social.get("social", 0) or 0)
    affordable_completions = (latest_social.get("affordable", 0) or 0)
    accessible_total = social_completions + affordable_completions
    accessible_pct = round(accessible_total / total_approvals * 100, 1) if total_approvals else 0

    # Years to clear waitlist at current net social housing delivery rate
    latest_wl = waitlist[-1]
    years_to_clear = round(latest_wl["applicants"] / social_completions) if social_completions else None

    return {
        "state": state,
        "state_full": info.get("full", state),
        "authority": info.get("authority", ""),
        "social_housing_stock": info.get("social_housing_stock", 0),
        "target_new_pa": info.get("target_new_pa", 0),
        "key_program": info.get("key_program", ""),
        "insight": info.get("insight", ""),
        "latest_waitlist": latest_wl["applicants"],
        "waitlist_year": latest_wl["year"],
        "wl_change_yoy": wl_change_yoy,
        "wl_change_decade": wl_change_decade,
        "earliest_year": earliest_wl["year"],
        "latest_approvals_total": total_approvals,
        "latest_approvals_houses": latest_approvals.get("houses", 0),
        "latest_approvals_other": latest_approvals.get("other", 0),
        "houses_pct_of_approvals": houses_pct,
        "demographics": demographics,
        "waitlist_trend": waitlist,
        "approvals_by_type": approvals,
        "social_housing_completions": social,
        "latest_social_completions": social_completions,
        "latest_affordable_completions": affordable_completions,
        "accessible_total": accessible_total,
        "accessible_pct_of_approvals": accessible_pct,
        "years_to_clear_waitlist": years_to_clear,
        "household_size_trend": hh_size,
    }


def get_all_states_latest():
    """Returns latest-year snapshot for all states for comparison chart."""
    results = []
    for state in ["NSW", "VIC", "QLD", "WA", "SA"]:
        s = get_state_summary(state)
        if "error" not in s:
            results.append({
                "state": state,
                "waitlist": s["latest_waitlist"],
                "approvals_total": s["latest_approvals_total"],
                "approvals_houses": s["latest_approvals_houses"],
                "approvals_other": s["latest_approvals_other"],
                "stock": s["social_housing_stock"],
            })
    return results
