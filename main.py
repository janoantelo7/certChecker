from certificate import Certificate
import argparse
import sys

__version__ = "0.1.4"

def check_certificate_expiry(hostname):
    if not hostname:
        print("Error: No hostname provided.", file=sys.stderr)
        return

    try:
        cert = Certificate(hostname)
        expiry_date = cert.get_expiry_date()
        days_left = cert.days_until_expiration()
    except (ConnectionError, ValueError) as e:
        print(f"Error checking certificate for {hostname}: {e}", file=sys.stderr)
        return
        
    if days_left <= 0:
        print(f"The certificate for {hostname} has already expired. (Expired on {expiry_date})")
    elif days_left <= 30:
        print(f"Warning: The certificate for {hostname} expires in {days_left} days! (Expiry date: {expiry_date})")
    else:
        print(f"The certificate for {hostname} is valid for another {days_left} days. (Expiry date: {expiry_date})")

def main():
    parser = argparse.ArgumentParser(description='Check SSL certificate expiry for a given hostname.')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument("-H", "--hostname", dest="hostname",type=str, help="Domain name to check the SSL certificate for", required=False)
    parser.add_argument("-f", "--file", dest="file", type=str, help="File containing a list of domain names to check", required=False)

    args = parser.parse_args()

    if args.hostname:
        check_certificate_expiry(args.hostname)
    elif args.file:
        try: 
            with open(args.file, 'r') as f:
                for line in f:
                    if not line.strip():
                        continue

                    check_certificate_expiry(line.strip())
        except FileNotFoundError:
            print(f"Error: The file '{args.file}' was not found.", file=sys.stderr)
            sys.exit(1)  
    else:
        hostname = input("Enter the domain name to check the SSL certificate for: ").strip()
        check_certificate_expiry(hostname)

if __name__ == "__main__":
    main()
