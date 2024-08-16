def clean_data(df):
    # Clean data
    df["MDC"] = df["Max Damage Cap (in M)"]
    df.dropna(subset=["MDC"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    df["MDC"] = df["MDC"].astype(float)
    df["Bishop"] = df["Class"] == "Bishop"

    return df
