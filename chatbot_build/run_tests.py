"""Test harness for the GFC financial chatbot. Captures responses to sample queries."""
from chatbot import simple_chatbot

test_queries = [
    "What is the total revenue of Microsoft?",
    "How has net income changed over the last year for Tesla?",
    "What are the total assets of Apple?",
    "What are the total liabilities of Microsoft?",
    "What is the cash flow from operating activities of Tesla?",
    "Give me a financial summary of Apple",
    "revenue AAPL",
    "How is the weather today?",          # unrecognized query -> error handling
    "What is the revenue?",               # no company mentioned
    "hello",                              # greeting -> help menu
]

lines = []
lines.append("=" * 70)
lines.append("GFC FINANCIAL CHATBOT - TEST RESULTS")
lines.append("=" * 70)
for i, q in enumerate(test_queries, 1):
    lines.append(f"\n[Test {i}] User: {q}")
    lines.append(f"Bot: {simple_chatbot(q)}")

output = "\n".join(lines)
print(output)
with open("test_results.txt", "w", encoding="utf-8") as f:
    f.write(output + "\n")
