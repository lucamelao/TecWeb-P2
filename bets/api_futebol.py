import requests
import json

round_api = "https://api.api-futebol.com.br/v1/campeonatos/10/rodadas/"
headers =  {"Authorization":"Bearer live_15eb31904abcf4415c0444bc1a2306"}

def get_results(round):
    api = round_api + str(round)
    json_api = (requests.get(api, headers=headers)).json()
    partidas = json_api["partidas"]
    return partidas
