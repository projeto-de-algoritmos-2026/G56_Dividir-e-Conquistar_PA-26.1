"""
Estimativa heurística de chance de título do Flamengo em 2026.

AVISO: Estas são estimativas baseadas em desempenho atual, não previsões reais.
Não representam probabilidades estatísticas nem odds de apostas.
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class TitleEstimate:
    competition: str
    probability: float
    factors: dict
    explanation: str
    disclaimer: str = (
        "Estimativa heurística baseada em desempenho atual. "
        "Não é uma previsão ou probabilidade real."
    )


def _clamp(value: float, lo: float = 0.0, hi: float = 95.0) -> float:
    return max(lo, min(hi, value))


def _recent_form_points(matches: list[dict], n: int = 5) -> float:
    """Calcula pontos nos últimos n jogos (vitória=3, empate=1, derrota=0)."""
    recent = [m for m in matches if m.get("result", "").strip().upper() in ("W", "D", "L")]
    recent = sorted(recent, key=lambda m: m.get("date", ""))[-n:]
    pts = 0
    for m in recent:
        r = m.get("result", "").strip().upper()
        if r == "W":
            pts += 3
        elif r == "D":
            pts += 1
    return pts


def estimate_brasileirao(brasileirao_matches: list[dict], standings: dict | None = None) -> TitleEstimate:
    """
    Estima a chance de título do Brasileirão com base no desempenho atual.

    Fatores:
    - Aproveitamento (pontos / pontos_possíveis): peso 40%
    - Forma recente (últimos 5 jogos): peso 20%
    - Saldo de gols normalizado: peso 15%
    - Fator histórico do Flamengo: peso 25%
    """
    played = [m for m in brasileirao_matches if m.get("result", "").strip().upper() in ("W", "D", "L")]
    if not played:
        return TitleEstimate(
            competition="Brasileirão",
            probability=0.0,
            factors={},
            explanation="Sem jogos suficientes para estimar.",
        )

    # Usa standings reais se disponíveis, senão calcula dos jogos
    st = standings or {}
    wins  = st.get("won",  sum(1 for m in played if m.get("result", "").upper() == "W"))
    draws = st.get("drawn", sum(1 for m in played if m.get("result", "").upper() == "D"))
    losses = st.get("lost", sum(1 for m in played if m.get("result", "").upper() == "L"))
    n      = st.get("played", len(played))
    points = st.get("points", wins * 3 + draws)
    saldo  = st.get("gd", 0)
    position = st.get("position", 5)

    max_points = n * 3
    aproveitamento = points / max_points if max_points > 0 else 0.0

    gd_factor = _clamp((saldo / (n * 2) + 0.5), 0.0, 1.0)

    # Forma real do standings ou dos últimos 5 jogos
    form_list = st.get("form", [])
    if form_list:
        form_pts = sum(3 if r == "W" else 1 if r == "D" else 0 for r in form_list[-5:])
    else:
        form_pts = _recent_form_points(played, n=5)
    form_factor = form_pts / 15.0

    # Penaliza pelo gap de pontos em relação ao líder
    leader_pts = st.get("leader", {}).get("points", points) if st else points
    gap = max(0, leader_pts - points)
    gap_factor = _clamp(1.0 - gap / 20.0, 0.0, 1.0)

    # Fator de posição (1º=1.0, 5º=0.8, 10º=0.5)
    position_factor = _clamp((21 - position) / 20, 0.0, 1.0)

    historical_factor = 0.72

    raw = (
        aproveitamento * 0.30
        + form_factor * 0.15
        + gd_factor * 0.10
        + gap_factor * 0.20
        + position_factor * 0.10
        + historical_factor * 0.15
    )
    probability = _clamp(raw * 100 * 1.15)

    return TitleEstimate(
        competition="Brasileirão",
        probability=round(probability, 1),
        factors={
            "aproveitamento": round(aproveitamento * 100, 1),
            "pontos": points,
            "posição": position,
            "jogos": n,
            "vitorias": wins,
            "empates": draws,
            "derrotas": losses,
            "saldo_gols": int(saldo),
            "forma_recente_pts": form_pts,
            "gap_lider": gap,
        },
        explanation=(
            f"Com {points} pontos em {n} jogos ({round(aproveitamento*100,1)}% de aproveitamento), "
            f"saldo de {int(saldo)} gols e {form_pts}/15 pontos nos últimos 5 jogos, "
            f"o índice heurístico aponta {round(probability,1)}% de chance de título."
        ),
    )


def estimate_libertadores(libertadores_matches: list[dict], standings: dict | None = None) -> TitleEstimate:
    """
    Estima a chance de título da Libertadores com base no desempenho atual.

    Fatores:
    - Aproveitamento geral: peso 35%
    - Fase alcançada: peso 30%
    - Desempenho como visitante: peso 20%
    - Forma recente: peso 15%
    """
    played = [m for m in libertadores_matches if m.get("result", "").strip().upper() in ("W", "D", "L")]
    if not played:
        return TitleEstimate(
            competition="Copa Libertadores",
            probability=0.0,
            factors={},
            explanation="Sem jogos suficientes para estimar.",
        )

    # Usa standings reais se disponíveis
    st = standings or {}
    wins   = st.get("group_won",   sum(1 for m in played if m.get("result", "").upper() == "W"))
    draws  = st.get("group_drawn", sum(1 for m in played if m.get("result", "").upper() == "D"))
    losses = st.get("group_lost",  sum(1 for m in played if m.get("result", "").upper() == "L"))
    n      = st.get("group_played", len(played))
    points = st.get("group_points", wins * 3 + draws)
    group_pos = st.get("group_position", 1)
    group_gd  = st.get("group_gd", 0)
    current_stage = st.get("current_stage", "")

    max_points = n * 3
    aproveitamento = points / max_points if max_points > 0 else 0.0

    away_played = [m for m in played if m.get("venue", "").strip().upper() == "A"]
    away_wins  = sum(1 for m in away_played if m.get("result", "").upper() == "W")
    away_draws = sum(1 for m in away_played if m.get("result", "").upper() == "D")
    away_pts = away_wins * 3 + away_draws
    away_max = len(away_played) * 3
    away_factor = (away_pts / away_max) if away_max > 0 else 0.5

    # Fase real do standings ou detectada dos jogos
    if current_stage:
        stage_factor = _stage_name_to_factor(current_stage)
    else:
        stage_factor = _detect_stage_factor(played)

    # Bônus por ter passado como 1º do grupo
    group_bonus = 0.05 if group_pos == 1 else 0.0

    form_pts = _recent_form_points(played, n=min(5, n))
    form_factor = form_pts / 15.0

    raw = (
        aproveitamento * 0.35
        + stage_factor * 0.30
        + away_factor * 0.20
        + form_factor * 0.15
        + group_bonus
    )
    probability = _clamp(raw * 100 * 1.10)

    return TitleEstimate(
        competition="Copa Libertadores",
        probability=round(probability, 1),
        factors={
            "aproveitamento": round(aproveitamento * 100, 1),
            "pontos_grupo": points,
            "pos_grupo": group_pos,
            "jogos": n,
            "vitorias": wins,
            "empates": draws,
            "derrotas": losses,
            "saldo_gols": group_gd,
            "aprov_fora": round(away_factor * 100, 1),
            "fase_atual": current_stage or "Grupos",
            "forma_recente_pontos": form_pts,
        },
        explanation=(
            f"Com {points} pontos em {n} jogos ({round(aproveitamento*100,1)}% de aproveitamento), "
            f"{round(away_factor*100,1)}% de aproveitamento fora e fase estimada em "
            f"{round(stage_factor*100,1)}% do caminho, "
            f"o índice heurístico aponta {round(probability,1)}% de chance de título."
        ),
    )


def _stage_name_to_factor(stage: str) -> float:
    """Converte nome de fase em fator numérico."""
    s = stage.lower()
    if "final" in s and "semi" not in s and "oitava" not in s and "quarta" not in s:
        return 0.85
    if "semi" in s:
        return 0.70
    if "quarta" in s or "quarter" in s:
        return 0.55
    if "oitava" in s or "round of 16" in s:
        return 0.40
    return 0.25


def _detect_stage_factor(matches: list[dict]) -> float:
    """Estima qual fase foi alcançada com base nos rounds presentes."""
    rounds = [m.get("round", "").lower() for m in matches]
    combined = " ".join(rounds)
    return _stage_name_to_factor(combined)
