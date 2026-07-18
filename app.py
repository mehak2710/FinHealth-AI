import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

st.set_page_config(page_title="FinHealth AI", page_icon="💜", layout="centered")

# ---------- Load custom CSS ----------
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<div class="topbar">
    <div class="topbar-title">💜 FinHealth AI</div>
    <div class="topbar-sub">Your personal money coach</div>
</div>
""", unsafe_allow_html=True)

# ---------- Input Card ----------
with st.container(border=True):
    st.markdown('<div class="card-title">Tell us about your money</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        income = st.number_input("Monthly Income (₹)", min_value=0, value=50000, step=1000)
        expenses = st.number_input("Monthly Expenses (₹)", min_value=0, value=30000, step=1000)
    with col2:
        savings = st.number_input("Total Savings (₹)", min_value=0, value=100000, step=1000)
        debt = st.number_input("Total Debt/EMI-related (₹)", min_value=0, value=50000, step=1000)

    check = st.button("Check My Financial Health", use_container_width=True)


# ---------- Scoring Logic (simple rule-based "AI") ----------
def calculate_score(income, expenses, savings, debt):
    if income <= 0:
        return 0, 0, 0, 0
    savings_rate = (income - expenses) / income
    debt_ratio = debt / income
    emergency_months = savings / expenses if expenses > 0 else 0

    score = 0
    score += max(min(savings_rate * 100, 40), 0)          # up to 40 pts
    score += max(30 - debt_ratio * 30, 0)                  # up to 30 pts
    score += min((emergency_months / 6) * 30, 30)           # up to 30 pts
    return round(min(score, 100)), savings_rate, debt_ratio, emergency_months


def score_label(score):
    if score >= 80:
        return "Excellent", "#00b86b"
    elif score >= 60:
        return "Good", "#5f259f"
    elif score >= 40:
        return "Fair", "#ff9500"
    else:
        return "Needs Attention", "#e53935"


# ---------- AI Advisor (Groq) ----------
def get_ai_tips(income, expenses, savings, debt, score, label, savings_rate, debt_ratio, emergency_months):
    """
    Asks Groq's Llama model for personalized tips based on the user's numbers.
    Falls back to simple rule-based tips only if no GROQ_API_KEY is set
    (e.g. offline demo) or the API call fails.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return _fallback_tips(savings_rate, debt_ratio, emergency_months), False

    prompt = f"""You are a friendly financial coach. Based on this person's numbers, give 4 short,
specific, encouraging tips (1 sentence each, start each with a relevant emoji).

Monthly Income: ₹{income}
Monthly Expenses: ₹{expenses}
Total Savings: ₹{savings}
Total Debt: ₹{debt}
Savings Rate: {savings_rate*100:.0f}%
Debt-to-Income Ratio: {debt_ratio*100:.0f}%
Emergency Fund: {emergency_months:.1f} months of expenses
Financial Health Score: {score}/100 ({label})

Return ONLY the 4 tips, one per line, no numbering, no extra text."""

    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=250,
        )
        text = response.choices[0].message.content.strip()
        tips = [line.strip("-• ") for line in text.split("\n") if line.strip()]
        return tips, True
    except Exception:
        return _fallback_tips(savings_rate, debt_ratio, emergency_months), False


def _fallback_tips(savings_rate, debt_ratio, emergency_months):
    """Simple offline backup used only when no API key is configured or the call fails."""
    tips = []
    if savings_rate < 0.2:
        tips.append("💡 Try to save at least 20% of your income every month.")
    else:
        tips.append("✅ Great job! You're saving a healthy portion of your income.")

    if debt_ratio > 0.3:
        tips.append("⚠️ Your debt is high relative to income — prioritize paying it down.")
    else:
        tips.append("✅ Your debt levels look manageable.")

    if emergency_months < 3:
        tips.append("🛟 Build an emergency fund covering at least 3–6 months of expenses.")
    else:
        tips.append("✅ You have a solid emergency fund cushion.")

    tips.append("📈 Consider investing surplus savings in SIPs/mutual funds for long-term growth.")
    return tips


# ---------- Results ----------
if check:
    score, savings_rate, debt_ratio, emergency_months = calculate_score(income, expenses, savings, debt)
    label, color = score_label(score)

    st.markdown(f"""
        <div class="card score-card">
            <div class="score-circle" style="background: conic-gradient({color} {score * 3.6}deg, #eee 0deg);">
                <div class="score-inner">
                    <div class="score-number">{score}</div>
                    <div class="score-max">/100</div>
                </div>
            </div>
            <div class="score-label" style="color:{color};">{label}</div>
        </div>
    """, unsafe_allow_html=True)

    # Metric cards
    st.markdown(f"""
        <div class="metric-row">
            <div class="metric-box"><div class="metric-label">Savings Rate</div><div class="metric-value">{savings_rate*100:.0f}%</div></div>
            <div class="metric-box"><div class="metric-label">Debt / Income</div><div class="metric-value">{debt_ratio*100:.0f}%</div></div>
            <div class="metric-box"><div class="metric-label">Emergency Fund</div><div class="metric-value">{emergency_months:.1f} mo</div></div>
        </div>
    """, unsafe_allow_html=True)

    # Tips card
    with st.spinner("Getting personalized advice..."):
        tips, used_ai = get_ai_tips(income, expenses, savings, debt, score, label,
                                     savings_rate, debt_ratio, emergency_months)

    tips_html = "".join(f'<div class="tip-item">{tip}</div>' for tip in tips)
    st.markdown(f"""
        <div class="card">
            <div class="card-title">🤖 Your AI Coach Says</div>
            {tips_html}
        </div>
    """, unsafe_allow_html=True)

    if not used_ai:
        st.caption("⚙️ Showing offline tips — add GROQ_API_KEY in .env for live AI-generated advice.")

st.markdown('<div class="footer">Made with 💜 · FinHealth AI</div>', unsafe_allow_html=True)