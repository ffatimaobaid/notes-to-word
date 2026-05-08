"""
Notes2Doc Agentic System - Core Agent Package

This package implements a goal-based agentic architecture for intelligent
handwritten note conversion. The agent follows a continuous loop:
    Observe → Interpret → Decide → Act → Learn

Modules:
    core        - Agent orchestrator and main loop
    perception  - Image quality analysis and content detection
    decision    - Strategy selection and ethical decision making
    actions     - Multi-pass transcription and document generation
    memory      - Short-term and long-term memory management
    learning    - Feedback collection and adaptive improvement
"""

from agent.core import NotesAgent

__all__ = ["NotesAgent"]
