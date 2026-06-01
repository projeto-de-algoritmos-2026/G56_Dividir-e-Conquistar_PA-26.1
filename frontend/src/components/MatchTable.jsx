import { useState } from 'react'
import { fmtDate, fmtResult, difficultyColor, competitionLabel, venueLabel } from '../utils/formatters'
import styles from './MatchTable.module.css'

const COMP_FILTER = ['Todos', 'Brasileirão', 'Libertadores']

export default function MatchTable({ matches }) {
  const [filter, setFilter] = useState('Todos')
  const [sortBy, setSortBy] = useState('date')
  const [sortDir, setSortDir] = useState('asc')

  const filtered = matches.filter(m => {
    if (filter === 'Todos') return true
    if (filter === 'Brasileirão') return m.competition?.toLowerCase().includes('brasileir')
    if (filter === 'Libertadores') return m.competition?.toLowerCase().includes('libertadores')
    return true
  })

  const sorted = [...filtered].sort((a, b) => {
    let va = a[sortBy] ?? ''
    let vb = b[sortBy] ?? ''
    if (sortBy === 'difficulty') {
      va = parseFloat(va) || 0
      vb = parseFloat(vb) || 0
    }
    if (va < vb) return sortDir === 'asc' ? -1 : 1
    if (va > vb) return sortDir === 'asc' ? 1 : -1
    return 0
  })

  function toggleSort(col) {
    if (sortBy === col) setSortDir(d => d === 'asc' ? 'desc' : 'asc')
    else { setSortBy(col); setSortDir('asc') }
  }

  function SortIcon({ col }) {
    if (sortBy !== col) return <span className={styles.sortIcon}>↕</span>
    return <span className={styles.sortIcon}>{sortDir === 'asc' ? '↑' : '↓'}</span>
  }

  return (
    <div>
      <div className={styles.filters}>
        {COMP_FILTER.map(f => (
          <button
            key={f}
            className={`${styles.filterBtn} ${filter === f ? styles.active : ''}`}
            onClick={() => setFilter(f)}
          >
            {f}
          </button>
        ))}
        <span className={styles.count}>{filtered.length} jogos</span>
      </div>

      <div className="table-wrap">
        <table className="data-table">
          <thead>
            <tr>
              <th onClick={() => toggleSort('date')} className={styles.sortable}>
                Data <SortIcon col="date" />
              </th>
              <th>Competição</th>
              <th>Fase</th>
              <th onClick={() => toggleSort('venue')} className={styles.sortable}>
                Local <SortIcon col="venue" />
              </th>
              <th onClick={() => toggleSort('opponent')} className={styles.sortable}>
                Adversário <SortIcon col="opponent" />
              </th>
              <th>Resultado</th>
              <th onClick={() => toggleSort('difficulty')} className={styles.sortable}>
                Dificuldade <SortIcon col="difficulty" />
              </th>
            </tr>
          </thead>
          <tbody>
            {sorted.map((m, i) => (
              <tr key={i}>
                <td>{fmtDate(m.date)}</td>
                <td>
                  <span className={`badge ${m.competition?.toLowerCase().includes('libertadores') ? 'badge-gold' : 'badge-red'}`}>
                    {competitionLabel(m.competition)}
                  </span>
                </td>
                <td className={styles.phase}>{m.round || '—'}</td>
                <td>{venueLabel(m.venue)}</td>
                <td className={styles.opponent}>{m.opponent || '—'}</td>
                <td className={`result-${m.result}`}>
                  <strong>{fmtResult(m.result, m.gf, m.ga)}</strong>
                </td>
                <td>
                  <span
                    className={styles.diffBadge}
                    style={{ color: difficultyColor(m.difficulty) }}
                  >
                    {parseFloat(m.difficulty || 0).toFixed(1)}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
