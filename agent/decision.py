"""
Decision Engine — Strategy Selection & Ethical Decision Making

The decision engine selects:
- Transcription strategy based on perception results
- Appropriate prompts for content types
- Whether to proceed autonomously or request human input
- Ethical compliance checks at each decision point
"""

from datetime import datetime


# --- Prompt Templates per Content Type ---

PROMPTS = {
    "text": """
Transcribe this handwritten note with high accuracy.
- Maintain all headings, subheadings, and bullet points.
- Preserve paragraph structure and indentation.
- Fix obvious spelling errors but flag uncertain words with [?].
- Return ONLY the clean transcription.
""",
    "math": """
Transcribe this handwritten note containing mathematical content.
- Convert all mathematical formulas to LaTeX notation wrapped in $...$ for inline or $$...$$ for display.
- Preserve all variable names, subscripts, and superscripts accurately.
- Maintain surrounding text context and structure.
- For chemical formulas, use proper notation (e.g., H₂O).
- Return ONLY the transcription.
""",
    "diagram": """
Transcribe this handwritten note containing diagrams.
- Transcribe all readable text accurately.
- For each diagram, provide a detailed description in [Diagram: ...] brackets.
- Include diagram labels, connections, and relationships.
- Describe flowcharts as step-by-step processes.
- Return ONLY the transcription with diagram descriptions.
""",
    "mixed": """
Transcribe this handwritten note containing mixed content (text, formulas, and/or diagrams).
- Transcribe all text accurately, maintaining headings and structure.
- Convert mathematical formulas to LaTeX notation ($...$ or $$...$$).
- Describe diagrams in [Diagram: ...] brackets with full detail.
- Maintain the original layout order of content.
- Flag uncertain elements with [?].
- Return ONLY the transcription.
""",
}

ENHANCEMENT_PROMPT = """
Review and enhance this transcription for accuracy and clarity:

ORIGINAL TRANSCRIPTION:
{text}

Instructions:
- Fix any OCR errors or misrecognized characters.
- Ensure mathematical notation is consistent.
- Improve formatting and structure.
- Add missing punctuation where obvious.
- Return the enhanced version ONLY.
"""


def select_strategy(perception_results: dict, memory_context: dict = None) -> dict:
    """
    Select the best transcription strategy based on perception analysis.
    
    Returns a strategy dict with: prompt, passes, confidence threshold,
    and whether human review is recommended.
    """
    quality = perception_results.get("quality", {})
    content = perception_results.get("content_type", {})
    recommendations = perception_results.get("recommendations", [])

    overall_quality = quality.get("overall_score", 50)
    primary_type = content.get("primary_type", "text")
    content_confidence = content.get("confidence", 0.5)

    # --- Strategy Decision Logic ---

    # Determine number of passes based on quality and complexity
    if overall_quality >= 70 and content_confidence >= 0.7:
        num_passes = 1  # High quality → single pass sufficient
        autonomy = "full"
    elif overall_quality >= 50:
        num_passes = 2  # Medium quality → rough + refined
        autonomy = "semi"
    else:
        num_passes = 2  # Low quality → rough + refined + human review
        autonomy = "human_required"

    # Determine if enhancement pass is needed
    needs_enhancement = overall_quality < 60 or primary_type in ("math", "mixed")

    # Select prompt
    prompt = PROMPTS.get(primary_type, PROMPTS["text"])

    # Confidence threshold for accepting results
    if primary_type == "text":
        accept_threshold = 0.6
    elif primary_type in ("math", "mixed"):
        accept_threshold = 0.7
    else:
        accept_threshold = 0.65

    # Check memory for learned preferences
    detail_level = "high"
    if memory_context:
        prefs = memory_context.get("learned_preferences", {})
        detail_level = prefs.get("detail_level", "high")

    strategy = {
        "primary_type": primary_type,
        "prompt": prompt,
        "num_passes": num_passes,
        "needs_enhancement": needs_enhancement,
        "enhancement_prompt": ENHANCEMENT_PROMPT if needs_enhancement else None,
        "autonomy_level": autonomy,
        "accept_threshold": accept_threshold,
        "detail_level": detail_level,
        "human_review_recommended": autonomy == "human_required",
        "reasoning": _generate_reasoning(
            overall_quality, primary_type, content_confidence, num_passes, autonomy
        ),
    }

    return strategy


def evaluate_result_confidence(result_text: str, strategy: dict) -> dict:
    """
    Evaluate the confidence of a transcription result.
    Uses heuristic indicators to assess quality.
    """
    if not result_text:
        return {"confidence": 0.0, "issues": ["Empty result"], "acceptable": False}

    issues = []
    confidence = 0.85  # Start with base confidence

    # Check for uncertainty markers
    uncertain_count = result_text.count("[?]")
    if uncertain_count > 5:
        confidence -= 0.15
        issues.append(f"{uncertain_count} uncertain elements detected")
    elif uncertain_count > 0:
        confidence -= 0.05
        issues.append(f"{uncertain_count} uncertain elements detected")

    # Check for very short output (may indicate failure)
    word_count = len(result_text.split())
    if word_count < 10:
        confidence -= 0.2
        issues.append("Very short output — possible transcription failure")

    # Check for error indicators
    error_phrases = ["I cannot", "I'm unable", "error", "failed"]
    for phrase in error_phrases:
        if phrase.lower() in result_text.lower():
            confidence -= 0.3
            issues.append(f"Error indicator found: '{phrase}'")
            break

    # Check for diagram descriptions if expected
    if strategy.get("primary_type") in ("diagram", "mixed"):
        if "[Diagram:" not in result_text and "[diagram:" not in result_text.lower():
            confidence -= 0.1
            issues.append("Expected diagram descriptions not found")

    # Check for LaTeX if math content expected
    if strategy.get("primary_type") in ("math", "mixed"):
        if "$" not in result_text:
            confidence -= 0.1
            issues.append("Expected LaTeX notation not found")

    confidence = max(0.0, min(1.0, confidence))
    acceptable = confidence >= strategy.get("accept_threshold", 0.6)

    if not issues:
        issues.append("No issues detected")

    return {
        "confidence": round(confidence, 2),
        "word_count": word_count,
        "issues": issues,
        "acceptable": acceptable,
        "recommendation": "accept" if acceptable else "review_required",
    }


def ethical_decision_check(action: str, context: dict = None) -> dict:
    """
    Run ethical compliance check before executing an action.
    Implements the 4-step ethical decision model.
    """
    checks = {
        "data_privacy": True,
        "user_consent": True,
        "transparency": True,
        "bias_check": True,
        "proportionality": True,
    }
    concerns = []

    # Check: Is the image data being stored?
    if action == "store_image":
        checks["data_privacy"] = False
        concerns.append("Storing user images violates data minimization principle")

    # Check: Is the user aware of what's happening?
    if context and not context.get("user_informed", True):
        checks["transparency"] = False
        concerns.append("User should be informed of autonomous actions")

    # Check: Is the action proportionate?
    if action == "share_data_externally":
        checks["proportionality"] = False
        concerns.append("External data sharing requires explicit consent")

    all_passed = all(checks.values())

    return {
        "action": action,
        "approved": all_passed,
        "checks": checks,
        "concerns": concerns,
        "timestamp": datetime.now().isoformat(),
    }


def _generate_reasoning(quality: float, content_type: str, confidence: float, 
                         passes: int, autonomy: str) -> str:
    """Generate human-readable reasoning for the selected strategy."""
    parts = []

    parts.append(
        f"Image quality score is {quality:.0f}/100 "
        f"({'good' if quality >= 70 else 'moderate' if quality >= 50 else 'low'})."
    )

    parts.append(
        f"Detected content type: {content_type} "
        f"(confidence: {confidence:.0%})."
    )

    if passes == 1:
        parts.append("Quality is sufficient for single-pass transcription.")
    else:
        parts.append(
            f"Using {passes}-pass approach for better accuracy."
        )

    if autonomy == "full":
        parts.append("Proceeding with full autonomy — high confidence in results.")
    elif autonomy == "semi":
        parts.append("Semi-autonomous mode — will present results for optional review.")
    else:
        parts.append("Human review recommended — quality below confidence threshold.")

    return " ".join(parts)
