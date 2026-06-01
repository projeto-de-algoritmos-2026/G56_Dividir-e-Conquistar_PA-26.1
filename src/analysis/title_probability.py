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


def estimate_brasileirao(brasileirao_matches: list[dict]) -> TitleEstimate:
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

    wins = sum(1 for m in played if m.get("result", "").strip().upper() == "W")
    draws = sum(1 for m in played if m.get("result", "").strip().upper() == "D")
    losses = sum(1 for m in played if m.get("result", "").strip().upper() == "L")
    n = len(played)

    points = wins * 3 + draws
    max_points = n * 3
    aproveitamento = points / max_points if max_points > 0 else 0.0

    gf_total = sum(float(m.get("gf", 0) or 0) for m in played)
    ga_total = sum(float(m.get("ga", 0) or 0) for m in played)
    saldo = gf_total - ga_total
    gd_factor = _clamp((saldo / (n * 2) + 0.5), 0.0, 1.0)

    form_pts = _recent_form_points(played, n=5)
    form_factor = form_pts / 15.0

    historical_factor = 0.72

    raw = (
        aproveitamento * 0.40
        + form_factor * 0.20
        + gd_factor * 0.15
        + historical_factor * 0.25
    )
    probability = _clamp(raw * 100 * 1.15)

    return TitleEstimate(
        competition="Brasileirão",
        probability=round(probability, 1),
        factors={
            "aproveitamento": round(aproveitamento * 100, 1),
            "pontos": points,
            "jogos": n,
            "vitorias": wins,
            "empates": draws,
            "derrotas": losses,
            "saldo_gols": int(saldo),
            "forma_recente_pontos": form_pts,
            "fator_historico": round(historical_factor * 100, 1),
        },
        explanation=(
            f"Com {points} pontos em {n} jogos ({round(aproveitamento*100,1)}% de aproveitamento), "
            f"saldo de {int(saldo)} gols e {form_pts}/15 pontos nos últimos 5 jogos, "
            f"o índice heurístico aponta {round(probability,1)}% de chance de título."
        ),
    )


def estimate_libertadores(libertadores_matches: list[dict]) -> TitleEstimate:
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

    wins = sum(1 for m in played if m.get("result", "").strip().upper() == "W")
    draws = sum(1 for m in played if m.get("result", "").strip().upper() == "D")
    losses = sum(1 for m in played if m.get("result", "").strip().upper() == "L")
    n = len(played)

    points = wins * 3 + draws
    max_points = n * 3
    aproveitamento = points / max_points if max_points > 0 else 0.0

    away_played = [m for m in played if m.get("venue", "").strip().upper() == "A"]
    away_wins = sum(1 for m in away_played if m.get("result", "").strip().upper() == "W")
    away_draws = sum(1 for m in away_played if m.get("result", "").strip().upper() == "D")
    away_pts = away_wins * 3 + away_draws
    away_max = len(away_played) * 3
    away_factor = (away_pts / away_max) if away_max > 0 else 0.5

    stage_factor = _detect_stage_factor(played)

    form_pts = _recent_form_points(played, n=min(5, n))
    form_factor = form_pts / 15.0

    raw = (
        aproveitamento * 0.35
        + stage_factor * 0.30
        + away_factor * 0.20
        + form_factor * 0.15
    )
    probability = _clamp(raw * 100 * 1.10)

    return TitleEstimate(
        competition="Copa Libertadores",
        probability=round(probability, 1),
        factors={
            "aproveitamento": round(aproveitamento * 100, 1),
            "pontos": points,
            "jogos": n,
            "vitorias": wins,
            "empates": draws,
            "derrotas": losses,
            "aproveitamento_fora": round(away_factor * 100, 1),
            "fase_fator": round(stage_factor * 100, 1),
            "forma_recente_pontos": form_pts,
        },
        explanation=(
            f"Com {points} pontos em {n} jogos ({round(aproveitamento*100,1)}% de aproveitamento), "
            f"{round(away_factor*100,1)}% de aproveitamento fora e fase estimada em "
            f"{round(stage_factor*100,1)}% do caminho, "
            f"o índice heurístico aponta {round(probability,1)}% de chance de título."
        ),
    )


def _detect_stage_factor(matches: list[dict]) -> float:
    """Estima qual fase foi alcançada com base nos rounds presentes."""
    rounds = [m.get("round", "").lower() for m in matches]
    combined = " ".join(rounds)

    if "final" in combined and "semi" not in combined:
        return 0.85
    if "semifinal" in combined or "semi" in combined:
        return 0.70
    if "quartas" in combined or "quarter" in combined:
        return 0.55
    if "oitavas" in combined or "round of 16" in combined:
        return 0.40
    if "grupo" in combined or "group" in combined:
        return 0.25
    return 0.20
