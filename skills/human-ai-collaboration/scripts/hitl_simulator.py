#!/usr/bin/env python3
"""
hitl_simulator.py

Simulates a human-in-the-loop review queue to test whether reviewer capacity
matches the expected review volume at a given automation level.

Use this during Alpha to validate that the HITL Map is feasible before
committing to a review process in Beta.

This is pseudocode demonstrating the pattern. Adapt for your specific
volume estimates, SLAs, and reviewer capacity.

Usage:
    python hitl_simulator.py --volume 200 --reviewers 2 --review-time 60 --sla-minutes 240
    python hitl_simulator.py --config hitl-config.json --days 5
"""

import argparse
import math
import random
import sys
from dataclasses import dataclass, field


@dataclass
class ReviewItem:
    item_id: str
    submitted_at: float
    reviewed_at: object = None  # float or None
    reviewer_id: object = None  # str or None
    sla_minutes: float = 240.0
    priority: str = "normal"

    @property
    def wait_time(self):
        if self.reviewed_at is None:
            return None
        return self.reviewed_at - self.submitted_at

    @property
    def sla_met(self):
        if self.wait_time is None:
            return None
        return self.wait_time <= self.sla_minutes


@dataclass
class Reviewer:
    reviewer_id: str
    hours_per_day: float = 7.5
    review_time_minutes: float = 5.0
    available_from_minute: float = 0.0

    @property
    def capacity_per_day(self):
        return (self.hours_per_day * 60) / self.review_time_minutes


def simulate_queue(daily_volume, reviewers, sla_minutes, simulation_days=5, priority_fraction=0.1, seed=42):
    """Simulate a HITL review queue over N days."""
    random.seed(seed)
    WORK_DAY_MINUTES = 540  # 9-hour window

    all_items = []
    item_counter = 0

    for day in range(simulation_days):
        day_start = day * WORK_DAY_MINUTES
        for _ in range(daily_volume):
            item_counter += 1
            arrival = day_start + random.uniform(0, WORK_DAY_MINUTES)
            priority = "priority" if random.random() < priority_fraction else "normal"
            all_items.append(ReviewItem(
                item_id=f"item-{item_counter:04d}",
                submitted_at=arrival,
                sla_minutes=sla_minutes,
                priority=priority,
            ))

    all_items.sort(key=lambda i: (i.submitted_at, 0 if i.priority == "priority" else 1))

    for reviewer in reviewers:
        reviewer.available_from_minute = 0.0

    unreviewed = list(all_items)

    while unreviewed:
        reviewer = min(reviewers, key=lambda r: r.available_from_minute)

        next_item = None
        for item in unreviewed:
            if item.submitted_at <= reviewer.available_from_minute:
                next_item = item
                break

        if next_item is None:
            if unreviewed:
                next_item = unreviewed[0]
                reviewer.available_from_minute = next_item.submitted_at
            else:
                break

        unreviewed.remove(next_item)
        start_review = max(reviewer.available_from_minute, next_item.submitted_at)
        end_review = start_review + reviewer.review_time_minutes

        next_item.reviewed_at = end_review
        next_item.reviewer_id = reviewer.reviewer_id
        reviewer.available_from_minute = end_review

    reviewed = [i for i in all_items if i.reviewed_at is not None]
    unreviewed_final = [i for i in all_items if i.reviewed_at is None]
    sla_met = [i for i in reviewed if i.sla_met]
    wait_times = [i.wait_time for i in reviewed if i.wait_time is not None]

    total_capacity = sum(r.capacity_per_day * simulation_days for r in reviewers)

    sla_pct = (len(sla_met) / len(reviewed) * 100) if reviewed else 0

    if unreviewed_final:
        status = "CAPACITY_ISSUE"
        recommendation = f"{len(unreviewed_final)} items not reviewed. Increase reviewer capacity or automation level."
    elif sla_pct < 80:
        status = "SLA_RISK"
        recommendation = f"Only {sla_pct:.0f}% SLA compliance. Consider more reviewers, faster review, or higher automation level."
    elif sla_pct < 95:
        status = "MARGINAL"
        recommendation = f"{sla_pct:.0f}% SLA compliance. Acceptable but leaves little buffer."
    else:
        status = "OK"
        recommendation = f"{sla_pct:.0f}% SLA compliance. Review process is feasible."

    return {
        "simulation": {
            "days": simulation_days,
            "daily_volume": daily_volume,
            "total_items": len(all_items),
            "reviewer_count": len(reviewers),
            "sla_minutes": sla_minutes,
        },
        "capacity": {
            "total_capacity": round(total_capacity),
            "utilisation_pct": round(len(all_items) / total_capacity * 100, 1) if total_capacity > 0 else 0,
        },
        "results": {
            "reviewed": len(reviewed),
            "unreviewed_at_end": len(unreviewed_final),
            "sla_met_pct": round(sla_pct, 1),
            "avg_wait_minutes": round(sum(wait_times) / len(wait_times), 1) if wait_times else 0,
            "p95_wait_minutes": round(sorted(wait_times)[int(len(wait_times) * 0.95)], 1) if wait_times else 0,
        },
        "assessment": {"status": status, "recommendation": recommendation},
    }


def main():
    parser = argparse.ArgumentParser(description="Simulate HITL review queue capacity")
    parser.add_argument("--volume", type=int, default=100)
    parser.add_argument("--reviewers", type=int, default=2)
    parser.add_argument("--review-time", type=float, default=5.0)
    parser.add_argument("--sla-minutes", type=float, default=240.0)
    parser.add_argument("--days", type=int, default=5)
    args = parser.parse_args()

    reviewers = [
        Reviewer(reviewer_id=f"reviewer-{i+1}", review_time_minutes=args.review_time)
        for i in range(args.reviewers)
    ]

    result = simulate_queue(
        daily_volume=args.volume,
        reviewers=reviewers,
        sla_minutes=args.sla_minutes,
        simulation_days=args.days,
    )

    print("\nHITL Queue Simulation Results")
    print("=" * 40)
    print(f"Volume: {result['simulation']['daily_volume']} items/day × {result['simulation']['days']} days")
    print(f"Reviewers: {result['simulation']['reviewer_count']}")
    print(f"SLA: {result['simulation']['sla_minutes']} minutes")
    print(f"\nCapacity utilisation: {result['capacity']['utilisation_pct']}%")
    print(f"SLA compliance: {result['results']['sla_met_pct']}%")
    print(f"Avg wait: {result['results']['avg_wait_minutes']} min")
    print(f"P95 wait: {result['results']['p95_wait_minutes']} min")
    print(f"\nStatus: {result['assessment']['status']}")
    print(f"Recommendation: {result['assessment']['recommendation']}")

    if result["assessment"]["status"] in ("CAPACITY_ISSUE", "SLA_RISK"):
        sys.exit(1)


if __name__ == "__main__":
    main()
