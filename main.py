from certificate import Certificate
import argparse
import sys

__version__ = "0.3.1"

def check_certificate_expiry(cert):
    expiry_date = cert.expiry_date()
    days_left = cert.days_until_expiration()
    
    if days_left <= 0:
        status_message = f"Status: EXPIRED on {expiry_date}"
    elif days_left <= 30:
        status_message = f"Status: WARNING - Expires in {days_left} days (on {expiry_date})"
    else:
        status_message = f"Status: OK - Valid for {days_left} more days (expires on {expiry_date})"
    print(status_message)

def process_hostname(hostname):
        
        if not hostname:
            print("Error: No hostname provided.", file=sys.stderr)
            return
        try:
            cert = Certificate(hostname)
            print(f"--> Checking certificate for {hostname}")
            check_certificate_expiry(cert)
        except (ConnectionError, ValueError) as e:
            print(f"Error checking certificate for {hostname}: {e}", file=sys.stderr)
            return

def main():
    parser = argparse.ArgumentParser(description='Check SSL certificate expiry for a given hostname.')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument("-H", "--hostname", dest="hostname",type=str, help="Domain name to check the SSL certificate for", required=False)
    parser.add_argument("-f", "--file", dest="file", type=str, help="File containing a list of domain names to check", required=False)

    args = parser.parse_args()

    if args.hostname:
        process_hostname(args.hostname)
    elif args.file:
        try: 
            with open(args.file, 'r') as f:
                for line in f:
                    if not line.strip():
                        # Skip empty lines
                        continue

                    process_hostname(line.strip())
                    print("--"*40)
        except FileNotFoundError:
            print(f"Error: The file '{args.file}' was not found.", file=sys.stderr)
            sys.exit(1)  
    else:
        hostname = input("Enter the domain name to check the SSL certificate for: ").strip()
        process_hostname(hostname)

if __name__ == "__main__":
    main()
