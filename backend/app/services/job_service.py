import logging
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.job import ProcessingJob
from app.models.user import User

logger = logging.getLogger("accesslearn.jobs")


class JobService:
    @staticmethod
    def get_job(db: Session, user: User, job_id: str) -> ProcessingJob:
        job = db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "JOB_NOT_FOUND", "message": "Processing job not found."}
            )

        # Check document ownership
        doc = db.query(Document).filter(Document.id == job.document_id).first()
        if not doc or doc.owner_id != user.id:
            logger.warning(f"Unauthorized job access attempt: job={job_id} by user={user.id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "FORBIDDEN", "message": "You do not have permission to access this processing job."}
            )

        return job
