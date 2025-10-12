# IP Pinger Tool – Automated Network Scanner & Monitor

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey)
![Threads](https://img.shields.io/badge/concurrency-multithreaded-orange)

## Overview

**IP Pinger Tool** is an advanced, automated network monitoring and diagnostics utility built in Python.
It’s designed for **network administrators, IT engineers, and DevOps professionals** who need to monitor device availability, detect outages, and analyze latency at scale.

This enhanced version supports:

- **Subnet auto-discovery**,
- **Automated Excel creation**,
- **Interval-based periodic scans**, and
- **Multi-format result export** — all while maintaining high performance through parallel execution.

---

## Features

- **Parallel Processing** – Ping hundreds of IPs simultaneously with `ThreadPoolExecutor`
- **Smart Retry Mechanism** – Reattempt unreachable IPs automatically
- **Auto Subnet Discovery** – Scan your entire `/24` subnet without input files
- **Automatic Input File Creation** – Creates `ip_list.xlsx` if not found
- **Comprehensive Reporting** – Summary by status, latency, and success rate
- **Multi-Format Export** – Save results in `Excel`, `CSV`, or `JSON`
- **Colorized CLI Output** – Clear visibility with `colorama`
- **Scheduled Scans** – Periodically run pings using `--interval` mode
- **Hostname Resolution** – Reverse DNS lookup for devices
- **Cross-Platform Compatibility** – Works seamlessly on **Windows** and **Linux**

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/sameeralam3127/IP_Management.git
cd IP_Management
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

### Basic Command

```bash
python ip_pinger.py
```

If no input file is found, the tool will automatically create a sample `ip_list.xlsx`.

---

### Advanced Options

| Parameter    | Description                            | Default        |
| ------------ | -------------------------------------- | -------------- |
| `--input`    | Input Excel file path                  | `ip_list.xlsx` |
| `--output`   | Output file base name                  | `ping_results` |
| `--timeout`  | Ping timeout in seconds                | `2`            |
| `--count`    | Number of ping packets per IP          | `1`            |
| `--retries`  | Number of retries per IP               | `1`            |
| `--threads`  | Max concurrent threads                 | `50`           |
| `--formats`  | Output formats (`xlsx`, `csv`, `json`) | `xlsx`         |
| `--discover` | Auto-discover local subnet IPs         | `False`        |
| `--interval` | Repeat scan every N minutes            | None           |
| `--verbose`  | Enable detailed debug logging          | Off            |

---

### Example: Custom Configuration

```bash
python ip_pinger.py \
  --input network_devices.xlsx \
  --output scan_results \
  --timeout 3 \
  --count 2 \
  --retries 2 \
  --threads 100 \
  --formats xlsx csv json
```

### Example: Auto Subnet Discovery

```bash
python ip_pinger.py --discover --threads 200
```

### Example: Periodic Pinging (every 10 minutes)

```bash
python ip_pinger.py --input ip_list.xlsx --interval 10
```

---

## Sample Output Report

```
=== Network Ping Summary ===
Active: 132
Inactive: 12
Unreachable: 4
Timeout: 2
Total: 150
Success Rate: 88.00%
```

---

## File Structure

```
ip-pinger/
├── ip_pinger.py         # Main application script
├── requirements.txt     # Python dependencies
├── auto_ping.log        # Runtime log file
├── ip_list.xlsx         # Sample input (auto-generated if missing)
└── ping_results_YYYYMMDD_HHMMSS.xlsx  # Timestamped output
```

---

## Key Functions Overview

### `parse_args()`

Parses CLI arguments (using `argparse`) to configure ping parameters, output options, and automation flags.

### `validate_ip(ip: str) -> bool`

Validates IP address syntax using `ipaddress`.

### `ping_ip(ip: str, timeout: int, count: int)`

Executes OS-appropriate ping command and returns `(status, latency)`.

### `ping_ips_parallel(ip_list, timeout, count, retries, max_workers)`

Pings all IPs concurrently with progress tracking via `tqdm`.

### `resolve_hostname(ip: str) -> str`

Performs reverse DNS lookup, handling errors gracefully.

### `save_results(df, filename, formats)`

Saves ping results in multiple formats — `.xlsx`, `.csv`, `.json`.

### `generate_report(df)`

Displays a colorized summary including latency averages and success rate.

### `get_local_subnet_ips()`

Auto-discovers local subnet IPs from the host’s current interface.

### `create_sample_excel(filename)`

Automatically generates a sample Excel file if none is found.

### `main()`

Main execution flow — parses arguments, validates input, runs pings, resolves hostnames, saves results, and displays a summary.

---

## Input File Format

Default: `ip_list.xlsx`

| IP Address  |
| ----------- |
| 192.168.1.1 |
| 10.0.0.1    |
| 8.8.8.8     |

---

## Output File Format

| IP Address  | Status  | Latency | Hostname     | Timestamp           |
| ----------- | ------- | ------- | ------------ | ------------------- |
| 192.168.1.1 | Active  | 24.5 ms | router.local | 2025-10-12 18:40:15 |
| 10.0.0.1    | Timeout | —       | Unresolvable | 2025-10-12 18:40:15 |

---

## Troubleshooting

| Issue                    | Cause                              | Solution                                                                 |
| ------------------------ | ---------------------------------- | ------------------------------------------------------------------------ |
| `Ping Command Not Found` | `ping` utility missing             | Install `iputils-ping` (Linux) or ensure `ping.exe` is in PATH (Windows) |
| `Permission Denied`      | No write access to folder          | Run with proper permissions or change output directory                   |
| `Hostname Unresolvable`  | DNS not reachable or no PTR record | Verify DNS or add reverse lookup entries                                 |
| `Excel Locked`           | File open in another program       | Close file before saving new results                                     |

View detailed runtime logs in **`auto_ping.log`** for debugging.

---

## Requirements

- **Python 3.8+**
- Libraries:

  ```bash
  pandas
  tqdm
  colorama
  openpyxl
  ```

---

## License

**MIT License**
Free for both personal and commercial use. Attribution appreciated.

---

## Contact

**Author:** [Sameer Alam](https://github.com/sameeralam3127)
For issues or feature requests, open a GitHub issue in the repository.

> Made with ❤️ and Python 🐍 by [Sameer Alam](https://github.com/sameeralam3127)
