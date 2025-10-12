"""
AutoPing — Comprehensive & Automated Network Ping Tool
Author: Sameer Alam
"""

import pandas as pd
import platform
import subprocess
import socket
import ipaddress
import concurrent.futures
import logging
import argparse
from datetime import datetime
from tqdm import tqdm
from colorama import Fore, init
import re
import warnings
import os
from typing import Dict, List, Tuple, Union

# Initialize colorama and logging
init(autoreset=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="auto_ping.log"
)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AutoPing: Automated IP Pinger with Enhanced Reporting")
    parser.add_argument("--input", default="ip_list.xlsx", help="Input Excel file path")
    parser.add_argument("--output", default="ping_results", help="Output base filename")
    parser.add_argument("--timeout", type=int, default=2, help="Ping timeout (s)")
    parser.add_argument("--count", type=int, default=1, help="Ping count per IP")
    parser.add_argument("--retries", type=int, default=1, help="Ping retries")
    parser.add_argument("--threads", type=int, default=50, help="Concurrent threads")
    parser.add_argument("--formats", nargs="+", default=["xlsx"], choices=["xlsx", "csv", "json"], help="Output formats")
    parser.add_argument("--discover", action="store_true", help="Auto-discover local subnet IPs")
    parser.add_argument("--interval", type=int, help="Repeat ping every N minutes")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    return parser.parse_args()

def validate_ip(ip: str) -> bool:
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def get_local_subnet_ips() -> List[str]:
    """Auto-discover local subnet IPs based on current network interface."""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    network = ipaddress.ip_network(local_ip + "/24", strict=False)
    return [str(ip) for ip in network.hosts()]

def create_sample_excel(filename: str) -> None:
    """Create a sample Excel file if none exists."""
    sample = pd.DataFrame({"IP Address": ["8.8.8.8", "1.1.1.1"]})
    sample.to_excel(filename, index=False)
    logging.info(f"Created sample input file: {filename}")

def parse_latency(ping_output: str) -> Union[float, None]:
    if platform.system().lower() == "windows":
        match = re.search(r"Average = (\d+)ms", ping_output)
    else:
        match = re.search(r"min/avg/max/[^=]+=\s*[\d.]+/([\d.]+)/", ping_output)
    return float(match.group(1)) if match else None

def ping_ip(ip: str, timeout: int, count: int) -> Tuple[str, Union[float, None]]:
    param = "-n" if platform.system().lower() == "windows" else "-c"
    timeout_param = "-w" if platform.system().lower() == "windows" else "-W"
    timeout_val = str(timeout * 1000) if platform.system().lower() == "windows" else str(timeout)
    
    command = ["ping", param, str(count), timeout_param, timeout_val, ip]
    
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout + 1)
        latency = parse_latency(result.stdout)
        if result.returncode == 0:
            return "Active", latency
        elif "unreachable" in result.stdout.lower():
            return "Unreachable", None
        elif "timed out" in result.stdout.lower():
            return "Timeout", None
        else:
            return "Inactive", None
    except subprocess.TimeoutExpired:
        return "Timeout", None
    except Exception as e:
        return f"Error: {str(e)}", None

def resolve_hostname(ip: str) -> str:
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return "Unresolvable"

def ping_ips_parallel(ip_list: List[str], timeout: int, count: int, retries: int, max_workers: int) -> Dict[str, Tuple[str, Union[float, None]]]:
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(ping_ip, ip, timeout, count): ip for ip in ip_list}
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(ip_list), desc="Pinging IPs", unit="IP"):
            ip = futures[future]
            try:
                results[ip] = future.result()
            except Exception as e:
                results[ip] = (f"Error: {e}", None)
    return results

def save_results(df: pd.DataFrame, filename: str, formats: List[str]) -> None:
    for fmt in formats:
        try:
            if fmt == "xlsx":
                df.to_excel(f"{filename}.xlsx", index=False)
            elif fmt == "csv":
                df.to_csv(f"{filename}.csv", index=False)
            elif fmt == "json":
                df.to_json(f"{filename}.json", orient="records")
            logging.info(f"Saved {fmt.upper()} results to {filename}.{fmt}")
        except Exception as e:
            logging.error(f"Error saving {fmt}: {e}")

def generate_report(df: pd.DataFrame) -> None:
    summary = df["Status"].value_counts().to_dict()
    active = summary.get("Active", 0)
    total = len(df)
    print(f"\n{Fore.CYAN}=== Network Ping Summary ===")
    for status, count in summary.items():
        color = {
            "Active": Fore.GREEN,
            "Timeout": Fore.RED,
            "Unreachable": Fore.YELLOW,
            "Inactive": Fore.MAGENTA
        }.get(status, Fore.WHITE)
        print(f"{color}{status}: {Fore.WHITE}{count}")
    print(f"{Fore.CYAN}Total: {Fore.WHITE}{total} | {Fore.GREEN}Success Rate: {(active/total)*100:.2f}%")

def main():
    args = parse_args()
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if not os.path.exists(args.input):
        create_sample_excel(args.input)
    
    while True:
        if args.discover:
            ip_list = get_local_subnet_ips()
            logging.info(f"Discovered {len(ip_list)} IPs in local subnet")
        else:
            df = pd.read_excel(args.input)
            ip_list = [ip for ip in df["IP Address"].astype(str) if validate_ip(ip)]
        
        results = ping_ips_parallel(ip_list, args.timeout, args.count, args.retries, args.threads)
        hostnames = {ip: resolve_hostname(ip) for ip in ip_list}
        
        output_df = pd.DataFrame([
            {"IP Address": ip, "Status": res[0], "Latency": res[1], "Hostname": hostnames[ip], "Timestamp": datetime.now()}
            for ip, res in results.items()
        ])
        
        save_results(output_df, f"{args.output}_{datetime.now():%Y%m%d_%H%M%S}", args.formats)
        generate_report(output_df)

        if not args.interval:
            break
        logging.info(f"Sleeping for {args.interval} minutes before next run...")
        time.sleep(args.interval * 60)

if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=UserWarning)
    main()
