const form = document.getElementById("ideaForm");
const result = document.getElementById("result");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const payload = {
    idea: document.getElementById("idea").value,
    country: document.getElementById("country").value,
    investment: Number(document.getElementById("investment").value),
    target_customers: document.getElementById("customers").value,
    industry: document.getElementById("industry").value
  };

  try {
    const response = await fetch("/analyze", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    });

    if (!response.ok) throw new Error("Analysis failed");

    const data = await response.json();
    document.getElementById("recommendation").textContent = data.recommendation;

    const labels = {
      market_demand: "Demand",
      innovation: "Innovation",
      competition: "Competition",
      profit_potential: "Profit Potential",
      risk: "Risk"
    };

    document.getElementById("scores").innerHTML = Object.entries(data.scores)
      .map(([key, value]) => `<div class="score">${labels[key]}<b>${value}</b>/100</div>`)
      .join("");

    document.getElementById("strengths").innerHTML =
      data.strengths.map(item => `<li>${item}</li>`).join("");

    document.getElementById("improvements").innerHTML =
      data.improvements.map(item => `<li>${item}</li>`).join("");

    result.classList.remove("hidden");
    result.scrollIntoView({behavior: "smooth"});
  } catch (error) {
    alert("Could not analyze the idea. Make sure the FastAPI server is running.");
  }
});
