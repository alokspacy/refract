from typing import Dict, List, Optional
from app.profiles.base import BaseProfile
from app.profiles.dyslexia import DyslexiaProfile
from app.profiles.cognitive import CognitiveProfile
from app.profiles.visual import VisualBasicProfile


class ProfileRegistry:
    """
    Registry for managing available accessibility profiles and resolving precedence.
    """

    def __init__(self):
        self._profiles: Dict[str, BaseProfile] = {
            "dyslexia": DyslexiaProfile(),
            "cognitive": CognitiveProfile(),
            "visual_basic": VisualBasicProfile(),
            "visual": VisualBasicProfile(),  # Alias
        }
        # Precedence order when resolving conflicting transformations
        self._precedence_order = ["cognitive", "dyslexia", "visual_basic"]

    def get_profile(self, profile_id: str) -> Optional[BaseProfile]:
        """Retrieve profile by ID."""
        return self._profiles.get(profile_id.lower())

    def list_profiles(self) -> List[BaseProfile]:
        """List distinct implemented profiles."""
        distinct_ids = ["dyslexia", "cognitive", "visual_basic"]
        return [self._profiles[pid] for pid in distinct_ids if pid in self._profiles]

    def resolve_precedence(self, profile_ids: List[str]) -> List[str]:
        """Sort profile IDs according to deterministic precedence rules."""
        cleaned = [p.lower() for p in profile_ids if p.lower() in self._profiles]
        # Sort based on established precedence order
        return sorted(list(set(cleaned)), key=lambda p: self._precedence_order.index(p) if p in self._precedence_order else 99)


_profile_registry_instance = ProfileRegistry()


def get_profile_registry() -> ProfileRegistry:
    return _profile_registry_instance
