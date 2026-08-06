from fastapi import FastAPI, UploadFile, File
import pandas as pd

from Backend.database import (
    create_database,
    store_transactions,
    get_transactions
)
from ML.main import preprocessing
from ML.analytics import (
    get_transaction_summary,
    prepare_chart_data
)
app = FastAPI()
@app.get("/summary")
async def summary():

    transactions = get_transactions()

    df = pd.DataFrame(transactions)
    df = df.rename(columns={
        "transaction_id": "Transaction_ID",
        "date": "Date",
        "description": "Description",
        "debit": "Debit",
        "credit": "Credit",
        "balance": "Balance",
        "category": "Category"
    })

    return get_transaction_summary(df)


@app.get("/analytics")
async def analytics():

    transactions = get_transactions()

    df = pd.DataFrame(transactions)

    df = df.rename(columns={
        "transaction_id": "Transaction_ID",
        "date": "Date",
        "description": "Description",
        "debit": "Debit",
        "credit": "Credit",
        "balance": "Balance",
        "category": "Category"
    })

    return prepare_chart_data(df)

# Create the database when FastAPI starts
create_database()


@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    try:
        # Read uploaded CSV
        df = pd.read_csv(file.file)

        # Preprocess the data
        processed_df = preprocessing(df)
       

        # Store the processed data into SQLite
        store_transactions(processed_df)

        return {
            "message": "Transactions uploaded and stored successfully.",
            "rows_inserted": len(processed_df)
        }

    except Exception as e:
        return {
            "error": str(e)
        }

@app.get("/transactions")
async def read_transactions():
    return get_transactions()