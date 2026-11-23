import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mentorship_matcher.models import Profile, load_profile
from mentorship_matcher.scoring import (
    compatibility,
    rank_matches,
    skill_overlap,
    interest_overlap,
)


def test_skill_overlap():
    a = Profile("A", "mentor", skills=["python", "data"])
    b = Profile("B", "learner", skills=["python", "web"])
    assert skill_overlap(a, b) == 1.0 / 3.0  # 1 common / 3 union


def test_skill_overlap_empty():
    a = Profile("A", "mentor", skills=[])
    b = Profile("B", "learner", skills=["python"])
    assert skill_overlap(a, b) == 0.0


def test_interest_overlap():
    a = Profile("A", "mentor", interests=["ai", "edu"])
    b = Profile("B", "learner", interests=["ai", "web"])
    assert interest_overlap(a, b) == 1.0 / 3.0


def test_compatibility_range():
    a = Profile("A", "mentor", skills=["python"], interests=["ai"], availability="weekends", experience_years=5)
    b = Profile("B", "learner", skills=["python"], interests=["ai"], availability="weekends", experience_years=0)
    score = compatibility(a, b)
    assert 0 <= score <= 100


def test_rank_matches_top_n():
    mentors = [
        Profile("M1", "mentor", skills=["python"], interests=["ai"], availability="weekends", experience_years=5),
        Profile("M2", "mentor", skills=["web"], interests=["web"], availability="weekdays", experience_years=3),
    ]
    learner = Profile("L1", "learner", skills=["python"], interests=["ai"], availability="weekends", experience_years=0)
    matches = rank_matches(mentors, learner, top_n=1)
    assert len(matches) == 1
    assert matches[0][0].name == "M1"


def test_no_mentors():
    learner = Profile("L1", "learner", skills=["python"], interests=["ai"], availability="weekends", experience_years=0)
    matches = rank_matches([], learner, top_n=3)
    assert matches == []


def test_ties_deterministic():
    mentors = [
        Profile("Zeta", "mentor", skills=["python"], interests=["ai"], availability="weekends", experience_years=5),
        Profile("Alpha", "mentor", skills=["python"], interests=["ai"], availability="weekends", experience_years=5),
    ]
    learner = Profile("L1", "learner", skills=["python"], interests=["ai"], availability="weekends", experience_years=0)
    matches = rank_matches(mentors, learner, top_n=2)
    assert matches[0][0].name == "Alpha"  # alphabetical tiebreak
