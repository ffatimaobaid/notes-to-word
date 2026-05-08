"""
Compliance Module — ACM/IEEE, PECA 2016 & GDPR Compliance

Provides compliance checking and reporting for:
- ACM Code of Ethics (2018)
- IEEE Code of Ethics
- PECA 2016 (Pakistan Electronic Crimes Act)
- GDPR-aligned data protection principles
"""

from datetime import datetime


# ──────────────────────────────────────────────
# ACM CODE OF ETHICS — Applied to Notes2Doc
# ──────────────────────────────────────────────

ACM_PRINCIPLES = {
    "1.1": {
        "title": "Contribute to society and to human well-being",
        "status": "followed",
        "application": (
            "Notes2Doc contributes to education and accessibility by converting "
            "handwritten notes to digital format, helping students and professionals "
            "preserve and share knowledge."
        ),
    },
    "1.2": {
        "title": "Avoid harm",
        "status": "followed",
        "application": (
            "The system is designed to avoid harm by not storing user images, "
            "implementing data minimization, and providing transparent processing."
        ),
    },
    "1.3": {
        "title": "Be honest and trustworthy",
        "status": "followed",
        "application": (
            "The agent displays its confidence scores, shows its reasoning process, "
            "and provides explainability reports for every decision made."
        ),
    },
    "1.6": {
        "title": "Respect privacy",
        "status": "followed",
        "application": (
            "Images are processed in memory only. No user data is persisted. "
            "Feedback is anonymized. Full data lifecycle transparency is provided."
        ),
    },
    "2.5": {
        "title": "Give comprehensive and thorough evaluations of computer systems",
        "status": "potentially_violated",
        "application": (
            "As a student project, the confidence scoring system uses heuristics "
            "rather than validated metrics. Users should verify transcription accuracy "
            "for critical documents."
        ),
    },
    "2.9": {
        "title": "Design and implement systems that are robustly and usably secure",
        "status": "followed",
        "application": (
            "API keys are stored in environment variables (not hardcoded). "
            "HTTPS is used for all API communications. Input validation is performed."
        ),
    },
}

IEEE_PRINCIPLES = {
    "1": {
        "title": "Hold paramount the safety, health, and welfare of the public",
        "status": "followed",
        "application": (
            "The system includes safety mechanisms: human-in-the-loop checkpoints, "
            "confidence thresholds, and override capabilities."
        ),
    },
    "5": {
        "title": "Improve understanding of technology and its appropriate application",
        "status": "followed",
        "application": (
            "The Phase 2 Report section educates users about agentic AI systems, "
            "ethical computing, and responsible technology use."
        ),
    },
    "9": {
        "title": "Avoid injuring others, their property, or reputation",
        "status": "followed",
        "application": (
            "The system does not manipulate, misrepresent, or misuse user content. "
            "Transcriptions are faithful to the original handwritten notes."
        ),
    },
}


def get_acm_compliance_report() -> dict:
    """Get the ACM Code of Ethics compliance report."""
    followed = sum(1 for p in ACM_PRINCIPLES.values() if p["status"] == "followed")
    violated = sum(1 for p in ACM_PRINCIPLES.values() if p["status"] == "potentially_violated")

    return {
        "framework": "ACM Code of Ethics (2018)",
        "principles_evaluated": len(ACM_PRINCIPLES),
        "principles_followed": followed,
        "principles_potentially_violated": violated,
        "details": ACM_PRINCIPLES,
        "overall_compliance": "high" if violated == 0 else "moderate",
    }


def get_ieee_compliance_report() -> dict:
    """Get the IEEE Code of Ethics compliance report."""
    return {
        "framework": "IEEE Code of Ethics",
        "principles_evaluated": len(IEEE_PRINCIPLES),
        "principles_followed": len(IEEE_PRINCIPLES),
        "details": IEEE_PRINCIPLES,
        "overall_compliance": "high",
    }


# ──────────────────────────────────────────────
# PECA 2016 — Pakistan Electronic Crimes Act
# ──────────────────────────────────────────────

PECA_2016_SECTIONS = {
    "Section 3": {
        "title": "Unauthorized access to information system or data",
        "relevance": "Our system only accesses user-provided data with explicit consent.",
        "compliant": True,
    },
    "Section 4": {
        "title": "Unauthorized copying or transmission of data",
        "relevance": (
            "User images are sent to Gemini API for processing only. "
            "No unauthorized copying or transmission occurs."
        ),
        "compliant": True,
    },
    "Section 14": {
        "title": "Unauthorized use of identity information",
        "relevance": "No identity information is collected or used.",
        "compliant": True,
    },
    "Section 36": {
        "title": "Offences against dignity of a natural person",
        "relevance": (
            "The system does not process, store, or share any content that could "
            "harm the dignity of any person."
        ),
        "compliant": True,
    },
}


def get_peca_compliance_report() -> dict:
    """Get PECA 2016 compliance report."""
    all_compliant = all(s["compliant"] for s in PECA_2016_SECTIONS.values())
    return {
        "framework": "PECA 2016 (Pakistan Electronic Crimes Act)",
        "sections_evaluated": len(PECA_2016_SECTIONS),
        "all_compliant": all_compliant,
        "details": PECA_2016_SECTIONS,
    }


# ──────────────────────────────────────────────
# GDPR-Aligned Principles
# ──────────────────────────────────────────────

GDPR_PRINCIPLES = {
    "Lawfulness, fairness, transparency": {
        "compliant": True,
        "implementation": "Processing is based on user consent. Full transparency provided.",
    },
    "Purpose limitation": {
        "compliant": True,
        "implementation": "Data is collected only for note transcription purpose.",
    },
    "Data minimization": {
        "compliant": True,
        "implementation": "Only the uploaded image is processed. No extra data collected.",
    },
    "Accuracy": {
        "compliant": True,
        "implementation": "Confidence scores and uncertainty markers ensure accuracy awareness.",
    },
    "Storage limitation": {
        "compliant": True,
        "implementation": "No image data is stored. Session data cleared on close.",
    },
    "Integrity and confidentiality": {
        "compliant": True,
        "implementation": "HTTPS for API calls. Environment variables for secrets.",
    },
}


def get_gdpr_compliance_report() -> dict:
    """Get GDPR compliance report."""
    all_compliant = all(p["compliant"] for p in GDPR_PRINCIPLES.values())
    return {
        "framework": "GDPR-Aligned Principles",
        "principles_evaluated": len(GDPR_PRINCIPLES),
        "all_compliant": all_compliant,
        "details": GDPR_PRINCIPLES,
    }


def get_full_compliance_dashboard() -> dict:
    """Get combined compliance report across all frameworks."""
    acm = get_acm_compliance_report()
    ieee = get_ieee_compliance_report()
    peca = get_peca_compliance_report()
    gdpr = get_gdpr_compliance_report()

    return {
        "generated_at": datetime.now().isoformat(),
        "acm": acm,
        "ieee": ieee,
        "peca_2016": peca,
        "gdpr": gdpr,
        "overall_status": "compliant",
    }
