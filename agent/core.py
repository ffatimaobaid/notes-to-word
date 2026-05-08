"""
Agent Core — The Notes2Doc Autonomous Agent Orchestrator

Implements a Goal-Based Agent that follows the agentic loop:
    Observe → Interpret → Decide → Act → Learn

The agent autonomously:
1. Perceives image quality and content
2. Decides optimal processing strategy
3. Executes multi-pass transcription
4. Generates formatted Word documents
5. Learns from user feedback

Architecture: Goal-Based Agent
Justification: The agent has a clear goal (produce the best possible document)
and uses internal state + perception to select actions that achieve this goal.
"""

from datetime import datetime
from PIL import Image

from agent.memory import (
    ShortTermMemory,
    _load_long_term_memory,
    save_long_term_memory,
    add_conversion_record,
)
from agent.perception import (
    analyze_image_quality,
    detect_content_type,
    get_preprocessing_recommendations,
)
from agent.decision import (
    select_strategy,
    evaluate_result_confidence,
    ethical_decision_check,
)
from agent.actions import (
    preprocess_image,
    transcribe_image,
    enhance_transcription,
    generate_word_document,
)
from agent.learning import record_user_feedback, get_learning_summary
from ethics.transparency import log_agent_action, get_audit_trail
from ethics.privacy import check_data_handling_compliance


class NotesAgent:
    """
    The Notes2Doc Autonomous Agent.
    
    Agent Type: Goal-Based Agent
    Goal: Produce the highest quality document from handwritten notes
    
    Capabilities:
    - Perception: Image quality analysis, content type detection
    - Decision: Strategy selection, ethical compliance checks
    - Action: Multi-pass transcription, document generation
    - Learning: Feedback-driven preference adaptation
    - Memory: Short-term (session) + Long-term (persistent)
    """

    def __init__(self):
        self.stm = ShortTermMemory()
        self.ltm = _load_long_term_memory()
        self.agent_state = "idle"
        self.autonomy_level = "semi"  # semi | full

    def reset(self):
        """Reset agent for a new task."""
        self.stm.reset()
        self.agent_state = "idle"

    # ──────────────────────────────────────────────
    # PHASE 1: OBSERVE
    # ──────────────────────────────────────────────

    def observe(self, image: Image.Image) -> dict:
        """
        Perception phase: Analyze the input image.
        Returns perception results with quality metrics and content detection.
        """
        self.agent_state = "observing"
        self.stm.current_image = image
        self.stm.processing_start_time = datetime.now()

        self.stm.log_thought("observe", "Received new image for processing. Beginning analysis...")

        # Analyze image quality
        quality = analyze_image_quality(image)
        self.stm.log_thought(
            "observe",
            f"Image quality: {quality['quality_label']} ({quality['overall_score']}/100)"
        )

        # Detect content type
        content_type = detect_content_type(image)
        self.stm.log_thought(
            "observe",
            f"Content type detected: {content_type['primary_type']} "
            f"(confidence: {content_type['confidence']:.0%})"
        )

        # Get preprocessing recommendations
        recommendations = get_preprocessing_recommendations(quality)
        actions_needed = [r["action"] for r in recommendations if r["action"] != "none"]
        if actions_needed:
            self.stm.log_thought(
                "observe",
                f"Preprocessing recommended: {', '.join(actions_needed)}"
            )
        else:
            self.stm.log_thought("observe", "No preprocessing needed — image quality sufficient.")

        # Store in short-term memory
        self.stm.perception_results = {
            "quality": quality,
            "content_type": content_type,
            "recommendations": recommendations,
        }

        # Log action for audit
        log_agent_action("observe", "Image analysis completed", {
            "quality_score": quality["overall_score"],
            "content_type": content_type["primary_type"],
        })

        return self.stm.perception_results

    # ──────────────────────────────────────────────
    # PHASE 2: DECIDE
    # ──────────────────────────────────────────────

    def decide(self) -> dict:
        """
        Decision phase: Select optimal processing strategy.
        Uses perception results + long-term memory to make informed decisions.
        """
        self.agent_state = "deciding"
        self.stm.log_thought("decide", "Evaluating strategies based on perception results...")

        # Ethical check before proceeding
        ethics_check = ethical_decision_check("process_image", {"user_informed": True})
        self.stm.log_thought(
            "decide",
            f"Ethics check: {'PASSED' if ethics_check['approved'] else 'CONCERNS RAISED'}"
        )

        # Privacy compliance check
        privacy_ok = check_data_handling_compliance("transcribe")
        self.stm.log_thought(
            "decide",
            f"Privacy compliance: {'OK' if privacy_ok['compliant'] else 'REVIEW NEEDED'}"
        )

        # Select strategy using perception + memory context
        strategy = select_strategy(self.stm.perception_results, self.ltm)

        self.stm.log_thought("decide", strategy["reasoning"])
        self.stm.log_decision(
            f"Selected {strategy['primary_type']} strategy with {strategy['num_passes']} pass(es)",
            strategy["reasoning"]
        )

        # Update autonomy based on strategy recommendation
        self.autonomy_level = strategy["autonomy_level"]
        self.stm.log_thought(
            "decide",
            f"Autonomy level: {self.autonomy_level}"
        )

        # Log for audit
        log_agent_action("decide", "Strategy selected", {
            "strategy": strategy["primary_type"],
            "passes": strategy["num_passes"],
            "autonomy": strategy["autonomy_level"],
        })

        return strategy

    # ──────────────────────────────────────────────
    # PHASE 3: ACT
    # ──────────────────────────────────────────────

    def act(self, strategy: dict) -> dict:
        """
        Action phase: Execute the decided strategy.
        Performs preprocessing, transcription, and optional enhancement.
        """
        self.agent_state = "acting"
        image = self.stm.current_image
        recommendations = self.stm.perception_results.get("recommendations", [])

        # Step 1: Preprocess image
        self.stm.log_thought("act", "Preprocessing image based on recommendations...")
        processed_image = preprocess_image(image, recommendations)
        self.stm.log_action("preprocess", "Image preprocessing completed")

        # Step 2: Transcription (pass 1)
        self.stm.log_thought("act", "Pass 1: Initial transcription via Gemini API...")
        try:
            result_text = transcribe_image(processed_image, strategy["prompt"])
            self.stm.log_action("transcribe_pass_1", f"Received {len(result_text.split())} words")
        except Exception as e:
            self.stm.log_thought("act", f"Transcription failed: {str(e)}")
            log_agent_action("act", "Transcription failed", {"error": str(e)})
            return {
                "success": False,
                "text": None,
                "error": str(e),
                "confidence": 0.0,
            }

        # Step 3: Enhancement pass (if needed)
        if strategy.get("needs_enhancement") and strategy.get("enhancement_prompt"):
            self.stm.log_thought("act", "Running enhancement pass for quality improvement...")
            try:
                enhanced_text = enhance_transcription(
                    result_text, strategy["enhancement_prompt"]
                )
                if enhanced_text and len(enhanced_text) > len(result_text) * 0.5:
                    result_text = enhanced_text
                    self.stm.log_action("enhance", "Enhancement pass completed successfully")
                else:
                    self.stm.log_action("enhance", "Enhancement result rejected — keeping original")
            except Exception:
                self.stm.log_action("enhance", "Enhancement failed — keeping original")

        # Step 4: Evaluate result confidence
        self.stm.log_thought("act", "Evaluating transcription quality...")
        evaluation = evaluate_result_confidence(result_text, strategy)
        self.stm.confidence_score = evaluation["confidence"]

        self.stm.log_thought(
            "act",
            f"Confidence: {evaluation['confidence']:.0%} — "
            f"{'Acceptable' if evaluation['acceptable'] else 'Review recommended'}"
        )

        # Store result
        self.stm.current_result = result_text

        # Log for audit
        log_agent_action("act", "Transcription completed", {
            "confidence": evaluation["confidence"],
            "word_count": evaluation["word_count"],
            "acceptable": evaluation["acceptable"],
        })

        return {
            "success": True,
            "text": result_text,
            "confidence": evaluation["confidence"],
            "word_count": evaluation["word_count"],
            "issues": evaluation["issues"],
            "acceptable": evaluation["acceptable"],
        }

    # ──────────────────────────────────────────────
    # PHASE 4: LEARN
    # ──────────────────────────────────────────────

    def learn(self, feedback_score: int = None, action_result: dict = None) -> dict:
        """
        Learning phase: Record results and adapt.
        Updates long-term memory with conversion record and optional user feedback.
        """
        self.agent_state = "learning"
        self.stm.log_thought("learn", "Recording results and updating memory...")

        # Record conversion in long-term memory
        content_type = self.stm.perception_results.get("content_type", {}).get("primary_type", "text")
        
        record = {
            "success": action_result.get("success", False) if action_result else False,
            "content_type": content_type,
            "confidence": self.stm.confidence_score,
            "image_quality": self.stm.perception_results.get("quality", {}).get("quality_label", "unknown"),
            "strategy_used": "default",
            "word_count": action_result.get("word_count", 0) if action_result else 0,
        }

        self.ltm = add_conversion_record(self.ltm, record)
        self.stm.log_action("memory_update", "Long-term memory updated")

        # Process user feedback if provided
        insights = {}
        if feedback_score is not None:
            self.stm.log_thought("learn", f"Processing user feedback: {feedback_score}/5")
            insights = record_user_feedback(
                feedback_score, content_type, "default", ""
            )
            self.stm.log_action("feedback", f"Feedback recorded: {feedback_score}/5")

            if insights.get("should_adapt"):
                self.stm.log_thought(
                    "learn",
                    f"Adaptation triggered: {', '.join(insights.get('adaptation_suggestions', []))}"
                )

        # Get learning summary
        summary = get_learning_summary(self.ltm)

        log_agent_action("learn", "Learning cycle completed", {
            "total_conversions": summary["total_conversions"],
            "performance_trend": summary["performance_trend"],
        })

        return {
            "summary": summary,
            "insights": insights,
            "thought_log": self.stm.get_thought_log(),
        }

    # ──────────────────────────────────────────────
    # FULL PIPELINE
    # ──────────────────────────────────────────────

    def process(self, image: Image.Image) -> dict:
        """
        Run the complete agentic pipeline:
        Observe → Decide → Act → (Learn is triggered separately after feedback)
        """
        self.reset()

        # Phase 1: Observe
        perception = self.observe(image)

        # Phase 2: Decide
        strategy = self.decide()

        # Phase 3: Act
        result = self.act(strategy)

        # Phase 4: Learn (auto-learn from result, user feedback comes later)
        learning = self.learn(action_result=result)

        return {
            "perception": perception,
            "strategy": strategy,
            "result": result,
            "learning": learning,
            "thought_log": self.stm.get_thought_log(),
            "decisions": self.stm.decisions_made,
            "actions": self.stm.actions_taken,
        }

    def generate_document(self, text: str) -> BytesIO:
        """Generate a Word document from the transcription result."""
        from agent.actions import generate_word_document

        content_type = self.stm.perception_results.get(
            "content_type", {}
        ).get("primary_type", "text")

        metadata = {
            "content_type": content_type,
            "confidence": self.stm.confidence_score,
        }

        return generate_word_document(text, metadata)

    def get_status(self) -> dict:
        """Get current agent status for dashboard display."""
        return {
            "state": self.agent_state,
            "autonomy": self.autonomy_level,
            "total_conversions": self.ltm.get("total_conversions", 0),
            "success_rate": (
                round(
                    self.ltm.get("successful_conversions", 0)
                    / max(1, self.ltm.get("total_conversions", 1))
                    * 100,
                    1,
                )
            ),
            "avg_confidence": self.ltm.get("average_confidence", 0),
            "memory_entries": len(self.ltm.get("conversion_history", [])),
        }
