"""
Multi-Agent Framework Core
Implements a strand-based agent system with memory, tools, and communication
"""

import asyncio
import json
import time
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import uuid


class AgentStatus(Enum):
    IDLE = "idle"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class Message:
    """Message passed between agents"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sender: str = ""
    receiver: str = ""
    content: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentMemory:
    """Shared memory system for agents"""
    short_term: Dict[str, Any] = field(default_factory=dict)
    long_term: List[Dict[str, Any]] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    
    def store(self, key: str, value: Any, persistent: bool = False):
        """Store data in memory"""
        self.short_term[key] = value
        if persistent:
            self.long_term.append({
                "key": key,
                "value": value,
                "timestamp": time.time()
            })
    
    def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve data from memory"""
        return self.short_term.get(key)
    
    def search_history(self, key: str) -> List[Dict[str, Any]]:
        """Search long-term memory"""
        return [item for item in self.long_term if item["key"] == key]


class Tool:
    """Base class for agent tools"""
    def __init__(self, name: str, description: str, func: Callable):
        self.name = name
        self.description = description
        self.func = func
    
    async def execute(self, *args, **kwargs) -> Any:
        """Execute the tool"""
        if asyncio.iscoroutinefunction(self.func):
            return await self.func(*args, **kwargs)
        return self.func(*args, **kwargs)


class Agent:
    """Base Agent class with strand-based execution"""
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        role: str,
        tools: List[Tool] = None,
        memory: AgentMemory = None
    ):
        self.id = agent_id
        self.name = name
        self.role = role
        self.tools = tools or []
        self.memory = memory or AgentMemory()
        self.status = AgentStatus.IDLE
        self.inbox: asyncio.Queue = asyncio.Queue()
        self.execution_log: List[Dict[str, Any]] = []
        self.metrics = {
            "total_executions": 0,
            "successful_executions": 0,
            "failed_executions": 0,
            "total_time": 0.0
        }
    
    async def receive_message(self, message: Message):
        """Receive a message from another agent"""
        await self.inbox.put(message)
        self.log(f"Received message from {message.sender}")
    
    async def send_message(self, receiver: str, content: Dict[str, Any]) -> Message:
        """Send a message to another agent"""
        message = Message(
            sender=self.id,
            receiver=receiver,
            content=content
        )
        self.log(f"Sent message to {receiver}")
        return message
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main processing logic - to be overridden by specific agents"""
        self.status = AgentStatus.PROCESSING
        start_time = time.time()
        
        try:
            # Default processing
            result = await self._execute_logic(input_data)
            
            self.status = AgentStatus.COMPLETED
            self.metrics["successful_executions"] += 1
            
            execution_time = time.time() - start_time
            self.metrics["total_time"] += execution_time
            
            self.log(f"Completed processing in {execution_time:.2f}s")
            
            return result
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            self.metrics["failed_executions"] += 1
            self.log(f"Error: {str(e)}", level="error")
            raise
        finally:
            self.metrics["total_executions"] += 1
            self.status = AgentStatus.IDLE
    
    async def _execute_logic(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent-specific logic"""
        # Store input in memory
        self.memory.store("last_input", input_data)
        
        # Simulate processing
        await asyncio.sleep(0.5)
        
        result = {
            "agent": self.name,
            "status": "success",
            "data": input_data,
            "timestamp": time.time()
        }
        
        # Store result in memory
        self.memory.store("last_output", result)
        
        return result
    
    def use_tool(self, tool_name: str) -> Optional[Tool]:
        """Get a tool by name"""
        for tool in self.tools:
            if tool.name == tool_name:
                return tool
        return None
    
    def log(self, message: str, level: str = "info"):
        """Log agent activity"""
        log_entry = {
            "timestamp": time.time(),
            "agent": self.name,
            "level": level,
            "message": message
        }
        self.execution_log.append(log_entry)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get agent performance metrics"""
        avg_time = (
            self.metrics["total_time"] / self.metrics["total_executions"]
            if self.metrics["total_executions"] > 0
            else 0
        )
        
        return {
            "agent_id": self.id,
            "agent_name": self.name,
            "total_executions": self.metrics["total_executions"],
            "successful_executions": self.metrics["successful_executions"],
            "failed_executions": self.metrics["failed_executions"],
            "success_rate": (
                self.metrics["successful_executions"] / self.metrics["total_executions"] * 100
                if self.metrics["total_executions"] > 0
                else 0
            ),
            "average_execution_time": avg_time
        }


class AgentStrand:
    """Manages a strand (sequence) of agents"""
    
    def __init__(self, name: str, agents: List[Agent], shared_memory: AgentMemory = None):
        self.name = name
        self.agents = agents
        self.shared_memory = shared_memory or AgentMemory()
        self.communication_graph: Dict[str, List[str]] = {}
        
        # Share memory with all agents
        for agent in agents:
            agent.memory = self.shared_memory
    
    def add_communication(self, from_agent: str, to_agent: str):
        """Define communication path between agents"""
        if from_agent not in self.communication_graph:
            self.communication_graph[from_agent] = []
        self.communication_graph[from_agent].append(to_agent)
    
    async def execute_sequential(self, initial_input: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agents sequentially"""
        current_data = initial_input
        results = []
        
        for agent in self.agents:
            result = await agent.process(current_data)
            results.append(result)
            current_data = result
        
        return {
            "strand": self.name,
            "results": results,
            "final_output": current_data
        }
    
    async def execute_parallel(self, initial_input: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agents in parallel"""
        tasks = [agent.process(initial_input) for agent in self.agents]
        results = await asyncio.gather(*tasks)
        
        return {
            "strand": self.name,
            "results": results
        }
    
    async def execute_graph(self, initial_input: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agents based on communication graph"""
        if not self.agents:
            return {"error": "No agents in strand"}
        
        # Start with first agent
        first_agent = self.agents[0]
        result = await first_agent.process(initial_input)
        
        # Follow communication graph
        processed = {first_agent.id}
        results = [result]
        
        async def process_next(agent_id: str, data: Dict[str, Any]):
            if agent_id not in self.communication_graph:
                return
            
            for next_agent_id in self.communication_graph[agent_id]:
                if next_agent_id in processed:
                    continue
                
                next_agent = next((a for a in self.agents if a.id == next_agent_id), None)
                if next_agent:
                    result = await next_agent.process(data)
                    results.append(result)
                    processed.add(next_agent_id)
                    await process_next(next_agent_id, result)
        
        await process_next(first_agent.id, result)
        
        return {
            "strand": self.name,
            "results": results
        }
    
    def get_all_metrics(self) -> List[Dict[str, Any]]:
        """Get metrics for all agents"""
        return [agent.get_metrics() for agent in self.agents]
    
    def get_all_logs(self) -> List[Dict[str, Any]]:
        """Get logs from all agents"""
        all_logs = []
        for agent in self.agents:
            all_logs.extend(agent.execution_log)
        return sorted(all_logs, key=lambda x: x["timestamp"])


class MultiAgentSystem:
    """Orchestrates multiple agent strands"""
    
    def __init__(self, name: str):
        self.name = name
        self.strands: Dict[str, AgentStrand] = {}
        self.global_memory = AgentMemory()
    
    def add_strand(self, strand: AgentStrand):
        """Add an agent strand to the system"""
        self.strands[strand.name] = strand
    
    async def execute_strand(self, strand_name: str, input_data: Dict[str, Any], mode: str = "sequential") -> Dict[str, Any]:
        """Execute a specific strand"""
        if strand_name not in self.strands:
            return {"error": f"Strand {strand_name} not found"}
        
        strand = self.strands[strand_name]
        
        if mode == "sequential":
            return await strand.execute_sequential(input_data)
        elif mode == "parallel":
            return await strand.execute_parallel(input_data)
        elif mode == "graph":
            return await strand.execute_graph(input_data)
        else:
            return {"error": f"Unknown execution mode: {mode}"}
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get metrics for entire system"""
        all_metrics = []
        for strand in self.strands.values():
            all_metrics.extend(strand.get_all_metrics())
        
        return {
            "system_name": self.name,
            "total_strands": len(self.strands),
            "total_agents": sum(len(s.agents) for s in self.strands.values()),
            "agent_metrics": all_metrics
        }
    
    def get_system_logs(self) -> List[Dict[str, Any]]:
        """Get all system logs"""
        all_logs = []
        for strand in self.strands.values():
            all_logs.extend(strand.get_all_logs())
        return sorted(all_logs, key=lambda x: x["timestamp"])
