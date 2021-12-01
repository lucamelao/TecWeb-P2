import requests
import json

round_api = "https://api.api-futebol.com.br/v1/campeonatos/10/rodadas/"
headers =  {"Authorization":"Bearer live_6cb4e5666f9c190794fd4e9ac930ca"}

def get_results(round):
    api = round_api + str(round)
    json_api = (requests.get(api, headers=headers)).json()
    partidas = json_api["partidas"]
    return partidas
