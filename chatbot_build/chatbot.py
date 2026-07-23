"""
BCG GenAI Consulting - Task 2
AI-Powered Financial Chatbot (Rule-Based Prototype)
---------------------------------------------------
A simple rule-based chatbot that answers predefined financial queries
about Microsoft, Apple, and Tesla using data extracted and analyzed in Task 1
(sourced from each company's 10-K filings, FY2023-FY2025).

Author: Pranjal - Junior Data Scientist, BCG GenAI Consulting Team
"""

# ---------------------------------------------------------------------------
# 1. FINANCIAL DATA  (all figures in US$ millions, from 10-K filings)
#    This dictionary maps predefined data points to each company/year.
# ---------------------------------------------------------------------------
financial_data = {
    "microsoft": {
        "2023": {"revenue": 211915, "net_income": 72361, "assets": 411976,
                 "liabilities": 205753, "operating_cash_flow": 87582},
        "2024": {"revenue": 245122, "net_income": 88136, "assets": 512163,
                 "liabilities": 243686, "operating_cash_flow": 118548},
        "2025": {"revenue": 281724, "net_income": 101832, "assets": 619003,
                 "liabilities": 275524, "operating_cash_flow": 136162},
    },
    "apple": {
        "2023": {"revenue": 383285, "net_income": 96995, "assets": 352583,
                 "liabilities": 290437, "operating_cash_flow": 110543},
        "2024": {"revenue": 391035, "net_income": 93736, "assets": 364980,
                 "liabilities": 308030, "operating_cash_flow": 118254},
        "2025": {"revenue": 416161, "net_income": 112010, "assets": 359241,
                 "liabilities": 285508, "operating_cash_flow": 111482},
    },
    "tesla": {
        "2023": {"revenue": 96773, "net_income": 14997, "assets": 106618,
                 "liabilities": 43009, "operating_cash_flow": 13256},
        "2024": {"revenue": 97690, "net_income": 7091, "assets": 122070,
                 "liabilities": 48390, "operating_cash_flow": 14923},
        "2025": {"revenue": 94827, "net_income": 3794, "assets": 137806,
                 "liabilities": 54941, "operating_cash_flow": 14747},
    },
}

LATEST_YEAR = "2025"
PREVIOUS_YEAR = "2024"


# ---------------------------------------------------------------------------
# 2. HELPER FUNCTIONS
# ---------------------------------------------------------------------------
def money(value):
    """Format a US$ millions figure into a readable string (e.g., $281.7B)."""
    return f"${value:,} million (~${value/1000:.1f}B)"


def pct_change(new, old):
    """Return the percentage change from old to new."""
    return (new - old) / old * 100


def detect_company(text):
    """Find which company the user is asking about (defaults to Microsoft)."""
    for company in financial_data:
        if company in text:
            return company
    # allow common tickers
    tickers = {"msft": "microsoft", "aapl": "apple", "tsla": "tesla"}
    for ticker, company in tickers.items():
        if ticker in text:
            return company
    return None


# ---------------------------------------------------------------------------
# 3. RULE-BASED CHATBOT LOGIC (if-else matching of predefined queries)
# ---------------------------------------------------------------------------
def simple_chatbot(user_query):
    """Match the user's query to a predefined response using rule-based logic."""
    query = user_query.lower().strip()

    # --- Greetings / help ---
    if query in ("hi", "hello", "hey", "help", "menu"):
        return help_message()

    # Identify the company being asked about
    company = detect_company(query)
    if company is None:
        return ("Please mention a company: Microsoft, Apple, or Tesla.\n"
                "Example: 'What is the total revenue of Apple?'")

    latest = financial_data[company][LATEST_YEAR]
    prev = financial_data[company][PREVIOUS_YEAR]
    name = company.capitalize()

    # --- Query 1: Total Revenue ---
    if "revenue" in query:
        change = pct_change(latest["revenue"], prev["revenue"])
        return (f"{name}'s total revenue for FY{LATEST_YEAR} was {money(latest['revenue'])}, "
                f"{'up' if change >= 0 else 'down'} {abs(change):.1f}% from FY{PREVIOUS_YEAR} "
                f"({money(prev['revenue'])}).")

    # --- Query 2: Net Income change over the last year ---
    elif "net income" in query or "profit" in query or "earnings" in query:
        change = pct_change(latest["net_income"], prev["net_income"])
        direction = "increased" if change >= 0 else "decreased"
        return (f"{name}'s net income {direction} by {abs(change):.1f}% over the last year, "
                f"from {money(prev['net_income'])} in FY{PREVIOUS_YEAR} to "
                f"{money(latest['net_income'])} in FY{LATEST_YEAR}.")

    # --- Query 3: Total Assets ---
    elif "asset" in query:
        change = pct_change(latest["assets"], prev["assets"])
        return (f"{name}'s total assets for FY{LATEST_YEAR} were {money(latest['assets'])}, "
                f"a change of {change:+.1f}% versus FY{PREVIOUS_YEAR} ({money(prev['assets'])}).")

    # --- Query 4: Total Liabilities ---
    elif "liabilit" in query or "debt" in query:
        change = pct_change(latest["liabilities"], prev["liabilities"])
        return (f"{name}'s total liabilities for FY{LATEST_YEAR} were {money(latest['liabilities'])}, "
                f"a change of {change:+.1f}% versus FY{PREVIOUS_YEAR} ({money(prev['liabilities'])}).")

    # --- Query 5: Cash Flow from Operating Activities ---
    elif "cash flow" in query or "operating" in query or "cash" in query:
        change = pct_change(latest["operating_cash_flow"], prev["operating_cash_flow"])
        return (f"{name}'s cash flow from operating activities for FY{LATEST_YEAR} was "
                f"{money(latest['operating_cash_flow'])}, a change of {change:+.1f}% "
                f"versus FY{PREVIOUS_YEAR} ({money(prev['operating_cash_flow'])}).")

    # --- Bonus: Financial summary ---
    elif "summary" in query or "overview" in query or "health" in query:
        margin = latest["net_income"] / latest["revenue"] * 100
        return (f"FY{LATEST_YEAR} snapshot for {name}:\n"
                f"  - Revenue: {money(latest['revenue'])}\n"
                f"  - Net income: {money(latest['net_income'])} (net margin {margin:.1f}%)\n"
                f"  - Total assets: {money(latest['assets'])}\n"
                f"  - Total liabilities: {money(latest['liabilities'])}\n"
                f"  - Operating cash flow: {money(latest['operating_cash_flow'])}")

    # --- Error handling: unrecognized query ---
    else:
        return ("Sorry, I can only provide information on predefined queries.\n"
                + help_message())


def help_message():
    """Guide the user toward supported queries (graceful error handling)."""
    return (
        "Hi! I'm GFC's financial chatbot. I can answer these questions about "
        "Microsoft, Apple, or Tesla (FY2023-FY2025):\n"
        "  1. What is the total revenue of <company>?\n"
        "  2. How has net income changed over the last year for <company>?\n"
        "  3. What are the total assets of <company>?\n"
        "  4. What are the total liabilities of <company>?\n"
        "  5. What is the cash flow from operating activities of <company>?\n"
        "  6. Give me a financial summary of <company>.\n"
        "Type 'exit' to quit."
    )


# ---------------------------------------------------------------------------
# 4. INTERACTIVE COMMAND-LINE LOOP
# ---------------------------------------------------------------------------
def run():
    print("=" * 60)
    print("   GFC AI-Powered Financial Chatbot (Prototype)")
    print("=" * 60)
    print(help_message())
    while True:
        user_query = input("\nYou: ")
        if user_query.lower().strip() in ("exit", "quit", "bye"):
            print("Bot: Thank you for using the GFC financial chatbot. Goodbye!")
            break
        print("Bot:", simple_chatbot(user_query))


if __name__ == "__main__":
    run()
