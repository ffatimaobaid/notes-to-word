"""
Learning Module — Feedback Collection & Adaptive Improvement

Tracks user feedback, identifies patterns, and adapts the agent's behavior
over time. Implements basic reinforcement through preference learning.
"""

from datetime import datetime
from agent.memory import (
    _load_long_term_memory,
    save_long_term_memory,
    add_feedback,
    get_average_feedback,
)


def record_user_feedback(score: int, content_type: str, strategy_used: str, 
                          notes: str = "") -> dict:
    """
    Record user feedback and trigger adaptive learning.
    
    Args:
        score: 1-5 rating from user
        content_type: Type of content that was processed
        strategy_used: Strategy that was used for this conversion
        notes: Optional text feedback from user
    
    Returns:
        Learning insights derived from the feedback
    """
    memory = _load_long_term_memory()
    memory = add_feedback(memory, score, notes)

    # Derive learning insights
    insights = _analyze_feedback_patterns(memory, content_type, score)

    # Apply adaptive changes
    if insights.get("should_adapt", False):
        memory = _apply_adaptations(memory, insights)
        save_long_term_memory(memory)

    return insights


def get_learning_summary(memory: dict) -> dict:
    """
    Generate a summary of what the agent has learned.
    """
    total = memory.get("total_conversions", 0)
    avg_feedback = get_average_feedback(memory)
    
    # Analyze content type performance
    type_counts = memory.get("content_type_counts", {})
    dominant_type = max(type_counts, key=type_counts.get) if any(type_counts.values()) else "none"

    # Analyze recent trends
    history = memory.get("conversion_history", [])
    recent = history[-10:] if len(history) >= 10 else history

    recent_confidence = [h.get("confidence", 0) for h in recent]
    avg_recent_confidence = (
        sum(recent_confidence) / len(recent_confidence) if recent_confidence else 0
    )

    # Determine performance trend
    if len(recent_confidence) >= 5:
        first_half = sum(recent_confidence[:len(recent_confidence)//2]) / (len(recent_confidence)//2)
        second_half = sum(recent_confidence[len(recent_confidence)//2:]) / (len(recent_confidence) - len(recent_confidence)//2)
        if second_half > first_half + 0.05:
            trend = "improving"
        elif second_half < first_half - 0.05:
            trend = "declining"
        else:
            trend = "stable"
    else:
        trend = "insufficient_data"

    return {
        "total_conversions": total,
        "average_feedback": avg_feedback,
        "dominant_content_type": dominant_type,
        "recent_avg_confidence": round(avg_recent_confidence, 2),
        "performance_trend": trend,
        "learned_preferences": memory.get("learned_preferences", {}),
        "common_corrections_count": len(memory.get("common_corrections", [])),
        "adaptations_applied": _count_adaptations(memory),
    }


def _analyze_feedback_patterns(memory: dict, content_type: str, 
                                latest_score: int) -> dict:
    """
    Analyze feedback patterns to derive learning insights.
    """
    feedback_scores = memory.get("feedback_scores", [])
    recent_scores = [f["score"] for f in feedback_scores[-10:]]

    insights = {
        "latest_score": latest_score,
        "recent_average": round(sum(recent_scores) / len(recent_scores), 1) if recent_scores else 0,
        "content_type": content_type,
        "should_adapt": False,
        "adaptation_suggestions": [],
    }

    # Trigger adaptation if recent scores show a pattern
    if len(recent_scores) >= 3:
        avg = insights["recent_average"]

        if avg < 3.0:
            insights["should_adapt"] = True
            insights["adaptation_suggestions"].append(
                "Consider increasing detail level — users want more comprehensive output"
            )

        if content_type == "math" and avg < 3.5:
            insights["should_adapt"] = True
            insights["adaptation_suggestions"].append(
                "Math transcription needs improvement — enable enhancement pass by default"
            )

    # Check for consistent low scores
    if len(recent_scores) >= 5 and all(s <= 2 for s in recent_scores[-3:]):
        insights["should_adapt"] = True
        insights["adaptation_suggestions"].append(
            "Multiple low ratings — switching to multi-pass strategy by default"
        )

    return insights


def _apply_adaptations(memory: dict, insights: dict) -> dict:
    """
    Apply learned adaptations to agent preferences.
    """
    prefs = memory.get("learned_preferences", {})

    for suggestion in insights.get("adaptation_suggestions", []):
        if "detail level" in suggestion.lower():
            prefs["detail_level"] = "very_high"
        if "enhancement pass" in suggestion.lower():
            prefs["always_enhance"] = True
        if "multi-pass" in suggestion.lower():
            prefs["min_passes"] = 2

    memory["learned_preferences"] = prefs

    # Log the adaptation
    if "adaptations_log" not in memory:
        memory["adaptations_log"] = []

    memory["adaptations_log"].append({
        "timestamp": datetime.now().isoformat(),
        "insights": insights["adaptation_suggestions"],
        "changes_applied": prefs,
    })

    # Keep log manageable
    memory["adaptations_log"] = memory["adaptations_log"][-20:]

    return memory


def _count_adaptations(memory: dict) -> int:
    """Count total adaptations applied."""
    return len(memory.get("adaptations_log", []))
