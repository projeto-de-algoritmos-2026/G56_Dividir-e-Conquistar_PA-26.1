import styles from './Header.module.css'

export default function Header({ metadata }) {
  const generated = metadata?.generated_at
    ? new Date(metadata.generated_at).toLocaleString('pt-BR')
    : null

  return (
    <header className={styles.header}>
      <div className={styles.stripe} />
      <div className={styles.inner}>
        <div className={styles.crest}>
          <svg viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="Flamengo">
            <path d="M40 4 L72 20 L72 48 C72 62 57 74 40 78 C23 74 8 62 8 48 L8 20 Z" fill="#E31D1C" />
            <path d="M40 10 L66 24 L66 48 C66 59 53 70 40 73 C27 70 14 59 14 48 L14 24 Z" fill="#1a1a1a" />
            <text x="40" y="52" textAnchor="middle" fill="#E31D1C" fontSize="28" fontWeight="900" fontFamily="Inter,sans-serif">CRF</text>
          </svg>
        </div>

        <div className={styles.titles}>
          <h1 className={styles.title}>
            Flamengo <span className={styles.year}>2026</span>
          </h1>
          <p className={styles.subtitle}>
            Análise da Temporada via{' '}
            <strong>Contagem de Inversões</strong>
            {' '}— Dividir e Conquistar
          </p>
          <div className={styles.badges}>
            <span className="badge badge-red">Brasileirão Série A</span>
            <span className="badge badge-gold">Copa Libertadores</span>
            {metadata?.source && (
              <span className="badge badge-gray">Fonte: {metadata.source}</span>
            )}
          </div>
        </div>

        {generated && (
          <div className={styles.meta}>
            <span className={styles.metaLabel}>Atualizado em</span>
            <span className={styles.metaValue}>{generated}</span>
          </div>
        )}
      </div>
    </header>
  )
}
