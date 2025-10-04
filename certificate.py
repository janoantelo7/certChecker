import ssl
import socket
import datetime
import sys

class Certificate:
    def __init__(self, hostname):
        self.hostname = hostname
        self.context = ssl.create_default_context()

        try:
            with socket.create_connection((self.hostname, 443)) as sock:
                with self.context.wrap_socket(sock, server_hostname=self.hostname) as ssock:
                    self.cert = ssock.getpeercert()
        except Exception as e:
            print(f"Error retrieving certificate for {self.hostname}: {e}")
            sys.exit(1)            

    def get_expiry_date(self):
        expiry_date = datetime.datetime.strptime(self.cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
        return expiry_date
    
    def days_until_expiration(self):
        expiry_date = self.get_expiry_date()
        return (expiry_date - datetime.datetime.now()).days
