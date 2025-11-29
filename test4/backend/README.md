# Multi-Agent System Backend

A powerful strand-based multi-agent system framework with FastAPI backend.

## 🏗️ Architecture

### Core Components

1. **Agent Framework** (`agent_framework.py`)
   - Base `Agent` class with memory and tools
   - `AgentStrand` for managing agent sequences
   - `MultiAgentSystem` for orchestrating multiple strands
   - Shared memory system
   - Performance metrics tracking

2. **Specialized Agents** (`specialized_agents.py`)
   - `IntakeAgent` - Receives and validates requests
   - `ClassificationAgent` - Categorizes and routes
   - `ProcessingAgent` - Transforms data
   - `ResolutionAgent` - Generates solutions
   - `QualityAgent` - Reviews and validates
   - `NotificationAgent` - Sends updates
   - `AnalyticsAgent` - Generates insights

3. **FastAPI Backend** (`api.py`)
   - RESTful API endpoints
   - System generation from workflows
   - Strand execution
   - Metrics and logging

## 🚀 Quick Start

### Installation

```bash
cd backend
pip install -r requirements.txt
```

### Run the Server

```bash
python run_server.py
```

Server will start at `http://localhost:8000`

### Run Examples

```bash
python example_usage.py
```

## 📡 API Endpoints

### Generate System
```http
POST /api/generate
Content-Type: application/json

{
  "workflow_description": "Customer support workflow",
  "workflow_type": "customer-support"
}
```

### Execute Strand
```http
POST /api/execute
Content-Type: application/json

{
  "strand_name": "customer-support_strand",
  "input_data": {
    "customer_id": "CUST-123",
    "message": "Need help with payment"
  },
  "execution_mode": "sequential"
}
```

### Get Metrics
```http
GET /api/metrics
```

### Get Logs
```http
GET /api/logs?limit=100
```

### List Strands
```http
GET /api/strands
```

## 🎯 Workflow Types

### Customer Support
- Intake → Classification → Resolution → Quality → Notification

### E-Commerce
- Order → Payment → Inventory → Shipping → Notification

### Content Creation
- Planner → Writer → Editor → Designer → Publisher

### HR Recruitment
- Sourcing → Screening → Interview → Assessment → Offer

## 💡 Usage Examples

### Basic Agent Creation

```python
from agent_framework import Agent, AgentMemory

agent = Agent(
    agent_id="agent1",
    name="My Agent",
    role="Process data",
    memory=AgentMemory()
)

result = await agent.process({"data": "input"})
```

### Creating a Strand

```python
from agent_framework import AgentStrand
from specialized_agents import IntakeAgent, ProcessingAgent

agents = [
    IntakeAgent("intake", "Intake", "Receives input"),
    ProcessingAgent("processor", "Processor", "Processes data")
]

strand = AgentStrand("my_strand", agents)
result = await strand.execute_sequential({"input": "data"})
```

### Multi-Agent System

```python
from agent_framework import MultiAgentSystem

system = MultiAgentSystem("My System")
system.add_strand(strand)

result = await system.execute_strand(
    "my_strand",
    {"input": "data"},
    "sequential"
)
```

### Custom Tools

```python
from agent_framework import Tool

async def my_tool_function(param):
    return {"result": param}

tool = Tool("my_tool", "Does something", my_tool_function)
agent.tools.append(tool)

# Use the tool
result = await agent.use_tool("my_tool").execute("value")
```

## 🔧 Execution Modes

### Sequential
Agents execute one after another, passing results forward.

```python
result = await strand.execute_sequential(input_data)
```

### Parallel
All agents execute simultaneously with the same input.

```python
result = await strand.execute_parallel(input_data)
```

### Graph
Agents execute based on communication graph.

```python
strand.add_communication("agent1", "agent2")
strand.add_communication("agent2", "agent3")
result = await strand.execute_graph(input_data)
```

## 📊 Memory System

### Short-term Memory
Temporary storage cleared between executions.

```python
agent.memory.store("key", "value")
value = agent.memory.retrieve("key")
```

### Long-term Memory
Persistent storage across executions.

```python
agent.memory.store("key", "value", persistent=True)
history = agent.memory.search_history("key")
```

### Shared Memory
All agents in a strand share the same memory.

```python
shared_memory = AgentMemory()
strand = AgentStrand("name", agents, shared_memory)
```

## 📈 Metrics

Each agent tracks:
- Total executions
- Successful executions
- Failed executions
- Average execution time
- Success rate

```python
metrics = agent.get_metrics()
print(f"Success rate: {metrics['success_rate']}%")
```

## 📝 Logging

All agent activities are logged:

```python
logs = strand.get_all_logs()
for log in logs:
    print(f"[{log['agent']}] {log['message']}")
```

## 🔌 Integration with Frontend

Update the frontend to connect to the backend:

```javascript
// In app.js
async function generateSystem() {
    const response = await fetch('http://localhost:8000/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            workflow_description: workflowInput,
            workflow_type: 'customer-support'
        })
    });
    
    const system = await response.json();
    visualizer.render(system);
}
```

## 🧪 Testing

Run the example script to test all features:

```bash
python example_usage.py
```

This will demonstrate:
- Customer support workflow
- Parallel execution
- Multi-system orchestration
- Custom tools

## 🎨 Customization

### Create Custom Agent

```python
from agent_framework import Agent

class MyCustomAgent(Agent):
    async def _execute_logic(self, input_data):
        # Your custom logic here
        result = {"processed": True}
        self.memory.store("result", result)
        return result
```

### Add Custom Workflow Type

In `api.py`, add to `create_agents_for_workflow()`:

```python
elif workflow_type == "my-workflow":
    return [
        MyCustomAgent("agent1", "Agent 1", "Does something"),
        MyCustomAgent("agent2", "Agent 2", "Does something else")
    ]
```

## 🚀 Production Deployment

### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "run_server.py"]
```

### Environment Variables

Create `.env` file:

```env
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=info
```

## 📚 API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🤝 Contributing

The framework is designed to be extensible:
1. Add new agent types in `specialized_agents.py`
2. Add new tools for agents
3. Implement new execution strategies
4. Add new memory strategies

## 📄 License

MIT License - Perfect for hackathons and prototypes!
