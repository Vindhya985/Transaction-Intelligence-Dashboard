import pandas as pd
from analytics import get_transaction_summary
from main import preprocessing


def test_data():
    raw = pd.read_csv('ML/sample-100-rows.csv')
    df = preprocessing(raw)
    res = get_transaction_summary(df)

    # Validate totals against raw frame sum
    assert round(res['total_spending'], 2) == round(
        df['Debit'].sum(), 2
    ), "Total spending mismatch"
    assert round(res['total_income'], 2) == round(
        df['Credit'].sum(), 2
    ), "Total income mismatch"

    # Validate row count and min/max bounds
    assert res['num_transactions'] == len(df), "Row count mismatch"
    assert res['highest_transaction'] == round(
        df['Debit'].max(), 2
    ), "Max debit mismatch"
    assert res['lowest_transaction'] == round(
        df['Debit'].min(), 2
    ), "Min debit mismatch"

    # Verify daily aggregate totals sum back up to total spending
    daily_total = sum(res['daily spending'].values())
    assert (
        abs(daily_total - res['total_spending']) < 0.01
    ), "Daily sum mismatch"

    print("Data validation successful. All analytics match dataset.")


if __name__ == "__main__":
    test_data()