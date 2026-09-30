import logging
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from app.workers.celery_app import celery_app
from app.db.database import SessionLocal
from app.models.document import Document
from app.models.job import ProcessingJob
from app.models.analysis import ContentAnalysis
from app.models.variant import GeneratedVariant
from app.storage.factory import get_storage_provider
from app.services.extraction_service import ExtractionService
from app.providers.ocr import get_ocr_provider
from app.providers.storage import StorageProvider
from app.pipeline.analyze import ContentAnalyzer
from app.pipeline.planner import AccessibilityPlanner
from app.pipeline.transform import TransformationEngine
from app.pipeline.validate import ContentValidator

logger = logging.getLogger("accesslearn.worker")


@celery_app.task(name="app.workers.tasks.process_document_job", bind=True)
def process_document_job(
    self,
    job_id: str,
    document_id: str,
    db_override: Optional[Session] = None,
    storage_override: Optional[StorageProvider] = None
):
    """
    Phase 2 Document Extraction & Normalization task.
    Pipeline: UPLOAD -> VALIDATE -> EXTRACT (25%) -> OCR (50% if needed) -> NORMALIZE (75%) -> COMPLETED (100%).
    """
    logger.info(f"Starting Phase 2 processing for job={job_id}, document={document_id}")
    db = db_override if db_override is not None else SessionLocal()
    should_close_db = db_override is None
    
    try:
        job = db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
        doc = db.query(Document).filter(Document.id == document_id).first()

        if not job or not doc:
            logger.error(f"Job or Document not found: job_id={job_id}, doc_id={document_id}")
            return {"status": "error", "message": "Job or document not found"}

        def update_progress(stage: str, progress_val: float):
            try:
                job.status = "PROCESSING" if progress_val < 100 else "COMPLETED"
                job.current_stage = stage
                job.progress = float(progress_val)
                db.commit()
            except Exception as commit_err:
                logger.warning(f"Failed to update job progress in DB: {commit_err}")

        storage = storage_override if storage_override is not None else get_storage_provider()
        ocr_provider = get_ocr_provider()
        extraction_service = ExtractionService(storage=storage, ocr_provider=ocr_provider)

        content_doc = extraction_service.process_document(
            document=doc,
            db=db,
            progress_callback=update_progress
        )

        logger.info(f"Phase 2 processing completed for job={job_id}, doc={document_id}")
        return {
            "status": "success",
            "job_id": job_id,
            "document_id": document_id,
            "sections_count": len(content_doc.sections)
        }

    except Exception as e:
        logger.exception(f"Error processing job={job_id}: {str(e)}")
        db.rollback()
        job = db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
        doc = db.query(Document).filter(Document.id == document_id).first()
        if job:
            job.status = "FAILED"
            job.error_message = str(e)
            db.commit()
        if doc:
            doc.status = "FAILED"
            doc.extraction_status = "FAILED"
            db.commit()
        raise e
    finally:
        if should_close_db:
            db.close()


@celery_app.task(name="app.workers.tasks.analyze_document_job", bind=True)
def analyze_document_job(
    self,
    job_id: str,
    document_id: str,
    db_override: Optional[Session] = None
):
    """
    Phase 3 Content Analysis task.
    Pipeline: LOAD -> ANALYZE WITH LLM -> EXTRACT OBJECTIVES/CONCEPTS/VOCABULARY -> COMPLETED.
    """
    logger.info(f"Starting Phase 3 analysis for job={job_id}, document={document_id}")
    db = db_override if db_override is not None else SessionLocal()
    should_close_db = db_override is None

    try:
        job = db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
        doc = db.query(Document).filter(Document.id == document_id).first()

        if not job or not doc:
            return {"status": "error", "message": "Job or document not found"}

        def update_progress(stage: str, progress_val: float):
            try:
                job.status = "PROCESSING" if progress_val < 100 else "COMPLETED"
                job.current_stage = stage
                job.progress = float(progress_val)
                db.commit()
            except Exception as commit_err:
                logger.warning(f"Failed to update job progress in DB: {commit_err}")

        analyzer = ContentAnalyzer()
        analysis = analyzer.analyze_document(document=doc, db=db, progress_callback=update_progress)

        return {
            "status": "success",
            "job_id": job_id,
            "document_id": document_id,
            "subject": analysis.subject,
            "objectives_count": len(analysis.learning_objectives)
        }

    except Exception as e:
        logger.exception(f"Error in analysis job={job_id}: {str(e)}")
        db.rollback()
        job = db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
        if job:
            job.status = "FAILED"
            job.error_message = str(e)
            db.commit()
        raise e
    finally:
        if should_close_db:
            db.close()


@celery_app.task(name="app.workers.tasks.generate_variant_job", bind=True)
def generate_variant_job(
    self,
    job_id: str,
    document_id: str,
    variant_id: str,
    profile_ids: List[str],
    metadata_overrides: Optional[Dict[str, Any]] = None,
    db_override: Optional[Session] = None
):
    """
    Phase 3 Accessible Variant Generation task.
    Pipeline: CONTENT JSON -> ANALYZING (20%) -> PLANNING (35%) -> TRANSFORMING (70%) -> VALIDATING (90%) -> COMPLETED (100%).
    """
    logger.info(f"Starting Phase 3 variant generation for job={job_id}, variant={variant_id}, profiles={profile_ids}")
    db = db_override if db_override is not None else SessionLocal()
    should_close_db = db_override is None

    try:
        job = db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
        doc = db.query(Document).filter(Document.id == document_id).first()
        variant = db.query(GeneratedVariant).filter(GeneratedVariant.id == variant_id).first()

        if not job or not doc or not variant:
            return {"status": "error", "message": "Job, document, or variant not found"}

        def update_progress(stage: str, progress_val: float):
            try:
                job.status = "PROCESSING" if progress_val < 100 else "COMPLETED"
                job.current_stage = stage
                job.progress = float(progress_val)
                db.commit()
            except Exception as commit_err:
                logger.warning(f"Failed to update job progress in DB: {commit_err}")

        # 1. Content Analysis (Run or retrieve existing)
        analyzer = ContentAnalyzer()
        update_progress("ANALYZING", 10.0)
        analysis = analyzer.analyze_document(document=doc, db=db)
        update_progress("PLANNING", 25.0)

        # 2. Accessibility Planner
        planner = AccessibilityPlanner()
        plan = planner.create_plan(
            document_id=doc.id,
            normalized_content=doc.normalized_content or {},
            analysis=analysis,
            profile_ids=profile_ids
        )
        update_progress("PLANNING", 35.0)

        # 3. Transformation Engine
        transformer = TransformationEngine()
        generated_blocks = transformer.transform_variant(
            variant=variant,
            document=doc,
            analysis=analysis,
            plan=plan,
            db=db,
            progress_callback=update_progress
        )

        # 4. Validation Engine
        validator = ContentValidator()
        val_result = validator.validate_variant(
            variant=variant,
            document=doc,
            generated_blocks=generated_blocks,
            db=db,
            progress_callback=update_progress
        )

        logger.info(f"Phase 3 variant generation finished for variant_id={variant.id}")
        return {
            "status": "success",
            "job_id": job_id,
            "variant_id": variant_id,
            "blocks_count": len(generated_blocks),
            "is_valid": val_result.is_valid,
            "grounded": val_result.grounded
        }

    except Exception as e:
        logger.exception(f"Error in variant generation job={job_id}: {str(e)}")
        db.rollback()
        job = db.query(ProcessingJob).filter(ProcessingJob.id == job_id).first()
        variant = db.query(GeneratedVariant).filter(GeneratedVariant.id == variant_id).first()
        if job:
            job.status = "FAILED"
            job.error_message = str(e)
            db.commit()
        if variant:
            variant.status = "FAILED"
            db.commit()
        raise e
    finally:
        if should_close_db:
            db.close()
