import { RadialBarChart, RadialBar, ResponsiveContainer, PolarAngleAxis } from 'recharts'
import styles from './TitleProbability.module.css'

function GaugeCard({ label, probability, factors, disclaimer, color }) {
  const pct = Math.min(100, Math.max(0, probability))
  const data = [{ value: pct, fill: color }]

  return (
    <div className={`card ${styles.gaugeCard}`} style={{ borderColor: `${color}44` }}>
      <div className={styles.gaugeWrap}>
        <ResponsiveContainer width="100%" height={160}>
          <RadialBarChart
            cx="50%" cy="80%"
            innerRadius="60%" outerRadius="90%"
            startAngle={180} endAngle={0}
            data={data}
          >
            <PolarAngleAxis type="number" domain={[0, 100]} angleAxisId={0} tick={false} />
            <RadialBar dataKey="value" cornerRadius={6} background={{ fill: 'rgba(255,255,255,0.05)' }} />
          </RadialBarChart>
        </ResponsiveContainer>
        <div className={styles.pctLabel} style={{ color }}>
          {pct}%
        </div>
      </div>

      <div className={styles.title}>{label}</div>

      <div className={styles.factorsGrid}>
        {Object.entries(factors || {}).slice(0, 6).map(([k, v]) => (
          <div key={k} className={styles.factorItem}>
            <span className={styles.factorKey}>{k.replace(/_/g, ' ')}</span>
            <span className={styles.factorVal}>{typeof v === 'number' ? (Number.isInteger(v) ? v : `${v}%`) : v}</span>
          </div>
        ))}
      </div>

      <p className={styles.disclaimer}>{disclaimer}</p>
    </div>
  )
}

export default function TitleProbability({ titleProbability }) {
  const br = titleProbability?.brasileirao
  const lib = titleProbability?.libertadores

  if (!br && !lib) return null

  return (
    <div className={styles.grid}>
      {br && (
        <GaugeCard
          label="Brasileirão 2026"
          probability={br.probability}
          factors={br.factors}
          disclaimer={br.disclaimer}
          color="#E31D1C"
        />
      )}
      {lib && (
        <GaugeCard
          label="Copa Libertadores 2026"
          probability={lib.probability}
          factors={lib.factors}
          disclaimer={lib.disclaimer}
          color="#C89B3C"
        />
      )}
    </div>
  )
}
