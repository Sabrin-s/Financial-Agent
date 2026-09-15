from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from enum import Enum

class ValidationStatus(str, Enum):
    PASS = "PASS"
    WARNING = "WARNING"
    FAIL = "FAIL"

class RiskLevel(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class MetricSource(BaseModel):
    document_name: str
    page_number: int
    raw_text: Optional[str] = None
    confidence: float = 0.95

class MetricItem(BaseModel):
    name: str
    period: str  # e.g. "2023", "2024", "2025"
    value: float
    unit: str = "₹ Cr"  # or "$ M", customizable
    source: Optional[MetricSource] = None

class FinancialStatements(BaseModel):
    # Income Statement
    revenue: Dict[str, float] = Field(default_factory=dict, description="Period to Revenue")
    cost_of_goods_sold: Dict[str, float] = Field(default_factory=dict)
    gross_profit: Dict[str, float] = Field(default_factory=dict)
    operating_expenses: Dict[str, float] = Field(default_factory=dict)
    operating_income: Dict[str, float] = Field(default_factory=dict)
    interest_expense: Dict[str, float] = Field(default_factory=dict)
    tax_expense: Dict[str, float] = Field(default_factory=dict)
    net_profit: Dict[str, float] = Field(default_factory=dict)
    
    # Balance Sheet
    cash_and_equivalents: Dict[str, float] = Field(default_factory=dict)
    accounts_receivable: Dict[str, float] = Field(default_factory=dict)
    inventory: Dict[str, float] = Field(default_factory=dict)
    current_assets: Dict[str, float] = Field(default_factory=dict)
    non_current_assets: Dict[str, float] = Field(default_factory=dict)
    total_assets: Dict[str, float] = Field(default_factory=dict)
    
    current_liabilities: Dict[str, float] = Field(default_factory=dict)
    short_term_debt: Dict[str, float] = Field(default_factory=dict)
    long_term_debt: Dict[str, float] = Field(default_factory=dict)
    total_debt: Dict[str, float] = Field(default_factory=dict)
    total_liabilities: Dict[str, float] = Field(default_factory=dict)
    shareholders_equity: Dict[str, float] = Field(default_factory=dict)
    
    # Cash Flow Statement
    cash_from_operations: Dict[str, float] = Field(default_factory=dict)
    capital_expenditures: Dict[str, float] = Field(default_factory=dict)
    cash_from_investing: Dict[str, float] = Field(default_factory=dict)
    cash_from_financing: Dict[str, float] = Field(default_factory=dict)
    beginning_cash: Dict[str, float] = Field(default_factory=dict)
    ending_cash: Dict[str, float] = Field(default_factory=dict)

    # Line item sources & provenance
    sources: Dict[str, MetricSource] = Field(default_factory=dict)

class RatioItem(BaseModel):
    category: str
    name: str
    value: float
    unit: str = "%"
    formula: str
    calculation_steps: str
    benchmark: Optional[str] = None
    status: str = "NORMAL"  # "HEALTHY", "WARNING", "CRITICAL"
    interpretation: Optional[str] = None

class ValidationAlert(BaseModel):
    rule_name: str
    period: str
    status: ValidationStatus
    expected_expression: str
    actual_expression: str
    discrepancy: float
    threshold: float
    message: str
    suggested_fix: Optional[str] = None

class TrendMetric(BaseModel):
    metric_name: str
    historical_values: Dict[str, float]
    cagr_or_growth: float
    direction: str  # "UP", "DOWN", "FLAT"
    is_positive_development: bool
    ai_commentary: str

class RiskIndicator(BaseModel):
    id: str
    category: str
    severity: RiskLevel
    title: str
    metric_evidence: str
    formula_or_rule: str
    ai_explanation: str

class Citation(BaseModel):
    document_name: str
    page_number: int
    snippet: str
    relevance_score: float

class AgentStepLog(BaseModel):
    agent_name: str
    status: str  # "pending", "running", "completed", "warning"
    timestamp: str
    summary: str
    details: Optional[Any] = None

class CompanyAnalysisState(BaseModel):
    company_id: str
    company_name: str
    currency_unit: str = "₹ Cr"
    periods: List[str]
    document_metadata: List[Dict[str, Any]] = Field(default_factory=list)
    raw_statements: FinancialStatements
    validation_status: ValidationStatus
    validation_alerts: List[ValidationAlert] = Field(default_factory=list)
    calculated_ratios: Dict[str, List[RatioItem]] = Field(default_factory=dict) # category -> ratios for latest period
    trends: List[TrendMetric] = Field(default_factory=list)
    overall_risk_score: float # 0 to 100
    overall_risk_level: RiskLevel
    risk_indicators: List[RiskIndicator] = Field(default_factory=list)
    executive_summary: str
    ai_interpretation: str
    agent_logs: List[AgentStepLog] = Field(default_factory=list)
