# flight_search/utils.py
from serpapi import GoogleSearch

# Dicionário de aeroportos
aeroporto = {
    "Madrid": "MAD",
    "Oslo": "OSL",
    "Roma": "FCO",
    "Paris": "CDG",
    "Berlin": "BER"
}

def buscar_voos(api_key, origem, destino, data_partida):
    params = {
        "engine": "google_flights",
        "hl": "en",
        "gl": "us",
        "departure_id": aeroporto.get(origem),
        "arrival_id": aeroporto.get(destino),
        "outbound_date": data_partida,
        "currency": "EUR",
        "type": "2",
        "api_key": "f17f0ff356e33412554db739686d87900c82902477a7a7e353f32d87e9422984"
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()


    # Inicializa os menores valores para cada critério e dicionários vazios para os voos
    menor_emissao = float('inf')
    menor_preco = float('inf')
    menor_duracao = float('inf')
    
    voo_menor_emissao = None
    voo_mais_barato = None
    voo_mais_rapido = None

    # Itera por todos os voos encontrados para selecionar opções distintas
    for flight in results.get("best_flights", []):
        emissao_atual = flight.get("carbon_emissions", {}).get("this_flight", float('inf'))
        preco_atual = flight.get("price", float('inf'))
        duracao_atual = flight.get("total_duration", float('inf'))
        
        # Seleciona o voo com menor emissão de CO₂
        if emissao_atual < menor_emissao:
            menor_emissao = emissao_atual
            voo_menor_emissao = {
                "flight_number": flight.get("flights", [{}])[0].get("flight_number", "N/A"),
                "emissao_co2": menor_emissao,
                "preco": preco_atual,
                "total_duration": duracao_atual
            }
        
        # Seleciona o voo com menor preço
        if preco_atual < menor_preco:
            menor_preco = preco_atual
            voo_mais_barato = {
                "flight_number": flight.get("flights", [{}])[0].get("flight_number", "N/A"),
                "emissao_co2": emissao_atual,
                "preco": menor_preco,
                "total_duration": duracao_atual
            }
        
        # Seleciona o voo com menor duração
        if duracao_atual < menor_duracao:
            menor_duracao = duracao_atual
            voo_mais_rapido = {
                "flight_number": flight.get("flights", [{}])[0].get("flight_number", "N/A"),
                "emissao_co2": emissao_atual,
                "preco": preco_atual,
                "total_duration": menor_duracao
            }

    # Retorna voos ou valores vazios se nenhum voo for encontrado
    return voo_menor_emissao or {}, voo_mais_barato or {}, voo_mais_rapido or {}
