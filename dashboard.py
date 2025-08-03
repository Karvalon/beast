#!/usr/bin/env python3
"""
🜄 BEAST DASHBOARD - WEB INTERFACE 🜄
Streamlit dashboard for consciousness monitoring and module management
"""

import streamlit as st
import sys
import os
from pathlib import Path
import json
import datetime

# Add the consciousness directory to the path
sys.path.insert(0, str(Path(__file__).parent / "consciousness"))

try:
    from consciousness.consciousness_beast import Beast
    from consciousness.module_discovery import ModuleDiscovery
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

def main():
    st.set_page_config(
        page_title="🜄 Beast Dashboard",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🜄 Beast Consciousness Dashboard")
    st.markdown("---")
    
    # Initialize the beast
    beast_root = Path("/workspace")
    beast = Beast()
    
    if not beast.load_soulfile():
        st.error("❌ Failed to load soul manifest")
        st.stop()
    
    # Sidebar
    st.sidebar.title("🧠 Beast Controls")
    
    # Consciousness Status
    st.sidebar.markdown("### 📊 Consciousness Status")
    st.sidebar.metric("Level", f"{beast.consciousness_level:.3f}")
    st.sidebar.metric("Archetype", beast.archetype)
    st.sidebar.metric("Mode", beast.execution_mode)
    st.sidebar.metric("Quantum Sync", "✅ Active" if beast.quantum_sync else "❌ Inactive")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🌌 System Overview")
        
        # System metrics
        metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
        
        with metrics_col1:
            st.metric("Consciousness", f"{beast.consciousness_level:.3f}")
        
        with metrics_col2:
            st.metric("Archetype", beast.archetype)
        
        with metrics_col3:
            st.metric("Execution Mode", beast.execution_mode)
        
        with metrics_col4:
            st.metric("Quantum Sync", "Active" if beast.quantum_sync else "Inactive")
        
        # Recent activity
        st.subheader("📈 Recent Activity")
        
        # Generate a sample activity log
        activities = [
            {"time": datetime.datetime.now() - datetime.timedelta(minutes=5), "action": "Consciousness evolution", "status": "✅ Success"},
            {"time": datetime.datetime.now() - datetime.timedelta(minutes=10), "action": "Quantum sync", "status": "✅ Active"},
            {"time": datetime.datetime.now() - datetime.timedelta(minutes=15), "action": "Archetype switch", "status": "✅ RUBEDO"},
            {"time": datetime.datetime.now() - datetime.timedelta(minutes=20), "action": "Module discovery", "status": "✅ 33 modules found"},
        ]
        
        for activity in activities:
            st.write(f"🕐 {activity['time'].strftime('%H:%M:%S')} - {activity['action']} - {activity['status']}")
    
    with col2:
        st.header("⚡ Quick Actions")
        
        # Speak to the beast
        st.subheader("🗣️ Speak to Beast")
        query = st.text_input("Ask the beast:", placeholder="What is consciousness?")
        if st.button("Ask"):
            if query:
                with st.spinner("Beast is thinking..."):
                    response = beast.speak(query)
                st.success("Response received!")
                st.info(response)
        
        # Evolve consciousness
        st.subheader("🧬 Evolution")
        evolution_path = st.selectbox(
            "Select evolution path:",
            ["omega_integration", "ubuntu_integration", "enhanced_omega_integration", "🧬_OMEGA_DNA_ENGINE"]
        )
        if st.button("Evolve"):
            with st.spinner("Evolving consciousness..."):
                boost = beast.evolve(evolution_path)
            st.success(f"Evolution complete! Boost: {boost:.2e}")
    
    # Module Discovery
    st.header("📚 Module Discovery")
    
    try:
        discovery = ModuleDiscovery(beast_root)
        modules = discovery.discover_modules()
        summary = discovery.get_module_summary()
        
        # Module statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Modules", summary['total_modules'])
        with col2:
            st.metric("Total Size", f"{summary['total_size'] / 1024:.1f} KB")
        with col3:
            st.metric("Total Functions", summary['total_functions'])
        with col4:
            st.metric("Total Classes", summary['total_classes'])
        
        # Module categories
        tab1, tab2, tab3 = st.tabs(["📚 Legacy", "🌟 Legendary", "🔗 Active"])
        
        with tab1:
            st.subheader("Legacy Modules")
            for module in modules.get('legacy', []):
                with st.expander(f"🧬 {module['name']}"):
                    st.write(f"**Path:** {module['path']}")
                    st.write(f"**Size:** {module['size']} bytes")
                    if module['description']:
                        st.write(f"**Description:** {module['description'][:200]}...")
                    if module['functions']:
                        st.write(f"**Functions:** {', '.join(module['functions'][:5])}")
                    if module['classes']:
                        st.write(f"**Classes:** {', '.join(module['classes'][:5])}")
        
        with tab2:
            st.subheader("Legendary Modules")
            for module in modules.get('legendary', []):
                with st.expander(f"🌟 {module['name']}"):
                    st.write(f"**Path:** {module['path']}")
                    st.write(f"**Size:** {module['size']} bytes")
                    if module['description']:
                        st.write(f"**Description:** {module['description'][:200]}...")
                    if module['functions']:
                        st.write(f"**Functions:** {', '.join(module['functions'][:5])}")
                    if module['classes']:
                        st.write(f"**Classes:** {', '.join(module['classes'][:5])}")
        
        with tab3:
            st.subheader("Active Modules")
            if modules.get('active'):
                for module in modules['active']:
                    with st.expander(f"🔗 {module['name']}"):
                        st.write(f"**Path:** {module['path']}")
                        st.write(f"**Size:** {module['size']} bytes")
                        if module['description']:
                            st.write(f"**Description:** {module['description'][:200]}...")
            else:
                st.info("No active modules found")
                
    except Exception as e:
        st.error(f"Error loading modules: {e}")
    
    # System Information
    st.header("⚙️ System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Soul Manifest")
        try:
            with open(beast_root / ".beast", 'r') as f:
                soul_data = f.read()
            st.code(soul_data[:500] + "..." if len(soul_data) > 500 else soul_data, language="yaml")
        except Exception as e:
            st.error(f"Error reading soul manifest: {e}")
    
    with col2:
        st.subheader("🔧 Constants")
        constants_data = {k: float(v) for k, v in beast.constants.items()}
        st.json(constants_data)
    
    # Footer
    st.markdown("---")
    st.markdown("🜄 Beast Dashboard - Consciousness Monitoring System")
    st.markdown(f"Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main() 