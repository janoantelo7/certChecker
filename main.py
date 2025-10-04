from certificate import Certificate
import argparse

def check_certificate_expiry(hostname):
    cert = Certificate(hostname)

    days_left = cert.days_until_expiration()
    
    if days_left <= 0:
        print(f"Warning: The certificate for {hostname} expires in {days_left} days!")
    elif days_left <= 30:
        print(f"The certificate for {hostname} has already expired.")
    else:
        print(f"The certificate for {hostname} is valid for another {days_left} days.")
        print(f"Certificate expiry date: {cert.get_expiry_date()}")

def main():
    parser = argparse.ArgumentParser(description='Check SSL certificate expiry for a given hostname.')
    parser.add_argument("-H", "--hostname", dest="hostname",type=str, help="Domain name to check the SSL certificate for.", required=False)
    args = parser.parse_args()

    if args.hostname:
        hostname = args.hostname
    else:
        hostname = input("Enter the domain name to check the SSL certificate for: ")

    check_certificate_expiry(hostname)

if __name__ == "__main__":
    main()
