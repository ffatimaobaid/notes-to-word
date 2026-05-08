"""
Memory Module — Short-term & Long-term Memory for the Notes Agent

Short-term memory: Session-scoped context (current images, decisions, results)
Long-term memory: Persistent JSON store of past conversions, preferences, patterns
"""

import json
import os
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
MEMORY_FILE = DATA_DIR / "memory_store.json"


def _ensure_data_dir():
    """Create data directory if it doesn't exist."""
    DATA_DIR.mkdir(exist_ok=True)


def _load_long_term_memory() -> dict:
    """Load long-term memory from persistent JSON store."""
    _ensure_data_dir()
    if MEMORY_FILE.exists():
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return _default_memory()
    return _default_memory()


def _default_memory() -> dict:
    """Return default empty memory structure."""
    return {
        "total_conversions": 0,
        "successful_conversions": 0,
        "failed_conversions": 0,
        "content_type_counts": {
            "text": 0,
            "math": 0,
            "diagram": 0,
            "mixed": 0,
        },
        "average_confidence": 0.0,
        "feedback_scores": [],
        "conversion_history": [],
        "learned_preferences": {
            "preferred_format": "structured",
            "detail_level": "high",
            "include_latex": True,
        },
        "common_corrections": [],
        "created_at": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat(),
    }


def save_long_term_memory(memory: dict):
    """Persist long-term memory to JSON file."""
    _ensure_data_dir()
    memory["last_updated"] = datetime.now().isoformat()
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, default=str)


def add_conversion_record(memory: dict, record: dict) -> dict:
    """Add a conversion record to long-term memory and update statistics."""
    memory["total_conversions"] += 1

    if record.get("success", False):
        memory["successful_conversions"] += 1
    else:
        memory["failed_conversions"] += 1

    # Update content type counts
    content_type = record.get("content_type", "text")
    if content_type in memory["content_type_counts"]:
        memory["content_type_counts"][content_type] += 1

    # Update average confidence
    confidence = record.get("confidence", 0.0)
    total = memory["total_conversions"]
    prev_avg = memory["average_confidence"]
    memory["average_confidence"] = round(
        ((prev_avg * (total - 1)) + confidence) / total, 3
    )

    # Append to history (keep last 50)
    history_entry = {
        "timestamp": datetime.now().isoformat(),
        "content_type": content_type,
        "confidence": confidence,
        "success": record.get("success", False),
        "image_quality": record.get("image_quality", "unknown"),
        "strategy_used": record.get("strategy_used", "default"),
        "word_count": record.get("word_count", 0),
    }
    memory["conversion_history"].append(history_entry)
    memory["conversion_history"] = memory["conversion_history"][-50:]

    save_long_term_memory(memory)
    return memory


def add_feedback(memory: dict, score: int, notes: str = "") -> dict:
    """Record user feedback (1-5 scale) into memory."""
    feedback_entry = {
        "timestamp": datetime.now().isoformat(),
        "score": score,
        "notes": notes,
    }
    memory["feedback_scores"].append(feedback_entry)
    memory["feedback_scores"] = memory["feedback_scores"][-100:]
    save_long_term_memory(memory)
    return memory


def get_success_rate(memory: dict) -> float:
    """Calculate overall success rate."""
    total = memory["total_conversions"]
    if total == 0:
        return 0.0
    return round(memory["successful_conversions"] / total * 100, 1)


def get_average_feedback(memory: dict) -> float:
    """Get average feedback score."""
    scores = [f["score"] for f in memory["feedback_scores"]]
    if not scores:
        return 0.0
    return round(sum(scores) / len(scores), 1)


def get_dominant_content_type(memory: dict) -> str:
    """Find the most frequently processed content type."""
    counts = memory["content_type_counts"]
    if not any(counts.values()):
        return "none"
    return max(counts, key=counts.get)


class ShortTermMemory:
    """Session-scoped working memory for the agent's current task."""

    def __init__(self):
        self.current_image = None
        self.perception_results = {}
        self.decisions_made = []
        self.actions_taken = []
        self.current_result = None
        self.confidence_score = 0.0
        self.processing_start_time = None
        self.thought_log = []

    def log_thought(self, stage: str, thought: str):
        """Record agent's reasoning for transparency."""
        self.thought_log.append({
            "timestamp": datetime.now().isoformat(),
            "stage": stage,
            "thought": thought,
        })

    def log_decision(self, decision: str, reason: str):
        """Record a decision and its justification."""
        self.decisions_made.append({
            "timestamp": datetime.now().isoformat(),
            "decision": decision,
            "reason": reason,
        })

    def log_action(self, action: str, result: str):
        """Record an action and its outcome."""
        self.actions_taken.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "result": result,
        })

    def get_thought_log(self) -> list:
        """Return the full thought log for transparency display."""
        return self.thought_log

    def reset(self):
        """Clear short-term memory for a new task."""
        self.__init__()
