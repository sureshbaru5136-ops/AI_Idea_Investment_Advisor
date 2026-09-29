from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import re

app = FastAPI(title="AI Idea Investment Advisor", version="1.0.0")


class IdeaRequest(BaseModel):
    idea: str = Field(min_length=5, max_length=1000)
    country: str = Field(min_length=2, max_length=100)
    investment: float = Field(gt=0)
    target_customers: str = Field(min_length=2, max_length=300)
    industry: str = Field(min_length=2, max_length=100)


INDUSTRY_DEMAND = {
    "ai": 88, "artificial intelligence": 90, "education": 82,
    "health": 86, "healthcare": 86, "fintech": 84,
    "agriculture": 78, "agritech": 80, "ecommerce": 76,
    "software": 84, "security": 83, "cybersecurity": 86,
    "logistics": 77, "climate": 79, "energy": 78
}

HIGH_COMPETITION = {
    "ecommerce": 78, "fintech": 76, "education": 65,
    "software": 68, "ai": 62, "healthcare": 58,
    "agriculture": 48, "logistics": 55, "climate": 45
}


def keyword_score(text: str, mapping: dict, default: int = 55) -> int:
    t = text.lower()
    matches = [score for key, score in mapping.items() if key in t]
    return max(matches) if matches else default


def analyze(data: IdeaRequest):
    text = f"{data.idea} {data.industry} {data.target_customers}".lower()

    demand = keyword_score(text, INDUSTRY_DEMAND, 60)

    # More unique/product-specific wording slightly improves the demo differentiation score.
    unique_terms = {
        "ai", "machine learning", "automation", "personalized",
        "drone", "blockchain", "iot", "predictive", "rural", "smart"
    }
    innovation = min(95, 45 + sum(5 for term in unique_terms if term in text))

    competition = keyword_score(data.industry, HIGH_COMPETITION, 55)

    # Larger capital can support execution, but excessive capital raises risk in this prototype.
    if data.investment < 100000:
        capital_factor = 58
    elif data.investment < 1000000:
        capital_factor = 78
    elif data.investment < 5000000:
        capital_factor = 72
    else:
        capital_factor = 62

    profit = round(
        0.35 * demand +
        0.30 * innovation +
        0.20 * (100 - competition) +
        0.15 * capital_factor
    )

    risk = round(100 - (0.40 * demand + 0.30 * innovation + 0.30 * (100 - competition)))

    if profit >= 75:
        recommendation = "Strong opportunity signals in this prototype analysis"
    elif profit >= 60:
        recommendation = "Moderate opportunity signals; validate the market before investing"
    else:
        recommendation = "Needs stronger validation and differentiation"

    strengths = []
    if demand >= 75:
        strengths.append("The selected industry shows strong demand signals in the prototype.")
    if innovation >= 65:
        strengths.append("The idea contains technology or differentiation keywords.")
    if competition < 60:
        strengths.append("Competition is relatively lower in the prototype model.")

    improvements = [
        "Interview potential customers and validate the problem before building.",
        "Compare at least 3 direct and 3 indirect competitors.",
        "Create a small MVP and measure user adoption.",
        "Estimate customer acquisition cost, operating cost and expected revenue separately."
    ]

    return {
        "idea": data.idea,
        "country": data.country,
        "industry": data.industry,
        "target_customers": data.target_customers,
        "investment": data.investment,
        "scores": {
            "market_demand": demand,
            "innovation": innovation,
            "competition": competition,
            "profit_potential": profit,
            "risk": risk
        },
        "recommendation": recommendation,
        "strengths": strengths or ["The idea needs additional market-specific validation."],
        "improvements": improvements
    }


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.post("/analyze")
def analyze_idea(data: IdeaRequest):
    return analyze(data)


app.mount("/static", StaticFiles(directory="static"), name="static")
