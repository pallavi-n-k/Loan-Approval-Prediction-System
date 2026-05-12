import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Loan Analytics",
    page_icon="📊",
    layout="wide"
)

# ---------------- LOAD DATA ----------------

df = pd.read_csv("final_loan_data.csv")

# ---------------- SIDEBAR FILTERS ----------------

st.sidebar.markdown("## 🎛️ Filters")

area = st.sidebar.multiselect(
    "Property Area",
    [0, 1, 2],
    default=[0, 1, 2],
    format_func=lambda x: [
        "Rural",
        "Semi-Urban",
        "Urban"
    ][x]
)

credit = st.sidebar.multiselect(
    "Credit History",
    [0, 1],
    default=[0, 1]
)

income_range = st.sidebar.slider(
    "Applicant Income Range",
    int(df.ApplicantIncome.min()),
    int(df.ApplicantIncome.max()),
    (
        int(df.ApplicantIncome.min()),
        int(df.ApplicantIncome.max())
    )
)

# ---------------- FILTER DATA ----------------

df = df[
    (df.Property_Area.isin(area)) &
    (df.Credit_History.isin(credit)) &
    (
        df.ApplicantIncome.between(
            income_range[0],
            income_range[1]
        )
    )
]

# ---------------- COLORS ----------------

bg = "#081C35"
card = "#132A46"
green = "#12D6A0"
red = "#FF6B6B"
text = "#E8F1FF"

# ---------------- CSS ----------------

st.markdown(f"""
<style>

.stApp {{
    background: linear-gradient(
    to right,
    #081C35,
    #102B4E
    );
    color: white;
}}

[data-testid="stSidebar"] {{
    background-color: #0B1F3A;
}}

.metric-card {{
    background-color: {card};
    padding: 25px;
    border-radius: 22px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0px 0px 20px rgba(0,0,0,0.4);
}}

.metric-title {{
    color: #9FB3C8;
    font-size: 20px;
}}

.metric-value {{
    font-size: 50px;
    font-weight: bold;
}}

.small-text {{
    color: #8FA6C1;
}}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

left, right = st.columns([5,2])

with left:

    st.markdown("""
    # 📊 Loan Analytics

    ### Loan Portfolio Overview

    Real-time snapshot of application status and credit performance.
    """)

with right:

    st.markdown("""
    <div style="
    background:#103B4A;
    padding:12px 20px;
    border-radius:20px;
    text-align:center;
    margin-top:20px;
    color:white;
    ">
    🟢 Live • FY 2024
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- KPI DATA ----------------

total_apps = len(df)

approved = len(
    df[df["Loan_Status"] == 1]
)

rejected = len(
    df[df["Loan_Status"] == 0]
)

avg_income = int(
    df.ApplicantIncome.mean()
)

avg_loan = int(
    df.LoanAmount.mean()
)

credit_good = len(
    df[df.Credit_History == 1]
)

# ---------------- KPI ROW 1 ----------------

c1, c2, c3 = st.columns(3)

with c1:

    st.markdown(f"""
    <div class="metric-card">

    <div class="metric-title">
    📁 TOTAL APPLICATIONS
    </div>

    <div class="metric-value">
    {total_apps}
    </div>

    <div class="small-text">
    Total portfolio applications
    </div>

    </div>
    """, unsafe_allow_html=True)

with c2:

    st.markdown(f"""
    <div class="metric-card">

    <div class="metric-title">
    ✅ APPROVED LOANS
    </div>

    <div class="metric-value"
    style="color:{green}">
    {approved}
    </div>

    <div class="small-text">
    Successfully approved applications
    </div>

    </div>
    """, unsafe_allow_html=True)

with c3:

    st.markdown(f"""
    <div class="metric-card">

    <div class="metric-title">
    ❌ REJECTED LOANS
    </div>

    <div class="metric-value"
    style="color:{red}">
    {rejected}
    </div>

    <div class="small-text">
    Rejected loan applications
    </div>

    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- KPI ROW 2 ----------------

c4, c5, c6 = st.columns(3)

with c4:

    st.markdown(f"""
    <div class="metric-card">

    <div class="metric-title">
    💰 AVG INCOME
    </div>

    <div class="metric-value"
    style="color:#4da6ff">
    {avg_income}
    </div>

    <div class="small-text">
    Average applicant income
    </div>

    </div>
    """, unsafe_allow_html=True)

with c5:

    st.markdown(f"""
    <div class="metric-card">

    <div class="metric-title">
    🏦 AVG LOAN
    </div>

    <div class="metric-value"
    style="color:#a78bfa">
    {avg_loan}
    </div>

    <div class="small-text">
    Average loan amount
    </div>

    </div>
    """, unsafe_allow_html=True)

with c6:

    st.markdown(f"""
    <div class="metric-card">

    <div class="metric-title">
    ⭐ GOOD CREDIT
    </div>

    <div class="metric-value"
    style="color:{green}">
    {credit_good}
    </div>

    <div class="small-text">
    Applicants with credit history
    </div>

    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- CHARTS ROW 1 ----------------

left_chart, right_chart = st.columns(2)

# DONUT CHART

with left_chart:

    loan_counts = df["Loan_Status"].value_counts()

    fig = go.Figure(data=[go.Pie(
        labels=["Approved", "Rejected"],
        values=[
            loan_counts[1],
            loan_counts[0]
        ],
        hole=0.65,
        marker_colors=[green, red]
    )])

    fig.update_layout(
        title="APPROVAL DISTRIBUTION",
        paper_bgcolor=card,
        plot_bgcolor=card,
        font_color=text,
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# CREDIT HISTORY CHART

with right_chart:

    fig2 = go.Figure()

    for status, color, label in [
        (0, red, "Rejected"),
        (1, green, "Approved")
    ]:
        subset = df[df.Loan_Status == status]
        fig2.add_trace(go.Histogram(
            x=subset['Credit_History'],
            name=label,
            marker_color=color
        ))

    fig2.update_layout(
        title='CREDIT HISTORY VS LOAN STATUS',
        barmode='stack',
        paper_bgcolor=card,
        plot_bgcolor=card,
        font_color=text,
        height=500
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- GAUGE CHART ----------------

st.markdown("## 🎯 Approval Rate")

approval_rate = round(
    approved / total_apps * 100,
    1
)

fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=approval_rate,

    title={
        "text": "Approval Rate"
    },

    gauge={
        "axis": {
            "range": [0, 100]
        },

        "bar": {
            "color": green
        }
    }
))

fig_gauge.update_layout(
    paper_bgcolor=card,
    font_color=text,
    height=350
)

st.plotly_chart(
    fig_gauge,
    use_container_width=True
)

# ---------------- FOOTER ----------------

st.markdown("""
<hr style="border:1px solid #29476B">

<center>

Built with ❤️ using Streamlit, Machine Learning, FastAPI & Plotly

</center>
""", unsafe_allow_html=True)
