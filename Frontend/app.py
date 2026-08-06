import streamlit as st
import requests
import pandas as pd
import plotly.express as px

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

            summary_response = requests.get(
                "http://127.0.0.1:8000/summary"
            )

            analytics_response = requests.get(
                "http://127.0.0.1:8000/analytics"
            )
            anomaly_response = requests.get(
                "http://127.0.0.1:8000/anomalies"
            )

            anomaly_df = pd.DataFrame(
                anomaly_response.json()
            )

            if summary_response.status_code != 200:
                st.error("Failed to load summary.")
                st.stop()

            if analytics_response.status_code != 200:
                st.error("Failed to load analytics.")
                st.stop()

            summary = summary_response.json()
            analytics = analytics_response.json()
            transactions = requests.get(
                "http://127.0.0.1:8000/transactions"
            )
        st.divider()
        
        st.subheader("📈 Dashboard Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
                st.metric(
                    "💰 Total Spending",
                    f"₹{summary['total_spending']:,.2f}"
                )
        
        with col2:
                st.metric(
                    "💵 Total Income",
                    f"₹{summary['total_income']:,.2f}"
                )
        
        with col3:
                st.metric(
                    "📄 Transactions",
                    summary["num_transactions"]
                )
        
        with col4:
                st.metric(
                    "💳 Highest Transaction",
                    f"₹{summary['highest_transaction']:,.2f}"
                )
            # Summary cards will go here
        st.divider()
        
        st.subheader("📊 Analytics")

        daily_df = pd.DataFrame(
            analytics["daily_spending"]
        )

        st.write("### 📅 Daily Spending")

        fig = px.line(
            daily_df,
            x="Date",
            y="Debit",
            title="Daily Spending"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        monthly_df = pd.DataFrame(
            analytics["monthly_spending"]
        )

        st.write("### 📆 Monthly Spending")

        fig = px.bar(
            monthly_df,
            x="Date",
            y="Debit",
            title="Monthly Spending"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        category_df = pd.DataFrame(
            analytics["category_spending"]
        )

        st.write("### 🛒 Category Spending")

        fig = px.bar(
            category_df,
            x="Category",
            y="Debit",
            title="Category Spending"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
        st.divider()

        st.subheader("🤖 Financial Insights")

        col1, col2 = st.columns(2)

        with col1:
            st.success(
                f"""
        **Highest Transaction**

        ₹{summary['highest_transaction']:,.2f}

        **Lowest Transaction**

        ₹{summary['lowest_transaction']:,.2f}
        """
            )

        with col2:
            st.info(
                f"""
        **Average Transaction**

        ₹{summary['average_transaction']:,.2f}

        **Total Transactions**

        {summary['num_transactions']}
        """
            )
        st.write("### 📌 Quick Summary")

        st.write(
            f"""
        - 💰 Total Spending: **₹{summary['total_spending']:,.2f}**
        - 💵 Total Income: **₹{summary['total_income']:,.2f}**
        - 📈 Average Transaction: **₹{summary['average_transaction']:,.2f}**
        - 📄 Total Transactions: **{summary['num_transactions']}**
        """
        )    
        st.divider()

        st.subheader("🚨 Anomaly Detection")

        if not anomaly_df.empty:

            st.warning(
                f"⚠️ {len(anomaly_df)} suspicious transaction(s) detected."
            )

        else:

            st.success(
                "✅ No suspicious transactions detected."
            )

        # ⬇️ Replace your old table code with this
        st.subheader("🚨 Suspicious Transactions")

        display_df = anomaly_df[
            [
                "Date",
                "Description",
                "Debit",
                "Credit",
                "Balance",
                "Category",
                "Anomaly_Status"
            ]
        ].rename(
            columns={
                "Anomaly_Status": "Status"
            }
        )

        st.dataframe(
            display_df,
            use_container_width=True
        )
        if transactions.status_code == 200:
            df = pd.DataFrame(transactions.json())
            
            st.divider()
            st.subheader("🔍 Filters")
                        
            selected_category = st.selectbox(
                                    "Category",
                                    ["All"] + sorted(df["category"].unique())
                                )
            filtered_df = df.copy()
                        
            if selected_category != "All":
                                filtered_df = filtered_df[
                                filtered_df["category"] == selected_category
                                ]
            st.write(f"Showing **{len(filtered_df)}** transaction(s)")

            st.subheader("📄 Recent Transactions")

            st.dataframe(
                filtered_df,
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

        

        st.success("✅ CSV uploaded successfully!")
    else:
        st.error("❌ Backend failed to process the CSV.")