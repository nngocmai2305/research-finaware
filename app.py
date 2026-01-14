import streamlit as st

st.set_page_config(page_title="FinAware", page_icon="💡", layout="centered")

st.title("FinAware 💡")
st.caption(
    "A research-informed decision-awareness tool for students. "
    "This tool does not recommend actions — it helps you explore trade-offs."
)

# ----------------------------
# Session State Initialization
# ----------------------------
if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "goal_name" not in st.session_state:
    st.session_state.goal_name = ""

# ----------------------------
# Section 1: Basic Profile
# ----------------------------
st.header("1. Your Financial Snapshot")

income = st.number_input(
    "Monthly income / allowance (VND)",
    min_value=0,
    step=50000
)

goal_name = st.text_input(
    "Optional: A personal financial goal (e.g., save for a laptop)",
    value=st.session_state.goal_name
)
st.session_state.goal_name = goal_name

# ----------------------------
# Section 2: Expenses
# ----------------------------
st.header("2. Monthly Expenses")

col1, col2, col3 = st.columns(3)

with col1:
    exp_name = st.text_input("Expense name")

with col2:
    exp_amount = st.number_input(
        "Amount (VND)",
        min_value=0,
        step=10000
    )

with col3:
    exp_category = st.selectbox(
        "Category",
        ["Need", "Want"]
    )

if st.button("Add Expense"):
    if exp_name and exp_amount > 0:
        st.session_state.expenses.append(
            {
                "name": exp_name,
                "amount": exp_amount,
                "category": exp_category
            }
        )

if st.session_state.expenses:
    st.subheader("Current Expenses")
    total_expenses = 0
    total_needs = 0
    total_wants = 0

    for e in st.session_state.expenses:
        st.write(f"- {e['name']} ({e['category']}): {e['amount']:,} VND")
        total_expenses += e["amount"]
        if e["category"] == "Need":
            total_needs += e["amount"]
        else:
            total_wants += e["amount"]

    if st.button("Clear All Expenses"):
        st.session_state.expenses = []
        st.rerun()
else:
    total_expenses = total_needs = total_wants = 0

remaining = income - total_expenses

st.markdown("---")
st.write(f"**Total expenses:** {total_expenses:,} VND")
st.write(f"**Remaining balance:** {remaining:,} VND")

# ----------------------------
# Section 3: Awareness Benchmarks
# ----------------------------
st.header("3. Spending Awareness")

if income > 0:
    needs_ratio = (total_needs / income) * 100
    wants_ratio = (total_wants / income) * 100

    st.write(
        f"Needs: **{needs_ratio:.1f}%** of income  \n"
        f"Wants: **{wants_ratio:.1f}%** of income"
    )

    st.info(
        "In financial education, simple benchmarks (such as separating needs and wants) "
        "are often used to encourage reflection. Individual situations may vary."
    )

# ----------------------------
# Section 4: Decision Scenarios
# ----------------------------
st.header("4. Explore a Decision Scenario")

scenario = st.selectbox(
    "Choose a scenario",
    ["Buy Now vs Save", "Work vs Free Time"]
)

if scenario == "Buy Now vs Save":
    st.subheader("Scenario: Buy Now vs Save")

    item_price = st.number_input(
        "Item price (VND)",
        min_value=0,
        step=50000
    )

    monthly_saving = st.number_input(
        "How much could you save per month? (VND)",
        min_value=0,
        step=50000
    )

    if monthly_saving > 0 and item_price > 0:
        months_needed = item_price / monthly_saving

        st.write(
            f"At this saving rate, it would take approximately "
            f"**{months_needed:.1f} months** to reach this amount."
        )

        st.info(
            "This comparison highlights a time trade-off. "
            "Some people prefer immediate access; others prioritize reaching goals sooner."
        )

elif scenario == "Work vs Free Time":
    st.subheader("Scenario: Work vs Free Time")

    hourly_wage = st.number_input(
        "Hourly wage (VND)",
        min_value=0,
        step=10000
    )

    hours_per_week = st.number_input(
        "Extra work hours per week",
        min_value=0,
        step=1
    )

    monthly_income_gain = hourly_wage * hours_per_week * 4

    st.write(
        f"Estimated additional monthly income: "
        f"**{monthly_income_gain:,} VND**"
    )

    st.info(
        "This scenario illustrates opportunity cost — "
        "gaining income may reduce free time or study time."
    )

# ----------------------------
# Section 5: Reflection
# ----------------------------
st.header("5. Reflection")

st.text_area(
    "What did you notice about the trade-offs in your situation?",
    placeholder="For example: Which option aligns better with your priorities or goals?"
)

st.caption(
    "FinAware is an educational prototype. "
    "It supports reflection and awareness rather than financial advice."
)
