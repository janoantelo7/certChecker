import ssl
import socket
import datetime

class Certificate:
    def __init__(self, hostname):
        self.hostname = hostname
        self.context = ssl.create_default_context()

        try:
            with socket.create_connection((self.hostname, 443)) as sock:
                with self.context.wrap_socket(sock, server_hostname=self.hostname) as ssock:
                    self.cert = ssock.getpeercert()
        except Exception as e:
            raise ConnectionError(f"Could not retrieve certificate for {self.hostname}: {e}")

    def expiry_date(self):
        try:
            expiry_date_str = self.cert.get('notAfter')
            if not expiry_date_str:
                raise ValueError("Expiry date not found in certificate.")
            return datetime.datetime.strptime(expiry_date_str, '%b %d %H:%M:%S %Y %Z')
        except (ValueError, KeyError) as e:
            raise ValueError(f"Could not parse expiry date for {self.hostname}: {e}")
    
    def days_until_expiration(self):
        expiry_date = self.expiry_date()
        return (expiry_date - datetime.datetime.now()).days
