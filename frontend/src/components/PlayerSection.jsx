import styles from './PlayerSection.module.css'

const POSITION_COLOR = {
  'Goleiro': '#3B82F6',
  'Zagueiro': '#8B5CF6',
  'Lateral': '#06B6D4',
  'Meia': '#22C55E',
  'Meia-atacante': '#84CC16',
  'Ponta-esquerda': '#F59E0B',
  'Centroavante': '#EF4444',
}

function PlayerCard({ player }) {
  const posColor = POSITION_COLOR[player.position] || '#888'
  const isToConfirm = player.status === 'a confirmar'

  return (
    <div className={`card ${styles.playerCard} ${isToConfirm ? styles.unconfirmed : ''}`}>
      <div className={styles.avatar} style={{ borderColor: posColor }}>
        <span className={styles.initials}>
          {player.name.split(' ').map(n => n[0]).slice(0, 2).join('')}
        </span>
        {player.number && (
          <span className={styles.number}>#{player.number}</span>
        )}
      </div>
      <div className={styles.info}>
        <div className={styles.name}>{player.name}</div>
        <div className={styles.position} style={{ color: posColor }}>{player.position}</div>
        <div className={styles.nationality}>{player.nationality}</div>
        {player.note && (
          <div className={styles.note}>{player.note}</div>
        )}
        {isToConfirm && (
          <span className="badge badge-gray" style={{ marginTop: 6 }}>A confirmar</span>
        )}
      </div>
    </div>
  )
}

export default function PlayerSection({ players }) {
  if (!players?.length) return null

  const confirmed = players.filter(p => p.status === 'confirmado')
  const toConfirm = players.filter(p => p.status !== 'confirmado')

  return (
    <div className={styles.wrap}>
      {confirmed.length > 0 && (
        <>
          <h3 className={styles.subheading}>Elenco Confirmado</h3>
          <div className={styles.grid}>
            {confirmed.map((p, i) => <PlayerCard key={i} player={p} />)}
          </div>
        </>
      )}
      {toConfirm.length > 0 && (
        <>
          <h3 className={styles.subheading} style={{ marginTop: 24 }}>
            Especulações / A Confirmar
          </h3>
          <p className={styles.disclaimer}>
            Informações não verificadas. Checar em fonte oficial antes de tratar como fato.
          </p>
          <div className={styles.grid}>
            {toConfirm.map((p, i) => <PlayerCard key={i} player={p} />)}
          </div>
        </>
      )}
    </div>
  )
}
