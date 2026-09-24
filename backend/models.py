"""Pydantic data objects shared by tools.py and agent.py."""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Course(BaseModel):
    """One row of data/yale_som_classes.json.

    The JSON uses spaced, title-cased keys ("Course Title"), so every field is
    declared with its raw key as an alias and a snake_case Python name.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    course_id: str | None = Field(default=None, alias="Course ID")
    course_number: str | None = Field(default=None, alias="Course Number")
    title: str | None = Field(default=None, alias="Course Title")
    category: str | None = Field(default=None, alias="Course Category")
    course_type: str | None = Field(default=None, alias="Course Type")
    section: str | None = Field(default=None, alias="Section")
    units: str | None = Field(default=None, alias="Units")

    description: str | None = Field(default=None, alias="Course Description")
    syllabus: str | None = Field(default=None, alias="Syllabus")
    old_syllabus: str | None = Field(default=None, alias="Old Syllabus")

    faculty: str | None = Field(default=None, alias="Faculty 1")
    faculty_email: str | None = Field(default=None, alias="Faculty 1 Email")
    faculty_bio: str | None = Field(default=None, alias="faculty_bio")

    daytimes: str | None = Field(default=None, alias="Daytimes")
    timings_day: Any | None = Field(default=None, alias="Timings Day")
    start_time: Any | None = Field(default=None, alias="Timings StartTime")
    end_time: Any | None = Field(default=None, alias="Timings EndTime")
    room: str | None = Field(default=None, alias="Room")

    session: str | None = Field(default=None, alias="Course Session")
    session_start: str | None = Field(default=None, alias="Course Session Start date")
    session_end: str | None = Field(default=None, alias="Course Session End Date")
    term_code: Any | None = Field(default=None, alias="TermCode")

    bid_or_permission: Any | None = Field(default=None, alias="Bid Or Permission")
    visible: Any | None = Field(default=None, alias="Visible")

    def summary(self) -> str:
        """Compact one-line form used in tool results and audit entries."""
        bits = [self.course_number, self.title, self.faculty, self.daytimes]
        return " | ".join(b for b in bits if b)


class CourseHit(BaseModel):
    """A single search result: the course plus why it matched."""

    course: Course
    matched_on: list[str] = Field(default_factory=list)


class SearchResult(BaseModel):
    """Return type of the search_courses tool."""

    query: str
    count: int
    truncated: bool = False
    hits: list[CourseHit] = Field(default_factory=list)


class AgentResult(BaseModel):
    """What run_agent hands back to main.py."""

    reply: str
    tools_used: list[str] = Field(default_factory=list)
