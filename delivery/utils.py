import requests
from django.conf import settings

def send_sms_via_smsoffice(destination):
    url = "https://smsoffice.ge/api/v2/send/"
    payload = {
        "key": settings.SMSOFFICE_API_KEY,
        "destination": destination,
        "sender": "Deliverow",
        "content": "თქვენთან მოემართება კურიერი!",
        "urgent": "true"
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    try:
        response = requests.post(url, data=payload, headers=headers)
        return response.json()
    except requests.RequestException as e:
        return None