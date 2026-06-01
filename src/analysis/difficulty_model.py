"""
Modelo de dificuldade dos jogos do Flamengo 2026.

Cada jogo recebe uma pontuação de dificuldade composta por:
- Força do adversário
- Peso da competição
- Mando de campo
- Fase da competição
- Ajuste pelo resultado
- Ajuste pelo saldo de gols
- Pressão de Expected Goals Against (xGA)
"""

from __future__ import annotations

OPPONENT_STRENGTH: dict[str, float] = {
    # Tier S — elite
    "Palmeiras": 9.2,
    "Atletico MG": 8.5,
    "Atlético-MG": 8.5,
    "Atletico Mineiro": 8.5,
    "River Plate": 8.8,
    "Boca Juniors": 8.0,
    "Fluminense": 8.0,
    "Botafogo": 8.2,
    "São Paulo": 7.8,
    "Sao Paulo": 7.8,
    # Tier A
    "Internacional": 7.3,
    "Grêmio": 7.2,
    "Gremio": 7.2,
    "Peñarol": 7.4,
    "Penarol": 7.4,
    "Talleres": 7.0,
    "Racing": 7.2,
    "Nacional": 6.8,
    "Cerro Porteño": 6.7,
    "Cerro Porteno": 6.7,
    "Olimpia": 6.5,
    "LDU": 7.0,
    "Independiente del Valle": 7.2,
    "Athletico PR": 7.0,
    "Athletico Paranaense": 7.0,
    "Cruzeiro": 7.0,
    # Tier B
    "Santos": 6.5,
    "Flamengo": 0.0,
    "Vasco": 6.2,
    "Fortaleza": 6.0,
    "Corinthians": 7.0,
    "Bahia": 6.0,
    "RB Bragantino": 6.3,
    "Bragantino": 6.3,
    "Cuiabá": 4.5,
    "Cuiaba": 4.5,
    "Criciúma": 4.8,
    "Criciuma": 4.8,
    # Tier C — menores
    "Bolívar": 5.5,
    "Bolivar": 5.5,
    "Deportivo Táchira": 4.0,
    "Táchira": 4.0,
    "Millonarios": 5.0,
    "Libertad": 5.2,
    "Aucas": 4.0,
}

COMPETITION_WEIGHT: dict[str, float] = {
    "Copa Libertadores": 1.5,
    "Copa Sulamericana": 1.3,
    "Brasileirão": 1.0,
    "Serie A": 1.0,
    "Copa do Brasil": 1.1,
    "Recopa Sul-Americana": 1.2,
    "Flamengo 2026": 1.0,
}

PHASE_WEIGHT: dict[str, float] = {
    "Final": 2.0,
    "Semifinal": 1.8,
    "Semis": 1.8,
    "Quartas de Final - Volta": 1.6,
    "Quartas de Final - Ida": 1.6,
    "Quartas": 1.6,
    "Oitavas de Final - Volta": 1.4,
    "Oitavas de Final - Ida": 1.4,
    "Oitavas": 1.4,
    "Fase de Grupos": 1.2,
    "Group Stage": 1.2,
    "Rodada": 1.0,
}

DIFF_SCALE_MIN = 1.0
DIFF_SCALE_MAX = 20.0


def get_opponent_strength(opponent: str) -> float:
    key = opponent.strip()
    if key in OPPONENT_STRENGTH:
        return OPPONENT_STRENGTH[key]
    for name, val in OPPONENT_STRENGTH.items():
        if name.lower() in key.lower() or key.lower() in name.lower():
            return val
    return 6.0


def get_competition_weight(competition: str) -> float:
    comp = competition.strip()
    if comp in COMPETITION_WEIGHT:
        return COMPETITION_WEIGHT[comp]
    for name, val in COMPETITION_WEIGHT.items():
        if name.lower() in comp.lower():
            return val
    return 1.0


def get_phase_weight(round_str: str) -> float:
    r = round_str.strip()
    for phase, weight in PHASE_WEIGHT.items():
        if phase.lower() in r.lower():
            return weight
    if "rodada" in r.lower():
        return 1.0
    return 1.0


def get_venue_weight(venue: str) -> float:
    v = venue.strip().upper()
    if v == "A":
        return 1.3
    if v == "N":
        return 1.1
    return 1.0


def _safe_float(val, default=0.0) -> float:
    try:
        return float(val)
    except (TypeError, ValueError):
        return default


def calculate_difficulty(match: dict) -> float:
    """
    Calcula a pontuação de dificuldade de um jogo.

    Fórmula:
        base = opponent_strength × competition_weight × venue_weight × phase_weight
        score = base + result_adj + goal_diff_adj + xga_adj
        difficulty = clamp(score, 1.0, 20.0)
    """
    opponent = match.get("opponent", "")
    competition = match.get("competition", "")
    venue = match.get("venue", "H")
    result = match.get("result", "")
    round_str = match.get("round", "")

    opponent_str = get_opponent_strength(opponent)
    comp_w = get_competition_weight(competition)
    venue_w = get_venue_weight(venue)
    phase_w = get_phase_weight(round_str)

    base = opponent_str * comp_w * venue_w * phase_w

    gf = _safe_float(match.get("gf"))
    ga = _safe_float(match.get("ga"))
    goal_diff = abs(gf - ga)

    result_adj = 0.0
    goal_adj = 0.0
    r = result.strip().upper()
    if r == "L":
        result_adj = 2.5
        goal_adj = goal_diff * 0.5
    elif r == "D":
        result_adj = 1.0
    elif r == "W":
        result_adj = 0.0
        goal_adj = -goal_diff * 0.3

    xga = _safe_float(match.get("xga"))
    xga_adj = max(0.0, (xga - 1.0) * 0.5)

    raw = base + result_adj + goal_adj + xga_adj
    return round(max(DIFF_SCALE_MIN, min(DIFF_SCALE_MAX, raw)), 2)


def enrich_matches(matches: list[dict]) -> list[dict]:
    """Adiciona 'difficulty' a cada jogo e retorna a lista enriquecida."""
    enriched = []
    for match in matches:
        m = dict(match)
        m["difficulty"] = calculate_difficulty(m)
        enriched.append(m)
    return enriched


def filter_competition(matches: list[dict], competition_key: str) -> list[dict]:
    """Filtra jogos por competição (substring case-insensitive)."""
    key = competition_key.lower()
    return [m for m in matches if key in m.get("competition", "").lower()]


def difficulty_vector(matches: list[dict]) -> list[float]:
    """Extrai o vetor de dificuldade em ordem cronológica."""
    return [m["difficulty"] for m in matches]


def top_hardest(matches: list[dict], n: int = 5) -> list[dict]:
    """Retorna os n jogos mais difíceis, ordenados por dificuldade decrescente."""
    return sorted(matches, key=lambda m: m["difficulty"], reverse=True)[:n]


def hardest_consecutive_sequence(matches: list[dict], threshold_delta: float = 0.0) -> dict:
    """
    Encontra a maior sequência contígua de jogos com dificuldade acima da média.
    Retorna informações sobre o início, fim, tamanho e dificuldade média da sequência.
    """
    if not matches:
        return {"start": 0, "end": 0, "length": 0, "avg_difficulty": 0.0, "matches": []}

    diffs = [m["difficulty"] for m in matches]
    avg = sum(diffs) / len(diffs)
    threshold = avg + threshold_delta

    best_start = 0
    best_len = 0
    cur_start = 0
    cur_len = 0

    for i, d in enumerate(diffs):
        if d >= threshold:
            if cur_len == 0:
                cur_start = i
            cur_len += 1
            if cur_len > best_len:
                best_len = cur_len
                best_start = cur_start
        else:
            cur_len = 0

    best_matches = matches[best_start : best_start + best_len]
    avg_diff = (
        sum(m["difficulty"] for m in best_matches) / best_len if best_len else 0.0
    )

    return {
        "start": best_start,
        "end": best_start + best_len - 1,
        "length": best_len,
        "avg_difficulty": round(avg_diff, 2),
        "matches": best_matches,
    }
