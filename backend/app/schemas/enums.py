"""Readability and educational level enums."""
from enum import Enum

class ReadabilityGradeBand(str, Enum):
    EARLY_PRIMARY = "early_primary"    # Grades 1-3
    UPPER_PRIMARY = "upper_primary"    # Grades 4-5
    MIDDLE_SCHOOL = "middle_school"    # Grades 6-8
    HIGH_SCHOOL = "high_school"        # Grades 9-12
    COLLEGE = "college"                # Undergraduate
    ACADEMIC_EXPERT = "academic_expert" # Post-grad / Scholarly

class CEFRLevel(str, Enum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"
