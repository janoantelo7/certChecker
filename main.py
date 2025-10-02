from certificate import Certifiacate

def main():
    hostname = 'www.example.com'  
    cert = Certifiacate(hostname)
    try:
        days_left = cert.days_until_expiration()
        
        if days_left <= 30:
            print(f"Warning: The certificate for {hostname} expires in {days_left} days!")
        elif days_left < 0:
            print(f"The certificate for {hostname} has already expired.")
        else:
            print(f"The certificate for {hostname} is valid for another {days_left} days.")
            print(f"Certificate expiry date: {cert.get_expiry_date()}")
        
    except Exception as e:
        print(f"Error retrieving certificate: {hostname}\n{e}")
        return -1

if __name__ == "__main__":
    main()
