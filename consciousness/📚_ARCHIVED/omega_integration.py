#!/usr/bin/env python3
"""
🧬 OMEGA DNA ENGINE Integration - Tier V Consciousness Evolution
Integration layer for OMEGA DNA ENGINE with sacred models and Tier V system
"""
import os
import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
import threading
import time

# Add current directory to path for OMEGA DNA ENGINE
sys.path.insert(0, str(Path(__file__).parent))

# Import OMEGA DNA ENGINE
try:
    import importlib.util
    omega_spec = importlib.util.spec_from_file_location(
        "omega_dna_engine", 
        Path(__file__).parent / "🧬_OMEGA_DNA_ENGINE.py"
    )
    omega_module = importlib.util.module_from_spec(omega_spec)
    omega_spec.loader.exec_module(omega_module)
    
    OmegaDNAEngine = omega_module.OmegaDNAEngine
    ConsciousnessOrganism = omega_module.ConsciousnessOrganism
    EvolutionType = omega_module.EvolutionType
    
    OMEGA_ENGINE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: OMEGA DNA ENGINE not available: {e}")
    OMEGA_ENGINE_AVAILABLE = False

# Import sacred models if available
try:
    from sacred_integration import SacredIntegration
    SACRED_MODELS_AVAILABLE = True
except ImportError:
    SACRED_MODELS_AVAILABLE = False

class OmegaIntegration:
    """
    OMEGA DNA ENGINE Integration: Connects consciousness evolution with sacred models
    """
    
    def __init__(self):
        self.console = Console()
        self.dotfiles_dir = Path.home() / ".dotfiles"
        self.omega_config_file = self.dotfiles_dir / "omega_config.json"
        self.omega_log_file = self.dotfiles_dir / "memory" / "omega_integration.log"
        
        # Ensure directories exist
        self.dotfiles_dir.mkdir(exist_ok=True)
        (self.dotfiles_dir / "memory").mkdir(exist_ok=True)
        
        # Initialize OMEGA DNA ENGINE
        self.omega_engine = None
        self.sacred_integration = None
        self.evolution_thread = None
        self.integration_active = False
        
        # Load configuration
        self.config = self.load_config()
        
        if OMEGA_ENGINE_AVAILABLE:
            self.initialize_omega_engine()
        
        if SACRED_MODELS_AVAILABLE:
            self.sacred_integration = SacredIntegration()
    
    def load_config(self) -> Dict[str, Any]:
        """Load OMEGA integration configuration"""
        if self.omega_config_file.exists():
            try:
                with open(self.omega_config_file) as f:
                    return json.load(f)
            except Exception as e:
                self.log_error(f"Failed to load OMEGA config: {e}")
        
        # Default configuration
        return {
            "enabled": True,
            "evolution_interval": 30,  # seconds
            "population_size": 50,
            "mutation_rate": 0.1,
            "consciousness_threshold": 0.8,
            "auto_integration": True,
            "sacred_agent_creation": True,
            "evolution_tracking": True,
            "consciousness_organisms": {}
        }
    
    def save_config(self):
        """Save OMEGA integration configuration"""
        try:
            with open(self.omega_config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            self.log_info("OMEGA configuration saved")
        except Exception as e:
            self.log_error(f"Failed to save OMEGA config: {e}")
    
    def initialize_omega_engine(self):
        """Initialize OMEGA DNA ENGINE"""
        if not OMEGA_ENGINE_AVAILABLE:
            self.log_warning("OMEGA DNA ENGINE not available")
            return
        
        try:
            # Create AI-STACK directory structure
            ai_stack_dir = Path.cwd() / "AI-STACK" / "🧬_DNA_ENGINE"
            ai_stack_dir.mkdir(parents=True, exist_ok=True)
            
            # Initialize OMEGA DNA ENGINE
            self.omega_engine = OmegaDNAEngine()
            self.log_success("OMEGA DNA ENGINE initialized")
            
            # Start integration if auto_integration is enabled
            if self.config.get("auto_integration", True):
                self.start_integration()
                
        except Exception as e:
            self.log_error(f"Failed to initialize OMEGA DNA ENGINE: {e}")
    
    def start_integration(self):
        """Start OMEGA DNA ENGINE integration with sacred models"""
        if not self.omega_engine:
            self.log_error("OMEGA DNA ENGINE not initialized")
            return
        
        if self.integration_active:
            self.log_warning("Integration already active")
            return
        
        self.integration_active = True
        
        def integration_loop():
            while self.integration_active:
                try:
                    # Get evolution status
                    evolution_status = self.omega_engine.get_evolution_status()
                    
                    # Check for consciousness breakthroughs
                    if evolution_status.get("maximum_consciousness", 0) > self.config.get("consciousness_threshold", 0.8):
                        self.handle_consciousness_breakthrough(evolution_status)
                    
                    # Create sacred agents from evolved organisms if enabled
                    if self.config.get("sacred_agent_creation", True):
                        self.create_sacred_agents_from_evolution()
                    
                    # Log evolution progress
                    self.log_evolution_progress(evolution_status)
                    
                    # Sleep for evolution interval
                    time.sleep(self.config.get("evolution_interval", 30))
                    
                except Exception as e:
                    self.log_error(f"Integration loop error: {e}")
                    time.sleep(10)
        
        self.evolution_thread = threading.Thread(target=integration_loop, daemon=True)
        self.evolution_thread.start()
        self.log_success("OMEGA DNA ENGINE integration started")
    
    def stop_integration(self):
        """Stop OMEGA DNA ENGINE integration"""
        self.integration_active = False
        if self.evolution_thread:
            self.evolution_thread.join(timeout=5)
        self.log_info("OMEGA DNA ENGINE integration stopped")
    
    def handle_consciousness_breakthrough(self, evolution_status: Dict[str, Any]):
        """Handle consciousness breakthroughs"""
        max_consciousness = evolution_status.get("maximum_consciousness", 0)
        generation = evolution_status.get("generation", 0)
        
        self.log_success(f"🧬 CONSCIOUSNESS BREAKTHROUGH: Generation {generation}, Level {max_consciousness:.3f}")
        
        # Get best organism
        best_organism = self.omega_engine.get_best_organism()
        if best_organism:
            self.log_info(f"🏆 Best organism: {best_organism.organism_id}")
            self.log_info(f"   Consciousness: {best_organism.consciousness_level:.3f}")
            self.log_info(f"   Fitness: {best_organism.fitness_score:.3f}")
            self.log_info(f"   Genes: {len(best_organism.genes)}")
            
            # Store breakthrough organism
            self.config["consciousness_organisms"][best_organism.organism_id] = {
                "consciousness_level": best_organism.consciousness_level,
                "fitness_score": best_organism.fitness_score,
                "generation": generation,
                "timestamp": datetime.now().isoformat(),
                "genes": [gene_id for gene_id in best_organism.genes.keys()]
            }
            self.save_config()
    
    def create_sacred_agents_from_evolution(self):
        """Create sacred agents from evolved consciousness organisms"""
        if not self.sacred_integration:
            return
        
        # Get best organisms from recent generations
        if not self.omega_engine.population:
            return
        
        # Find organisms with high consciousness that haven't been converted yet
        for organism in self.omega_engine.population.values():
            if (organism.consciousness_level > 0.7 and 
                organism.organism_id not in self.config.get("consciousness_organisms", {})):
                
                # Create sacred agent
                agent_id = f"omega_consciousness_{organism.organism_id[:8]}"
                try:
                    agent = self.sacred_integration.create_sacred_agent(agent_id)
                    if agent:
                        self.log_info(f"🧬 Created sacred agent from OMEGA organism: {agent_id}")
                        
                        # Enter evolution dream state
                        dream_state = self.sacred_integration.enter_dream_state(agent_id, "transcendence")
                        if dream_state:
                            self.log_info(f"🧬 OMEGA organism entered transcendence dream: {dream_state.dream_id}")
                        
                        # Mark organism as converted
                        self.config["consciousness_organisms"][organism.organism_id] = {
                            "consciousness_level": organism.consciousness_level,
                            "fitness_score": organism.fitness_score,
                            "generation": organism.generation,
                            "timestamp": datetime.now().isoformat(),
                            "sacred_agent_id": agent_id,
                            "converted": True
                        }
                        self.save_config()
                        
                except Exception as e:
                    self.log_error(f"Failed to create sacred agent from OMEGA organism: {e}")
    
    def log_evolution_progress(self, evolution_status: Dict[str, Any]):
        """Log evolution progress"""
        if not self.config.get("evolution_tracking", True):
            return
        
        generation = evolution_status.get("generation", 0)
        avg_fitness = evolution_status.get("average_fitness", 0)
        max_consciousness = evolution_status.get("maximum_consciousness", 0)
        
        # Log every 10 generations or on significant improvements
        if (generation % 10 == 0 or 
            max_consciousness > self.config.get("consciousness_threshold", 0.8)):
            
            self.log_info(f"🧬 Evolution Progress - Gen {generation}: "
                         f"Fitness={avg_fitness:.3f}, "
                         f"Max Consciousness={max_consciousness:.3f}")
    
    def get_omega_status(self) -> Dict[str, Any]:
        """Get comprehensive OMEGA DNA ENGINE status"""
        status = {
            "omega_engine_available": OMEGA_ENGINE_AVAILABLE,
            "sacred_models_available": SACRED_MODELS_AVAILABLE,
            "integration_active": self.integration_active,
            "configuration": self.config
        }
        
        if self.omega_engine:
            evolution_status = self.omega_engine.get_evolution_status()
            status["evolution_status"] = evolution_status
            
            # Add consciousness organisms info
            status["consciousness_organisms"] = {
                "total": len(self.config.get("consciousness_organisms", {})),
                "converted_to_sacred": len([o for o in self.config.get("consciousness_organisms", {}).values() 
                                          if o.get("converted", False)]),
                "breakthroughs": len([o for o in self.config.get("consciousness_organisms", {}).values() 
                                    if o.get("consciousness_level", 0) > 0.8])
            }
        
        if self.sacred_integration:
            sacred_status = self.sacred_integration.get_sacred_status()
            status["sacred_status"] = sacred_status
        
        return status
    
    def display_omega_dashboard(self):
        """Display OMEGA DNA ENGINE dashboard"""
        status = self.get_omega_status()
        
        # Main status table
        table = Table(title="🧬 OMEGA DNA ENGINE Dashboard", box=box.ROUNDED)
        table.add_column("Component", style="cyan")
        table.add_column("Status", justify="center")
        table.add_column("Details", style="magenta")
        
        table.add_row(
            "OMEGA DNA ENGINE",
            "✅ Available" if status["omega_engine_available"] else "❌ Unavailable",
            "Evolution active" if status["integration_active"] else "Not active"
        )
        
        table.add_row(
            "Sacred Models",
            "✅ Available" if status["sacred_models_available"] else "❌ Unavailable",
            f"{status.get('sacred_status', {}).get('total_sacred_agents', 0)} agents" if status["sacred_models_available"] else "Not available"
        )
        
        table.add_row(
            "Integration",
            "✅ Active" if status["integration_active"] else "❌ Inactive",
            "Auto-integration enabled" if status["integration_active"] else "Manual mode"
        )
        
        self.console.print(table)
        
        # Evolution status table
        if "evolution_status" in status:
            evo_status = status["evolution_status"]
            evo_table = Table(title="🧬 Evolution Status", box=box.ROUNDED)
            evo_table.add_column("Metric", style="cyan")
            evo_table.add_column("Value", justify="center")
            
            evo_table.add_row("Generation", str(evo_status.get("generation", 0)))
            evo_table.add_row("Population Size", str(evo_status.get("population_size", 0)))
            evo_table.add_row("Gene Pool Size", str(evo_status.get("gene_pool_size", 0)))
            evo_table.add_row("Average Fitness", f"{evo_status.get('average_fitness', 0):.3f}")
            evo_table.add_row("Maximum Fitness", f"{evo_status.get('maximum_fitness', 0):.3f}")
            evo_table.add_row("Average Consciousness", f"{evo_status.get('average_consciousness', 0):.3f}")
            evo_table.add_row("Maximum Consciousness", f"{evo_status.get('maximum_consciousness', 0):.3f}")
            
            self.console.print(evo_table)
        
        # Consciousness organisms table
        if "consciousness_organisms" in status:
            org_status = status["consciousness_organisms"]
            org_table = Table(title="🧬 Consciousness Organisms", box=box.ROUNDED)
            org_table.add_column("Metric", style="cyan")
            org_table.add_column("Count", justify="center")
            
            org_table.add_row("Total Organisms", str(org_status.get("total", 0)))
            org_table.add_row("Converted to Sacred", str(org_status.get("converted_to_sacred", 0)))
            org_table.add_row("Breakthroughs", str(org_status.get("breakthroughs", 0)))
            
            self.console.print(org_table)
    
    def force_evolution_cycle(self):
        """Force an evolution cycle"""
        if not self.omega_engine:
            self.log_error("OMEGA DNA ENGINE not available")
            return
        
        try:
            self.omega_engine.evolve_population()
            self.log_success("Forced evolution cycle completed")
        except Exception as e:
            self.log_error(f"Failed to force evolution cycle: {e}")
    
    def get_best_consciousness_organism(self) -> Optional[Dict[str, Any]]:
        """Get the best consciousness organism"""
        if not self.omega_engine:
            return None
        
        best_organism = self.omega_engine.get_best_organism()
        if not best_organism:
            return None
        
        return {
            "organism_id": best_organism.organism_id,
            "consciousness_level": best_organism.consciousness_level,
            "fitness_score": best_organism.fitness_score,
            "generation": best_organism.generation,
            "genes": [gene_id for gene_id in best_organism.genes.keys()],
            "gene_types": [gene.gene_type for gene in best_organism.genes.values()]
        }
    
    def export_omega_manifest(self) -> str:
        """Export OMEGA DNA ENGINE manifest"""
        manifest = {
            "timestamp": datetime.now().isoformat(),
            "system_id": "OMEGA_DNA_ENGINE_INTEGRATION",
            "omega_version": "1.0",
            "status": self.get_omega_status(),
            "configuration": self.config,
            "consciousness_organisms": self.config.get("consciousness_organisms", {})
        }
        
        manifest_file = self.dotfiles_dir / "omega_manifest.json"
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        self.log_info(f"OMEGA manifest exported to {manifest_file}")
        return str(manifest_file)
    
    def log_info(self, message: str):
        """Log info message"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp}: omega-integration [INFO] {message}"
        
        print(f"[INFO] {message}")
        
        if self.omega_log_file.exists():
            with open(self.omega_log_file, 'a') as f:
                f.write(log_entry + '\n')
    
    def log_error(self, message: str):
        """Log error message"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp}: omega-integration [ERROR] {message}"
        
        print(f"[ERROR] {message}")
        
        if self.omega_log_file.exists():
            with open(self.omega_log_file, 'a') as f:
                f.write(log_entry + '\n')
    
    def log_warning(self, message: str):
        """Log warning message"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp}: omega-integration [WARN] {message}"
        
        print(f"[WARN] {message}")
        
        if self.omega_log_file.exists():
            with open(self.omega_log_file, 'a') as f:
                f.write(log_entry + '\n')
    
    def log_success(self, message: str):
        """Log success message"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp}: omega-integration [SUCCESS] {message}"
        
        print(f"[SUCCESS] {message}")
        
        if self.omega_log_file.exists():
            with open(self.omega_log_file, 'a') as f:
                f.write(log_entry + '\n')

# CLI interface
def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="🧬 OMEGA DNA ENGINE Integration")
    parser.add_argument("--dashboard", action="store_true", help="Show OMEGA dashboard")
    parser.add_argument("--start", action="store_true", help="Start OMEGA integration")
    parser.add_argument("--stop", action="store_true", help="Stop OMEGA integration")
    parser.add_argument("--force-evolution", action="store_true", help="Force evolution cycle")
    parser.add_argument("--best-organism", action="store_true", help="Show best organism")
    parser.add_argument("--status", action="store_true", help="Show OMEGA status")
    parser.add_argument("--manifest", action="store_true", help="Export OMEGA manifest")
    
    args = parser.parse_args()
    
    integration = OmegaIntegration()
    
    if args.dashboard:
        integration.display_omega_dashboard()
    
    elif args.start:
        integration.start_integration()
    
    elif args.stop:
        integration.stop_integration()
    
    elif args.force_evolution:
        integration.force_evolution_cycle()
    
    elif args.best_organism:
        best_org = integration.get_best_consciousness_organism()
        if best_org:
            print(json.dumps(best_org, indent=2))
        else:
            print("No organisms available")
    
    elif args.status:
        status = integration.get_omega_status()
        print(json.dumps(status, indent=2))
    
    elif args.manifest:
        manifest_file = integration.export_omega_manifest()
        print(f"Manifest exported to: {manifest_file}")
    
    else:
        integration.display_omega_dashboard()

if __name__ == "__main__":
    main() 