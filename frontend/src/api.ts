// Render supplies VITE_API_URL at build time; the fallback keeps `npm run dev` working.
const API_BASE = (import.meta.env.VITE_API_URL ?? 'http://127.0.0.1:8000').replace(/\/$/, '')

export interface Course {
  'Course ID'?: string
  'Course Number'?: string
  'Course Title'?: string
  'Course Category'?: string
  'Course Type'?: string
  'Course Description'?: string
  'Faculty 1'?: string
  'Faculty 1 Email'?: string
  faculty_bio?: string
  Daytimes?: string
  Room?: string
  Section?: string
  Units?: string
  'Course Session'?: string
  Syllabus?: string
  [key: string]: unknown
}

export interface CoursesResponse {
  count: number
  courses: Course[]
}

export interface ChatResponse {
  reply: string
  tools_used: string[]
}

async function asJson<T>(response: Response): Promise<T> {
  if (!response.ok) {
    throw new Error(`${response.status} ${response.statusText}`)
  }
  return (await response.json()) as T
}

export async function fetchCourses(query?: string): Promise<CoursesResponse> {
  const url = new URL('/api/courses', API_BASE)
  if (query) {
    url.searchParams.set('q', query)
  }
  return asJson<CoursesResponse>(await fetch(url.toString()))
}

export async function sendChat(message: string): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  })
  return asJson<ChatResponse>(response)
}
