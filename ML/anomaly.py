import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_anomalies(df, contamination=0.05):
    result = df.copy()

    # Get numeric feature columns (Debit, Credit, Balance, etc.)
    cols = [c for c in ['Debit', 'Credit', 'Balance'] if c in result.columns]
    if not cols:
        cols = result.select_dtypes(include=['number']).columns.tolist()

    features = result[cols].fillna(0)

    # Train isolation forest model
    model = IsolationForest(contamination=contamination, random_state=42)
    model.fit(features)

    # Predict anomalies (-1 = anomaly, 1 = normal)
    predictions = model.predict(features)

    # Save predictions and map to string labels
    result['prediction_raw'] = predictions
    result['Anomaly_Status'] = result['prediction_raw'].map(
        {1: 'normal', -1: 'Anomaly'}
    )

    return result


def get_flagged_transactions(df):
    data = detect_anomalies(df)
    return data[data['Anomaly_Status'] == 'Anomaly']