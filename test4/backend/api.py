"""
FastAPI Backend for Multi-Agent System
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import asyncio

from agent_framework import (
    Agent, AgentStrand, MultiAgentSystem, AgentMemory, Tool
)
from specialized_agents import (
    IntakeAgent, ClassificationAgent, ProcessingAgent,
    ResolutionAgent, QualityAgent, NotificationAgent, AnalyticsAgent
)

app = FastAPI(title="Multi-Agent System API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global system instance
multi_agent_system = MultiAgentSystem("Global System")


class WorkflowRequest(BaseModel):
    workflow_description: str
    workflow_type: str = "customer-support"


class ExecutionRequest(BaseModel):
    strand_name: str
    input_data: Dict[str, Any]
    execution_mode: str = "sequential"


class SystemConfig(BaseModel):
    system_name: str
    agents: List[Dict[str, Any]]
    communications: List[Dict[str, str]]


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Multi-Agent System API",
        "version": "1.0.0",
        "endpoints": {
            "generate": "/api/generate",
            "execute": "/api/execute",
            "metrics": "/api/metrics",
            "logs": "/api/logs",
            "strands": "/api/strands"
        }
    }


@app.post("/api/generate")
async def generate_system(request: WorkflowRequest):
    """Generate a multi-agent system from workflow description"""
    
    try:
        # Create agents based on workflow type
        agents = create_agents_for_workflow(request.workflow_type)
        
        # Create strand
        strand_name = f"{request.workflow_type}_strand"
        shared_memory = AgentMemory()
        strand = AgentStrand(strand_name, agents, shared_memory)
        
        # Setup communication graph
        for i in range(len(agents) - 1):
            strand.add_communication(agents[i].id, agents[i + 1].id)
        
        # Add to system
        multi_agent_system.add_strand(strand)
        
        # Generate response
        agent_configs = [
            {
                "id": agent.id,
                "name": agent.name,
                "role": agent.role,
                "tools": [tool.name for tool in agent.tools],
                "icon": get_agent_icon(agent.name)
            }
            for agent in agents
        ]
        
        communications = [
            {
                "from": agents[i].id,
                "to": agents[i + 1].id,
                "protocol": "async-message",
                "trigger": "on-completion"
            }
            for i in range(len(agents) - 1)
        ]
        
        return {
            "systemName": strand_name,
            "agents": agent_configs,
            "communications": communications,
            "memory": {
                "type": "shared",
                "strategy": "event-driven",
                "persistence": "in-memory"
            },
            "metrics": {
                "enabled": True,
                "trackResponseTime": True,
                "trackSuccessRate": True
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/execute")
async def execute_strand(request: ExecutionRequest):
    """Execute a specific agent strand"""
    
    try:
        result = await multi_agent_system.execute_strand(
            request.strand_name,
            request.input_data,
            request.execution_mode
        )
        
        return {
            "success": True,
            "result": result,
            "execution_mode": request.execution_mode
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/metrics")
async def get_metrics():
    """Get system-wide metrics"""
    
    try:
        metrics = multi_agent_system.get_system_metrics()
        return metrics
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/logs")
async def get_logs(limit: Optional[int] = 100):
    """Get system logs"""
    
    try:
        logs = multi_agent_system.get_system_logs()
        
        # Limit logs
        if limit:
            logs = logs[-limit:]
        
        return {
            "total_logs": len(logs),
            "logs": logs
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/strands")
async def list_strands():
    """List all available strands"""
    
    try:
        strands_info = []
        
        for strand_name, strand in multi_agent_system.strands.items():
            strands_info.append({
                "name": strand_name,
                "agent_count": len(strand.agents),
                "agents": [
                    {
                        "id": agent.id,
                        "name": agent.name,
                        "status": agent.status.value
                    }
                    for agent in strand.agents
                ]
            })
        
        return {
            "total_strands": len(strands_info),
            "strands": strands_info
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/strand/{strand_name}/metrics")
async def get_strand_metrics(strand_name: str):
    """Get metrics for a specific strand"""
    
    try:
        if strand_name not in multi_agent_system.strands:
            raise HTTPException(status_code=404, detail="Strand not found")
        
        strand = multi_agent_system.strands[strand_name]
        metrics = strand.get_all_metrics()
        
        return {
            "strand_name": strand_name,
            "metrics": metrics
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/strand/{strand_name}")
async def delete_strand(strand_name: str):
    """Delete a strand"""
    
    try:
        if strand_name not in multi_agent_system.strands:
            raise HTTPException(status_code=404, detail="Strand not found")
        
        del multi_agent_system.strands[strand_name]
        
        return {
            "success": True,
            "message": f"Strand {strand_name} deleted"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def create_agents_for_workflow(workflow_type: str) -> List[Agent]:
    """Create agents based on workflow type"""
    
    if workflow_type == "customer-support":
        return [
            IntakeAgent("intake", "Intake Agent", "Receives and validates customer inquiries"),
            ClassificationAgent("classifier", "Classification Agent", "Categorizes issues"),
            ResolutionAgent("resolver", "Resolution Agent", "Generates solutions"),
            QualityAgent("quality", "Quality Agent", "Reviews responses"),
            NotificationAgent("notification", "Notification Agent", "Sends updates")
        ]
    
    elif workflow_type == "ecommerce":
        return [
            IntakeAgent("order", "Order Agent", "Processes incoming orders"),
            ProcessingAgent("payment", "Payment Agent", "Handles payment processing"),
            ProcessingAgent("inventory", "Inventory Agent", "Manages stock"),
            ProcessingAgent("shipping", "Shipping Agent", "Coordinates delivery"),
            NotificationAgent("notification", "Notification Agent", "Sends customer updates")
        ]
    
    elif workflow_type == "content":
        return [
            ProcessingAgent("planner", "Content Planner", "Plans content strategy"),
            ProcessingAgent("writer", "Content Writer", "Creates written content"),
            QualityAgent("editor", "Content Editor", "Reviews and refines content"),
            ProcessingAgent("designer", "Visual Designer", "Creates visual assets"),
            NotificationAgent("publisher", "Publishing Agent", "Publishes content")
        ]
    
    elif workflow_type == "hr":
        return [
            IntakeAgent("sourcing", "Sourcing Agent", "Finds candidates"),
            ClassificationAgent("screening", "Screening Agent", "Reviews applications"),
            ProcessingAgent("interview", "Interview Agent", "Coordinates interviews"),
            AnalyticsAgent("assessment", "Assessment Agent", "Evaluates candidates"),
            NotificationAgent("offer", "Offer Agent", "Manages offers")
        ]
    
    else:
        # Generic workflow
        return [
            IntakeAgent("input", "Input Agent", "Receives input"),
            ProcessingAgent("processor", "Processing Agent", "Processes data"),
            NotificationAgent("output", "Output Agent", "Delivers output")
        ]


def get_agent_icon(agent_name: str) -> str:
    """Get icon for agent based on name"""
    icons = {
        "Intake Agent": "🎯",
        "Classification Agent": "🏷️",
        "Resolution Agent": "💡",
        "Quality Agent": "✅",
        "Notification Agent": "📧",
        "Order Agent": "🛒",
        "Payment Agent": "💳",
        "Inventory Agent": "📦",
        "Shipping Agent": "🚚",
        "Content Planner": "📋",
        "Content Writer": "✍️",
        "Content Editor": "📝",
        "Visual Designer": "🎨",
        "Publishing Agent": "🚀",
        "Sourcing Agent": "🔍",
        "Screening Agent": "📄",
        "Interview Agent": "🗓️",
        "Assessment Agent": "📊",
        "Offer Agent": "🤝",
        "Input Agent": "📥",
        "Processing Agent": "⚙️",
        "Output Agent": "📤"
    }
    return icons.get(agent_name, "🤖")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
