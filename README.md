# AI Idea Investment Advisor

An AI/ML student project that analyzes a startup/business idea using industry, target customers, region, and investment amount, then produces an explainable market-opportunity report.

## Features
- Business idea analysis form
- Investment, region, industry and target-customer inputs
- Demand, competition, profit-potential and risk scores
- Explainable recommendation summary
- FastAPI backend
- Simple HTML/CSS/JavaScript frontend
- No paid API required

## Tech Stack
- Python
- FastAPI
- Pydantic
- HTML, CSS, JavaScript

## Project Structure
```text
AI-Idea-Investment-Advisor/
├── main.py
├── requirements.txt
├── README.md
└── static/
    ├── index.html
    ├── style.css
    └── script.js
```

## Run Locally

1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start the API:

```bash
uvicorn main:app --reload
```

5. Open:

```text
http://127.0.0.1:8000
```

## API
POST `/analyze`

Example JSON:
```json
{
  "idea": "AI tutor for school students",
  "country": "India",
  "investment": 500000,
  "target_customers": "school students",
  "industry": "Education"
}
```

## Important
This is an educational prototype. Scores are heuristic/demo estimates and should not be treated as financial advice or a real investment recommendation.
