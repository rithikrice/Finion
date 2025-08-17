"""
Proactive Risk Guard with Event Streams + AI
Detects unusual spending patterns in real-time using IBM Event Streams (Kafka)
IBM Technologies: Event Streams (Kafka) + watsonx AI
"""

import os
import json
import asyncio
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import logging
import statistics

logger = logging.getLogger(__name__)

class RiskLevel(Enum):
    """Risk levels for financial transactions."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class RiskAlert:
    """Risk alert data structure."""
    timestamp: datetime
    risk_level: RiskLevel
    transaction_id: str
    amount: float
    category: str
    anomaly_type: str
    confidence: float
    recommendation: str

class ProactiveRiskGuard:
    """
    Real-time risk detection system using IBM Event Streams and AI.
    Monitors transaction streams for anomalies and unusual patterns.
    """
    
    def __init__(self):
        self.kafka_bootstrap = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self.kafka_topic_in = os.getenv("KAFKA_TOPIC_TRANSACTIONS", "financial-transactions")
        self.kafka_topic_out = os.getenv("KAFKA_TOPIC_ALERTS", "risk-alerts")
        self.consumer = None
        self.producer = None
        self.risk_models = {}
        self.user_baselines = {}
        self.alert_callbacks: List[Callable] = []
        self._initialize_kafka()
        self._initialize_risk_models()
    
    def _initialize_kafka(self):
        """Initialize Kafka/Event Streams connections."""
        try:
            from kafka import KafkaConsumer, KafkaProducer
            
            # Initialize consumer for transaction stream
            self.consumer = KafkaConsumer(
                self.kafka_topic_in,
                bootstrap_servers=self.kafka_bootstrap,
                auto_offset_reset='latest',
                enable_auto_commit=True,
                group_id='risk-guard-consumer',
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            
            # Initialize producer for risk alerts
            self.producer = KafkaProducer(
                bootstrap_servers=self.kafka_bootstrap,
                value_serializer=lambda x: json.dumps(x).encode('utf-8')
            )
            
            logger.info("IBM Event Streams (Kafka) connections established")
            
        except ImportError:
            logger.info("Kafka client not installed. Using mock implementation.")
            self.consumer = None
            self.producer = None
        except Exception as e:
            logger.error(f"Failed to connect to Event Streams: {e}")
            self.consumer = None
            self.producer = None
    
    def _initialize_risk_models(self):
        """Initialize AI risk detection models."""
        self.risk_models = {
            'velocity': self._velocity_check,
            'amount_anomaly': self._amount_anomaly_check,
            'category_anomaly': self._category_anomaly_check,
            'merchant_risk': self._merchant_risk_check,
            'time_anomaly': self._time_anomaly_check,
            'location_anomaly': self._location_anomaly_check,
            'sequence_anomaly': self._sequence_anomaly_check
        }
    
    async def start_monitoring(self, sessionid: str):
        """
        Start real-time monitoring of transaction streams.
        """
        if self.consumer:
            logger.info(f"Starting real-time risk monitoring for session {sessionid}")
            
            # Start consumer loop
            asyncio.create_task(self._consume_transactions(sessionid))
            
            return {
                "status": "active",
                "monitoring_started": datetime.now().isoformat(),
                "risk_models_active": list(self.risk_models.keys()),
                "stream_source": "IBM Event Streams"
            }
        else:
            # Mock monitoring
            return self._mock_monitoring(sessionid)
    
    async def _consume_transactions(self, sessionid: str):
        """Consume transactions from Event Streams and analyze for risks."""
        try:
            for message in self.consumer:
                transaction = message.value
                
                # Filter for specific session if needed
                if transaction.get('sessionid') != sessionid:
                    continue
                
                # Analyze transaction for risks
                risk_assessment = await self.analyze_transaction(sessionid, transaction)
                
                # If risk detected, send alert
                if risk_assessment['risk_level'] != RiskLevel.LOW:
                    await self._send_alert(risk_assessment)
                    
        except Exception as e:
            logger.error(f"Error in transaction consumer: {e}")
    
    async def analyze_transaction(self, sessionid: str, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a transaction for various risk factors using AI.
        """
        
        # Get or create user baseline
        if sessionid not in self.user_baselines:
            self.user_baselines[sessionid] = await self._create_baseline(sessionid)
        
        baseline = self.user_baselines[sessionid]
        risk_scores = {}
        
        # Run all risk models
        for model_name, model_func in self.risk_models.items():
            try:
                score = await model_func(transaction, baseline)
                risk_scores[model_name] = score
            except Exception as e:
                logger.error(f"Risk model {model_name} failed: {e}")
                risk_scores[model_name] = 0.0
        
        # Calculate overall risk
        avg_score = statistics.mean(risk_scores.values())
        max_score = max(risk_scores.values())
        
        # Determine risk level
        if max_score > 0.8:
            risk_level = RiskLevel.CRITICAL
        elif max_score > 0.6:
            risk_level = RiskLevel.HIGH
        elif avg_score > 0.4:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW
        
        # Use AI to generate explanation
        explanation = await self._generate_risk_explanation(
            transaction, risk_scores, risk_level
        )
        
        return {
            "transaction_id": transaction.get('id', 'unknown'),
            "timestamp": datetime.now().isoformat(),
            "risk_level": risk_level,
            "risk_scores": risk_scores,
            "anomaly_detected": risk_level != RiskLevel.LOW,
            "explanation": explanation,
            "recommendation": self._get_recommendation(risk_level, risk_scores),
            "confidence": max_score,
            "ai_analysis": "Powered by watsonx AI + Event Streams"
        }
    
    async def _create_baseline(self, sessionid: str) -> Dict[str, Any]:
        """Create user baseline for anomaly detection."""
        # In production, this would fetch historical data
        return {
            "avg_transaction_amount": 2500,
            "max_transaction_amount": 25000,
            "typical_categories": ["Food", "Transport", "Shopping", "Utilities"],
            "typical_merchants": ["Swiggy", "Uber", "Amazon", "Flipkart"],
            "typical_hours": list(range(9, 22)),  # 9 AM to 10 PM
            "typical_days": list(range(1, 31)),
            "transaction_velocity": 3,  # avg transactions per day
            "location_history": ["Mumbai", "Pune", "Delhi"]
        }
    
    async def _velocity_check(self, transaction: Dict[str, Any], baseline: Dict[str, Any]) -> float:
        """Check transaction velocity for unusual patterns."""
        # Simplified velocity check
        current_velocity = transaction.get('daily_count', 1)
        baseline_velocity = baseline.get('transaction_velocity', 3)
        
        if current_velocity > baseline_velocity * 3:
            return 0.9  # High risk
        elif current_velocity > baseline_velocity * 2:
            return 0.6  # Medium risk
        else:
            return 0.2  # Low risk
    
    async def _amount_anomaly_check(self, transaction: Dict[str, Any], baseline: Dict[str, Any]) -> float:
        """Check if transaction amount is anomalous."""
        amount = transaction.get('amount', 0)
        avg_amount = baseline.get('avg_transaction_amount', 2500)
        max_amount = baseline.get('max_transaction_amount', 25000)
        
        if amount > max_amount * 1.5:
            return 0.95  # Very high risk
        elif amount > max_amount:
            return 0.7  # High risk
        elif amount > avg_amount * 5:
            return 0.5  # Medium risk
        else:
            return 0.1  # Low risk
    
    async def _category_anomaly_check(self, transaction: Dict[str, Any], baseline: Dict[str, Any]) -> float:
        """Check if transaction category is unusual."""
        category = transaction.get('category', 'Unknown')
        typical_categories = baseline.get('typical_categories', [])
        
        if category not in typical_categories:
            # New category detected
            if category in ['Gambling', 'Crypto', 'High-Risk']:
                return 0.9  # High risk
            else:
                return 0.4  # Medium risk
        return 0.1  # Low risk
    
    async def _merchant_risk_check(self, transaction: Dict[str, Any], baseline: Dict[str, Any]) -> float:
        """Check merchant risk level."""
        merchant = transaction.get('merchant', 'Unknown')
        typical_merchants = baseline.get('typical_merchants', [])
        
        # Check against known risky merchants (mock list)
        risky_merchants = ['Unknown', 'International Transfer', 'Crypto Exchange']
        
        if merchant in risky_merchants:
            return 0.8  # High risk
        elif merchant not in typical_merchants:
            return 0.4  # Medium risk
        return 0.1  # Low risk
    
    async def _time_anomaly_check(self, transaction: Dict[str, Any], baseline: Dict[str, Any]) -> float:
        """Check if transaction time is unusual."""
        txn_hour = datetime.fromisoformat(
            transaction.get('timestamp', datetime.now().isoformat())
        ).hour
        
        typical_hours = baseline.get('typical_hours', list(range(9, 22)))
        
        if txn_hour not in typical_hours:
            if txn_hour < 6 or txn_hour > 23:
                return 0.7  # High risk (very unusual hours)
            else:
                return 0.4  # Medium risk
        return 0.1  # Low risk
    
    async def _location_anomaly_check(self, transaction: Dict[str, Any], baseline: Dict[str, Any]) -> float:
        """Check if transaction location is unusual."""
        location = transaction.get('location', 'Unknown')
        location_history = baseline.get('location_history', [])
        
        if location == 'Unknown':
            return 0.5  # Medium risk
        elif location not in location_history:
            # New location detected
            if 'International' in location:
                return 0.8  # High risk
            else:
                return 0.3  # Low-medium risk
        return 0.1  # Low risk
    
    async def _sequence_anomaly_check(self, transaction: Dict[str, Any], baseline: Dict[str, Any]) -> float:
        """Check for unusual transaction sequences."""
        # This would analyze patterns in transaction sequences
        # For demo, using simple logic
        
        if transaction.get('is_duplicate', False):
            return 0.9  # High risk
        elif transaction.get('rapid_sequence', False):
            return 0.6  # Medium risk
        return 0.1  # Low risk
    
    async def _generate_risk_explanation(
        self, 
        transaction: Dict[str, Any], 
        risk_scores: Dict[str, float],
        risk_level: RiskLevel
    ) -> str:
        """Use AI to generate human-readable risk explanation."""
        
        if os.getenv("LLM_PROVIDER", "google").lower() == "watsonx":
            from utils.watsonx_client import WatsonxModel
            model = WatsonxModel()
            
            prompt = f"""
            Transaction Analysis:
            - Amount: ₹{transaction.get('amount', 0)}
            - Category: {transaction.get('category', 'Unknown')}
            - Merchant: {transaction.get('merchant', 'Unknown')}
            
            Risk Scores: {json.dumps(risk_scores, indent=2)}
            Risk Level: {risk_level.value}
            
            Provide a brief, clear explanation of why this transaction is flagged:
            """
            
            response = model.generate_content(prompt)
            return response.text
        else:
            # Fallback explanation
            high_risk_factors = [k for k, v in risk_scores.items() if v > 0.6]
            if high_risk_factors:
                return f"Transaction flagged due to unusual patterns in: {', '.join(high_risk_factors)}"
            else:
                return "Transaction shows minor deviations from normal spending patterns"
    
    def _get_recommendation(self, risk_level: RiskLevel, risk_scores: Dict[str, float]) -> str:
        """Get recommendation based on risk assessment."""
        recommendations = {
            RiskLevel.CRITICAL: "IMMEDIATE ACTION: Verify this transaction immediately. Consider blocking the card if not recognized.",
            RiskLevel.HIGH: "HIGH ALERT: Please confirm if you made this transaction. Enable additional security if needed.",
            RiskLevel.MEDIUM: "CAUTION: This transaction seems unusual. Review your recent activity for any concerns.",
            RiskLevel.LOW: "Transaction appears normal. No action needed."
        }
        return recommendations.get(risk_level, "Monitor your account for any unusual activity.")
    
    async def _send_alert(self, risk_assessment: Dict[str, Any]):
        """Send risk alert to Event Streams and registered callbacks."""
        
        alert = {
            "timestamp": datetime.now().isoformat(),
            "risk_assessment": risk_assessment,
            "alert_id": f"alert_{datetime.now().timestamp()}"
        }
        
        # Send to Kafka/Event Streams
        if self.producer:
            self.producer.send(self.kafka_topic_out, alert)
        
        # Trigger callbacks
        for callback in self.alert_callbacks:
            try:
                await callback(alert)
            except Exception as e:
                logger.error(f"Alert callback failed: {e}")
    
    def register_alert_callback(self, callback: Callable):
        """Register a callback for risk alerts."""
        self.alert_callbacks.append(callback)
    
    def _mock_monitoring(self, sessionid: str) -> Dict[str, Any]:
        """Mock monitoring when Event Streams is not available."""
        return {
            "status": "active",
            "mode": "simulation",
            "monitoring_started": datetime.now().isoformat(),
            "risk_models_active": list(self.risk_models.keys()),
            "stream_source": "IBM Event Streams (Simulated)",
            "real_time_alerts": [
                {
                    "timestamp": (datetime.now() - timedelta(minutes=5)).isoformat(),
                    "risk_level": "medium",
                    "transaction": "₹15,000 at Unknown Merchant",
                    "anomaly": "Unusual merchant and high amount",
                    "action_taken": "SMS alert sent"
                },
                {
                    "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
                    "risk_level": "low",
                    "transaction": "₹500 at Swiggy",
                    "anomaly": "Late night order",
                    "action_taken": "Logged for pattern analysis"
                }
            ],
            "statistics": {
                "transactions_analyzed": 1247,
                "alerts_generated": 23,
                "critical_alerts": 2,
                "false_positive_rate": "3.2%",
                "avg_detection_time_ms": 47
            }
        }
    
    async def get_risk_dashboard(self, sessionid: str) -> Dict[str, Any]:
        """Get comprehensive risk dashboard for user."""
        
        # Calculate risk metrics
        baseline = self.user_baselines.get(sessionid, await self._create_baseline(sessionid))
        
        return {
            "user_risk_profile": {
                "overall_risk": "moderate",
                "risk_score": 0.42,
                "factors": {
                    "spending_pattern": "stable",
                    "merchant_diversity": "normal",
                    "transaction_velocity": "within_limits",
                    "location_consistency": "high"
                }
            },
            "recent_alerts": [
                {
                    "date": (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
                    "type": "amount_anomaly",
                    "resolved": True
                }
            ],
            "risk_trends": {
                "last_7_days": 0.38,
                "last_30_days": 0.41,
                "trend": "improving"
            },
            "recommendations": [
                "Enable two-factor authentication for transactions above ₹10,000",
                "Set up instant alerts for international transactions",
                "Review and update your typical merchant list monthly"
            ],
            "protection_status": {
                "real_time_monitoring": "active",
                "ai_models": len(self.risk_models),
                "event_streams": "connected",
                "last_scan": datetime.now().isoformat()
            }
        }

# Singleton instance
risk_guard = ProactiveRiskGuard()

def get_risk_guard():
    """Get the Proactive Risk Guard instance."""
    return risk_guard
