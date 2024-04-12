import json
import requests

class IPGeolocation:
    def __init__(self):
        self.api_key = "be0d647a4e1c44ec828ae2abd8f37ef6"

    def get_geolocation(self, ip):

        # Montar url da Request
        url = f"https://api.ipgeolocation.io/ipgeo?apiKey={self.api_key}&ip={ip}"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Ler a resposta da API e retornar latitude e longitude
            response_json = json.loads(response.text)
            return {
                "latitude": response_json["latitude"],
                "longitude": response_json["longitude"]
            }
        else:
            print("Error:", response.status_code, response.reason)
            return None
