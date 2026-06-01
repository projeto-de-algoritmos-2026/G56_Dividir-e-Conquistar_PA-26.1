import {
  ResponsiveContainer,
  ComposedChart,
  Bar,
  Cell,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceLine,
  Legend,
} from 'recharts'
import { fmtDate, difficultyColor, competitionLabel } from '../utils/formatters'
import styles from './DifficultyChart.module.css'

function CustomTooltip({ active, payload }) {
  if (!active || !payload?.length) return null
  const d = payload[0]?.payload
  return (
    <div className={styles.tooltip}>
      <div className={styles.ttDate}>{fmtDate(d.date)}</div>
      <div className={styles.ttOpp}>vs {d.opponent}</div>
      <div className={styles.ttComp}>{competitionLabel(d.competition)}</div>
      <div className={styles.ttResult} data-result={d.result}>
        {d.result} {d.gf !== '' ? `${d.gf}–${d.ga}` : ''}
      </div>
      <div className={styles.ttDiff}>
        <span>Dificuldade:</span>
        <strong style={{ color: difficultyColor(d.difficulty) }}>
          {parseFloat(d.difficulty).toFixed(1)}
        </strong>
      </div>
    </div>
  )
}

export default function DifficultyChart({ matches }) {
  if (!matches?.length) return null

  const avg = matches.reduce((s, m) => s + parseFloat(m.difficulty || 0), 0) / matches.length

  const chartData = matches.map((m, i) => ({
    ...m,
    idx: i + 1,
    difficulty: parseFloat(m.difficulty || 0),
    isLibertadores: m.competition?.toLowerCase().includes('libertadores'),
  }))

  return (
    <div className={styles.wrap}>
      <ResponsiveContainer width="100%" height={320}>
        <ComposedChart data={chartData} margin={{ top: 8, right: 16, bottom: 8, left: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
          <XAxis
            dataKey="idx"
            tick={{ fill: '#888', fontSize: 11 }}
            label={{ value: 'Jogo nº', position: 'insideBottomRight', offset: -4, fill: '#888', fontSize: 11 }}
          />
          <YAxis
            domain={[0, 22]}
            tick={{ fill: '#888', fontSize: 11 }}
            label={{ value: 'Dificuldade', angle: -90, position: 'insideLeft', fill: '#888', fontSize: 11, offset: 10 }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend
            wrapperStyle={{ fontSize: 12, color: '#aaa', paddingTop: 12 }}
            formatter={(value) => value === 'difficulty' ? 'Dificuldade' : value}
          />
          <ReferenceLine
            y={avg}
            stroke="rgba(200,155,60,0.7)"
            strokeDasharray="6 3"
            label={{ value: `Média: ${avg.toFixed(1)}`, fill: '#C89B3C', fontSize: 11, position: 'right' }}
          />
          <Bar dataKey="difficulty" name="Dificuldade" radius={[4, 4, 0, 0]}>
            {chartData.map((entry) => (
              <Cell
                key={`cell-${entry.idx}`}
                fill={entry.isLibertadores ? '#C89B3C' : '#E31D1C'}
              />
            ))}
          </Bar>
          <Line
            type="monotone"
            dataKey="difficulty"
            stroke="rgba(255,255,255,0.3)"
            strokeWidth={1.5}
            dot={false}
            name=" "
          />
        </ComposedChart>
      </ResponsiveContainer>
      <div className={styles.legend}>
        <span><span className={styles.dotRed} />Brasileirão</span>
        <span><span className={styles.dotGold} />Libertadores</span>
        <span><span className={styles.dotLine} />Média</span>
      </div>
    </div>
  )
}
