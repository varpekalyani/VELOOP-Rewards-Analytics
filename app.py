import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="VELOOP | Rewards Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# PROFESSIONAL DARK THEME
# --------------------------------------------------

st.markdown("""
<style>
    .stApp {
        background-color: #0b1120;
        color: #f1f5f9;
    }

    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #263449;
    }

    h1, h2, h3 {
        color: #f8fafc;
    }

    [data-testid="stMetric"] {
        background-color: #172235;
        border: 1px solid #293950;
        padding: 18px;
        border-radius: 12px;
    }

    [data-testid="stMetricLabel"] {
        color: #a5b4fc;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff;
    }

    .subtitle {
        color: #94a3b8;
        font-size: 15px;
    }

    .section-title {
        color: #93c5fd;
        font-size: 22px;
        font-weight: 600;
        margin-top: 20px;
    }

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD ACTUAL DATA
# --------------------------------------------------

DATA_FILE = Path(__file__).parent / "data" / "users.csv"

st.sidebar.title("📊 VELOOP Analytics")
st.sidebar.caption("Rewards & User Intelligence")
st.sidebar.divider()

if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
    st.title("📊 VELOOP Rewards Analytics")
    st.error(
        "users.csv is empty or missing. "
        "Place your actual user dataset inside the data folder."
    )
    st.stop()

try:
    df = pd.read_csv(DATA_FILE)
except Exception as error:
    st.error(f"Could not read users.csv: {error}")
    st.stop()

if df.empty:
    st.error("The CSV contains no data rows.")
    st.stop()

# Clean column names without changing the original file.
df.columns = (
    df.columns.astype(str)
    .str.strip()
    .str.lower()
    .str.replace(r"[^a-z0-9]+", "_", regex=True)
    .str.strip("_")
)

# Identify common column-name variations.
def find_column(possible_names):
    for name in possible_names:
        if name in df.columns:
            return name
    return None

user_col = find_column(["user_id", "userid", "user"])
date_col = find_column([
    "registration_date", "registered_at", "signup_date",
    "registration_datetime", "created_at"
])
status_col = find_column([
    "account_status", "status", "user_status"
])
onboarding_col = find_column([
    "onboarding_status", "onboarding"
])
email_status_col = find_column([
    "email_verification_status", "email_status",
    "verification_status"
])
country_col = find_column(["country", "country_name"])
state_col = find_column(["state", "state_name"])
city_col = find_column(["city", "city_name"])
platform_col = find_column(["platform", "device_platform"])
gender_col = find_column(["gender"])

# Parse registration dates safely.
if date_col:
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Executive Overview",
        "User Analytics",
        "Data Explorer",
        "Data Quality",
        "Rewards & Wallet Readiness"
    ]
)

st.sidebar.divider()
st.sidebar.caption(f"Dataset rows: {len(df):,}")
st.sidebar.caption("Source: supplied user dataset")

# --------------------------------------------------
# SHARED FILTERS
# --------------------------------------------------

st.sidebar.subheader("🔎 Filters")

filtered = df.copy()

location_col = country_col or state_col

if location_col:
    options = sorted(
        filtered[location_col].dropna().astype(str).unique().tolist()
    )
    selected_locations = st.sidebar.multiselect(
        "Location", options
    )

    if selected_locations:
        filtered = filtered[
            filtered[location_col].astype(str).isin(selected_locations)
        ]

if platform_col:
    options = sorted(
        filtered[platform_col].dropna().astype(str).unique().tolist()
    )
    selected_platforms = st.sidebar.multiselect(
        "Platform", options
    )

    if selected_platforms:
        filtered = filtered[
            filtered[platform_col].astype(str).isin(selected_platforms)
        ]

if date_col:
    valid_dates = filtered[date_col].dropna()

    if not valid_dates.empty:
        min_date = valid_dates.min().date()
        max_date = valid_dates.max().date()

        selected_dates = st.sidebar.date_input(
            "Registration date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

        if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
            start_date, end_date = selected_dates
            filtered = filtered[
                filtered[date_col].dt.date.between(start_date, end_date)
            ]

# --------------------------------------------------
# REUSABLE CHART STYLE
# --------------------------------------------------

def style_chart(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font_color="#e5e7eb",
        margin=dict(l=20, r=20, t=60, b=20),
        legend_title_text=""
    )
    return fig

def count_unique_users(data):
    if user_col:
        return int(data[user_col].nunique())
    return len(data)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("📊 VELOOP Rewards Analytics")
st.markdown(
    '<p class="subtitle">User intelligence • Engagement readiness • Data quality</p>',
    unsafe_allow_html=True
)

st.caption(
    "Interactive analytics based on the supplied user dataset. "
    "Unavailable transaction datasets are not simulated."
)

# --------------------------------------------------
# PAGE 1: EXECUTIVE OVERVIEW
# --------------------------------------------------

if page == "Executive Overview":

    st.markdown('<div class="section-title">Executive Overview</div>',
                unsafe_allow_html=True)

    total_users = count_unique_users(filtered)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("👥 Registered Users", f"{total_users:,}")

    if status_col:
        active_count = (
            filtered[status_col].astype(str).str.strip().str.lower()
            .eq("active").sum()
        )
        col2.metric("🟢 Active Accounts", f"{active_count:,}")
    else:
        col2.metric("🟢 Active Accounts", "Unavailable")

    if onboarding_col:
        onboarding = (
            filtered[onboarding_col].astype(str).str.strip().str.lower()
        )
        completed = onboarding.isin(["completed", "complete"]).sum()
        col3.metric("✅ Onboarding Completed", f"{completed:,}")
    else:
        col3.metric("✅ Onboarding", "Unavailable")

    if email_status_col:
        verified = (
            filtered[email_status_col].astype(str).str.strip().str.lower()
            .isin(["verified", "complete", "completed", "yes", "true"])
            .sum()
        )
        col4.metric("✉️ Email Verified", f"{verified:,}")
    else:
        col4.metric("✉️ Email Verification", "Unavailable")

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Account Status Distribution")

        if status_col:
            status_data = (
                filtered[status_col]
                .fillna("Missing")
                .astype(str)
                .value_counts()
                .rename_axis("Account Status")
                .reset_index(name="Users")
            )

            fig = px.pie(
                status_data,
                names="Account Status",
                values="Users",
                hole=0.55
            )
            st.plotly_chart(style_chart(fig), use_container_width=True)
        else:
            st.info("Account status field is not available.")

    with right:
        st.subheader("Registration Trend")

        if date_col:
            dates = filtered[date_col].dropna()

            if not dates.empty:
                trend = (
                    dates.dt.date.value_counts()
                    .sort_index()
                    .rename_axis("Date")
                    .reset_index(name="Registrations")
                )

                fig = px.line(
                    trend,
                    x="Date",
                    y="Registrations",
                    markers=True
                )
                st.plotly_chart(style_chart(fig), use_container_width=True)
            else:
                st.info("No valid registration dates are available.")
        else:
            st.info("Registration date field is not available.")

    left, right = st.columns(2)

    with left:
        st.subheader("Users by Location")

        if location_col:
            location_data = (
                filtered[location_col]
                .fillna("Missing")
                .astype(str)
                .value_counts()
                .head(10)
                .rename_axis("Location")
                .reset_index(name="Users")
            )

            fig = px.bar(
                location_data,
                x="Location",
                y="Users",
                text="Users"
            )
            st.plotly_chart(style_chart(fig), use_container_width=True)
        else:
            st.info("Location field is not available.")

    with right:
        st.subheader("Users by Platform")

        if platform_col:
            platform_data = (
                filtered[platform_col]
                .fillna("Missing")
                .astype(str)
                .value_counts()
                .rename_axis("Platform")
                .reset_index(name="Users")
            )

            fig = px.bar(
                platform_data,
                x="Platform",
                y="Users"
            )
            st.plotly_chart(style_chart(fig), use_container_width=True)
        else:
            st.info("Platform field is not available in the dataset.")

# --------------------------------------------------
# PAGE 2: USER ANALYTICS
# --------------------------------------------------

elif page == "User Analytics":

    st.header("👥 User Analytics")

    st.write(
        "Explore registration, demographic, onboarding "
        "and account-status information."
    )

    left, right = st.columns(2)

    with left:
        if gender_col:
            gender_data = (
                filtered[gender_col]
                .fillna("Missing")
                .astype(str)
                .value_counts()
                .rename_axis("Gender")
                .reset_index(name="Users")
            )

            fig = px.bar(
                gender_data,
                x="Gender",
                y="Users",
                title="User Distribution"
            )
            st.plotly_chart(style_chart(fig), use_container_width=True)

        if state_col:
            state_data = (
                filtered[state_col]
                .fillna("Missing")
                .astype(str)
                .value_counts()
                .head(10)
                .rename_axis("State")
                .reset_index(name="Users")
            )

            fig = px.bar(
                state_data,
                x="State",
                y="Users",
                title="Top States"
            )
            st.plotly_chart(style_chart(fig), use_container_width=True)

    with right:
        if onboarding_col:
            onboarding_data = (
                filtered[onboarding_col]
                .fillna("Missing")
                .astype(str)
                .value_counts()
                .rename_axis("Onboarding Status")
                .reset_index(name="Users")
            )

            fig = px.pie(
                onboarding_data,
                names="Onboarding Status",
                values="Users",
                hole=0.45,
                title="Onboarding Status"
            )
            st.plotly_chart(style_chart(fig), use_container_width=True)

        if city_col:
            city_data = (
                filtered[city_col]
                .fillna("Missing")
                .astype(str)
                .value_counts()
                .head(10)
                .rename_axis("City")
                .reset_index(name="Users")
            )

            fig = px.bar(
                city_data,
                x="Users",
                y="City",
                orientation="h",
                title="Top Cities"
            )
            st.plotly_chart(style_chart(fig), use_container_width=True)

    st.subheader("User Records")
    st.dataframe(filtered, use_container_width=True, hide_index=True)

# --------------------------------------------------
# PAGE 3: DATA EXPLORER
# --------------------------------------------------

elif page == "Data Explorer":

    st.header("🔍 Data Explorer")

    st.write("Inspect the actual records loaded from the supplied CSV.")

    search = st.text_input("Search records")

    display_df = filtered.copy()

    if search:
        matches = display_df.astype(str).apply(
            lambda col: col.str.contains(search, case=False, na=False)
        ).any(axis=1)
        display_df = display_df[matches]

    st.metric("Matching Records", f"{len(display_df):,}")

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download Filtered CSV",
        data=display_df.to_csv(index=False).encode("utf-8"),
        file_name="veloop_filtered_users.csv",
        mime="text/csv"
    )

# --------------------------------------------------
# PAGE 4: DATA QUALITY
# --------------------------------------------------

elif page == "Data Quality":

    st.header("🛡️ Data Quality Overview")

    missing = filtered.isna().sum()

    quality_df = pd.DataFrame({
        "Column": filtered.columns,
        "Missing Values": missing.values,
        "Missing Percentage": (
            missing.values / max(len(filtered), 1) * 100
        ).round(2)
    }).sort_values("Missing Percentage", ascending=False)

    col1, col2, col3 = st.columns(3)

    col1.metric("Rows", f"{len(filtered):,}")
    col2.metric("Columns", f"{len(filtered.columns):,}")
    col3.metric(
        "Duplicate Rows",
        f"{int(filtered.duplicated().sum()):,}"
    )

    st.subheader("Missing Values by Column")

    fig = px.bar(
        quality_df.head(15),
        x="Column",
        y="Missing Percentage",
        title="Top 15 Columns by Missing Data"
    )
    fig.update_xaxes(tickangle=-40)

    st.plotly_chart(style_chart(fig), use_container_width=True)

    st.dataframe(quality_df, use_container_width=True, hide_index=True)

    if user_col:
        st.write(
            f"Unique user IDs in filtered data: "
            f"{filtered[user_col].nunique():,}"
        )

# --------------------------------------------------
# PAGE 5: REWARDS AND WALLET READINESS
# --------------------------------------------------

elif page == "Rewards & Wallet Readiness":

    st.header("🎁 Rewards, Wallet & Withdrawals")

    st.warning(
        "The supplied user dataset does not by itself establish "
        "reward, wallet, withdrawal or referral transaction performance."
    )

    st.subheader("Dataset Readiness")

    readiness = pd.DataFrame({
        "Analytics Area": [
            "User Analytics",
            "Task Engagement",
            "Rewards",
            "Wallet Transactions",
            "Withdrawals",
            "Referrals"
        ],
        "Current Status": [
            "User dataset loaded",
            "Requires task/event data",
            "Requires reward transaction data",
            "Requires wallet ledger data",
            "Requires withdrawal request data",
            "Requires referral data"
        ]
    })

    st.dataframe(readiness, use_container_width=True, hide_index=True)

    st.info(
        "Connect the corresponding verified source datasets before "
        "showing transaction KPIs or trends."
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "VELOOP Rewards Analytics | Data-driven reporting | "
    "Transaction metrics require verified source data."
)