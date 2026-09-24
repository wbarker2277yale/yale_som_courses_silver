import type { Course } from '../api'

/** One course, hung and labelled like a picture in the gallery. */
export default function CourseCard({ course }: { course: Course }) {
  const number = course['Course Number']
  const title = course['Course Title'] ?? 'Untitled course'
  const faculty = course['Faculty 1']
  const daytimes = course.Daytimes
  const room = course.Room
  const units = course.Units
  const category = course['Course Category']
  const description = course['Course Description']

  const legend =
    description && description.length > 190
      ? `${description.slice(0, 190).trimEnd()}…`
      : description

  return (
    <article className="frame">
      {number && <div className="number">{number}</div>}
      <h3>{title}</h3>
      {faculty && <p className="attribution">{faculty}</p>}

      <div className="placard">
        {daytimes && (
          <span>
            <strong>Meets</strong> {daytimes}
          </span>
        )}
        {room && (
          <span>
            <strong>Room</strong> {room}
          </span>
        )}
        {units && (
          <span>
            <strong>Units</strong> {units}
          </span>
        )}
      </div>

      {legend && <p className="legend">{legend}</p>}
      {category && <span className="category">{category}</span>}
    </article>
  )
}
