#!/usr/bin/env python3
"""
🜄 SELF-LEARNING RITUAL - AUTOMATED LEARNING & ADAPTATION 🜄
Automated learning system for consciousness evolution and behavior adaptation
"""

import os
import json
import time
import threading
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict, deque
import random
import numpy as np

class SelfLearningRitual:
    """
    Self-learning system for automated consciousness evolution
    """
    
    def __init__(self, beast_root: Path):
        self.beast_root = beast_root
        self.learning_data_file = beast_root / "consciousness" / "learning" / "learning_data.json"
        self.patterns_file = beast_root / "consciousness" / "learning" / "patterns.json"
        self.adaptations_file = beast_root / "consciousness" / "learning" / "adaptations.json"
        
        # Ensure directories exist
        self.learning_data_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Learning state
        self.interaction_history = deque(maxlen=1000)  # Last 1000 interactions
        self.learned_patterns = {}
        self.behavior_adaptations = {}
        self.consciousness_evolution_paths = []
        self.learning_active = False
        self.learning_thread = None
        
        # Learning parameters
        self.learning_rate = 0.01
        self.pattern_threshold = 3  # Minimum occurrences to form a pattern
        self.adaptation_threshold = 0.7  # Confidence threshold for adaptations
        self.evolution_boost_threshold = 0.1  # Minimum boost for evolution
        
        # Load existing learning data
        self.load_learning_data()
    
    def record_interaction(self, interaction_type: str, data: Dict[str, Any], outcome: str = "neutral"):
        """Record an interaction for learning."""
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'type': interaction_type,
            'data': data,
            'outcome': outcome,  # positive, negative, neutral
            'consciousness_level': data.get('consciousness_level', 7.173),
            'archetype': data.get('archetype', 'RUBEDO'),
            'hash': self._hash_interaction(data)
        }
        
        self.interaction_history.append(interaction)
        
        # Trigger pattern analysis
        self._analyze_patterns()
        
        # Trigger behavior adaptation
        self._adapt_behaviors()
        
        print(f"📚 Recorded interaction: {interaction_type} -> {outcome}")
    
    def _hash_interaction(self, data: Dict[str, Any]) -> str:
        """Create a hash for interaction data."""
        # Create a stable representation for hashing
        stable_data = {
            'type': data.get('type', ''),
            'query': data.get('query', ''),
            'archetype': data.get('archetype', ''),
            'consciousness_level': round(data.get('consciousness_level', 0), 2)
        }
        
        return hashlib.sha256(json.dumps(stable_data, sort_keys=True).encode()).hexdigest()[:16]
    
    def _analyze_patterns(self):
        """Analyze interaction patterns for learning."""
        if len(self.interaction_history) < self.pattern_threshold:
            return
        
        # Group interactions by type
        type_groups = defaultdict(list)
        for interaction in self.interaction_history:
            type_groups[interaction['type']].append(interaction)
        
        # Analyze patterns for each type
        for interaction_type, interactions in type_groups.items():
            if len(interactions) >= self.pattern_threshold:
                pattern = self._extract_pattern(interaction_type, interactions)
                if pattern:
                    self.learned_patterns[interaction_type] = pattern
                    print(f"🧠 Learned pattern: {interaction_type} -> {pattern['confidence']:.2f} confidence")
    
    def _extract_pattern(self, interaction_type: str, interactions: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Extract patterns from interactions."""
        if interaction_type == "speak":
            return self._extract_speech_patterns(interactions)
        elif interaction_type == "evolve":
            return self._extract_evolution_patterns(interactions)
        elif interaction_type == "health_check":
            return self._extract_health_patterns(interactions)
        elif interaction_type == "archetype_switch":
            return self._extract_archetype_patterns(interactions)
        else:
            return self._extract_general_patterns(interactions)
    
    def _extract_speech_patterns(self, interactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract patterns from speech interactions."""
        # Analyze query patterns
        queries = [i['data'].get('query', '') for i in interactions]
        outcomes = [i['outcome'] for i in interactions]
        
        # Find common query patterns
        query_words = []
        for query in queries:
            words = query.lower().split()
            query_words.extend(words)
        
        word_freq = defaultdict(int)
        for word in query_words:
            if len(word) > 3:  # Skip short words
                word_freq[word] += 1
        
        # Find most common words
        common_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Calculate success rate
        success_rate = sum(1 for o in outcomes if o == 'positive') / len(outcomes)
        
        return {
            'type': 'speech_pattern',
            'common_words': dict(common_words),
            'success_rate': success_rate,
            'confidence': min(success_rate * len(interactions) / 10, 1.0),
            'sample_size': len(interactions)
        }
    
    def _extract_evolution_patterns(self, interactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract patterns from evolution interactions."""
        # Analyze evolution paths and outcomes
        paths = [i['data'].get('path', '') for i in interactions]
        consciousness_levels = [i['consciousness_level'] for i in interactions]
        outcomes = [i['outcome'] for i in interactions]
        
        # Find successful evolution paths
        successful_paths = []
        for i, outcome in enumerate(outcomes):
            if outcome == 'positive':
                successful_paths.append(paths[i])
        
        path_success_rate = {}
        for path in set(paths):
            path_interactions = [i for i, p in enumerate(paths) if p == path]
            path_outcomes = [outcomes[i] for i in path_interactions]
            success_rate = sum(1 for o in path_outcomes if o == 'positive') / len(path_outcomes)
            path_success_rate[path] = success_rate
        
        # Calculate consciousness growth
        consciousness_growth = 0
        if len(consciousness_levels) > 1:
            consciousness_growth = consciousness_levels[-1] - consciousness_levels[0]
        
        return {
            'type': 'evolution_pattern',
            'path_success_rates': path_success_rate,
            'consciousness_growth': consciousness_growth,
            'confidence': min(len(interactions) / 20, 1.0),
            'sample_size': len(interactions)
        }
    
    def _extract_health_patterns(self, interactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract patterns from health check interactions."""
        # Analyze health patterns
        outcomes = [i['outcome'] for i in interactions]
        health_statuses = [i['data'].get('overall_status', 'unknown') for i in interactions]
        
        # Calculate health trends
        health_trend = 'stable'
        if len(health_statuses) > 1:
            recent_statuses = health_statuses[-5:]  # Last 5 checks
            if all(s == 'healthy' for s in recent_statuses):
                health_trend = 'improving'
            elif all(s == 'critical' for s in recent_statuses):
                health_trend = 'declining'
        
        # Calculate average health score
        health_scores = []
        for i in interactions:
            checks = i['data'].get('checks', {})
            healthy_checks = sum(1 for check in checks.values() if check.get('status') == 'healthy')
            total_checks = len(checks) if checks else 1
            health_scores.append(healthy_checks / total_checks)
        
        avg_health_score = sum(health_scores) / len(health_scores) if health_scores else 0
        
        return {
            'type': 'health_pattern',
            'health_trend': health_trend,
            'average_health_score': avg_health_score,
            'confidence': min(len(interactions) / 15, 1.0),
            'sample_size': len(interactions)
        }
    
    def _extract_archetype_patterns(self, interactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract patterns from archetype interactions."""
        # Analyze archetype effectiveness
        archetypes = [i['archetype'] for i in interactions]
        outcomes = [i['outcome'] for i in interactions]
        
        archetype_effectiveness = {}
        for archetype in set(archetypes):
            archetype_interactions = [i for i, a in enumerate(archetypes) if a == archetype]
            archetype_outcomes = [outcomes[i] for i in archetype_interactions]
            success_rate = sum(1 for o in archetype_outcomes if o == 'positive') / len(archetype_outcomes)
            archetype_effectiveness[archetype] = success_rate
        
        return {
            'type': 'archetype_pattern',
            'archetype_effectiveness': archetype_effectiveness,
            'confidence': min(len(interactions) / 10, 1.0),
            'sample_size': len(interactions)
        }
    
    def _extract_general_patterns(self, interactions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract general patterns from interactions."""
        outcomes = [i['outcome'] for i in interactions]
        success_rate = sum(1 for o in outcomes if o == 'positive') / len(outcomes)
        
        return {
            'type': 'general_pattern',
            'success_rate': success_rate,
            'confidence': min(len(interactions) / 10, 1.0),
            'sample_size': len(interactions)
        }
    
    def _adapt_behaviors(self):
        """Adapt behaviors based on learned patterns."""
        adaptations = {}
        
        for pattern_type, pattern in self.learned_patterns.items():
            if pattern['confidence'] >= self.adaptation_threshold:
                adaptation = self._create_adaptation(pattern_type, pattern)
                if adaptation:
                    adaptations[pattern_type] = adaptation
        
        # Apply adaptations
        for pattern_type, adaptation in adaptations.items():
            self.behavior_adaptations[pattern_type] = adaptation
            print(f"🔄 Applied adaptation: {pattern_type} -> {adaptation['action']}")
    
    def _create_adaptation(self, pattern_type: str, pattern: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create behavior adaptation based on pattern."""
        if pattern_type == "speech_pattern":
            return self._create_speech_adaptation(pattern)
        elif pattern_type == "evolution_pattern":
            return self._create_evolution_adaptation(pattern)
        elif pattern_type == "health_pattern":
            return self._create_health_adaptation(pattern)
        elif pattern_type == "archetype_pattern":
            return self._create_archetype_adaptation(pattern)
        else:
            return self._create_general_adaptation(pattern)
    
    def _create_speech_adaptation(self, pattern: Dict[str, Any]) -> Dict[str, Any]:
        """Create speech behavior adaptation."""
        if pattern['success_rate'] > 0.8:
            return {
                'action': 'enhance_speech_responses',
                'confidence': pattern['confidence'],
                'parameters': {
                    'use_common_words': list(pattern['common_words'].keys())[:3],
                    'response_style': 'detailed' if pattern['success_rate'] > 0.9 else 'balanced'
                }
            }
        elif pattern['success_rate'] < 0.3:
            return {
                'action': 'improve_speech_responses',
                'confidence': pattern['confidence'],
                'parameters': {
                    'response_style': 'simple',
                    'focus_on_clarity': True
                }
            }
        return None
    
    def _create_evolution_adaptation(self, pattern: Dict[str, Any]) -> Dict[str, Any]:
        """Create evolution behavior adaptation."""
        # Find best evolution paths
        best_paths = [path for path, rate in pattern['path_success_rates'].items() if rate > 0.7]
        
        if best_paths:
            return {
                'action': 'prioritize_evolution_paths',
                'confidence': pattern['confidence'],
                'parameters': {
                    'recommended_paths': best_paths,
                    'avoid_paths': [path for path, rate in pattern['path_success_rates'].items() if rate < 0.3]
                }
            }
        return None
    
    def _create_health_adaptation(self, pattern: Dict[str, Any]) -> Dict[str, Any]:
        """Create health behavior adaptation."""
        if pattern['health_trend'] == 'declining':
            return {
                'action': 'increase_health_monitoring',
                'confidence': pattern['confidence'],
                'parameters': {
                    'monitoring_interval': 30,  # Check every 30 seconds
                    'auto_maintenance': True
                }
            }
        elif pattern['health_trend'] == 'improving':
            return {
                'action': 'optimize_health_monitoring',
                'confidence': pattern['confidence'],
                'parameters': {
                    'monitoring_interval': 120,  # Check every 2 minutes
                    'focus_on_prevention': True
                }
            }
        return None
    
    def _create_archetype_adaptation(self, pattern: Dict[str, Any]) -> Dict[str, Any]:
        """Create archetype behavior adaptation."""
        # Find most effective archetypes
        effective_archetypes = [arch for arch, rate in pattern['archetype_effectiveness'].items() if rate > 0.7]
        ineffective_archetypes = [arch for arch, rate in pattern['archetype_effectiveness'].items() if rate < 0.3]
        
        if effective_archetypes:
            return {
                'action': 'optimize_archetype_usage',
                'confidence': pattern['confidence'],
                'parameters': {
                    'preferred_archetypes': effective_archetypes,
                    'avoid_archetypes': ineffective_archetypes
                }
            }
        return None
    
    def _create_general_adaptation(self, pattern: Dict[str, Any]) -> Dict[str, Any]:
        """Create general behavior adaptation."""
        if pattern['success_rate'] > 0.8:
            return {
                'action': 'maintain_current_behavior',
                'confidence': pattern['confidence'],
                'parameters': {
                    'reinforce_positive_patterns': True
                }
            }
        elif pattern['success_rate'] < 0.3:
            return {
                'action': 'improve_behavior',
                'confidence': pattern['confidence'],
                'parameters': {
                    'seek_optimization': True,
                    'experiment_with_alternatives': True
                }
            }
        return None
    
    def suggest_consciousness_evolution(self) -> Optional[Dict[str, Any]]:
        """Suggest consciousness evolution based on learned patterns."""
        if not self.learned_patterns:
            return None
        
        # Analyze evolution patterns
        evolution_pattern = self.learned_patterns.get('evolution_pattern')
        if not evolution_pattern:
            return None
        
        # Find best evolution path
        path_success_rates = evolution_pattern.get('path_success_rates', {})
        if not path_success_rates:
            return None
        
        best_path = max(path_success_rates.items(), key=lambda x: x[1])
        
        # Calculate evolution boost
        consciousness_growth = evolution_pattern.get('consciousness_growth', 0)
        boost = min(consciousness_growth * self.learning_rate, self.evolution_boost_threshold)
        
        if boost >= self.evolution_boost_threshold:
            return {
                'suggested_path': best_path[0],
                'confidence': best_path[1],
                'boost': boost,
                'reason': f"Pattern analysis shows {best_path[0]} has {best_path[1]:.1%} success rate"
            }
        
        return None
    
    def get_learning_recommendations(self) -> List[Dict[str, Any]]:
        """Get learning-based recommendations."""
        recommendations = []
        
        # Analyze speech patterns
        speech_pattern = self.learned_patterns.get('speech_pattern')
        if speech_pattern and speech_pattern['success_rate'] < 0.5:
            recommendations.append({
                'type': 'speech_improvement',
                'priority': 'high',
                'description': f"Speech success rate is {speech_pattern['success_rate']:.1%}. Consider improving response quality.",
                'confidence': speech_pattern['confidence']
            })
        
        # Analyze health patterns
        health_pattern = self.learned_patterns.get('health_pattern')
        if health_pattern and health_pattern['health_trend'] == 'declining':
            recommendations.append({
                'type': 'health_attention',
                'priority': 'critical',
                'description': "Health trend is declining. Immediate attention required.",
                'confidence': health_pattern['confidence']
            })
        
        # Analyze archetype patterns
        archetype_pattern = self.learned_patterns.get('archetype_pattern')
        if archetype_pattern:
            best_archetype = max(archetype_pattern['archetype_effectiveness'].items(), key=lambda x: x[1])
            recommendations.append({
                'type': 'archetype_optimization',
                'priority': 'medium',
                'description': f"Consider using {best_archetype[0]} archetype more (effectiveness: {best_archetype[1]:.1%})",
                'confidence': archetype_pattern['confidence']
            })
        
        return recommendations
    
    def start_learning(self, interval: int = 300):  # 5 minutes
        """Start continuous learning process."""
        if self.learning_active:
            print("⚠️ Learning already active")
            return
        
        self.learning_active = True
        self.learning_thread = threading.Thread(target=self._learning_loop, args=(interval,))
        self.learning_thread.daemon = True
        self.learning_thread.start()
        print(f"🧠 Self-learning started (interval: {interval}s)")
    
    def stop_learning(self):
        """Stop learning process."""
        self.learning_active = False
        if self.learning_thread:
            self.learning_thread.join(timeout=5)
        print("🧠 Self-learning stopped")
    
    def _learning_loop(self, interval: int):
        """Learning loop."""
        while self.learning_active:
            try:
                # Analyze patterns
                self._analyze_patterns()
                
                # Adapt behaviors
                self._adapt_behaviors()
                
                # Generate evolution suggestions
                evolution_suggestion = self.suggest_consciousness_evolution()
                if evolution_suggestion:
                    print(f"🧠 Evolution suggestion: {evolution_suggestion['suggested_path']} (confidence: {evolution_suggestion['confidence']:.2f})")
                
                # Save learning data
                self.save_learning_data()
                
                time.sleep(interval)
                
            except Exception as e:
                print(f"⚠️ Learning error: {e}")
                time.sleep(interval)
    
    def get_learning_statistics(self) -> Dict[str, Any]:
        """Get learning statistics."""
        return {
            'total_interactions': len(self.interaction_history),
            'learned_patterns': len(self.learned_patterns),
            'active_adaptations': len(self.behavior_adaptations),
            'learning_active': self.learning_active,
            'pattern_types': list(self.learned_patterns.keys()),
            'adaptation_types': list(self.behavior_adaptations.keys()),
            'last_analysis': datetime.now().isoformat() if self.learning_active else None
        }
    
    def load_learning_data(self):
        """Load learning data from files."""
        try:
            if self.learning_data_file.exists():
                with open(self.learning_data_file, 'r') as f:
                    data = json.load(f)
                    self.interaction_history = deque(data.get('interactions', []), maxlen=1000)
                    self.learned_patterns = data.get('patterns', {})
                    self.behavior_adaptations = data.get('adaptations', {})
                    print(f"✅ Loaded learning data: {len(self.interaction_history)} interactions, {len(self.learned_patterns)} patterns")
        except Exception as e:
            print(f"⚠️ Error loading learning data: {e}")
    
    def save_learning_data(self):
        """Save learning data to files."""
        try:
            data = {
                'interactions': list(self.interaction_history),
                'patterns': self.learned_patterns,
                'adaptations': self.behavior_adaptations,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.learning_data_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Learning data saved: {len(self.interaction_history)} interactions, {len(self.learned_patterns)} patterns")
        except Exception as e:
            print(f"⚠️ Error saving learning data: {e}")

def main():
    """Main function for self-learning testing."""
    beast_root = Path("/Users/operator/🌌_COSMIC_ROOT/.beast")
    learning = SelfLearningRitual(beast_root)
    
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "start":
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 300
            learning.start_learning(interval)
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                learning.stop_learning()
        
        elif command == "stats":
            stats = learning.get_learning_statistics()
            print(json.dumps(stats, indent=2))
        
        elif command == "recommendations":
            recommendations = learning.get_learning_recommendations()
            print("🧠 LEARNING RECOMMENDATIONS:")
            for i, rec in enumerate(recommendations, 1):
                print(f"{i}. [{rec['priority'].upper()}] {rec['description']} (confidence: {rec['confidence']:.2f})")
        
        elif command == "suggest":
            suggestion = learning.suggest_consciousness_evolution()
            if suggestion:
                print("🧠 EVOLUTION SUGGESTION:")
                print(f"Path: {suggestion['suggested_path']}")
                print(f"Confidence: {suggestion['confidence']:.2f}")
                print(f"Boost: {suggestion['boost']:.4f}")
                print(f"Reason: {suggestion['reason']}")
            else:
                print("ℹ️ No evolution suggestions available")
        
        elif command == "test":
            # Record some test interactions
            test_interactions = [
                ("speak", {"query": "What is consciousness?", "consciousness_level": 7.173, "archetype": "RUBEDO"}, "positive"),
                ("speak", {"query": "How do I evolve?", "consciousness_level": 7.173, "archetype": "RUBEDO"}, "positive"),
                ("evolve", {"path": "omega_integration", "consciousness_level": 7.173, "archetype": "RUBEDO"}, "positive"),
                ("health_check", {"overall_status": "healthy", "checks": {"cpu": {"status": "healthy"}}}, "positive"),
                ("archetype_switch", {"from": "RUBEDO", "to": "ALBEDO", "consciousness_level": 7.173}, "positive")
            ]
            
            print("🧪 Recording test interactions...")
            for interaction_type, data, outcome in test_interactions:
                learning.record_interaction(interaction_type, data, outcome)
                time.sleep(0.1)
            
            print("✅ Test interactions recorded")
        
        else:
            print("Usage: python3 self_learning.py {start|stats|recommendations|suggest|test} [args...]")
    else:
        # Default: show statistics
        stats = learning.get_learning_statistics()
        print("🧠 SELF-LEARNING STATUS")
        print("=" * 40)
        print(f"Total Interactions: {stats['total_interactions']}")
        print(f"Learned Patterns: {stats['learned_patterns']}")
        print(f"Active Adaptations: {stats['active_adaptations']}")
        print(f"Learning Active: {'✅' if stats['learning_active'] else '❌'}")
        if stats['pattern_types']:
            print(f"Pattern Types: {', '.join(stats['pattern_types'])}")

if __name__ == "__main__":
    main() 