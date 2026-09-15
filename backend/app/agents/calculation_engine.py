import math
from typing import Dict, List, Tuple
from app.models.financial_schema import (
    FinancialStatements, RatioItem, ValidationAlert, ValidationStatus,
    TrendMetric, RiskIndicator, RiskLevel
)

class DeterministicCalculationEngine:
    """
    Pure mathematical calculations for financial ratios and metrics.
    Ensures zero hallucination and strict arithmetic fidelity.
    """

    @staticmethod
    def calculate_ratios(statements: FinancialStatements, period: str) -> Dict[str, List[RatioItem]]:
        rev = statements.revenue.get(period, 0.0)
        cogs = statements.cost_of_goods_sold.get(period, 0.0)
        gp = statements.gross_profit.get(period, rev - cogs if rev else 0.0)
        op_inc = statements.operating_income.get(period, 0.0)
        net_inc = statements.net_profit.get(period, 0.0)
        int_exp = statements.interest_expense.get(period, 0.0)
        
        ca = statements.current_assets.get(period, 0.0)
        cl = statements.current_liabilities.get(period, 0.0)
        inv = statements.inventory.get(period, 0.0)
        cash = statements.cash_and_equivalents.get(period, 0.0)
        ta = statements.total_assets.get(period, 0.0)
        equity = statements.shareholders_equity.get(period, 0.0)
        debt = statements.total_debt.get(period, 0.0)
        rec = statements.accounts_receivable.get(period, 0.0)
        
        cfo = statements.cash_from_operations.get(period, 0.0)
        capex = statements.capital_expenditures.get(period, 0.0)
        fcf = cfo - capex

        ratios: Dict[str, List[RatioItem]] = {
            "Profitability": [],
            "Liquidity": [],
            "Leverage": [],
            "Efficiency": [],
            "Cash Flow": []
        }

        # 1. Profitability
        if rev > 0:
            gm = (gp / rev) * 100
            ratios["Profitability"].append(RatioItem(
                category="Profitability",
                name="Gross Profit Margin",
                value=round(gm, 2),
                unit="%",
                formula="(Gross Profit / Revenue) * 100",
                calculation_steps=f"({gp:,.1f} / {rev:,.1f}) * 100 = {gm:.2f}%",
                benchmark="> 25%",
                status="HEALTHY" if gm >= 25 else "WARNING",
                interpretation="Measures percentage of revenue left after production/procurement costs."
            ))

            om = (op_inc / rev) * 100
            ratios["Profitability"].append(RatioItem(
                category="Profitability",
                name="Operating Margin",
                value=round(om, 2),
                unit="%",
                formula="(Operating Income / Revenue) * 100",
                calculation_steps=f"({op_inc:,.1f} / {rev:,.1f}) * 100 = {om:.2f}%",
                benchmark="> 12%",
                status="HEALTHY" if om >= 12 else ("WARNING" if om >= 6 else "CRITICAL"),
                interpretation="Reflects operating efficiency before tax and financing costs."
            ))

            npm = (net_inc / rev) * 100
            ratios["Profitability"].append(RatioItem(
                category="Profitability",
                name="Net Profit Margin",
                value=round(npm, 2),
                unit="%",
                formula="(Net Income / Revenue) * 100",
                calculation_steps=f"({net_inc:,.1f} / {rev:,.1f}) * 100 = {npm:.2f}%",
                benchmark="> 8%",
                status="HEALTHY" if npm >= 8 else ("WARNING" if npm >= 3 else "CRITICAL"),
                interpretation="Net return generated from every rupee/dollar of sales."
            ))

        if equity > 0:
            roe = (net_inc / equity) * 100
            ratios["Profitability"].append(RatioItem(
                category="Profitability",
                name="Return on Equity (ROE)",
                value=round(roe, 2),
                unit="%",
                formula="(Net Income / Shareholders Equity) * 100",
                calculation_steps=f"({net_inc:,.1f} / {equity:,.1f}) * 100 = {roe:.2f}%",
                benchmark="> 15%",
                status="HEALTHY" if roe >= 15 else "WARNING",
                interpretation="Shows how effectively shareholder capital is deployed to generate profits."
            ))

        if ta > 0:
            roa = (net_inc / ta) * 100
            ratios["Profitability"].append(RatioItem(
                category="Profitability",
                name="Return on Assets (ROA)",
                value=round(roa, 2),
                unit="%",
                formula="(Net Income / Total Assets) * 100",
                calculation_steps=f"({net_inc:,.1f} / {ta:,.1f}) * 100 = {roa:.2f}%",
                benchmark="> 6%",
                status="HEALTHY" if roa >= 6 else "WARNING",
                interpretation="Demonstrates asset profitability regardless of financing structure."
            ))

        # 2. Liquidity
        if cl > 0:
            cr = ca / cl
            ratios["Liquidity"].append(RatioItem(
                category="Liquidity",
                name="Current Ratio",
                value=round(cr, 2),
                unit="x",
                formula="Current Assets / Current Liabilities",
                calculation_steps=f"{ca:,.1f} / {cl:,.1f} = {cr:.2f}x",
                benchmark="1.2x - 2.0x",
                status="HEALTHY" if cr >= 1.2 else "CRITICAL",
                interpretation="Ability to cover short-term obligations due within one operating cycle."
            ))

            qr = (ca - inv) / cl
            ratios["Liquidity"].append(RatioItem(
                category="Liquidity",
                name="Quick Ratio (Acid-Test)",
                value=round(qr, 2),
                unit="x",
                formula="(Current Assets - Inventory) / Current Liabilities",
                calculation_steps=f"({ca:,.1f} - {inv:,.1f}) / {cl:,.1f} = {qr:.2f}x",
                benchmark="> 1.0x",
                status="HEALTHY" if qr >= 1.0 else "WARNING",
                interpretation="Measures immediate liquid assets available without needing to liquidate inventory."
            ))

            cash_ratio = cash / cl
            ratios["Liquidity"].append(RatioItem(
                category="Liquidity",
                name="Cash Ratio",
                value=round(cash_ratio, 2),
                unit="x",
                formula="Cash & Equivalents / Current Liabilities",
                calculation_steps=f"{cash:,.1f} / {cl:,.1f} = {cash_ratio:.2f}x",
                benchmark="> 0.2x",
                status="HEALTHY" if cash_ratio >= 0.2 else "WARNING",
                interpretation="Direct liquidity buffer available instantaneously."
            ))

        # 3. Leverage / Solvency
        if equity > 0:
            de = debt / equity
            ratios["Leverage"].append(RatioItem(
                category="Leverage",
                name="Debt-to-Equity (D/E)",
                value=round(de, 2),
                unit="x",
                formula="Total Debt / Shareholders Equity",
                calculation_steps=f"{debt:,.1f} / {equity:,.1f} = {de:.2f}x",
                benchmark="< 1.2x",
                status="HEALTHY" if de <= 1.2 else ("WARNING" if de <= 2.0 else "CRITICAL"),
                interpretation="Financial leverage indicator comparing debt capital to shareholder net worth."
            ))

        if ta > 0:
            da = debt / ta
            ratios["Leverage"].append(RatioItem(
                category="Leverage",
                name="Debt-to-Assets",
                value=round(da, 2),
                unit="x",
                formula="Total Debt / Total Assets",
                calculation_steps=f"{debt:,.1f} / {ta:,.1f} = {da:.2f}x",
                benchmark="< 0.5x",
                status="HEALTHY" if da <= 0.5 else "WARNING",
                interpretation="Proportion of total business assets financed through borrowed money."
            ))

        if int_exp > 0:
            ic = op_inc / int_exp
            ratios["Leverage"].append(RatioItem(
                category="Leverage",
                name="Interest Coverage Ratio",
                value=round(ic, 2),
                unit="x",
                formula="Operating Income / Interest Expense",
                calculation_steps=f"{op_inc:,.1f} / {int_exp:,.1f} = {ic:.2f}x",
                benchmark="> 3.0x",
                status="HEALTHY" if ic >= 3.0 else "CRITICAL",
                interpretation="Ability to service periodic debt interest obligations comfortably."
            ))

        # 4. Efficiency
        if ta > 0 and rev > 0:
            at = rev / ta
            ratios["Efficiency"].append(RatioItem(
                category="Efficiency",
                name="Asset Turnover",
                value=round(at, 2),
                unit="x",
                formula="Revenue / Total Assets",
                calculation_steps=f"{rev:,.1f} / {ta:,.1f} = {at:.2f}x",
                benchmark="> 0.8x",
                status="HEALTHY" if at >= 0.8 else "NORMAL",
                interpretation="Capital velocity showing how efficiently assets generate top-line turnover."
            ))

        if rec > 0 and rev > 0:
            dso = (rec / rev) * 365
            ratios["Efficiency"].append(RatioItem(
                category="Efficiency",
                name="Days Sales Outstanding (DSO)",
                value=round(dso, 1),
                unit="Days",
                formula="(Accounts Receivable / Revenue) * 365",
                calculation_steps=f"({rec:,.1f} / {rev:,.1f}) * 365 = {dso:.1f} Days",
                benchmark="< 60 Days",
                status="HEALTHY" if dso <= 60 else "WARNING",
                interpretation="Average days required to convert credit sales into cleared customer cash."
            ))

        # 5. Cash Flow Quality
        if rev > 0:
            cf_margin = (cfo / rev) * 100
            ratios["Cash Flow"].append(RatioItem(
                category="Cash Flow",
                name="Operating Cash Flow Margin",
                value=round(cf_margin, 2),
                unit="%",
                formula="(CFO / Revenue) * 100",
                calculation_steps=f"({cfo:,.1f} / {rev:,.1f}) * 100 = {cf_margin:.2f}%",
                benchmark="> 10%",
                status="HEALTHY" if cf_margin >= 10 else "WARNING",
                interpretation="Proportion of actual cash converted from reported revenue."
            ))

        ratios["Cash Flow"].append(RatioItem(
            category="Cash Flow",
            name="Free Cash Flow (FCF)",
            value=round(fcf, 2),
            unit="Cr",
            formula="Operating Cash Flow - Capital Expenditures",
            calculation_steps=f"{cfo:,.1f} - {capex:,.1f} = {fcf:,.1f}",
            benchmark="> 0",
            status="HEALTHY" if fcf > 0 else "WARNING",
            interpretation="Discretionary cash remaining after investing in long-term operating assets."
        ))

        if net_inc > 0:
            quality = cfo / net_inc
            ratios["Cash Flow"].append(RatioItem(
                category="Cash Flow",
                name="Earnings Quality (CFO / Net Income)",
                value=round(quality, 2),
                unit="x",
                formula="CFO / Net Income",
                calculation_steps=f"{cfo:,.1f} / {net_inc:,.1f} = {quality:.2f}x",
                benchmark="> 1.0x",
                status="HEALTHY" if quality >= 1.0 else "WARNING",
                interpretation="Ratios < 1.0 indicate non-cash accrual gains or aggressive revenue recognition."
            ))

        return ratios
