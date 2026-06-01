import styles from './InversionExplainer.module.css'

function VectorViz({ vec, label, color }) {
  if (!vec?.length) return null
  const max = Math.max(...vec)

  return (
    <div className={styles.vecWrap}>
      <div className={styles.vecLabel}>{label}</div>
      <div className={styles.vec}>
        {vec.map((v, i) => (
          <div key={i} className={styles.vecItem}>
            <div
              className={styles.bar}
              style={{
                height: `${(v / max) * 60}px`,
                background: color,
                opacity: 0.7 + (v / max) * 0.3,
              }}
            />
            <span className={styles.vecVal}>{v.toFixed(0)}</span>
            <span className={styles.vecIdx}>{i + 1}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

export default function InversionExplainer({ combined, brasileirao, libertadores }) {
  const combVec = combined?.difficulty_vector?.slice(0, 15) ?? []
  const brVec = brasileirao?.difficulty_vector?.slice(0, 12) ?? []
  const libVec = libertadores?.difficulty_vector ?? []

  return (
    <div className={styles.wrap}>
      <div className={styles.explanation}>
        <div className={styles.concept}>
          <h3 className={styles.h3}>O que é uma Inversão?</h3>
          <p>
            Dado um vetor de dificuldades <code className={styles.code}>[d₁, d₂, ..., dₙ]</code>, uma{' '}
            <strong>inversão</strong> é um par <code className={styles.code}>(i, j)</code> onde{' '}
            <code className={styles.code}>i &lt; j</code> mas{' '}
            <code className={styles.code}>dᵢ &gt; dⱼ</code> — ou seja, um jogo mais difícil aparece
            antes de um jogo mais fácil na sequência cronológica.
          </p>
          <p>
            O total de inversões mede o <strong>grau de irregularidade</strong> do calendário.
            Um valor alto indica que o Flamengo enfrentou muitos picos de dificuldade
            intercalados com jogos mais tranquilos, sem uma progressão ordenada.
          </p>
        </div>

        <div className={styles.algo}>
          <h3 className={styles.h3}>Dividir e Conquistar — O(n log n)</h3>
          <pre className={styles.code2}>{`sort_and_count(arr, left, right):
  if left >= right: return 0    # caso base

  mid = (left + right) / 2
  left_inv  = sort_and_count(arr, left, mid)
  right_inv = sort_and_count(arr, mid+1, right)
  cross_inv = merge_and_count(arr, left, mid, right)

  return left_inv + right_inv + cross_inv

merge_and_count(arr, left, mid, right):
  # Durante o merge de duas metades ordenadas:
  # Se arr[i] > arr[j] → todas as (mid - i + 1)
  # posições restantes na esquerda formam inversão com j
  inversões += (mid - i + 1)`}</pre>

          <div className={styles.complexity}>
            <div className={styles.cmpItem}>
              <span className={styles.cmpBad}>O(n²)</span>
              <span>Força Bruta</span>
            </div>
            <div className={styles.cmpArrow}>→</div>
            <div className={styles.cmpItem}>
              <span className={styles.cmpGood}>O(n log n)</span>
              <span>Sort-and-Count</span>
            </div>
          </div>
        </div>

        <div className={styles.interp}>
          <h3 className={styles.h3}>Interpretação</h3>
          <div className={styles.interpGrid}>
            {[
              ['0–20%', '🟢', 'Calendário ordenado (crescente em dificuldade)'],
              ['20–40%', '🟡', 'Leve irregularidade'],
              ['40–60%', '🟠', 'Calendário desequilibrado'],
              ['60–80%', '🔴', 'Muito irregular e pesado'],
              ['80–100%', '⚫', 'Sequência decrescente em dificuldade'],
            ].map(([range, icon, desc]) => (
              <div key={range} className={styles.interpItem}>
                <span className={styles.interpIcon}>{icon}</span>
                <strong className={styles.interpRange}>{range}</strong>
                <span className={styles.interpDesc}>{desc}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className={styles.vizSection}>
        <h3 className={styles.h3}>Vetor de Dificuldades (primeiros 15 jogos)</h3>
        <VectorViz vec={combVec} label="Temporada completa" color="#E31D1C" />
        <div className={styles.vizRow}>
          <VectorViz vec={brVec} label="Brasileirão" color="#E31D1C" />
          <VectorViz vec={libVec} label="Libertadores" color="#C89B3C" />
        </div>
      </div>
    </div>
  )
}
