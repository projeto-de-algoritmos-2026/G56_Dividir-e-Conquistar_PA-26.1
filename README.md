# Flamengo 2026 — Análise de Temporada via Contagem de Inversões

**Disciplina:** Projeto de Algoritmos — Dividir e Conquistar  
**Turma:** G56 · PA-26.1  
**Autor:** Arthur Leite  

---

## Tema

Análise da temporada 2026 do Flamengo no **Brasileirão Série A** e na **Copa Libertadores** usando **Contagem de Inversões** como problema central de Dividir e Conquistar.

---

## Descrição do Problema

Cada jogo do Flamengo em 2026 recebe uma **pontuação de dificuldade** baseada em:

- Força do adversário (escala 1–10)
- Competição (Libertadores pesa 1.5×, Brasileirão 1.0×)
- Mando de campo (fora = 1.3×, casa = 1.0×)
- Fase da competição (mata-mata > fase de grupos > rodada)
- Resultado (derrota adiciona pontuação, vitória reduz)
- Saldo de gols
- xGA (Expected Goals Against), se disponível

A sequência cronológica dos jogos se torna um **vetor de dificuldades**:

```
[12.3, 4.1, 18.7, 2.8, 15.0, 1.5, 8.2, ...]
```

A **Contagem de Inversões** responde: *quantas vezes um jogo mais difícil aparece antes de um jogo mais fácil nessa sequência?*

Um número alto de inversões indica um calendário **irregular e desequilibrado** — picos de dificuldade espalhados sem progressão ordenada.

---

## Por que Contagem de Inversões é Dividir e Conquistar?

A abordagem ingênua compara todos os pares (i, j) com i < j: O(**n²**).

A abordagem eficiente usa a mesma estrutura recursiva do Merge Sort:

```
sort_and_count(arr, left, right):
  mid = (left + right) / 2
  left_inv  = sort_and_count(arr, left, mid)         # DIVIDIR
  right_inv = sort_and_count(arr, mid+1, right)      # DIVIDIR
  cross_inv = merge_and_count(arr, left, mid, right) # CONQUISTAR
  return left_inv + right_inv + cross_inv
```

Durante o merge, quando `arr[i] > arr[j]`, todos os `(mid - i + 1)` elementos restantes à esquerda também formam inversão com `arr[j]` — contagem em bloco em vez de um a um.

**Complexidade: O(n log n)** pela recorrência T(n) = 2T(n/2) + O(n) (Teorema Mestre, caso 2).

---

## Estrutura do Projeto

```
G56_Dividir-e-Conquistar_PA-26.1/
├── README.md
├── requirements.txt                    # Dependências Python
├── data/
│   ├── raw/                            # Dados brutos do scraping (gerado)
│   ├── processed/                      # Jogos processados com dificuldade (gerado)
│   └── fallback/
│       ├── flamengo_2026_fallback.csv  # Dados manuais de segurança
│       └── players.json               # Elenco configurável
├── scripts/
│   ├── scrape_fbref.py                 # Web scraping do FBref
│   ├── process_matches.py             # Enriquece jogos com dificuldade
│   └── generate_analysis.py           # Gera JSON final para o frontend
├── src/
│   ├── algorithms/
│   │   └── inversion_count.py          # Algoritmo de Contagem de Inversões
│   ├── analysis/
│   │   ├── difficulty_model.py         # Modelo de pontuação de dificuldade
│   │   └── title_probability.py       # Estimativa heurística de título
│   └── api/
│       └── analysis.json              # JSON gerado (fonte dos dados do frontend)
├── frontend/
│   ├── index.html
│   ├── package.json                   # React + Vite + Recharts
│   ├── vite.config.js
│   ├── public/
│   │   └── analysis.json             # Cópia do JSON para o servidor Vite
│   └── src/
│       ├── App.jsx                   # Componente principal
│       ├── App.css                   # Estilos globais (tema Flamengo)
│       ├── components/               # Componentes React
│       ├── hooks/useAnalysis.js      # Carregamento de dados
│       └── utils/formatters.js      # Formatadores
└── docs/
    ├── explicacao_algoritmo.md
    ├── metodologia.md
    └── fontes.md
```

---

## Como Rodar

### Pré-requisitos

- Python 3.10+
- Node.js 18+ (para o frontend)

### 1. Instalar dependências Python

```bash
pip install -r requirements.txt
```

### 2. Coletar dados (opcional — usa fallback automático se falhar)

```bash
python scripts/scrape_fbref.py
```

> O FBref pode bloquear requisições. O script detecta falhas e usa `data/fallback/flamengo_2026_fallback.csv` automaticamente.

### 3. Processar os jogos

```bash
python scripts/process_matches.py
```

### 4. Gerar a análise completa

```bash
python scripts/generate_analysis.py
```

Isso gera `src/api/analysis.json` e `frontend/public/analysis.json`.

### 5. Rodar o frontend

```bash
cd frontend
npm install
npm run dev
```

Acesse: **http://localhost:5173**

---

### Atalho — rodar tudo de uma vez

```bash
pip install -r requirements.txt
python scripts/scrape_fbref.py
python scripts/process_matches.py
python scripts/generate_analysis.py
cd frontend && npm install && npm run dev
```

---

## Explicação das Funções Principais

### `sort_and_count(arr, temp, left, right)`
**`src/algorithms/inversion_count.py`**

Função recursiva central. Divide o vetor ao meio e acumula:
- inversões na metade esquerda (recursão)
- inversões na metade direita (recursão)
- inversões cruzadas entre as duas metades (merge)

### `merge_and_count(arr, temp, left, mid, right)`
**`src/algorithms/inversion_count.py`**

Faz o merge de `arr[left..mid]` e `arr[mid+1..right]` (ambos ordenados) contando as inversões cruzadas. Quando `arr[i] > arr[j]`, contabiliza `(mid - i + 1)` inversões de uma vez.

### `count_inversions(sequence)`
**`src/algorithms/inversion_count.py`**

Interface pública. Recebe a sequência de dificuldades e retorna `InversionResult` com:
- `inversions` — total de inversões encontradas
- `max_inversions` — máximo possível = n(n-1)/2
- `percentage` — `inversions / max_inversions × 100`
- `sorted_sequence` — sequência ordenada resultante

### `calculate_difficulty(match)`
**`src/analysis/difficulty_model.py`**

Calcula a pontuação de dificuldade (escala 1–20) de um jogo:

```
base  = opponent_strength × competition_weight × venue_weight × phase_weight
score = base + result_adj + goal_diff_adj + xga_adj
difficulty = clamp(score, 1.0, 20.0)
```

### `estimate_brasileirao(matches)` / `estimate_libertadores(matches)`
**`src/analysis/title_probability.py`**

Estimativas heurísticas baseadas em aproveitamento, forma recente, saldo de gols e fase alcançada na competição.

---

## Análise de Complexidade

| Abordagem      | Recorrência              | Complexidade   |
|----------------|--------------------------|----------------|
| Força bruta    | —                        | **O(n²)**      |
| Sort-and-Count | T(n) = 2T(n/2) + O(n)   | **O(n log n)** |

A recorrência T(n) = 2T(n/2) + O(n) é resolvida pelo Teorema Mestre:
- a=2, b=2, f(n)=O(n) → f(n) = Θ(n^log₂2) = Θ(n) → **Caso 2** → T(n) = **O(n log n)**

---

## Métricas de Inversão

```
max_inversions     = n × (n - 1) / 2
inversion_percentage = inversions / max_inversions × 100
```

| Faixa     | Interpretação                             |
|-----------|-------------------------------------------|
| 0–20%     | Calendário ordenado (fácil → difícil)     |
| 20–40%    | Leve irregularidade                       |
| 40–60%    | Calendário desequilibrado                 |
| 60–80%    | Muito irregular e pesado                  |
| 80–100%   | Sequência decrescente em dificuldade      |

---

## Estimativa Heurística de Título

> **Aviso:** Os percentuais exibidos no dashboard são **estimativas heurísticas baseadas em desempenho atual**, não previsões estatísticas nem odds de apostas.

**Brasileirão:**
```
raw = aproveitamento×0.40 + forma_recente×0.20 + saldo_gols×0.15 + fator_histórico×0.25
prob = clamp(raw × 100 × 1.15, 0, 95)
```

**Libertadores:**
```
raw = aproveitamento×0.35 + fase_alcançada×0.30 + desempenho_fora×0.20 + forma×0.15
prob = clamp(raw × 100 × 1.10, 0, 95)
```

---

## Limitações

1. **Dados parciais** — a temporada 2026 ainda está em andamento; o fallback contém dados até junho de 2026.
2. **Scraping pode falhar** — o FBref pode bloquear requisições ou alterar o HTML; o sistema usa `data/fallback/` automaticamente.
3. **Probabilidade de título é heurística** — não é previsão real, apenas indicador de tendência baseado em desempenho atual.
4. **Dados de jogadores** — entradas com `"status": "a confirmar"` em `data/fallback/players.json` não foram verificadas em fonte oficial.
5. **Força dos adversários** — a tabela em `src/analysis/difficulty_model.py` é estimativa qualitativa e pode ser ajustada manualmente.

---

## Fonte dos Dados

| Fonte                     | URL                                                                   |
|---------------------------|-----------------------------------------------------------------------|
| FBref — Todas competições | https://fbref.com/en/squads/639950ae/2026/matchlogs/all_comps/schedule/ |
| FBref — Brasileirão       | https://fbref.com/en/squads/639950ae/2026/matchlogs/c24/schedule/     |
| FBref — Libertadores      | https://fbref.com/en/squads/639950ae/2026/matchlogs/c14/schedule/     |

---

## Referências

- Cormen, T.H. et al. *Introduction to Algorithms*, 3rd ed. MIT Press. (Merge Sort e análise de inversões — Seção 2.3)
- Kleinberg, J.; Tardos, E. *Algorithm Design*. Pearson Education, 2005. (Capítulo 5 — Divide and Conquer)
- FBref.com — Estatísticas de futebol (dados reais via scraping)
