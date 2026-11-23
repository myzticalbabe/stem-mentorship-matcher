"""CLI for mentorship matcher."""
import argparse
import json
import sys

import yaml

from .models import load_profile
from .scoring import rank_matches


def load_profiles(path: str):
    with open(path) as f:
        data = yaml.safe_load(f)
    return [load_profile(p) for p in data]


def main(argv=None):
    parser = argparse.ArgumentParser(description="Mentorship Matcher")
    parser.add_argument("--mentors", required=True, help="YAML file of mentor profiles")
    parser.add_argument("--learners", required=True, help="YAML file of learner profiles")
    parser.add_argument("--top", type=int, default=3, help="Number of top matches")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args(argv)

    mentors = load_profiles(args.mentors)
    learners = load_profiles(args.learners)

    results = {}
    for learner in learners:
        matches = rank_matches(mentors, learner, args.top)
        results[learner.name] = [
            {"mentor": m.name, "score": s} for m, s in matches
        ]

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for learner_name, matches in results.items():
            print(f"\n{learner_name}:")
            if not matches:
                print("  No mentors available.")
            for m in matches:
                print(f"  {m['mentor']} — score {m['score']}")


if __name__ == "__main__":
    main()
