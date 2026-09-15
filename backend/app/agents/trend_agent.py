from typing import List, Dict
from app.models.financial_schema import FinancialStatements, TrendMetric

class TrendAnalysisAgent:
    """
    Computes multi-year CAGR, year-over-year momentum, and qualitative trend commentary.
    """

    @staticmethod
    def analyze_trends(statements: FinancialStatements, periods: List[str]) -> List[TrendMetric]:
        if len(periods) < 2:
            return []

        sorted_periods = sorted(periods)
        start_yr = sorted_periods[0]
        end_yr = sorted_periods[-1]
        n_years = len(sorted_periods) - 1

        metrics_to_track = [
            ("Revenue", statements.revenue, True),
            ("Operating Income", statements.operating_income, True),
            ("Net Profit", statements.net_profit, True),
            ("Total Debt", statements.total_debt, False),
            ("Cash from Operations (CFO)", statements.cash_from_operations, True),
            ("Accounts Receivable", statements.accounts_receivable, False),
        ]

        results: List[TrendMetric] = []

        for name, series, positive_if_growing in metrics_to_track:
            v_start = series.get(start_yr)
            v_end = series.get(end_yr)
            history = {yr: series[yr] for yr in sorted_periods if yr in series}

            if v_start is not None and v_end is not None and len(history) >= 2:
                growth_rate = 0.0
                if v_start > 0:
                    if n_years > 1 and v_end > 0:
                        growth_rate = round(((v_end / v_start) ** (1.0 / n_years) - 1.0) * 100, 2)
                    else:
                        growth_rate = round(((v_end - v_start) / v_start) * 100, 2)

                direction = "UP" if v_end > v_start else ("DOWN" if v_end < v_start else "FLAT")
                is_positive = (direction == "UP" and positive_if_growing) or (direction == "DOWN" and not positive_if_growing)

                commentary = ""
                if name == "Revenue":
                    commentary = (
                        f"Revenue demonstrated a {growth_rate:+.1f}% annualized expansion from {v_start:,.0f} to {v_end:,.0f}, "
                        f"showing persistent market capture." if growth_rate > 0 else
                        f"Revenue contracted by {abs(growth_rate):.1f}% over the observation period."
                    )
                elif name == "Operating Income":
                    rev_growth = ((statements.revenue.get(end_yr, 1) / statements.revenue.get(start_yr, 1)) - 1) * 100 if statements.revenue.get(start_yr) else 0
                    if growth_rate > rev_growth:
                        commentary = f"Operating income expansion ({growth_rate:+.1f}%) outpaced top-line growth, signaling expanding operational leverage."
                    else:
                        commentary = f"Operating income grew at {growth_rate:+.1f}%, impacted by rising SG&A and raw materials."
                elif name == "Total Debt":
                    if direction == "UP":
                        commentary = f"Leverage climbed {growth_rate:+.1f}%. Capital investments financed via debt increase financial risk."
                    else:
                        commentary = f"Debt deleveraged by {abs(growth_rate):.1f}%, strengthening capital structure resilience."
                elif name == "Accounts Receivable":
                    rev_growth = ((statements.revenue.get(end_yr, 1) / statements.revenue.get(start_yr, 1)) - 1) * 100 if statements.revenue.get(start_yr) else 0
                    if growth_rate > (rev_growth + 5):
                        commentary = f"Warning: Receivables grew ({growth_rate:+.1f}%) significantly faster than sales ({rev_growth:+.1f}%), indicating customer collection friction."
                    else:
                        commentary = f"Receivables trajectory remains aligned with sales growth."
                else:
                    commentary = f"{name} moved from {v_start:,.0f} to {v_end:,.0f} ({direction} {growth_rate:+.1f}%)."

                results.append(TrendMetric(
                    metric_name=name,
                    historical_values=history,
                    cagr_or_growth=growth_rate,
                    direction=direction,
                    is_positive_development=is_positive,
                    ai_commentary=commentary
                ))

        return results
