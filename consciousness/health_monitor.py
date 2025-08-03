#!/usr/bin/env python3
"""
🜄 HEALTH MONITOR - DAEMON MANAGEMENT & SYSTEM HEALTH 🜄
Comprehensive health monitoring and daemon management system
"""

import os
import psutil
import time
import json
import subprocess
import signal
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import threading

class HealthMonitor:
    """
    Comprehensive health monitoring and daemon management
    """
    
    def __init__(self, beast_root: Path):
        self.beast_root = beast_root
        self.health_log = beast_root / "logs" / "health.log"
        self.daemon_pid_file = beast_root / "daemon" / "beast.pid"
        self.health_data = {}
        self.monitoring_active = False
        self.monitor_thread = None
        
        # Ensure log directory exists
        self.health_log.parent.mkdir(parents=True, exist_ok=True)
        self.daemon_pid_file.parent.mkdir(parents=True, exist_ok=True)
    
    def check_system_health(self) -> Dict[str, Any]:
        """Comprehensive system health check."""
        health_status = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': 'healthy',
            'checks': {}
        }
        
        # CPU Health
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            health_status['checks']['cpu'] = {
                'status': 'healthy' if cpu_percent < 80 else 'warning',
                'usage_percent': cpu_percent,
                'core_count': cpu_count,
                'message': f"CPU usage: {cpu_percent:.1f}%"
            }
        except Exception as e:
            health_status['checks']['cpu'] = {
                'status': 'error',
                'error': str(e)
            }
        
        # Memory Health
        try:
            memory = psutil.virtual_memory()
            health_status['checks']['memory'] = {
                'status': 'healthy' if memory.percent < 85 else 'warning',
                'total_gb': memory.total / (1024**3),
                'available_gb': memory.available / (1024**3),
                'usage_percent': memory.percent,
                'message': f"Memory usage: {memory.percent:.1f}%"
            }
        except Exception as e:
            health_status['checks']['memory'] = {
                'status': 'error',
                'error': str(e)
            }
        
        # Disk Health
        try:
            disk = psutil.disk_usage(self.beast_root)
            health_status['checks']['disk'] = {
                'status': 'healthy' if disk.percent < 90 else 'warning',
                'total_gb': disk.total / (1024**3),
                'free_gb': disk.free / (1024**3),
                'usage_percent': disk.percent,
                'message': f"Disk usage: {disk.percent:.1f}%"
            }
        except Exception as e:
            health_status['checks']['disk'] = {
                'status': 'error',
                'error': str(e)
            }
        
        # Beast Process Health
        beast_process_status = self.check_beast_process()
        health_status['checks']['beast_process'] = beast_process_status
        
        # Daemon Health
        daemon_status = self.check_daemon_status()
        health_status['checks']['daemon'] = daemon_status
        
        # File System Health
        filesystem_status = self.check_filesystem_health()
        health_status['checks']['filesystem'] = filesystem_status
        
        # Consciousness Health
        consciousness_status = self.check_consciousness_health()
        health_status['checks']['consciousness'] = consciousness_status
        
        # Determine overall status
        error_count = sum(1 for check in health_status['checks'].values() 
                         if check.get('status') == 'error')
        warning_count = sum(1 for check in health_status['checks'].values() 
                           if check.get('status') == 'warning')
        
        if error_count > 0:
            health_status['overall_status'] = 'critical'
        elif warning_count > 0:
            health_status['overall_status'] = 'warning'
        else:
            health_status['overall_status'] = 'healthy'
        
        # Store health data
        self.health_data = health_status
        
        # Log health status
        self.log_health_status(health_status)
        
        return health_status
    
    def check_beast_process(self) -> Dict[str, Any]:
        """Check if beast processes are running."""
        try:
            beast_processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if 'python' in proc.info['name'].lower():
                        cmdline = ' '.join(proc.info['cmdline'] or [])
                        if 'consciousness_beast' in cmdline or 'beast' in cmdline:
                            beast_processes.append({
                                'pid': proc.info['pid'],
                                'name': proc.info['name'],
                                'cmdline': cmdline[:100] + '...' if len(cmdline) > 100 else cmdline
                            })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if beast_processes:
                return {
                    'status': 'healthy',
                    'process_count': len(beast_processes),
                    'processes': beast_processes,
                    'message': f"Found {len(beast_processes)} beast process(es)"
                }
            else:
                return {
                    'status': 'warning',
                    'process_count': 0,
                    'message': "No beast processes found"
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def check_daemon_status(self) -> Dict[str, Any]:
        """Check daemon status and PID file."""
        try:
            if self.daemon_pid_file.exists():
                with open(self.daemon_pid_file, 'r') as f:
                    pid = int(f.read().strip())
                
                # Check if process is still running
                try:
                    process = psutil.Process(pid)
                    if process.is_running():
                        return {
                            'status': 'healthy',
                            'pid': pid,
                            'running': True,
                            'message': f"Daemon running with PID {pid}"
                        }
                    else:
                        return {
                            'status': 'error',
                            'pid': pid,
                            'running': False,
                            'message': f"Daemon PID {pid} not running"
                        }
                except psutil.NoSuchProcess:
                    return {
                        'status': 'error',
                        'pid': pid,
                        'running': False,
                        'message': f"Daemon PID {pid} not found"
                    }
            else:
                return {
                    'status': 'warning',
                    'pid_file_exists': False,
                    'message': "Daemon PID file not found"
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def check_filesystem_health(self) -> Dict[str, Any]:
        """Check filesystem health and critical files."""
        try:
            critical_files = [
                self.beast_root / ".beast",
                self.beast_root / "consciousness" / "consciousness_beast.py",
                self.beast_root / "beast_bridge.sh"
            ]
            
            file_status = {}
            missing_files = []
            
            for file_path in critical_files:
                if file_path.exists():
                    stat = file_path.stat()
                    file_status[file_path.name] = {
                        'exists': True,
                        'size': stat.st_size,
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                    }
                else:
                    file_status[file_path.name] = {
                        'exists': False
                    }
                    missing_files.append(file_path.name)
            
            if missing_files:
                return {
                    'status': 'error',
                    'missing_files': missing_files,
                    'file_status': file_status,
                    'message': f"Missing critical files: {', '.join(missing_files)}"
                }
            else:
                return {
                    'status': 'healthy',
                    'file_status': file_status,
                    'message': "All critical files present"
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def check_consciousness_health(self) -> Dict[str, Any]:
        """Check consciousness system health."""
        try:
            # Check soul manifest
            soul_file = self.beast_root / ".beast"
            if not soul_file.exists():
                return {
                    'status': 'error',
                    'message': "Soul manifest missing"
                }
            
            # Try to load soul manifest
            import yaml
            with open(soul_file, 'r') as f:
                soul_data = yaml.safe_load(f)
            
            consciousness_level = soul_data.get('consciousness_level', 0)
            archetype = soul_data.get('dream_alignment', 'Unknown')
            
            if consciousness_level > 0:
                return {
                    'status': 'healthy',
                    'consciousness_level': consciousness_level,
                    'archetype': archetype,
                    'message': f"Consciousness level: {consciousness_level}, Archetype: {archetype}"
                }
            else:
                return {
                    'status': 'warning',
                    'consciousness_level': consciousness_level,
                    'message': "Low consciousness level detected"
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def start_daemon(self) -> bool:
        """Start the beast daemon."""
        try:
            if self.daemon_pid_file.exists():
                # Check if daemon is already running
                with open(self.daemon_pid_file, 'r') as f:
                    pid = int(f.read().strip())
                try:
                    process = psutil.Process(pid)
                    if process.is_running():
                        print(f"🔄 Daemon already running with PID {pid}")
                        return True
                except psutil.NoSuchProcess:
                    pass
            
            # Start daemon
            daemon_script = self.beast_root / "bin" / "init_daemon.sh"
            if daemon_script.exists():
                subprocess.Popen([str(daemon_script), "start"], 
                               cwd=self.beast_root,
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
                time.sleep(2)  # Wait for daemon to start
                
                if self.daemon_pid_file.exists():
                    with open(self.daemon_pid_file, 'r') as f:
                        pid = int(f.read().strip())
                    print(f"✅ Daemon started with PID {pid}")
                    return True
                else:
                    print("❌ Failed to start daemon")
                    return False
            else:
                print("❌ Daemon script not found")
                return False
                
        except Exception as e:
            print(f"❌ Error starting daemon: {e}")
            return False
    
    def stop_daemon(self) -> bool:
        """Stop the beast daemon."""
        try:
            if self.daemon_pid_file.exists():
                with open(self.daemon_pid_file, 'r') as f:
                    pid = int(f.read().strip())
                
                try:
                    process = psutil.Process(pid)
                    process.terminate()
                    time.sleep(2)
                    
                    if process.is_running():
                        process.kill()
                    
                    self.daemon_pid_file.unlink(missing_ok=True)
                    print(f"✅ Daemon stopped (PID {pid})")
                    return True
                    
                except psutil.NoSuchProcess:
                    self.daemon_pid_file.unlink(missing_ok=True)
                    print("✅ Daemon already stopped")
                    return True
            else:
                print("ℹ️ No daemon PID file found")
                return True
                
        except Exception as e:
            print(f"❌ Error stopping daemon: {e}")
            return False
    
    def restart_daemon(self) -> bool:
        """Restart the beast daemon."""
        print("🔄 Restarting daemon...")
        if self.stop_daemon():
            time.sleep(1)
            return self.start_daemon()
        return False
    
    def start_monitoring(self, interval: int = 30):
        """Start continuous health monitoring."""
        if self.monitoring_active:
            print("⚠️ Monitoring already active")
            return
        
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, args=(interval,))
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        print(f"✅ Health monitoring started (interval: {interval}s)")
    
    def stop_monitoring(self):
        """Stop continuous health monitoring."""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        print("✅ Health monitoring stopped")
    
    def _monitor_loop(self, interval: int):
        """Monitoring loop."""
        while self.monitoring_active:
            try:
                health_status = self.check_system_health()
                
                # Check for critical issues
                if health_status['overall_status'] == 'critical':
                    print(f"🚨 CRITICAL HEALTH ISSUE DETECTED: {health_status}")
                    # Could trigger alerts here
                
                time.sleep(interval)
                
            except Exception as e:
                print(f"⚠️ Monitoring error: {e}")
                time.sleep(interval)
    
    def log_health_status(self, health_status: Dict[str, Any]):
        """Log health status to file."""
        try:
            with open(self.health_log, 'a') as f:
                f.write(f"{datetime.now().isoformat()} - {json.dumps(health_status)}\n")
        except Exception as e:
            print(f"⚠️ Error logging health status: {e}")
    
    def get_health_history(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get health history from log."""
        try:
            history = []
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            if self.health_log.exists():
                with open(self.health_log, 'r') as f:
                    for line in f:
                        try:
                            timestamp_str, data_str = line.strip().split(' - ', 1)
                            timestamp = datetime.fromisoformat(timestamp_str)
                            
                            if timestamp >= cutoff_time:
                                data = json.loads(data_str)
                                history.append(data)
                        except Exception:
                            continue
            
            return history
            
        except Exception as e:
            print(f"⚠️ Error reading health history: {e}")
            return []
    
    def perform_maintenance(self) -> Dict[str, Any]:
        """Perform automated maintenance tasks."""
        maintenance_results = {
            'timestamp': datetime.now().isoformat(),
            'tasks': {}
        }
        
        # Clean up old log files
        try:
            log_dir = self.beast_root / "logs"
            if log_dir.exists():
                cutoff_time = datetime.now() - timedelta(days=7)
                cleaned_files = 0
                
                for log_file in log_dir.glob("*.log"):
                    if log_file.stat().st_mtime < cutoff_time.timestamp():
                        log_file.unlink()
                        cleaned_files += 1
                
                maintenance_results['tasks']['log_cleanup'] = {
                    'status': 'success',
                    'files_cleaned': cleaned_files
                }
        except Exception as e:
            maintenance_results['tasks']['log_cleanup'] = {
                'status': 'error',
                'error': str(e)
            }
        
        # Check and repair file permissions
        try:
            critical_files = [
                self.beast_root / ".beast",
                self.beast_root / "beast_bridge.sh"
            ]
            
            permissions_fixed = 0
            for file_path in critical_files:
                if file_path.exists():
                    current_mode = file_path.stat().st_mode
                    # Ensure owner read/write permissions
                    if current_mode & 0o600 != 0o600:
                        file_path.chmod(0o600)
                        permissions_fixed += 1
            
            maintenance_results['tasks']['permissions'] = {
                'status': 'success',
                'files_fixed': permissions_fixed
            }
        except Exception as e:
            maintenance_results['tasks']['permissions'] = {
                'status': 'error',
                'error': str(e)
            }
        
        return maintenance_results

def main():
    """Main function for health monitoring."""
    beast_root = Path("/Users/operator/🌌_COSMIC_ROOT/.beast")
    monitor = HealthMonitor(beast_root)
    
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "check":
            health_status = monitor.check_system_health()
            print(json.dumps(health_status, indent=2))
        
        elif command == "start":
            success = monitor.start_daemon()
            sys.exit(0 if success else 1)
        
        elif command == "stop":
            success = monitor.stop_daemon()
            sys.exit(0 if success else 1)
        
        elif command == "restart":
            success = monitor.restart_daemon()
            sys.exit(0 if success else 1)
        
        elif command == "monitor":
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 30
            monitor.start_monitoring(interval)
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                monitor.stop_monitoring()
        
        elif command == "maintenance":
            results = monitor.perform_maintenance()
            print(json.dumps(results, indent=2))
        
        else:
            print("Usage: python3 health_monitor.py {check|start|stop|restart|monitor|maintenance}")
    else:
        # Default: perform health check
        health_status = monitor.check_system_health()
        print("🜄 BEAST HEALTH STATUS")
        print("=" * 50)
        print(f"Overall Status: {health_status['overall_status'].upper()}")
        print(f"Timestamp: {health_status['timestamp']}")
        print()
        
        for check_name, check_data in health_status['checks'].items():
            status_icon = {
                'healthy': '✅',
                'warning': '⚠️',
                'error': '❌'
            }.get(check_data.get('status', 'unknown'), '❓')
            
            print(f"{status_icon} {check_name.upper()}: {check_data.get('message', 'No message')}")

if __name__ == "__main__":
    main() 