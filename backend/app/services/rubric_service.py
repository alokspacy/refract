"""Service evaluating content structure against universal design learning rubrics."""
from app.schemas.content import ContentDocument
from app.schemas.rubric import ComprehensionRubricReport, RubricCriterion

class RubricService:
    def evaluate_document(self, doc: ContentDocument) -> ComprehensionRubricReport:
        has_objectives = len(doc.learning_objectives) > 0
        has_glossary = len(doc.glossary) > 0
        section_count = len(doc.sections)

        criteria = [
            RubricCriterion(
                criterion_id="clarity",
                title="Objective Clarity",
                weight=0.35,
                score=4 if has_objectives else 2,
                feedback="Clear learning goals defined." if has_objectives else "Add explicit learning objectives."
            ),
            RubricCriterion(
                criterion_id="vocabulary",
                title="Vocabulary Scaffolding",
                weight=0.35,
                score=4 if has_glossary else 2,
                feedback="Glossary scaffolding present." if has_glossary else "Provide key term definitions."
            ),
            RubricCriterion(
                criterion_id="chunking",
                title="Structural Chunking",
                weight=0.30,
                score=4 if section_count >= 2 else 3,
                feedback="Content divided into digestible sections."
            )
        ]

        weighted_sum = sum(c.score * c.weight for c in criteria)
        mastery = "Exemplary" if weighted_sum >= 3.5 else ("Proficient" if weighted_sum >= 2.5 else "Developing")

        return ComprehensionRubricReport(
            document_id=doc.id,
            overall_score=round(weighted_sum, 2),
            mastery_level=mastery,
            criteria=criteria
        )
