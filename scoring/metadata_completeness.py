# metadata_completeness.py
# Checks for empty pages, inactive relationships, and legacy tables.

import re

def score_metadata_completeness(report):
    issues = []
    deductions = 0
    max_deductions = 10

    for page in report.get("pages", []):
        if page.get("visuals_count", 0) == 0:
            deductions += 1.5
            issues.append(
                f"Page '{page['name']}' has no visuals "
                f"— consider removing it to reduce model noise"
            )

    for rel in report.get("relationships", []):
        if not rel.get("active", True):
            deductions += 1.5
            issues.append(
                f"Inactive relationship between '{rel['from_table']}' and "
                f"'{rel['to_table']}' — remove if unused"
            )

    for rel in report.get("relationships", []):
        for table in [rel["from_table"], rel["to_table"]]:
            if re.search(r'(legacy|old|temp|draft|archive)', table.lower()):
                deductions += 1
                issues.append(
                    f"Table '{table}' has a legacy or temp name "
                    f"— review if still needed"
                )

    score = max(0, round(100 - (deductions / max_deductions * 100)))

    return score, issues