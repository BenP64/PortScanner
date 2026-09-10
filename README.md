# Python Port Scanner
A simple project I made to learn about sockets and multithreading. It's a multithreaded TCP port scanner written completely in python. 
When given a target IP address and a port range, it attempts to connect to each port and reports which ones are open, optionally returning a service banner as well.

## Features
- Concurrent scanning using a thread pool for faster results.
- IP address validation
- Basic banner grabbing on open ports 
- Elapsed time reporting for scans

## Requirements
- Python 3.8+

## Installation
```bash
git clone ...
cd ...
```

## Usage
Run the script directly:
```bash
python scanner.py
```
You'll be prompted for two inputs:
```
Target ip: 192.168.1.1
Port range: 20-100
```

**Target ip** - A valid IPv4 or IPv6 address.

**Port range** - Two integers separated by a hyphen, e.g. "20-100".
Both values must be between "0" and "65535", and start port cannot be larger than the end port.

### Example output
```
Target ip: 192.168.1.1
Port range: 20-100
Starting scan on 192.168.1.1 from port 20 to port 100...
Port 22 is Open: SSH-2.0-OpenSSH_8.9
Port 80 is open.
 
Scan complete! 2 open port(s) found in: 0:00:01.243
```

## Specifications
| Item                 | Detail                                                          | 
|----------------------|-----------------------------------------------------------------|
| Language             | Python 3                                                        |
| Concurrency model    | `ThreadPoolExecutor`, default `max_workers=2000`                |
| Connection timeout   | 1 second per port                                               |
| Banner read          | Up to 1024 bytes, best effort (skipped silently if unavailable) |
| Supported IP formats | IPv4 and IPv6 (validated via `ipaddress` module)                |
| Port range           | 0–65535                                                         |
| Output               | Printed to stdout in real time as results complete              |

## How it works
1. **`validate_ip`** — checks the target IP is well-formed using Python's `ipaddress` module.
2. **`parse_port_range`** — parses the `start-end` input into two integers and checks they fall within valid bounds.
3. **`scan_port`** — attempts a TCP connection to a single port; if successful, tries to read a short banner.
4. **`scan`** — dispatches a `scan_port` call for every port in the range across a thread pool, printing results as they arrive.
5. **`port_scanner`** — the entry point that collects user input and ties the above together.


## Known Limitations
- Only supports TCP connect scans (no UDP or SYN scanning)
- No command-line flags — all input is via interactive prompts
- Very high thread counts (`max_workers=2000`) may hit OS-level file descriptor limits on some systems
- No logging to file; output is console-only