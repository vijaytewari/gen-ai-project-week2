from typing import Literal
from pydantic import BaseModel, Field


class Change(BaseModel):
    field_id: str
    value: str = Field(max_length=4000)
    status: Literal["present", "blank", "missing", "unreadable", "not_applicable"] = "present"


class SaveRequest(BaseModel):
    revision: int = Field(ge=1)
    changes: list[Change] = Field(max_length=1000)
    actor: str = Field(default="Reviewer", min_length=1, max_length=100)


class ReviewRequest(BaseModel):
    revision: int = Field(ge=1)
    group: str
    reason: str = Field(default="", max_length=1000)


class Question(BaseModel):
    query: str = Field(min_length=1, max_length=1000)
    strategy: Literal["fixed", "semantic"] = "semantic"
    rerank: bool = True
    revision: int = Field(ge=1)
