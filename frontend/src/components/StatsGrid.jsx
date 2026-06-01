import styles from './StatsGrid.module.css'

function StatCard({ label, value, sub, accent, icon }) {
  return (
    <div className={`card ${styles.card} ${accent === 'red' ? 'card-red' : accent === 'gold' ? 'card-gold' : ''}`}>
      {icon && <div className={styles.icon}>{icon}</div>}
      <div className={styles.value}>{value}</div>
      <div className={styles.label}>{label}</div>
      {sub && <div className={styles.sub}>{sub}</div>}
    </div>
  )
}

export default function StatsGrid({ data }) {
  const br = data.brasileirao
  const lib = data.libertadores
  const comb = data.combined
  const meta = data.metadata

  const brProb = data.title_probability?.brasileirao?.probability ?? 0
  const libProb = data.title_probability?.libertadores?.probability ?? 0

  return (
    <div className={styles.grid}>
      <StatCard
        icon="⚽"
        label="Jogos Analisados"
        value={meta.total_matches}
        sub={`${br.matches.length} Brasileirão · ${lib.matches.length} Libertadores`}
      />
      <StatCard
        icon="🔢"
        label="Inversões Brasileirão"
        value={br.inversions}
        sub={`de ${br.max_inversions} possíveis · ${br.inversion_percentage}%`}
      />
      <StatCard
        icon="🏆"
        label="Inversões Libertadores"
        value={lib.inversions}
        sub={`de ${lib.max_inversions} possíveis · ${lib.inversion_percentage}%`}
        accent="gold"
      />
      <StatCard
        icon="📊"
        label="Inversões Totais"
        value={comb.inversions}
        sub={`de ${comb.max_inversions} possíveis`}
      />
      <StatCard
        icon="🌀"
        label="Desordem da Temporada"
        value={`${comb.inversion_percentage}%`}
        sub="Percentual de inversões no calendário completo"
      />
      <StatCard
        icon="🇧🇷"
        label="Chance Título Brasileirão"
        value={`${brProb}%`}
        sub="Estimativa heurística"
        accent="red"
      />
      <StatCard
        icon="🌎"
        label="Chance Título Libertadores"
        value={`${libProb}%`}
        sub="Estimativa heurística"
        accent="gold"
      />
      <StatCard
        icon="🔥"
        label="Jogo Mais Difícil"
        value={data.top_hardest_matches?.[0]?.difficulty ?? '—'}
        sub={data.top_hardest_matches?.[0]
          ? `vs ${data.top_hardest_matches[0].opponent}`
          : ''}
        accent="red"
      />
    </div>
  )
}
