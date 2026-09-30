from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class LearningObjectiveItem(BaseModel):
    id: str = Field(..., description="Unique objective identifier")
    text: str = Field(..., description="Objective description")
    inferred: bool = Field(False, description="Whether objective was inferred from context")


class ConceptItem(BaseModel):
    id: str = Field(..., description="Unique concept identifier")
    name: str = Field(..., description="Concept name/title")
    description: str = Field(..., description="Concept definition or explanation")
    source_block_ids: List[str] = Field(default_factory=list, description="Traceable source block references")


class VocabularyItem(BaseModel):
    term: str = Field(..., description="Academic term")
    definition: str = Field(..., description="Clear definition grounded in source")
    example: Optional[str] = Field(None, description="Illustrative example where supported")
    source_block_ids: List[str] = Field(default_factory=list, description="Traceable source block references")


class ContentAnalysisCreate(BaseModel):
    document_id: str
    language: str = Field("en", description="Detected language code")
    subject: Optional[str] = Field(None, description="Detected academic subject")
    grade_hint: Optional[str] = Field(None, description="Estimated grade level")
    complexity: str = Field("intermediate", description="Reading complexity level")
    learning_objectives: List[LearningObjectiveItem] = Field(default_factory=list)
    concepts: List[ConceptItem] = Field(default_factory=list)
    vocabulary: List[VocabularyItem] = Field(default_factory=list)
    extra_metadata: Dict[str, Any] = Field(default_factory=dict)


class ContentAnalysisResponse(BaseModel):
    id: str
    document_id: str
    language: str
    subject: Optional[str] = None
    grade_hint: Optional[str] = None
    complexity: str
    learning_objectives: List[LearningObjectiveItem] = Field(default_factory=list)
    concepts: List[ConceptItem] = Field(default_factory=list)
    vocabulary: List[VocabularyItem] = Field(default_factory=list)
    extra_metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
