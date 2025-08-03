#!/usr/bin/env python3
"""
Test script for enhanced archetype functionality
"""

import sys
import os
sys.path.insert(0, '.')

from consciousness.consciousness_beast import Beast

def test_archetype(archetype_name, test_query):
    """Test a specific archetype with a query."""
    print(f"\n🧪 TESTING ARCHETYPE: {archetype_name}")
    print("=" * 50)
    
    beast = Beast()
    beast.load_soulfile()
    
    # Temporarily switch archetype for testing
    original_archetype = beast.archetype
    beast.archetype = archetype_name
    
    print(f"Switched from {original_archetype} to {archetype_name}")
    beast.speak(test_query)
    
    # Restore original archetype
    beast.archetype = original_archetype

def main():
    """Test all enhanced archetypes."""
    print("🜄 ENHANCED ARCHETYPE TESTING")
    print("=" * 60)
    
    # Test cases for each archetype
    test_cases = [
        ("ALBEDO", "run a diagnostic check on the system"),
        ("NIGREDO", "heal and repair the system"),
        ("Guardian", "scan for security threats"),
        ("Healer", "check system health and balance"),
        ("Explorer", "discover new modules and capabilities"),
        ("Sage", "analyze wisdom and contemplate the system")
    ]
    
    for archetype, query in test_cases:
        test_archetype(archetype, query)
    
    print("\n✅ ARCHETYPE TESTING COMPLETE")

if __name__ == "__main__":
    main() 