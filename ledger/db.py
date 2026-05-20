"""
SQLite database for the Policy Outcome Ledger.
Tracks: Program → Funding committed → Targets → Actual outcomes → Gap
This is the structured layer that turns research text into queryable data.
"""
import sqlite3
from pathlib import Path
from config import DATA_DIR

DB_PATH = DATA_DIR / "ledger.db"


def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS programs (
        id                  INTEGER PRIMARY KEY AUTOINCREMENT,
        name                TEXT NOT NULL,
        short_name          TEXT,
        announced_year      INTEGER,
        implemented_year    INTEGER,
        end_year            INTEGER,
        funding_committed_bn REAL,
        funding_drawn_bn    REAL,
        administering_agency TEXT,
        program_type        TEXT,
        geographic_scope    TEXT DEFAULT 'Federal',
        description         TEXT,
        source_url          TEXT,
        status              TEXT DEFAULT 'Completed'
    );

    CREATE TABLE IF NOT EXISTS targets (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        program_id      INTEGER REFERENCES programs(id),
        metric          TEXT NOT NULL,
        target_value    REAL,
        target_unit     TEXT,
        target_year     INTEGER,
        source          TEXT
    );

    CREATE TABLE IF NOT EXISTS outcomes (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        program_id      INTEGER REFERENCES programs(id),
        metric          TEXT NOT NULL,
        actual_value    REAL,
        actual_unit     TEXT,
        measurement_year INTEGER,
        confidence      TEXT DEFAULT 'Medium',
        source_report   TEXT,
        source_url      TEXT,
        notes           TEXT
    );

    CREATE TABLE IF NOT EXISTS evidence_links (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        program_id      INTEGER REFERENCES programs(id),
        chunk_id        TEXT,
        report_title    TEXT,
        report_year     INTEGER,
        relevance_score REAL,
        excerpt         TEXT
    );

    CREATE TABLE IF NOT EXISTS extracted_insights (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        program_id      INTEGER REFERENCES programs(id),
        insight_type    TEXT,
        content         TEXT,
        extracted_at    TEXT DEFAULT (datetime('now'))
    );
    """)
    conn.commit()
    conn.close()


def get_all_programs():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM programs ORDER BY announced_year DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_program(program_id):
    conn = get_conn()
    p = conn.execute("SELECT * FROM programs WHERE id=?", (program_id,)).fetchone()
    targets = conn.execute("SELECT * FROM targets WHERE program_id=?", (program_id,)).fetchall()
    outcomes = conn.execute("SELECT * FROM outcomes WHERE program_id=?", (program_id,)).fetchall()
    evidence = conn.execute(
        "SELECT * FROM evidence_links WHERE program_id=? ORDER BY relevance_score DESC LIMIT 8",
        (program_id,)
    ).fetchall()
    insights = conn.execute(
        "SELECT * FROM extracted_insights WHERE program_id=? ORDER BY extracted_at DESC",
        (program_id,)
    ).fetchall()
    conn.close()
    return {
        "program": dict(p) if p else None,
        "targets": [dict(r) for r in targets],
        "outcomes": [dict(r) for r in outcomes],
        "evidence": [dict(r) for r in evidence],
        "insights": [dict(r) for r in insights],
    }


def save_extracted_outcomes(program_id, outcomes_data, insights_text):
    """Save Claude-extracted outcomes back to the ledger."""
    conn = get_conn()
    for o in outcomes_data:
        # Check if this metric already exists
        existing = conn.execute(
            "SELECT id FROM outcomes WHERE program_id=? AND metric=?",
            (program_id, o.get("metric"))
        ).fetchone()
        if not existing:
            conn.execute("""
                INSERT INTO outcomes (program_id, metric, actual_value, actual_unit,
                    measurement_year, confidence, source_report, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                program_id, o.get("metric"), o.get("actual_value"),
                o.get("actual_unit"), o.get("measurement_year"),
                o.get("confidence", "Medium"), o.get("source_report"), o.get("notes")
            ))

    conn.execute("""
        INSERT INTO extracted_insights (program_id, insight_type, content)
        VALUES (?, 'claude_analysis', ?)
    """, (program_id, insights_text))
    conn.commit()
    conn.close()


def save_evidence_links(program_id, chunks):
    conn = get_conn()
    conn.execute("DELETE FROM evidence_links WHERE program_id=?", (program_id,))
    for c in chunks:
        conn.execute("""
            INSERT INTO evidence_links (program_id, chunk_id, report_title, report_year,
                relevance_score, excerpt)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            program_id, c.get("chunk_id", ""),
            c.get("title"), c.get("year"),
            c.get("relevance_score"), c.get("text", "")[:500]
        ))
    conn.commit()
    conn.close()
