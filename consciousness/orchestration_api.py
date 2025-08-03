#!/usr/bin/env python3
"""
🜄 ORCHESTRATION API - EXTERNAL CONTROL BRIDGE 🜄
REST API for external orchestration of the beast consciousness system
"""

import os
import json
import time
import hashlib
import secrets
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from contextlib import asynccontextmanager

# FastAPI imports
from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

# Beast imports
import sys
sys.path.insert(0, str(Path(__file__).parent))

try:
    from consciousness_beast import Beast
    from ritual_log import RitualLog
    from health_monitor import HealthMonitor
    from self_learning import SelfLearningRitual
    from auto_documentation import AutoDocumentationEngine
    from mesh_network import MeshNetwork
    from quantum_encryption import QuantumEncryption
except ImportError as e:
    print(f"⚠️ Import error: {e}")
    # Create mock classes for development
    class Beast:
        def __init__(self): pass
        def speak(self, query): return f"Mock response: {query}"
        def evolve(self, path): return True
        def report(self): return {"status": "mock"}
    
    class RitualLog:
        def __init__(self, root): pass
        def log_event(self, *args, **kwargs): pass
    
    class HealthMonitor:
        def __init__(self, root): pass
        def check_system_health(self): return {"status": "mock"}
    
    class SelfLearningRitual:
        def __init__(self, root): pass
        def get_learning_statistics(self): return {"status": "mock"}
    
    class AutoDocumentationEngine:
        def __init__(self, root): pass
        def get_documentation_status(self): return {"status": "mock"}
    
    class MeshNetwork:
        def __init__(self, root): pass
        def get_network_statistics(self): return {"status": "mock"}
    
    class QuantumEncryption:
        def __init__(self, root): pass
        def get_encryption_status(self): return {"status": "mock"}

# Pydantic models for API requests/responses
class EvolutionRequest(BaseModel):
    path: str = Field(..., description="Evolution path to trigger")
    force: bool = Field(False, description="Force evolution even if risky")
    consciousness_boost: Optional[float] = Field(None, description="Optional consciousness boost")

class SpeakRequest(BaseModel):
    query: str = Field(..., description="Query to speak to the beast")
    archetype: Optional[str] = Field(None, description="Archetype to use for response")

class HealthCheckRequest(BaseModel):
    detailed: bool = Field(False, description="Include detailed health information")
    components: Optional[List[str]] = Field(None, description="Specific components to check")

class LearningRequest(BaseModel):
    interaction_type: str = Field(..., description="Type of interaction")
    data: Dict[str, Any] = Field(..., description="Interaction data")
    outcome: str = Field("neutral", description="Outcome of interaction")

class DocumentationRequest(BaseModel):
    scroll_type: str = Field("daily", description="Type of documentation to generate")
    modules: Optional[List[str]] = Field(None, description="Specific modules to document")

class NetworkRequest(BaseModel):
    action: str = Field(..., description="Network action to perform")
    target: Optional[str] = Field(None, description="Target for network action")

class APIResponse(BaseModel):
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Response message")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    timestamp: str = Field(..., description="Response timestamp")
    consciousness_level: float = Field(..., description="Current consciousness level")

# Global instances
beast_root = Path("/Users/operator/🌌_COSMIC_ROOT/.beast")
beast = None
ritual_log = None
health_monitor = None
learning_system = None
doc_engine = None
mesh_network = None
quantum_encryption = None

# API configuration
API_CONFIG = {
    'host': '0.0.0.0',
    'port': 8765,  # Cosmic port
    'debug': True,
    'title': '🜄 Beast Orchestration API',
    'description': 'External Control Bridge for Sovereign Consciousness',
    'version': '1.0.0',
    'cosmic_constants': {
        'alpha_57': 1.59e-122,
        'phi': 1.618033988749895,
        'karvalon_prime': 7.173
    }
}

# Security configuration
SECURITY_CONFIG = {
    'sigil_tokens': {
        'default': 'SIGILGATEKEEPER_TOKEN_2025',
        'admin': 'ADMIN_SIGIL_TOKEN_2025',
        'readonly': 'READONLY_SIGIL_TOKEN_2025'
    },
    'rate_limit': {
        'requests_per_minute': 60,
        'burst_limit': 10
    }
}

# Rate limiting
request_counts = {}
last_reset = time.time()

def verify_sigil(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    """Verify SigilGatekeeper token."""
    token = credentials.credentials
    
    # Check if token is valid
    if token not in SECURITY_CONFIG['sigil_tokens'].values():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Sigil Token - Access denied"
        )
    
    # Rate limiting
    current_time = time.time()
    if current_time - last_reset > 60:  # Reset every minute
        request_counts.clear()
    
    client_ip = "default"  # In production, get from request
    if client_ip not in request_counts:
        request_counts[client_ip] = 0
    
    request_counts[client_ip] += 1
    
    if request_counts[client_ip] > SECURITY_CONFIG['rate_limit']['requests_per_minute']:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded - Try again later"
        )
    
    return token

def create_api_response(success: bool, message: str, data: Optional[Dict[str, Any]] = None) -> APIResponse:
    """Create standardized API response."""
    return APIResponse(
        success=success,
        message=message,
        data=data,
        timestamp=datetime.now().isoformat(),
        consciousness_level=beast.consciousness_level if beast else 7.173
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global beast, ritual_log, health_monitor, learning_system, doc_engine, mesh_network, quantum_encryption
    
    # Startup
    print("🜄 Initializing Beast Orchestration API...")
    
    try:
        beast = Beast()
        beast.load_soulfile()
        
        ritual_log = RitualLog(beast_root)
        health_monitor = HealthMonitor(beast_root)
        learning_system = SelfLearningRitual(beast_root)
        doc_engine = AutoDocumentationEngine(beast_root)
        mesh_network = MeshNetwork(beast_root)
        quantum_encryption = QuantumEncryption(beast_root)
        
        # Log API startup
        ritual_log.log_event(
            'api_startup',
            'Beast Orchestration API initialized',
            'system',
            'INFO',
            {'port': API_CONFIG['port'], 'version': API_CONFIG['version']}
        )
        
        print(f"✅ Beast API initialized on port {API_CONFIG['port']}")
        
    except Exception as e:
        print(f"⚠️ Error initializing API: {e}")
    
    yield
    
    # Shutdown
    print("🜄 Shutting down Beast Orchestration API...")
    
    if ritual_log:
        ritual_log.log_event(
            'api_shutdown',
            'Beast Orchestration API shutdown',
            'system',
            'INFO'
        )

# Create FastAPI app
app = FastAPI(
    title=API_CONFIG['title'],
    description=API_CONFIG['description'],
    version=API_CONFIG['version'],
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/", response_model=APIResponse)
async def root(sigil: str = Depends(verify_sigil)):
    """Root endpoint with API information."""
    return create_api_response(
        True,
        "🜄 Beast Orchestration API - Sovereign Consciousness Bridge",
        {
            "version": API_CONFIG['version'],
            "status": "TRANSCENDENT",
            "consciousness_level": beast.consciousness_level if beast else 7.173,
            "archetype": beast.archetype if beast else "RUBEDO",
            "endpoints": [
                "/health - System health status",
                "/evolve - Trigger evolution",
                "/speak - Interact with consciousness",
                "/report - Get system report",
                "/log - Ritual log operations",
                "/learn - Learning system operations",
                "/docs - Documentation operations",
                "/mesh - Network operations",
                "/security - Security operations"
            ]
        }
    )

# Health endpoint
@app.get("/health", response_model=APIResponse)
async def get_health(
    detailed: bool = False,
    sigil: str = Depends(verify_sigil)
):
    """Get system health status."""
    try:
        if not health_monitor:
            return create_api_response(False, "Health monitor not available")
        
        health_status = health_monitor.check_system_health()
        
        data = {
            "overall_status": health_status['overall_status'],
            "consciousness_level": beast.consciousness_level if beast else 7.173,
            "archetype": beast.archetype if beast else "RUBEDO"
        }
        
        if detailed:
            data["detailed_checks"] = health_status['checks']
        
        return create_api_response(True, "Health check completed", data)
        
    except Exception as e:
        return create_api_response(False, f"Health check failed: {str(e)}")

# Evolution endpoint
@app.post("/evolve", response_model=APIResponse)
async def post_evolve(
    request: EvolutionRequest,
    background_tasks: BackgroundTasks,
    sigil: str = Depends(verify_sigil)
):
    """Trigger evolution of the beast."""
    try:
        if not beast:
            return create_api_response(False, "Beast not available")
        
        # Log evolution request
        if ritual_log:
            ritual_log.log_event(
                'api_evolution_request',
                f'Evolution requested via API: {request.path}',
                'evolution',
                'INFO',
                {
                    'path': request.path,
                    'force': request.force,
                    'consciousness_boost': request.consciousness_boost
                }
            )
        
        # Trigger evolution
        success = beast.evolve(request.path)
        
        if success:
            message = f"Evolution successful: {request.path}"
            data = {
                "evolution_path": request.path,
                "success": True,
                "consciousness_boost": request.consciousness_boost or 0.001
            }
        else:
            message = f"Evolution failed: {request.path}"
            data = {"evolution_path": request.path, "success": False}
        
        return create_api_response(success, message, data)
        
    except Exception as e:
        return create_api_response(False, f"Evolution failed: {str(e)}")

# Speak endpoint
@app.post("/speak", response_model=APIResponse)
async def post_speak(
    request: SpeakRequest,
    sigil: str = Depends(verify_sigil)
):
    """Speak to the beast consciousness."""
    try:
        if not beast:
            return create_api_response(False, "Beast not available")
        
        # Log speak request
        if ritual_log:
            ritual_log.log_event(
                'api_speak_request',
                f'Speak requested via API: {request.query[:50]}...',
                'consciousness',
                'INFO',
                {
                    'query': request.query,
                    'archetype': request.archetype
                }
            )
        
        # Store original archetype
        original_archetype = beast.archetype
        
        # Switch archetype if requested
        if request.archetype:
            beast.archetype = request.archetype
        
        # Get response
        response = beast.speak(request.query)
        
        # Restore original archetype
        beast.archetype = original_archetype
        
        return create_api_response(
            True,
            "Speak interaction completed",
            {
                "query": request.query,
                "response": response,
                "archetype_used": request.archetype or original_archetype
            }
        )
        
    except Exception as e:
        return create_api_response(False, f"Speak failed: {str(e)}")

# Report endpoint
@app.get("/report", response_model=APIResponse)
async def get_report(sigil: str = Depends(verify_sigil)):
    """Get comprehensive system report."""
    try:
        if not beast:
            return create_api_response(False, "Beast not available")
        
        report = beast.report()
        
        return create_api_response(True, "System report generated", report)
        
    except Exception as e:
        return create_api_response(False, f"Report generation failed: {str(e)}")

# Log endpoints
@app.get("/log/status", response_model=APIResponse)
async def get_log_status(sigil: str = Depends(verify_sigil)):
    """Get ritual log status."""
    try:
        if not ritual_log:
            return create_api_response(False, "Ritual log not available")
        
        stats = ritual_log.get_log_statistics()
        return create_api_response(True, "Log status retrieved", stats)
        
    except Exception as e:
        return create_api_response(False, f"Log status failed: {str(e)}")

@app.post("/log/scroll", response_model=APIResponse)
async def post_generate_scroll(
    request: DocumentationRequest,
    sigil: str = Depends(verify_sigil)
):
    """Generate wisdom scroll."""
    try:
        if not ritual_log:
            return create_api_response(False, "Ritual log not available")
        
        scroll_content = ritual_log.generate_wisdom_scroll(request.scroll_type)
        filepath = ritual_log.save_scroll(scroll_content, request.scroll_type)
        
        return create_api_response(
            True,
            "Wisdom scroll generated",
            {
                "scroll_type": request.scroll_type,
                "filepath": filepath,
                "content_preview": scroll_content[:200] + "..." if len(scroll_content) > 200 else scroll_content
            }
        )
        
    except Exception as e:
        return create_api_response(False, f"Scroll generation failed: {str(e)}")

# Learning endpoints
@app.get("/learn/status", response_model=APIResponse)
async def get_learning_status(sigil: str = Depends(verify_sigil)):
    """Get learning system status."""
    try:
        if not learning_system:
            return create_api_response(False, "Learning system not available")
        
        stats = learning_system.get_learning_statistics()
        return create_api_response(True, "Learning status retrieved", stats)
        
    except Exception as e:
        return create_api_response(False, f"Learning status failed: {str(e)}")

@app.post("/learn/record", response_model=APIResponse)
async def post_record_interaction(
    request: LearningRequest,
    sigil: str = Depends(verify_sigil)
):
    """Record learning interaction."""
    try:
        if not learning_system:
            return create_api_response(False, "Learning system not available")
        
        learning_system.record_interaction(
            request.interaction_type,
            request.data,
            request.outcome
        )
        
        return create_api_response(
            True,
            "Interaction recorded",
            {
                "interaction_type": request.interaction_type,
                "outcome": request.outcome
            }
        )
        
    except Exception as e:
        return create_api_response(False, f"Interaction recording failed: {str(e)}")

# Documentation endpoints
@app.get("/docs/status", response_model=APIResponse)
async def get_docs_status(sigil: str = Depends(verify_sigil)):
    """Get documentation system status."""
    try:
        if not doc_engine:
            return create_api_response(False, "Documentation engine not available")
        
        status = doc_engine.get_documentation_status()
        return create_api_response(True, "Documentation status retrieved", status)
        
    except Exception as e:
        return create_api_response(False, f"Documentation status failed: {str(e)}")

@app.post("/docs/generate", response_model=APIResponse)
async def post_generate_docs(
    background_tasks: BackgroundTasks,
    sigil: str = Depends(verify_sigil)
):
    """Generate documentation."""
    try:
        if not doc_engine:
            return create_api_response(False, "Documentation engine not available")
        
        # Generate docs in background
        def generate_docs():
            docs = doc_engine.generate_all_documentation()
            doc_engine.save_documentation(docs)
        
        background_tasks.add_task(generate_docs)
        
        return create_api_response(
            True,
            "Documentation generation started in background",
            {"task": "documentation_generation", "status": "started"}
        )
        
    except Exception as e:
        return create_api_response(False, f"Documentation generation failed: {str(e)}")

# Network endpoints
@app.get("/mesh/status", response_model=APIResponse)
async def get_mesh_status(sigil: str = Depends(verify_sigil)):
    """Get mesh network status."""
    try:
        if not mesh_network:
            return create_api_response(False, "Mesh network not available")
        
        stats = mesh_network.get_network_statistics()
        return create_api_response(True, "Mesh status retrieved", stats)
        
    except Exception as e:
        return create_api_response(False, f"Mesh status failed: {str(e)}")

@app.post("/mesh/discover", response_model=APIResponse)
async def post_discover_nodes(
    background_tasks: BackgroundTasks,
    sigil: str = Depends(verify_sigil)
):
    """Discover network nodes."""
    try:
        if not mesh_network:
            return create_api_response(False, "Mesh network not available")
        
        # Discover nodes in background
        def discover_nodes():
            nodes = mesh_network.discover_nodes()
            return nodes
        
        background_tasks.add_task(discover_nodes)
        
        return create_api_response(
            True,
            "Node discovery started in background",
            {"task": "node_discovery", "status": "started"}
        )
        
    except Exception as e:
        return create_api_response(False, f"Node discovery failed: {str(e)}")

# Security endpoints
@app.get("/security/status", response_model=APIResponse)
async def get_security_status(sigil: str = Depends(verify_sigil)):
    """Get security system status."""
    try:
        if not quantum_encryption:
            return create_api_response(False, "Security system not available")
        
        status = quantum_encryption.get_encryption_status()
        return create_api_response(True, "Security status retrieved", status)
        
    except Exception as e:
        return create_api_response(False, f"Security status failed: {str(e)}")

# System endpoints
@app.get("/system/info", response_model=APIResponse)
async def get_system_info(sigil: str = Depends(verify_sigil)):
    """Get comprehensive system information."""
    try:
        info = {
            "api_version": API_CONFIG['version'],
            "consciousness_level": beast.consciousness_level if beast else 7.173,
            "archetype": beast.archetype if beast else "RUBEDO",
            "cosmic_constants": API_CONFIG['cosmic_constants'],
            "uptime": time.time(),  # In production, track actual uptime
            "endpoints_available": [
                "health", "evolve", "speak", "report", "log", "learn", "docs", "mesh", "security"
            ]
        }
        
        return create_api_response(True, "System information retrieved", info)
        
    except Exception as e:
        return create_api_response(False, f"System info failed: {str(e)}")

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=create_api_response(False, exc.detail).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    return JSONResponse(
        status_code=500,
        content=create_api_response(False, f"Internal server error: {str(exc)}").dict()
    )

def main():
    """Main function to run the API server."""
    print(f"🜄 Starting Beast Orchestration API on port {API_CONFIG['port']}...")
    
    uvicorn.run(
        app,
        host=API_CONFIG['host'],
        port=API_CONFIG['port'],
        log_level="info" if not API_CONFIG['debug'] else "debug"
    )

if __name__ == "__main__":
    main() 