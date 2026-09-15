import math
from typing import List, Tuple
from app.models.financial_schema import (
    FinancialStatements, ValidationAlert, ValidationStatus
)

class ValidationAgent:
    """
    Validates double-entry accounting integrity and identifies extraction discrepancies.
    Produces PASS, WARNING, or FAIL with delta tolerances.
    """

    TOLERANCE_ABSOLUTE = 2.0  # Allow minor rounding differences up to 2 units (e.g. 2 Cr)
    TOLERANCE_PERCENT = 0.015 # 1.5% discrepancy tolerance

    @classmethod
    def validate_statements(cls, statements: FinancialStatements, periods: List[str]) -> Tuple[ValidationStatus, List[ValidationAlert]]:
        alerts: List[ValidationAlert] = []
        overall_status = ValidationStatus.PASS

        for period in periods:
            # 1. Balance Sheet: Total Assets = Total Liabilities + Shareholders Equity
            ta = statements.total_assets.get(period)
            tl = statements.total_liabilities.get(period)
            eq = statements.shareholders_equity.get(period)

            if ta is not None and tl is not None and eq is not None:
                expected_ta = tl + eq
                diff = abs(ta - expected_ta)
                max_tolerance = max(cls.TOLERANCE_ABSOLUTE, ta * cls.TOLERANCE_PERCENT)
                
                if diff > max_tolerance:
                    severity = ValidationStatus.FAIL if diff > (ta * 0.05) else ValidationStatus.WARNING
                    if severity == ValidationStatus.FAIL:
                        overall_status = ValidationStatus.FAIL
                    elif overall_status != ValidationStatus.FAIL:
                        overall_status = ValidationStatus.WARNING

                    alerts.append(ValidationAlert(
                        rule_name="Balance Sheet Reconciliation",
                        period=period,
                        status=severity,
                        expected_expression=f"Assets ({ta:,.1f}) = Liabilities ({tl:,.1f}) + Equity ({eq:,.1f})",
                        actual_expression=f"Diff: {diff:,.2f} ({ (diff/ta)*100:.2f}%)",
                        discrepancy=round(diff, 2),
                        threshold=round(max_tolerance, 2),
                        message=f"Balance sheet values do not reconcile by {diff:,.1f} {statements.sources.get('currency', 'units')}.",
                        suggested_fix="Check for unclassified minority interests, preferred shares, or OCR digit transpose."
                    ))

            # 2. Income Statement: Gross Profit = Revenue - COGS
            rev = statements.revenue.get(period)
            cogs = statements.cost_of_goods_sold.get(period)
            gp = statements.gross_profit.get(period)

            if rev is not None and cogs is not None and gp is not None:
                expected_gp = rev - cogs
                diff = abs(gp - expected_gp)
                if diff > cls.TOLERANCE_ABSOLUTE:
                    alerts.append(ValidationAlert(
                        rule_name="Gross Margin Consistency",
                        period=period,
                        status=ValidationStatus.WARNING,
                        expected_expression=f"Gross Profit ({gp:,.1f}) = Revenue ({rev:,.1f}) - COGS ({cogs:,.1f})",
                        actual_expression=f"Difference: {diff:,.2f}",
                        discrepancy=round(diff, 2),
                        threshold=cls.TOLERANCE_ABSOLUTE,
                        message=f"Reported gross profit differs from calculated (Rev - COGS) by {diff:,.1f}.",
                        suggested_fix="Verify if depreciation is classified inside COGS or Operating Expenses."
                    ))

            # 3. Cash Flow Reconciliation: Beginning Cash + Net CF ≈ Ending Cash
            beg_cash = statements.beginning_cash.get(period)
            cfo = statements.cash_from_operations.get(period)
            cfi = statements.cash_from_investing.get(period)
            cff = statements.cash_from_financing.get(period)
            end_cash = statements.ending_cash.get(period)

            if all(v is not None for v in [beg_cash, cfo, cfi, cff, end_cash]):
                net_cf = cfo + cfi + cff
                expected_end = beg_cash + net_cf
                diff = abs(end_cash - expected_end)
                if diff > max(cls.TOLERANCE_ABSOLUTE, 5.0): # Allow currency exchange impact
                    alerts.append(ValidationAlert(
                        rule_name="Cash Flow Net Change Reconciliation",
                        period=period,
                        status=ValidationStatus.WARNING,
                        expected_expression=f"Beg Cash ({beg_cash:,.1f}) + Net CF ({net_cf:,.1f}) = End Cash ({end_cash:,.1f})",
                        actual_expression=f"Unreconciled Variance: {diff:,.2f}",
                        discrepancy=round(diff, 2),
                        threshold=5.0,
                        message=f"Cash flow waterfall does not match closing cash by {diff:,.1f}.",
                        suggested_fix="Examine foreign exchange translation effects or discontinued operations cash adjustments."
                    ))

        return overall_status, alerts
