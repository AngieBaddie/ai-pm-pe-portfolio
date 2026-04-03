# recommendations.py
# Uses Claude to turn raw scoring issues into plain English explanations
# and specific fix recommendations for each report.

import anthropic
import os
from dotenv import load_dotenv

# Load your API key from the .env file
load_dotenv()

# Set up the Claude client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def get_recommendations(report_name, dimension, issues):
    """
    Takes a list of issues found in a report and asks Claude to:
    1. Explain why each issue matters for Copilot in plain English
    2. Give a specific, actionable fix for each one
    """

    if not issues:
        return "No issues found in this dimension. This area is Copilot-ready."

    # Format the issues into a clean list for Claude
    issues_text = "\n".join([f"- {issue}" for issue in issues])

    prompt = f"""You are an expert in Microsoft Power BI and Power BI Copilot.

A report called "{report_name}" has been scanned for AI readiness.
The following issues were found in the "{dimension}" dimension:

{issues_text}

For each issue:
1. Explain in one plain English sentence why this specific issue causes Copilot to underperform
2. Give a specific, actionable fix the developer can apply today

Be concise, practical, and speak directly to a BI developer.
Format your response as a simple numbered list matching the issues above.
Do not use jargon. Do not repeat the issue back — just explain and fix."""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text


def get_report_summary(report_name, final_score, dimensions):
    """
    Generates a one-paragraph executive summary for the report —
    what's wrong, how serious it is, and where to start.
    """

    # Build a summary of dimension scores to give Claude context
    dimension_summary = "\n".join([
        f"- {dim}: {data['score']}/100 ({len(data['issues'])} issues)"
        for dim, data in dimensions.items()
    ])

    prompt = f"""You are an expert in Microsoft Power BI Copilot readiness.

A Power BI report called "{report_name}" has been scanned.
Overall AI Readiness Score: {final_score}/100

Dimension scores:
{dimension_summary}

Write a 3-sentence executive summary for a BI developer that:
1. States how ready this report is for Copilot in plain language
2. Identifies the single most important area to fix first
3. Gives one encouraging, practical next step they can take today

Be direct, honest, and constructive. No bullet points — just 3 clear sentences."""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=300,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text
