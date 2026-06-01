# Contagem de Inversões — Explicação do Algoritmo

## O que é uma Inversão?

Dado um vetor `A` de `n` elementos, uma **inversão** é um par de índices `(i, j)` tal que:

```
i < j  e  A[i] > A[j]
```

Em outras palavras, um elemento maior aparece antes de um elemento menor na sequência. O número total de inversões mede o **grau de desordem** de um vetor.

### Exemplos

| Vetor               | Inversões | Pares                    |
|---------------------|-----------|--------------------------|
| `[1, 2, 3, 4]`      | 0         | Nenhum                   |
| `[4, 3, 2, 1]`      | 6         | (4,3),(4,2),(4,1),(3,2),(3,1),(2,1) |
| `[2, 3, 8, 6, 1]`   | 5         | (2,1),(3,1),(8,6),(8,1),(6,1) |

---

## Por que isso é Dividir e Conquistar?

O problema de **contar inversões** é resolvido com a mesma estrutura recursiva do **Merge Sort**, tornando-o um exemplo clássico de **Dividir e Conquistar**.

### Abordagem Ingênua — O(n²)

```python
def brute_force_inversions(arr):
    n = len(arr)
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                count += 1
    return count
```

Para cada elemento, verificamos todos os seguintes. Dois laços aninhados → O(n²).

### Abordagem Eficiente — O(n log n)

Usando **Dividir e Conquistar** (`sort_and_count` + `merge_and_count`):

```
sort_and_count(arr, left, right):
    if left >= right:
        return 0                             # base: um elemento, zero inversões

    mid = (left + right) / 2
    left_inv  = sort_and_count(arr, left, mid)        # DIVIDIR (esquerda)
    right_inv = sort_and_count(arr, mid+1, right)     # DIVIDIR (direita)
    cross_inv = merge_and_count(arr, left, mid, right) # CONQUISTAR (merge)

    return left_inv + right_inv + cross_inv
```

#### Onde as inversões cruzadas são contadas

Durante o merge de dois subvetores já ordenados `L` e `R`:

```
Se L[i] > R[j]:
    # todos os elementos restantes em L também são > R[j]
    inversões += (mid - i + 1)
```

Isso aproveita a propriedade de que `L` já está ordenado para contar múltiplas inversões de uma vez.

---

## Análise de Complexidade

| Etapa         | Recorrência              | Complexidade |
|---------------|--------------------------|--------------|
| Divisão       | T(n) = 2·T(n/2) + O(n)  | —            |
| Merge         | O(n) por nível           | —            |
| Total (Mestre)| a=2, b=2, f(n)=n → caso 2 | **O(n log n)** |

A recorrência `T(n) = 2T(n/2) + O(n)` se resolve pelo **Teorema Mestre** como `O(n log n)`.

---

## Aplicação no Projeto

Neste projeto, o vetor de entrada não é de inteiros aleatórios — é a **sequência de dificuldades dos jogos do Flamengo em 2026**:

```
[dificuldade(jogo_1), dificuldade(jogo_2), ..., dificuldade(jogo_n)]
```

O total de inversões responde à pergunta:

> *Quantas vezes o Flamengo enfrentou um jogo mais difícil depois de um jogo mais fácil, considerando a ordem cronológica?*

Uma sequência com muitas inversões indica um calendário **irregular e desequilibrado** — alternando jogos muito difíceis com jogos mais tranquilos sem uma progressão ordenada de dificuldade.

A **porcentagem de inversões** é calculada como:

```
max_inversions = n * (n - 1) / 2
inversion_percentage = (inversions / max_inversions) * 100
```

- **0%** → sequência perfeitamente ordenada (do mais fácil ao mais difícil)
- **100%** → sequência totalmente invertida (do mais difícil ao mais fácil)
- **~50%** → sequência aleatória/sem padrão claro

---

## Funções Principais

### `sort_and_count(arr, temp, left, right)`
Divide o vetor recursivamente ao meio e soma as inversões de cada metade mais as cruzadas.

### `merge_and_count(arr, temp, left, mid, right)`
Realiza o merge das duas metades ordenadas contando as inversões cruzadas durante o processo.

### `count_inversions(sequence)`
Interface pública: recebe a sequência de dificuldades e retorna `(sorted, inversions, max_inv, percentage)`.
