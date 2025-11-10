const dateFormatter = new Intl.DateTimeFormat(undefined, {
  weekday: 'short',
  month: 'short',
  day: 'numeric',
})

const timeFormatter = new Intl.DateTimeFormat(undefined, {
  hour: '2-digit',
  minute: '2-digit',
})

export const formatDateRange = (startIso: string, endIso: string): string => {
  const start = new Date(startIso)
  const end = new Date(endIso)

  const sameDay =
    start.getFullYear() === end.getFullYear() &&
    start.getMonth() === end.getMonth() &&
    start.getDate() === end.getDate()

  const startLabel = `${dateFormatter.format(start)} · ${timeFormatter.format(start)}`
  const endLabel = sameDay
    ? timeFormatter.format(end)
    : `${dateFormatter.format(end)} · ${timeFormatter.format(end)}`

  return `${startLabel} – ${endLabel}`
}

export const toDateTimeLocalInput = (value?: string | null): string => {
  if (!value) {
    return ''
  }
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) {
    return ''
  }
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}T${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

export const fromDateTimeLocalInput = (value: string): string | undefined => {
  if (!value) {
    return undefined
  }
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) {
    return undefined
  }
  return date.toISOString()
}
