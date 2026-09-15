import pytest
from app.models.financial_schema import FinancialStatements, ValidationStatus
from app.agents.calculation_engine import DeterministicCalculationEngine
from app.agents.validation_agent import ValidationAgent
from app.agents.trend_agent import TrendAnalysisAgent
from app.agents.risk_agent import RiskIntelligenceAgent

def test_calculation_engine():
    statements = FinancialStatements(
        revenue={"2025": 1000.0},
        gross_profit={"2025": 400.0},
        operating_income={"2025": 150.0},
        net_profit={"2025": 100.0},
        current_assets={"2025": 500.0},
        current_liabilities={"2025": 250.0},
        inventory={"2025": 100.0},
        total_assets={"2025": 1200.0},
        shareholders_equity={"2025": 600.0},
        total_debt={"2025": 300.0},
        cash_from_operations={"2025": 120.0},
        capital_expenditures={"2025": 40.0}
    )
    ratios = DeterministicCalculationEngine.calculate_ratios(statements, "2025")
    
    # Profitability checks
    gm = next(r for r in ratios["Profitability"] if r.name == "Gross Profit Margin")
    assert gm.value == 40.0
    
    om = next(r for r in ratios["Profitability"] if r.name == "Operating Margin")
    assert om.value == 15.0
    
    # Liquidity checks
    cr = next(r for r in ratios["Liquidity"] if r.name == "Current Ratio")
    assert cr.value == 2.0
    
    # Leverage checks
    de = next(r for r in ratios["Leverage"] if r.name == "Debt-to-Equity (D/E)")
    assert de.value == 0.5

def test_validation_agent_balance_sheet():
    # Balanced case
    balanced = FinancialStatements(
        total_assets={"2025": 1000.0},
        total_liabilities={"2025": 600.0},
        shareholders_equity={"2025": 400.0}
    )
    status, alerts = ValidationAgent.validate_statements(balanced, ["2025"])
    assert status == ValidationStatus.PASS
    assert len(alerts) == 0

    # Unbalanced case
    unbalanced = FinancialStatements(
        total_assets={"2025": 1000.0},
        total_liabilities={"2025": 700.0},
        shareholders_equity={"2025": 400.0} # 700 + 400 = 1100 != 1000
    )
    status, alerts = ValidationAgent.validate_statements(unbalanced, ["2025"])
    assert status in [ValidationStatus.WARNING, ValidationStatus.FAIL]
    assert len(alerts) >= 1
