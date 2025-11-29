# 🚀 Complete Setup Guide

## Quick Start (Frontend Only)

If you just want to see the visualization without the backend:

1. Open `index.html` in your browser
2. Done! The app works standalone with local simulation

## Full Setup (Frontend + Backend)

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser

### Step 1: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Start the Backend Server

**Option A: Using the batch file (Windows)**
```bash
cd backend
start.bat
```

**Option B: Manual start**
```bash
cd backend
python run_server.py
```

The server will start at `http://localhost:8000`

### Step 3: Update Frontend to Use Backend

Replace the script tag in `index.html`:

Change:
```html
<script src="app.js"></script>
```

To:
```html
<script src="app-with-backend.js"></script>
```

### Step 4: Open the Frontend

Open `index.html` in your browser. The app will automatically:
- Connect to the backend if available
- Fall back to local simulation if backend is not running

## 🧪 Testing the Backend

### Test with Example Script

```bash
cd backend
python example_usage.py
```

This will run several examples demonstrating:
- Customer support workflow
- Parallel execution
- Multi-system orchestration
- Custom tools

### Test API Endpoints

Visit `http://localhost:8000/docs` for interactive API documentation.

**Example API Call:**

```bash
curl -X POST "http://localhost:8000/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_description": "Customer support system",
    "workflow_type": "customer-support"
  }'
```

## 📁 Project Structure

```
.
├── index.html              # Main HTML file
├── styles.css              # Styling
├── agent-system.js         # Local agent logic
├── visualization.js        # Canvas visualization
├── app.js                  # Frontend app (standalone)
├── app-with-backend.js     # Frontend app (with backend)
├── backend/
│   ├── agent_framework.py  # Core agent framework
│   ├── specialized_agents.py # Agent implementations
│   ├── api.py              # FastAPI backend
│   ├── run_server.py       # Server startup
│   ├── example_usage.py    # Usage examples
│   ├── requirements.txt    # Python dependencies
│   └── start.bat           # Windows startup script
└── README.md
```

## 🎯 Usage Modes

### Mode 1: Standalone Frontend
- No backend required
- Local simulation only
- Perfect for demos and presentations
- Just open `index.html`

### Mode 2: Frontend + Backend
- Full agent execution
- Real metrics and logging
- Persistent memory
- Scalable architecture

## 🔧 Configuration

### Backend Configuration

Edit `run_server.py` to change:
- Host (default: `0.0.0.0`)
- Port (default: `8000`)
- Reload mode (default: `True`)

### Frontend Configuration

Edit `app-with-backend.js` to change:
- API base URL (default: `http://localhost:8000`)

## 🐛 Troubleshooting

### Backend won't start

**Error: "Module not found"**
```bash
pip install -r requirements.txt
```

**Error: "Port already in use"**
Change the port in `run_server.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Changed to 8001
```

### Frontend can't connect to backend

1. Check if backend is running: `http://localhost:8000`
2. Check browser console for CORS errors
3. Verify API_BASE_URL in `app-with-backend.js`

### CORS Issues

The backend has CORS enabled for all origins. If you still have issues:

In `api.py`, verify:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Should be "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🚀 Deployment

### Deploy Backend

**Using Docker:**

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["python", "run_server.py"]
```

Build and run:
```bash
docker build -t multi-agent-backend .
docker run -p 8000:8000 multi-agent-backend
```

**Using Cloud Services:**
- AWS: Elastic Beanstalk or ECS
- Google Cloud: Cloud Run or App Engine
- Azure: App Service
- Heroku: `heroku create` + `git push heroku main`

### Deploy Frontend

**Static Hosting:**
- GitHub Pages
- Netlify
- Vercel
- AWS S3 + CloudFront

Just upload these files:
- `index.html`
- `styles.css`
- `agent-system.js`
- `visualization.js`
- `app-with-backend.js` (or `app.js` for standalone)

## 📊 Performance Tips

### Backend
- Use async/await for all I/O operations
- Enable caching for repeated requests
- Use connection pooling for databases
- Monitor memory usage with shared memory

### Frontend
- Limit number of agents displayed (< 20 for best performance)
- Use requestAnimationFrame for animations
- Debounce user inputs
- Lazy load large JSON outputs

## 🎨 Customization

### Add New Workflow Type

1. In `backend/api.py`, add to `create_agents_for_workflow()`:
```python
elif workflow_type == "my-workflow":
    return [
        IntakeAgent("agent1", "Agent 1", "Description"),
        ProcessingAgent("agent2", "Agent 2", "Description")
    ]
```

2. In `app-with-backend.js`, add to templates:
```javascript
'my-workflow': `My Workflow Description...`
```

### Create Custom Agent

In `backend/specialized_agents.py`:
```python
class MyCustomAgent(Agent):
    async def _execute_logic(self, input_data):
        # Your logic here
        return {"result": "success"}
```

## 📚 Resources

- FastAPI Docs: https://fastapi.tiangolo.com
- Python asyncio: https://docs.python.org/3/library/asyncio.html
- SVG Tutorial: https://developer.mozilla.org/en-US/docs/Web/SVG

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the example code
3. Check API documentation at `/docs`

## ✅ Checklist for Hackathon

- [ ] Backend running on `http://localhost:8000`
- [ ] Frontend opens without errors
- [ ] Can generate systems from templates
- [ ] Visualization displays correctly
- [ ] Can run simulations
- [ ] Metrics update properly
- [ ] Can export JSON
- [ ] API documentation accessible

## 🎉 You're Ready!

Your multi-agent system is now ready for your hackathon demo!

**Quick Demo Flow:**
1. Open frontend
2. Click "Customer Support" template
3. Click "Generate Agent System"
4. Watch the beautiful visualization
5. Click "Run Simulation"
6. Show the metrics and logs
7. Export JSON to show the system configuration

Good luck! 🚀
