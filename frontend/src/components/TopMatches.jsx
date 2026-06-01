import { fmtDate, difficultyColor, competitionLabel, venueLabel } from '../utils/formatters'
import styles from './TopMatches.module.css'

const MEDALS = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣']

export default function TopMatches({ matches }) {
  if (!matches?.length) return null

  return (
    <div className={styles.list}>
      {matches.map((m, i) => (
        <div key={i} className={styles.item}>
          <div className={styles.rank}>{MEDALS[i]}</div>
          <div className={styles.info}>
            <div className={styles.opponent}>{m.opponent}</div>
            <div className={styles.meta}>
              <span className={`badge ${m.competition?.toLowerCase().includes('libertadores') ? 'badge-gold' : 'badge-red'}`}>
                {competitionLabel(m.competition)}
              </span>
              <span className={styles.metaText}>{venueLabel(m.venue)}</span>
              <span className={styles.metaText}>{fmtDate(m.date)}</span>
              <span className={styles.metaText}>{m.round}</span>
            </div>
          </div>
          <div className={styles.result}>
            <span className={`result-${m.result}`}>{m.result} {m.gf !== '' ? `${m.gf}–${m.ga}` : ''}</span>
          </div>
          <div className={styles.diff} style={{ color: difficultyColor(m.difficulty) }}>
            {parseFloat(m.difficulty || 0).toFixed(1)}
          </div>
        </div>
      ))}
    </div>
  )
}
