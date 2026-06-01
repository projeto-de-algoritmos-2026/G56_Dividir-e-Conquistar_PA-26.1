# Metodologia — Pontuação de Dificuldade dos Jogos

## Visão Geral

Cada jogo do Flamengo em 2026 recebe uma **pontuação de dificuldade** composta por múltiplos fatores. O objetivo é transformar a sequência cronológica de jogos em um vetor numérico sobre o qual a Contagem de Inversões possa operar de forma significativa.

---

## Componentes da Pontuação

### 1. Força do Adversário (`opponent_strength`)

Escala de 1 a 10, baseada no histórico e desempenho recente do clube adversário:

| Tier | Força | Exemplos                                          |
|------|-------|---------------------------------------------------|
| S    | 8–10  | Palmeiras, Atlético-MG, River Plate, Boca Juniors |
| A    | 6–8   | Botafogo, São Paulo, Fluminense, Peñarol          |
| B    | 4–6   | Santos, Cruzeiro, Inter, Grêmio                   |
| C    | 1–4   | Vasco, Cuiabá, Fortaleza, Bolívar                 |

### 2. Peso da Competição (`competition_weight`)

| Competição       | Multiplicador |
|------------------|---------------|
| Copa Libertadores | 1.5×          |
| Brasileirão       | 1.0×          |

### 3. Mando de Campo (`venue_weight`)

| Local   | Multiplicador |
|---------|---------------|
| Fora    | 1.3×          |
| Neutro  | 1.1×          |
| Casa    | 1.0×          |

### 4. Fase da Competição (`phase_weight`)

| Fase                 | Multiplicador |
|----------------------|---------------|
| Final                | 2.0×          |
| Semifinal            | 1.8×          |
| Quartas              | 1.6×          |
| Oitavas              | 1.4×          |
| Fase de Grupos       | 1.2×          |
| Rodada (Brasileirão) | 1.0×          |

### 5. Ajuste de Resultado (`result_adjustment`)

| Resultado | Ajuste   |
|-----------|----------|
| Derrota   | +2.5     |
| Empate    | +1.0     |
| Vitória   | 0.0      |

### 6. Saldo de Gols (`goal_diff_adjustment`)

```
goal_diff_adjustment = abs(gf - ga) * fator
```

- Derrota: `+0.5 × |saldo|` (derrota por goleada aumenta a dificuldade)
- Vitória: `−0.3 × |saldo|` (goleada de vitória reduz a dificuldade percebida)
- Empate: `0`

### 7. Pressão xGA (`xga_adjustment`)

Quando disponível:
```
xga_adjustment = max(0, xga - 1.0) * 0.5
```
Jogos onde o adversário criou muitas chances (xGA alto) recebem bônus de dificuldade.

---

## Fórmula Final

```
base_difficulty = opponent_strength × competition_weight × venue_weight × phase_weight

raw_score = base_difficulty + result_adjustment + goal_diff_adjustment + xga_adjustment

difficulty = max(1.0, min(20.0, raw_score))
```

A normalização para o intervalo [1, 20] garante comparabilidade entre jogos de diferentes competições.

---

## Estimativa Heurística de Título

### Brasileirão

```
perf_factor    = aproveitamento (pontos / pontos_possíveis)
position_factor = (21 - posição) / 20        # 1º lugar = 1.0, 20º = 0.05
form_factor    = pontos_últimos_5_jogos / 15  # máximo 5 vitórias = 15 pontos
gd_factor      = min(1.0, max(0, saldo_gols / 20 + 0.5))

raw_prob = perf_factor*0.4 + position_factor*0.3 + form_factor*0.2 + gd_factor*0.1
title_prob = min(95, raw_prob * 100 * 1.15)  # fator Flamengo histórico
```

### Copa Libertadores

```
perf_factor    = aproveitamento na competição
stage_factor   = fase_alcançada / 7  # 7 = campeão
home_factor    = aproveitamento em casa
away_factor    = aproveitamento fora

raw_prob = perf_factor*0.4 + stage_factor*0.3 + home_factor*0.15 + away_factor*0.15
title_prob = min(95, raw_prob * 100 * 1.1)
```

> **Importante**: Estas estimativas são **heurísticas baseadas em desempenho atual**, não previsões estatísticas ou probabilidades reais. São exibidas apenas como indicadores de tendência.

---

## Interpretação das Inversões

| Faixa de Inversões | Interpretação                                        |
|--------------------|------------------------------------------------------|
| 0–20%              | Calendário bem distribuído, dificuldade crescente    |
| 20–40%             | Leve irregularidade no calendário                    |
| 40–60%             | Calendário desequilibrado, sem padrão claro          |
| 60–80%             | Calendário muito pesado e irregular                  |
| 80–100%            | Calendário decrescente em dificuldade (ou invertido) |
