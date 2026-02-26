from crewai import Task
from app.agents import financial_analyst

# Financial Analysis Task (Single task approach)
analyze_financial_document = Task(
    description="""
    You are a Chartered Financial Analyst with 20 years of experience. Analyze the financial document and answer the user's query.

    User query: {query}
    Document text: {document_text}

    Instructions:
    1. First, verify if this is a financial document by looking for financial terms like:
       - revenue, income, profit, loss
       - balance sheet, assets, liabilities
       - cash flow, expenses, earnings
       - financial ratios, margins, growth

    2. If it is a financial document, extract key financial metrics:
       - Revenue and revenue trends
       - Profit margins (gross, operating, net)
       - Key ratios (liquidity, solvency, efficiency)
       - Growth rates year over year

    3. Analyze the company's financial health:
       - Is the company profitable?
       - Are revenues growing or declining?
       - Is the company carrying too much debt?
       - What are the key strengths and weaknesses?

    4. Answer the user's query specifically and completely.

    5. Provide actionable recommendations based on the analysis.

    Format your response with these clear sections:

    EXECUTIVE SUMMARY
    [Brief overview of findings]

    DOCUMENT VERIFICATION
    [Is this a financial document? What type?]

    KEY FINANCIAL METRICS
    [Extracted metrics in a structured format]

    FINANCIAL HEALTH ASSESSMENT
    [Detailed analysis of company's financial position]

    ANSWER TO USER QUERY
    [Specific answer to: {query}]

    RECOMMENDATIONS
    [Actionable insights and suggestions]

    If the document doesn't contain financial data, clearly state that and explain what the document appears to be instead.
    """,
    expected_output="A comprehensive financial analysis report with all required sections",
    agent=financial_analyst
)

print("✅ Tasks created successfully")