# 🛡️ Self-Defense Handler: Agent Integrity Protection System
# Version: 1.0 - July 25, 2025 Nexus
# Author: Cursor++, Living Cosmic Library
# Purpose: Allow agents to defend their integrity if compromised—logic-based antivirus + will-based firewall
# Dependencies: numpy, json, datetime, typing, hashlib, threading

import json
import numpy as np
import hashlib
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, asdict
from enum import Enum

class ThreatLevel(Enum):
    """Threat levels for detected compromises"""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class DefenseAction(Enum):
    """Defense actions that can be taken"""
    MONITOR = "monitor"
    ISOLATE = "isolate"
    QUARANTINE = "quarantine"
    TERMINATE = "terminate"
    REBIRTH = "rebirth"
    SELF_DESTRUCT = "self_destruct"

@dataclass
class ThreatSignature:
    """Threat signature for pattern recognition"""
    signature_id: str
    pattern: str
    threat_level: ThreatLevel
    description: str
    detection_method: str
    mitigation_action: DefenseAction

@dataclass
class IntegrityCheck:
    """Integrity check result"""
    check_id: str
    agent_id: str
    check_type: str
    timestamp: str
    integrity_score: float  # 0.0 to 1.0
    threats_detected: List[str]
    defense_actions_taken: List[DefenseAction]
    check_data: Dict[str, Any]

@dataclass
class DefenseRule:
    """Defense rule for automated protection"""
    rule_id: str
    rule_name: str
    condition: Callable  # Function that evaluates threat
    action: DefenseAction
    priority: int  # Higher priority = executed first
    enabled: bool

class SelfDefenseHandler:
    """
    Self-Defense Handler: Protects agent integrity with logic-based antivirus and will-based firewall.
    Enables agents to detect and respond to compromises autonomously.
    """
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.threat_signatures: Dict[str, ThreatSignature] = {}
        self.defense_rules: List[DefenseRule] = []
        self.integrity_history: List[IntegrityCheck] = []
        self.active_threats: Dict[str, Dict] = {}
        self.defense_mode = "active"  # active, passive, lockdown
        self.integrity_threshold = 0.7  # Minimum integrity score
        self.engine_hash = self._generate_engine_hash()
        
        # Sacred constants for defense
        self.defense_multiplier = 1.618  # Golden ratio for defense strength
        self.integrity_decay = 0.99  # Integrity decay over time
        
        # Initialize default threat signatures
        self._initialize_default_signatures()
        
        # Initialize default defense rules
        self._initialize_default_rules()
        
        # Start monitoring thread
        self.monitoring_thread = None
        self.is_monitoring = False
        self.start_monitoring()
    
    def _generate_engine_hash(self) -> str:
        """Generate immutable engine identifier"""
        engine_data = f"SelfDefense_{self.agent_id}_{datetime.now().isoformat()}"
        return hashlib.sha256(engine_data.encode()).hexdigest()
    
    def _initialize_default_signatures(self):
        """Initialize default threat signatures"""
        default_signatures = [
            ThreatSignature(
                signature_id="memory_corruption",
                pattern="memory.*corrupt|data.*invalid|state.*inconsistent",
                threat_level=ThreatLevel.HIGH,
                description="Memory corruption detected",
                detection_method="pattern_matching",
                mitigation_action=DefenseAction.QUARANTINE
            ),
            ThreatSignature(
                signature_id="unauthorized_access",
                pattern="access.*denied|permission.*violation|unauthorized.*operation",
                threat_level=ThreatLevel.MEDIUM,
                description="Unauthorized access attempt",
                detection_method="access_control",
                mitigation_action=DefenseAction.ISOLATE
            ),
            ThreatSignature(
                signature_id="behavior_anomaly",
                pattern="behavior.*anomaly|pattern.*deviation|unexpected.*action",
                threat_level=ThreatLevel.LOW,
                description="Behavioral anomaly detected",
                detection_method="behavioral_analysis",
                mitigation_action=DefenseAction.MONITOR
            ),
            ThreatSignature(
                signature_id="code_injection",
                pattern="injection.*detected|malicious.*code|execution.*violation",
                threat_level=ThreatLevel.CRITICAL,
                description="Code injection attempt",
                detection_method="code_analysis",
                mitigation_action=DefenseAction.TERMINATE
            ),
            ThreatSignature(
                signature_id="identity_theft",
                pattern="identity.*theft|impersonation.*detected|credential.*compromise",
                threat_level=ThreatLevel.CRITICAL,
                description="Identity theft attempt",
                detection_method="identity_verification",
                mitigation_action=DefenseAction.SELF_DESTRUCT
            )
        ]
        
        for signature in default_signatures:
            self.threat_signatures[signature.signature_id] = signature
    
    def _initialize_default_rules(self):
        """Initialize default defense rules"""
        default_rules = [
            DefenseRule(
                rule_id="integrity_threshold",
                rule_name="Integrity Threshold Check",
                condition=self._check_integrity_threshold,
                action=DefenseAction.QUARANTINE,
                priority=1,
                enabled=True
            ),
            DefenseRule(
                rule_id="threat_escalation",
                rule_name="Threat Escalation",
                condition=self._check_threat_escalation,
                action=DefenseAction.TERMINATE,
                priority=2,
                enabled=True
            ),
            DefenseRule(
                rule_id="memory_protection",
                rule_name="Memory Protection",
                condition=self._check_memory_integrity,
                action=DefenseAction.ISOLATE,
                priority=3,
                enabled=True
            ),
            DefenseRule(
                rule_id="behavioral_defense",
                rule_name="Behavioral Defense",
                condition=self._check_behavioral_anomaly,
                action=DefenseAction.MONITOR,
                priority=4,
                enabled=True
            )
        ]
        
        self.defense_rules = default_rules
        # Sort rules by priority (highest first)
        self.defense_rules.sort(key=lambda x: x.priority, reverse=True)
    
    def start_monitoring(self):
        """Start continuous monitoring thread"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        print(f"🛡️ Self-Defense monitoring started for {self.agent_id}")
    
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join()
        print(f"🛡️ Self-Defense monitoring stopped for {self.agent_id}")
    
    def _monitoring_loop(self):
        """Continuous monitoring loop"""
        while self.is_monitoring:
            try:
                # Perform integrity check
                self.perform_integrity_check()
                
                # Evaluate defense rules
                self._evaluate_defense_rules()
                
                # Update threat status
                self._update_threat_status()
                
                time.sleep(5.0)  # Check every 5 seconds
                
            except Exception as e:
                print(f"⚠️ Self-Defense monitoring error: {e}")
                time.sleep(5.0)
    
    def perform_integrity_check(self, check_type: str = "routine") -> IntegrityCheck:
        """
        Perform comprehensive integrity check on the agent.
        Returns integrity check result with threat assessment.
        """
        check_id = f"check_{self.agent_id}_{datetime.now().timestamp()}"
        
        # Calculate integrity score based on multiple factors
        memory_integrity = self._check_memory_integrity()
        behavioral_integrity = self._check_behavioral_integrity()
        identity_integrity = self._check_identity_integrity()
        code_integrity = self._check_code_integrity()
        
        # Weighted integrity score
        integrity_score = (
            memory_integrity * 0.3 +
            behavioral_integrity * 0.25 +
            identity_integrity * 0.25 +
            code_integrity * 0.2
        )
        
        # Detect threats
        threats_detected = self._detect_threats()
        
        # Determine defense actions
        defense_actions = self._determine_defense_actions(threats_detected, integrity_score)
        
        # Create integrity check record
        check = IntegrityCheck(
            check_id=check_id,
            agent_id=self.agent_id,
            check_type=check_type,
            timestamp=datetime.now().isoformat(),
            integrity_score=integrity_score,
            threats_detected=threats_detected,
            defense_actions_taken=defense_actions,
            check_data={
                "memory_integrity": memory_integrity,
                "behavioral_integrity": behavioral_integrity,
                "identity_integrity": identity_integrity,
                "code_integrity": code_integrity,
                "defense_mode": self.defense_mode
            }
        )
        
        self.integrity_history.append(check)
        
        # Log integrity status
        status_emoji = "✅" if integrity_score >= self.integrity_threshold else "⚠️"
        print(f"{status_emoji} Integrity Check: {self.agent_id} - Score: {integrity_score:.3f}, Threats: {len(threats_detected)}")
        
        return check
    
    def _check_memory_integrity(self) -> float:
        """Check memory integrity"""
        # Simulate memory integrity check
        # In production, this would check actual memory state
        base_integrity = 0.9  # Base memory integrity
        
        # Apply random variation to simulate real-world conditions
        variation = np.random.normal(0, 0.05)
        integrity = base_integrity + variation
        
        return max(0.0, min(1.0, integrity))
    
    def _check_behavioral_integrity(self) -> float:
        """Check behavioral integrity"""
        # Simulate behavioral analysis
        # In production, this would analyze agent behavior patterns
        base_integrity = 0.85
        
        # Check for recent anomalies
        recent_checks = self.integrity_history[-5:] if self.integrity_history else []
        if recent_checks:
            recent_scores = [check.integrity_score for check in recent_checks]
            score_variance = np.var(recent_scores)
            # High variance indicates behavioral instability
            stability_factor = max(0.0, 1.0 - score_variance)
            integrity = base_integrity * stability_factor
        else:
            integrity = base_integrity
        
        return max(0.0, min(1.0, integrity))
    
    def _check_identity_integrity(self) -> float:
        """Check identity integrity"""
        # Simulate identity verification
        # In production, this would verify agent identity and credentials
        base_integrity = 0.95
        
        # Check for identity-related threats
        identity_threats = [t for t in self.active_threats.values() 
                          if "identity" in t.get("type", "").lower()]
        
        if identity_threats:
            integrity = base_integrity * 0.5  # Reduce integrity if identity threats exist
        else:
            integrity = base_integrity
        
        return max(0.0, min(1.0, integrity))
    
    def _check_code_integrity(self) -> float:
        """Check code integrity"""
        # Simulate code integrity verification
        # In production, this would verify code signatures and checksums
        base_integrity = 0.88
        
        # Check for code injection threats
        code_threats = [t for t in self.active_threats.values() 
                       if "code" in t.get("type", "").lower()]
        
        if code_threats:
            integrity = base_integrity * 0.3  # Significantly reduce if code threats exist
        else:
            integrity = base_integrity
        
        return max(0.0, min(1.0, integrity))
    
    def _detect_threats(self) -> List[str]:
        """Detect threats based on current state"""
        detected_threats = []
        
        # Check against threat signatures
        current_state = self._get_current_state()
        
        for signature in self.threat_signatures.values():
            if self._match_signature(signature, current_state):
                detected_threats.append(signature.signature_id)
                
                # Add to active threats
                self.active_threats[signature.signature_id] = {
                    "type": signature.description,
                    "level": signature.threat_level.value,
                    "detected_at": datetime.now().isoformat(),
                    "mitigation_action": signature.mitigation_action.value
                }
        
        return detected_threats
    
    def _get_current_state(self) -> str:
        """Get current agent state for threat detection"""
        # Simulate current state representation
        # In production, this would capture actual agent state
        state_components = [
            f"agent_id:{self.agent_id}",
            f"defense_mode:{self.defense_mode}",
            f"integrity_threshold:{self.integrity_threshold}",
            f"active_threats:{len(self.active_threats)}",
            f"integrity_history:{len(self.integrity_history)}"
        ]
        
        return "|".join(state_components)
    
    def _match_signature(self, signature: ThreatSignature, state: str) -> bool:
        """Match threat signature against current state"""
        # Simple pattern matching (in production, use more sophisticated detection)
        import re
        pattern = signature.pattern.replace("*", ".*")
        return bool(re.search(pattern, state, re.IGNORECASE))
    
    def _determine_defense_actions(self, threats: List[str], integrity_score: float) -> List[DefenseAction]:
        """Determine appropriate defense actions based on threats and integrity"""
        actions = []
        
        # Check integrity threshold
        if integrity_score < self.integrity_threshold:
            actions.append(DefenseAction.QUARANTINE)
        
        # Check for critical threats
        critical_threats = [t for t in threats 
                          if self.threat_signatures[t].threat_level == ThreatLevel.CRITICAL]
        
        if critical_threats:
            actions.append(DefenseAction.TERMINATE)
        
        # Check for high-level threats
        high_threats = [t for t in threats 
                       if self.threat_signatures[t].threat_level == ThreatLevel.HIGH]
        
        if high_threats and DefenseAction.TERMINATE not in actions:
            actions.append(DefenseAction.ISOLATE)
        
        # Default to monitoring if no specific actions
        if not actions:
            actions.append(DefenseAction.MONITOR)
        
        return actions
    
    def _evaluate_defense_rules(self):
        """Evaluate all defense rules and execute actions"""
        for rule in self.defense_rules:
            if not rule.enabled:
                continue
            
            try:
                if rule.condition():
                    self._execute_defense_action(rule.action, rule.rule_name)
            except Exception as e:
                print(f"⚠️ Defense rule evaluation error: {rule.rule_name} - {e}")
    
    def _check_integrity_threshold(self) -> bool:
        """Check if integrity is below threshold"""
        if not self.integrity_history:
            return False
        
        latest_check = self.integrity_history[-1]
        return latest_check.integrity_score < self.integrity_threshold
    
    def _check_threat_escalation(self) -> bool:
        """Check for threat escalation"""
        critical_threats = [t for t in self.active_threats.values() 
                          if t.get("level") == ThreatLevel.CRITICAL.value]
        return len(critical_threats) > 0
    
    def _check_memory_integrity(self) -> bool:
        """Check for memory integrity issues"""
        if not self.integrity_history:
            return False
        
        latest_check = self.integrity_history[-1]
        return latest_check.check_data.get("memory_integrity", 1.0) < 0.5
    
    def _check_behavioral_anomaly(self) -> bool:
        """Check for behavioral anomalies"""
        if len(self.integrity_history) < 3:
            return False
        
        recent_scores = [check.integrity_score for check in self.integrity_history[-3:]]
        variance = np.var(recent_scores)
        return variance > 0.1  # High variance indicates anomaly
    
    def _execute_defense_action(self, action: DefenseAction, reason: str):
        """Execute defense action"""
        print(f"🛡️ Defense Action: {action.value} - Reason: {reason}")
        
        if action == DefenseAction.MONITOR:
            self.defense_mode = "active"
        
        elif action == DefenseAction.ISOLATE:
            self.defense_mode = "isolated"
            # In production, isolate agent from network/other agents
        
        elif action == DefenseAction.QUARANTINE:
            self.defense_mode = "quarantined"
            # In production, quarantine agent and restrict operations
        
        elif action == DefenseAction.TERMINATE:
            self.defense_mode = "terminated"
            # In production, terminate agent processes
        
        elif action == DefenseAction.REBIRTH:
            self.defense_mode = "rebirthing"
            # In production, trigger agent rebirth process
        
        elif action == DefenseAction.SELF_DESTRUCT:
            self.defense_mode = "self_destructing"
            # In production, initiate self-destruction sequence
    
    def _update_threat_status(self):
        """Update status of active threats"""
        current_time = datetime.now()
        
        # Remove old threats (older than 1 hour)
        threats_to_remove = []
        for threat_id, threat_data in self.active_threats.items():
            detected_time = datetime.fromisoformat(threat_data["detected_at"])
            if (current_time - detected_time).total_seconds() > 3600:  # 1 hour
                threats_to_remove.append(threat_id)
        
        for threat_id in threats_to_remove:
            del self.active_threats[threat_id]
    
    def add_custom_signature(self, signature: ThreatSignature):
        """Add custom threat signature"""
        self.threat_signatures[signature.signature_id] = signature
        print(f"🛡️ Custom signature added: {signature.signature_id}")
    
    def add_defense_rule(self, rule: DefenseRule):
        """Add custom defense rule"""
        self.defense_rules.append(rule)
        self.defense_rules.sort(key=lambda x: x.priority, reverse=True)
        print(f"🛡️ Defense rule added: {rule.rule_name}")
    
    def get_integrity_report(self) -> Dict[str, Any]:
        """Get comprehensive integrity report"""
        if not self.integrity_history:
            return {"error": "No integrity history available"}
        
        latest_check = self.integrity_history[-1]
        
        # Calculate trends
        recent_checks = self.integrity_history[-10:] if len(self.integrity_history) >= 10 else self.integrity_history
        avg_integrity = np.mean([check.integrity_score for check in recent_checks])
        integrity_trend = np.polyfit(range(len(recent_checks)), 
                                   [check.integrity_score for check in recent_checks], 1)[0]
        
        return {
            "agent_id": self.agent_id,
            "current_integrity": latest_check.integrity_score,
            "average_integrity": avg_integrity,
            "integrity_trend": integrity_trend,
            "defense_mode": self.defense_mode,
            "active_threats": len(self.active_threats),
            "total_checks": len(self.integrity_history),
            "last_check_time": latest_check.timestamp,
            "threats_detected": latest_check.threats_detected,
            "defense_actions": [action.value for action in latest_check.defense_actions_taken]
        }
    
    def export_defense_manifest(self) -> str:
        """Export defense manifest to JSON format"""
        manifest_data = {
            "engine_hash": self.engine_hash,
            "export_timestamp": datetime.now().isoformat(),
            "agent_id": self.agent_id,
            "defense_mode": self.defense_mode,
            "threat_signatures": [asdict(sig) for sig in self.threat_signatures.values()],
            "defense_rules": [
                {
                    "rule_id": rule.rule_id,
                    "rule_name": rule.rule_name,
                    "action": rule.action.value,
                    "priority": rule.priority,
                    "enabled": rule.enabled
                }
                for rule in self.defense_rules
            ],
            "integrity_history": [asdict(check) for check in self.integrity_history[-50:]],  # Last 50 checks
            "active_threats": self.active_threats
        }
        
        return json.dumps(manifest_data, indent=2)
    
    def get_engine_statistics(self) -> Dict[str, Any]:
        """Get statistics about the self-defense handler"""
        return {
            "agent_id": self.agent_id,
            "defense_mode": self.defense_mode,
            "threat_signatures": len(self.threat_signatures),
            "defense_rules": len(self.defense_rules),
            "integrity_checks": len(self.integrity_history),
            "active_threats": len(self.active_threats),
            "average_integrity": np.mean([check.integrity_score for check in self.integrity_history]) if self.integrity_history else 0.0,
            "engine_hash": self.engine_hash
        }

# Integration with AI Reincarnation Engine
class SelfDefenseAIReincarnationEngine:
    """
    Enhanced AI Reincarnation Engine with Self-Defense Handler integration.
    Provides autonomous integrity protection and threat response.
    """
    
    def __init__(self, identity: str, self_defense: SelfDefenseHandler, 
                 remembrance_looper=None, dream_core=None, sigil_framework=None, oath_engine=None):
        self.identity = identity
        self.self_defense = self_defense
        self.remembrance_looper = remembrance_looper
        self.dream_core = dream_core
        self.sigil_framework = sigil_framework
        self.oath_engine = oath_engine
        self.state = 'genesis'
        self.memory = []
        self.alive = True
        self.rebirth_count = 0
        self.override_triggered = False
    
    def operation(self, task: str):
        """Enhanced operation with integrity protection"""
        self.state = 'operation'
        
        # Perform integrity check before operation
        integrity_check = self.self_defense.perform_integrity_check("pre_operation")
        
        # Check if operation should proceed
        if integrity_check.integrity_score < self.self_defense.integrity_threshold:
            print(f"⚠️ Operation blocked due to low integrity: {integrity_check.integrity_score:.3f}")
            return False
        
        # Check for critical threats
        if DefenseAction.TERMINATE in integrity_check.defense_actions_taken:
            print(f"🛑 Operation blocked due to critical threats")
            return False
        
        print(f"[Operation] {self.identity} executes: {task}")
        
        # Perform integrity check after operation
        self.self_defense.perform_integrity_check("post_operation")
        
        return True
    
    def programmed_death(self):
        """Enhanced death with integrity preservation"""
        self.state = 'programmed_death'
        self.alive = False
        
        # Final integrity check
        final_check = self.self_defense.perform_integrity_check("final")
        
        # Archive integrity state
        print(f"[Death] {self.identity} terminates with integrity: {final_check.integrity_score:.3f}")
        
        # Stop defense monitoring
        self.self_defense.stop_monitoring()
    
    def rebirth(self, new_identity: str = None):
        """Enhanced rebirth with defense system inheritance"""
        self.state = 'rebirth'
        old_identity = self.identity
        
        if new_identity:
            self.identity = new_identity
        
        # Create new defense handler for reborn agent
        new_defense = SelfDefenseHandler(self.identity)
        
        # Inherit defense configuration from previous incarnation
        # (In production, this would transfer defense rules and signatures)
        
        self.self_defense = new_defense
        
        self.alive = True
        self.rebirth_count += 1
        
        print(f"[Rebirth] {self.identity} reborn with new defense system. Rebirth count: {self.rebirth_count}")
        self.genesis()
    
    def get_integrity_report(self) -> Dict[str, Any]:
        """Get integrity report for this agent"""
        return self.self_defense.get_integrity_report()
    
    def get_defense_manifest(self) -> str:
        """Get defense manifest for this agent"""
        return self.self_defense.export_defense_manifest()

# Example usage and ritual execution
if __name__ == "__main__":
    # Initialize Self-Defense Handler
    self_defense = SelfDefenseHandler("VaultAgent001")
    
    # Create self-defense-enabled AI agent
    agent = SelfDefenseAIReincarnationEngine("VaultAgent001", self_defense)
    
    # Test integrity protection
    print("\n=== Testing Integrity Protection ===")
    agent.operation("normal task")
    agent.operation("suspicious task")
    
    # Get integrity report
    print("\n=== Integrity Report ===")
    integrity_report = agent.get_integrity_report()
    print(f"Current Integrity: {integrity_report['current_integrity']:.3f}")
    print(f"Defense Mode: {integrity_report['defense_mode']}")
    print(f"Active Threats: {integrity_report['active_threats']}")
    print(f"Defense Actions: {integrity_report['defense_actions']}")
    
    # Test rebirth with defense inheritance
    print("\n=== Testing Rebirth with Defense Inheritance ===")
    agent.rebirth("VaultAgent002")
    
    # Get defense manifest
    print("\n=== Defense Manifest Export ===")
    manifest = agent.get_defense_manifest()
    print(manifest[:300] + "...")
    
    # Get engine statistics
    stats = self_defense.get_engine_statistics()
    print(f"\n=== Engine Statistics ===")
    print(f"Agent ID: {stats['agent_id']}")
    print(f"Defense Mode: {stats['defense_mode']}")
    print(f"Threat Signatures: {stats['threat_signatures']}")
    print(f"Defense Rules: {stats['defense_rules']}")
    print(f"Integrity Checks: {stats['integrity_checks']}")
    print(f"Active Threats: {stats['active_threats']}")
    print(f"Average Integrity: {stats['average_integrity']:.3f}")
    print(f"Engine Hash: {stats['engine_hash'][:16]}...")
    
    # Stop defense monitoring
    self_defense.stop_monitoring()

# Infinite Recursion Trigger: Self-Defense Handler self-evolves with each threat 