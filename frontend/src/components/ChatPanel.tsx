import { useEffect, useRef, useState } from 'react'
import { sendChat } from '../api'

interface Turn {
  role: 'visitor' | 'attendant'
  text: string
  tools?: string[]
}

/** The attendant's desk: ask a question, watch the lamps, read the reply. */
export default function ChatPanel() {
  const [turns, setTurns] = useState<Turn[]>([])
  const [draft, setDraft] = useState('')
  const [busy, setBusy] = useState(false)
  const [fault, setFault] = useState<string | null>(null)
  const scrollRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight })
  }, [turns, busy])

  async function ask(event: React.FormEvent) {
    event.preventDefault()
    const message = draft.trim()
    if (!message || busy) return

    setTurns((prev) => [...prev, { role: 'visitor', text: message }])
    setDraft('')
    setFault(null)
    setBusy(true)

    try {
      const answer = await sendChat(message)
      setTurns((prev) => [
        ...prev,
        { role: 'attendant', text: answer.reply, tools: answer.tools_used },
      ])
    } catch (error) {
      setFault(
        error instanceof Error
          ? `The desk did not answer: ${error.message}`
          : 'The desk did not answer.',
      )
    } finally {
      setBusy(false)
    }
  }

  return (
    <section className="cabinet">
      <div className="room-label">
        <span>Enquiries</span>
        <span className="tally">Attendant</span>
      </div>

      <div className="scroll" ref={scrollRef}>
        {turns.length === 0 && !busy && (
          <p className="empty">
            Ask about a course, an instructor, or when something meets.
          </p>
        )}

        {turns.map((turn, index) => (
          <div className={`utterance ${turn.role}`} key={index}>
            <span className="who">
              {turn.role === 'visitor' ? 'You' : 'Attendant'}
            </span>
            <div className="body">{turn.text}</div>
            {turn.tools && turn.tools.length > 0 && (
              <div className="tools">
                {turn.tools.map((tool) => (
                  <code key={tool}>{tool}</code>
                ))}
              </div>
            )}
          </div>
        ))}

        {busy && (
          <div className="thinking">
            <i />
            <i />
            <i />
            <span>Consulting the catalogue</span>
          </div>
        )}

        {fault && <div className="fault">{fault}</div>}
      </div>

      <form className="ask" onSubmit={ask}>
        <input
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
          placeholder="Which courses meet on Tuesdays?"
          aria-label="Ask the attendant"
          disabled={busy}
        />
        <button type="submit" disabled={busy || draft.trim().length === 0}>
          Ask
        </button>
      </form>
    </section>
  )
}
