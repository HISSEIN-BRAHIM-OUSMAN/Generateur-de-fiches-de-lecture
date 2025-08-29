from pydantic import BaseModel, Field
from typing import List, Optional

class Citation(BaseModel):
    quote: str
    location: Optional[str] = None  # page/section

class FicheLecture(BaseModel):
    title: str = Field(..., description="Titre du document")
    author: Optional[str] = None
    source: Optional[str] = None
    date: Optional[str] = None
    thesis: str
    key_ideas: List[str]
    short_summary: str
    detailed_summary: str
    key_concepts: List[str]
    keywords: List[str]
    discussion_questions: List[str]
    difficulty: int = Field(ge=1, le=5)
    audience: Optional[str] = None
    highlights: List[Citation] = []