from fastapi import FastAPI, UploadFile, File
import pandas as pd

app = FastAPI()

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):

    df = pd.read_csv(file.file)

    df = df.fillna("")

    return {
        "success": True,
        "rows": len(df),
        "columns": list(df.columns),
        "preview": df.head().to_dict(orient="records")
    }