import pandas as pd
import dagster as dg


@dg.asset
def processed_data():
    # https://docs.dagster.io/getting-started/quickstart#step-3-define-the-assets

    # Read data from the CSV
    df = pd.read_csv("data/samples/people.csv")

    # Add an age_group column based on the value of age
    df["age_group"] = pd.cut(
        df["age"], bins=[0, 30, 40, 100], labels=["Young", "Middle", "Senior"]
    )

    # Save processed data
    df.to_csv("data/processed_data.csv", index=False)
    return "Data loaded successfully"
