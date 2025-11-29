"""
Quick test script to verify the system works
"""

import asyncio
import sys

def test_imports():
    """Test if all modules can be imported"""
    print("Testing imports...")
    try:
        from agent_framework import Agent, AgentStrand, MultiAgentSystem, AgentMemory
        from specialized_agents import IntakeAgent, ClassificationAgent
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False


async def test_basic_agent():
    """Test basic agent functionality"""
    print("\nTesting basic agent...")
    try:
        from agent_framework import Agent, AgentMemory
        
        agent = Agent("test", "Test Agent", "Testing", memory=AgentMemory())
        result = await agent.process({"test": "data"})
        
        assert result["status"] == "success"
        assert agent.metrics["total_executions"] == 1
        
        print("✅ Basic agent works")
        return True
    except Exception as e:
        print(f"❌ Agent test failed: {e}")
        return False


async def test_specialized_agents():
    """Test specialized agents"""
    print("\nTesting specialized agents...")
    try:
        from specialized_agents import IntakeAgent, ClassificationAgent
        
        intake = IntakeAgent("intake", "Intake", "Test intake")
        result = await intake.process({"message": "urgent payment issue"})
        
        assert result["validated"] == True
        assert "request_id" in result
        
        classifier = ClassificationAgent("classifier", "Classifier", "Test classifier")
        result2 = await classifier.process(result)
        
        assert "category" in result2
        
        print("✅ Specialized agents work")
        return True
    except Exception as e:
        print(f"❌ Specialized agent test failed: {e}")
        return False


async def test_strand():
    """Test agent strand"""
    print("\nTesting agent strand...")
    try:
        from agent_framework import AgentStrand
        from specialized_agents import IntakeAgent, ProcessingAgent
        
        agents = [
            IntakeAgent("a1", "Agent 1", "First"),
            ProcessingAgent("a2", "Agent 2", "Second")
        ]
        
        strand = AgentStrand("test_strand", agents)
        result = await strand.execute_sequential({"test": "data"})
        
        assert "results" in result
        assert len(result["results"]) == 2
        
        print("✅ Agent strand works")
        return True
    except Exception as e:
        print(f"❌ Strand test failed: {e}")
        return False


async def test_multi_system():
    """Test multi-agent system"""
    print("\nTesting multi-agent system...")
    try:
        from agent_framework import MultiAgentSystem, AgentStrand
        from specialized_agents import IntakeAgent
        
        system = MultiAgentSystem("Test System")
        
        agents = [IntakeAgent("a1", "Agent 1", "Test")]
        strand = AgentStrand("test", agents)
        
        system.add_strand(strand)
        result = await system.execute_strand("test", {"data": "test"}, "sequential")
        
        assert "results" in result
        
        metrics = system.get_system_metrics()
        assert metrics["total_agents"] == 1
        
        print("✅ Multi-agent system works")
        return True
    except Exception as e:
        print(f"❌ Multi-system test failed: {e}")
        return False


async def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("MULTI-AGENT SYSTEM TEST SUITE")
    print("=" * 60)
    
    results = []
    
    # Test imports
    results.append(test_imports())
    
    # Test basic functionality
    results.append(await test_basic_agent())
    results.append(await test_specialized_agents())
    results.append(await test_strand())
    results.append(await test_multi_system())
    
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("✅ All tests passed! System is ready.")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
