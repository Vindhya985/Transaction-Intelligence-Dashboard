import pandas as pd
def prepare_daily_chart(df):

    daily = (
        df.groupby("Date")["Debit"]
        .sum()
        .reset_index()
    )

    return daily.to_dict(orient="records")
def prepare_monthly_chart(df):

    monthly_df = df.copy()

    monthly_df["Date"] = pd.to_datetime(monthly_df["Date"])


    monthly = (
        df.groupby(
            df["Date"].dt.to_period("M")
        )["Debit"]
        .sum()
        .reset_index()
    )

    monthly["Date"] = monthly["Date"].astype(str)

    return monthly.to_dict(
        orient="records"
    )
def prepare_category_chart(df):

    category = (
        df.groupby("Category")["Debit"]
        .sum()
        .reset_index()
    )

    return category.to_dict(
        orient="records"
    )
def prepare_chart_data(df):

    return {

        "daily_spending":
        prepare_daily_chart(df),

        "monthly_spending":
        prepare_monthly_chart(df),

        "category_spending":
        prepare_category_chart(df)

    }