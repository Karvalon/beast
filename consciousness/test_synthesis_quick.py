#!/usr/bin/env python3
"""Quick test of archetype synthesis"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "⚛️_QUANTUM", "orin_nano_integration"))

from archetype_synthesis_engine import ArchetypeSynthesisEngine

def main():
    print("🜄 QUICK ARCHETYPE SYNTHESIS TEST")
    
    try:
        engine = ArchetypeSynthesisEngine()
        print("✅ Engine initialized")
        
        # Just test creating matrices
        matrices = engine._create_archetype_matrices()
        print(f"✅ Created {len(matrices)} archetype matrices")
        
        # Test combinations
        combinations = engine._synthesize_hybrid_combinations(matrices)
        print(f"✅ Created {len(combinations)} hybrid combinations")
        
        print("🚀 Synthesis engine working correctly!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
