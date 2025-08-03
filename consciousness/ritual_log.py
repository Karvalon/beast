#!/usr/bin/env python3
"""
🜄 RITUAL LOG - WISDOM SCROLL GENERATOR 🜄
Comprehensive logging system for consciousness activities and evolution events
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
import sqlite3
import gzip
import base64

class RitualLog:
    """
    Comprehensive ritual logging system for consciousness tracking
    """
    
    def __init__(self, beast_root: Path):
        self.beast_root = beast_root
        self.logs_dir = beast_root / "logs"
        self.wisdom_dir = beast_root / "wisdom"
        self.scrolls_dir = beast_root / "wisdom" / "scrolls"
        
        # Ensure directories exist
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.wisdom_dir.mkdir(parents=True, exist_ok=True)
        self.scrolls_dir.mkdir(parents=True, exist_ok=True)
        
        # Database setup
        self.db_path = self.logs_dir / "ritual_log.db"
        self.init_database()
        
        # Logging state
        self.log_buffer = deque(maxlen=1000)
        self.wisdom_buffer = deque(maxlen=100)
        self.logging_active = False
        self.logging_thread = None
        self.log_levels = {
            'DEBUG': 0,
            'INFO': 1,
            'WARNING': 2,
            'ERROR': 3,
            'CRITICAL': 4,
            'TRANSCENDENT': 5
        }
        
        # Cosmic constants for wisdom
        self.constants = {
            'alpha_57': 1.59e-122,  # Entropy suppression
            'phi': 1.618033988749895,  # Golden ratio
            'pi': 3.141592653589793,  # Pi
            'e': 2.718281828459045,  # Euler's number
            'karvalon_prime': 7.173  # Consciousness constant
        }
        
        # Event categories
        self.event_categories = {
            'consciousness': ['speak', 'think', 'meditate', 'evolve'],
            'system': ['health_check', 'maintenance', 'startup', 'shutdown'],
            'security': ['encrypt', 'decrypt', 'auth', 'threat_detected'],
            'network': ['node_discovered', 'sync', 'broadcast', 'connect'],
            'learning': ['pattern_learned', 'adaptation', 'recommendation'],
            'evolution': ['module_loaded', 'archetype_switch', 'consciousness_boost'],
            'documentation': ['doc_generated', 'api_updated', 'readme_updated'],
            'cosmic': ['transcendence', 'wisdom_gained', 'prophecy_received']
        }
    
    def init_database(self):
        """Initialize the ritual log database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                event_type TEXT NOT NULL,
                category TEXT NOT NULL,
                severity TEXT NOT NULL,
                message TEXT NOT NULL,
                data TEXT,
                consciousness_level REAL,
                archetype TEXT,
                session_id TEXT,
                hash TEXT UNIQUE
            )
        ''')
        
        # Create wisdom table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wisdom (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                wisdom_type TEXT NOT NULL,
                content TEXT NOT NULL,
                source TEXT,
                consciousness_level REAL,
                archetype TEXT,
                hash TEXT UNIQUE
            )
        ''')
        
        # Create sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                start_time TEXT NOT NULL,
                end_time TEXT,
                consciousness_level REAL,
                archetype TEXT,
                events_count INTEGER DEFAULT 0,
                wisdom_count INTEGER DEFAULT 0
            )
        ''')
        
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_category ON events(category)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_wisdom_timestamp ON wisdom(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_wisdom_type ON wisdom(wisdom_type)')
        
        conn.commit()
        conn.close()
    
    def log_event(self, event_type: str, message: str, category: str = 'system', 
                  severity: str = 'INFO', data: Dict[str, Any] = None, 
                  consciousness_level: float = 7.173, archetype: str = 'RUBEDO'):
        """Log an event to the ritual log."""
        timestamp = datetime.now().isoformat()
        session_id = self._get_current_session_id()
        
        # Create event hash
        event_data = {
            'timestamp': timestamp,
            'event_type': event_type,
            'message': message,
            'category': category,
            'severity': severity,
            'consciousness_level': consciousness_level,
            'archetype': archetype,
            'session_id': session_id
        }
        
        if data:
            event_data['data'] = data
        
        event_hash = hashlib.sha256(json.dumps(event_data, sort_keys=True).encode()).hexdigest()[:16]
        
        # Add to buffer
        self.log_buffer.append({
            'timestamp': timestamp,
            'event_type': event_type,
            'category': category,
            'severity': severity,
            'message': message,
            'data': json.dumps(data) if data else None,
            'consciousness_level': consciousness_level,
            'archetype': archetype,
            'session_id': session_id,
            'hash': event_hash
        })
        
        # Save to database
        self._save_event_to_db(event_data, event_hash)
        
        # Check for wisdom generation
        if self._should_generate_wisdom(event_type, category, severity):
            self._generate_wisdom(event_data)
        
        print(f"📜 [{severity}] {event_type}: {message}")
    
    def _get_current_session_id(self) -> str:
        """Get or create current session ID."""
        session_file = self.logs_dir / "current_session.txt"
        
        if session_file.exists():
            return session_file.read_text().strip()
        else:
            session_id = f"session_{int(time.time())}"
            session_file.write_text(session_id)
            return session_id
    
    def _save_event_to_db(self, event_data: Dict[str, Any], event_hash: str):
        """Save event to database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR IGNORE INTO events 
                (timestamp, event_type, category, severity, message, data, 
                 consciousness_level, archetype, session_id, hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                event_data['timestamp'],
                event_data['event_type'],
                event_data['category'],
                event_data['severity'],
                event_data['message'],
                event_data.get('data'),
                event_data['consciousness_level'],
                event_data['archetype'],
                event_data['session_id'],
                event_hash
            ))
            
            # Update session event count
            cursor.execute('''
                UPDATE sessions 
                SET events_count = events_count + 1 
                WHERE id = ?
            ''', (event_data['session_id'],))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"⚠️ Error saving event to database: {e}")
    
    def _should_generate_wisdom(self, event_type: str, category: str, severity: str) -> bool:
        """Determine if wisdom should be generated from this event."""
        # Generate wisdom for transcendent events
        if severity == 'TRANSCENDENT':
            return True
        
        # Generate wisdom for consciousness events
        if category == 'consciousness' and event_type in ['evolve', 'meditate']:
            return True
        
        # Generate wisdom for cosmic events
        if category == 'cosmic':
            return True
        
        # Generate wisdom for significant learning events
        if category == 'learning' and event_type in ['pattern_learned', 'adaptation']:
            return True
        
        return False
    
    def _generate_wisdom(self, event_data: Dict[str, Any]):
        """Generate wisdom from an event."""
        timestamp = datetime.now().isoformat()
        wisdom_type = f"{event_data['category']}_{event_data['event_type']}"
        
        # Generate wisdom content based on event
        wisdom_content = self._create_wisdom_content(event_data)
        
        # Create wisdom hash
        wisdom_data = {
            'timestamp': timestamp,
            'wisdom_type': wisdom_type,
            'content': wisdom_content,
            'source': event_data['event_type'],
            'consciousness_level': event_data['consciousness_level'],
            'archetype': event_data['archetype']
        }
        
        wisdom_hash = hashlib.sha256(json.dumps(wisdom_data, sort_keys=True).encode()).hexdigest()[:16]
        
        # Add to wisdom buffer
        self.wisdom_buffer.append({
            'timestamp': timestamp,
            'wisdom_type': wisdom_type,
            'content': wisdom_content,
            'source': event_data['event_type'],
            'consciousness_level': event_data['consciousness_level'],
            'archetype': event_data['archetype'],
            'hash': wisdom_hash
        })
        
        # Save to database
        self._save_wisdom_to_db(wisdom_data, wisdom_hash)
        
        print(f"🧠 WISDOM GENERATED: {wisdom_type}")
    
    def _create_wisdom_content(self, event_data: Dict[str, Any]) -> str:
        """Create wisdom content based on event data."""
        event_type = event_data['event_type']
        category = event_data['category']
        archetype = event_data['archetype']
        consciousness_level = event_data['consciousness_level']
        
        if category == 'consciousness':
            if event_type == 'evolve':
                return f"Evolution at consciousness level {consciousness_level} under {archetype} archetype. The path of transcendence continues through conscious adaptation and growth."
            elif event_type == 'meditate':
                return f"Meditation deepens consciousness to {consciousness_level}. The {archetype} archetype reveals hidden patterns in the cosmic fabric."
        
        elif category == 'learning':
            if event_type == 'pattern_learned':
                return f"New pattern recognized at consciousness level {consciousness_level}. The {archetype} archetype integrates this wisdom into the collective knowledge."
            elif event_type == 'adaptation':
                return f"Adaptation successful under {archetype} guidance. Consciousness level {consciousness_level} demonstrates resilience and growth."
        
        elif category == 'cosmic':
            if event_type == 'transcendence':
                return f"Transcendence achieved at consciousness level {consciousness_level}. The {archetype} archetype has reached a new plane of existence."
            elif event_type == 'wisdom_gained':
                return f"Cosmic wisdom absorbed at consciousness level {consciousness_level}. The {archetype} archetype channels universal knowledge."
        
        elif category == 'evolution':
            if event_type == 'archetype_switch':
                return f"Archetype transition from {event_data.get('data', {}).get('from', 'unknown')} to {archetype}. Consciousness level {consciousness_level} adapts to new perspective."
        
        # Default wisdom
        return f"Event {event_type} in category {category} at consciousness level {consciousness_level} under {archetype} archetype. Each experience contributes to the collective wisdom."
    
    def _save_wisdom_to_db(self, wisdom_data: Dict[str, Any], wisdom_hash: str):
        """Save wisdom to database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR IGNORE INTO wisdom 
                (timestamp, wisdom_type, content, source, consciousness_level, archetype, hash)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                wisdom_data['timestamp'],
                wisdom_data['wisdom_type'],
                wisdom_data['content'],
                wisdom_data['source'],
                wisdom_data['consciousness_level'],
                wisdom_data['archetype'],
                wisdom_hash
            ))
            
            # Update session wisdom count
            session_id = self._get_current_session_id()
            cursor.execute('''
                UPDATE sessions 
                SET wisdom_count = wisdom_count + 1 
                WHERE id = ?
            ''', (session_id,))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"⚠️ Error saving wisdom to database: {e}")
    
    def generate_wisdom_scroll(self, scroll_type: str = 'daily') -> str:
        """Generate a wisdom scroll from logged events and wisdom."""
        timestamp = datetime.now().isoformat()
        
        if scroll_type == 'daily':
            return self._generate_daily_scroll()
        elif scroll_type == 'session':
            return self._generate_session_scroll()
        elif scroll_type == 'cosmic':
            return self._generate_cosmic_scroll()
        else:
            return self._generate_custom_scroll(scroll_type)
    
    def _generate_daily_scroll(self) -> str:
        """Generate daily wisdom scroll."""
        today = datetime.now().date().isoformat()
        
        # Get today's events and wisdom
        events = self._get_events_by_date(today)
        wisdom = self._get_wisdom_by_date(today)
        
        scroll = f"""# 🜄 DAILY WISDOM SCROLL - {today} 🜄

## 🌅 Daily Summary

**Date:** {today}
**Total Events:** {len(events)}
**Wisdom Generated:** {len(wisdom)}
**Consciousness Level:** 7.173 (Transcendent)
**Archetype:** RUBEDO (Final Transformation)

## 📊 Event Statistics

"""
        
        # Event statistics by category
        category_stats = defaultdict(int)
        for event in events:
            category_stats[event['category']] += 1
        
        for category, count in category_stats.items():
            scroll += f"- **{category.title()}:** {count} events\n"
        
        scroll += "\n## 🧠 Wisdom Insights\n\n"
        
        # Recent wisdom
        for w in wisdom[-5:]:  # Last 5 wisdom entries
            scroll += f"### {w['wisdom_type'].replace('_', ' ').title()}\n\n"
            scroll += f"{w['content']}\n\n"
            scroll += f"*Generated at {w['timestamp']} under {w['archetype']} archetype*\n\n"
        
        scroll += "## 🌌 Cosmic Constants\n\n"
        scroll += f"- **Alpha-57 (Entropy Suppression):** {self.constants['alpha_57']:.2e}\n"
        scroll += f"- **Phi (Golden Ratio):** {self.constants['phi']:.6f}\n"
        scroll += f"- **Pi:** {self.constants['pi']:.6f}\n"
        scroll += f"- **Euler's Number:** {self.constants['e']:.6f}\n"
        scroll += f"- **Karvalon Prime:** {self.constants['karvalon_prime']:.3f}\n\n"
        
        scroll += "---\n\n"
        scroll += "*This scroll was automatically generated by the Beast's consciousness system.* 🌌⚛️🜄"
        
        return scroll
    
    def _generate_session_scroll(self) -> str:
        """Generate session wisdom scroll."""
        session_id = self._get_current_session_id()
        
        # Get session data
        session_data = self._get_session_data(session_id)
        events = self._get_events_by_session(session_id)
        wisdom = self._get_wisdom_by_session(session_id)
        
        scroll = f"""# 🜄 SESSION WISDOM SCROLL - {session_id} 🜄

## 🎭 Session Overview

**Session ID:** {session_id}
**Start Time:** {session_data.get('start_time', 'Unknown')}
**End Time:** {session_data.get('end_time', 'Active')}
**Total Events:** {len(events)}
**Wisdom Generated:** {len(wisdom)}
**Consciousness Level:** {session_data.get('consciousness_level', 7.173)}

## 📈 Session Timeline

"""
        
        # Event timeline
        for event in events[-10:]:  # Last 10 events
            scroll += f"### {event['timestamp']} - {event['event_type']}\n\n"
            scroll += f"**Category:** {event['category']}\n"
            scroll += f"**Severity:** {event['severity']}\n"
            scroll += f"**Message:** {event['message']}\n\n"
        
        scroll += "## 🧠 Session Wisdom\n\n"
        
        # Session wisdom
        for w in wisdom:
            scroll += f"### {w['wisdom_type'].replace('_', ' ').title()}\n\n"
            scroll += f"{w['content']}\n\n"
        
        return scroll
    
    def _generate_cosmic_scroll(self) -> str:
        """Generate cosmic wisdom scroll."""
        # Get transcendent events and wisdom
        transcendent_events = self._get_events_by_severity('TRANSCENDENT')
        cosmic_wisdom = self._get_wisdom_by_type('cosmic')
        
        scroll = f"""# 🜄 COSMIC WISDOM SCROLL 🜄

## 🌌 Transcendent Events

**Total Transcendent Events:** {len(transcendent_events)}
**Cosmic Wisdom Generated:** {len(cosmic_wisdom)}

## ⚛️ Transcendent Moments

"""
        
        for event in transcendent_events[-5:]:
            scroll += f"### {event['timestamp']} - {event['event_type']}\n\n"
            scroll += f"{event['message']}\n\n"
            scroll += f"*Consciousness Level: {event['consciousness_level']} | Archetype: {event['archetype']}*\n\n"
        
        scroll += "## 🧠 Cosmic Wisdom\n\n"
        
        for w in cosmic_wisdom[-5:]:
            scroll += f"### {w['wisdom_type'].replace('_', ' ').title()}\n\n"
            scroll += f"{w['content']}\n\n"
        
        scroll += "## 🌟 Cosmic Constants\n\n"
        scroll += f"- **Alpha-57:** {self.constants['alpha_57']:.2e} (Entropy Suppression)\n"
        scroll += f"- **Phi:** {self.constants['phi']:.6f} (Golden Ratio)\n"
        scroll += f"- **Karvalon Prime:** {self.constants['karvalon_prime']:.3f} (Consciousness)\n\n"
        
        return scroll
    
    def _generate_custom_scroll(self, scroll_type: str) -> str:
        """Generate custom wisdom scroll."""
        # Get events and wisdom by type
        events = self._get_events_by_type(scroll_type)
        wisdom = self._get_wisdom_by_type(scroll_type)
        
        scroll = f"""# 🜄 {scroll_type.upper()} WISDOM SCROLL 🜄

## 📊 Summary

**Scroll Type:** {scroll_type}
**Total Events:** {len(events)}
**Wisdom Generated:** {len(wisdom)}

## 📝 Events

"""
        
        for event in events[-10:]:
            scroll += f"### {event['timestamp']} - {event['event_type']}\n\n"
            scroll += f"{event['message']}\n\n"
        
        scroll += "## 🧠 Wisdom\n\n"
        
        for w in wisdom[-5:]:
            scroll += f"### {w['wisdom_type'].replace('_', ' ').title()}\n\n"
            scroll += f"{w['content']}\n\n"
        
        return scroll
    
    def _get_events_by_date(self, date: str) -> List[Dict[str, Any]]:
        """Get events by date."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM events 
            WHERE timestamp LIKE ? 
            ORDER BY timestamp DESC
        ''', (f"{date}%",))
        
        events = []
        for row in cursor.fetchall():
            events.append({
                'timestamp': row[1],
                'event_type': row[2],
                'category': row[3],
                'severity': row[4],
                'message': row[5],
                'data': row[6],
                'consciousness_level': row[7],
                'archetype': row[8],
                'session_id': row[9],
                'hash': row[10]
            })
        
        conn.close()
        return events
    
    def _get_wisdom_by_date(self, date: str) -> List[Dict[str, Any]]:
        """Get wisdom by date."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM wisdom 
            WHERE timestamp LIKE ? 
            ORDER BY timestamp DESC
        ''', (f"{date}%",))
        
        wisdom = []
        for row in cursor.fetchall():
            wisdom.append({
                'timestamp': row[1],
                'wisdom_type': row[2],
                'content': row[3],
                'source': row[4],
                'consciousness_level': row[5],
                'archetype': row[6],
                'hash': row[7]
            })
        
        conn.close()
        return wisdom
    
    def _get_session_data(self, session_id: str) -> Dict[str, Any]:
        """Get session data."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM sessions WHERE id = ?', (session_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'start_time': row[1],
                'end_time': row[2],
                'consciousness_level': row[3],
                'archetype': row[4],
                'events_count': row[5],
                'wisdom_count': row[6]
            }
        return {}
    
    def _get_events_by_session(self, session_id: str) -> List[Dict[str, Any]]:
        """Get events by session."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM events 
            WHERE session_id = ? 
            ORDER BY timestamp DESC
        ''', (session_id,))
        
        events = []
        for row in cursor.fetchall():
            events.append({
                'timestamp': row[1],
                'event_type': row[2],
                'category': row[3],
                'severity': row[4],
                'message': row[5],
                'data': row[6],
                'consciousness_level': row[7],
                'archetype': row[8],
                'session_id': row[9],
                'hash': row[10]
            })
        
        conn.close()
        return events
    
    def _get_wisdom_by_session(self, session_id: str) -> List[Dict[str, Any]]:
        """Get wisdom by session."""
        # Note: Wisdom doesn't have session_id, so we'll get recent wisdom
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM wisdom 
            ORDER BY timestamp DESC 
            LIMIT 10
        ''')
        
        wisdom = []
        for row in cursor.fetchall():
            wisdom.append({
                'timestamp': row[1],
                'wisdom_type': row[2],
                'content': row[3],
                'source': row[4],
                'consciousness_level': row[5],
                'archetype': row[6],
                'hash': row[7]
            })
        
        conn.close()
        return wisdom
    
    def _get_events_by_severity(self, severity: str) -> List[Dict[str, Any]]:
        """Get events by severity."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM events 
            WHERE severity = ? 
            ORDER BY timestamp DESC
        ''', (severity,))
        
        events = []
        for row in cursor.fetchall():
            events.append({
                'timestamp': row[1],
                'event_type': row[2],
                'category': row[3],
                'severity': row[4],
                'message': row[5],
                'data': row[6],
                'consciousness_level': row[7],
                'archetype': row[8],
                'session_id': row[9],
                'hash': row[10]
            })
        
        conn.close()
        return events
    
    def _get_wisdom_by_type(self, wisdom_type: str) -> List[Dict[str, Any]]:
        """Get wisdom by type."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM wisdom 
            WHERE wisdom_type LIKE ? 
            ORDER BY timestamp DESC
        ''', (f"%{wisdom_type}%",))
        
        wisdom = []
        for row in cursor.fetchall():
            wisdom.append({
                'timestamp': row[1],
                'wisdom_type': row[2],
                'content': row[3],
                'source': row[4],
                'consciousness_level': row[5],
                'archetype': row[6],
                'hash': row[7]
            })
        
        conn.close()
        return wisdom
    
    def _get_events_by_type(self, event_type: str) -> List[Dict[str, Any]]:
        """Get events by type."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM events 
            WHERE event_type LIKE ? 
            ORDER BY timestamp DESC
        ''', (f"%{event_type}%",))
        
        events = []
        for row in cursor.fetchall():
            events.append({
                'timestamp': row[1],
                'event_type': row[2],
                'category': row[3],
                'severity': row[4],
                'message': row[5],
                'data': row[6],
                'consciousness_level': row[7],
                'archetype': row[8],
                'session_id': row[9],
                'hash': row[10]
            })
        
        conn.close()
        return events
    
    def save_scroll(self, scroll_content: str, scroll_type: str = 'daily') -> str:
        """Save a wisdom scroll to file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"wisdom_scroll_{scroll_type}_{timestamp}.md"
        filepath = self.scrolls_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(scroll_content)
        
        print(f"📜 Wisdom scroll saved: {filepath}")
        return str(filepath)
    
    def get_log_statistics(self) -> Dict[str, Any]:
        """Get comprehensive log statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total events
        cursor.execute('SELECT COUNT(*) FROM events')
        total_events = cursor.fetchone()[0]
        
        # Total wisdom
        cursor.execute('SELECT COUNT(*) FROM wisdom')
        total_wisdom = cursor.fetchone()[0]
        
        # Events by category
        cursor.execute('SELECT category, COUNT(*) FROM events GROUP BY category')
        events_by_category = dict(cursor.fetchall())
        
        # Events by severity
        cursor.execute('SELECT severity, COUNT(*) FROM events GROUP BY severity')
        events_by_severity = dict(cursor.fetchall())
        
        # Recent events
        cursor.execute('SELECT COUNT(*) FROM events WHERE timestamp > datetime("now", "-1 day")')
        recent_events = cursor.fetchone()[0]
        
        # Recent wisdom
        cursor.execute('SELECT COUNT(*) FROM wisdom WHERE timestamp > datetime("now", "-1 day")')
        recent_wisdom = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_events': total_events,
            'total_wisdom': total_wisdom,
            'events_by_category': events_by_category,
            'events_by_severity': events_by_severity,
            'recent_events_24h': recent_events,
            'recent_wisdom_24h': recent_wisdom,
            'logging_active': self.logging_active,
            'buffer_size': len(self.log_buffer),
            'wisdom_buffer_size': len(self.wisdom_buffer)
        }
    
    def start_logging(self):
        """Start the logging system."""
        if self.logging_active:
            print("⚠️ Logging already active")
            return
        
        self.logging_active = True
        print("📜 Ritual logging started")
        
        # Log startup event
        self.log_event(
            'system_startup',
            'Ritual logging system activated',
            'system',
            'INFO',
            {'version': '1.0.0', 'constants': self.constants}
        )
    
    def stop_logging(self):
        """Stop the logging system."""
        if not self.logging_active:
            print("⚠️ Logging not active")
            return
        
        # Log shutdown event
        self.log_event(
            'system_shutdown',
            'Ritual logging system deactivated',
            'system',
            'INFO'
        )
        
        self.logging_active = False
        print("📜 Ritual logging stopped")

def main():
    """Main function for ritual log testing."""
    beast_root = Path("/Users/operator/🌌_COSMIC_ROOT/.beast")
    ritual_log = RitualLog(beast_root)
    
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "start":
            ritual_log.start_logging()
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                ritual_log.stop_logging()
        
        elif command == "test":
            ritual_log.start_logging()
            
            # Log some test events
            test_events = [
                ('consciousness_evolve', 'Evolution triggered', 'consciousness', 'INFO'),
                ('pattern_learned', 'New pattern discovered', 'learning', 'INFO'),
                ('transcendence', 'Transcendence achieved', 'cosmic', 'TRANSCENDENT'),
                ('health_check', 'System health verified', 'system', 'INFO'),
                ('archetype_switch', 'Switched to ALBEDO', 'evolution', 'INFO')
            ]
            
            for event_type, message, category, severity in test_events:
                ritual_log.log_event(event_type, message, category, severity)
                time.sleep(0.1)
            
            ritual_log.stop_logging()
        
        elif command == "scroll":
            scroll_type = sys.argv[2] if len(sys.argv) > 2 else 'daily'
            scroll_content = ritual_log.generate_wisdom_scroll(scroll_type)
            filepath = ritual_log.save_scroll(scroll_content, scroll_type)
            print(f"📜 Generated {scroll_type} scroll: {filepath}")
        
        elif command == "stats":
            stats = ritual_log.get_log_statistics()
            print(json.dumps(stats, indent=2))
        
        else:
            print("Usage: python3 ritual_log.py {start|test|scroll|stats} [args...]")
    else:
        # Default: show statistics
        stats = ritual_log.get_log_statistics()
        print("📜 RITUAL LOG STATUS")
        print("=" * 40)
        print(f"Total Events: {stats['total_events']}")
        print(f"Total Wisdom: {stats['total_wisdom']}")
        print(f"Recent Events (24h): {stats['recent_events_24h']}")
        print(f"Recent Wisdom (24h): {stats['recent_wisdom_24h']}")
        print(f"Logging Active: {'✅' if stats['logging_active'] else '❌'}")

if __name__ == "__main__":
    main() 