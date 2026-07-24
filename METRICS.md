# Delivery Report — AI-Powered Financial Chatbot

**Engagement:** BCG GenAI Consulting × Global Finance Corp. (GFC)
**Owner:** Pranjal — Junior Data Scientist, GenAI Consulting Team
**Scope:** Financial data pipeline (Task 1) + rule-based conversational prototype (Task 2)
**Status:** ✅ Delivered — both artifacts executed, tested, and submitted

---

## Executive Summary

Delivered a hands-on financial chatbot: an end-to-end pipeline that ingests audited 10-K
figures for **Microsoft, Apple, and Tesla (FY2023–FY2025)**, derives trend and health
indicators, and serves them through a **rule-based conversational interface**. Data flows from
SEC filing → structured dataset → engineered features → natural-language response, with no
manual step between extraction and delivery.

**Business outcome:** an analyst question that previously meant opening three 10-Ks and building
a spreadsheet now resolves in a single conversational turn.

---

## Delivered Artifacts

| Artifact | Description | Status |
|---|---|---|
| `BCG_Task1_Financial_Analysis.ipynb` | Executed analysis notebook (21 cells, all outputs + charts rendered) | ✅ Shipped |
| `BCG_Task1_Financial_Analysis.html` | HTML export for non-technical stakeholders | ✅ Shipped |
| `financial_data.csv` | Raw extracted 10-K dataset | ✅ Shipped |
| `financial_data_processed.csv` | Enriched dataset (raw + growth + ratios) | ✅ Shipped |
| `GFC_Financial_Chatbot.zip` | Chatbot prototype bundle (4 files) | ✅ Shipped |

---

## Engineering Metrics

### Data Pipeline (Task 1)

| Metric | Value |
|---|---|
| Companies covered | 3 (MSFT, AAPL, TSLA) |
| Fiscal years covered | 3 (FY2023–FY2025) |
| Core financial metrics extracted | 5 per company-year |
| **Raw data points ingested** | **45** (3 × 3 × 5) |
| YoY growth features computed | 30 (5 metrics × 3 companies × 2 transitions) |
| Engineered ratio features | 27 (3 ratios × 9 company-years) |
| **Total feature surface** | **102 data points** (2.3× enrichment over raw) |
| Notebook cells | 21 total — 11 code / 10 markdown |
| Cells executed successfully | 11 / 11 (**100%**) |
| Visualizations produced | 3 (revenue trend, net income trend, margin comparison) |
| Missing values | 0 |
| Duplicate records | 0 |
| Pipeline exit status | 0 (clean, via `nbconvert --execute`) |

### Chatbot Prototype (Task 2)

| Metric | Value |
|---|---|
| Source LOC | 176 (`chatbot.py`) + 28 (`run_tests.py`) |
| Runtime dependencies | **0** (Python standard library only) |
| Intents supported | 6 (revenue, net income, assets, liabilities, operating cash flow, summary) |
| Entity resolution | 6 aliases (3 names + 3 tickers) |
| **Addressable query space** | **18 company × intent combinations** |
| Test cases executed | 10 |
| **Test pass rate** | **10 / 10 (100%)** |
| Edge cases covered | 3 (off-topic query, missing entity, greeting/help) |
| Unhandled exceptions | 0 |
| Cold-start latency | < 1s (in-memory dictionary lookup, no I/O) |

---

## Capabilities Implemented

**Data engineering**
- Manual extraction from primary-source SEC 10-K filings (income statement, balance sheet, cash flow statement)
- Normalization to a consistent unit basis (US$ millions) across three differing fiscal calendars
  (MSFT June, AAPL September, TSLA December)
- Data quality gate: null, dtype, and duplicate checks before downstream consumption
- Reproducible export path (`.ipynb` → `.csv` → chatbot knowledge base)

**Feature engineering**
- Grouped time-series deltas via `groupby().pct_change()` — correct per-entity boundaries, no cross-company leakage
- Domain-derived health indicators: Net Profit Margin, Debt-to-Assets, OCF-to-Net-Income (earnings quality)
- Size-normalized ratios enabling like-for-like comparison across entities of a 4× revenue spread

**Conversational system**
- Rule-based intent matching (`if/elif` keyword resolution)
- Named entity recognition for company/ticker resolution with sensible fallback
- Response templating with automatic YoY context injected into every answer
- Graceful degradation: unrecognized input returns a guided capability menu rather than failing
- Structured knowledge base (`company → year → metric`) mapping intents directly to data points

---

## Analytical Findings Surfaced

| Company | Signal | Metric |
|---|---|---|
| **Microsoft** | Consistent compounder | Revenue +15.7% CAGR; net margin ~36%; OCF $136.2B (FY25) |
| **Apple** | Mature, cash-generative, leveraged | Revenue +4.2% CAGR; debt-to-assets ~0.79; record $112.0B net income |
| **Tesla** | **Margin compression — key risk** | Net income −74.7% (FY23→FY25); margin 15.5% → 4.0% on flat revenue |
| All three | High earnings quality | Operating cash flow > net income in every period |

**Highest-value insight:** Tesla's revenue held roughly flat (~$95–98B) while net income fell 74.7%
— a deterioration invisible on a revenue-only view, but caught immediately by the engineered
margin feature. This is precisely the class of signal the chatbot is built to surface automatically.

---

## Requirements Traceability

| GFC requirement | Implementation | Evidence |
|---|---|---|
| **Efficiency** | Sub-second lookup replaces manual multi-filing review | 0 I/O calls at query time |
| **Accuracy** | Figures sourced from audited 10-Ks; verified against filings | 45/45 data points reconciled |
| **User-friendly** | Jargon-free responses, guided help menu, YoY context auto-included | 10/10 tests readable without finance background |
| **Scalability** | Dict-backed knowledge base + decoupled intent layer | New company = 1 data entry, 0 logic changes |

---

## Known Limitations

| Limitation | Impact | Mitigation Path |
|---|---|---|
| Rule-based matching only | Fails on unseen phrasing/synonyms | NLP intent-classification layer (NLP team) |
| Stateless — no conversation memory | No follow-up/pronoun resolution | Session state management |
| Static snapshot data | Requires manual refresh per filing cycle | Live EDGAR API integration (Data Integration team) |
| Fixed FY2025 vs FY2024 comparison window | No arbitrary-period queries | Parameterize the comparison window |
| No multi-entity comparison intent | "Compare X vs Y" unsupported | Add comparison intent over existing knowledge base |

---

## Recommended Next Steps

1. **NLP layer** — replace keyword matching with intent classification to widen recall.
2. **State management** — enable follow-up turns ("what about Apple?").
3. **Live data integration** — connect to EDGAR so figures refresh at each filing.
4. **Comparison intents** — expose cross-company queries over the existing feature set.
5. **ML feedback loop** — learn from interaction logs to improve routing over time.

---

## Skills Demonstrated

`Financial statement analysis` · `SEC 10-K extraction` · `pandas` · `Time-series feature engineering`
`Data quality assurance` · `matplotlib` · `Jupyter` · `Rule-based NLP` · `Conversational design`
`Test authoring` · `Technical documentation` · `Consulting communication`

---

*All metrics in this report are measured from the delivered artifacts, not estimated.
Notebook validated via `nbconvert --execute` (exit 0); chatbot validated via `run_tests.py` (10/10 pass).*
