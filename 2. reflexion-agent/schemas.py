from typing import List

from pydantic import BaseModel, Field

class Reflection(BaseModel):
    missing: str = Field(description="Critique of what is missing.")
    superfluous: str = Field(description="Critique of what is superfluous.")


class AnswerQuestion(BaseModel):
    """Tool for answering questions with structured reflection and search recommendations."""
    answer: str = Field(description="~250 words detailed answer to the question.")
    reflection: Reflection = Field(description="Your reflection on the initial answer with missing and superfluous critiques.")
    search_queries: List[str] = Field(
        description="SEPARATE list of 1-3 search queries for researching improvements. This is NOT part of reflection."
    )

class RevisedAnswer(AnswerQuestion):
    references: List[str] = Field(
        description="Citations supporting your updated answer."
    )