from datetime import datetime

import pandas as pd

from ipmg.ping import validate_ip


def load_ip_file(path: str) -> list[str]:
    df = pd.read_excel(path)
    return [ip for ip in df["IP Address"].astype(str) if validate_ip(ip)]


def create_sample_file(path: str):
    df = pd.DataFrame({"IP Address": ["8.8.8.8", "1.1.1.1"]})
    df.to_excel(path, index=False)


def save_results(df, base_name: str, formats: list[str]):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{base_name}_{timestamp}"

    for fmt in formats:
        if fmt == "xlsx":
            df.to_excel(f"{filename}.xlsx", index=False)
        elif fmt == "csv":
            df.to_csv(f"{filename}.csv", index=False)
        elif fmt == "json":
            df.to_json(f"{filename}.json", orient="records")
