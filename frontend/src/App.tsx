import { useEffect, useState } from 'react'
import { fetchCourses, type Course } from './api'
import CourseCard from './components/CourseCard'
import ChatPanel from './components/ChatPanel'
import { Anthemion, FretBand, SaucerDome } from './components/Ornament'

export default function App() {
  const [courses, setCourses] = useState<Course[]>([])
  const [count, setCount] = useState(0)
  const [draft, setDraft] = useState('')
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(true)
  const [fault, setFault] = useState<string | null>(null)

  useEffect(() => {
    let live = true
    setLoading(true)
    setFault(null)

    fetchCourses(query)
      .then((data) => {
        if (!live) return
        setCourses(data.courses)
        setCount(data.count)
      })
      .catch((error: unknown) => {
        if (!live) return
        setFault(
          error instanceof Error
            ? `Could not reach the catalogue: ${error.message}. Is the backend running on port 8000?`
            : 'Could not reach the catalogue.',
        )
        setCourses([])
        setCount(0)
      })
      .finally(() => {
        if (live) setLoading(false)
      })

    return () => {
      live = false
    }
  }, [query])

  return (
    <div className="plan">
      <header className="vestibule">
        <SaucerDome />
        <div className="frontispiece">
          <h1>Yale SOM Course Explorer</h1>
          <p className="subtitle">A top-lit gallery of the catalogue</p>
        </div>
        <FretBand />
      </header>

      <div className="rooms">
        <section>
          <div className="room-label">
            <span>The Catalogue</span>
            <span className="tally">
              {loading ? 'Hanging…' : `${count} course${count === 1 ? '' : 's'}`}
            </span>
          </div>

          <form
            className="search"
            onSubmit={(event) => {
              event.preventDefault()
              setQuery(draft.trim())
            }}
          >
            <input
              value={draft}
              onChange={(event) => setDraft(event.target.value)}
              placeholder="Search titles, faculty, categories, days…"
              aria-label="Search courses"
            />
            <button type="submit">Search</button>
          </form>

          {fault && <div className="fault">{fault}</div>}

          {!fault && !loading && courses.length === 0 && (
            <p className="empty" style={{ color: 'var(--umber-soft)' }}>
              Nothing hung under that title. Try a broader search.
            </p>
          )}

          <div className="hang">
            {courses.map((course, index) => (
              <CourseCard
                key={(course['Course ID'] as string) ?? index}
                course={course}
              />
            ))}
          </div>
        </section>

        <ChatPanel />
      </div>

      <footer className="colophon">
        <Anthemion />
        <p>After Sir John Soane · Dulwich Picture Gallery · 1817</p>
      </footer>
    </div>
  )
}
