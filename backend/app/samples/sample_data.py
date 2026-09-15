from app.models.financial_schema import FinancialStatements, MetricSource

SAMPLE_COMPANIES = {
    "FIN-TCS": {
        "company_id": "FIN-TCS",
        "company_name": "Tata Consultancy Services (TCS)",
        "currency_unit": "₹ Cr",
        "periods": ["2023", "2024", "2025"],
        "statements": FinancialStatements(
            revenue={"2023": 225458.0, "2024": 240893.0, "2025": 261800.0},
            cost_of_goods_sold={"2023": 133240.0, "2024": 142100.0, "2025": 151844.0},
            gross_profit={"2023": 92218.0, "2024": 98793.0, "2025": 109956.0},
            operating_expenses={"2023": 33110.0, "2024": 35700.0, "2025": 38100.0},
            operating_income={"2023": 59108.0, "2024": 63093.0, "2025": 71856.0},
            interest_expense={"2023": 779.0, "2024": 820.0, "2025": 890.0},
            tax_expense={"2023": 14604.0, "2024": 15400.0, "2025": 17400.0},
            net_profit={"2023": 42303.0, "2024": 46099.0, "2025": 51200.0},
            
            cash_and_equivalents={"2023": 11028.0, "2024": 14320.0, "2025": 18450.0},
            accounts_receivable={"2023": 41200.0, "2024": 44800.0, "2025": 48200.0},
            inventory={"2023": 120.0, "2024": 140.0, "2025": 150.0},
            current_assets={"2023": 98400.0, "2024": 108500.0, "2025": 121000.0},
            non_current_assets={"2023": 44500.0, "2024": 46200.0, "2025": 49800.0},
            total_assets={"2023": 142900.0, "2024": 154700.0, "2025": 170800.0},
            
            current_liabilities={"2023": 42100.0, "2024": 45600.0, "2025": 49200.0},
            short_term_debt={"2023": 0.0, "2024": 0.0, "2025": 0.0},
            long_term_debt={"2023": 0.0, "2024": 0.0, "2025": 0.0},
            total_debt={"2023": 0.0, "2024": 0.0, "2025": 0.0},
            total_liabilities={"2023": 52400.0, "2024": 56200.0, "2025": 60500.0},
            shareholders_equity={"2023": 90500.0, "2024": 98500.0, "2025": 110300.0},
            
            cash_from_operations={"2023": 42000.0, "2024": 45200.0, "2025": 49800.0},
            capital_expenditures={"2023": 3100.0, "2024": 3400.0, "2025": 3800.0},
            cash_from_investing={"2023": -4500.0, "2024": -5200.0, "2025": -5600.0},
            cash_from_financing={"2023": -34200.0, "2024": -36700.0, "2025": -40100.0},
            beginning_cash={"2023": 7728.0, "2024": 11028.0, "2025": 14320.0},
            ending_cash={"2023": 11028.0, "2024": 14320.0, "2025": 18450.0},

            sources={
                "revenue": MetricSource(document_name="TCS_Annual_Report_2025.pdf", page_number=142, raw_text="Statement of Profit and Loss - Revenue from Operations"),
                "net_profit": MetricSource(document_name="TCS_Annual_Report_2025.pdf", page_number=143, raw_text="Profit for the Year attributable to shareholders"),
                "total_assets": MetricSource(document_name="TCS_Annual_Report_2025.pdf", page_number=144, raw_text="Consolidated Balance Sheet - Total Assets")
            }
        ),
        "annual_report_mda": """
Tata Consultancy Services Management Discussion & Analysis (MD&A) FY2025:
Executive Overview:
During FY2025, TCS delivered robust industry-leading operating margins of 27.4% and free cash flow generation of ₹46,000 Cr. Revenue expanded 8.7% driven by artificial intelligence enterprise transformations, cloud migration architectures, and resilient banking & financial services customer renewals.

Cost & Margin Dynamics (Page 73):
Operating expenditures rose 6.7% primarily due to compensation adjustments, strategic hiring of generative AI specialists, and localized onshore delivery center expansions in North America and Continental Europe. SG&A costs remained strictly disciplined at 14.5% of sales.

Capital Structure & Debt Policy (Page 84):
TCS operates as a zero-net-debt corporation. The company maintains negligible borrowings, consisting solely of statutory lease obligations. Free cash flow conversion to net income surpassed 97%, allowing consistent distribution of 80%+ earnings through interim dividends and capital return buybacks.

Key Risks (Page 112):
1. Geopolitical uncertainty impacting European client discretionary digital spending.
2. Talent retention and wage inflation for advanced LLM engineering roles.
3. Currency fluctuations in GBP and USD versus INR.
"""
    },
    "FIN-GROWTH-CORP": {
        "company_id": "FIN-GROWTH-CORP",
        "company_name": "FinTech Logistics & Retail Corp",
        "currency_unit": "₹ Cr",
        "periods": ["2023", "2024", "2025"],
        "statements": FinancialStatements(
            revenue={"2023": 820.0, "2024": 965.0, "2025": 1139.0},
            cost_of_goods_sold={"2023": 510.0, "2024": 605.0, "2025": 708.0},
            gross_profit={"2023": 310.0, "2024": 360.0, "2025": 431.0},
            operating_expenses={"2023": 192.0, "2024": 228.0, "2025": 262.0},
            operating_income={"2023": 118.0, "2024": 132.0, "2025": 169.0},
            interest_expense={"2023": 32.0, "2024": 42.0, "2025": 58.0},
            tax_expense={"2023": 21.0, "2024": 22.0, "2025": 27.0},
            net_profit={"2023": 65.0, "2024": 68.0, "2025": 84.0},
            
            cash_and_equivalents={"2023": 45.0, "2024": 52.0, "2025": 64.0},
            accounts_receivable={"2023": 160.0, "2024": 215.0, "2025": 288.0},
            inventory={"2023": 135.0, "2024": 170.0, "2025": 210.0},
            current_assets={"2023": 360.0, "2024": 460.0, "2025": 590.0},
            non_current_assets={"2023": 410.0, "2024": 490.0, "2025": 580.0},
            total_assets={"2023": 770.0, "2024": 950.0, "2025": 1170.0},
            
            current_liabilities={"2023": 280.0, "2024": 370.0, "2025": 485.0},
            short_term_debt={"2023": 110.0, "2024": 140.0, "2025": 170.0},
            long_term_debt={"2023": 240.0, "2024": 250.0, "2025": 250.0},
            total_debt={"2023": 350.0, "2024": 390.0, "2025": 420.0},
            total_liabilities={"2023": 540.0, "2024": 670.0, "2025": 874.0},
            shareholders_equity={"2023": 230.0, "2024": 280.0, "2025": 296.0},
            
            cash_from_operations={"2023": 78.0, "2024": 82.0, "2025": 96.0},
            capital_expenditures={"2023": 55.0, "2024": 65.0, "2025": 72.0},
            cash_from_investing={"2023": -60.0, "2024": -70.0, "2025": -78.0},
            cash_from_financing={"2023": -11.0, "2024": -5.0, "2025": -6.0},
            beginning_cash={"2023": 38.0, "2024": 45.0, "2025": 52.0},
            ending_cash={"2023": 45.0, "2024": 52.0, "2025": 64.0},

            sources={
                "revenue": MetricSource(document_name="GrowthCorp_Annual_Report.pdf", page_number=52, raw_text="Consolidated Profit and Loss Account - Total Revenue ₹1,139 Cr"),
                "total_debt": MetricSource(document_name="GrowthCorp_Annual_Report.pdf", page_number=84, raw_text="Note 16 - Borrowings: Term Loans ₹250 Cr + Working Capital ₹170 Cr"),
                "shareholders_equity": MetricSource(document_name="GrowthCorp_Annual_Report.pdf", page_number=85, raw_text="Statement of Changes in Equity - Total Equity ₹296 Cr")
            }
        ),
        "annual_report_mda": """
FinTech Logistics & Retail Corp Annual Report FY2025:
Executive Summary (Page 4):
The company achieved revenue growth of 18.0% reaching ₹1,139 Cr. Operating margin expanded from 13.7% to 14.8% due to automated fulfillment centers and higher software logistics subscriptions.

Capital Expenditures & Leverage (Page 84):
To meet growing e-commerce fulfillment demand, total debt rose to ₹420 Cr, resulting in a Debt-to-Equity ratio of 1.42x. Management entered long-term bank credit lines with average interest coupons of 9.2%.

Working Capital & Receivables (Page 91):
Accounts receivable rose 34.0% to ₹288 Cr. The increase was driven by extended 90-day settlement terms granted to strategic retail enterprise accounts. Management has implemented automated credit scoring to contain potential bad debt allowances.
"""
    }
}
