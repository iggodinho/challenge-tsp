# flight_search/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from .utils import buscar_voos, aeroporto  # Importe aeroporto de utils.py

def flight_selection_view(request):
    if request.method == "POST":
        origem = request.POST.get("origem")
        num_destinos = request.POST.get("numDestinos")

        # Defina um valor padrão para `num_destinos` se não for especificado
        num_destinos = int(num_destinos) if num_destinos else 1
        
        destinos = []
        
        # Coleta os destinos e as datas de partida, evitando duplicação com origem
        for i in range(1, num_destinos + 1):
            destino = request.POST.get(f"destino-{i}")
            data_partida = request.POST.get(f"data-partida-{i}")
            if destino and destino != origem:  # Certifique-se de que destino é diferente da origem
                destinos.append({"destino": destino, "data_partida": data_partida})

        # Salve a origem e destinos no session
        request.session['origem'] = origem
        request.session['destinos'] = destinos
        
        return redirect(reverse('flight_results'))

    return render(request, 'flight_search/selection.html', {'aeroporto': aeroporto})

def flight_results_view(request):
    # Recupera os dados da seleção de voos armazenados na session
    origem = request.session.get("origem")
    destinos = request.session.get("destinos", [])
    api_key = 'f17f0ff356e33412554db739686d87900c82902477a7a7e353f32d87e9422984'  # Substitua pela sua chave de API da SerpApi

    results = []
    # Itera por todos os destinos, criando um trajeto para cada destino intermediário
    for trajeto in destinos:
        destino = trajeto['destino']
        data_partida = trajeto['data_partida']
        
        # Chama buscar_voos para cada trajeto e coleta o resultado
        menor_emissao, mais_barato, mais_rapido = buscar_voos(api_key, origem, destino, data_partida)
        
        # Adiciona o resultado do trajeto à lista de results
        results.append({
            "origem": origem,
            "destino": destino,
            "data_partida": data_partida,
            "menor_emissao": menor_emissao,
            "mais_barato": mais_barato,
            "mais_rapido": mais_rapido
        })
        
        # Atualiza a origem para o próximo destino
        origem = destino

    # Passa todos os trajetos para o template
    return render(request, 'flight_search/results.html', {'results': results})

    