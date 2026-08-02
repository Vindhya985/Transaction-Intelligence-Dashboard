from fastapi import FastAPI, UploadFile, File
import pandas as pd

from Backend.database import (
    create_database,
    store_transactions,
    get_transactions
)
from ML.main import preprocessing

app = FastAPI()

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