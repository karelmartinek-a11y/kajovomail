export type EventListener = (data: Record<string, unknown>) => void

export const startEventStream = (
  onMessage: EventListener,
  onError?: (error: Event) => void,
  path = '/api/v1/events/ws'
) => {
  const stream = new EventSource(path, { withCredentials: true })

  stream.onmessage = (event) => {
    try {
      onMessage(JSON.parse(event.data))
    } catch (error) {
      console.warn('Unable to parse event payload', error)
    }
  }

  stream.onerror = (error) => {
    onError?.(error)
  }

  return () => stream.close()
}
