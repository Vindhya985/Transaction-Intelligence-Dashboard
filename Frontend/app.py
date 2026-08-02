import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="Transaction Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Transaction Intelligence Dashboard")

st.write(
    "Upload, analyze and visualize your bank transactions."
)
st.divider()
st.subheader("📁 Upload Bank Statement")

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"]
)
st.divider()

st.subheader("📈 Dashboard Summary")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Total Spending",
        "—"
    )

with col2:
    st.metric(
        "💵 Total Income",
        "—"
    )

with col3:
    st.metric(
        "📄 Transactions",
        "—"
    )

with col4:
    st.metric(
        "🏦 Current Balance",
        "—"
    )

# Summary cards will go here
st.divider()

st.subheader("📊 Analytics")
st.info(
    "Analytics charts will appear here after data processing."
)

st.divider()

st.subheader("🤖 AI Insights")
st.info(
    "AI-generated insights will appear here."
)

if uploaded_file is not None:

    # ---------------- File Size Validation ----------------
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

    if uploaded_file.size > MAX_FILE_SIZE:
        st.error("❌ File size exceeds 10 MB.")
        st.stop()

    # ---------------- Send File to FastAPI ----------------
    try:

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file,
                "text/csv"
            )
        }

        response = requests.post(
            "http://127.0.0.1:8000/upload",
            files=files
        )
        if response.status_code == 200:
            st.success("")
        transactions = requests.get(
            "http://127.0.0.1:8000/transactions"
        )
        if transactions.status_code == 200:
            df = pd.DataFrame(transactions.json())
            st.divider()

            st.subheader("📄 Recent Transactions")

            st.dataframe(
                df,
                use_container_width=True
            )

            

            

    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the backend. Is FastAPI running?")
        st.stop()

    except Exception as e:
        st.error(f"❌ {e}")
        st.stop()

    # ---------------- Handle Backend Response ----------------
    if response.status_code == 200:

        data = response.json()

        st.success("✅ CSV uploaded successfully!")
    else:
        st.error("❌ Backend failed to process the CSV.")