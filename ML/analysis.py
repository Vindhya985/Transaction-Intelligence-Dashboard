
import pandas as pd
def get_transaction_summary(df):
    df['Data'] = pd.to_datetime(df['Date'])

    # total spending (debit) and total income (credit)
    total_spending = df['Debit'].sum()
    total_income = df['Credit'].sum()

    # no.of transactions
    num_transactions = len(df)

    # highest,lowest and average transaction amounts
    highest_transaction = df['Debit'].max()
    lowest_transaction = df['Debit'].min()
    average_transaction = df['Debit'].mean()

    # daily spending(total debit grouped by date)
    daily_spending = df.groupby(df['Data'].dt.date)['Debit'].sum().to_dict()

    # monthly spending(total debit grouped by year month)
    monthly_spending = df.groupby(df['Data'].dt.to_period('M'))['Debit'].sum().to_dict()

    # convert period  keys to string format
    monthly_spending = {str(k): v for k, v in monthly_spending.items()}


    return {
        "total_spending":   round(total_spending, 2),
        "total_income": round(total_income, 2),
        "num_transactions": num_transactions,
        "highest_transaction": round(highest_transaction, 2),
        "lowest_transaction": round(lowest_transaction, 2),
        "average_transaction": round(average_transaction, 2),
        "daily spending": daily_spending,
        "monthly spending": monthly_spending,
    }
