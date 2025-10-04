from certificate import Certificate
import argparse
import sys

__version__ = "0.1.0"

def check_certificate_expiry(hostname):
    try:
        cert = Certificate(hostname)
    except ConnectionError as e:
        print(f"Error: {e}", file=sys.stderr)
        return
    
    days_left = cert.days_until_expiration()
    
    if days_left <= 0:
        print(f"The certificate for {hostname} has already expired.")
    elif days_left <= 30:
        print(f"Warning: The certificate for {hostname} expires in {days_left} days!")
    else:
        print(f"The certificate for {hostname} is valid for another {days_left} days.")
        print(f"Certificate expiry date: {cert.get_expiry_date()}")

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
                    hostname = line.strip()
                    check_certificate_expiry(hostname)
        except FileNotFoundError:
            print(f"Error: The file '{args.file}' was not found.", file=sys.stderr)
            sys.exit(1)
    else:
        hostname = input("Enter the domain name to check the SSL certificate for: ").strip()
        check_certificate_expiry(hostname)

if __name__ == "__main__":
    main()
