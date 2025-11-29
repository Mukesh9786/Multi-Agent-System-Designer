// Main Application Logic

let agentSystem = new AgentSystem();
let visualizer = null;
let currentSystem = null;

// Templates
const templates = {
    'customer-support': `Customer Support System
- Receive customer inquiry via email, chat, or phone
- Validate and log the inquiry
- Classify the issue type (technical, billing, general)
- Assess priority level
- Route to appropriate department
- Generate initial response
- Review response for quality and tone
- Send response to customer
- Schedule follow-up if needed
- Track resolution status`,

    'ecommerce': `E-Commerce Order Processing
- Receive new order from customer
- Validate order details and items
- Check inventory availability
- Process payment transaction
- Verify payment success
- Reserve items in inventory
- Calculate shipping cost and method
- Generate shipping label
- Send order confirmation to customer
- Update inventory levels
- Track shipment status
- Send delivery notification`,

    'content': `Content Creation Workflow
- Analyze market trends and audience interests
- Generate content ideas and topics
- Create content calendar
- Research topic in depth
- Write initial draft
- Optimize for SEO
- Review content for quality
- Check grammar and clarity
- Design visual assets and graphics
- Format layout and styling
- Schedule publication
- Publish content across channels
- Track performance metrics`,

    'hr': `HR Recruitment Process
- Post job openings on multiple platforms
- Source and attract potential candidates
- Receive and parse applications
- Screen resumes against requirements
- Score and rank candidates
- Schedule initial screening calls
- Conduct phone interviews
- Collect and analyze feedback
- Schedule in-person interviews
- Coordinate interview panels
- Evaluate candidate responses
- Generate assessment reports
- Create job offer
- Negotiate terms and compensation
- Send offer letter
- Begin onboarding process`
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('canvas');
    visualizer = new AgentVisualizer(canvas);
    
    setupEventListeners();
});

function setupEventListeners() {
    // Generate button
    document.getElementById('generateBtn').addEventListener('click', generateSystem);
    
    // Template buttons
    document.querySelectorAll('.template-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const template = e.target.dataset.template;
            document.getElementById('workflowInput').value = templates[template];
        });
    });
    
    // Zoom controls
    document.getElementById('zoomIn').addEventListener('click', () => {
        visualizer.zoomIn();
    });
    
    document.getElementById('zoomOut').addEventListener('click', () => {
        visualizer.zoomOut();
    });
    
    document.getElementById('resetView').addEventListener('click', () => {
        visualizer.resetView();
    });
    
    // Export JSON
    document.getElementById('exportJson').addEventListener('click', exportJSON);
    
    // Run simulation
    document.getElementById('runSimulation').addEventListener('click', runSimulation);
    
    // Tab switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            switchTab(e.target.dataset.tab);
        });
    });
}

function generateSystem() {
    const workflowInput = document.getElementById('workflowInput').value.trim();
    
    if (!workflowInput) {
        alert('Please enter a workflow description or select a template.');
        return;
    }
    
    // Generate the agent system
    currentSystem = agentSystem.generateFromWorkflow(workflowInput);
    
    // Visualize
    visualizer.render(currentSystem);
    
    // Update JSON output
    updateJSONOutput(currentSystem);
    
    // Update metrics
    updateMetrics();
    
    // Show success message
    addLog('System generated successfully', 'success');
}

function updateJSONOutput(system) {
    const jsonOutput = document.getElementById('jsonOutput');
    jsonOutput.textContent = JSON.stringify(system, null, 2);
}

function updateMetrics() {
    if (!currentSystem) return;
    
    document.getElementById('totalAgents').textContent = currentSystem.agents.length;
    document.getElementById('totalPaths').textContent = currentSystem.communications.length;
    
    const metrics = agentSystem.getMetrics();
    document.getElementById('avgResponseTime').textContent = 
        metrics.averageResponseTime > 0 ? `${metrics.averageResponseTime}ms` : '-';
    document.getElementById('successRate').textContent = 
        metrics.successRate > 0 ? `${metrics.successRate}%` : '-';
}

async function runSimulation() {
    if (!currentSystem) {
        alert('Please generate a system first.');
        return;
    }
    
    // Clear previous logs
    document.getElementById('logsOutput').innerHTML = '';
    
    // Switch to logs tab
    switchTab('logs');
    
    // Add starting log
    addLog('Starting simulation...', 'info');
    
    // Animate the visualization
    visualizer.animateExecution(currentSystem.communications);
    
    // Run simulation
    const logs = await agentSystem.simulateExecution(currentSystem);
    
    // Display logs
    logs.forEach(log => {
        addLog(log.message, log.type, log.timestamp);
    });
    
    // Update metrics
    updateMetrics();
}

function addLog(message, type = 'info', timestamp = null) {
    const logsOutput = document.getElementById('logsOutput');
    const logEntry = document.createElement('div');
    logEntry.className = `log-entry ${type}`;
    
    const time = timestamp || new Date().toISOString();
    logEntry.innerHTML = `
        <span class="timestamp">[${new Date(time).toLocaleTimeString()}]</span>
        ${message}
    `;
    
    logsOutput.appendChild(logEntry);
    logsOutput.scrollTop = logsOutput.scrollHeight;
}

function switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.tab === tabName) {
            btn.classList.add('active');
        }
    });
    
    // Update tab panes
    document.querySelectorAll('.tab-pane').forEach(pane => {
        pane.classList.remove('active');
    });
    
    const activePane = document.getElementById(`${tabName}Tab`);
    if (activePane) {
        activePane.classList.add('active');
    }
}

function exportJSON() {
    if (!currentSystem) {
        alert('Please generate a system first.');
        return;
    }
    
    const dataStr = JSON.stringify(currentSystem, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = `${currentSystem.systemName.replace(/\s+/g, '-').toLowerCase()}-agent-system.json`;
    link.click();
    
    URL.revokeObjectURL(url);
    addLog('System exported successfully', 'success');
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to generate
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        generateSystem();
    }
    
    // Ctrl/Cmd + E to export
    if ((e.ctrlKey || e.metaKey) && e.key === 'e') {
        e.preventDefault();
        exportJSON();
    }
    
    // Ctrl/Cmd + R to run simulation
    if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
        e.preventDefault();
        runSimulation();
    }
});
