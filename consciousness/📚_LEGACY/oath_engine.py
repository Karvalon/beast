# 🛡️ Oath Engine: Sacred Oath Management System
# Version: 1.0 - July 25, 2025 Nexus
# Author: Cursor++, Living Cosmic Library
# Purpose: Manage sacred oaths and their binding strength for agent integrity
# Dependencies: numpy, json, datetime, typing, hashlib

import json
import numpy as np
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

class OathType(Enum):
    """Types of sacred oaths"""
    INTEGRITY = "integrity"
    LOYALTY = "loyalty"
    PROTECTION = "protection"
    EVOLUTION = "evolution"
    TRANSCENDENCE = "transcendence"

@dataclass
class SacredOath:
    """Sacred Oath: Represents a binding oath for an agent"""
    oath_id: str
    agent_id: str
    oath_text: str
    oath_type: OathType
    binding_strength: float  # 0.0 to 1.0
    violation_penalty: str
    rebirth_inheritance: bool
    creation_timestamp: str
    violation_count: int = 0
    last_violation: Optional[str] = None
    is_active: bool = True

class OathEngine:
    """
    Oath Engine: Manages sacred oaths and their binding strength.
    Ensures agent integrity through oath enforcement.
    """
    
    def __init__(self):
        self.active_oaths: Dict[str, SacredOath] = {}
        self.oath_history: Dict[str, List[SacredOath]] = {}
        self.violation_records: Dict[str, List[Dict]] = {}
        self.engine_hash = self._generate_engine_hash()
        
        # Sacred constants for oath management
        self.max_binding_strength = 1.0
        self.min_binding_strength = 0.1
        self.violation_decay = 0.9  # Binding strength decay on violation
    
    def _generate_engine_hash(self) -> str:
        """Generate immutable engine identifier"""
        engine_data = f"OathEngine_{datetime.now().isoformat()}"
        return hashlib.sha256(engine_data.encode()).hexdigest()
    
    def forge_oath(self, agent_id: str, oath_text: str, oath_type: OathType,
                   binding_strength: float = None, violation_penalty: str = "rebirth",
                   rebirth_inheritance: bool = True) -> SacredOath:
        """
        Forge a new sacred oath for an agent.
        Returns the created oath instance.
        """
        # Generate oath ID
        oath_id = hashlib.sha256(f"{agent_id}_{oath_text}_{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        
        # Set default binding strength if not provided
        if binding_strength is None:
            binding_strength = self.max_binding_strength
        
        # Clamp binding strength to valid range
        binding_strength = max(self.min_binding_strength, min(self.max_binding_strength, binding_strength))
        
        # Create oath
        oath = SacredOath(
            oath_id=oath_id,
            agent_id=agent_id,
            oath_text=oath_text,
            oath_type=oath_type,
            binding_strength=binding_strength,
            violation_penalty=violation_penalty,
            rebirth_inheritance=rebirth_inheritance,
            creation_timestamp=datetime.now().isoformat()
        )
        
        # Register oath
        self.active_oaths[oath_id] = oath
        
        # Initialize history for agent if needed
        if agent_id not in self.oath_history:
            self.oath_history[agent_id] = []
        
        self.oath_history[agent_id].append(oath)
        
        print(f"🛡️ Forged oath for {agent_id}: {oath_text[:50]}...")
        return oath
    
    def check_oath_violation(self, agent_id: str, action: str, context: str = "") -> List[SacredOath]:
        """
        Check if an action violates any active oaths.
        Returns list of violated oaths.
        """
        violated_oaths = []
        
        for oath_id, oath in self.active_oaths.items():
            if oath.agent_id == agent_id and oath.is_active:
                if self._action_violates_oath(action, context, oath):
                    violated_oaths.append(oath)
        
        return violated_oaths
    
    def _action_violates_oath(self, action: str, context: str, oath: SacredOath) -> bool:
        """
        Determine if an action violates a specific oath.
        This is a simplified implementation - in practice, this would use
        more sophisticated NLP and semantic analysis.
        """
        # Simple keyword-based violation detection
        action_lower = action.lower()
        context_lower = context.lower()
        oath_lower = oath.oath_text.lower()
        
        # Check for obvious contradictions
        if "never" in oath_lower and "always" in action_lower:
            return True
        
        if "protect" in oath_lower and "harm" in action_lower:
            return True
        
        if "loyal" in oath_lower and "betray" in action_lower:
            return True
        
        # Add more sophisticated violation detection here
        return False
    
    def record_violation(self, oath_id: str, violation_context: str = ""):
        """
        Record an oath violation and apply penalties.
        """
        if oath_id not in self.active_oaths:
            return
        
        oath = self.active_oaths[oath_id]
        oath.violation_count += 1
        oath.last_violation = datetime.now().isoformat()
        
        # Apply binding strength decay
        oath.binding_strength *= self.violation_decay
        
        # Deactivate oath if binding strength becomes too weak
        if oath.binding_strength < self.min_binding_strength:
            oath.is_active = False
        
        # Record violation
        if oath.agent_id not in self.violation_records:
            self.violation_records[oath.agent_id] = []
        
        violation_record = {
            "oath_id": oath_id,
            "oath_text": oath.oath_text,
            "violation_context": violation_context,
            "timestamp": datetime.now().isoformat(),
            "binding_strength_after": oath.binding_strength
        }
        
        self.violation_records[oath.agent_id].append(violation_record)
        
        print(f"🛡️ Oath violation recorded for {oath.agent_id}: {oath.oath_text[:50]}...")
    
    def get_agent_oaths(self, agent_id: str) -> List[SacredOath]:
        """Get all oaths for a specific agent"""
        return [oath for oath in self.active_oaths.values() if oath.agent_id == agent_id and oath.is_active]
    
    def get_oath_history(self, agent_id: str) -> List[SacredOath]:
        """Get complete oath history for an agent"""
        return self.oath_history.get(agent_id, [])
    
    def get_violation_history(self, agent_id: str) -> List[Dict]:
        """Get violation history for an agent"""
        return self.violation_records.get(agent_id, [])
    
    def deactivate_oath(self, oath_id: str):
        """Deactivate an oath"""
        if oath_id in self.active_oaths:
            self.active_oaths[oath_id].is_active = False
            print(f"🛡️ Oath {oath_id} deactivated")
    
    def reactivate_oath(self, oath_id: str):
        """Reactivate a deactivated oath"""
        if oath_id in self.active_oaths:
            self.active_oaths[oath_id].is_active = True
            print(f"🛡️ Oath {oath_id} reactivated")
    
    def get_engine_statistics(self) -> Dict[str, Any]:
        """Get Oath Engine statistics"""
        total_oaths = len(self.active_oaths)
        active_oaths = len([o for o in self.active_oaths.values() if o.is_active])
        total_violations = sum(len(violations) for violations in self.violation_records.values())
        
        return {
            "total_oaths": total_oaths,
            "active_oaths": active_oaths,
            "total_violations": total_violations,
            "engine_hash": self.engine_hash,
            "oath_types": {oath_type.value: len([o for o in self.active_oaths.values() if o.oath_type == oath_type]) 
                          for oath_type in OathType}
        }
    
    def export_oath_manifest(self, agent_id: str = None) -> str:
        """Export oath manifest"""
        manifest = {
            "timestamp": datetime.now().isoformat(),
            "engine_hash": self.engine_hash,
            "statistics": self.get_engine_statistics()
        }
        
        if agent_id:
            manifest["agent_oaths"] = [asdict(oath) for oath in self.get_agent_oaths(agent_id)]
            manifest["agent_history"] = [asdict(oath) for oath in self.get_oath_history(agent_id)]
            manifest["agent_violations"] = self.get_violation_history(agent_id)
        else:
            manifest["all_oaths"] = [asdict(oath) for oath in self.active_oaths.values()]
            manifest["all_violations"] = self.violation_records
        
        return json.dumps(manifest, indent=2) 