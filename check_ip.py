import socket
import requests
from requests.exceptions import RequestException

def get_ip():
    try:
        # Get local IP using alternative method
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        print(f"Local IP: {local_ip}")
    except Exception as e:
        print(f"Could not get local IP: {e}")

    # Try multiple services for public IP
    ip_services = [
        'https://api.ipify.org',
        'https://ifconfig.me/ip',
        'https://icanhazip.com'
    ]

    for service in ip_services:
        try:
            public_ip = requests.get(service, timeout=5).text.strip()
            print(f"Public IP: {public_ip}")
            break
        except RequestException as e:
            print(f"Error with {service}: {e}")
            continue

if __name__ == "__main__":
    get_ip()