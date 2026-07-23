# GFC AI-Powered Financial Chatbot — Prototype Documentation

**Project:** BCG GenAI Consulting — AI-Powered Financial Chatbot for Global Finance Corp. (GFC)
**Task 2:** Rule-based chatbot prototype
**Author:** Pranjal — Junior Data Scientist, GenAI Consulting Team

---

## 1. Overview
This is a **rule-based chatbot prototype** that answers predefined financial queries about
**Microsoft, Apple, and Tesla**. It uses the financial data extracted and analyzed in Task 1
(sourced from each company's 10-K filings, **FY2023–FY2025**), turning static financial data
into interactive, conversational insights.

## 2. How It Works
The chatbot uses simple **rule-based (if-else) logic**:

1. **Input handling** — the user's question is converted to lowercase and stripped of whitespace.
2. **Company detection** — the bot scans the query for a company name or ticker
   (Microsoft/MSFT, Apple/AAPL, Tesla/TSLA).
3. **Query matching** — keyword matching (`if`/`elif`) maps the question to a predefined
   data point (revenue, net income, assets, liabilities, or operating cash flow).
4. **Response generation** — the bot retrieves the relevant figure from a structured Python
   dictionary (`financial_data`), formats it, and adds year-over-year context.
5. **Error handling** — unrecognized queries return a helpful message that guides the user
   toward supported questions.

Data is stored in a nested **dictionary** structure (`company → year → metric`), which acts as
the chatbot's knowledge base and maps each predefined query directly to a specific data point.

## 3. Predefined Queries Supported
The chatbot can respond to the following (for any of the three companies):

| # | Example query | Data point returned |
|---|---------------|---------------------|
| 1 | "What is the total revenue of Microsoft?" | Total Revenue (+ YoY change) |
| 2 | "How has net income changed over the last year for Tesla?" | Net Income change YoY |
| 3 | "What are the total assets of Apple?" | Total Assets (+ YoY change) |
| 4 | "What are the total liabilities of Microsoft?" | Total Liabilities (+ YoY change) |
| 5 | "What is the cash flow from operating activities of Tesla?" | Operating Cash Flow (+ YoY change) |
| 6 | "Give me a financial summary of Apple" | Full FY2025 snapshot + net margin |

It also recognizes greetings ("hi", "hello", "help") and shows a menu of supported questions.

## 4. How to Run
```bash
# Requires Python 3 (no external libraries needed)
python chatbot.py
```
Then type a question at the `You:` prompt. Type `exit` to quit.

To reproduce the automated test results:
```bash
python run_tests.py
```

## 5. Files Included
| File | Description |
|------|-------------|
| `chatbot.py` | The chatbot script (data + rule-based logic + interactive CLI) |
| `run_tests.py` | Automated test harness that runs sample queries |
| `test_results.txt` | Captured output demonstrating the chatbot's responses |
| `README.md` | This documentation |

## 6. Limitations
- **Rule-based only** — it matches predefined keywords, so it cannot understand free-form
  natural language or answer questions outside its predefined set.
- **No true NLP** — synonyms or unusual phrasing may not be recognized (that layer is being
  built by the NLP team).
- **Static data** — the data is a fixed snapshot from the 10-K filings (FY2023–FY2025); it does
  not update in real time.
- **No memory/state** — each query is handled independently; the bot does not remember prior
  turns in the conversation.
- **Fixed comparison window** — "over the last year" compares FY2025 vs FY2024.

## 7. Next Steps (Roadmap)
- Add an **NLP layer** (e.g., intent recognition) to handle varied phrasing.
- Introduce **conversation state management** for follow-up questions.
- Connect to a **live data source** so figures update automatically.
- Add **machine learning** so the bot improves from user interactions and handles complex,
  multi-company comparison queries.
