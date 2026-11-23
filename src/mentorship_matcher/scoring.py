"""Compatibility scoring between mentor and learner profiles."""
from typing import List

from .models import Profile


def skill_overlap(a: Profile, b: Profile) -> float:
    sa = set(s.lower() for s in a.skills)
    sb = set(s.lower() for s in b.skills)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def interest_overlap(a: Profile, b: Profile) -> float:
    ia = set(i.lower() for i in a.interests)
    ib = set(i.lower() for i in b.interests)
    if not ia or not ib:
        return 0.0
    return len(ia & ib) / len(ia | ib)


def availability_match(a: Profile, b: Profile) -> float:
    if not a.availability or not b.availability:
        return 0.0
    return 1.0 if a.availability.lower() == b.availability.lower() else 0.0


def experience_score(mentor: Profile, learner: Profile) -> float:
    if mentor.experience_years <= 0:
        return 0.0
    # More experience is better, capped at 1.0 for 10+ years
    return min(mentor.experience_years / 10.0, 1.0)


def compatibility(mentor: Profile, learner: Profile) -> float:
    """Compute a 0-100 compatibility score."""
    s = skill_overlap(mentor, learner)
    i = interest_overlap(mentor, learner)
    av = availability_match(mentor, learner)
    ex = experience_score(mentor, learner)
    score = (s * 40 + i * 30 + av * 20 + ex * 10)
    return round(score, 2)


def rank_matches(mentors: List[Profile], learner: Profile, top_n: int = 3):
    scored = [(m, compatibility(m, learner)) for m in mentors]
    scored.sort(key=lambda x: (-x[1], x[0].name))
    return scored[:top_n]
