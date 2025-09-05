# backend/utils/score_calculator.py

import re


def calculate_match_score_from_feedback(ai_feedback: str, years_match: bool) -> int:
    """
    Estimate match score from AI feedback text
    """
    feedback = ai_feedback.lower()

    # Start with base score
    score = 70  # base

    # Adjust for experience
    if years_match:
        score += 15
    else:
        score -= 20

    # Penalize for missing keywords
    penalties = {
        "missing": -10,
        "not mentioned": -8,
        "not found": -8,
        "absent": -10,
        "lack": -10,
        "without": -6,
    }

    for keyword, penalty in penalties.items():
        count = feedback.count(keyword)
        score += penalty * count

    # Bonus for strong positives
    bonuses = {
        "exceeds": 10,
        "strong fit": 12,
        "excellent match": 15,
        "highly qualified": 10,
    }

    for keyword, bonus in bonuses.items():
        if keyword in feedback:
            score += bonus

    # Normalize
    score = max(0, min(100, score))

    # If no clear feedback, fallback
    if score == 70 and "missing" not in feedback and "lack" not in feedback:
        # Assume medium-high fit
        score = 85 if years_match else 60

    return int(score)
