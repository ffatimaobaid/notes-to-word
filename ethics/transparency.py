"""
Transparency Module — Audit Trails & Explainability

Provides full transparency into the agent's operations:
- Audit trail of all agent decisions and actions
- Explainability reports for each conversion
- "Why did the agent do this?" answers
"""

import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
AUDIT_FILE = DATA_DIR / "audit_log.json"


def _ensure_data_dir():
    """Create data directory if it doesn't exist."""
    DATA_DIR.mkdir(exist_ok=True)


def _load_audit_log() -> list:
    """Load audit log from persistent storage."""
    _ensure_data_dir()
    if AUDIT_FILE.exists():
        try:
            with open(AUDIT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def _save_audit_log(log: list):
    """Save audit log to persistent storage."""
    _ensure_data_dir()
    # Keep last 200 entries
    log = log[-200:]
    with open(AUDIT_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, default=str)


def log_agent_action(phase: str, action: str, details: dict = None):
    """
    Log an agent action to the audit trail.
    
    Args:
        phase: Agent phase (observe, decide, act, learn)
        action: Description of the action
        details: Additional context data
    """
    log = _load_audit_log()

    entry = {
        "id": len(log) + 1,
        "timestamp": datetime.now().isoformat(),
        "phase": phase,
        "action": action,
        "details": details or {},
    }

    log.append(entry)
    _save_audit_log(log)


def get_audit_trail(limit: int = 50) -> list:
    """Retrieve the most recent audit trail entries."""
    log = _load_audit_log()
    return log[-limit:]


def get_audit_summary() -> dict:
    """Get a summary of audit trail statistics."""
    log = _load_audit_log()

    if not log:
        return {
            "total_entries": 0,
            "phases": {},
            "first_entry": None,
            "last_entry": None,
        }

    # Count by phase
    phases = {}
    for entry in log:
        phase = entry.get("phase", "unknown")
        phases[phase] = phases.get(phase, 0) + 1

    return {
        "total_entries": len(log),
        "phases": phases,
        "first_entry": log[0].get("timestamp"),
        "last_entry": log[-1].get("timestamp"),
    }


def generate_explainability_report(thought_log: list, decisions: list, 
                                     actions: list) -> str:
    """
    Generate a human-readable explainability report from agent's
    thought process, decisions, and actions.
    """
    report = []
    report.append("=" * 50)
    report.append("AGENT EXPLAINABILITY REPORT")
    report.append("=" * 50)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")

    # Thought Process
    report.append("── THOUGHT PROCESS ──")
    for i, thought in enumerate(thought_log, 1):
        stage = thought.get("stage", "")
        text = thought.get("thought", "")
        report.append(f"  {i}. [{stage.upper()}] {text}")
    report.append("")

    # Decisions Made
    report.append("── DECISIONS MADE ──")
    for i, dec in enumerate(decisions, 1):
        report.append(f"  {i}. {dec.get('decision', '')}")
        report.append(f"     Reason: {dec.get('reason', '')}")
    report.append("")

    # Actions Taken
    report.append("── ACTIONS TAKEN ──")
    for i, act in enumerate(actions, 1):
        report.append(f"  {i}. {act.get('action', '')} → {act.get('result', '')}")
    report.append("")

    report.append("=" * 50)
    report.append("This report provides full transparency into the agent's")
    report.append("autonomous decision-making process, in compliance with")
    report.append("ACM Code of Ethics Principle 1.3 (Be honest and trustworthy)")
    report.append("=" * 50)

    return "\n".join(report)
