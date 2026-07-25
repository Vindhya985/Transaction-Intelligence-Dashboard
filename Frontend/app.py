import streamlit as st
import requests

st.set_page_config(
    page_title="Transaction Intelligence Dashboard",
    page_icon="📊",
    layout="centered"
)

st.title("📊 Transaction Intelligence Dashboard")

st.write(
    "Upload your bank statement in CSV format."
)

uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=["csv"]
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

        st.subheader("Preview")

        st.dataframe(
            data["preview"],
            use_container_width=True
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Transactions", data["rows"])

        with col2:
            st.metric("Columns", len(data["columns"]))

    else:
        st.error("❌ Backend failed to process the CSV.")