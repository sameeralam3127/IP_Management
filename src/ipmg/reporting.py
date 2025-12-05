from colorama import Fore


def print_summary(df):
    summary = df["Status"].value_counts().to_dict()
    total = len(df)
    active = summary.get("Active", 0)

    print(f"\n{Fore.CYAN}=== IPMG Summary ===")
    for status, count in summary.items():
        print(f"{status}: {count}")

    print(f"\nSuccess Rate: {(active / total) * 100:.2f}%")
