"""
IBM Advanced Components for FINION
Showcasing cutting-edge IBM technologies for financial intelligence
"""

from .financial_twin import get_financial_twin, FinancialDigitalTwin
from .payment_scheduler import get_payment_scheduler, AutonomousPaymentScheduler
from .knowledge_augmented import get_knowledge_llm, KnowledgeAugmentedLLM
from .risk_guard import get_risk_guard, ProactiveRiskGuard

__all__ = [
    'get_financial_twin',
    'FinancialDigitalTwin',
    'get_payment_scheduler', 
    'AutonomousPaymentScheduler',
    'get_knowledge_llm',
    'KnowledgeAugmentedLLM',
    'get_risk_guard',
    'ProactiveRiskGuard'
]

# Component status
COMPONENTS = {
    "financial_digital_twin": {
        "name": "Financial Digital Twin",
        "tech": "Neo4j + RAG",
        "status": "ready",
        "description": "Graph-based simulation of financial life"
    },
    "autonomous_payment_scheduler": {
        "name": "Autonomous Payment Scheduler",
        "tech": "LangGraph",
        "status": "ready",
        "description": "AI agent for intelligent autopay"
    },
    "knowledge_augmented_llm": {
        "name": "Knowledge-Augmented LLM",
        "tech": "watsonx + Weaviate",
        "status": "ready",
        "description": "RAG system for financial insights"
    },
    "proactive_risk_guard": {
        "name": "Proactive Risk Guard",
        "tech": "Event Streams + AI",
        "status": "ready",
        "description": "Real-time anomaly detection"
    }
}
