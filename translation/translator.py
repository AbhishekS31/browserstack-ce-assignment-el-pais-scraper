import requests
from config.settings import RAPID_API_KEY

URL = "https://rapid-translate-multi-traduction.p.rapidapi.com/t"

HEADERS = {
    "content-type": "application/json",
    "X-RapidAPI-Key": RAPID_API_KEY,
    "X-RapidAPI-Host": "rapid-translate-multi-traduction.p.rapidapi.com"
}

def translate_to_english(text):
    if not text or not text.strip():
        return ""
    
    payload = {
        "from": "es",
        "to": "en",
        "q": text
    }

    try:
        response = requests.post(URL, json=payload, headers=HEADERS, timeout=10)

        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0]
            elif isinstance(result, str):
                return result
            return text  
        else:
            print(f"Translation API error: {response.status_code}")
            return text  
    except Exception as e:
        print(f"Translation error: {e}")
        return text  