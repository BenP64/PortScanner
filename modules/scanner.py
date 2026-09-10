import socket, ipaddress, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import timedelta

def validate_ip(target_ip):
    """ Validates the IP and returns it as a string """
    stripped_ip = target_ip.strip()
    try:
        validated_ip = ipaddress.ip_address(stripped_ip)
        return str(validated_ip) # Returns the validated IP as a string
    except ValueError:
        print(f'"{target_ip}" is not a valid IP address')
        return None


def parse_port_range(input_range):
    """ Parses input port range into (start, end), raises ValueError on bad input. """
    try:
        start_str, end_str = input_range.split("-")
        start, end = int(start_str.strip()), int(end_str.strip())
    except ValueError:
        raise ValueError("Port range must be integers and include a hyphen '-', (e.g. 20-100)")

    if not (0 <= start <= 65535 and 0 <= end <= 65535):
        print("Ports must be between 0 and 65535")
    if start > end:
        print("Start port cannot be larger than end port")

    return start, end # returns start and end port as validated integers.


def scan_port(ip, port):
    """ Returns (port, open status, banner) for every port scanned. """
    try:
        with socket.socket() as s:
            s.settimeout(1)
            s.connect((ip, port)) # Port is open when .connect() succeeds
            banner = ""
            try:
                banner = s.recv(1024).decode().strip() # receive socket banner
            except (socket.timeout, UnicodeDecodeError, OSError):
                pass # no banner, port is still open.
            return port, True, banner

    except (TimeoutError, ConnectionRefusedError):
        return port, False, ""

    except OSError as e: # Handles unexpected errors: resource limits, routing issues...
        return port, False, f"Error: {e}"


def scan(target_ip, start_port, end_port, max_workers=2000):
    """ Scan a range of ports and print the open ones """
    ip = validate_ip(target_ip)
    if isinstance(ip, str):
        print(f"Starting scan on {ip} from port {start_port} to port {end_port}...")
        start_time = time.time()

        open_ports = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(scan_port, ip, port)
                for port in range(start_port, end_port + 1)
            ]
            for future in as_completed(futures):
                port, open_status, banner = future.result()
                if open_status:
                    if banner:
                        print(f"Port {port} is Open: {banner}")
                    else:
                        print(f"Port {port} is open.")
                    open_ports.append(port)

        end_time = time.time()
        elapsed = end_time - start_time
        print(f"\nScan complete! {len(open_ports)} open port(s) found in: {str(timedelta(seconds=elapsed))[:-3]}")
        return True
    else:
        print(f"Error. {target_ip} is not a valid IP address")
        return False


def port_scanner():
    """ Main function responsible for combining the functions to create the scan and output"""
    try:
        input_ip = input("Target ip: ")
        input_port_range = input("Port range: ")
        start, end = parse_port_range(input_port_range)
        scan(input_ip, start, end)
    except ValueError as e:
        print(f"{e}")
    except KeyboardInterrupt:
        print("Scan cancelled.")
