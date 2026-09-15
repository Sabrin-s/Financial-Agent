import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

from app.models.financial_schema import CompanyAnalysisState, FinancialStatements, ValidationStatus
from app.agents.orchestrator import FinancialIntelligenceOrchestrator
from app.agents.document_agent import DocumentAgent
from app.samples.sample_data import SAMPLE_COMPANIES

app = FastAPI(
    title="FinSight AI API",
    description="Institutional Multi-Agent Financial Intelligence & Statement Analysis API",
    version="1.0.0"
)

# Enable CORS for local dev and frontend ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = FinancialIntelligenceOrchestrator()

# In-memory storage for analyzed companies
ANALYSIS_CACHE: Dict[str, CompanyAnalysisState] = {}

# Preload sample companies into analysis cache
for cid, sample in SAMPLE_COMPANIES.items():
    state = orchestrator.run_pipeline(
        company_id=cid,
        company_name=sample["company_name"],
        currency=sample["currency_unit"],
        periods=sample["periods"],
        statements=sample["statements"],
        mda_text=sample["annual_report_mda"]
    )
    ANALYSIS_CACHE[cid] = state

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "FinSight AI - Financial Intelligence Engine",
        "version": "1.0.0",
        "active_companies": list(ANALYSIS_CACHE.keys())
    }

@app.get("/api/companies")
def get_companies():
    """Return available preloaded & analyzed companies."""
    return [
        {
            "id": c.company_id,
            "name": c.company_name,
            "currency": c.currency_unit,
            "latest_period": sorted(c.periods)[-1],
            "risk_score": c.overall_risk_score,
            "risk_level": c.overall_risk_level,
            "validation_status": c.validation_status
        }
        for c in ANALYSIS_CACHE.values()
    ]

@app.get("/api/analysis/{company_id}", response_model=CompanyAnalysisState)
def get_company_analysis(company_id: str):
    """Fetch complete multi-agent analysis state for a specific company."""
    if company_id not in ANALYSIS_CACHE:
        raise HTTPException(status_code=404, detail=f"Company ID {company_id} not found.")
    return ANALYSIS_CACHE[company_id]

class ChatRequest(BaseModel):
    company_id: str
    question: str

@app.post("/api/chat")
def ask_grounded_question(req: ChatRequest):
    """
    RAG Agent endpoint: Semantic retrieval over the company's annual report
    producing citations with exact page numbers and evidence snippets.
    """
    if req.company_id not in ANALYSIS_CACHE:
        raise HTTPException(status_code=404, detail="Company not found")
    
    state = ANALYSIS_CACHE[req.company_id]
    summary_context = f"{state.company_name} (Risk: {state.overall_risk_level.value})"
    response = orchestrator.rag_agent.answer_query(
        query=req.question,
        company_name=state.company_name,
        financial_context_summary=summary_context
    )
    return response

@app.post("/api/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload financial PDF statement / Annual Report.
    Extracts text and tables, and returns parsed metadata.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF documents are supported.")
    
    contents = await file.read()
    try:
        parsed_doc = DocumentAgent.parse_pdf(contents, file.filename)
        return {
            "status": "success",
            "filename": file.filename,
            "total_pages": parsed_doc["total_pages"],
            "document_type": parsed_doc["document_type"],
            "tables_found": sum(len(p["tables"]) for p in parsed_doc["pages"])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF Parsing failed: {str(e)}")

class CustomAnalysisPayload(BaseModel):
    company_name: str
    currency: str = "₹ Cr"
    periods: List[str]
    statements: FinancialStatements
    annual_report_text: Optional[str] = ""

@app.post("/api/analysis/run")
def run_custom_analysis(payload: CustomAnalysisPayload):
    """
    Execute full multi-agent pipeline on user-submitted or extracted financial data.
    """
    new_cid = f"COMP-{len(ANALYSIS_CACHE) + 1}"
    state = orchestrator.run_pipeline(
        company_id=new_cid,
        company_name=payload.company_name,
        currency=payload.currency,
        periods=payload.periods,
        statements=payload.statements,
        mda_text=payload.annual_report_text or ""
    )
    ANALYSIS_CACHE[new_cid] = state
    return state
