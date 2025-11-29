// Multi-Agent System Core Logic

class AgentSystem {
    constructor() {
        this.agents = [];
        this.communications = [];
        this.memory = {};
        this.metrics = {
            totalExecutions: 0,
            successfulExecutions: 0,
            averageResponseTime: 0,
            executionTimes: []
        };
    }

    generateFromWorkflow(workflowDescription) {
        // Parse workflow and generate agents
        const agents = this.parseWorkflowToAgents(workflowDescription);
        const communications = this.generateCommunications(agents);
        
        return {
            systemName: this.extractSystemName(workflowDescription),
            agents: agents,
            communications: communications,
            memory: {
                type: "shared",
                strategy: "event-driven",
                persistence: "in-memory"
            },
            metrics: {
                enabled: true,
                trackResponseTime: true,
                trackSuccessRate: true,
                trackAgentLoad: true
            }
        };
    }

    parseWorkflowToAgents(workflow) {
        const agents = [];
        const lines = workflow.toLowerCase().split('\n').filter(l => l.trim());
        
        // Detect workflow type and generate appropriate agents
        if (workflow.toLowerCase().includes('customer') || workflow.toLowerCase().includes('support')) {
            agents.push(
                this.createAgent('intake', 'Intake Agent', 'Receives and validates customer inquiries', 
                    ['receive_request', 'validate_input', 'log_inquiry'], '🎯'),
                this.createAgent('classifier', 'Classification Agent', 'Categorizes issues and determines priority',
                    ['classify_issue', 'assess_priority', 'route_decision'], '🏷️'),
                this.createAgent('resolver', 'Resolution Agent', 'Generates solutions and responses',
                    ['analyze_issue', 'generate_solution', 'create_response'], '💡'),
                this.createAgent('quality', 'Quality Agent', 'Reviews responses for accuracy and tone',
                    ['review_response', 'check_quality', 'approve_or_revise'], '✅'),
                this.createAgent('followup', 'Follow-up Agent', 'Schedules and manages follow-ups',
                    ['schedule_followup', 'track_resolution', 'close_ticket'], '📅')
            );
        } else if (workflow.toLowerCase().includes('ecommerce') || workflow.toLowerCase().includes('order')) {
            agents.push(
                this.createAgent('order', 'Order Agent', 'Processes incoming orders',
                    ['receive_order', 'validate_items', 'check_inventory'], '🛒'),
                this.createAgent('payment', 'Payment Agent', 'Handles payment processing',
                    ['process_payment', 'verify_transaction', 'handle_refunds'], '💳'),
                this.createAgent('inventory', 'Inventory Agent', 'Manages stock and availability',
                    ['check_stock', 'reserve_items', 'update_inventory'], '📦'),
                this.createAgent('shipping', 'Shipping Agent', 'Coordinates delivery',
                    ['calculate_shipping', 'generate_label', 'track_shipment'], '🚚'),
                this.createAgent('notification', 'Notification Agent', 'Sends customer updates',
                    ['send_confirmation', 'send_tracking', 'send_delivery_notice'], '📧')
            );
        } else if (workflow.toLowerCase().includes('content') || workflow.toLowerCase().includes('creation')) {
            agents.push(
                this.createAgent('planner', 'Content Planner', 'Plans content strategy and topics',
                    ['analyze_trends', 'generate_ideas', 'create_calendar'], '📋'),
                this.createAgent('writer', 'Content Writer', 'Creates written content',
                    ['write_draft', 'research_topic', 'optimize_seo'], '✍️'),
                this.createAgent('editor', 'Content Editor', 'Reviews and refines content',
                    ['review_content', 'check_grammar', 'improve_clarity'], '📝'),
                this.createAgent('designer', 'Visual Designer', 'Creates visual assets',
                    ['design_graphics', 'create_thumbnails', 'format_layout'], '🎨'),
                this.createAgent('publisher', 'Publishing Agent', 'Publishes and distributes content',
                    ['schedule_post', 'publish_content', 'track_performance'], '🚀')
            );
        } else if (workflow.toLowerCase().includes('hr') || workflow.toLowerCase().includes('recruit')) {
            agents.push(
                this.createAgent('sourcing', 'Sourcing Agent', 'Finds and attracts candidates',
                    ['search_candidates', 'post_jobs', 'reach_out'], '🔍'),
                this.createAgent('screening', 'Screening Agent', 'Reviews applications and resumes',
                    ['parse_resume', 'match_requirements', 'score_candidates'], '📄'),
                this.createAgent('interview', 'Interview Agent', 'Coordinates interview process',
                    ['schedule_interviews', 'send_invites', 'collect_feedback'], '🗓️'),
                this.createAgent('assessment', 'Assessment Agent', 'Evaluates candidate fit',
                    ['analyze_responses', 'score_interviews', 'generate_report'], '📊'),
                this.createAgent('offer', 'Offer Agent', 'Manages offer process',
                    ['generate_offer', 'negotiate_terms', 'onboard_candidate'], '🤝')
            );
        } else {
            // Generic workflow
            agents.push(
                this.createAgent('input', 'Input Agent', 'Receives and validates input',
                    ['receive_data', 'validate', 'preprocess'], '📥'),
                this.createAgent('processor', 'Processing Agent', 'Processes the main workflow',
                    ['analyze', 'transform', 'execute'], '⚙️'),
                this.createAgent('output', 'Output Agent', 'Formats and delivers output',
                    ['format_result', 'validate_output', 'deliver'], '📤')
            );
        }

        return agents;
    }

    createAgent(id, name, role, tools, icon) {
        return {
            id: id,
            name: name,
            role: role,
            responsibilities: [role],
            tools: tools,
            icon: icon,
            memory: {
                access: "read-write",
                scope: "shared"
            },
            position: { x: 0, y: 0 } // Will be set by visualization
        };
    }

    generateCommunications(agents) {
        const communications = [];
        
        // Create sequential communication flow
        for (let i = 0; i < agents.length - 1; i++) {
            communications.push({
                from: agents[i].id,
                to: agents[i + 1].id,
                protocol: "async-message",
                dataFormat: "json",
                trigger: "on-completion"
            });
        }

        // Add feedback loops for certain agent types
        if (agents.length > 2) {
            communications.push({
                from: agents[agents.length - 1].id,
                to: agents[0].id,
                protocol: "async-message",
                dataFormat: "json",
                trigger: "on-error"
            });
        }

        return communications;
    }

    extractSystemName(workflow) {
        const firstLine = workflow.split('\n')[0].trim();
        if (firstLine.length > 0 && firstLine.length < 50) {
            return firstLine.replace(/[^a-zA-Z0-9\s]/g, '');
        }
        return "Multi-Agent System";
    }

    async simulateExecution(system) {
        const logs = [];
        const startTime = Date.now();

        logs.push({
            timestamp: new Date().toISOString(),
            type: 'info',
            message: `Starting execution of ${system.systemName}`
        });

        for (const agent of system.agents) {
            const agentStartTime = Date.now();
            
            logs.push({
                timestamp: new Date().toISOString(),
                type: 'info',
                message: `Agent ${agent.name} started processing`
            });

            // Simulate processing time
            await this.sleep(Math.random() * 1000 + 500);

            const success = Math.random() > 0.1; // 90% success rate
            
            if (success) {
                logs.push({
                    timestamp: new Date().toISOString(),
                    type: 'success',
                    message: `Agent ${agent.name} completed successfully (${Date.now() - agentStartTime}ms)`
                });
            } else {
                logs.push({
                    timestamp: new Date().toISOString(),
                    type: 'error',
                    message: `Agent ${agent.name} encountered an error`
                });
            }

            this.metrics.executionTimes.push(Date.now() - agentStartTime);
        }

        const totalTime = Date.now() - startTime;
        this.metrics.totalExecutions++;
        this.metrics.successfulExecutions++;
        this.metrics.averageResponseTime = 
            this.metrics.executionTimes.reduce((a, b) => a + b, 0) / this.metrics.executionTimes.length;

        logs.push({
            timestamp: new Date().toISOString(),
            type: 'success',
            message: `Execution completed in ${totalTime}ms`
        });

        return logs;
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    getMetrics() {
        return {
            totalExecutions: this.metrics.totalExecutions,
            successfulExecutions: this.metrics.successfulExecutions,
            averageResponseTime: Math.round(this.metrics.averageResponseTime),
            successRate: this.metrics.totalExecutions > 0 
                ? Math.round((this.metrics.successfulExecutions / this.metrics.totalExecutions) * 100)
                : 0
        };
    }
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AgentSystem;
}
