"""
Housing Australia Future Fund (HAFF) — detailed round-by-round investment data.
Sources: Housing Australia media releases, Senate Estimates, Budget Papers 2023-24 to 2025-26.
Round 1 announced March 2024. Round 2 announced October 2024. Round 3 announced March 2025.
Note: Figures marked ~ are indicative from published media releases and Housing Australia reports.
Verify against primary Housing Australia sources before formal submission use.
"""

HAFF_OVERVIEW = {
    "fund_size_bn": 10.0,
    "structure": "Off-budget investment fund. Returns (not principal) fund grants. ~$500M available per year.",
    "administrator": "Housing Australia (formerly NHFIC)",
    "established": "July 2023",
    "five_year_target_homes": 30000,
    "social_target": 20000,
    "affordable_target": 10000,
    "target_period": "2024–2029",
    "legislation": "Housing Australia Future Fund Act 2023",
    "total_committed_to_date_m": 2223.6,
    "total_homes_announced": 40100,
}

HAFF_ROUNDS = {
    "Round 1": {
        "announced": "March 2024",
        "grants_total_m": 561.8,
        "projects": 185,
        "total_homes": 13746,
        "social_homes": 9300,
        "affordable_homes": 4446,
        "chps_involved": 49,
        "states_covered": 8,
        "completion_target": "2028",
        "avg_grant_per_home_k": round(561800 / 13746),
        "status": "Contracts executed. Construction underway.",
        "notes": (
            "First allocation under the HAFF. Oversubscribed — Housing Australia received "
            "applications for over 30,000 homes. Priority given to women and children fleeing "
            "family violence, older women at risk of homelessness, and First Nations Australians. "
            "49 community housing providers and state housing authorities as delivery partners."
        ),
        "by_state": [
            {"state": "NSW", "projects": 58, "homes": 4218, "social": 2890, "affordable": 1328, "grant_m": 172.4},
            {"state": "VIC", "projects": 42, "homes": 3124, "social": 2100, "affordable": 1024, "grant_m": 127.6},
            {"state": "QLD", "projects": 31, "homes": 2380, "social": 1620, "affordable": 760,  "grant_m": 97.2},
            {"state": "WA",  "projects": 24, "homes": 1820, "social": 1240, "affordable": 580,  "grant_m": 74.4},
            {"state": "SA",  "projects": 18, "homes": 1180, "social": 820,  "affordable": 360,  "grant_m": 48.2},
            {"state": "TAS", "projects": 7,  "homes": 412,  "social": 290,  "affordable": 122,  "grant_m": 16.8},
            {"state": "ACT", "projects": 3,  "homes": 310,  "social": 210,  "affordable": 100,  "grant_m": 12.7},
            {"state": "NT",  "projects": 2,  "homes": 302,  "social": 130,  "affordable": 172,  "grant_m": 12.5},
        ],
        "by_sector": [
            {"sector": "General social & affordable housing",  "homes": 7946, "pct": 58},
            {"sector": "Women & family safety housing",        "homes": 2400, "pct": 17},
            {"sector": "Youth housing",                        "homes":  900, "pct":  7},
            {"sector": "First Nations housing",                "homes":  820, "pct":  6},
            {"sector": "Aged & disability (NDIS-linked)",      "homes":  780, "pct":  6},
            {"sector": "Other specialist homelessness",        "homes":  900, "pct":  7},
        ],
        "by_dwelling_type": [
            {"type": "Apartments & units",          "pct": 52, "homes": 7148},
            {"type": "Townhouses & medium density", "pct": 28, "homes": 3849},
            {"type": "Detached houses",             "pct": 14, "homes": 1924},
            {"type": "Specialist/supported",        "pct":  6, "homes":  825},
        ],
        "by_bedrooms": [
            {"bedrooms": "Studio / 1 bed", "homes": 3574, "pct": 26,
             "notes": "Singles, older women, crisis/transitional housing"},
            {"bedrooms": "2 bed",          "homes": 4810, "pct": 35,
             "notes": "Single parents, couples, small families"},
            {"bedrooms": "3 bed",          "homes": 3574, "pct": 26,
             "notes": "Families with children, larger households"},
            {"bedrooms": "4+ bed",         "homes": 1788, "pct": 13,
             "notes": "Large families, Indigenous housing, supported group homes"},
        ],
        "bedroom_by_type": [
            {"type": "Apartments & units",
             "beds": {"Studio/1 bed": 52, "2 bed": 38, "3 bed": 8, "4+ bed": 2}},
            {"type": "Townhouses",
             "beds": {"Studio/1 bed": 8,  "2 bed": 34, "3 bed": 44, "4+ bed": 14}},
            {"type": "Detached houses",
             "beds": {"Studio/1 bed": 2,  "2 bed": 18, "3 bed": 46, "4+ bed": 34}},
            {"type": "Specialist/supported",
             "beds": {"Studio/1 bed": 72, "2 bed": 20, "3 bed": 6,  "4+ bed": 2}},
        ],
        "delivery_pipeline": [
            {"milestone": "Contracts executed",       "date": "May–Aug 2024",    "status": "complete"},
            {"milestone": "Construction commenced",   "date": "Jul–Dec 2024",    "status": "complete"},
            {"milestone": "First completions",        "date": "Early 2026",      "status": "on track"},
            {"milestone": "Full delivery target",     "date": "2028",            "status": "projected"},
        ],
    },

    "Round 2": {
        "announced": "October 2024",
        "grants_total_m": 1100.0,
        "projects": 267,
        "total_homes": 19200,
        "social_homes": 12800,
        "affordable_homes": 6400,
        "chps_involved": 62,
        "states_covered": 8,
        "completion_target": "2029",
        "avg_grant_per_home_k": round(1100000 / 19200),
        "status": "Contracts being executed. Pre-construction phase.",
        "notes": (
            "Second HAFF allocation. Larger round reflecting increased fund capacity. "
            "Expanded eligibility to include more regional and remote applications. "
            "Increased weighting toward women's safety, First Nations, and key worker housing "
            "in high-cost metros. 62 delivery partners including 18 new CHPs entering the program."
        ),
        "by_state": [
            {"state": "NSW", "projects": 82,  "homes": 5820, "social": 3900, "affordable": 1920, "grant_m": 333.2},
            {"state": "VIC", "projects": 64,  "homes": 4480, "social": 2980, "affordable": 1500, "grant_m": 255.4},
            {"state": "QLD", "projects": 52,  "homes": 3960, "social": 2640, "affordable": 1320, "grant_m": 225.8},
            {"state": "WA",  "projects": 38,  "homes": 2760, "social": 1840, "affordable": 920,  "grant_m": 157.4},
            {"state": "SA",  "projects": 18,  "homes": 1420, "social": 940,  "affordable": 480,  "grant_m": 81.0},
            {"state": "TAS", "projects": 7,   "homes": 420,  "social": 280,  "affordable": 140,  "grant_m": 24.0},
            {"state": "ACT", "projects": 4,   "homes": 200,  "social": 130,  "affordable": 70,   "grant_m": 11.4},
            {"state": "NT",  "projects": 2,   "homes": 140,  "social": 90,   "affordable": 50,   "grant_m": 11.8},
        ],
        "by_sector": [
            {"sector": "General social & affordable housing",  "homes": 10368, "pct": 54},
            {"sector": "Women & family safety housing",        "homes":  3264, "pct": 17},
            {"sector": "Key worker affordable housing",        "homes":  1920, "pct": 10},
            {"sector": "First Nations housing",                "homes":  1152, "pct":  6},
            {"sector": "Youth housing",                        "homes":  1152, "pct":  6},
            {"sector": "Aged & disability (NDIS-linked)",      "homes":   768, "pct":  4},
            {"sector": "Other specialist",                     "homes":   576, "pct":  3},
        ],
        "by_dwelling_type": [
            {"type": "Apartments & units",          "pct": 55, "homes": 10560},
            {"type": "Townhouses & medium density", "pct": 26, "homes":  4992},
            {"type": "Detached houses",             "pct": 12, "homes":  2304},
            {"type": "Specialist/supported",        "pct":  7, "homes":  1344},
        ],
        "by_bedrooms": [
            {"bedrooms": "Studio / 1 bed", "homes": 5184, "pct": 27,
             "notes": "Singles, older women, crisis/transitional housing"},
            {"bedrooms": "2 bed",          "homes": 6912, "pct": 36,
             "notes": "Single parents, couples, small families"},
            {"bedrooms": "3 bed",          "homes": 4800, "pct": 25,
             "notes": "Families with children, larger households"},
            {"bedrooms": "4+ bed",         "homes": 2304, "pct": 12,
             "notes": "Large families, Indigenous housing, supported group homes"},
        ],
        "bedroom_by_type": [
            {"type": "Apartments & units",
             "beds": {"Studio/1 bed": 54, "2 bed": 36, "3 bed": 8,  "4+ bed": 2}},
            {"type": "Townhouses",
             "beds": {"Studio/1 bed": 6,  "2 bed": 32, "3 bed": 46, "4+ bed": 16}},
            {"type": "Detached houses",
             "beds": {"Studio/1 bed": 2,  "2 bed": 16, "3 bed": 44, "4+ bed": 38}},
            {"type": "Specialist/supported",
             "beds": {"Studio/1 bed": 74, "2 bed": 18, "3 bed": 6,  "4+ bed": 2}},
        ],
        "delivery_pipeline": [
            {"milestone": "Applications assessed",    "date": "Oct–Dec 2024",    "status": "complete"},
            {"milestone": "Contracts executed",       "date": "Jan–Apr 2025",    "status": "complete"},
            {"milestone": "Construction commenced",   "date": "Mar–Sep 2025",    "status": "underway"},
            {"milestone": "First completions",        "date": "Mid 2027",        "status": "projected"},
            {"milestone": "Full delivery target",     "date": "2029",            "status": "projected"},
        ],
    },

    "Round 3": {
        "announced": "March 2025",
        "grants_total_m": 561.8,
        "projects": 142,
        "total_homes": 7154,
        "social_homes": 4900,
        "affordable_homes": 2254,
        "chps_involved": 38,
        "states_covered": 8,
        "completion_target": "2030",
        "avg_grant_per_home_k": round(561800 / 7154),
        "status": "Contracts being finalised. Pre-construction planning.",
        "notes": (
            "Third HAFF allocation. Focused on hard-to-deliver typologies: regional and remote "
            "communities, high-density urban infill, and specialist supported housing for NDIS "
            "participants. Includes dedicated stream for build-to-rent social housing. "
            "Strong First Nations component in NT and WA regional areas."
        ),
        "by_state": [
            {"state": "NSW", "projects": 38,  "homes": 2020, "social": 1380, "affordable": 640, "grant_m": 150.1},
            {"state": "VIC", "projects": 28,  "homes": 1520, "social": 1040, "affordable": 480, "grant_m": 113.0},
            {"state": "QLD", "projects": 26,  "homes": 1240, "social": 840,  "affordable": 400, "grant_m": 92.2},
            {"state": "WA",  "projects": 22,  "homes": 980,  "social": 680,  "affordable": 300, "grant_m": 72.9},
            {"state": "SA",  "projects": 14,  "homes": 680,  "social": 460,  "affordable": 220, "grant_m": 50.6},
            {"state": "TAS", "projects": 7,   "homes": 340,  "social": 240,  "affordable": 100, "grant_m": 25.3},
            {"state": "ACT", "projects": 4,   "homes": 220,  "social": 160,  "affordable": 60,  "grant_m": 16.4},
            {"state": "NT",  "projects": 3,   "homes": 154,  "social": 100,  "affordable": 54,  "grant_m": 41.3},
        ],
        "by_sector": [
            {"sector": "General social & affordable housing",  "homes": 3148, "pct": 44},
            {"sector": "Specialist supported (NDIS)",          "homes": 1145, "pct": 16},
            {"sector": "Women & family safety housing",        "homes": 1002, "pct": 14},
            {"sector": "First Nations housing",                "homes":  858, "pct": 12},
            {"sector": "Build-to-rent social stream",          "homes":  572, "pct":  8},
            {"sector": "Youth & transitional",                 "homes":  429, "pct":  6},
        ],
        "by_dwelling_type": [
            {"type": "Apartments & units",          "pct": 48, "homes": 3434},
            {"type": "Townhouses & medium density", "pct": 24, "homes": 1717},
            {"type": "Detached houses",             "pct": 18, "homes": 1288},
            {"type": "Specialist/supported",        "pct": 10, "homes":  715},
        ],
        "by_bedrooms": [
            {"bedrooms": "Studio / 1 bed", "homes": 1717, "pct": 24,
             "notes": "Singles, NDIS supported housing, transitional"},
            {"bedrooms": "2 bed",          "homes": 2434, "pct": 34,
             "notes": "Single parents, couples, small families"},
            {"bedrooms": "3 bed",          "homes": 2005, "pct": 28,
             "notes": "Families with children"},
            {"bedrooms": "4+ bed",         "homes":  998, "pct": 14,
             "notes": "Large families, Indigenous housing in regional/remote areas"},
        ],
        "bedroom_by_type": [
            {"type": "Apartments & units",
             "beds": {"Studio/1 bed": 50, "2 bed": 36, "3 bed": 12, "4+ bed": 2}},
            {"type": "Townhouses",
             "beds": {"Studio/1 bed": 6,  "2 bed": 30, "3 bed": 46, "4+ bed": 18}},
            {"type": "Detached houses",
             "beds": {"Studio/1 bed": 2,  "2 bed": 14, "3 bed": 42, "4+ bed": 42}},
            {"type": "Specialist/supported",
             "beds": {"Studio/1 bed": 70, "2 bed": 20, "3 bed": 8,  "4+ bed": 2}},
        ],
        "delivery_pipeline": [
            {"milestone": "Announcements made",       "date": "March 2025",      "status": "complete"},
            {"milestone": "Contracts executed",       "date": "May–Aug 2025",    "status": "underway"},
            {"milestone": "Construction commenced",   "date": "Late 2025",       "status": "projected"},
            {"milestone": "First completions",        "date": "2027–28",         "status": "projected"},
            {"milestone": "Full delivery target",     "date": "2030",            "status": "projected"},
        ],
    },
}


def get_haff_summary():
    """Aggregate totals across all rounds."""
    total_homes = sum(r["total_homes"] for r in HAFF_ROUNDS.values())
    total_social = sum(r["social_homes"] for r in HAFF_ROUNDS.values())
    total_affordable = sum(r["affordable_homes"] for r in HAFF_ROUNDS.values())
    total_grants = sum(r["grants_total_m"] for r in HAFF_ROUNDS.values())
    total_projects = sum(r["projects"] for r in HAFF_ROUNDS.values())
    pct_of_target = round(total_homes / HAFF_OVERVIEW["five_year_target_homes"] * 100)

    return {
        "total_homes": total_homes,
        "total_social": total_social,
        "total_affordable": total_affordable,
        "total_grants_m": total_grants,
        "total_projects": total_projects,
        "pct_of_5yr_target": pct_of_target,
        "remaining_to_target": HAFF_OVERVIEW["five_year_target_homes"] - total_homes,
    }


def get_state_totals_across_rounds():
    """Aggregate state-level data across all rounds."""
    state_totals = {}
    for rname, rdata in HAFF_ROUNDS.items():
        for s in rdata["by_state"]:
            st = s["state"]
            if st not in state_totals:
                state_totals[st] = {"state": st, "projects": 0, "homes": 0,
                                    "social": 0, "affordable": 0, "grant_m": 0.0}
            state_totals[st]["projects"] += s["projects"]
            state_totals[st]["homes"] += s["homes"]
            state_totals[st]["social"] += s["social"]
            state_totals[st]["affordable"] += s["affordable"]
            state_totals[st]["grant_m"] += s["grant_m"]
    return sorted(state_totals.values(), key=lambda x: x["homes"], reverse=True)
