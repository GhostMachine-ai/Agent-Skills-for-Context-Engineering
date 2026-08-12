#!/usr/bin/env python3
"""
drift_detector.py

Statistical drift detection for AI agent production systems.

Compares a current sample of evaluation rubric scores against a historical
baseline to detect model drift, prompt drift, or data drift.

This is pseudocode demonstrating the pattern. Adapt data loading and
storage to your specific infrastructure.

Usage:
    python drift_detector.py --baseline-file baseline.json --current-file current.json
    python drift_detector.py --days 7 --alert-threshold 0.3
"""

import argparse
import json
import math
import sys


def mean(values):
    if not values:
        return 0.0
    return sum(values) / len(values)


def std_dev(values):
    if len(values) < 2:
        return 0.0
    m = mean(values)
    variance = sum((v - m) ** 2 for v in values) / (len(values) - 1)
    return math.sqrt(variance)


def cohen_d(group_a, group_b):
    """Effect size. |d| > 0.5 is medium; > 0.8 is large."""
    if len(group_a) < 2 or len(group_b) < 2:
        return 0.0
    pooled_std = math.sqrt((std_dev(group_a) ** 2 + std_dev(group_b) ** 2) / 2)
    if pooled_std == 0:
        return 0.0
    return (mean(group_a) - mean(group_b)) / pooled_std


def welch_t_significant(group_a, group_b):
    """Returns True if difference is statistically significant (p < ~0.05)."""
    n_a, n_b = len(group_a), len(group_b)
    if n_a < 5 or n_b < 5:
        return False
    mean_diff = mean(group_a) - mean(group_b)
    se = math.sqrt((std_dev(group_a) ** 2 / n_a) + (std_dev(group_b) ** 2 / n_b))
    if se == 0:
        return False
    return abs(mean_diff / se) > 2.0


def analyse_dimension(dimension, baseline_scores, current_scores, alert_threshold):
    baseline_mean = mean(baseline_scores)
    current_mean = mean(current_scores)
    delta = current_mean - baseline_mean
    is_significant = welch_t_significant(baseline_scores, current_scores)
    effect_size = cohen_d(baseline_scores, current_scores)
    alert = abs(delta) >= alert_threshold and is_significant

    return {
        "dimension": dimension,
        "baseline_mean": round(baseline_mean, 3),
        "current_mean": round(current_mean, 3),
        "delta": round(delta, 3),
        "baseline_n": len(baseline_scores),
        "current_n": len(current_scores),
        "statistically_significant": is_significant,
        "effect_size_cohen_d": round(effect_size, 3),
        "alert": alert,
        "direction": "degraded" if delta < -alert_threshold else "improved" if delta > alert_threshold else "stable",
    }


def detect_drift(baseline, current, alert_threshold=0.3):
    """
    Detect drift across all rubric dimensions.

    Args:
        baseline: dict mapping dimension name -> list of historical scores
        current: dict mapping dimension name -> list of recent scores
        alert_threshold: minimum score delta to trigger an alert (default 0.3)
    """
    dimensions = set(baseline.keys()) | set(current.keys())
    analyses = {}
    alerts = []

    for dim in sorted(dimensions):
        b_scores = baseline.get(dim, [])
        c_scores = current.get(dim, [])

        if not b_scores or not c_scores:
            analyses[dim] = {"error": "insufficient data for comparison"}
            continue

        result = analyse_dimension(dim, b_scores, c_scores, alert_threshold)
        analyses[dim] = result

        if result["alert"]:
            alerts.append({
                "dimension": dim,
                "delta": result["delta"],
                "direction": result["direction"],
                "severity": "high" if abs(result["delta"]) >= alert_threshold * 2 else "medium",
            })

    return {
        "summary": {
            "total_dimensions": len(dimensions),
            "dimensions_with_alerts": len(alerts),
            "overall_status": "ALERT" if alerts else "OK",
        },
        "dimensions": analyses,
        "alerts": alerts,
    }


def load_scores_from_file(path):
    """
    Load evaluation scores from a JSON file.
    Expected format: {"accuracy": [4.2, 3.8, ...], "completeness": [3.9, ...]}
    """
    with open(path) as f:
        return json.load(f)


def render_report(result):
    lines = [
        "Drift Detection Report",
        "=" * 40,
        f"Status: {result['summary']['overall_status']}",
        f"Dimensions with alerts: {result['summary']['dimensions_with_alerts']} / {result['summary']['total_dimensions']}",
        "",
    ]

    if result["alerts"]:
        lines.append("ALERTS:")
        for alert in result["alerts"]:
            lines.append(f"  [{alert['severity'].upper()}] {alert['dimension']}: {alert['delta']:+.3f} ({alert['direction']})")
        lines.append("")

    lines.append("Dimension Details:")
    for dim, analysis in result["dimensions"].items():
        if "error" in analysis:
            lines.append(f"  {dim}: {analysis['error']}")
        else:
            status = "ALERT" if analysis["alert"] else "ok"
            lines.append(
                f"  {dim}: baseline={analysis['baseline_mean']:.2f} current={analysis['current_mean']:.2f} "
                f"delta={analysis['delta']:+.3f} [{status}]"
            )

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Detect drift in AI agent evaluation scores")
    parser.add_argument("--baseline-file", required=True, help="JSON file with baseline scores")
    parser.add_argument("--current-file", required=True, help="JSON file with current scores")
    parser.add_argument("--alert-threshold", type=float, default=0.3)
    parser.add_argument("--output-json", action="store_true")
    args = parser.parse_args()

    baseline = load_scores_from_file(args.baseline_file)
    current = load_scores_from_file(args.current_file)
    result = detect_drift(baseline, current, alert_threshold=args.alert_threshold)

    if args.output_json:
        print(json.dumps(result, indent=2))
    else:
        print(render_report(result))

    if result["summary"]["overall_status"] == "ALERT":
        sys.exit(1)


if __name__ == "__main__":
    main()
