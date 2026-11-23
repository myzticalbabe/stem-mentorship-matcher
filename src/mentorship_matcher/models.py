"""Data models for mentor/learner profiles."""
from dataclasses import dataclass, field
from typing import List


@dataclass
class Profile:
    name: str
    role: str  # "mentor" or "learner"
    skills: List[str] = field(default_factory=list)
    interests: List[str] = field(default_factory=list)
    availability: str = ""
    experience_years: int = 0


def load_profile(data: dict) -> Profile:
    return Profile(
        name=data["name"],
        role=data["role"],
        skills=data.get("skills", []),
        interests=data.get("interests", []),
        availability=data.get("availability", ""),
        experience_years=data.get("experience_years", 0),
    )
