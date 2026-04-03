# naming_conventions.py
# Checks if measure and column names are human-readable for Copilot.

import re

def score_naming_conventions(report):
    all_names = []

    for measure in report.get("measures", []):
        all_names.append(measure["name"])

    for column in report.get("columns", []):
        all_names.append(column["name"])

    if not all_names:
        return 50, []

    issues = []
    bad_count = 0

    for name in all_names:
        problems = []

        if len(name) <= 3:
            problems.append(f"'{name}' is too short — likely an abbreviation Copilot won't understand")

        if "_" in name:
            problems.append(f"'{name}' uses underscores — consider spaces or Title Case")

        if name.isupper() and len(name) > 3:
            problems.append(f"'{name}' is all uppercase — use Title Case instead")

        if re.search(r'(v\d|final|temp|old|draft|new|test)', name.lower()):
            problems.append(f"'{name}' contains a version or temp suffix — clean up the name")

        if problems:
            bad_count += 1
            issues.extend(problems)

    clean_ratio = 1 - (bad_count / len(all_names))
    score = round(clean_ratio * 100)

    return score, issues