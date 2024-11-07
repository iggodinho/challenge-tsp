#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <float.h>

#define MAX_CITIES 100
#define MAX_PATH 10
#define INF 1e9

// Estrutura para representar um trajeto
typedef struct {
    char origem[50];
    char destino[50];
    char meioDeTransporte[20];
    int preco;
    float duracao;
    float emissaoCO2;
} Trajeto;

// Estrutura para representar um grafo
typedef struct {
    int numCidades;
    char cidades[MAX_CITIES][50];
    float matrizCusto[MAX_CITIES][MAX_CITIES];
    float matrizDuracao[MAX_CITIES][MAX_CITIES];
    float matrizEmissaoCO2[MAX_CITIES][MAX_CITIES];
    char matrizTransporteCusto[MAX_CITIES][MAX_CITIES][20];   // Meio de transporte para menor custo
    char matrizTransporteDuracao[MAX_CITIES][MAX_CITIES][20]; // Meio de transporte para menor duração
    char matrizTransporteEmissao[MAX_CITIES][MAX_CITIES][20]; // Meio de transporte para menor emissão de CO₂
} Grafo;

// Funções para inicializar o grafo e adicionar trajeto
void inicializarGrafo(Grafo *g) {
    g->numCidades = 0;
    for (int i = 0; i < MAX_CITIES; i++) {
        for (int j = 0; j < MAX_CITIES; j++) {
            g->matrizCusto[i][j] = INF;
            g->matrizDuracao[i][j] = INF;
            g->matrizEmissaoCO2[i][j] = INF;
        }
    }
}

int encontrarIndiceCidade(Grafo *g, char *cidade) {
    for (int i = 0; i < g->numCidades; i++) {
        if (strcmp(g->cidades[i], cidade) == 0)
            return i;
    }
    strcpy(g->cidades[g->numCidades], cidade);
    return g->numCidades++;
}

void adicionarTrajeto(Grafo *g, Trajeto t) {
    int origem = encontrarIndiceCidade(g, t.origem);
    int destino = encontrarIndiceCidade(g, t.destino);
    
    // Atualiza matriz de custo e meio de transporte correspondente
    if (g->matrizCusto[origem][destino] > t.preco) {
        g->matrizCusto[origem][destino] = t.preco;
        strcpy(g->matrizTransporteCusto[origem][destino], t.meioDeTransporte);
    }
    
    // Atualiza matriz de duração e meio de transporte correspondente
    if (g->matrizDuracao[origem][destino] > t.duracao) {
        g->matrizDuracao[origem][destino] = t.duracao;
        strcpy(g->matrizTransporteDuracao[origem][destino], t.meioDeTransporte);
    }

    // Atualiza matriz de emissão e meio de transporte correspondente
    if (g->matrizEmissaoCO2[origem][destino] > t.emissaoCO2) {
        g->matrizEmissaoCO2[origem][destino] = t.emissaoCO2;
        strcpy(g->matrizTransporteEmissao[origem][destino], t.meioDeTransporte);
    }
}
#include <stdbool.h>

// Função Dijkstra para calcular a menor distância entre duas cidades em uma matriz específica (custo, duração ou emissão)
void dijkstra(int n, int origem, int destino, float matriz[MAX_CITIES][MAX_CITIES], float *distanciaTotal) {
    float dist[MAX_CITIES];
    bool visitado[MAX_CITIES] = {false};

    for (int i = 0; i < n; i++) {
        dist[i] = INF;
    }
    dist[origem] = 0;

    for (int count = 0; count < n - 1; count++) {
        float min = INF;
        int u = -1;

        for (int v = 0; v < n; v++)
            if (!visitado[v] && dist[v] <= min)
                min = dist[v], u = v;

        if (u == -1) break;

        visitado[u] = true;

        for (int v = 0; v < n; v++) {
            if (!visitado[v] && matriz[u][v] != INF && dist[u] + matriz[u][v] < dist[v]) {
                dist[v] = dist[u] + matriz[u][v];
            }
        }
    }

    *distanciaTotal = dist[destino];
}

// Função para gerar a próxima permutação em C
int next_permutation(int *array, int n) {
    int i = n - 2;
    while (i >= 0 && array[i] >= array[i + 1]) i--;
    if (i < 0) return 0; // Não há mais permutações

    int j = n - 1;
    while (array[j] <= array[i]) j--;

    // Troca
    int temp = array[i];
    array[i] = array[j];
    array[j] = temp;

    // Reverte a sequência a partir de i + 1
    for (int a = i + 1, b = n - 1; a < b; a++, b--) {
        temp = array[a];
        array[a] = array[b];
        array[b] = temp;
    }

    return 1;
}

// Função para permutar os destinos intermediários e encontrar a melhor rota
void permutarDestinos(Grafo *g, int *intermediarios, int n, int origem, int destino, 
                      float matriz[MAX_CITIES][MAX_CITIES], float *melhorDistancia, int *melhorCaminho, int *melhorTam) {
    int indices[MAX_PATH];
    for (int i = 0; i < n; i++) indices[i] = intermediarios[i];
    float distanciaTotal;

    do {
        distanciaTotal = 0;
        int cidadeAtual = origem;
        int tempCaminho[MAX_PATH];
        int tempTam = 0;

        for (int i = 0; i < n; i++) {
            float distanciaParcial;
            dijkstra(g->numCidades, cidadeAtual, indices[i], matriz, &distanciaParcial);
            distanciaTotal += distanciaParcial;
            tempCaminho[tempTam++] = cidadeAtual;
            cidadeAtual = indices[i];
        }

        float distanciaFinal;
        dijkstra(g->numCidades, cidadeAtual, destino, matriz, &distanciaFinal);
        distanciaTotal += distanciaFinal;
        tempCaminho[tempTam++] = cidadeAtual;
        tempCaminho[tempTam++] = destino;

        if (distanciaTotal < *melhorDistancia) {
            *melhorDistancia = distanciaTotal;
            *melhorTam = tempTam;
            for (int i = 0; i < tempTam; i++) {
                melhorCaminho[i] = tempCaminho[i];
            }
        }
    } while (next_permutation(indices, n));
}

// Função para exibir as cidades disponíveis com números
void listarCidades(Grafo *g) {
    printf("Cidades disponíveis:\n");
    for (int i = 0; i < g->numCidades; i++) {
        printf("%d: %s\n", i, g->cidades[i]);
    }
}

// Função para carregar dados de um arquivo CSV
void carregarDadosCSV(Grafo *g, const char *nomeArquivo) {
    FILE *file = fopen(nomeArquivo, "r");
    if (file == NULL) {
        printf("Erro ao abrir o arquivo %s\n", nomeArquivo);
        return;
    }

    char linha[256];
    while (fgets(linha, sizeof(linha), file)) {
        Trajeto t;
        sscanf(linha, "%49[^,],%49[^,],%19[^,],%d,%f,%f",
               t.origem, t.destino, t.meioDeTransporte, &t.preco, &t.duracao, &t.emissaoCO2);

        // Ignorar trajetos onde a origem ou destino seja "Origem" ou "Destino"
        if (strcmp(t.origem, "Origem") == 0 || strcmp(t.destino, "Destino") == 0) {
            continue;
        }

        adicionarTrajeto(g, t);
    }

    fclose(file);
}

// Função principal
int main() {
    Grafo g;
    inicializarGrafo(&g);

    // Carregar dados do arquivo CSV
    carregarDadosCSV(&g, "Realistic_Travel_Itinerary_Dataset.csv");

    // Listar as cidades disponíveis para que o usuário possa escolher
    listarCidades(&g);

    int cidadeOrigem, cidadeDestino;
    int numIntermediarios;

    // Entrada do usuário usando números para cidades
    printf("Digite o número da cidade de partida: ");
    scanf("%d", &cidadeOrigem);

    printf("Quantos destinos intermediários? ");
    scanf("%d", &numIntermediarios);

    int intermediariosIndices[numIntermediarios];
    for (int i = 0; i < numIntermediarios; i++) {
        printf("Digite o número do destino intermediário %d: ", i + 1);
        scanf("%d", &intermediariosIndices[i]);
    }

    printf("Digite o número da cidade de destino final: ");
    scanf("%d", &cidadeDestino);

    float melhorCusto = INF, melhorDuracao = INF, melhorEmissao = INF;
    int melhorCaminhoCusto[MAX_PATH], melhorTamCusto;
    int melhorCaminhoDuracao[MAX_PATH], melhorTamDuracao;
    int melhorCaminhoEmissao[MAX_PATH], melhorTamEmissao;

    // Calcular a melhor rota para cada métrica
    permutarDestinos(&g, intermediariosIndices, numIntermediarios, cidadeOrigem, cidadeDestino, g.matrizCusto, &melhorCusto, melhorCaminhoCusto, &melhorTamCusto);
    permutarDestinos(&g, intermediariosIndices, numIntermediarios, cidadeOrigem, cidadeDestino, g.matrizDuracao, &melhorDuracao, melhorCaminhoDuracao, &melhorTamDuracao);
    permutarDestinos(&g, intermediariosIndices, numIntermediarios, cidadeOrigem, cidadeDestino, g.matrizEmissaoCO2, &melhorEmissao, melhorCaminhoEmissao, &melhorTamEmissao);

    // Exibir resultados detalhados para cada métrica
    printf("\n=== Melhor Custo ===\n");
    printf("Trajeto: ");
    for (int i = 0; i < melhorTamCusto - 1; i++) {
        int origemIdx = melhorCaminhoCusto[i];
        int destinoIdx = melhorCaminhoCusto[i + 1];

        float custoParcial = g.matrizCusto[origemIdx][destinoIdx];
        float duracaoParcial = g.matrizDuracao[origemIdx][destinoIdx];
        float emissaoParcial = g.matrizEmissaoCO2[origemIdx][destinoIdx];
        char *meioTransporte = g.matrizTransporteCusto[origemIdx][destinoIdx];

        printf("%s -> %s\n", g.cidades[origemIdx], g.cidades[destinoIdx]);
        printf("  Meio de transporte: %s\n", meioTransporte);
        printf("  Custo parcial: €%.2f\n", custoParcial);
        printf("  Duração parcial: %.2f horas\n", duracaoParcial);
        printf("  Emissão parcial: %.2f kg CO₂\n", emissaoParcial);
    }
    printf("Custo total: €%.2f\n", melhorCusto);

    printf("\n=== Menor Duração ===\n");
    printf("Trajeto: ");
    for (int i = 0; i < melhorTamDuracao - 1; i++) {
        int origemIdx = melhorCaminhoDuracao[i];
        int destinoIdx = melhorCaminhoDuracao[i + 1];

        float custoParcial = g.matrizCusto[origemIdx][destinoIdx];
        float duracaoParcial = g.matrizDuracao[origemIdx][destinoIdx];
        float emissaoParcial = g.matrizEmissaoCO2[origemIdx][destinoIdx];
        char *meioTransporte = g.matrizTransporteDuracao[origemIdx][destinoIdx];

        printf("%s -> %s\n", g.cidades[origemIdx], g.cidades[destinoIdx]);
        printf("  Meio de transporte: %s\n", meioTransporte);
        printf("  Custo parcial: €%.2f\n", custoParcial);
        printf("  Duração parcial: %.2f horas\n", duracaoParcial);
        printf("  Emissão parcial: %.2f kg CO₂\n", emissaoParcial);
    }
    printf("Duração total: %.2f horas\n", melhorDuracao);

    printf("\n=== Menor Emissão de CO₂ ===\n");
    printf("Trajeto: ");
    for (int i = 0; i < melhorTamEmissao - 1; i++) {
        int origemIdx = melhorCaminhoEmissao[i];
        int destinoIdx = melhorCaminhoEmissao[i + 1];

        float custoParcial = g.matrizCusto[origemIdx][destinoIdx];
        float duracaoParcial = g.matrizDuracao[origemIdx][destinoIdx];
        float emissaoParcial = g.matrizEmissaoCO2[origemIdx][destinoIdx];
        char *meioTransporte = g.matrizTransporteEmissao[origemIdx][destinoIdx];

        printf("%s -> %s\n", g.cidades[origemIdx], g.cidades[destinoIdx]);
        printf("  Meio de transporte: %s\n", meioTransporte);
        printf("  Custo parcial: €%.2f\n", custoParcial);
        printf("  Duração parcial: %.2f horas\n", duracaoParcial);
        printf("  Emissão parcial: %.2f kg CO₂\n", emissaoParcial);
    }
    printf("Emissão total de CO₂: %.2f kg\n", melhorEmissao);

    return 0;
}

