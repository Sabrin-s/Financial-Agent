# FinSight AI — Multi-Agent Financial Intelligence Platform

> **Institutional-grade multi-agent financial statement analysis and risk intelligence system.** Built on the core principle:
> **"Deterministic code calculates and validates numbers; LLMs orchestrate, reason, explain, and ground analysis in audited annual reports."**

---

## 🌟 Key Innovations

1. **Deterministic Calculation Engine**: Zero hallucination risk for financial ratios (Operating Margin, ROE, Current Ratio, Debt-to-Equity, FCF). Every ratio provides a step-by-step arithmetic breakdown.
2. **Financial Validation Agent**: Automated double-entry reconciliation checks ($Assets = Liabilities + Equity$, $Cash_{start} + \Sigma CF = Cash_{end}$) issuing audit delta warnings.
3. **Multi-Year Trend Analysis**: Computes annualized growth (CAGR), revenue vs operating leverage divergence, and accounts receivable bloat.
4. **Risk Intelligence Engine**: Rules-based risk evaluation flagging solvency, debt cushion, and earnings quality concerns with institutional reasoning.
5. **Grounded RAG Agent**: Indexes audited MD&A and footnotes with exact page numbers and evidence snippets.
6. **Innovative Light/Dark Dashboard**: High-contrast glassmorphic financial UI with real-time agent execution pipeline tracking and formula inspector.

---

## 🏗️ Architecture

```text
                  ┌─────────────────────────────────────────┐
                  │    React + Vite + Vanilla CSS UI        │
                  │       (Light & Dark Mode)               │
                  └──────────────────┬──────────────────────┘
                                     │ (REST API)
                                     ▼
                  ┌─────────────────────────────────────────┐
                  │          FastAPI Backend                │
                  └──────────────────┬──────────────────────┘
                                     │
       ┌─────────────────────────────┼─────────────────────────────┐
       ▼                             ▼                             ▼
  Document Agent              Validation Agent             Calculation Engine
(PyMuPDF Table Parser)      (Accounting Integrity)       (Pure Math Ratios)
       │                             │                             │
       └─────────────────────────────┼─────────────────────────────┘
                                     ▼
                            Trend & Risk Agents
                         (Multi-year CAGR & Rules)
                                     ▼
                            Grounded RAG Agent
                      (Page-level Footnote Citations)
                                     ▼
                            Report Writer Agent
                        (Executive Memorandum)
```

---

## 🚀 Quickstart Guide

### 1. Start FastAPI Backend
```bash
cd "backend"
# Set python path and start uvicorn server
$env:PYTHONPATH = "."
python -m uvicorn app.main:app --reload --port 8000
```
API Documentation will be available at: `http://localhost:8000/docs`

### 2. Start Vite Frontend
```bash
cd "frontend"
npm install
npm run dev
```
Dashboard will be available at: `http://localhost:5173`

---

## 🧪 Running Automated Tests
```bash
cd "backend"
$env:PYTHONPATH = "."
python -m pytest tests/test_financial_agents.py
```
