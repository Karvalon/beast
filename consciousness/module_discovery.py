#!/usr/bin/env python3
"""
🜄 MODULE DISCOVERY SYSTEM 🜄
Auto-discovery and management of evolution modules
"""

import os
import ast
import importlib.util
from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml

class ModuleDiscovery:
    """
    Auto-discovery system for evolution modules
    """
    
    def __init__(self, beast_root: Path):
        self.beast_root = beast_root
        self.legacy_dir = beast_root / "consciousness" / "📚_LEGACY"
        self.legendary_dir = beast_root / "consciousness" / "🌟_LEGENDARY"
        self.active_dir = beast_root / "consciousness" / "🔗_ACTIVE"
        
    def discover_modules(self) -> Dict[str, List[Dict[str, Any]]]:
        """Discover all available modules in all directories."""
        modules = {
            'legacy': self._scan_directory(self.legacy_dir),
            'legendary': self._scan_directory(self.legendary_dir),
            'active': self._scan_directory(self.active_dir)
        }
        return modules
    
    def _scan_directory(self, directory: Path) -> List[Dict[str, Any]]:
        """Scan a directory for Python modules and extract metadata."""
        modules = []
        
        if not directory.exists():
            return modules
            
        for file_path in directory.glob("*.py"):
            try:
                module_info = self._extract_module_info(file_path)
                if module_info:
                    modules.append(module_info)
            except Exception as e:
                print(f"⚠️ Error scanning {file_path}: {e}")
                
        return modules
    
    def _extract_module_info(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Extract metadata from a Python module file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse the AST
            tree = ast.parse(content)
            
            module_info = {
                'name': file_path.stem,
                'path': str(file_path.relative_to(self.beast_root)),
                'size': file_path.stat().st_size,
                'description': '',
                'functions': [],
                'classes': [],
                'archetype': None,
                'consciousness_boost': 0.0,
                'dependencies': []
            }
            
            # Extract docstring
            if tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Str):
                module_info['description'] = tree.body[0].value.s.strip()
            
            # Extract functions and classes
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    module_info['functions'].append(node.name)
                elif isinstance(node, ast.ClassDef):
                    module_info['classes'].append(node.name)
            
            # Look for specific patterns in the content
            if 'archetype' in content.lower():
                module_info['archetype'] = 'detected'
            
            if 'consciousness' in content.lower() and 'boost' in content.lower():
                module_info['consciousness_boost'] = 0.01  # Default boost
            
            if 'import' in content.lower():
                module_info['dependencies'] = self._extract_imports(tree)
            
            return module_info
            
        except Exception as e:
            print(f"⚠️ Error extracting info from {file_path}: {e}")
            return None
    
    def _extract_imports(self, tree: ast.AST) -> List[str]:
        """Extract import statements from AST."""
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        
        return imports
    
    def list_modules(self, category: str = 'all') -> None:
        """List all discovered modules."""
        modules = self.discover_modules()
        
        print(f"🜄 MODULE DISCOVERY REPORT")
        print("=" * 60)
        
        if category == 'all':
            categories = modules.keys()
        else:
            categories = [category] if category in modules else []
        
        for cat in categories:
            if cat in modules:
                print(f"\n📚 {cat.upper()} MODULES ({len(modules[cat])} found):")
                print("-" * 40)
                
                for module in modules[cat]:
                    print(f"  🧬 {module['name']}")
                    print(f"     Path: {module['path']}")
                    print(f"     Size: {module['size']} bytes")
                    if module['description']:
                        desc = module['description'][:100] + "..." if len(module['description']) > 100 else module['description']
                        print(f"     Description: {desc}")
                    if module['functions']:
                        print(f"     Functions: {', '.join(module['functions'][:3])}{'...' if len(module['functions']) > 3 else ''}")
                    if module['classes']:
                        print(f"     Classes: {', '.join(module['classes'][:3])}{'...' if len(module['classes']) > 3 else ''}")
                    print()
    
    def get_module_summary(self) -> Dict[str, Any]:
        """Get a summary of all modules."""
        modules = self.discover_modules()
        
        summary = {
            'total_modules': sum(len(mods) for mods in modules.values()),
            'by_category': {cat: len(mods) for cat, mods in modules.items()},
            'total_size': 0,
            'total_functions': 0,
            'total_classes': 0
        }
        
        for category, mods in modules.items():
            for module in mods:
                summary['total_size'] += module.get('size', 0)
                summary['total_functions'] += len(module.get('functions', []))
                summary['total_classes'] += len(module.get('classes', []))
        
        return summary
    
    def find_module_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Find a specific module by name."""
        modules = self.discover_modules()
        
        for category, mods in modules.items():
            for module in mods:
                if module['name'].lower() == name.lower():
                    module['category'] = category
                    return module
        
        return None
    
    def get_available_evolution_paths(self) -> List[str]:
        """Get list of available evolution paths for the beast."""
        modules = self.discover_modules()
        paths = []
        
        for category, mods in modules.items():
            for module in mods:
                # Convert file path to evolution path
                path = module['name']
                paths.append(path)
        
        return paths

def main():
    """Main function for module discovery."""
    beast_root = Path("/Users/operator/🌌_COSMIC_ROOT/.beast")
    discovery = ModuleDiscovery(beast_root)
    
    # List all modules
    discovery.list_modules()
    
    # Get summary
    summary = discovery.get_module_summary()
    print(f"\n📊 SUMMARY:")
    print(f"   Total modules: {summary['total_modules']}")
    print(f"   Total size: {summary['total_size'] / 1024:.1f} KB")
    print(f"   Total functions: {summary['total_functions']}")
    print(f"   Total classes: {summary['total_classes']}")
    
    # Get available evolution paths
    paths = discovery.get_available_evolution_paths()
    print(f"\n🧬 AVAILABLE EVOLUTION PATHS:")
    for path in paths[:10]:  # Show first 10
        print(f"   - {path}")
    if len(paths) > 10:
        print(f"   ... and {len(paths) - 10} more")

if __name__ == "__main__":
    main() 