import pandas as pd
import random
import time
from copy import deepcopy
import matplotlib.pyplot as plt

df = pd.read_csv("SAP-4000.csv")
df.columns = df.columns.str.strip()
coluna = "Exam_Score"    
if coluna not in df.columns:
    raise ValueError(f"Coluna '{coluna}' não encontrada.")
dados = df[coluna].dropna().astype(int).tolist()

# Subconjuntos (1k, 4k e 10k)
dados_1k  = dados[:1000]
dados_4k  = dados[:4000]          
dados_10k = (dados * 3)[:10000]
random.shuffle(dados_10k)

def preparar_casos(vetor):
    return {
        "melhor_caso": sorted(vetor),
        "caso_medio" : vetor[:],
        "pior_caso"  : sorted(vetor, reverse=True)
    }

# Algoritmos com contadores 

def bubble_sort(arr):
    a = arr[:]
    n = len(a)
    comp = troc = 0
    for i in range(n - 1):
        for j in range(n - 1 - i):
            comp += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                troc += 1
    return a, comp, troc

def bubble_sort_improved(arr):
    a = arr[:]
    n = len(a)
    comp = troc = 0
    for i in range(n - 1):
        trocou = False
        for j in range(n - 1 - i):
            comp += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                troc += 1
                trocou = True
        if not trocou:
            break
    return a, comp, troc

def selection_sort(arr):
    a = arr[:]
    n = len(a)
    comp = troc = 0
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            comp += 1
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            troc += 1
    return a, comp, troc

def insertion_sort(arr): 
    a = arr[:]
    comp = troc = 0
    for i in range(1, len(a)):
        chave = a[i]
        j = i - 1
        while j >= 0 and a[j] > chave:
            comp += 1
            a[j + 1] = a[j]
            troc += 1
            j -= 1
        comp += 1
        a[j + 1] = chave
        troc += 1
    return a, comp, troc

def merge_sort(arr):
    comp = troc = 0
    def merge(esq, dir):
        nonlocal comp, troc
        res = []
        i = j = 0
        while i < len(esq) and j < len(dir):
            comp += 1
            if esq[i] <= dir[j]:
                res.append(esq[i]); i += 1
            else:
                res.append(dir[j]); j += 1
                troc += 1
        res.extend(esq[i:]); res.extend(dir[j:])
        return res
    def ms(v):
        if len(v) <= 1:
            return v
        meio = len(v) // 2
        return merge(ms(v[:meio]), ms(v[meio:]))
    result = ms(arr[:])
    return result, comp, troc

def quick_sort(arr):
    comp = troc = 0
    a = arr[:]
    def qs(low, high):
        nonlocal comp, troc
        if low < high:
            p = part(low, high)
            qs(low, p - 1)
            qs(p + 1, high)
    def part(low, high):
        nonlocal comp, troc
        pivot_idx = random.randint(low, high)
        a[high], a[pivot_idx] = a[pivot_idx], a[high]
        pivot = a[high]
        i = low - 1
        for j in range(low, high):
            comp += 1
            if a[j] <= pivot:
                i += 1
                a[i], a[j] = a[j], a[i]
                troc += 1
        a[i + 1], a[high] = a[high], a[i + 1]
        troc += 1
        return i + 1
    qs(0, len(a) - 1)
    return a, comp, troc

def heap_sort(arr):
    a = arr[:]
    comp = troc = 0
    n = len(a)
    def heapify(i, heap_size):
        nonlocal comp, troc
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2
        if l < heap_size and a[l] > a[largest]:
            comp += 1
            largest = l
        if r < heap_size and a[r] > a[largest]:
            comp += 1
            largest = r
        if largest != i:
            a[i], a[largest] = a[largest], a[i]
            troc += 1
            heapify(largest, heap_size)
  
    for i in range(n // 2 - 1, -1, -1):
        heapify(i, n)
  
    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]
        troc += 1
        heapify(0, i)
    return a, comp, troc

# Função de teste 
def testar(alg_nome, funcao, vetor, tam, caso):
    inicio = time.perf_counter()
    _, comp, troc = funcao(vetor)
    dur = time.perf_counter() - inicio
    return {
        "Algoritmo"  : alg_nome,
        "Tamanho"    : tam,
        "Caso"       : caso,
        "Tempo (s)"  : round(dur, 5),
        "Comparações": comp,
        "Trocas"     : troc
    }

# Executa e coleta 
algoritmos = [
    ("Bubble Sort"         , bubble_sort),
    ("Improved Bubble Sort", bubble_sort_improved),
    ("Selection Sort"      , selection_sort),
    ("Merge Sort"          , merge_sort),
    ("Quick Sort"          , quick_sort),
    ("Heap Sort"           , heap_sort),
]

resultados = []

for tam, casos in [(1000, preparar_casos(dados_1k)),
                   (10000, preparar_casos(dados_10k))]:   # adicione (100000, ...) se desejar
    for caso_nome, vetor in casos.items():
        for alg_nome, alg_func in algoritmos:
            resultados.append(testar(alg_nome, alg_func, vetor, tam, caso_nome))

df_result = pd.DataFrame(resultados)
print("\n===== RESULTADOS =====")
print(df_result)



# Gráfico: Tempo de execução vs Tamanho da entrada
plt.figure(figsize=(10, 6))
for alg in df_result['Algoritmo'].unique():
    sub = df_result[(df_result['Algoritmo'] == alg) & (df_result['Caso'] == 'caso_medio')]
    plt.plot(sub['Tamanho'], sub['Tempo (s)'], marker='o', label=alg)
plt.xlabel("Tamanho da entrada (n)")
plt.ylabel("Tempo de execução (s)")
plt.title("Tempo de Execução vs Tamanho da Entrada (caso médio)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Gráfico: Comparações vs Tamanho da entrada
plt.figure(figsize=(10, 6))
for alg in df_result['Algoritmo'].unique():
    sub = df_result[(df_result['Algoritmo'] == alg) & (df_result['Caso'] == 'caso_medio')]
    plt.plot(sub['Tamanho'], sub['Comparações'], marker='o', label=alg)
plt.xlabel("Tamanho da entrada (n)")
plt.ylabel("Número de comparações")
plt.title("Comparações vs Tamanho da Entrada (caso médio)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Gráfico: Trocas vs Tamanho da entrada
plt.figure(figsize=(10, 6))
for alg in df_result['Algoritmo'].unique():
    sub = df_result[(df_result['Algoritmo'] == alg) & (df_result['Caso'] == 'caso_medio')]
    plt.plot(sub['Tamanho'], sub['Trocas'], marker='o', label=alg)
plt.xlabel("Tamanho da entrada (n)")
plt.ylabel("Número de trocas")
plt.title("Trocas vs Tamanho da Entrada (caso médio)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


