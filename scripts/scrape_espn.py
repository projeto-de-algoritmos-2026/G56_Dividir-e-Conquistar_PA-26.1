"""
Scraping alternativo via API interna da ESPN.
Usa endpoints JSON públicos (não documentados mas acessíveis).

Flamengo team_id ESPN: 819
Brasileirão: bra.1
Copa Libertadores: conmebol.libertadores
"""

import json
import time
from datetime import datetime
from pathlib import Path

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

ROOT = Path(__file__).parent.parent
DATA_RAW = ROOT / "data" / "raw"
DATA_FALLBACK = ROOT / "data" / "fallback"

ESPN_API = "https://site.api.espn.com/apis/site/v2/sports/soccer"
FLAMENGO_ID = "819"
SEASON = "2026"

LEAGUES = {
    "brasileirao": "bra.1",
    "libertadores": "conmebol.libertadores",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Referer": "https://www.espn.com.br/",
}

RESULT_MAP = {"win": "W", "loss": "L", "tie": "D"}
VENUE_MAP = {"home": "H", "away": "A", "neutral": "N"}


def fetch_json(url: str) -> dict | None:
    if not HAS_REQUESTS:
        return None
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code == 200:
            return r.json()
        print(f"  ESPN API retornou {r.status_code}: {url}")
    except Exception as e:
        print(f"  Erro ESPN API: {e}")
    return None


def fetch_team_schedule(league_slug: str) -> list[dict]:
    """
    Busca o calendário do Flamengo via ESPN Team Schedule API.
    Endpoint: /soccer/{league}/teams/{id}/schedule?season={year}
    """
    url = f"{ESPN_API}/{league_slug}/teams/{FLAMENGO_ID}/schedule?season={SEASON}"
    print(f"  GET {url}")
    data = fetch_json(url)
    if not data:
        return []

    events = data.get("events", [])
    matches = []

    for event in events:
        competitions = event.get("competitions", [])
        if not competitions:
            continue
        comp = competitions[0]

        date_raw = event.get("date", "")
        date = date_raw[:10] if date_raw else ""
        time_str = date_raw[11:16] if len(date_raw) > 15 else ""

        competitors = comp.get("competitors", [])
        flamengo_comp = next((c for c in competitors if c.get("id") == FLAMENGO_ID), None)
        if not flamengo_comp:
            flamengo_comp = next(
                (c for c in competitors if "flamengo" in c.get("team", {}).get("displayName", "").lower()),
                None
            )
        if not flamengo_comp:
            continue

        opponent_comp = next((c for c in competitors if c != flamengo_comp), None)
        opponent = opponent_comp.get("team", {}).get("displayName", "") if opponent_comp else ""

        venue_raw = flamengo_comp.get("homeAway", "home")
        venue = VENUE_MAP.get(venue_raw, "H")

        winner = comp.get("status", {}).get("type", {}).get("completed", False)
        result_raw = flamengo_comp.get("winner")
        score_fla = flamengo_comp.get("score", "")
        score_opp = (opponent_comp or {}).get("score", "") if opponent_comp else ""

        if not winner or score_fla == "" or score_opp == "":
            continue

        try:
            gf = int(score_fla)
            ga = int(score_opp)
            if result_raw is True:
                result = "W"
            elif result_raw is False:
                result = "L"
            else:
                result = "D"
        except (ValueError, TypeError):
            continue

        season_type = event.get("seasonType", {}).get("name", "")
        round_text = event.get("week", {}).get("displayValue", "") or season_type
        comp_name = event.get("season", {}).get("name", "") or league_slug

        matches.append({
            "date": date,
            "time": time_str,
            "competition": comp_name,
            "round": round_text,
            "day": "",
            "venue": venue,
            "result": result,
            "gf": gf,
            "ga": ga,
            "opponent": opponent,
            "xg": "",
            "psxg": "",
            "xga": "",
            "poss": "",
            "attendance": "",
            "captain": "",
            "formation": "",
            "referee": "",
            "match_report": f"https://www.espn.com.br/futebol/partida/_/gameId/{event.get('id', '')}",
        })

    return matches


def fetch_scoreboard_range(league_slug: str, label: str) -> list[dict]:
    """
    Busca jogos via scoreboard da ESPN para datas específicas.
    Útil quando o schedule não retorna dados completos.
    """
    matches = []
    months = [
        (2026, 2), (2026, 3), (2026, 4), (2026, 5), (2026, 6),
    ]
    for year, month in months:
        url = (
            f"{ESPN_API}/{league_slug}/scoreboard"
            f"?limit=40&dates={year}{month:02d}01-{year}{month:02d}31"
            f"&lang=pt&region=br"
        )
        data = fetch_json(url)
        if not data:
            continue
        for event in data.get("events", []):
            comps = event.get("competitions", [])
            if not comps:
                continue
            comp = comps[0]
            competitors = comp.get("competitors", [])

            fla = next(
                (c for c in competitors
                 if "flamengo" in c.get("team", {}).get("displayName", "").lower()
                 or c.get("team", {}).get("id") == FLAMENGO_ID),
                None
            )
            if not fla:
                continue

            opp = next((c for c in competitors if c != fla), None)
            if not opp:
                continue

            completed = comp.get("status", {}).get("type", {}).get("completed", False)
            if not completed:
                continue

            score_fla = fla.get("score", "")
            score_opp = opp.get("score", "")
            try:
                gf = int(score_fla)
                ga = int(score_opp)
            except (ValueError, TypeError):
                continue

            winner = fla.get("winner")
            if winner is True:
                result = "W"
            elif winner is False:
                result = "L"
            else:
                result = "D"

            date_raw = event.get("date", "")
            date = date_raw[:10]
            venue = VENUE_MAP.get(fla.get("homeAway", "home"), "H")

            matches.append({
                "date": date,
                "time": date_raw[11:16] if len(date_raw) > 15 else "",
                "competition": label,
                "round": event.get("week", {}).get("displayValue", ""),
                "day": "",
                "venue": venue,
                "result": result,
                "gf": gf,
                "ga": ga,
                "opponent": opp.get("team", {}).get("displayName", ""),
                "xg": "", "psxg": "", "xga": "", "poss": "",
                "attendance": "", "captain": "", "formation": "", "referee": "",
                "match_report": f"https://www.espn.com.br/futebol/partida/_/gameId/{event.get('id', '')}",
            })
        time.sleep(1)

    seen = set()
    unique = []
    for m in matches:
        key = (m["date"], m["opponent"], m["gf"], m["ga"])
        if key not in seen:
            seen.add(key)
            unique.append(m)
    return unique


def scrape_espn() -> list[dict]:
    if not HAS_REQUESTS:
        print("requests não instalado — pulando ESPN.")
        return []

    all_matches = []

    for label, slug in LEAGUES.items():
        print(f"\nESPN schedule — {label}...")
        matches = fetch_team_schedule(slug)
        if matches:
            print(f"  {len(matches)} jogos via schedule")
        else:
            print(f"  schedule vazio, tentando scoreboard...")
            matches = fetch_scoreboard_range(slug, label.capitalize())
            print(f"  {len(matches)} jogos via scoreboard")

        all_matches.extend(matches)
        time.sleep(2)

    return sorted(all_matches, key=lambda m: m.get("date", ""))


def save_espn(matches: list[dict]):
    import csv
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    path = DATA_RAW / "flamengo_2026_espn.csv"
    if not matches:
        print("Nenhum dado ESPN para salvar.")
        return

    fieldnames = [
        "date", "time", "competition", "round", "day", "venue",
        "result", "gf", "ga", "opponent",
        "xg", "psxg", "xga", "poss",
        "attendance", "captain", "formation", "referee", "match_report",
    ]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(matches)
    print(f"Salvo: {path} ({len(matches)} jogos)")


if __name__ == "__main__":
    print("=== Scraping ESPN API ===")
    matches = scrape_espn()
    save_espn(matches)
    print(f"\nTotal ESPN: {len(matches)} jogos")
