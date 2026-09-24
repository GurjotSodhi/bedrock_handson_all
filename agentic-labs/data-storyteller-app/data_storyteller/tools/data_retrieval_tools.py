"""Tools for retrieving data"""

from strands import tool


@tool(description="Retrieve data to discuss in the document.")
def retrieve_data():
    """From Docstring"""

    source_data = {
        "sales_by_country": [
            {
                "country": "Spain",
                "profits": 809468,
                "units_sold": 66262,
                "employees": 32,
                "units_sold_pct_change_since_previous_year": 13.2,
            },
            {
                "country": "France",
                "profits": 124793,
                "units_sold": 37335,
                "employees": 21,
                "units_sold_pct_change_since_previous_year": -5.4,
            },
            {
                "country": "Italy",
                "profits": 798045,
                "units_sold": 98246,
                "employees": 16,
                "units_sold_pct_change_since_previous_year": 21.1,
            },
            {
                "country": "Germany",
                "profits": 30247,
                "units_sold": 198467,
                "employees": 66,
                "units_sold_pct_change_since_previous_year": 0.0,
            },
            {
                "country": "Netherlands",
                "profits": 802489,
                "units_sold": 201552,
                "employees": 33,
                "units_sold_pct_change_since_previous_year": -3.1,
            },
        ],
        "overall_revenue_by_year": {
            "year_2025": 4008343,
            "year_2024": 4059341,
            "year_2023": 3807986,
            "year_2022": 3716634,
            "year_2021": 2803129,
        },
    }

    return {
        "status": "success",
        "content": [{"json": {"content_type": "source_data", "source_data": source_data}}],
    }
