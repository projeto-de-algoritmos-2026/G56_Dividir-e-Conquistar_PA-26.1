import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from 'recharts'
import styles from './WindowAnalysis.module.css'

export default function WindowAnalysis({ monthlyWindows }) {
  if (!monthlyWindows?.length) return null

  return (
    <div className={styles.wrap}>
      <div className={styles.chartWrap}>
        <ResponsiveContainer width="100%" height={220}>
          <AreaChart data={monthlyWindows} margin={{ top: 8, right: 16, bottom: 8, left: 0 }}>
            <defs>
              <linearGradient id="gradDiff" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#E31D1C" stopOpacity={0.4} />
                <stop offset="95%" stopColor="#E31D1C" stopOpacity={0.02} />
              </linearGradient>
              <linearGradient id="gradInv" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#C89B3C" stopOpacity={0.4} />
                <stop offset="95%" stopColor="#C89B3C" stopOpacity={0.02} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
            <XAxis dataKey="label" tick={{ fill: '#aaa', fontSize: 12 }} />
            <YAxis yAxisId="left" domain={[0, 20]} tick={{ fill: '#888', fontSize: 11 }} />
            <YAxis yAxisId="right" orientation="right" domain={[0, 100]} tick={{ fill: '#888', fontSize: 11 }} unit="%" />
            <Tooltip
              contentStyle={{ background: '#1a1a1a', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 8 }}
              labelStyle={{ color: '#fff', fontWeight: 600 }}
              itemStyle={{ color: '#aaa' }}
            />
            <Area
              yAxisId="left"
              type="monotone"
              dataKey="avg_difficulty"
              stroke="#E31D1C"
              strokeWidth={2}
              fill="url(#gradDiff)"
              name="Dif. média"
            />
            <Area
              yAxisId="right"
              type="monotone"
              dataKey="inversion_percentage"
              stroke="#C89B3C"
              strokeWidth={2}
              fill="url(#gradInv)"
              name="Desordem %"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      <div className={styles.cards}>
        {monthlyWindows.map(w => (
          <div key={w.month} className={styles.card}>
            <div className={styles.month}>{w.label}</div>
            <div className={styles.stats}>
              <div>
                <span className={styles.statVal}>{w.matches_count}</span>
                <span className={styles.statLabel}>jogos</span>
              </div>
              <div>
                <span className={styles.statVal} style={{ color: '#E31D1C' }}>{w.avg_difficulty}</span>
                <span className={styles.statLabel}>dif. média</span>
              </div>
              <div>
                <span className={styles.statVal} style={{ color: '#C89B3C' }}>{w.inversion_percentage}%</span>
                <span className={styles.statLabel}>desordem</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
