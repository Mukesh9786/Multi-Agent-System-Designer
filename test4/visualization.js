// Visualization Engine for Agent Workflow

class AgentVisualizer {
    constructor(canvasElement) {
        this.canvas = canvasElement;
        this.agents = [];
        this.connections = [];
        this.selectedAgent = null;
        this.scale = 1;
        this.offset = { x: 0, y: 0 };
        this.isDragging = false;
        this.draggedAgent = null;
        this.animationFrame = null;
    }

    render(system) {
        this.clear();
        this.agents = system.agents;
        this.connections = system.communications;
        
        // Calculate positions
        this.calculatePositions();
        
        // Draw connections first (so they appear behind agents)
        this.drawConnections();
        
        // Draw agents
        this.drawAgents();
        
        // Setup interactions
        this.setupInteractions();
    }

    calculatePositions() {
        const canvasWidth = this.canvas.offsetWidth;
        const canvasHeight = this.canvas.offsetHeight;
        const agentCount = this.agents.length;
        
        if (agentCount <= 3) {
            // Linear layout for small number of agents
            const spacing = canvasWidth / (agentCount + 1);
            this.agents.forEach((agent, index) => {
                agent.position = {
                    x: spacing * (index + 1),
                    y: canvasHeight / 2
                };
            });
        } else if (agentCount <= 6) {
            // Two-row layout
            const cols = Math.ceil(agentCount / 2);
            const spacingX = canvasWidth / (cols + 1);
            const spacingY = canvasHeight / 3;
            
            this.agents.forEach((agent, index) => {
                const row = Math.floor(index / cols);
                const col = index % cols;
                agent.position = {
                    x: spacingX * (col + 1),
                    y: spacingY * (row + 1)
                };
            });
        } else {
            // Circular layout for many agents
            const centerX = canvasWidth / 2;
            const centerY = canvasHeight / 2;
            const radius = Math.min(canvasWidth, canvasHeight) * 0.35;
            
            this.agents.forEach((agent, index) => {
                const angle = (index / agentCount) * 2 * Math.PI - Math.PI / 2;
                agent.position = {
                    x: centerX + radius * Math.cos(angle),
                    y: centerY + radius * Math.sin(angle)
                };
            });
        }
    }

    drawAgents() {
        this.agents.forEach(agent => {
            const node = document.createElement('div');
            node.className = 'agent-node';
            node.id = `agent-${agent.id}`;
            node.style.left = `${agent.position.x - 90}px`;
            node.style.top = `${agent.position.y - 50}px`;
            
            node.innerHTML = `
                <div class="agent-icon">${agent.icon}</div>
                <div class="agent-name">${agent.name}</div>
                <div class="agent-role">${agent.role.substring(0, 30)}...</div>
            `;
            
            node.addEventListener('click', (e) => {
                e.stopPropagation();
                this.selectAgent(agent);
            });
            
            node.addEventListener('mousedown', (e) => {
                this.startDrag(agent, e);
            });
            
            this.canvas.appendChild(node);
        });
    }

    drawConnections() {
        // Create SVG for connections
        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.style.position = 'absolute';
        svg.style.top = '0';
        svg.style.left = '0';
        svg.style.width = '100%';
        svg.style.height = '100%';
        svg.style.pointerEvents = 'none';
        
        // Define arrowhead marker
        const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
        const marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
        marker.setAttribute('id', 'arrowhead');
        marker.setAttribute('markerWidth', '10');
        marker.setAttribute('markerHeight', '10');
        marker.setAttribute('refX', '9');
        marker.setAttribute('refY', '3');
        marker.setAttribute('orient', 'auto');
        
        const polygon = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
        polygon.setAttribute('points', '0 0, 10 3, 0 6');
        polygon.setAttribute('fill', '#667eea');
        
        marker.appendChild(polygon);
        defs.appendChild(marker);
        svg.appendChild(defs);
        
        // Draw connection lines
        this.connections.forEach(conn => {
            const fromAgent = this.agents.find(a => a.id === conn.from);
            const toAgent = this.agents.find(a => a.id === conn.to);
            
            if (fromAgent && toAgent) {
                const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                line.setAttribute('x1', fromAgent.position.x);
                line.setAttribute('y1', fromAgent.position.y);
                line.setAttribute('x2', toAgent.position.x);
                line.setAttribute('y2', toAgent.position.y);
                line.setAttribute('stroke', '#667eea');
                line.setAttribute('stroke-width', '2');
                line.setAttribute('marker-end', 'url(#arrowhead)');
                
                svg.appendChild(line);
            }
        });
        
        this.canvas.insertBefore(svg, this.canvas.firstChild);
    }

    selectAgent(agent) {
        // Remove previous selection
        const prevSelected = this.canvas.querySelector('.agent-node.selected');
        if (prevSelected) {
            prevSelected.classList.remove('selected');
        }
        
        // Add new selection
        const node = document.getElementById(`agent-${agent.id}`);
        if (node) {
            node.classList.add('selected');
        }
        
        this.selectedAgent = agent;
        this.showAgentDetails(agent);
    }

    showAgentDetails(agent) {
        const detailsContent = document.getElementById('detailsContent');
        detailsContent.innerHTML = `
            <div class="detail-item">
                <span class="detail-label">Name:</span> ${agent.name}
            </div>
            <div class="detail-item">
                <span class="detail-label">Role:</span> ${agent.role}
            </div>
            <div class="detail-item">
                <span class="detail-label">Tools:</span> ${agent.tools.join(', ')}
            </div>
            <div class="detail-item">
                <span class="detail-label">Memory Access:</span> ${agent.memory.access}
            </div>
            <div class="detail-item">
                <span class="detail-label">Memory Scope:</span> ${agent.memory.scope}
            </div>
        `;
    }

    startDrag(agent, event) {
        this.isDragging = true;
        this.draggedAgent = agent;
        this.dragOffset = {
            x: event.clientX - agent.position.x,
            y: event.clientY - agent.position.y
        };
    }

    setupInteractions() {
        document.addEventListener('mousemove', (e) => {
            if (this.isDragging && this.draggedAgent) {
                const rect = this.canvas.getBoundingClientRect();
                this.draggedAgent.position.x = e.clientX - rect.left - this.dragOffset.x;
                this.draggedAgent.position.y = e.clientY - rect.top - this.dragOffset.y;
                this.updateAgentPosition(this.draggedAgent);
                this.updateConnections();
            }
        });
        
        document.addEventListener('mouseup', () => {
            this.isDragging = false;
            this.draggedAgent = null;
        });
    }

    updateAgentPosition(agent) {
        const node = document.getElementById(`agent-${agent.id}`);
        if (node) {
            node.style.left = `${agent.position.x - 90}px`;
            node.style.top = `${agent.position.y - 50}px`;
        }
    }

    updateConnections() {
        const svg = this.canvas.querySelector('svg');
        if (svg) {
            svg.remove();
            this.drawConnections();
        }
    }

    clear() {
        this.canvas.innerHTML = '';
        this.selectedAgent = null;
    }

    zoomIn() {
        this.scale = Math.min(this.scale * 1.2, 3);
        this.applyTransform();
    }

    zoomOut() {
        this.scale = Math.max(this.scale / 1.2, 0.5);
        this.applyTransform();
    }

    resetView() {
        this.scale = 1;
        this.offset = { x: 0, y: 0 };
        this.applyTransform();
    }

    applyTransform() {
        this.canvas.style.transform = `scale(${this.scale}) translate(${this.offset.x}px, ${this.offset.y}px)`;
    }

    animateExecution(communications) {
        let index = 0;
        
        const animate = () => {
            if (index >= communications.length) {
                return;
            }
            
            const conn = communications[index];
            const fromAgent = this.agents.find(a => a.id === conn.from);
            const toAgent = this.agents.find(a => a.id === conn.to);
            
            if (fromAgent && toAgent) {
                // Highlight agents
                const fromNode = document.getElementById(`agent-${fromAgent.id}`);
                const toNode = document.getElementById(`agent-${toAgent.id}`);
                
                if (fromNode) fromNode.style.borderColor = '#4caf50';
                
                setTimeout(() => {
                    if (toNode) toNode.style.borderColor = '#4caf50';
                    
                    setTimeout(() => {
                        if (fromNode) fromNode.style.borderColor = '#667eea';
                        if (toNode) toNode.style.borderColor = '#667eea';
                        index++;
                        animate();
                    }, 500);
                }, 500);
            } else {
                index++;
                animate();
            }
        };
        
        animate();
    }
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AgentVisualizer;
}
