import pandas as pd
import platform
import subprocess
import socket
import ipaddress
import concurrent.futures
from tqdm import tqdm
import logging
import argparse
from colorama import Fore, init
import re
import warnings
from typing import Dict, List, Tuple, Union

# Initialize colorama and logging
init(autoreset=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="ip_pinger.log"
)

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Advanced IP Pinger with Parallel Processing")
    parser.add_argument("--input", default="ip_list.xlsx", help="Input Excel file path")
    parser.add_argument("--output", default="ping_results", help="Output file base name")
    parser.add_argument("--timeout", type=int, default=2, help="Ping timeout in seconds")
    parser.add_argument("--count", type=int, default=1, help="Number of ping packets")
    parser.add_argument("--retries", type=int, default=1, help="Number of ping retries")
    parser.add_argument("--threads", type=int, default=50, help="Max concurrent threads")
    parser.add_argument("--formats", nargs="+", default=["xlsx"], 
                      choices=["xlsx", "csv", "json"], help="Output formats")
    return parser.parse_args()

def validate_ip(ip: str) -> bool:
    """Validate an IP address format."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def parse_latency(ping_output: str) -> Union[float, None]:
    """Extract latency from ping output."""
    try:
        if platform.system().lower() == "windows":
            match = re.search(r"Average = (\d+)ms", ping_output)
            return float(match.group(1)) if match else None
        else:
            match = re.search(r"min/avg/max/[^=]+=\s*[\d.]+/([\d.]+)/", ping_output)
            return float(match.group(1)) if match else None
    except Exception:
        return None

def ping_ip(ip: str, timeout: int = 2, count: int = 1) -> Tuple[str, Union[float, None]]:
    """Ping an IP address with configurable parameters."""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    timeout_param = "-w" if platform.system().lower() == "windows" else "-W"
    timeout_val = str(timeout * 1000) if platform.system().lower() == "windows" else str(timeout)
    
    command = ["ping", param, str(count), timeout_param, timeout_val, ip]
    
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout + 1
        )
        
        latency = parse_latency(result.stdout)
        
        if result.returncode == 0:
            return "Active", latency
        else:
            output = result.stdout.lower()
            if "destination host unreachable" in output:
                return "Unreachable", None
            elif "request timed out" in output:
                return "Timeout", None
            elif "could not find host" in output:
                return "Unknown Host", None
            else:
                return "Inactive", None
                
    except subprocess.TimeoutExpired:
        return "Timeout", None
    except FileNotFoundError:
        return "Ping Command Not Found", None
    except Exception as e:
        return f"Error: {str(e)}", None

def ping_with_retry(ip: str, timeout: int = 2, count: int = 1, retries: int = 1) -> Tuple[str, Union[float, None]]:
    """Ping with retry mechanism."""
    for attempt in range(retries):
        status, latency = ping_ip(ip, timeout, count)
        if status == "Active":
            return status, latency
    return status, latency

def resolve_hostname(ip: str) -> str:
    """Resolve hostname from IP address."""
    try:
        return socket.gethostbyaddr(ip)[0]
    except (socket.herror, socket.gaierror):
        return "Unresolvable"
    except Exception:
        return "Error resolving"

def ping_ips_parallel(ip_list: List[str], timeout: int, count: int, retries: int, max_workers: int) -> Dict[str, Tuple[str, Union[float, None]]]:
    """Ping multiple IPs in parallel with progress tracking."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(ping_with_retry, ip, timeout, count, retries): ip 
            for ip in ip_list
        }
        results = {}
        for future in tqdm(
            concurrent.futures.as_completed(futures),
            total=len(ip_list),
            desc="Pinging IPs",
            unit="IP"
        ):
            ip = futures[future]
            results[ip] = future.result()
    return results

def save_results(df: pd.DataFrame, filename: str, formats: List[str]) -> None:
    """Save results in multiple formats."""
    for fmt in formats:
        try:
            if fmt == "xlsx":
                df.to_excel(f"{filename}.xlsx", index=False, engine='openpyxl')
            elif fmt == "csv":
                df.to_csv(f"{filename}.csv", index=False)
            elif fmt == "json":
                df.to_json(f"{filename}.json", orient="records")
            logging.info(f"Saved results to {filename}.{fmt}")
        except Exception as e:
            logging.error(f"Failed to save {fmt} file: {e}")

def generate_report(df: pd.DataFrame) -> None:
    """Generate and display a colorful summary report."""
    report = {
        "Total IPs": len(df),
        "Active": len(df[df["Status"] == "Active"]),
        "Inactive": len(df[df["Status"] == "Inactive"]),
        "Unreachable": len(df[df["Status"] == "Unreachable"]),
        "Timeouts": len(df[df["Status"] == "Timeout"]),
        "Avg Latency (ms)": df[df["Status"] == "Active"]["Latency"].mean(),
        "Unresolvable Hosts": len(df[df["Hostname"] == "Unresolvable"])
    }
    
    print(f"\n{Fore.CYAN}=== Ping Results Summary ===")
    for key, value in report.items():
        color = Fore.GREEN if key in ["Active", "Avg Latency (ms)"] else Fore.YELLOW
        print(f"{color}{key}: {Fore.WHITE}{value}")
    
    if report["Total IPs"] > 0:
        success_rate = (report["Active"] / report["Total IPs"]) * 100
        print(f"{Fore.GREEN}Success Rate: {success_rate:.2f}%")

def main():
    args = parse_args()
    
    try:
        # Read and validate input
        logging.info(f"Reading input file: {args.input}")
        df = pd.read_excel(args.input, engine='openpyxl')
        
        if "IP Address" not in df.columns:
            raise ValueError("Input file must contain 'IP Address' column")
            
        # Clean and validate IPs
        ip_list = df["IP Address"].astype(str).tolist()
        valid_ips = [ip for ip in ip_list if validate_ip(ip)]
        
        if len(valid_ips) < len(ip_list):
            invalid_count = len(ip_list) - len(valid_ips)
            logging.warning(f"Skipped {invalid_count} invalid IP addresses")
            print(f"{Fore.YELLOW}Warning: Skipped {invalid_count} invalid IP addresses")

        # Process IPs
        logging.info(f"Pinging {len(valid_ips)} IPs (timeout: {args.timeout}s, count: {args.count}, retries: {args.retries})")
        results = ping_ips_parallel(valid_ips, args.timeout, args.count, args.retries, args.threads)
        
        # Resolve hostnames
        logging.info("Resolving hostnames...")
        hostnames = {}
        for ip in tqdm(valid_ips, desc="Resolving Hostnames", unit="IP"):
            hostnames[ip] = resolve_hostname(ip)
        
        # Update DataFrame
        df["Status"] = df["IP Address"].astype(str).map(lambda ip: results.get(ip, ("Skipped", None))[0])
        df["Latency"] = df["IP Address"].astype(str).map(lambda ip: results.get(ip, (None, None))[1])
        df["Hostname"] = df["IP Address"].astype(str).map(hostnames)
        
        # Save and report
        save_results(df, args.output, args.formats)
        generate_report(df)
        
    except FileNotFoundError:
        error_msg = f"Input file not found: {args.input}"
        logging.error(error_msg)
        print(f"{Fore.RED}Error: {error_msg}")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}", exc_info=True)
        print(f"{Fore.RED}Error: {str(e)}")

if __name__ == "__main__":
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')
    main()