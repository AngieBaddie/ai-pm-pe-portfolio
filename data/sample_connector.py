# sample_data.py
# This simulates what the Power BI API returns for your reports and semantic models.
# When you connect to real Power BI later, this file gets replaced — nothing else changes.

def get_sample_reports():
    return [
        {
            "report_id": "RPT-001",
            "report_name": "Monthly Sales Summary",
            "workspace": "Company A",
            "last_modified": "2022-03-15",
            "measures": [
                {
                    "name": "tot_rev",
                    "description": "",
                    "expression": "SUM(Sales[Revenue])",
                    "is_hidden": False
                },
                {
                    "name": "YTD_REV",
                    "description": "",
                    "expression": "TOTALYTD(SUM(Sales[Revenue]), Dates[Date])",
                    "is_hidden": False
                },
                {
                    "name": "gross_margin_calc_final_v2",
                    "description": "",
                    "expression": "DIVIDE(SUM(Sales[Revenue]) - SUM(Sales[Cost]), SUM(Sales[Revenue]))",
                    "is_hidden": False
                },
            ],
            "columns": [
                {"name": "cust_id", "description": "", "is_hidden": False},
                {"name": "prod_cd", "description": "", "is_hidden": False},
                {"name": "trans_dt", "description": "", "is_hidden": False},
            ],
            "relationships": [
                {"from_table": "Sales", "to_table": "Dates", "active": True},
                {"from_table": "Sales", "to_table": "Customers", "active": False},
                {"from_table": "Orphan_Table", "to_table": "Sales", "active": False},
            ],
            "pages": [
                {"name": "Overview", "visuals_count": 8},
                {"name": "Page 2", "visuals_count": 0},
                {"name": "Detail Drill", "visuals_count": 5},
                {"name": "Old Report", "visuals_count": 0},
            ]
        },
        {
            "report_id": "RPT-002",
            "report_name": "HR Headcount Dashboard",
            "workspace": "Company B",
            "last_modified": "2023-11-20",
            "measures": [
                {
                    "name": "Total Headcount",
                    "description": "Total number of active employees at the end of the selected period.",
                    "expression": "COUNTROWS(Employees)",
                    "is_hidden": False
                },
                {
                    "name": "Attrition Rate",
                    "description": "Percentage of employees who left during the period.",
                    "expression": "DIVIDE([Leavers], [Total Headcount])",
                    "is_hidden": False
                },
                {
                    "name": "Leavers",
                    "description": "Count of employees who exited during the selected period.",
                    "expression": "COUNTROWS(FILTER(Employees, Employees[Status] = \"Left\"))",
                    "is_hidden": False
                },
            ],
            "columns": [
                {"name": "Employee ID", "description": "Unique identifier for each employee.", "is_hidden": False},
                {"name": "Department Name", "description": "The department the employee belongs to.", "is_hidden": False},
                {"name": "Job Grade", "description": "Employee seniority level.", "is_hidden": False},
            ],
            "relationships": [
                {"from_table": "Employees", "to_table": "Departments", "active": True},
                {"from_table": "Employees", "to_table": "Dates", "active": True},
            ],
            "pages": [
                {"name": "Headcount Overview", "visuals_count": 6},
                {"name": "Attrition Analysis", "visuals_count": 7},
                {"name": "Recruitment", "visuals_count": 4},
            ]
        },
        {
            "report_id": "RPT-003",
            "report_name": "Finance P&L Report",
            "workspace": "Company A",
            "last_modified": "2021-06-10",
            "measures": [
                {
                    "name": "x1",
                    "description": "",
                    "expression": "SUM(Finance[Amount])",
                    "is_hidden": False
                },
                {
                    "name": "x2_adj",
                    "description": "",
                    "expression": "CALCULATE(SUM(Finance[Amount]), Finance[Type]=\"Adjusted\")",
                    "is_hidden": False
                },
                {
                    "name": "EBITDA_FINAL_USE_THIS",
                    "description": "",
                    "expression": "CALCULATE([x1] - [x2_adj], ALLEXCEPT(Finance, Finance[Year]))",
                    "is_hidden": False
                },
            ],
            "columns": [
                {"name": "acct_no", "description": "", "is_hidden": False},
                {"name": "cost_ctr", "description": "", "is_hidden": False},
                {"name": "amt_lcy", "description": "", "is_hidden": False},
            ],
            "relationships": [
                {"from_table": "Finance", "to_table": "Dates", "active": True},
                {"from_table": "Finance", "to_table": "CostCenters", "active": True},
                {"from_table": "Legacy_Mapping", "to_table": "Finance", "active": False},
            ],
            "pages": [
                {"name": "P&L Summary", "visuals_count": 9},
                {"name": "Variance Analysis", "visuals_count": 6},
                {"name": "Temp", "visuals_count": 0},
                {"name": "Draft", "visuals_count": 0},
            ]
        },
    ]
