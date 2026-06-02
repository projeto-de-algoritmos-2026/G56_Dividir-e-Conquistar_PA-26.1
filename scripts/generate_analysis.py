"""
Gera a análise completa de Contagem de Inversões e escreve o JSON
final que o frontend consome.

Saída:
  src/api/analysis.json
  frontend/public/analysis.json  (cópia para o servidor de dev Vite)
"""

import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.algorithms.inversion_count import count_inversions, sliding_window_inversions
from src.analysis.difficulty_model import (
    difficulty_vector,
    filter_competition,
    hardest_consecutive_sequence,
    top_hardest,
)
from src.analysis.title_probability import estimate_brasileirao, estimate_libertadores

DATA_PROCESSED = ROOT / "data" / "processed"
DATA_FALLBACK = ROOT / "data" / "fallback"
SRC_API = ROOT / "src" / "api"
FRONTEND_PUBLIC = ROOT / "frontend" / "public"


def _load_standings() -> dict:
    path = DATA_FALLBACK / "standings.json"
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def load_processed() -> tuple[list[dict], str]:
    path = DATA_PROCESSED / "flamengo_2026_analysis.json"
    if path.exists():
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return data["matches"], data.get("source", "processado")

    print("Arquivo processado não encontrado. Usando fallback + processamento inline.")
    import csv
    from src.analysis.difficulty_model import enrich_matches

    fallback = DATA_FALLBACK / "flamengo_2026_fallback.csv"
    with open(fallback, encoding="utf-8") as f:
        matches = list(csv.DictReader(f))

    for m in matches:
        for col in ("gf", "ga", "xg", "xga"):
            try:
                m[col] = float(m[col]) if m.get(col, "").strip() else None
            except (ValueError, AttributeError):
                m[col] = None

    matches = [m for m in matches if m.get("result", "").strip().upper() in ("W", "D", "L")]
    matches = sorted(matches, key=lambda x: x.get("date", ""))
    matches = enrich_matches(matches)
    return matches, "Fallback local"


def analyse_group(matches: list[dict], label: str) -> dict:
    if not matches:
        return {
            "label": label,
            "matches": [],
            "difficulty_vector": [],
            "inversions": 0,
            "max_inversions": 0,
            "inversion_percentage": 0.0,
        }

    vec = difficulty_vector(matches)
    inv = count_inversions(vec)

    return {
        "label": label,
        "matches": matches,
        "difficulty_vector": [round(v, 2) for v in vec],
        "inversions": inv.inversions,
        "max_inversions": inv.max_inversions,
        "inversion_percentage": inv.percentage,
    }


def monthly_windows(matches: list[dict]) -> list[dict]:
    by_month: dict[str, list[dict]] = defaultdict(list)
    for m in matches:
        date = m.get("date", "")
        if len(date) >= 7:
            key = date[:7]
            by_month[key].append(m)

    result = []
    for month in sorted(by_month):
        group_matches = by_month[month]
        vec = difficulty_vector(group_matches)
        inv = count_inversions(vec)
        wins = sum(1 for m in group_matches if m.get("result", "").upper() == "W")
        result.append(
            {
                "month": month,
                "label": _month_label(month),
                "matches_count": len(group_matches),
                "wins": wins,
                "avg_difficulty": round(sum(vec) / len(vec), 2) if vec else 0.0,
                "inversions": inv.inversions,
                "inversion_percentage": inv.percentage,
                "difficulty_vector": [round(v, 2) for v in vec],
            }
        )
    return result


def _month_label(ym: str) -> str:
    months = {
        "01": "Jan", "02": "Fev", "03": "Mar", "04": "Abr",
        "05": "Mai", "06": "Jun", "07": "Jul", "08": "Ago",
        "09": "Set", "10": "Out", "11": "Nov", "12": "Dez",
    }
    year, month = ym[:4], ym[5:7]
    return f"{months.get(month, month)}/{year}"


def match_summary(m: dict) -> dict:
    return {
        "date": m.get("date", ""),
        "competition": m.get("competition", ""),
        "round": m.get("round", ""),
        "venue": m.get("venue", ""),
        "opponent": m.get("opponent", ""),
        "result": m.get("result", ""),
        "gf": m.get("gf", ""),
        "ga": m.get("ga", ""),
        "xg": m.get("xg", ""),
        "xga": m.get("xga", ""),
        "difficulty": m.get("difficulty", 0.0),
    }


def main():
    SRC_API.mkdir(parents=True, exist_ok=True)
    FRONTEND_PUBLIC.mkdir(parents=True, exist_ok=True)

    matches, source = load_processed()
    print(f"Gerando análise para {len(matches)} jogos ({source})...")

    brasileirao = filter_competition(matches, "brasileir")
    libertadores = filter_competition(matches, "libertadores")
    combined = sorted(matches, key=lambda m: m.get("date", ""))

    br_analysis = analyse_group(brasileirao, "Brasileirão 2026")
    lib_analysis = analyse_group(libertadores, "Copa Libertadores 2026")
    comb_analysis = analyse_group(combined, "Temporada Completa 2026")

    standings = _load_standings()
    br_estimate = estimate_brasileirao(brasileirao, standings.get("brasileirao"))
    lib_estimate = estimate_libertadores(libertadores, standings.get("libertadores"))

    top = [match_summary(m) for m in top_hardest(combined, 5)]
    hardest_seq = hardest_consecutive_sequence(combined)
    hardest_seq["matches"] = [match_summary(m) for m in hardest_seq["matches"]]

    window_inv = sliding_window_inversions(difficulty_vector(combined), window_size=5)

    def comp_summary(analysis: dict) -> dict:
        return {
            "label": analysis["label"],
            "matches": [match_summary(m) for m in analysis["matches"]],
            "difficulty_vector": analysis["difficulty_vector"],
            "inversions": analysis["inversions"],
            "max_inversions": analysis["max_inversions"],
            "inversion_percentage": analysis["inversion_percentage"],
        }

    players_path = DATA_FALLBACK / "players.json"
    players = []
    if players_path.exists():
        with open(players_path, encoding="utf-8") as f:
            players = json.load(f)

    output = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "source": source,
            "total_matches": len(matches),
            "competitions": list({m.get("competition", "") for m in matches}),
        },
        "brasileirao": comp_summary(br_analysis),
        "libertadores": comp_summary(lib_analysis),
        "combined": comp_summary(comb_analysis),
        "monthly_windows": monthly_windows(combined),
        "top_hardest_matches": top,
        "hardest_sequence": hardest_seq,
        "window_inversions": window_inv,
        "title_probability": {
            "brasileirao": {
                "probability": br_estimate.probability,
                "factors": br_estimate.factors,
                "explanation": br_estimate.explanation,
                "disclaimer": br_estimate.disclaimer,
            },
            "libertadores": {
                "probability": lib_estimate.probability,
                "factors": lib_estimate.factors,
                "explanation": lib_estimate.explanation,
                "disclaimer": lib_estimate.disclaimer,
            },
        },
        "players": players,
    }

    for path in [SRC_API / "analysis.json", FRONTEND_PUBLIC / "analysis.json"]:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"  Escrito: {path}")

    br = output["brasileirao"]
    lib = output["libertadores"]
    comb = output["combined"]
    print(f"\nBrasileirao  — {br['inversions']}/{br['max_inversions']} inversões ({br['inversion_percentage']}%)")
    print(f"Libertadores — {lib['inversions']}/{lib['max_inversions']} inversões ({lib['inversion_percentage']}%)")
    print(f"Combinado    — {comb['inversions']}/{comb['max_inversions']} inversões ({comb['inversion_percentage']}%)")
    print(f"\nChance heurística título Brasileirão:  {br_estimate.probability}%")
    print(f"Chance heurística título Libertadores: {lib_estimate.probability}%")


if __name__ == "__main__":
    main()
