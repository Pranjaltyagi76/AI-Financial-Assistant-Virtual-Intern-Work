# AI-Powered Financial Chatbot — BCG GenAI Consulting × Global Finance Corp. (GFC)

End-to-end project that extracts financial data from SEC 10-K filings, analyzes it for trends
and health indicators, and serves those insights through a conversational chatbot interface.

**Author:** Pranjal — Junior Data Scientist, BCG GenAI Consulting Team
**Companies analyzed:** Microsoft (MSFT), Apple (AAPL), Tesla (TSLA)
**Period:** FY2023 – FY2025
**Data source:** SEC EDGAR 10-K filings (audited, primary source)

---

## The Problem

GFC's traditional financial analysis is reliable but slow — answering a single question about a
company's performance means opening multiple 10-Ks and building a spreadsheet by hand. This
project builds the foundation for an AI tool that collapses that work into one conversational turn.

---

## Architecture

```
SEC 10-K filings
      │
      ▼
[ Task 1 ] Extraction & Analysis  ──►  BCG_Task1_Financial_Analysis.ipynb
      │                                 • data quality gate
      │                                 • YoY growth (pct_change)
      │                                 • engineered ratios
      │                                 • visualizations
      ▼
financial_data.csv / financial_data_processed.csv   ◄── structured knowledge base
      │
      ▼
[ Task 2 ] Conversational Layer  ──►  chatbot.py
                                        • entity resolution (company/ticker)
                                        • rule-based intent matching
                                        • response templating + YoY context
                                        • graceful error handling
```

Data flows one way: filing → structured dataset → engineered features → natural-language answer.

---

## Project Structure

| File | Task | Description |
|---|---|---|
| `BCG_Task1_Financial_Analysis.ipynb` | 1 | **Main analysis notebook** — extraction, cleaning, YoY trends, ratios, charts, findings (21 cells, fully executed) |
| `BCG_Task1_Financial_Analysis.html` | 1 | HTML export for non-technical stakeholders |
| `financial_data.csv` | 1 | Raw extracted 10-K dataset (45 data points) |
| `financial_data_processed.csv` | 1 | Enriched dataset — raw + growth rates + ratios |
| `chatbot_build/chatbot.py` | 2 | **Chatbot script** — rule-based logic + knowledge base + CLI |
| `chatbot_build/run_tests.py` | 2 | Automated test harness (10 cases) |
| `chatbot_build/test_results.txt` | 2 | Captured test output |
| `chatbot_build/README.md` | 2 | Chatbot-specific documentation |
| `GFC_Financial_Chatbot.zip` | 2 | Packaged Task 2 submission |
| `METRICS.md` | — | Delivery report with measured engineering metrics |

---

## Task 1 — Financial Data Extraction & Analysis

**Objective:** Extract key financial data from 10-K filings, identify trends, and prepare the data
for AI integration.

**Metrics extracted** (5 per company-year, all in US$ millions):
Total Revenue · Net Income · Total Assets · Total Liabilities · Cash Flow from Operating Activities

**What the notebook does:**
1. **Loads** the extracted 10-K data into a pandas DataFrame (also exported to CSV).
2. **Validates** data quality — shape, nulls, dtypes, duplicates (0 nulls, 0 duplicates).
3. **Computes YoY growth** for all 5 metrics using `groupby('Company').pct_change()` — grouping
   ensures no cross-company leakage at year boundaries.
4. **Engineers ratio features** that normalize for company size:
   - **Net Profit Margin** = Net Income / Revenue — profitability per dollar of sales
   - **Debt-to-Assets** = Liabilities / Assets — solvency
   - **OCF-to-Net-Income** = Operating Cash Flow / Net Income — earnings quality
5. **Visualizes** revenue trend, net income trend, and margin comparison (3 charts).
6. **Documents** findings in markdown and exports the enriched dataset.

**Normalization note:** the three companies have different fiscal calendars (Microsoft ends June,
Apple ends September, Tesla ends December). All figures were normalized to a consistent unit basis
(US$ millions) and labeled by fiscal year.

### Key Findings

| Company | FY2025 Revenue | FY2025 Net Income | Net Margin | Signal |
|---|---|---|---|---|
| **Microsoft** | $281.7B | $101.8B | ~36% | Consistent compounder (+15.7% CAGR), strong solvency |
| **Apple** | $416.2B | $112.0B | ~27% | Largest by revenue, mature growth (+4.2% CAGR), high leverage (~0.79 debt-to-assets) |
| **Tesla** | $94.8B | $3.8B | ~4% | **Margin compression** — net income −74.7% since FY23 on flat revenue |

**Headline insight:** Tesla's revenue stayed roughly flat (~$95–98B) while net income fell 74.7%
(15.5% → 4.0% margin). This deterioration is invisible on a revenue-only view but surfaces
immediately through the engineered margin feature — exactly the class of signal the chatbot exists
to catch automatically.

**Cross-company:** operating cash flow exceeded net income for all three companies in every period,
indicating high earnings quality — a useful automated health check.

### Running the notebook

```bash
pip install pandas matplotlib notebook
jupyter notebook BCG_Task1_Financial_Analysis.ipynb
```

---

## Task 2 — Rule-Based Chatbot Prototype

**Objective:** Turn the analyzed data into interactive, conversational insights.

**How it works:**
1. **Input handling** — normalize the query (lowercase, strip).
2. **Entity resolution** — detect the company from a name or ticker (Microsoft/MSFT, Apple/AAPL, Tesla/TSLA).
3. **Intent matching** — `if/elif` keyword rules map the question to a data point.
4. **Response generation** — retrieve from the `company → year → metric` dictionary, format, and
   inject YoY context automatically.
5. **Error handling** — unrecognized input returns a guided capability menu rather than failing.

**Supported intents (6):** total revenue · net income change · total assets · total liabilities ·
operating cash flow · full financial summary
→ **18 addressable query combinations** (6 intents × 3 companies)

**Sample interaction** (actual output):

> **You:** How has net income changed over the last year for Tesla?
> **Bot:** Tesla's net income decreased by 46.5% over the last year, from $7,091 million (~$7.1B)
> in FY2024 to $3,794 million (~$3.8B) in FY2025.

### Running the chatbot

```bash
cd chatbot_build
python chatbot.py      # interactive CLI — no external dependencies
python run_tests.py    # run the 10-case test suite
```

**Test status:** 10/10 passing, including 3 edge cases (off-topic query, missing company, greeting).

---

## Requirements Traceability

| GFC requirement | How it's met |
|---|---|
| **Efficiency** | Sub-second in-memory lookup replaces manual multi-filing review |
| **Accuracy** | Figures sourced from audited 10-Ks; all 45 data points reconciled to filings |
| **User-friendly** | Jargon-free responses, guided help menu, YoY context in every answer |
| **Scalability** | Dict-backed knowledge base decoupled from intent logic — a new company is 1 data entry, 0 logic changes |

---

## Limitations

- **Rule-based only** — matches predefined keywords; cannot handle free-form phrasing or synonyms.
- **Stateless** — no conversation memory, so no follow-up or pronoun resolution.
- **Static data** — a fixed 10-K snapshot (FY2023–FY2025); requires manual refresh per filing cycle.
- **Fixed comparison window** — "over the last year" means FY2025 vs FY2024.
- **No multi-entity comparison** — "compare Apple vs Tesla" is unsupported.

## Roadmap

1. **NLP layer** — intent classification to replace keyword matching and widen recall.
2. **State management** — support follow-up turns ("what about Apple?").
3. **Live data integration** — connect to the EDGAR API so figures refresh each filing cycle.
4. **Comparison intents** — cross-company queries over the existing feature set.
5. **ML feedback loop** — learn from interaction logs to improve routing.

---

## Tech Stack

`Python 3` · `pandas` · `matplotlib` · `Jupyter` · `nbconvert`
The chatbot itself has **zero external dependencies** (standard library only).

---

*See [METRICS.md](METRICS.md) for the full delivery report with measured engineering metrics.*
