from serpapi import GoogleSearch
import requests

# Substitua 'SUA_API_KEY' pela sua chave de API
api_key = 'f17f0ff356e33412554db739686d87900c82902477a7a7e353f32d87e9422984'

params = {
  "engine": "google_flights",
  "hl": "en",
  "gl": "us",
  "departure_id": "CDG",
  "arrival_id": "OSL",
  "outbound_date": "2024-11-08",
  "currency": "EUR",
  "type": "2",
  "api_key": api_key
}

search = GoogleSearch(params)
results = search.get_dict()

# Exiba os resultados
print(results)
