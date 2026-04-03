# calculation_structure.py
# Checks if DAX expressions are simple enough for Copilot to reason over.

import re

def score_calculation_structure(report):
    measures = report.get("measures", [])

    if not measures:
        return 50, []

    issues = []
    complex_count = 0

    for measure in measures:
        expression = measure.get("expression", "")
        name = measure["name"]
        problems = []

        if len(expression) > 150:
            problems.append(
                f"'{name}' has a very long expression ({len(expression)} chars) "
                f"— consider breaking it into smaller measures"
            )

        if expression.upper().count("CALCULATE") > 1:
            problems.append(
                f"'{name}' has nested CALCULATE statements "
                f"— Copilot struggles with these"
            )

        if "ALLEXCEPT" in expression.upper() or expression.upper().count("ALL(") > 1:
            problems.append(
                f"'{name}' uses complex filter removal "
                f"— add a description explaining its intent"
            )

        if re.search(r'\[x\d', expression):
            problems.append(
                f"'{name}' references cryptically named measures "
                f"— rename dependencies first"
            )

        if problems:
            complex_count += 1
            issues.extend(problems)

    clean_ratio = 1 - (complex_count / len(measures))
    score = round(clean_ratio * 100)

    return score, issues