export function fmtDate(dateStr) {
  if (!dateStr) return '—'
  const [y, m, d] = dateStr.split('-')
  return `${d}/${m}/${y}`
}

export function fmtResult(result, gf, ga) {
  if (!result) return '—'
  const score = (gf !== '' && ga !== '') ? ` ${gf}–${ga}` : ''
  return `${result}${score}`
}

export function fmtDifficulty(val) {
  const n = parseFloat(val)
  if (isNaN(n)) return '—'
  return n.toFixed(1)
}

export function difficultyColor(val) {
  const n = parseFloat(val)
  if (isNaN(n)) return '#888'
  if (n >= 16) return '#FF3B3A'
  if (n >= 12) return '#F97316'
  if (n >= 8) return '#F59E0B'
  if (n >= 5) return '#84CC16'
  return '#22C55E'
}

export function competitionLabel(comp) {
  if (!comp) return '—'
  if (comp.toLowerCase().includes('libertadores')) return 'Libertadores'
  if (comp.toLowerCase().includes('brasileir') || comp.toLowerCase().includes('serie a')) return 'Brasileirão'
  return comp
}

export function venueLabel(venue) {
  const v = (venue || '').toUpperCase()
  if (v === 'H') return 'Casa'
  if (v === 'A') return 'Fora'
  if (v === 'N') return 'Neutro'
  return venue
}
