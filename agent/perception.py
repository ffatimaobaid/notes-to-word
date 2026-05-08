"""
Perception Module — Image Analysis & Content Detection

Analyzes uploaded images to determine:
- Image quality (blur, lighting, contrast, resolution)
- Content types present (text, math, diagrams, mixed)
- Confidence scores for each detection
- Recommended pre-processing steps
"""

from PIL import Image, ImageStat, ImageFilter
import math


def analyze_image_quality(image: Image.Image) -> dict:
    """
    Perform comprehensive image quality analysis.
    Returns quality metrics and an overall quality score (0-100).
    """
    # Convert to grayscale for analysis
    gray = image.convert("L")
    stat = ImageStat.Stat(gray)

    # 1. Brightness analysis
    mean_brightness = stat.mean[0]
    brightness_score = _score_brightness(mean_brightness)

    # 2. Contrast analysis
    std_dev = stat.stddev[0]
    contrast_score = _score_contrast(std_dev)

    # 3. Sharpness / blur detection (Laplacian variance approximation)
    sharpness_score = _score_sharpness(gray)

    # 4. Resolution analysis
    width, height = image.size
    resolution_score = _score_resolution(width, height)

    # 5. Overall quality score (weighted average)
    overall = (
        brightness_score * 0.2
        + contrast_score * 0.25
        + sharpness_score * 0.35
        + resolution_score * 0.2
    )

    quality_label = _quality_label(overall)

    return {
        "brightness": {
            "value": round(mean_brightness, 1),
            "score": round(brightness_score, 1),
            "status": "good" if brightness_score > 60 else "poor",
        },
        "contrast": {
            "value": round(std_dev, 1),
            "score": round(contrast_score, 1),
            "status": "good" if contrast_score > 60 else "poor",
        },
        "sharpness": {
            "score": round(sharpness_score, 1),
            "status": "good" if sharpness_score > 60 else "poor",
        },
        "resolution": {
            "width": width,
            "height": height,
            "megapixels": round((width * height) / 1_000_000, 2),
            "score": round(resolution_score, 1),
            "status": "good" if resolution_score > 60 else "poor",
        },
        "overall_score": round(overall, 1),
        "quality_label": quality_label,
    }


def detect_content_type(image: Image.Image) -> dict:
    """
    Heuristic-based content type detection.
    Returns likely content types and confidence scores.

    In a fully agentic system, this would use a trained classifier.
    Here we use image statistics as heuristic indicators.
    """
    gray = image.convert("L")
    stat = ImageStat.Stat(gray)

    # Edge density as proxy for content complexity
    edges = gray.filter(ImageFilter.FIND_EDGES)
    edge_stat = ImageStat.Stat(edges)
    edge_density = edge_stat.mean[0]

    # Variance indicates content diversity
    variance = stat.var[0]

    # Heuristic classification
    has_text = edge_density > 5  # Text creates moderate edges
    has_math = variance > 2000   # Math symbols create high variance
    has_diagram = edge_density > 20  # Diagrams have strong edges

    if has_diagram and has_text:
        primary_type = "mixed"
        confidence = 0.7
    elif has_math and has_text:
        primary_type = "math"
        confidence = 0.65
    elif has_diagram:
        primary_type = "diagram"
        confidence = 0.6
    else:
        primary_type = "text"
        confidence = 0.8

    return {
        "primary_type": primary_type,
        "confidence": round(confidence, 2),
        "indicators": {
            "text_likely": has_text,
            "math_likely": has_math,
            "diagram_likely": has_diagram,
            "edge_density": round(edge_density, 2),
            "content_variance": round(variance, 2),
        },
    }


def get_preprocessing_recommendations(quality: dict) -> list:
    """
    Based on quality analysis, recommend preprocessing steps.
    The agent uses these to decide actions autonomously.
    """
    recommendations = []

    if quality["brightness"]["score"] < 50:
        if quality["brightness"]["value"] < 100:
            recommendations.append({
                "action": "increase_brightness",
                "reason": "Image is too dark for reliable OCR",
                "priority": "high",
            })
        else:
            recommendations.append({
                "action": "decrease_brightness",
                "reason": "Image is overexposed",
                "priority": "medium",
            })

    if quality["contrast"]["score"] < 50:
        recommendations.append({
            "action": "enhance_contrast",
            "reason": "Low contrast may cause character misrecognition",
            "priority": "high",
        })

    if quality["sharpness"]["score"] < 50:
        recommendations.append({
            "action": "sharpen_image",
            "reason": "Blurry image will reduce transcription accuracy",
            "priority": "high",
        })

    if quality["resolution"]["score"] < 50:
        recommendations.append({
            "action": "upscale_image",
            "reason": "Low resolution may lose fine details like subscripts",
            "priority": "medium",
        })

    if not recommendations:
        recommendations.append({
            "action": "none",
            "reason": "Image quality is sufficient for processing",
            "priority": "none",
        })

    return recommendations


# --- Private helper functions ---

def _score_brightness(mean: float) -> float:
    """Score brightness on 0-100 scale. Optimal range: 100-180."""
    if 100 <= mean <= 180:
        return 100.0
    elif mean < 100:
        return max(0, mean)
    else:
        return max(0, 100 - (mean - 180) * 2)


def _score_contrast(std: float) -> float:
    """Score contrast on 0-100 scale. Optimal range: 40-80."""
    if 40 <= std <= 80:
        return 100.0
    elif std < 40:
        return max(0, std * 2.5)
    else:
        return max(0, 100 - (std - 80))


def _score_sharpness(gray_image: Image.Image) -> float:
    """Estimate sharpness using edge detection variance."""
    edges = gray_image.filter(ImageFilter.FIND_EDGES)
    stat = ImageStat.Stat(edges)
    edge_variance = stat.var[0]
    # Normalize: higher variance = sharper (cap at 100)
    score = min(100, edge_variance / 10)
    return score


def _score_resolution(width: int, height: int) -> float:
    """Score resolution. >= 1MP is good, >= 2MP is excellent."""
    megapixels = (width * height) / 1_000_000
    if megapixels >= 2:
        return 100.0
    elif megapixels >= 1:
        return 80.0
    elif megapixels >= 0.5:
        return 60.0
    elif megapixels >= 0.3:
        return 40.0
    else:
        return 20.0


def _quality_label(score: float) -> str:
    """Convert numeric score to human-readable label."""
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Fair"
    elif score >= 20:
        return "Poor"
    else:
        return "Very Poor"
