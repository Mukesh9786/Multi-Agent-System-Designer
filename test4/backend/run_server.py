"""
Server startup script
"""

import uvicorn
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("=" * 60)
    print("Starting Multi-Agent System API Server")
    print("=" * 60)
    print("\nAPI Documentation: http://localhost:8000/docs")
    print("API Root: http://localhost:8000")
    print("\nAvailable Endpoints:")
    print("  POST /api/generate - Generate agent system")
    print("  POST /api/execute - Execute agent strand")
    print("  GET  /api/metrics - Get system metrics")
    print("  GET  /api/logs - Get execution logs")
    print("  GET  /api/strands - List all strands")
    print("\nPress CTRL+C to stop the server")
    print("=" * 60)
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
