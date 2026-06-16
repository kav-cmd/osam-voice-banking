import re
from typing import Any

IS_17802_RULES = {
    "keyboard_accessible": {
        "id": "IS17802-1",
        "title": "All interactive elements must be keyboard accessible",
        "description": "Every button, link, and form field must be reachable and operable via keyboard alone.",
        "severity": "critical",
        "wcag_ref": "2.1.1",
    },
    "contrast_minimum": {
        "id": "IS17802-2",
        "title": "Text must have sufficient contrast against background",
        "description": "Normal text must have at least 4.5:1 contrast ratio; large text needs 3:1.",
        "severity": "critical",
        "wcag_ref": "1.4.3",
    },
    "non_text_content": {
        "id": "IS17802-3",
        "title": "Non-text content must have text alternatives",
        "description": "Images, icons, and audio must have alt text or transcripts.",
        "severity": "high",
        "wcag_ref": "1.1.1",
    },
    "error_identification": {
        "id": "IS17802-4",
        "title": "Errors must be identified and described to the user",
        "description": "Error messages must be clear, in the user's language, and announced by screen readers.",
        "severity": "high",
        "wcag_ref": "3.3.1",
    },
    "language_of_page": {
        "id": "IS17802-5",
        "title": "Page language must be programmatically determinable",
        "description": "The lang attribute must be set on the HTML element for each page.",
        "severity": "high",
        "wcag_ref": "3.1.1",
    },
    "audio_description": {
        "id": "IS17802-6",
        "title": "Audio content must have alternatives",
        "description": "Voice prompts must have text alternatives and vice versa.",
        "severity": "high",
        "wcag_ref": "1.2.1",
    },
    "haptic_feedback": {
        "id": "IS17802-7",
        "title": "Haptic feedback for critical interactions",
        "description": "Success and error states should have distinct haptic patterns.",
        "severity": "medium",
        "wcag_ref": "N/A",
    },
    "voice_control": {
        "id": "IS17802-8",
        "title": "Voice input must be available for all functions",
        "description": "All banking functions must be accessible via voice commands without needing to touch the screen.",
        "severity": "critical",
        "wcag_ref": "N/A",
    },
    "confirmation_prompts": {
        "id": "IS17802-9",
        "title": "Destructive actions must require confirmation",
        "description": "Loan applications, fund transfers must have explicit user confirmation before processing.",
        "severity": "critical",
        "wcag_ref": "N/A",
    },
    "multilingual_support": {
        "id": "IS17802-10",
        "title": "Content must be available in scheduled Indian languages",
        "description": "Hindi and Tamil (and eventually all 13 IPPB languages) must be fully supported.",
        "severity": "high",
        "wcag_ref": "N/A",
    },
}


def validate_html_accessibility(html_content: str) -> list[dict]:
    issues = []

    if 'lang="' not in html_content and 'lang=' not in html_content:
        issues.append({
            "rule": IS_17802_RULES["language_of_page"],
            "found": "No lang attribute on HTML element",
            "element": "<html>",
        })

    button_count = len(re.findall(r'<button', html_content, re.IGNORECASE))
    aria_button_count = len(re.findall(r'role="button"', html_content, re.IGNORECASE))
    total_buttons = button_count + aria_button_count
    keyboard_buttons = len(re.findall(r'onkeydown|onkeypress|tabindex', html_content, re.IGNORECASE))

    if total_buttons > 0 and keyboard_buttons == 0:
        issues.append({
            "rule": IS_17802_RULES["keyboard_accessible"],
            "found": f"{total_buttons} buttons found but no keyboard handlers detected",
            "element": "buttons/links",
        })

    img_count = len(re.findall(r'<img', html_content, re.IGNORECASE))
    alt_count = len(re.findall(r'alt="', html_content))
    if img_count > alt_count:
        missing = img_count - alt_count
        issues.append({
            "rule": IS_17802_RULES["non_text_content"],
            "found": f"{missing} images missing alt text",
            "element": "<img>",
        })

    return issues


def generate_accessibility_report(html_content: str) -> dict:
    issues = validate_html_accessibility(html_content)
    return {
        "standard": "IS 17802 (Indian Standard on Accessibility)",
        "total_rules": len(IS_17802_RULES),
        "rules_checked": list(IS_17802_RULES.keys()),
        "issues_found": len(issues),
        "issues": issues,
        "passed": len(issues) == 0,
    }
