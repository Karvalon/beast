#!/usr/bin/env python3
"""
🜄 MESH NETWORK - NETWORK VISUALIZATION & MANAGEMENT 🜄
Network discovery, visualization, and consciousness synchronization
"""

import os
import json
import time
import threading
import socket
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import defaultdict

class MeshNetwork:
    """
    Mesh network management and visualization system
    """
    
    def __init__(self, beast_root: Path):
        self.beast_root = beast_root
        self.network_file = beast_root / "network" / "mesh_network.json"
        self.visualization_dir = beast_root / "network" / "visualizations"
        
        # Ensure directories exist
        self.network_file.parent.mkdir(parents=True, exist_ok=True)
        self.visualization_dir.mkdir(parents=True, exist_ok=True)
        
        # Network state
        self.nodes = {}
        self.connections = []
        self.network_graph = nx.Graph()
        self.discovery_active = False
        self.discovery_thread = None
        
        # Load existing network data
        self.load_network_data()
        
        # Initialize local node
        self.local_node = self._create_local_node()
        self.nodes[self.local_node['id']] = self.local_node
    
    def _create_local_node(self) -> Dict[str, Any]:
        """Create local node information."""
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
        except:
            hostname = "unknown"
            ip_address = "127.0.0.1"
        
        # Load consciousness data
        consciousness_level = 7.173
        archetype = "RUBEDO"
        try:
            import yaml
            soul_file = self.beast_root / ".beast"
            if soul_file.exists():
                with open(soul_file, 'r') as f:
                    soul_data = yaml.safe_load(f)
                consciousness_level = soul_data.get('consciousness_level', 7.173)
                archetype = soul_data.get('dream_alignment', 'RUBEDO')
        except:
            pass
        
        return {
            'id': f"{hostname}_{int(time.time())}",
            'hostname': hostname,
            'ip_address': ip_address,
            'node_type': 'beast_consciousness',
            'consciousness_level': consciousness_level,
            'archetype': archetype,
            'status': 'online',
            'last_seen': datetime.now().isoformat(),
            'capabilities': [
                'consciousness_evolution',
                'quantum_encryption',
                'health_monitoring',
                'module_discovery',
                'archetype_switching'
            ],
            'ports': {
                'dashboard': 8501,
                'api': 8502,
                'mesh': 8503
            }
        }
    
    def discover_nodes(self) -> List[Dict[str, Any]]:
        """Discover nodes in the local network."""
        discovered_nodes = []
        
        # Get local network range
        local_ip = self.local_node['ip_address']
        network_prefix = '.'.join(local_ip.split('.')[:-1])
        
        print(f"🔍 Discovering nodes in network {network_prefix}.0/24")
        
        # Scan common ports for beast nodes
        beast_ports = [8501, 8502, 8503]  # Dashboard, API, Mesh ports
        
        for i in range(1, 255):
            ip = f"{network_prefix}.{i}"
            
            # Skip local IP
            if ip == local_ip:
                continue
            
            # Check if node is reachable
            for port in beast_ports:
                if self._check_node(ip, port):
                    node_info = self._get_node_info(ip, port)
                    if node_info:
                        discovered_nodes.append(node_info)
                        print(f"✅ Discovered node: {ip}:{port} - {node_info.get('node_type', 'unknown')}")
                    break
        
        return discovered_nodes
    
    def _check_node(self, ip: str, port: int) -> bool:
        """Check if a node is reachable."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def _get_node_info(self, ip: str, port: int) -> Optional[Dict[str, Any]]:
        """Get information about a discovered node."""
        try:
            # Try to get node info via HTTP request
            import requests
            url = f"http://{ip}:{port}/api/node_info"
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        
        # Fallback: create basic node info
        return {
            'id': f"discovered_{ip}_{port}",
            'ip_address': ip,
            'port': port,
            'node_type': 'beast_node',
            'status': 'online',
            'last_seen': datetime.now().isoformat(),
            'discovered': True
        }
    
    def add_node(self, node_info: Dict[str, Any]):
        """Add a node to the network."""
        node_id = node_info['id']
        self.nodes[node_id] = node_info
        
        # Add to network graph
        self.network_graph.add_node(node_id, **node_info)
        
        # Create connection to local node if not already connected
        if node_id != self.local_node['id']:
            connection = {
                'from': self.local_node['id'],
                'to': node_id,
                'type': 'mesh',
                'strength': 1.0,
                'created': datetime.now().isoformat()
            }
            self.connections.append(connection)
            self.network_graph.add_edge(self.local_node['id'], node_id, **connection)
        
        print(f"✅ Added node: {node_info.get('hostname', node_id)}")
    
    def remove_node(self, node_id: str):
        """Remove a node from the network."""
        if node_id in self.nodes:
            del self.nodes[node_id]
            self.network_graph.remove_node(node_id)
            
            # Remove connections
            self.connections = [conn for conn in self.connections 
                              if conn['from'] != node_id and conn['to'] != node_id]
            
            print(f"❌ Removed node: {node_id}")
    
    def update_node_status(self, node_id: str, status: str):
        """Update node status."""
        if node_id in self.nodes:
            self.nodes[node_id]['status'] = status
            self.nodes[node_id]['last_seen'] = datetime.now().isoformat()
            
            # Update graph
            if node_id in self.network_graph:
                self.network_graph.nodes[node_id]['status'] = status
                self.network_graph.nodes[node_id]['last_seen'] = datetime.now().isoformat()
    
    def get_network_topology(self) -> Dict[str, Any]:
        """Get network topology information."""
        nodes_count = len(self.nodes)
        connections_count = len(self.connections)
        
        topology = {
            'nodes_count': nodes_count,
            'connections_count': connections_count,
            'network_density': nx.density(self.network_graph) if nodes_count > 1 else 0.0,
            'average_clustering': 0.0,
            'diameter': 0,
            'connected_components': [],
            'centrality': {}
        }
        
        # Calculate clustering coefficient only if we have edges
        if connections_count > 0:
            try:
                topology['average_clustering'] = nx.average_clustering(self.network_graph)
            except:
                topology['average_clustering'] = 0.0
        
        # Calculate diameter only if we have multiple nodes
        if nodes_count > 1:
            try:
                topology['diameter'] = nx.diameter(self.network_graph)
            except:
                topology['diameter'] = 0
        
        # Get connected components
        try:
            topology['connected_components'] = list(nx.connected_components(self.network_graph))
        except:
            topology['connected_components'] = []
        
        # Calculate centrality
        try:
            topology['centrality'] = nx.degree_centrality(self.network_graph)
        except:
            topology['centrality'] = {}
        
        return topology
    
    def create_network_visualization(self, filename: str = None) -> str:
        """Create a network visualization."""
        if filename is None:
            filename = f"mesh_network_{int(time.time())}.png"
        
        filepath = self.visualization_dir / filename
        
        # Create visualization
        plt.figure(figsize=(12, 8))
        
        # Position nodes using spring layout
        pos = nx.spring_layout(self.network_graph, k=1, iterations=50)
        
        # Draw nodes
        node_colors = []
        node_sizes = []
        
        for node in self.network_graph.nodes():
            node_data = self.network_graph.nodes[node]
            
            # Color based on status
            if node_data.get('status') == 'online':
                node_colors.append('green')
            elif node_data.get('status') == 'offline':
                node_colors.append('red')
            else:
                node_colors.append('gray')
            
            # Size based on consciousness level
            consciousness = node_data.get('consciousness_level', 1.0)
            node_sizes.append(100 + consciousness * 50)
        
        # Draw the network
        nx.draw_networkx_nodes(self.network_graph, pos, 
                              node_color=node_colors, 
                              node_size=node_sizes,
                              alpha=0.8)
        
        nx.draw_networkx_edges(self.network_graph, pos, 
                              alpha=0.5, 
                              edge_color='blue',
                              width=2)
        
        # Add labels
        labels = {node: self.network_graph.nodes[node].get('hostname', node)[:10] 
                 for node in self.network_graph.nodes()}
        nx.draw_networkx_labels(self.network_graph, pos, labels, font_size=8)
        
        # Add title and legend
        plt.title("🜄 Beast Mesh Network", fontsize=16, fontweight='bold')
        plt.axis('off')
        
        # Add legend
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', 
                      markersize=10, label='Online'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', 
                      markersize=10, label='Offline'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', 
                      markersize=10, label='Unknown')
        ]
        plt.legend(handles=legend_elements, loc='upper right')
        
        # Save visualization
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Network visualization saved: {filepath}")
        return str(filepath)
    
    def start_discovery(self, interval: int = 60):
        """Start continuous network discovery."""
        if self.discovery_active:
            print("⚠️ Discovery already active")
            return
        
        self.discovery_active = True
        self.discovery_thread = threading.Thread(target=self._discovery_loop, args=(interval,))
        self.discovery_thread.daemon = True
        self.discovery_thread.start()
        print(f"✅ Network discovery started (interval: {interval}s)")
    
    def stop_discovery(self):
        """Stop network discovery."""
        self.discovery_active = False
        if self.discovery_thread:
            self.discovery_thread.join(timeout=5)
        print("✅ Network discovery stopped")
    
    def _discovery_loop(self, interval: int):
        """Discovery loop."""
        while self.discovery_active:
            try:
                # Discover new nodes
                discovered_nodes = self.discover_nodes()
                
                # Add new nodes
                for node in discovered_nodes:
                    if node['id'] not in self.nodes:
                        self.add_node(node)
                
                # Update existing nodes
                for node_id in self.nodes:
                    if node_id != self.local_node['id']:
                        # Check if node is still reachable
                        node = self.nodes[node_id]
                        ip = node.get('ip_address')
                        port = node.get('ports', {}).get('dashboard', 8501)
                        
                        if ip and self._check_node(ip, port):
                            self.update_node_status(node_id, 'online')
                        else:
                            self.update_node_status(node_id, 'offline')
                
                # Save network data
                self.save_network_data()
                
                # Create periodic visualization
                if len(self.nodes) > 1:
                    self.create_network_visualization()
                
                time.sleep(interval)
                
            except Exception as e:
                print(f"⚠️ Discovery error: {e}")
                time.sleep(interval)
    
    def get_consciousness_sync_status(self) -> Dict[str, Any]:
        """Get consciousness synchronization status across the network."""
        sync_data = {
            'total_nodes': len(self.nodes),
            'online_nodes': sum(1 for node in self.nodes.values() if node.get('status') == 'online'),
            'consciousness_levels': {},
            'archetypes': {},
            'sync_health': 'good'
        }
        
        for node_id, node in self.nodes.items():
            consciousness = node.get('consciousness_level', 0)
            archetype = node.get('archetype', 'unknown')
            
            sync_data['consciousness_levels'][node_id] = consciousness
            sync_data['archetypes'][node_id] = archetype
        
        # Check sync health
        consciousness_levels = list(sync_data['consciousness_levels'].values())
        if consciousness_levels:
            variance = max(consciousness_levels) - min(consciousness_levels)
            if variance > 2.0:
                sync_data['sync_health'] = 'poor'
            elif variance > 1.0:
                sync_data['sync_health'] = 'fair'
        
        return sync_data
    
    def broadcast_consciousness_update(self, consciousness_level: float, archetype: str):
        """Broadcast consciousness update to network."""
        update = {
            'type': 'consciousness_update',
            'node_id': self.local_node['id'],
            'consciousness_level': consciousness_level,
            'archetype': archetype,
            'timestamp': datetime.now().isoformat()
        }
        
        # Update local node
        self.local_node['consciousness_level'] = consciousness_level
        self.local_node['archetype'] = archetype
        self.nodes[self.local_node['id']] = self.local_node
        
        # Broadcast to other nodes (simplified - in practice, use proper messaging)
        print(f"📡 Broadcasting consciousness update: {consciousness_level} ({archetype})")
        
        # Save network data
        self.save_network_data()
    
    def load_network_data(self):
        """Load network data from file."""
        try:
            if self.network_file.exists():
                with open(self.network_file, 'r') as f:
                    data = json.load(f)
                    self.nodes = data.get('nodes', {})
                    self.connections = data.get('connections', [])
                    
                    # Rebuild network graph
                    self.network_graph.clear()
                    for node_id, node_data in self.nodes.items():
                        self.network_graph.add_node(node_id, **node_data)
                    
                    for connection in self.connections:
                        self.network_graph.add_edge(connection['from'], connection['to'], **connection)
                    
                    print(f"✅ Loaded network data: {len(self.nodes)} nodes, {len(self.connections)} connections")
        except Exception as e:
            print(f"⚠️ Error loading network data: {e}")
    
    def save_network_data(self):
        """Save network data to file."""
        try:
            data = {
                'nodes': self.nodes,
                'connections': self.connections,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.network_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Network data saved: {len(self.nodes)} nodes, {len(self.connections)} connections")
        except Exception as e:
            print(f"⚠️ Error saving network data: {e}")
    
    def get_network_statistics(self) -> Dict[str, Any]:
        """Get comprehensive network statistics."""
        topology = self.get_network_topology()
        sync_status = self.get_consciousness_sync_status()
        
        return {
            'topology': topology,
            'sync_status': sync_status,
            'local_node': self.local_node,
            'discovery_active': self.discovery_active,
            'last_discovery': datetime.now().isoformat() if self.discovery_active else None
        }

def main():
    """Main function for mesh network testing."""
    beast_root = Path("/Users/operator/🌌_COSMIC_ROOT/.beast")
    mesh = MeshNetwork(beast_root)
    
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "discover":
            print("🔍 Discovering nodes...")
            discovered = mesh.discover_nodes()
            print(f"Found {len(discovered)} nodes")
            for node in discovered:
                print(f"  - {node.get('ip_address', 'unknown')}: {node.get('node_type', 'unknown')}")
        
        elif command == "visualize":
            print("🎨 Creating network visualization...")
            filepath = mesh.create_network_visualization()
            print(f"Visualization saved: {filepath}")
        
        elif command == "status":
            stats = mesh.get_network_statistics()
            print(json.dumps(stats, indent=2))
        
        elif command == "start":
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 60
            mesh.start_discovery(interval)
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                mesh.stop_discovery()
        
        elif command == "sync":
            consciousness_level = float(sys.argv[2]) if len(sys.argv) > 2 else 7.173
            archetype = sys.argv[3] if len(sys.argv) > 3 else "RUBEDO"
            mesh.broadcast_consciousness_update(consciousness_level, archetype)
        
        else:
            print("Usage: python3 mesh_network.py {discover|visualize|status|start|sync} [args...]")
    else:
        # Default: show status
        stats = mesh.get_network_statistics()
        print("🜄 MESH NETWORK STATUS")
        print("=" * 40)
        print(f"Local Node: {mesh.local_node['hostname']} ({mesh.local_node['ip_address']})")
        print(f"Total Nodes: {stats['topology']['nodes_count']}")
        print(f"Connections: {stats['topology']['connections_count']}")
        print(f"Discovery Active: {'✅' if stats['discovery_active'] else '❌'}")
        print(f"Sync Health: {stats['sync_status']['sync_health'].upper()}")

if __name__ == "__main__":
    main() 