# IP Pinger Tool - Advanced Network Monitoring

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Overview

The IP Pinger Tool is a robust Python application designed for network administrators and IT professionals to efficiently monitor network devices. It provides parallel ping operations, hostname resolution, and comprehensive reporting capabilities.

## ✨ Features

- **Parallel Processing**: Ping hundreds of IPs simultaneously
- **Detailed Reporting**: Get latency metrics and status reports
- **Multiple Output Formats**: Export results in Excel, CSV, or JSON
- **Smart Retry Mechanism**: Configurable retries for flaky connections
- **Hostname Resolution**: Automatically resolves hostnames
- **Colorful Console Output**: Easy-to-read status information
- **Comprehensive Logging**: Detailed operation logs for debugging

## Installation

1. Clone the repository:

```bash
git clone https://github.com/sameeralam3127/IP_Management.git
cd IP_Management
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Command

```bash
python ip_pinger.py
```

### Advanced Options

| Parameter   | Description                    | Default      |
| ----------- | ------------------------------ | ------------ |
| `--input`   | Input Excel file path          | ip_list.xlsx |
| `--output`  | Output file base name          | ping_results |
| `--timeout` | Ping timeout in seconds        | 2            |
| `--count`   | Number of ping packets         | 1            |
| `--retries` | Number of ping retries         | 1            |
| `--threads` | Max concurrent threads         | 50           |
| `--formats` | Output formats (xlsx,csv,json) | xlsx         |

Example:

```bash
python ip_pinger.py --input network_devices.xlsx --output scan_results --timeout 3 --count 2 --retries 2 --threads 100 --formats xlsx csv
```

## Sample Report Output

```
=== Ping Results Summary ===
Total IPs: 150
Active: 132
Inactive: 12
Unreachable: 4
Timeouts: 2
Avg Latency (ms): 24.57
Unresolvable Hosts: 8
Success Rate: 88.00%
```

## File Structure

```
ip-pinger/
├── ip_pinger.py       # Main application code
├── requirements.txt   # Dependency list
├── ip_pinger.log      # Generated log file
├── ip_list.xlsx       # Sample input file
└── ping_results.xlsx  # Sample output file
```

## **Functions Overview**

### `parse_args() -> argparse.Namespace`

Parses command-line arguments using Python's `argparse` module.  
Allows the user to configure:

- Input file path
- Output file name and formats
- Ping timeout, count, and retries
- Maximum number of concurrent threads  
  Returns an `argparse.Namespace` object with the parsed options.

---

### `validate_ip(ip: str) -> bool`

Checks whether the given IP address is valid.  
Uses Python’s `ipaddress` module to verify format correctness.  
Returns `True` if valid, otherwise `False`.

---

### `parse_latency(ping_output: str) -> Union[float, None]`

Extracts the average ping latency from the raw ping output string.  
Handles both Windows and Linux/Unix ping output formats using regular expressions.  
Returns:

- `float` value representing latency in milliseconds, or
- `None` if latency couldn't be determined.

---

### `ping_ip(ip: str, timeout: int = 2, count: int = 1) -> Tuple[str, Union[float, None]]`

Executes a single ping operation to the given IP address.  
Automatically adjusts ping command based on the operating system.  
Parses response to determine status and latency.

Returns a tuple:

- `status`: A string like `"Active"`, `"Timeout"`, `"Unreachable"`, `"Unknown Host"`, or error.
- `latency`: Ping response time in ms, or `None` if not available.

---

### `ping_with_retry(ip: str, timeout: int = 2, count: int = 1, retries: int = 1) -> Tuple[str, Union[float, None]]`

Adds retry logic around the `ping_ip()` function.  
Attempts to ping an IP multiple times if initial attempts fail.  
Returns the first `"Active"` result found, or the final failed result after retries.

---

### `resolve_hostname(ip: str) -> str`

Attempts to resolve the hostname associated with the given IP address using reverse DNS lookup (`socket.gethostbyaddr`).  
Handles errors gracefully.

Returns:

- Hostname as a string if successful,
- `"Unresolvable"` if it can't be resolved,
- `"Error resolving"` for unexpected errors.

---

### `ping_ips_parallel(ip_list: List[str], timeout: int, count: int, retries: int, max_workers: int) -> Dict[str, Tuple[str, Union[float, None]]]`

Executes ping operations for a list of IPs in parallel using a thread pool.  
Improves efficiency by using `concurrent.futures.ThreadPoolExecutor`.  
Displays a real-time progress bar via `tqdm`.

Returns:

- A dictionary mapping each IP to a tuple `(status, latency)`.

---

### `save_results(df: pd.DataFrame, filename: str, formats: List[str]) -> None`

Saves the result DataFrame to one or more file formats:

- Excel (`.xlsx`)
- CSV (`.csv`)
- JSON (`.json`)

Handles file write operations safely and logs success or failure.

---

### `generate_report(df: pd.DataFrame) -> None`

Generates a colorful summary report of ping statistics.  
Uses `colorama` to highlight output in the terminal.  
Displays:

- Total IPs processed
- Count of each status (Active, Inactive, Timeout, etc.)
- Average latency for active IPs
- Count of unresolvable hostnames
- Overall success rate as a percentage

---

### `main()`

The primary driver of the script. It:

1. Parses command-line arguments
2. Reads the input Excel file
3. Validates IPs
4. Performs parallel ping operations
5. Resolves hostnames
6. Updates the DataFrame
7. Saves results
8. Prints a summary report

Includes robust exception handling for common errors (missing files, bad IPs, etc.).

---

## Input File Format

Create an Excel file (`ip_list.xlsx` by default) with:

| IP Address  |
| ----------- |
| 192.168.1.1 |
| 10.0.0.1    |
| ...         |

## Output File Contents

The output file will contain:

| IP Address  | Status  | Latency | Hostname      |
| ----------- | ------- | ------- | ------------- |
| 192.168.1.1 | Active  | 24.5    | router1.local |
| 10.0.0.1    | Timeout | -       | Unresolvable  |
| ...         | ...     | ...     | ...           |

## Troubleshooting

1. **Permission Errors**:

   - Ensure write permissions in output directory
   - Close Excel before running if outputting to xlsx

2. **Ping Command Not Found**:

   - Verify ping utility is in system PATH
   - On Windows, check if ICMP is allowed through firewall

3. **Hostname Resolution Issues**:
   - Verify DNS server accessibility
   - Check reverse DNS records exist for your IPs

View detailed logs in `ip_pinger.log` for debugging.

## License

MIT License - Free for commercial and personal use

## Contact

For support or feature requests, please open a GitHub issue.
