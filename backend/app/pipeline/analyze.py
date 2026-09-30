import logging
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.analysis import ContentAnalysis
from app.models.variant import ProviderUsage
from app.schemas.content import ContentDocument
from app.schemas.analysis import ContentAnalysisCreate
from app.providers.llm import LLMProvider, get_llm_provider
from app.prompts.analysis import (
    ANALYSIS_PROMPT_VERSION,
    ANALYSIS_SYSTEM_PROMPT,
    ANALYSIS_USER_TEMPLATE
)

logger = logging.getLogger("accesslearn.pipeline.analyze")


class ContentAnalyzer:
    """
    Analyzes normalized ContentDocument using an LLM to extract educational metadata:
    subject, grade level, language, complexity, learning objectives, concepts, and vocabulary.
    """

    def __init__(self, llm_provider: Optional[LLMProvider] = None):
        self.llm = llm_provider or get_llm_provider()

    def analyze_document(
        self,
        document: Document,
        db: Session,
        progress_callback: Optional[Any] = None
    ) -> ContentAnalysis:
        logger.info(f"Starting content analysis for document_id={document.id} ({document.original_filename})")
        
        if progress_callback:
            progress_callback("ANALYZING", 10.0)

        # 1. Check if analysis already exists
        existing_analysis = db.query(ContentAnalysis).filter(ContentAnalysis.document_id == document.id).first()
        if existing_analysis:
            logger.info(f"Existing analysis found for document_id={document.id}, reusing")
            if progress_callback:
                progress_callback("ANALYZING", 100.0)
            return existing_analysis

        # 2. Extract content blocks text from normalized_content
        raw_content = document.normalized_content or {}
        doc_title = raw_content.get("title", document.original_filename)
        sections = raw_content.get("sections", [])

        formatted_blocks: List[str] = []
        for sec in sections:
            for blk in sec.get("blocks", []):
                blk_id = blk.get("id", "unknown")
                blk_type = blk.get("type", "paragraph")
                text = (blk.get("source_text") or "").strip()
                if text:
                    formatted_blocks.append(f"[Block ID: {blk_id}] ({blk_type}): {text}")

        content_blocks_str = "\n\n".join(formatted_blocks[:60])  # Cap at top 60 blocks for analysis prompt
        if not content_blocks_str:
            content_blocks_str = f"[Block ID: blk_001] (paragraph): {document.original_filename}"

        # 3. Build Prompt
        user_prompt = ANALYSIS_USER_TEMPLATE.format(
            title=doc_title,
            content_blocks=content_blocks_str
        )

        if progress_callback:
            progress_callback("ANALYZING", 50.0)

        # 4. Invoke LLM Provider
        response = self.llm.generate(
            system_prompt=ANALYSIS_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            model=None,
            temperature=0.1
        )

        analysis_data = response.content_json

        # 5. Record API Usage
        usage = response.usage or {}
        usage_record = ProviderUsage(
            provider=response.provider,
            model=response.model,
            operation="content_analysis",
            prompt_tokens=usage.get("prompt_tokens", 0),
            completion_tokens=usage.get("completion_tokens", 0),
            total_tokens=usage.get("total_tokens", 0),
            estimated_cost_usd=usage.get("estimated_cost_usd", 0.0)
        )
        db.add(usage_record)

        # 6. Construct and save ContentAnalysis record
        analysis = ContentAnalysis(
            document_id=document.id,
            language=analysis_data.get("language", "en") or "en",
            subject=analysis_data.get("subject", "General Education"),
            grade_hint=str(analysis_data.get("grade_hint", "Standard")),
            complexity=analysis_data.get("complexity", "intermediate"),
            learning_objectives=analysis_data.get("learning_objectives", []),
            concepts=analysis_data.get("concepts", []),
            vocabulary=analysis_data.get("vocabulary", []),
            extra_metadata={
                "prompt_version": ANALYSIS_PROMPT_VERSION,
                "model": response.model,
                "provider": response.provider
            }
        )

        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        if progress_callback:
            progress_callback("ANALYZING", 100.0)

        logger.info(f"Content analysis completed for document_id={document.id}: subject={analysis.subject}, complexity={analysis.complexity}")
        return analysis
