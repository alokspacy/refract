"""Schemas for Augmentative and Alternative Communication (AAC) symbol boards."""
from typing import List, Optional
from pydantic import BaseModel, Field

class AACSymbolCell(BaseModel):
    cell_id: str
    label: str
    speech_phrase: str
    category: str = Field(default="core", description="Fitzgerald key category: verb, noun, social, question")
    color_hex: str = "#dbeafe"
    icon_key: Optional[str] = None

class AACCommunicationBoard(BaseModel):
    board_id: str
    title: str
    grid_columns: int = Field(default=4, ge=2, le=8)
    cells: List[AACSymbolCell] = Field(default_factory=list)
