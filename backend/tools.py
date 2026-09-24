"""The two agent tools: search_courses (local JSON) and web_search (OpenAI native)."""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from pydantic_ai import WebSearchTool

from models import Course, CourseHit, SearchResult

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA_PATH = ROOT / "data" / "yale_som_classes.json"

MAX_RESULTS = 15

# Fields searched by search_courses, mapped to the label reported in `matched_on`.
SEARCHABLE: dict[str, str] = {
    "title": "title",
    "course_number": "number",
    "course_id": "id",
    "faculty": "faculty",
    "faculty_bio": "faculty_bio",
    "category": "category",
    "course_type": "type",
    "daytimes": "day/time",
    "room": "room",
    "session": "session",
    "description": "description",
}


@lru_cache(maxsize=1)
def load_courses() -> list[Course]:
    """Parse the course JSON once and keep it in memory."""
    rows = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    return [Course.model_validate(row) for row in rows]


def _field_text(course: Course, field: str) -> str:
    value = getattr(course, field, None)
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        return " ".join(str(v) for v in value)
    return str(value)


def search_courses(query: str, limit: int = MAX_RESULTS) -> SearchResult:
    """Search the Yale SOM course catalog.

    Matches the query against course title, number, faculty name and bio,
    category, type, meeting day/time, room, session and description. Every term
    in the query must appear somewhere in the course for it to match.

    Args:
        query: What to look for, e.g. "Rodrigo", "accounting", "Tuesday", "MGT 656".
        limit: Maximum number of courses to return (capped at 15).

    Returns:
        The matching courses, each with the fields that matched.
    """
    limit = max(1, min(limit, MAX_RESULTS))
    terms = [t for t in query.lower().split() if t]
    courses = load_courses()

    if not terms:
        hits = [CourseHit(course=c, matched_on=[]) for c in courses[:limit]]
        return SearchResult(
            query=query,
            count=len(courses),
            truncated=len(courses) > limit,
            hits=hits,
        )

    matches: list[CourseHit] = []
    for course in courses:
        haystacks = {
            label: _field_text(course, field).lower()
            for field, label in SEARCHABLE.items()
        }
        blob = " ".join(haystacks.values())
        if not all(term in blob for term in terms):
            continue
        matched_on = sorted(
            {
                label
                for label, text in haystacks.items()
                if any(term in text for term in terms)
            }
        )
        matches.append(CourseHit(course=course, matched_on=matched_on))

    return SearchResult(
        query=query,
        count=len(matches),
        truncated=len(matches) > limit,
        hits=matches[:limit],
    )


def build_web_search_tool() -> WebSearchTool:
    """OpenAI's native web search, run server-side via the Responses endpoint.

    Deliberately not DuckDuckGo or any other scraped search: the model calls
    OpenAI's own hosted tool as part of the same Responses request.
    """
    return WebSearchTool(search_context_size="medium")
