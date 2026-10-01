"""System-wide accessibility and WCAG constants."""
MIN_CONTRAST_NORMAL_TEXT = 4.5
MIN_CONTRAST_LARGE_TEXT = 3.0
ENHANCED_CONTRAST_RATIO = 7.0

MAX_COGNITIVE_WORDS_PER_SENTENCE = 22
OPTIMAL_READING_LINE_HEIGHT = 1.5
MIN_RECOMMENDED_FONT_PX = 16

WCAG_RULES = {
    "1.1.1": {"name": "Non-text Content", "level": "A", "principle": "perceivable"},
    "1.3.1": {"name": "Info and Relationships", "level": "A", "principle": "perceivable"},
    "1.4.3": {"name": "Contrast (Minimum)", "level": "AA", "principle": "perceivable"},
    "1.4.6": {"name": "Contrast (Enhanced)", "level": "AAA", "principle": "perceivable"},
    "2.4.6": {"name": "Headings and Labels", "level": "AA", "principle": "operable"},
    "3.1.5": {"name": "Reading Level", "level": "AAA", "principle": "understandable"},
}
