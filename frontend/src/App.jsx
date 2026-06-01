import { useAnalysis } from './hooks/useAnalysis'
import Header from './components/Header'
import StatsGrid from './components/StatsGrid'
import DifficultyChart from './components/DifficultyChart'
import CompetitionComparison from './components/CompetitionComparison'
import MatchTable from './components/MatchTable'
import TopMatches from './components/TopMatches'
import TitleProbability from './components/TitleProbability'
import WindowAnalysis from './components/WindowAnalysis'
import InversionExplainer from './components/InversionExplainer'
import PlayerSection from './components/PlayerSection'

export default function App() {
  const { data, loading, error } = useAnalysis()

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner" />
        <p style={{ color: 'var(--gray-light)', fontSize: '0.9rem' }}>Carregando análise…</p>
      </div>
    )
  }

  if (error || !data) {
    return (
      <div className="loading">
        <p style={{ color: 'var(--red-light)', fontSize: '1rem' }}>
          Erro ao carregar dados: {error || 'análise não disponível'}.
        </p>
        <p style={{ color: 'var(--gray)', fontSize: '0.82rem', marginTop: 8 }}>
          Execute <code>python scripts/generate_analysis.py</code> e recarregue a página.
        </p>
      </div>
    )
  }

  return (
    <>
      <Header metadata={data.metadata} />

      <main className="page">
        <div className="section">
          <StatsGrid data={data} />
        </div>

        <div className="section">
          <h2 className="section-title">Dificuldade por Jogo — Temporada Completa</h2>
          <DifficultyChart matches={data.combined?.matches ?? []} />
        </div>

        <div className="section">
          <h2 className="section-title">Brasileirão vs Libertadores</h2>
          <CompetitionComparison
            brasileirao={data.brasileirao}
            libertadores={data.libertadores}
          />
        </div>

        <div className="section">
          <h2 className="section-title">Análise por Período</h2>
          <WindowAnalysis monthlyWindows={data.monthly_windows} />
        </div>

        <div className="section">
          <h2 className="section-title">Estimativa Heurística de Título</h2>
          <p style={{ fontSize: '0.82rem', color: 'var(--gray)', marginBottom: 20 }}>
            Métrica baseada em desempenho atual. Não é previsão estatística nem odds de apostas.
          </p>
          <TitleProbability titleProbability={data.title_probability} />
        </div>

        <div className="section">
          <h2 className="section-title">Top 5 Jogos Mais Difíceis</h2>
          <TopMatches matches={data.top_hardest_matches} />
        </div>

        {data.hardest_sequence?.length > 0 && (
          <div className="section">
            <h2 className="section-title">Sequência Mais Pesada</h2>
            <div className="card" style={{ marginBottom: 16 }}>
              <div style={{ display: 'flex', gap: 24, flexWrap: 'wrap' }}>
                <div>
                  <div style={{ fontSize: '0.72rem', textTransform: 'uppercase', letterSpacing: '0.06em', color: 'var(--gray)', marginBottom: 4 }}>Comprimento</div>
                  <div style={{ fontSize: '2rem', fontWeight: 900 }}>{data.hardest_sequence.length} jogos</div>
                </div>
                <div>
                  <div style={{ fontSize: '0.72rem', textTransform: 'uppercase', letterSpacing: '0.06em', color: 'var(--gray)', marginBottom: 4 }}>Dificuldade média</div>
                  <div style={{ fontSize: '2rem', fontWeight: 900, color: 'var(--red-light)' }}>{data.hardest_sequence.avg_difficulty}</div>
                </div>
                <div>
                  <div style={{ fontSize: '0.72rem', textTransform: 'uppercase', letterSpacing: '0.06em', color: 'var(--gray)', marginBottom: 4 }}>Jogos</div>
                  <div style={{ fontSize: '0.9rem', color: 'var(--white-muted)', marginTop: 4 }}>
                    {data.hardest_sequence.matches?.map(m => m.opponent).join(' → ')}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="section">
          <h2 className="section-title">Tabela de Jogos</h2>
          <MatchTable matches={data.combined?.matches ?? []} />
        </div>

        <div className="section">
          <h2 className="section-title">Contagem de Inversões — Conceito e Algoritmo</h2>
          <InversionExplainer
            combined={data.combined}
            brasileirao={data.brasileirao}
            libertadores={data.libertadores}
          />
        </div>

        {data.players?.length > 0 && (
          <div className="section">
            <h2 className="section-title">Elenco 2026</h2>
            <PlayerSection players={data.players} />
          </div>
        )}

        <footer style={{
          marginTop: 80,
          paddingTop: 32,
          borderTop: '1px solid rgba(255,255,255,0.06)',
          textAlign: 'center',
          fontSize: '0.78rem',
          color: 'var(--gray)',
          lineHeight: 1.8,
        }}>
          <p>Projeto Acadêmico — Análise de Algoritmos · Dividir e Conquistar</p>
          <p>Dados via FBref.com · Algoritmo: Contagem de Inversões O(n log n)</p>
          <p style={{ marginTop: 8 }}>
            <a href="https://fbref.com/en/squads/639950ae/2026/" target="_blank" rel="noopener noreferrer">
              FBref — Flamengo 2026
            </a>
          </p>
        </footer>
      </main>
    </>
  )
}
