import tkinter as tk
from tkinter import ttk, messagebox
from serpapi import GoogleSearch

# Funções principais do programa
def escolher_destinos():
    origem = origem_var.get()
    data_partida = partida_entry.get()
    data_retorno = retorno_entry.get()
    intermediarios = int(destinos_var.get())
    destinos = []

    if not origem or not data_partida:
        messagebox.showerror("Erro", "Por favor, preencha a origem e a data de partida.")
        return
    
    for i in range(intermediarios):
        destino = destino_entries[i].get()
        data = data_entries[i].get()
        if destino and data:
            destinos.append({"origem": origem, "destino": destino, "data_partida": data})
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos de destino.")
            return
    
    buscar_voo(destinos)

def buscar_voo(destinos):
    # Substitua pela sua chave de API da SerpApi
    api_key = 'f17f0ff356e33412554db739686d87900c82902477a7a7e353f32d87e9422984'
    
    result_text.delete(1.0, tk.END)  # Limpa o campo de resultado

    for trajeto in destinos:
        origem = trajeto["origem"]
        destino = trajeto["destino"]
        data_partida = trajeto["data_partida"]
        
        # Parâmetros de busca
        params = {
            "engine": "google_flights",
            "hl": "en",
            "gl": "us",
            "departure_id": origem[:3].upper(),
            "arrival_id": destino[:3].upper(),
            "outbound_date": data_partida,
            "currency": "EUR",
            "type": "2",
            "api_key": api_key
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()

        menor_emissao = float('inf')
        voo_menor_emissao = None
        for flight in results.get("best_flights", []):
            emissao_atual = flight.get("carbon_emissions", {}).get("this_flight", float('inf'))
            if emissao_atual < menor_emissao:
                menor_emissao = emissao_atual
                voo_menor_emissao = {
                    "origem": origem,
                    "destino": destino,
                    "data_partida": data_partida,
                    "emissao_co2": menor_emissao,
                    "preco": flight.get("price"),
                    "total_duration": flight.get("total_duration"),
                    "flight_number": flight.get("flights", [{}])[0].get("flight_number")
                }
        
        # Exibe os resultados na interface
        if voo_menor_emissao:
            result_text.insert(tk.END, f"\nVoo encontrado:\nOrigem: {voo_menor_emissao['origem']} -> Destino: {voo_menor_emissao['destino']}\n")
            result_text.insert(tk.END, f"Data: {voo_menor_emissao['data_partida']}\nVoo: {voo_menor_emissao['flight_number']}\n")
            result_text.insert(tk.END, f"Emissão CO₂: {voo_menor_emissao['emissao_co2']}g\nPreço: €{voo_menor_emissao['preco']}\nDuração: {voo_menor_emissao['total_duration']} minutos\n\n")
        else:
            result_text.insert(tk.END, f"\nNenhum voo encontrado de {origem} para {destino} na data {data_partida}.\n")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Travel Planner")
root.geometry("600x500")

# Labels e caixas de entrada
ttk.Label(root, text="Origem:").grid(row=0, column=0, padx=10, pady=10)
origem_var = tk.StringVar()
origem_entry = ttk.Entry(root, textvariable=origem_var)
origem_entry.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(root, text="Data de Partida:").grid(row=0, column=2, padx=10, pady=10)
partida_entry = ttk.Entry(root)
partida_entry.grid(row=0, column=3, padx=10, pady=10)

ttk.Label(root, text="Data de Retorno:").grid(row=1, column=2, padx=10, pady=10)
retorno_entry = ttk.Entry(root)
retorno_entry.grid(row=1, column=3, padx=10, pady=10)

ttk.Label(root, text="Número de Destinos Intermediários:").grid(row=2, column=0, padx=10, pady=10)
destinos_var = tk.StringVar(value="1")
destinos_combo = ttk.Combobox(root, textvariable=destinos_var, values=[1, 2, 3, 4])
destinos_combo.grid(row=2, column=1, padx=10, pady=10)

# Campos para destinos e datas
destino_entries = []
data_entries = []
for i in range(4):
    destino_label = ttk.Label(root, text=f"Destino {i + 1}:")
    destino_label.grid(row=3 + i, column=0, padx=10, pady=5)
    destino_entry = ttk.Entry(root)
    destino_entry.grid(row=3 + i, column=1, padx=10, pady=5)
    destino_entries.append(destino_entry)
    
    data_label = ttk.Label(root, text="Data:")
    data_label.grid(row=3 + i, column=2, padx=10, pady=5)
    data_entry = ttk.Entry(root)
    data_entry.grid(row=3 + i, column=3, padx=10, pady=5)
    data_entries.append(data_entry)

# Botão para gerar itinerário
generate_button = ttk.Button(root, text="Gerar Itinerário", command=escolher_destinos)
generate_button.grid(row=7, column=0, columnspan=4, pady=20)

# Campo de texto para resultados
result_text = tk.Text(root, wrap="word", width=70, height=10)
result_text.grid(row=8, column=0, columnspan=4, padx=10, pady=10)

root.mainloop()