# Fontes de Dados

## Fonte Principal

### FBref — Football Reference

**URL base:** https://fbref.com

| Competição            | URL                                                                                   |
|-----------------------|---------------------------------------------------------------------------------------|
| Todas as competições  | https://fbref.com/en/squads/639950ae/2026/matchlogs/all_comps/schedule/              |
| Brasileirão Série A   | https://fbref.com/en/squads/639950ae/2026/matchlogs/c24/schedule/                    |
| Copa Libertadores     | https://fbref.com/en/squads/639950ae/2026/matchlogs/c14/schedule/                    |

**Dados coletados via web scraping** usando `requests` + `BeautifulSoup4`.

**Colunas extraídas:**
- `date` — data do jogo
- `competition` — nome da competição
- `round` — rodada ou fase
- `venue` — H (casa), A (fora), N (neutro)
- `result` — W/D/L
- `gf` — gols marcados
- `ga` — gols sofridos
- `opponent` — adversário
- `xg` — Expected Goals (se disponível)
- `xga` — Expected Goals Against (se disponível)
- `attendance` — público (se disponível)
- `captain` — capitão (se disponível)
- `formation` — formação (se disponível)
- `referee` — árbitro (se disponível)
- `match_report` — URL do relatório do jogo

**Avisos sobre o scraping:**
- O FBref pode retornar 429 (Too Many Requests) se muitas requisições forem feitas rapidamente
- O script respeita um intervalo de 3 segundos entre requisições
- Se o scraping falhar, o sistema usa automaticamente os dados de fallback em `data/fallback/`

---

## Fallback Local

Quando o scraping falha ou está indisponível, o sistema usa:

- `data/fallback/flamengo_2026_fallback.csv` — jogos manuais com colunas completas
- `data/fallback/players.json` — dados do elenco 2026

Estes arquivos representam uma aproximação baseada em informações públicas disponíveis até a data de criação do projeto.

---

## Dados do Elenco

Os dados dos jogadores em `data/fallback/players.json` devem ser verificados e atualizados manualmente com base em fontes confiáveis como:

- Site oficial do Flamengo: https://flamengo.com.br
- Transfermarkt: https://transfermarkt.com.br
- Globo Esporte: https://globoesporte.globo.com

**Nota:** Qualquer informação marcada como `"status": "a confirmar"` no arquivo JSON não foi verificada e não deve ser tratada como fato.

---

## Força dos Adversários

A tabela de força dos adversários (`src/analysis/difficulty_model.py`) foi construída com base em:

- Histórico recente de títulos nacionais e internacionais
- Desempenho em competições continentais nas últimas 5 edições
- Ranking da CONMEBOL para times sul-americanos

Estas notas são **estimativas qualitativas** para fins de cálculo e podem ser ajustadas no arquivo de configuração.

---

## Algoritmo de Contagem de Inversões

- **Referência clássica:** Cormen, T.H. et al. *Introduction to Algorithms*, 3rd ed. MIT Press. (Seção 2.3, exercício)
- **Referência adicional:** Kleinberg, J.; Tardos, E. *Algorithm Design*, Pearson Education, 2005.

---

## Licença dos Dados

Os dados do FBref são de uso público para fins educacionais e de pesquisa. O scraping é realizado de forma respeitosa com intervalos entre requisições. Para uso comercial, consulte os termos de serviço do FBref.
