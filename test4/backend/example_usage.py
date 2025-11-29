"""
Example usage of the Multi-Agent System
"""

import asyncio
from agent_framework import AgentStrand, MultiAgentSystem, AgentMemory, Tool
from specialized_agents import (
    IntakeAgent, ClassificationAgent, ProcessingAgent,
    ResolutionAgent, QualityAgent, NotificationAgent
)


async def example_customer_support():
    """Example: Customer Support Workflow"""
    
    print("=" * 60)
    print("CUSTOMER SUPPORT WORKFLOW EXAMPLE")
    print("=" * 60)
    
    # Create agents
    intake = IntakeAgent("intake", "Intake Agent", "Receives customer inquiries")
    classifier = ClassificationAgent("classifier", "Classification Agent", "Categorizes issues")
    resolver = ResolutionAgent("resolver", "Resolution Agent", "Generates solutions")
    quality = QualityAgent("quality", "Quality Agent", "Reviews responses")
    notifier = NotificationAgent("notifier", "Notification Agent", "Sends updates")
    
    # Create strand
    shared_memory = AgentMemory()
    strand = AgentStrand("customer_support", [intake, classifier, resolver, quality, notifier], shared_memory)
    
    # Setup communication
    strand.add_communication("intake", "classifier")
    strand.add_communication("classifier", "resolver")
    strand.add_communication("resolver", "quality")
    strand.add_communication("quality", "notifier")
    
    # Execute
    input_data = {
        "customer_id": "CUST-12345",
        "message": "I have an urgent payment issue with my last transaction",
        "channel": "email",
        "timestamp": "2024-01-15T10:30:00Z"
    }
    
    print("\nInput Data:")
    print(input_data)
    print("\nExecuting strand...")
    
    result = await strand.execute_sequential(input_data)
    
    print("\n" + "=" * 60)
    print("EXECUTION RESULTS")
    print("=" * 60)
    
    for i, agent_result in enumerate(result["results"], 1):
        print(f"\nStep {i}: {agent_result.get('agent', 'Unknown')}")
        print(f"Status: {agent_result.get('status', 'N/A')}")
        if 'category' in agent_result:
            print(f"Category: {agent_result['category']}")
        if 'solution' in agent_result:
            print(f"Solution Type: {agent_result['solution']['type']}")
        if 'quality_score' in agent_result:
            print(f"Quality Score: {agent_result['quality_score']:.2f}")
    
    print("\n" + "=" * 60)
    print("AGENT METRICS")
    print("=" * 60)
    
    metrics = strand.get_all_metrics()
    for metric in metrics:
        print(f"\n{metric['agent_name']}:")
        print(f"  Executions: {metric['total_executions']}")
        print(f"  Success Rate: {metric['success_rate']:.1f}%")
        print(f"  Avg Time: {metric['average_execution_time']:.2f}s")
    
    print("\n" + "=" * 60)
    print("EXECUTION LOGS")
    print("=" * 60)
    
    logs = strand.get_all_logs()
    for log in logs[-10:]:  # Last 10 logs
        print(f"[{log['agent']}] {log['message']}")


async def example_parallel_execution():
    """Example: Parallel Agent Execution"""
    
    print("\n\n" + "=" * 60)
    print("PARALLEL EXECUTION EXAMPLE")
    print("=" * 60)
    
    # Create multiple processing agents
    agent1 = ProcessingAgent("proc1", "Processor 1", "Handles data processing")
    agent2 = ProcessingAgent("proc2", "Processor 2", "Handles data processing")
    agent3 = ProcessingAgent("proc3", "Processor 3", "Handles data processing")
    
    strand = AgentStrand("parallel_processing", [agent1, agent2, agent3])
    
    input_data = {"task": "Process large dataset", "chunks": 3}
    
    print("\nExecuting agents in parallel...")
    result = await strand.execute_parallel(input_data)
    
    print(f"\nProcessed {len(result['results'])} tasks in parallel")
    print(f"All agents completed successfully")


async def example_multi_system():
    """Example: Multi-Agent System with Multiple Strands"""
    
    print("\n\n" + "=" * 60)
    print("MULTI-SYSTEM EXAMPLE")
    print("=" * 60)
    
    # Create system
    system = MultiAgentSystem("Enterprise System")
    
    # Create customer support strand
    cs_agents = [
        IntakeAgent("cs_intake", "CS Intake", "Customer support intake"),
        ResolutionAgent("cs_resolver", "CS Resolver", "Customer support resolution")
    ]
    cs_strand = AgentStrand("customer_support", cs_agents)
    system.add_strand(cs_strand)
    
    # Create order processing strand
    order_agents = [
        IntakeAgent("order_intake", "Order Intake", "Order processing"),
        ProcessingAgent("order_processor", "Order Processor", "Order fulfillment")
    ]
    order_strand = AgentStrand("order_processing", order_agents)
    system.add_strand(order_strand)
    
    # Execute customer support
    print("\nExecuting Customer Support strand...")
    cs_result = await system.execute_strand(
        "customer_support",
        {"type": "support_ticket", "issue": "Account access"},
        "sequential"
    )
    
    # Execute order processing
    print("Executing Order Processing strand...")
    order_result = await system.execute_strand(
        "order_processing",
        {"type": "new_order", "items": ["item1", "item2"]},
        "sequential"
    )
    
    # Get system metrics
    print("\n" + "=" * 60)
    print("SYSTEM METRICS")
    print("=" * 60)
    
    metrics = system.get_system_metrics()
    print(f"\nSystem: {metrics['system_name']}")
    print(f"Total Strands: {metrics['total_strands']}")
    print(f"Total Agents: {metrics['total_agents']}")


async def example_with_tools():
    """Example: Agent with Custom Tools"""
    
    print("\n\n" + "=" * 60)
    print("AGENT WITH TOOLS EXAMPLE")
    print("=" * 60)
    
    # Define custom tools
    async def search_database(query: str):
        await asyncio.sleep(0.2)
        return {"results": [f"Result for {query}"]}
    
    async def send_email(to: str, subject: str):
        await asyncio.sleep(0.1)
        return {"status": "sent", "to": to}
    
    # Create tools
    search_tool = Tool("search_database", "Search the database", search_database)
    email_tool = Tool("send_email", "Send an email", send_email)
    
    # Create agent with tools
    agent = ProcessingAgent(
        "tool_agent",
        "Tool Agent",
        "Agent with custom tools",
        tools=[search_tool, email_tool]
    )
    
    print(f"\nAgent: {agent.name}")
    print(f"Tools: {[tool.name for tool in agent.tools]}")
    
    # Use tools
    print("\nUsing search tool...")
    search_result = await agent.use_tool("search_database").execute("customer data")
    print(f"Search result: {search_result}")
    
    print("\nUsing email tool...")
    email_result = await agent.use_tool("send_email").execute("customer@example.com", "Update")
    print(f"Email result: {email_result}")


async def main():
    """Run all examples"""
    
    # Run examples
    await example_customer_support()
    await example_parallel_execution()
    await example_multi_system()
    await example_with_tools()
    
    print("\n\n" + "=" * 60)
    print("ALL EXAMPLES COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
