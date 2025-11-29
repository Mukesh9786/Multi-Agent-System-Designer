# 🚀 START HERE - Quick Demo Guide

## For Your Hackathon Demo (Easiest Way)

### Step 1: Run the Frontend (No Installation Required!)

1. Simply open `index.html` in your browser
2. That's it! The app works standalone.

### Step 2: Try It Out

1. Click **"Customer Support"** template button
2. Click **"Generate Agent System"**
3. Watch the beautiful visualization appear with animated nodes
4. Click **"Run Simulation"** to see agents communicate
5. Check the **Metrics** tab to see performance data
6. Click **"Export JSON"** to download the system configuration

**Perfect for quick demos!** No backend needed.

---

## Want the Full Backend? (Optional)

### Install Backend (One-Time Setup)

Open a terminal/command prompt:

```bash
cd backend
pip install -r requirements.txt
```

### Start the Backend Server

```bash
cd backend
python run_server.py
```

You should see:
```
Starting Multi-Agent System API Server
API Documentation: http://localhost:8000/docs
```

### Connect Frontend to Backend

1. Open `index.html` in a text editor
2. Find this line (near the end):
   ```html
   <script src="app.js"></script>
   ```
3. Change it to:
   ```html
   <script src="app-with-backend.js"></script>
   ```
4. Save and refresh your browser

Now the frontend will use the real backend for execution!

---

## 🎯 Demo Script for Judges

### 1. Introduction (30 seconds)
"This is a Multi-Agent System Designer that converts any business workflow into an intelligent agent system with beautiful visualization."

### 2. Show Templates (30 seconds)
- Click through different templates
- Show how it understands different domains
- "We have pre-built templates for Customer Support, E-Commerce, Content Creation, and HR"

### 3. Generate System (1 minute)
- Select "Customer Support" template
- Click "Generate Agent System"
- Point out the visualization:
  - "Each node is an intelligent agent"
  - "Arrows show communication flow"
  - "You can drag agents around"
  - Click on an agent to show details

### 4. Run Simulation (1 minute)
- Click "Run Simulation"
- Show the animation
- Switch to "Logs" tab: "Real-time execution logs"
- Switch to "Metrics" tab: "Performance tracking"

### 5. Show JSON Export (30 seconds)
- Click "Export JSON"
- Open the file
- "This is deployment-ready configuration for AWS Bedrock or any agent platform"

### 6. Backend Demo (Optional - 1 minute)
- Show API documentation at `http://localhost:8000/docs`
- "We have a full Python backend with FastAPI"
- "Supports sequential, parallel, and graph-based execution"
- Show the example execution

**Total Time: 3-4 minutes**

---

## 🎨 Key Features to Highlight

1. **Beautiful UI** - N8N-style workflow visualization
2. **Smart Generation** - Automatically creates appropriate agents
3. **Real Execution** - Not just mockups, actually runs
4. **Production Ready** - Full backend with API
5. **Extensible** - Easy to add new agent types
6. **Metrics** - Built-in performance tracking

---

## 🐛 Troubleshooting

### Frontend won't open?
- Make sure you're opening `index.html` in a modern browser (Chrome, Firefox, Edge)
- Try right-click → Open with → Chrome

### Backend won't start?
```bash
# Install dependencies
pip install fastapi uvicorn pydantic aiohttp python-dotenv

# Try running directly
python backend/run_server.py
```

### Can't see the visualization?
- Check browser console (F12) for errors
- Make sure JavaScript is enabled
- Try a different browser

---

## 📁 What Each File Does

### Frontend Files
- `index.html` - Main application page
- `styles.css` - Beautiful styling
- `agent-system.js` - Agent logic (local mode)
- `visualization.js` - Canvas and node rendering
- `app.js` - App controller (standalone)
- `app-with-backend.js` - App controller (with backend)

### Backend Files
- `backend/agent_framework.py` - Core agent system
- `backend/specialized_agents.py` - Pre-built agents
- `backend/api.py` - FastAPI REST API
- `backend/run_server.py` - Server startup
- `backend/example_usage.py` - Usage examples
- `backend/test_system.py` - Test suite

---

## 💡 Tips for Best Demo

1. **Practice the flow** - Run through it 2-3 times
2. **Have both modes ready** - Frontend-only and full-stack
3. **Prepare the browser** - Have tabs open and ready
4. **Show the code** - Judges love seeing actual implementation
5. **Explain the architecture** - Strand-based, async, scalable
6. **Mention use cases** - Customer support, order processing, content creation

---

## 🎉 You're Ready!

Your multi-agent system is production-ready and demo-ready!

**Quick checklist:**
- ✅ Frontend opens and looks beautiful
- ✅ Can generate systems from templates
- ✅ Visualization is smooth and interactive
- ✅ Simulation runs and shows logs
- ✅ Can export JSON
- ✅ (Optional) Backend API is running

**Good luck with your hackathon! 🚀**

---

## 📞 Need Help?

Check these files:
- `README.md` - Full documentation
- `SETUP.md` - Detailed setup instructions
- `backend/README.md` - Backend documentation
- `backend/example_usage.py` - Code examples

The system is designed to work out of the box. If something doesn't work, the frontend-only mode will always work as a fallback!
