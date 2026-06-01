"""
Processa os jogos coletados e enriquece com pontuação de dificuldade.
Entrada:  data/raw/flamengo_2026_matches.csv
Saída:    data/processed/flamengo_2026_analysis.json
"""

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.analysis.difficulty_model import enrich_matches

DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
DATA_FALLBACK = ROOT / "data" / "fallback"


def load_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_matches() -> tuple[list[dict], str]:
    raw_path = DATA_RAW / "flamengo_2026_matches.csv"
    if raw_path.exists():
        matches = load_csv(raw_path)
        if matches:
            return matches, "FBref (scraping)"

    fallback_path = DATA_FALLBACK / "flamengo_2026_fallback.csv"
    matches = load_csv(fallback_path)
    return matches, "Fallback local"


def normalize(matches: list[dict]) -> list[dict]:
    """Padroniza campos e remove jogos sem resultado."""
    valid = []
    for m in matches:
        result = m.get("result", "").strip().upper()
        if result not in ("W", "D", "L"):
            continue
        m["result"] = result
        m["venue"] = m.get("venue", "H").strip().upper() or "H"

        for col in ("gf", "ga", "xg", "xga", "poss"):
            try:
                m[col] = float(m[col]) if m.get(col, "").strip() else None
            except (ValueError, AttributeError):
                m[col] = None

        valid.append(m)
    return sorted(valid, key=lambda x: x.get("date", ""))


def main():
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

    matches, source = load_matches()
    if not matches:
        print("Nenhum dado de entrada encontrado. Execute scrape_fbref.py primeiro.")
        sys.exit(1)

    matches = normalize(matches)
    matches = enrich_matches(matches)

    for m in matches:
        m["gf"] = m["gf"] if m["gf"] is not None else ""
        m["ga"] = m["ga"] if m["ga"] is not None else ""
        m["xg"] = m["xg"] if m["xg"] is not None else ""
        m["xga"] = m["xga"] if m["xga"] is not None else ""

    out_path = DATA_PROCESSED / "flamengo_2026_analysis.json"
    payload = {
        "source": source,
        "total_matches": len(matches),
        "matches": matches,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"Processados {len(matches)} jogos de '{source}' → {out_path}")
    diffs = [m["difficulty"] for m in matches]
    print(f"Dificuldade: mín={min(diffs):.1f} | máx={max(diffs):.1f} | média={sum(diffs)/len(diffs):.1f}")


if __name__ == "__main__":
    main()
