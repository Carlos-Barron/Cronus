import time
import numpy as np
import pandas as pd

df = pd.DataFrame({
    "email": ["test@test.com", "charly@wizeline.com"] * 100_000,
    "name": ["Test", "Charly"] * 100_000
})

def cronometer(label, function):
    begin = time.perf_counter()
    function()
    print(f"{label}: {time.perf_counter() - begin:.3f}s")

def with_iterrows():
    result = [row["email"].split("@")[1] for _, row in df.iterrows()]
    return result

def with_apply():
    return df["email"].apply(lambda e: e.split("@")[1])

def vectored():
    return df["email"].str.split("@").str[1]


cronometer("iterrows", with_iterrows)
cronometer("Apply", with_apply)
cronometer("Vectored", vectored)