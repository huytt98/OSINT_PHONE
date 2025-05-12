import requests
from bs4 import BeautifulSoup
import re
import time
import json

class SocialScanner:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.social_sites = {
            'facebook': 'https://www.facebook.com',
            'instagram': 'https://www.instagram.com',
            'twitter': 'https://twitter.com',
            'linkedin': 'https://www.linkedin.com',
            'telegram': 'https://t.me',
            'whatsapp': 'https://wa.me'
        }
        
    def find_social_accounts(self, phone_number):
        """Find social media accounts associated with the phone number."""
        results = {}
        clean_number = phone_number.replace('+', '').replace(' ', '')
        
        for platform, url in self.social_sites.items():
            try:
                response = requests.head(f"{url}/{clean_number}", 
                                      headers=self.headers, 
                                      allow_redirects=True,
                                      timeout=5)
                if response.status_code == 200:
                    results[platform] = f"{url}/{clean_number}"
            except:
                continue
            time.sleep(1)
        
        return results
    
    def find_email_accounts(self, phone_number):
        """Find email accounts associated with the phone number."""
        email_services = [
            'gmail.com',
            'yahoo.com',
            'hotmail.com',
            'outlook.com'
        ]
        
        clean_number = phone_number.replace('+', '').replace(' ', '')
        possible_emails = []
        
        # Generate possible email patterns
        patterns = [
            f"{clean_number}@",
            f"phone{clean_number}@",
            f"mobile{clean_number}@",
            f"tel{clean_number}@"
        ]
        
        for pattern in patterns:
            for service in email_services:
                possible_emails.append(f"{pattern}{service}")
        
        return possible_emails
