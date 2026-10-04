"""FastAPI router for comprehension checks and self-quizzes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.document import Document
from app.schemas.content import ContentDocument
from app.schemas.quiz import ComprehensionQuiz
from app.services.quiz_service import QuizService

router = APIRouter(prefix="/quiz", tags=["Comprehension Quiz"])
service = QuizService()

@router.get("/documents/{document_id}", response_model=ComprehensionQuiz)
def get_document_quiz(document_id: str, db: Session = Depends(get_db)):
    """Generate or fetch self-paced comprehension check questions."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc or not doc.normalized_content:
        raise HTTPException(status_code=404, detail="Document not found")
    cd = ContentDocument.model_validate(doc.normalized_content)
    return service.generate_quiz(cd)
