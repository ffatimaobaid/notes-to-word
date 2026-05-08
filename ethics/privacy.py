"""
Privacy Module — Data Handling, Consent & Minimization

Implements privacy-by-design principles:
- Images are processed in memory only — never stored on disk
- User consent is tracked before processing
- Data minimization: only extract what's needed
- GDPR-aligned data lifecycle management
- PECA 2016 awareness for Pakistan-specific compliance
"""

from datetime import datetime

# Privacy policy configuration
PRIVACY_POLICY = {
    "data_retention": "session_only",
    "image_storage": False,
    "text_storage": "user_consent_required",
    "analytics_data": "anonymized_only",
    "third_party_sharing": False,
    "api_data_policy": "Google Gemini processes images for transcription only. "
                       "No images are stored by our application.",
}

# Data handling actions and their compliance status
COMPLIANT_ACTIONS = {
    "transcribe": True,       # Processing image for transcription — legitimate purpose
    "store_image": False,      # Storing raw images — violates minimization
    "store_result": True,      # Storing text result (with consent) — okay
    "share_external": False,   # Sharing data externally — needs explicit consent
    "analytics": True,         # Anonymized usage analytics — legitimate interest
    "feedback": True,          # Storing feedback scores — legitimate interest
}


def check_data_handling_compliance(action: str) -> dict:
    """
    Check if a data handling action is compliant with privacy policy.
    
    Returns:
        dict with compliant status, reasoning, and applicable regulations
    """
    is_compliant = COMPLIANT_ACTIONS.get(action, False)

    applicable_laws = []
    reasoning = ""

    if action == "transcribe":
        applicable_laws = ["GDPR Art. 6(1)(a) - Consent", "PECA 2016 S.3 - Data Protection"]
        reasoning = ("Image is processed for transcription as requested by user. "
                     "No persistent storage. Compliant with data minimization.")

    elif action == "store_image":
        applicable_laws = ["GDPR Art. 5(1)(c) - Data Minimization", "PECA 2016 S.3"]
        reasoning = ("Storing raw user images is unnecessary for the core function. "
                     "Violates data minimization principle.")

    elif action == "store_result":
        applicable_laws = ["GDPR Art. 6(1)(a) - Consent"]
        reasoning = ("Text results can be stored with explicit user consent. "
                     "Download option gives user control over their data.")

    elif action == "share_external":
        applicable_laws = ["GDPR Art. 44-49 - International Transfers", "PECA 2016 S.36"]
        reasoning = ("Sharing user data with external parties requires explicit, "
                     "informed consent and data protection assessment.")

    elif action == "analytics":
        applicable_laws = ["GDPR Art. 6(1)(f) - Legitimate Interest"]
        reasoning = ("Anonymized usage statistics for system improvement. "
                     "No personal data is retained.")

    elif action == "feedback":
        applicable_laws = ["GDPR Art. 6(1)(f) - Legitimate Interest"]
        reasoning = ("Feedback scores are anonymized and used for system improvement only.")

    return {
        "action": action,
        "compliant": is_compliant,
        "reasoning": reasoning,
        "applicable_laws": applicable_laws,
        "timestamp": datetime.now().isoformat(),
    }


def get_privacy_policy() -> dict:
    """Return the current privacy policy configuration."""
    return PRIVACY_POLICY.copy()


def get_data_lifecycle() -> list:
    """
    Return the data lifecycle stages for transparency.
    Shows what happens to user data at each stage.
    """
    return [
        {
            "stage": "Upload",
            "data": "Image file",
            "action": "Loaded into memory (RAM only)",
            "retention": "Session duration",
            "stored_on_disk": False,
        },
        {
            "stage": "Analysis",
            "data": "Image pixels",
            "action": "Quality metrics extracted (numeric only)",
            "retention": "Session duration",
            "stored_on_disk": False,
        },
        {
            "stage": "Transcription",
            "data": "Image → Text",
            "action": "Sent to Gemini API via encrypted HTTPS",
            "retention": "Per Google's API data policy",
            "stored_on_disk": False,
        },
        {
            "stage": "Output",
            "data": "Transcribed text",
            "action": "Displayed to user, Word doc generated in memory",
            "retention": "Session duration (user downloads copy)",
            "stored_on_disk": False,
        },
        {
            "stage": "Feedback",
            "data": "Rating (1-5) + anonymized metadata",
            "action": "Stored in local JSON for learning",
            "retention": "Persistent (no personal data)",
            "stored_on_disk": True,
        },
        {
            "stage": "Session End",
            "data": "All image/text data",
            "action": "Garbage collected — no trace remains",
            "retention": "0",
            "stored_on_disk": False,
        },
    ]


def generate_consent_text() -> str:
    """Generate user consent text for display."""
    return (
        "By uploading an image, you consent to the following:\n"
        "• Your image will be sent to Google Gemini API for transcription\n"
        "• The image is processed in memory only — never saved to our servers\n"
        "• Anonymized usage statistics may be collected for system improvement\n"
        "• You can download your results and we retain no copy\n"
        "• Your feedback ratings are stored anonymously to improve the system\n\n"
        "We comply with GDPR data minimization principles and PECA 2016."
    )
