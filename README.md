# Flamengo 2026 — Análise de Temporada via Contagem de Inversões

**Disciplina:** Projeto de Algoritmos — Dividir e Conquistar  
**Turma:** G56 · PA-26.1  
**Autor:** Arthur Leite

---

## Tema

Análise da temporada 2026 do Flamengo no **Brasileirão Série A** e na **Copa Libertadores** usando **Contagem de Inversões** como problema central de Dividir e Conquistar.

---

## Descrição do Problema

Cada jogo do Flamengo em 2026 recebe uma **pontuação de dificuldade** calculada a partir de:

- Força do adversário (escala 1–10 baseada em desempenho real em 2026)
- Competição (Libertadores pesa 1.5×, Brasileirão 1.0×)
- Mando de campo (fora = 1.3×, casa = 1.0×)
- Fase da competição (mata-mata > fase de grupos > rodada)
- Resultado (derrota adiciona pontuação, vitória reduz)
- Saldo de gols
- xGA (Expected Goals Against), quando disponível

A sequência cronológica dos jogos forma um **vetor de dificuldades**:

```
[3.5, 8.2, 12.7, 5.1, 16.1, 4.3, 9.8, ...]
```

A **Contagem de Inversões** responde: *quantas vezes um jogo mais difícil aparece antes de um jogo mais fácil nessa sequência?*

Um número alto de inversões indica um calendário **irregular e desequilibrado** — picos de dificuldade intercalados com jogos tranquilos, sem uma progressão ordenada.

---

## Dados Reais — Temporada 2026

Os dados foram coletados de **ESPN**, **Wikipedia** e **FBref** e refletem a situação real até **01/06/2026**:

### Brasileirão Série A 2026

| Posição | Pontos | Jogos | V | E | D | GP | GC | SG |
|---------|--------|-------|---|---|---|----|----|-----|
| **2º** | **34** | **17** | **10** | **4** | **3** | **31** | **16** | **+15** |

- Líder: Palmeiras (41 pts em 18 jogos)
- Artilheiro: **Pedro** (10 gols)
- Garçom: **Samuel Lino** (6 assistências)
- Rodada 18 (31/05): Flamengo **3×0** Coritiba *(ainda fora da tabela acima)*

### Copa Libertadores 2026

| Grupo A — Posição | Pontos | J | V | E | D | GP | GC | SG |
|-------------------|--------|---|---|---|---|----|----|-----|
| **1º** | **16** | **6** | **5** | **1** | **0** | **14** | **2** | **+12** |

- Fase atual: **Oitavas de Final**
- Campanha invicta na fase de grupos
- Adversários: Estudiantes (ARG), Independiente Medellín (COL), Cusco (PER)

---

## Por que Contagem de Inversões é Dividir e Conquistar?

A abordagem ingênua compara todos os pares (i, j) com i < j: **O(n²)**.

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
├── requirements.txt
├── data/
│   ├── raw/                              # Saída do scraping (gerado)
│   ├── processed/                        # Jogos enriquecidos com dificuldade (gerado)
│   └── fallback/
│       ├── flamengo_2026_fallback.csv    # 24 jogos reais (6 Lib + 18 BRA)
│       ├── players.json                  # Elenco 2026 real (ESPN)
│       └── standings.json               # Classificação real (01/06/2026)
├── scripts/
│   ├── scrape_fbref.py                   # Scraping principal via FBref
│   ├── scrape_espn.py                   # Scraping alternativo via API ESPN
│   ├── process_matches.py               # Calcula dificuldade de cada jogo
│   └── generate_analysis.py            # Gera JSON final para o frontend
├── src/
│   ├── algorithms/
│   │   └── inversion_count.py           # Algoritmo de Contagem de Inversões
│   ├── analysis/
│   │   ├── difficulty_model.py          # Modelo de pontuação de dificuldade
│   │   └── title_probability.py        # Estimativa heurística de título
│   └── api/
│       └── analysis.json               # JSON gerado (fonte do frontend)
├── frontend/
│   ├── index.html
│   ├── package.json                     # React + Vite + Recharts
│   ├── public/
│   │   └── analysis.json               # Cópia do JSON para o servidor Vite
│   └── src/
│       ├── App.jsx
│       ├── components/                  # 9 componentes React
│       ├── hooks/useAnalysis.js
│       └── utils/formatters.js
└── docs/
    ├── explicacao_algoritmo.md
    ├── metodologia.md
    └── fontes.md
```

---

## Como Rodar

### Pré-requisitos

- Python 3.10+
- Node.js 18+

### 1. Instalar dependências Python

```bash
pip install -r requirements.txt
```

### 2. Coletar dados (opcional)

Tenta FBref primeiro. Se falhar, tenta a API ESPN:

```bash
python scripts/scrape_fbref.py
python scripts/scrape_espn.py   # alternativa ESPN
```

> Se ambos falharem, o sistema usa `data/fallback/flamengo_2026_fallback.csv` automaticamente.

### 3. Processar os jogos

```bash
python scripts/process_matches.py
```

### 4. Gerar a análise completa

```bash
python scripts/generate_analysis.py
```

Gera `src/api/analysis.json` e `frontend/public/analysis.json`.

### 5. Rodar o frontend

```bash
cd frontend
npm install
npm run dev
```

Acesse: **http://localhost:5173**

---

### Atalho — tudo de uma vez

```bash
pip install -r requirements.txt
python scripts/scrape_fbref.py
python scripts/process_matches.py
python scripts/generate_analysis.py
cd frontend && npm install && npm run dev
```

---

## Fontes de Dados

| Fonte | Uso | URL |
|-------|-----|-----|
| FBref | Scraping principal de partidas | https://fbref.com/en/squads/639950ae/2026/ |
| ESPN API | Scraping alternativo (JSON) | https://site.api.espn.com/apis/site/v2/sports/soccer/ |
| ESPN Elenco | Elenco real 2026 | https://www.espn.com.br/futebol/time/elenco/_/id/819/bra.flamengo |
| Wikipedia | Tabelas de classificação e resultados | https://pt.wikipedia.org/wiki/Campeonato_Brasileiro_de_Futebol_de_2026 |
| Fallback local | CSV com 24 jogos reais (backup) | `data/fallback/flamengo_2026_fallback.csv` |

---

## Explicação das Funções Principais

### `sort_and_count(arr, temp, left, right)`
**`src/algorithms/inversion_count.py`**

Divide o vetor ao meio recursivamente e acumula inversões da esquerda, da direita e as cruzadas.

### `merge_and_count(arr, temp, left, mid, right)`
**`src/algorithms/inversion_count.py`**

Merge das duas metades ordenadas com contagem de inversões cruzadas. Quando `arr[i] > arr[j]`, contabiliza `(mid - i + 1)` inversões de uma vez.

### `count_inversions(sequence)`
**`src/algorithms/inversion_count.py`**

Interface pública. Retorna `InversionResult` com:
- `inversions` — total de inversões
- `max_inversions` — máximo possível = n(n-1)/2
- `percentage` — `inversions / max_inversions × 100`
- `sorted_sequence` — sequência ordenada

### `calculate_difficulty(match)`
**`src/analysis/difficulty_model.py`**

```
base       = opponent_strength × competition_weight × venue_weight × phase_weight
difficulty = clamp(base + result_adj + goal_diff_adj + xga_adj, 1.0, 20.0)
```

### `estimate_brasileirao(matches, standings)` / `estimate_libertadores(matches, standings)`
**`src/analysis/title_probability.py`**

Estimativas heurísticas que incorporam a **classificação real** de `data/fallback/standings.json` (posição, pontos, gap para o líder, forma recente) quando disponível.

---

## Análise de Complexidade

| Abordagem      | Recorrência              | Complexidade   |
|----------------|--------------------------|----------------|
| Força bruta    | —                        | **O(n²)**      |
| Sort-and-Count | T(n) = 2T(n/2) + O(n)   | **O(n log n)** |

Pelo Teorema Mestre: a=2, b=2, f(n)=O(n) → caso 2 → **O(n log n)**.

---

## Resultados com Dados Reais (01/06/2026)

| Competição | Jogos | Inversões | Desordem |
|------------|-------|-----------|----------|
| Brasileirão | 18 | 49 / 153 | **32%** |
| Copa Libertadores | 6 | 7 / 15 | **47%** |
| Temporada completa | 24 | 124 / 276 | **45%** |

**Probabilidade heurística de título:**
- Brasileirão: **80.2%** — 2º lugar, 34 pts, 7 pts atrás do Palmeiras, forma W-D-L-W-L
- Copa Libertadores: **91.4%** — 1º no Grupo A, invicto, SG+12, na fase de oitavas

> Aviso: são estimativas baseadas em desempenho atual, **não previsões estatísticas**.

---

## Estimativa Heurística de Título

**Brasileirão:**
```
raw = aproveitamento×0.30 + forma×0.15 + saldo×0.10
    + gap_lider×0.20 + posição×0.10 + fator_histórico×0.15
prob = clamp(raw × 100 × 1.15, 0, 95)
```

**Libertadores:**
```
raw = aproveitamento×0.35 + fase_alcançada×0.30
    + desempenho_fora×0.20 + forma×0.15
prob = clamp(raw × 100 × 1.10, 0, 95)
```

> Aviso: métrica de desempenho, não odds de apostas ou previsão real.

---

## Limitações

1. **Dados parciais** — temporada 2026 em andamento; dados refletem até 01/06/2026.
2. **Scraping pode falhar** — FBref e ESPN podem bloquear requisições; fallback local é acionado automaticamente.
3. **Probabilidade heurística** — fórmula simplificada, não é modelo estatístico real.
4. **Datas de jogos** — algumas datas no fallback são aproximadas; o pipeline ordena cronologicamente antes de calcular.
5. **xG/xGA** — disponíveis apenas nos jogos com dados completos no FBref.

---

## Referências

- Cormen, T.H. et al. *Introduction to Algorithms*, 3rd ed. MIT Press. (Seção 2.3)
- Kleinberg, J.; Tardos, E. *Algorithm Design*. Pearson Education, 2005. (Cap. 5)
- ESPN Brasil — https://www.espn.com.br/futebol/
- FBref — https://fbref.com/en/squads/639950ae/2026/
- Wikipedia — Campeonato Brasileiro de Futebol de 2026 - Série A
- Wikipedia — Copa Libertadores da América de 2026
