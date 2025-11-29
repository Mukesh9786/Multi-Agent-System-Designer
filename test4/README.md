# 🤖 Multi-Agent System Designer

A complete, production-ready multi-agent system with beautiful N8N-style visualization and powerful strand-based backend architecture.

## ✨ Features

### Frontend
- **Visual Workflow Designer**: N8N-style drag-and-drop interface with Google-like UI
- **Smart Agent Generation**: Automatically converts business workflows into specialized agents
- **Real-time Visualization**: Interactive node-based visualization with animations
- **Pre-built Templates**: Quick start with Customer Support, E-Commerce, Content Creation, and HR workflows
- **Execution Simulation**: Run simulations to see how agents communicate
- **Performance Metrics**: Track response times, success rates, and agent performance
- **JSON Export**: Export complete agent system configurations
- **Responsive Design**: Beautiful gradient UI with smooth animations

### Backend (Python + FastAPI)
- **Strand-Based Architecture**: Organize agents into execution strands
- **Specialized Agents**: Pre-built agents for common workflows
- **Shared Memory System**: Agents share context and state
- **Async Execution**: High-performance async/await patterns
- **RESTful API**: Complete API for system generation and execution
- **Metrics & Logging**: Comprehensive tracking and monitoring
- **Tool System**: Extensible tool framework for agents
- **Multiple Execution Modes**: Sequential, parallel, and graph-based execution

## 🚀 Quick Start

### Option 1: Frontend Only (Instant Demo)

1. Open `index.html` in your web browser
2. Select a template or describe your workflow
3. Click "Generate Agent System"
4. Watch the visualization come to life!
5. Click "Run Simulation" to see agents in action

### Option 2: Full Stack (Frontend + Backend)

1. **Start Backend:**
   ```bash
   cd backend
   pip install -r requirements.txt
   python run_server.py
   ```

2. **Update Frontend:**
   In `index.html`, change:
   ```html
   <script src="app.js"></script>
   ```
   to:
   ```html
   <script src="app-with-backend.js"></script>
   ```

3. **Open Frontend:**
   Open `index.html` in your browser

4. **Test Everything:**
   ```bash
   cd backend
   python test_system.py
   ```

See [SETUP.md](SETUP.md) for detailed instructions.

## 📋 Templates Included

### Customer Support System
- Intake Agent → Classification Agent → Resolution Agent → Quality Agent → Follow-up Agent

### E-Commerce Order Processing
- Order Agent → Payment Agent → Inventory Agent → Shipping Agent → Notification Agent

### Content Creation Workflow
- Content Planner → Content Writer → Content Editor → Visual Designer → Publishing Agent

### HR Recruitment Process
- Sourcing Agent → Screening Agent → Interview Agent → Assessment Agent → Offer Agent

## 🎨 UI Features

- **Drag & Drop**: Move agents around the canvas
- **Zoom Controls**: Zoom in/out and reset view
- **Agent Details**: Click any agent to see detailed information
- **Live Logs**: Real-time execution logs with timestamps
- **Metrics Dashboard**: Performance tracking with visual cards
- **Dark Theme JSON**: Syntax-highlighted JSON output

## 🔧 System Architecture

Each generated system includes:

```json
{
  "systemName": "Your System Name",
  "agents": [
    {
      "id": "unique-id",
      "name": "Agent Name",
      "role": "Agent responsibility",
      "tools": ["tool1", "tool2"],
      "memory": {
        "access": "read-write",
        "scope": "shared"
      }
    }
  ],
  "communications": [
    {
      "from": "agent1",
      "to": "agent2",
      "protocol": "async-message",
      "trigger": "on-completion"
    }
  ],
  "memory": {
    "type": "shared",
    "strategy": "event-driven"
  },
  "metrics": {
    "enabled": true,
    "trackResponseTime": true
  }
}
```

## ⌨️ Keyboard Shortcuts

- `Ctrl/Cmd + Enter`: Generate system
- `Ctrl/Cmd + E`: Export JSON
- `Ctrl/Cmd + R`: Run simulation

## 🎯 Use Cases

- **Business Process Automation**: Convert manual workflows into automated agent systems
- **System Design**: Visualize and design multi-agent architectures
- **Hackathon Demos**: Quick prototyping of intelligent systems
- **Education**: Learn about multi-agent systems and distributed computing
- **Proof of Concepts**: Rapidly create agent system designs for stakeholders

## 🛠️ Technology Stack

- Pure HTML5, CSS3, JavaScript (No dependencies!)
- SVG for connection visualization
- CSS Grid & Flexbox for responsive layout
- Modern ES6+ JavaScript features

## 📊 Agent Communication

Agents communicate through:
- **Async Messages**: Event-driven communication
- **Shared Memory**: Access to common data store
- **Trigger-based**: On-completion, on-error, on-schedule
- **JSON Protocol**: Standardized data format

## 🎨 Customization

The system automatically adapts to different workflow types:
- **Sequential**: Linear agent chains
- **Parallel**: Multiple agents working simultaneously
- **Circular**: Feedback loops and iterative processes
- **Hierarchical**: Supervisor-worker patterns

## 📈 Metrics Tracked

- Total number of agents
- Communication paths
- Average response time
- Success rate
- Individual agent performance

## 🌟 Perfect For

- Hackathons and demos
- System architecture presentations
- Business process modeling
- AI/ML workflow design
- Educational purposes

## 💡 Tips

1. Start with a template and modify it
2. Use clear, descriptive workflow steps
3. Drag agents to reorganize the layout
4. Run simulations to validate the flow
5. Export JSON for implementation

## 🚀 Future Enhancements

- Save/Load workflows
- Custom agent creation
- More communication protocols
- Integration with actual AI services
- Collaborative editing
- Version control

## 📝 License

MIT License - Feel free to use for your hackathon!

---

Built with ❤️ for hackathons and rapid prototyping
