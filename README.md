## 📝 **You're Absolutely Right! Let Me Give You a Natural, Human-Written README**

Here's a README that sounds like you actually wrote it yourself:

---

# Financial Document Analyzer - VWO GenAI Debug Challenge

## What is this?
A tool that reads financial documents (like company reports) and tells you if a company is doing well financially. You upload a PDF or text file, ask a question, and the AI analyzes it.

## What I Fixed

### The Bugs I Found

| What Was Broken | Where | What I Did |
|-----------------|-------|------------|
| API key not working | `.env` file | Saved file correctly without hidden characters |
| No error when key missing | `agents.py` | Added proper error messages |
| Wrong AI model | `agents.py` | Changed to working "gemma-3-27b-it" model |
| Tool import errors | `tools.py` | Simplified the code |
| Task dependencies | `tasks.py` | Made it simpler with one task |
| Agent setup | `agents.py` | Fixed how agents are created |
| PDF reading | `tools.py` | Added fallback for corrupted files |

### The Prompts I Improved

| Problem | What I Changed |
|---------|----------------|
| Agent role was vague | Gave it a clear identity (CFA with 20 years experience) |
| Instructions were unclear | Added step-by-step guidance |
| No structure in answers | Made it return organized sections |
| Error messages were bad | Now explains what went wrong simply |

## How to Run It

### What You Need
- Python 3.10 or newer
- A Google API key (free from Google AI Studio)

### Steps

```bash
# 1. Download the code
git clone https://github.com/VADANEAMRUTA/vwo-genai-debug-challenge.git
cd vwo-genai-debug-challenge

# 2. Set up Python
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 3. Install requirements
pip install -r requirements.txt

# 4. Add your API key
echo "GOOGLE_API_KEY=your_key_here" > .env

# 5. Start the server
python -m app.main
```

Then open `http://localhost:8000/docs` in your browser.

## How to Use It

### Check if it's working
```bash
curl http://localhost:8000/health
```

### Analyze a document
```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@company_report.pdf" \
  -F "query=Is this company profitable?"
```

### What you'll get back
The response has clear sections:
- **Executive Summary** - Quick overview
- **Key Financial Metrics** - The important numbers
- **Financial Health Assessment** - Is the company doing well?
- **Answer to your question** - Direct response
- **Recommendations** - What to do next

## Try it with a sample

Create a test file:
```
echo "Revenue: $10M, Profit: $2M" > test.txt
```

Then run:
```
curl -X POST "http://localhost:8000/analyze" -F "file=@test.txt" -F "query=Is this profitable?"
```

## Project Structure
```
├── app/
│   ├── agents.py     # AI agent setup
│   ├── tasks.py      # What the AI does
│   ├── tools.py      # Reads PDFs/text files
│   └── main.py       # The API server
├── requirements.txt  # What to install
├── .env.example     # Template for API key
└── README.md        # This file
```

## Things to Know

| Issue | What Happens |
|-------|--------------|
| PDF doesn't work | Falls back to reading as text |
| API limits reached | Free tier has daily limits (20-1500 requests) |
| File too large | Best with documents under 100 pages |

## What's Working
- [x] Server starts without errors
- [x] Health check works
- [x] File upload works
- [x] AI analyzes documents
- [x] Error handling works

## About Me
- **Name**: Amruta Sakharam Vadane
- **Applied for**: Intern - Generative AI at VWO
- **Date**: 26 February 2026

## My GitHub
https://github.com/VADANEAMRUTA

---

**Thanks for reviewing my work!** 🚀