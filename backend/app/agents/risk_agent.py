from typing import List, Tuple
from app.models.financial_schema import (
    FinancialStatements, RatioItem, RiskIndicator, RiskLevel
)

class RiskIntelligenceAgent:
    """
    Deterministic rule-based risk evaluation engine coupled with institutional explanations.
    Produces an overall composite risk score (0-100) and actionable alert vectors.
    """

    @classmethod
    def evaluate_risks(cls, statements: FinancialStatements, ratios_by_category: dict, period: str) -> Tuple[float, RiskLevel, List[RiskIndicator]]:
        indicators: List[RiskIndicator] = []
        penalty_score = 0.0  # 0 is pristine health, 100 is distress

        # Extract latest values
        debt = statements.total_debt.get(period, 0.0)
        equity = statements.shareholders_equity.get(period, 0.0)
        ca = statements.current_assets.get(period, 0.0)
        cl = statements.current_liabilities.get(period, 0.0)
        cfo = statements.cash_from_operations.get(period, 0.0)
        net_inc = statements.net_profit.get(period, 0.0)
        op_inc = statements.operating_income.get(period, 0.0)
        int_exp = statements.interest_expense.get(period, 0.0)
        rec = statements.accounts_receivable.get(period, 0.0)
        rev = statements.revenue.get(period, 0.0)

        # 1. Leverage / Debt Risk
        de_ratio = (debt / equity) if equity > 0 else 999.0
        if de_ratio > 2.0:
            penalty_score += 25
            indicators.append(RiskIndicator(
                id="RISK-LEV-01",
                category="Leverage Risk",
                severity=RiskLevel.HIGH,
                title="Elevated Debt-to-Equity Ratio",
                metric_evidence=f"D/E Ratio is {de_ratio:.2f}x (Total Debt: {debt:,.0f} vs Equity: {equity:,.0f})",
                formula_or_rule="D/E > 2.0x Threshold",
                ai_explanation="The entity has incurred significant leverage relative to net worth. High debt exposes equity holders to severe volatility if interest rates climb or operating profits falter."
            ))
        elif de_ratio > 1.3:
            penalty_score += 15
            indicators.append(RiskIndicator(
                id="RISK-LEV-02",
                category="Leverage Risk",
                severity=RiskLevel.MODERATE,
                title="Moderate Financial Leverage",
                metric_evidence=f"D/E Ratio is {de_ratio:.2f}x",
                formula_or_rule="1.3x < D/E <= 2.0x",
                ai_explanation="Debt obligations are sizable and require dedicated free cash flow allocation for servicing."
            ))

        # 2. Interest Coverage Risk
        if int_exp > 0:
            ic_ratio = op_inc / int_exp
            if ic_ratio < 1.5:
                penalty_score += 30
                indicators.append(RiskIndicator(
                    id="RISK-SOLV-01",
                    category="Solvency Risk",
                    severity=RiskLevel.CRITICAL,
                    title="Impaired Interest Coverage Cushion",
                    metric_evidence=f"Operating Income ({op_inc:,.0f}) covers Interest Expense ({int_exp:,.0f}) only {ic_ratio:.2f}x",
                    formula_or_rule="EBIT / Interest < 1.5x",
                    ai_explanation="Company is close to operating cash breakeven with respect to debt service. Any cyclical downturn could trigger interest default."
                ))
            elif ic_ratio < 3.0:
                penalty_score += 12
                indicators.append(RiskIndicator(
                    id="RISK-SOLV-02",
                    category="Solvency Risk",
                    severity=RiskLevel.MODERATE,
                    title="Tight Interest Coverage Cushion",
                    metric_evidence=f"Interest Coverage at {ic_ratio:.2f}x",
                    formula_or_rule="1.5x <= EBIT / Interest < 3.0x",
                    ai_explanation="Interest payments consume a significant proportion of operating profit."
                ))

        # 3. Liquidity Risk
        current_ratio = (ca / cl) if cl > 0 else 1.0
        if current_ratio < 1.0:
            penalty_score += 25
            indicators.append(RiskIndicator(
                id="RISK-LIQ-01",
                category="Liquidity Risk",
                severity=RiskLevel.HIGH,
                title="Working Capital Deficit (Current Ratio < 1.0x)",
                metric_evidence=f"Current Assets ({ca:,.0f}) < Current Liabilities ({cl:,.0f}). Ratio: {current_ratio:.2f}x",
                formula_or_rule="CA / CL < 1.0x",
                ai_explanation="Short-term obligations due within 12 months exceed liquid current assets. Reliance on credit facility rollover is high."
            ))
        elif current_ratio < 1.25:
            penalty_score += 10
            indicators.append(RiskIndicator(
                id="RISK-LIQ-02",
                category="Liquidity Risk",
                severity=RiskLevel.MODERATE,
                title="Narrow Liquidity Runway",
                metric_evidence=f"Current Ratio at {current_ratio:.2f}x",
                formula_or_rule="1.0x <= CA / CL < 1.25x",
                ai_explanation="Buffer against sudden trade receivable delays or supply chain cost spikes is slim."
            ))

        # 4. Earnings Quality & Cash Flow Risk
        if net_inc > 0 and cfo < 0:
            penalty_score += 25
            indicators.append(RiskIndicator(
                id="RISK-EARN-01",
                category="Earnings Quality",
                severity=RiskLevel.HIGH,
                title="Divergence: Positive Net Profit with Negative CFO",
                metric_evidence=f"Reported Net Profit: {net_inc:,.0f} | Operating Cash Flow: {cfo:,.0f}",
                formula_or_rule="Net Income > 0 AND CFO < 0",
                ai_explanation="High risk of aggressive revenue recognition or ballooning uncollected receivables. Accounting profit is not translating into realized bank deposits."
            ))
        elif net_inc > 0 and (cfo / net_inc) < 0.7:
            penalty_score += 12
            indicators.append(RiskIndicator(
                id="RISK-EARN-02",
                category="Earnings Quality",
                severity=RiskLevel.MODERATE,
                title="Sub-par Cash Conversion Efficiency",
                metric_evidence=f"CFO / Net Income = {(cfo / net_inc):.2f}x (< 0.70x benchmark)",
                formula_or_rule="CFO / Net Income < 0.7x",
                ai_explanation="Working capital lockups (inventory pile-up or supplier credit shrinkage) are dampening cash generation."
            ))

        # 5. Receivables Bloat
        if rev > 0 and (rec / rev) > 0.25: # over 90 days of revenue in receivables
            penalty_score += 10
            indicators.append(RiskIndicator(
                id="RISK-OPS-01",
                category="Operational Risk",
                severity=RiskLevel.MODERATE,
                title="Customer Credit Exposure (High Receivables / Revenue)",
                metric_evidence=f"Receivables ({rec:,.0f}) represent {(rec/rev)*100:.1f}% of total annual sales",
                formula_or_rule="Receivables / Revenue > 25%",
                ai_explanation="Elevated customer credit risk; possible concentration in slow-paying clients or generous payment terms to artificially prop up sales."
            ))

        # Cap penalty at 100
        overall_risk_score = min(100.0, max(10.0, penalty_score))
        
        if overall_risk_score >= 60:
            overall_level = RiskLevel.HIGH
        elif overall_risk_score >= 35:
            overall_level = RiskLevel.MODERATE
        else:
            overall_level = RiskLevel.LOW

        return overall_risk_score, overall_level, indicators
