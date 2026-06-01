import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Cell,
} from 'recharts'
import styles from './CompetitionComparison.module.css'

export default function CompetitionComparison({ brasileirao, libertadores }) {
  const brMatches = brasileirao?.matches ?? []
  const libMatches = libertadores?.matches ?? []

  const brAvg = brMatches.length
    ? brMatches.reduce((s, m) => s + parseFloat(m.difficulty || 0), 0) / brMatches.length
    : 0

  const libAvg = libMatches.length
    ? libMatches.reduce((s, m) => s + parseFloat(m.difficulty || 0), 0) / libMatches.length
    : 0

  const barData = [
    {
      name: 'Brasileirão',
      inversions: brasileirao?.inversion_percentage ?? 0,
      avg_difficulty: parseFloat(brAvg.toFixed(1)),
      matches: brMatches.length,
      color: '#E31D1C',
    },
    {
      name: 'Libertadores',
      inversions: libertadores?.inversion_percentage ?? 0,
      avg_difficulty: parseFloat(libAvg.toFixed(1)),
      matches: libMatches.length,
      color: '#C89B3C',
    },
  ]

  return (
    <div className={styles.wrap}>
      <div className={styles.charts}>
        <div className={styles.chartBlock}>
          <h4 className={styles.chartTitle}>Desordem (% de inversões)</h4>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={barData} margin={{ top: 8, right: 16, bottom: 8, left: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey="name" tick={{ fill: '#aaa', fontSize: 12 }} />
              <YAxis domain={[0, 100]} tick={{ fill: '#888', fontSize: 11 }} unit="%" />
              <Tooltip
                formatter={(v, name) => [`${v}%`, 'Desordem']}
                contentStyle={{ background: '#1a1a1a', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 8 }}
                labelStyle={{ color: '#fff' }}
                itemStyle={{ color: '#aaa' }}
              />
              <Bar dataKey="inversions" radius={[6, 6, 0, 0]}>
                {barData.map((entry) => (
                  <Cell key={entry.name} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className={styles.chartBlock}>
          <h4 className={styles.chartTitle}>Dificuldade Média</h4>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={barData} margin={{ top: 8, right: 16, bottom: 8, left: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey="name" tick={{ fill: '#aaa', fontSize: 12 }} />
              <YAxis domain={[0, 20]} tick={{ fill: '#888', fontSize: 11 }} />
              <Tooltip
                formatter={(v, name) => [v.toFixed(1), 'Dificuldade média']}
                contentStyle={{ background: '#1a1a1a', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 8 }}
                labelStyle={{ color: '#fff' }}
                itemStyle={{ color: '#aaa' }}
              />
              <Bar dataKey="avg_difficulty" radius={[6, 6, 0, 0]}>
                {barData.map((entry) => (
                  <Cell key={entry.name} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className={styles.summary}>
        {barData.map(d => (
          <div key={d.name} className={styles.summaryItem} style={{ borderColor: d.color }}>
            <div className={styles.summaryComp} style={{ color: d.color }}>{d.name}</div>
            <div className={styles.summaryStats}>
              <span>{d.matches} jogos</span>
              <span>{d.inversions}% de desordem</span>
              <span>Dif. média: {d.avg_difficulty}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
