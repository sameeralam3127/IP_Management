# IP Pinger Tool - Advanced Network Monitoring

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 📝 Overview

The IP Pinger Tool is a robust Python application designed for network administrators and IT professionals to efficiently monitor network devices. It provides parallel ping operations, hostname resolution, and comprehensive reporting capabilities.

## ✨ Features

- **Parallel Processing**: Ping hundreds of IPs simultaneously
- **Detailed Reporting**: Get latency metrics and status reports
- **Multiple Output Formats**: Export results in Excel, CSV, or JSON
- **Smart Retry Mechanism**: Configurable retries for flaky connections
- **Hostname Resolution**: Automatically resolves hostnames
- **Colorful Console Output**: Easy-to-read status information
- **Comprehensive Logging**: Detailed operation logs for debugging

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/sameeralam3127/IP_Management.git
cd IP_Management
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Basic Command
```bash
python ip_pinger.py
```

### Advanced Options
| Parameter       | Description                          | Default      |
|-----------------|--------------------------------------|--------------|
| `--input`       | Input Excel file path                | ip_list.xlsx |
| `--output`      | Output file base name                | ping_results |
| `--timeout`     | Ping timeout in seconds              | 2            |
| `--count`       | Number of ping packets               | 1            |
| `--retries`     | Number of ping retries               | 1            |
| `--threads`     | Max concurrent threads               | 50           |
| `--formats`     | Output formats (xlsx,csv,json)       | xlsx         |

Example:
```bash
python ip_pinger.py --input network_devices.xlsx --output scan_results --timeout 3 --count 2 --retries 2 --threads 100 --formats xlsx csv
```

## 📊 Sample Report Output

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

## 📂 File Structure

```
ip-pinger/
├── ip_pinger.py       # Main application code
├── requirements.txt   # Dependency list
├── ip_pinger.log      # Generated log file
├── ip_list.xlsx       # Sample input file
└── ping_results.xlsx  # Sample output file
```

## 🔧 Functions Reference

### `ping_ip(ip, timeout=2, count=1)`
- Performs a single ping operation
- Returns: (status, latency) tuple
- Handles platform-specific ping commands

### `ping_with_retry(ip, timeout=2, count=1, retries=1)`
- Implements retry logic for unreliable connections
- Returns best available status from multiple attempts

### `ping_ips_parallel(ip_list, timeout=2, count=1, retries=1, max_workers=50)`
- Parallel ping execution using ThreadPoolExecutor
- Includes progress bar visualization

### `resolve_hostname(ip)`
- Performs reverse DNS lookup
- Handles various resolution error cases

### `generate_report(df)`
- Creates comprehensive summary statistics
- Displays colored output to console
- Calculates success rate metrics

### `save_results(df, filename, formats)`
- Exports results to multiple formats
- Supports concurrent file writing
- Handles write errors gracefully

## 📋 Input File Format

Create an Excel file (`ip_list.xlsx` by default) with:

| IP Address  |
|-------------|
| 192.168.1.1 |
| 10.0.0.1    |
| ...         |

## 📈 Output File Contents

The output file will contain:

| IP Address  | Status    | Latency | Hostname        |
|-------------|-----------|---------|-----------------|
| 192.168.1.1 | Active    | 24.5    | router1.local   |
| 10.0.0.1    | Timeout   | -       | Unresolvable    |
| ...         | ...       | ...     | ...             |

## 🛠 Troubleshooting

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

## 📜 License

MIT License - Free for commercial and personal use

## 📧 Contact

For support or feature requests, please open a GitHub issue.