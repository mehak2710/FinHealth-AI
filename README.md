# 💜 FinHealth AI — AI-Powered Financial Health Coach

A lightweight, fintech-styled Streamlit app that scores a user's financial
health and delivers personalized, AI-generated money advice — built to
demonstrate how a modern fintech product can combine simple financial logic
with an LLM-powered coaching layer.

**🔗 Live Demo:** [https://gsnxfhcj3nhtoxzcjs58yi.streamlit.app/]

---

## Overview

FinHealth AI takes four core numbers — monthly income, monthly expenses,
savings, and debt — and turns them into:
- A **0–100 Financial Health Score**, categorized as Poor / Fair / Good / Excellent
- Three key financial ratios (Savings Rate, Debt-to-Income, Emergency Fund Coverage)
- **Personalized coaching tips generated live by an LLM** (Groq's Llama 3.3),
  tailored to the user's exact numbers — with an offline rule-based fallback
  so the app never breaks if no API key is configured

The UI is designed to feel like a real consumer fintech product — a purple
gradient header, rounded cards, and a circular score gauge — rather than a
bare-bones data app.

---

## Features

- 📊 **Instant financial health scoring** (0–100) from a simple, transparent formula
- 🤖 **AI-generated coaching** — Groq/Llama 3.3 analyzes the user's real numbers and writes custom tips (not templated text)
- 🛟 **Graceful offline fallback** — works with zero setup even without an API key
- 💜 **Realistic fintech UI** — PhonePe-inspired purple theme, gradient header, score ring, metric cards
- ⚡ **Zero backend/database** — fully client-facing, stateless, deploy-anywhere
- 🔒 **Environment-based secrets** — API key never hardcoded, loaded via `.env`

---

## Tech Stack

| Layer | Technology |
|---|---|
| App framework | [Streamlit](https://streamlit.io/) |
| AI / LLM | [Groq API](https://console.groq.com/) — Llama 3.3 70B Versatile |
| Config | [python-dotenv](https://pypi.org/project/python-dotenv/) |
| Styling | Custom CSS (`style.css`) |
| Language | Python 3.9+ |

---

## How to Run

**1. Clone the repo**
```bash
git clone https://github.com/<your-username>/finhealth-ai.git
cd finhealth-ai
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your Groq API key** *(optional but recommended)*
```bash
cp .env.example .env
```
Open `.env` and paste your key from [console.groq.com/keys](https://console.groq.com/keys):
```
GROQ_API_KEY=your_groq_api_key_here
```

**4. Run the app**
```bash
streamlit run app.py
```
Opens automatically at `http://localhost:8501`.

> No API key? The app still runs — it just uses built-in offline tips
> instead of live AI-generated advice.

### Deploy on Streamlit Community Cloud
1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app → point to `app.py`
3. Add `GROQ_API_KEY` under **App settings → Secrets**

---

## How the Score Works

| Component | Weight | Formula |
|---|---|---|
| Savings Rate | up to 40 pts | (Income − Expenses) / Income |
| Debt-to-Income | up to 30 pts | Lower debt relative to income scores higher |
| Emergency Fund | up to 30 pts | Savings ÷ Monthly Expenses, capped at 6 months |

> This is a simplified, illustrative scoring model for demo purposes — not
> financial or credit advice.

---

## Future Enhancements

- 📈 Add interactive charts (income vs. expenses, expense breakdown, debt vs. savings) using Plotly
- 🎯 Goal-based planning (emergency fund, house, retirement) with progress tracking
- 🧮 "What-if" scenario simulator (increase income, cut expenses, pay off debt)
- 💬 Conversational AI chat for follow-up financial questions
- 📄 Downloadable PDF financial report
- 🕘 Save and compare past assessments (persistent storage)
- 🌗 Dark mode toggle
- 💱 Multi-currency support
- 🔐 User accounts for returning, personalized sessions

---

## Project Structure
```
finhealth-ai/
├── app.py              # Streamlit UI, scoring logic, Groq AI integration
├── style.css            # PhonePe-inspired fintech theme
├── requirements.txt
├── .env.example
└── README.md
```

---

## License
This project is open for educational and portfolio use.
