# missing_descriptions.py
# Checks if measures and columns have descriptions for Copilot to use.

def score_missing_descriptions(report):
    all_items = []

    for measure in report.get("measures", []):
        all_items.append(("measure", measure["name"], measure.get("description", "")))

    for column in report.get("columns", []):
        all_items.append(("column", column["name"], column.get("description", "")))

    if not all_items:
        return 50, []

    issues = []
    missing_count = 0

    for item_type, name, description in all_items:
        if not description or not description.strip():
            missing_count += 1
            issues.append(
                f"{item_type.capitalize()} '{name}' has no description "
                f"— Copilot will guess its purpose"
            )

    filled_ratio = 1 - (missing_count / len(all_items))
    score = round(filled_ratio * 100)

    return score, issues