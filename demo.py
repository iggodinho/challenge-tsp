from serpapi import GoogleSearch
import requests

# Dicionário de aeroportos
aeroporto = {
    "Madrid": "MAD",
    "Oslo": "OSL",
    "Roma": "ROM",
    "Paris": "CDG",
    "Berlin": "BER"
}

def escolher_destinos():
    cidades = list(aeroporto.keys())
    print("Escolha a cidade de origem:")
    for i, cidade in enumerate(cidades, start=1):
        print(f"{i}. {cidade}")
    origem_idx = int(input("Digite o número da cidade de origem: ")) - 1
    origem = cidades[origem_idx]
    
    print("\nQuantos destinos intermediários deseja (1-4)?")
    intermediarios = int(input("Digite o número de destinos: "))
    if intermediarios < 1 or intermediarios > 4:
        print("Número inválido. Por favor, escolha entre 1 e 4.")
        return
    
    destinos = []
    for i in range(intermediarios):
        print("\nEscolha a próxima cidade de destino:")
        for j, cidade in enumerate(cidades, start=1):
            if cidade != origem and cidade not in destinos:
                print(f"{j}. {cidade}")
        
        destino_idx = int(input("Digite o número da cidade de destino: ")) - 1
        destino = cidades[destino_idx]
        data_partida = input("Digite a data de partida (AAAA-MM-DD): ")
        destinos.append({"origem": origem, "destino": destino, "data_partida": data_partida})
        origem = destino
    
    return destinos

def buscar_voos(api_key, origem, destino, data_partida):
    params = {
        "engine": "google_flights",
        "hl": "en",
        "gl": "us",
        "departure_id": aeroporto[origem],
        "arrival_id": aeroporto[destino],
        "outbound_date": data_partida,
        "currency": "EUR",
        "type": "2",
        "api_key": api_key
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    
    # Inicializa as variáveis para armazenar os menores valores para cada critério
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
                "origem": origem,
                "destino": destino,
                "data_partida": data_partida,
                "emissao_co2": menor_emissao,
                "preco": preco_atual,
                "total_duration": duracao_atual,
                "flight_number": flight.get("flights", [{}])[0].get("flight_number")
            }
        
        # Seleciona o voo com menor preço
        if preco_atual < menor_preco:
            menor_preco = preco_atual
            voo_mais_barato = {
                "origem": origem,
                "destino": destino,
                "data_partida": data_partida,
                "emissao_co2": emissao_atual,
                "preco": menor_preco,
                "total_duration": duracao_atual,
                "flight_number": flight.get("flights", [{}])[0].get("flight_number")
            }
        
        # Seleciona o voo com menor duração
        if duracao_atual < menor_duracao:
            menor_duracao = duracao_atual
            voo_mais_rapido = {
                "origem": origem,
                "destino": destino,
                "data_partida": data_partida,
                "emissao_co2": emissao_atual,
                "preco": preco_atual,
                "total_duration": menor_duracao,
                "flight_number": flight.get("flights", [{}])[0].get("flight_number")
            }

    return voo_menor_emissao, voo_mais_barato, voo_mais_rapido

# Substitua pela sua chave de API da SerpApi
api_key = 'f17f0ff356e33412554db739686d87900c82902477a7a7e353f32d87e9422984'

# Executa o programa
destinos_escolhidos = escolher_destinos()

# Busca e exibe o voo de menor emissão, mais barato e mais rápido para cada trajeto escolhido
for trajeto in destinos_escolhidos:
    origem = trajeto["origem"]
    destino = trajeto["destino"]
    data_partida = trajeto["data_partida"]
    voo_menor_emissao, voo_mais_barato, voo_mais_rapido = buscar_voos(api_key, origem, destino, data_partida)
    
    print("\nResultados para o trajeto:")
    print(f"Origem: {origem} -> Destino: {destino}")
    print(f"Data de Partida: {data_partida}")
    
    if voo_menor_emissao:
        print("\nOpção com menor emissão de CO₂:")
        print(f"Voo: {voo_menor_emissao['flight_number']}")
        print(f"Emissão de CO₂: {voo_menor_emissao['emissao_co2']} gramas")
        print(f"Preço: €{voo_menor_emissao['preco']}")
        print(f"Duração Total: {voo_menor_emissao['total_duration']} minutos")

    if voo_mais_barato:
        print("\nOpção mais barata:")
        print(f"Voo: {voo_mais_barato['flight_number']}")
        print(f"Emissão de CO₂: {voo_mais_barato['emissao_co2']} gramas")
        print(f"Preço: €{voo_mais_barato['preco']}")
        print(f"Duração Total: {voo_mais_barato['total_duration']} minutos")

    if voo_mais_rapido:
        print("\nOpção mais rápida:")
        print(f"Voo: {voo_mais_rapido['flight_number']}")
        print(f"Emissão de CO₂: {voo_mais_rapido['emissao_co2']} gramas")
        print(f"Preço: €{voo_mais_rapido['preco']}")
        print(f"Duração Total: {voo_mais_rapido['total_duration']} minutos")
