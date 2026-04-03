# engine.py
# Master scoring function — imports all 4 dimension scorers
# and combines them into one final weighted score.

from scoring.naming_conventions    import score_naming_conventions
from scoring.missing_descriptions  import score_missing_descriptions
from scoring.calculation_structure import score_calculation_structure
from scoring.metadata_completeness import score_metadata_completeness

WEIGHTS = {
    "naming_conventions":    25,
    "missing_descriptions":  30,
    "calculation_structure": 20,
    "metadata_completeness": 25,
}

def score_report(report):
    naming_score,      naming_issues      = score_naming_conventions(report)
    description_score, description_issues = score_missing_descriptions(report)
    calculation_score, calculation_issues = score_calculation_structure(report)
    metadata_score,    metadata_issues    = score_metadata_completeness(report)

    final_score = round(
        (naming_score      * WEIGHTS["naming_conventions"]    / 100) +
        (description_score * WEIGHTS["missing_descriptions"]  / 100) +
        (calculation_score * WEIGHTS["calculation_structure"] / 100) +
        (metadata_score    * WEIGHTS["metadata_completeness"] / 100)
    )

    return {
        "report_id":   report["report_id"],
        "report_name": report["report_name"],
        "workspace":   report["workspace"],
        "final_score": final_score,
        "dimensions": {
            "naming_conventions":    {"score": naming_score,      "issues": naming_issues},
            "missing_descriptions":  {"score": description_score, "issues": description_issues},
            "calculation_structure": {"score": calculation_score, "issues": calculation_issues},
            "metadata_completeness": {"score": metadata_score,    "issues": metadata_issues},
        }
    }


def score_all_reports(reports):
    results = [score_report(r) for r in reports]
    results.sort(key=lambda x: x["final_score"])
    return results