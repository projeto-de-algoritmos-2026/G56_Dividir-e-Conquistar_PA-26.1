"""
Scraping de jogos do Flamengo 2026 no FBref.
Coleta dados de todas as competições e salva em data/raw/.
Em caso de falha, usa fallback de data/fallback/.
"""

import csv
import json
import os
import sys
import time
import re
from datetime import datetime
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False

ROOT = Path(__file__).parent.parent
DATA_RAW = ROOT / "data" / "raw"
DATA_FALLBACK = ROOT / "data" / "fallback"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

URLS = {
    "all": (
        "https://fbref.com/en/squads/639950ae/2026/matchlogs/"
        "all_comps/schedule/Flamengo-Scores-and-Fixtures-All-Competitions"
    ),
    "brasileirao": (
        "https://fbref.com/en/squads/639950ae/2026/matchlogs/"
        "c24/schedule/Flamengo-Scores-and-Fixtures-Serie-A"
    ),
    "libertadores": (
        "https://fbref.com/en/squads/639950ae/2026/matchlogs/"
        "c14/schedule/Flamengo-Scores-and-Fixtures-Copa-Libertadores"
    ),
}

COLUMNS = [
    "date", "time", "competition", "round", "day", "venue",
    "result", "gf", "ga", "opponent",
    "xg", "psxg", "xga", "poss",
    "attendance", "captain", "formation", "referee",
    "match_report",
]


def fetch_page(url: str, retries: int = 3) -> str | None:
    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=20)
            if resp.status_code == 200:
                return resp.text
            if resp.status_code == 429:
                wait = 30 * (attempt + 1)
                print(f"  Rate limited. Aguardando {wait}s...")
                time.sleep(wait)
            else:
                print(f"  HTTP {resp.status_code} em {url}")
                return None
        except requests.RequestException as e:
            print(f"  Erro de rede (tentativa {attempt + 1}): {e}")
            time.sleep(5)
    return None


def parse_text(tag) -> str:
    if tag is None:
        return ""
    text = tag.get_text(strip=True)
    return text if text and text != "—" else ""


def parse_table(html: str, competition_label: str) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table", id=re.compile(r"matchlogs"))
    if table is None:
        table = soup.find("table", class_=re.compile(r"stats_table"))
    if table is None:
        return []

    rows = table.find("tbody").find_all("tr")
    matches = []

    for row in rows:
        if row.get("class") and "spacer" in row.get("class", []):
            continue
        if row.get("class") and "thead" in row.get("class", []):
            continue

        def cell(stat):
            td = row.find(["td", "th"], {"data-stat": stat})
            return parse_text(td)

        def cell_href(stat):
            td = row.find(["td", "th"], {"data-stat": stat})
            if td:
                a = td.find("a")
                if a and a.get("href"):
                    return "https://fbref.com" + a["href"]
            return ""

        date = cell("date")
        if not date or not re.match(r"\d{4}-\d{2}-\d{2}", date):
            continue

        comp = cell("comp") or competition_label
        result = cell("result")
        if not result:
            continue

        match = {
            "date": date,
            "time": cell("time"),
            "competition": comp,
            "round": cell("round"),
            "day": cell("dayofweek"),
            "venue": cell("venue"),
            "result": result,
            "gf": cell("goals_for"),
            "ga": cell("goals_against"),
            "opponent": cell("opponent"),
            "xg": cell("xg"),
            "psxg": cell("psxg"),
            "xga": cell("xga"),
            "poss": cell("possession"),
            "attendance": cell("attendance"),
            "captain": cell("captain"),
            "formation": cell("formation"),
            "referee": cell("referee"),
            "match_report": cell_href("match_report"),
        }
        matches.append(match)

    return matches


def save_csv(matches: list[dict], path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(matches)
    print(f"  Salvo: {path} ({len(matches)} jogos)")


def load_fallback() -> list[dict]:
    path = DATA_FALLBACK / "flamengo_2026_fallback.csv"
    if not path.exists():
        print("  Fallback não encontrado em", path)
        return []
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        matches = list(reader)
    print(f"  Fallback carregado: {len(matches)} jogos de {path}")
    return matches


def scrape_all() -> list[dict]:
    if not HAS_DEPS:
        print("Dependências ausentes (requests, bs4). Usando fallback.")
        return load_fallback()

    print("Coletando jogos de todas as competições...")
    html = fetch_page(URLS["all"])
    time.sleep(3)

    if html:
        matches = parse_table(html, "Flamengo 2026")
        if matches:
            return matches
        print("  Tabela vazia na página all_comps. Tentando por competição...")

    all_matches = []
    for comp, url in [("Brasileirão", URLS["brasileirao"]), ("Copa Libertadores", URLS["libertadores"])]:
        print(f"Coletando {comp}...")
        html = fetch_page(url)
        time.sleep(3)
        if html:
            parsed = parse_table(html, comp)
            print(f"  {len(parsed)} jogos encontrados")
            all_matches.extend(parsed)

    if not all_matches:
        print("Scraping falhou. Usando fallback local.")
        return load_fallback()

    return all_matches


def main():
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    matches = scrape_all()

    if not matches:
        print("Nenhum dado disponível.")
        sys.exit(1)

    matches.sort(key=lambda m: m.get("date", ""))

    out_path = DATA_RAW / "flamengo_2026_matches.csv"
    save_csv(matches, out_path)

    meta = {
        "source": "FBref scraping" if HAS_DEPS else "Fallback local",
        "scraped_at": datetime.now().isoformat(),
        "total_matches": len(matches),
        "competitions": list({m["competition"] for m in matches}),
    }
    meta_path = DATA_RAW / "scraping_meta.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"\nTotal: {len(matches)} jogos | Meta: {meta_path}")


if __name__ == "__main__":
    main()
