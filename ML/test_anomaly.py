import pandas as pd
from anomaly import detect_anomalies, get_flagged_transactions
from main import preprocessing


def run_test():
    raw_data = pd.read_csv('ML/sample-100-rows.csv')
    df = preprocessing(raw_data)

    out = detect_anomalies(df)
    flagged_rows = get_flagged_transactions(df)

    # Basic checks
    assert 'Anomaly_Status' in out.columns, 'Missing Anomaly_Status column'
    assert len(flagged_rows) > 0, 'No anomalies detected'

    print(f'Total rows checked: {len(out)}')
    print(f'Anomalies found: {len(flagged_rows)}')
    print('\nSample flagged rows:')
    print(
        flagged_rows[['Date', 'Description', 'Debit', 'Anomaly_Status']].head()
    )


if __name__ == '__main__':
    run_test()