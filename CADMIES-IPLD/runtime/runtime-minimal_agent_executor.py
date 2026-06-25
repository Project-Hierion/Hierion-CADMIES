#!/usr/bin/env python3
"""
File: runtime_minimal_agent_executor.py
Tool: CADMIES Minimal Agent Executor
Version: 1.0.0
System: CADMIES / agents
Status: ACTIVE
License: AGPLv3 with Commons Clause

Purpose: Execute AgentNode specifications by loading and running their
         implementations. Air-gapped compatible. Uses existing tools + stdlib.

Usage:
    python agents/runtime_minimal_agent_executor.py
"""

import json
import sys
import importlib.util
from pathlib import Path
from typing import Dict, Any, Optional

def load_agent_spec_direct(agent_identifier: str) -> Dict[str, Any]:
    """
    Load agent spec directly using same logic as cbor_reader.
    Air-gapped, no external dependencies, builds on existing patterns.
    """
    import dag_cbor
    from pathlib import Path
    
    project_root = Path(__file__).parent.parent
    
    # Determine if it's a CID or human_id
    if agent_identifier.startswith('bafy'):
        # It's a CID - load directly
        cid = agent_identifier
        block_path = project_root / "store" / "blocks" / f"{cid}.cbor"
        if not block_path.exists():
            block_path = project_root / "store" / "blocks" / cid
    else:
        # It's a human_id - look up in index first
        human_id = agent_identifier
        index_path = project_root / "store" / "index" / "human_id_to_cid.json"
        
        with open(index_path, 'r') as f:
            index = json.load(f)
        
        if human_id not in index:
            raise ValueError(f"Human ID '{human_id}' not found in index")
        
        cid = index[human_id]
        block_path = project_root / "store" / "blocks" / f"{cid}.cbor"
        if not block_path.exists():
            block_path = project_root / "store" / "blocks" / cid
    
    # Load and decode the block (same as cbor_reader)
    with open(block_path, 'rb') as f:
        cbor_data = f.read()
    
    return dag_cbor.decode(cbor_data)

class MinimalAgentExecutor:
    """
    Minimal executor for AgentNode specifications.
    Loads agent spec, finds implementation, executes function.
    """
    
    def __init__(self, project_root: Path = None):
        """
        Initialize executor with project root.
        
        Args:
            project_root: Path to CADMIES project root (auto-detected if None)
        """
        if project_root is None:
            # Auto-detect project root (assuming this file is in runtime/)
            current_file = Path(__file__).resolve()
            self.project_root = current_file.parent.parent
        else:
            self.project_root = Path(project_root)
        
        self.agents_code_path = self.project_root / "agents" / "code"
        
        print(f"MinimalAgentExecutor initialized")
        print(f"  Project root: {self.project_root}")
        print(f"  Agents code: {self.agents_code_path}")
        
        if not self.agents_code_path.exists():
            print(f"  WARNING: Agents code directory not found: {self.agents_code_path}")
    
    def load_agent_spec(self, agent_identifier: str) -> Dict[str, Any]:
        """
        Load agent specification by CID or human_id.
        
        Args:
            agent_identifier: Either CID string or human_id
            
        Returns:
            Agent specification data
        """
        print(f"Loading agent spec: {agent_identifier}")
        
        # Use our direct loading function
        agent_data = load_agent_spec_direct(agent_identifier)
        
        # Validate this is an AgentNode
        if 'agent_type' not in agent_data:
            print(f"WARNING: Loaded data doesn't have 'agent_type' field")
            print(f"  Type: {agent_data.get('type', 'Unknown')}")
            print(f"  Title: {agent_data.get('title', 'Unknown')}")
        
        return agent_data
    
    def resolve_implementation(self, agent_type: str) -> Any:
        """
        Find and import the implementation module for an agent type.
        
        Args:
            agent_type: Agent type string (e.g., "philosophical_analyzer")
            
        Returns:
            Imported module object
        
        Raises:
            ImportError: If module cannot be found or loaded
        """
        # Map agent_type to module filename
        module_name = agent_type  # e.g., "philosophical_analyzer" -> "philosophical_analyzer.py"
        module_path = self.agents_code_path / f"{module_name}.py"
        
        if not module_path.exists():
            raise FileNotFoundError(
                f"Agent implementation not found: {module_path}\n"
                f"Available modules: {list(self.agents_code_path.glob('*.py'))}"
            )
        
        print(f"Loading implementation: {module_path}")
        
        # Dynamically import the module
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec is None:
            raise ImportError(f"Could not create spec for {module_name}")
        
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        
        try:
            spec.loader.exec_module(module)
        except Exception as e:
            raise ImportError(f"Failed to execute module {module_name}: {e}")
        
        return module
    
    def execute_agent(self, 
                     agent_identifier: str, 
                     input_context: Dict[str, Any] = None,
                     return_raw_result: bool = False) -> Dict[str, Any]:
        """
        Execute an agent by loading its spec and running its implementation.
        
        Args:
            agent_identifier: CID or human_id of agent
            input_context: Optional execution context
            return_raw_result: If True, returns raw function result instead of wrapped
            
        Returns:
            Execution results with metadata
        """
        execution_id = f"exec_{int(1000 * sys.float_info.epsilon)}"
        
        print("=" * 60)
        print(f"AGENT EXECUTION: {execution_id}")
        print("=" * 60)
        
        try:
            # Step 1: Load agent specification
            agent_spec = self.load_agent_spec(agent_identifier)
            
            # Extract key information
            agent_type = agent_spec.get('agent_type')
            execution_spec = agent_spec.get('execution_spec', {})
            entry_point = execution_spec.get('entry_point', '')
            
            if not agent_type:
                raise ValueError("Agent specification missing 'agent_type' field")
            
            if not entry_point:
                raise ValueError("Agent specification missing 'entry_point' in execution_spec")
            
            # Extract function name from entry point signature
            # Format: "function_name(param: type, ...) -> return_type"
            func_name = entry_point.split('(')[0].strip()
            
            print(f"Agent Type: {agent_type}")
            print(f"Entry Point: {entry_point}")
            print(f"Function Name: {func_name}")
            
            # Step 2: Load implementation module
            impl_module = self.resolve_implementation(agent_type)
            
            # Step 3: Get the function
            if not hasattr(impl_module, func_name):
                available_funcs = [attr for attr in dir(impl_module) 
                                 if not attr.startswith('_') and callable(getattr(impl_module, attr))]
                raise AttributeError(
                    f"Function '{func_name}' not found in module {agent_type}.py\n"
                    f"Available functions: {available_funcs}"
                )
            
            target_function = getattr(impl_module, func_name)
            
            # Step 4: Prepare execution context
            if input_context is None:
                input_context = {}
            
            # Get requirements from execution_spec
            requirements = execution_spec.get('requirements', [])
            
            print(f"Requirements: {len(requirements)} CIDs")
            if requirements:
                print(f"  First requirement: {requirements[0][:16]}...")
            
            # Step 5: Execute the function
            print(f"\nEXECUTING: {func_name}(requirements={len(requirements)}, context=...)")
            
            result = target_function(requirements, input_context)
            
            # Step 6: Package results
            execution_result = {
                'execution_id': execution_id,
                'success': True,
                'agent_identifier': agent_identifier,
                'agent_type': agent_type,
                'function_executed': func_name,
                'input_context': input_context,
                'requirements_count': len(requirements),
                'raw_result': result if return_raw_result else None,
                'wrapped_result': self._wrap_result(result) if not return_raw_result else None,
                'metadata': {
                    'executor_version': '1.0.0',
                    'execution_timestamp': self._current_timestamp()
                }
            }
            
            print(f"\nEXECUTION COMPLETE")
            print(f"  Success: {execution_result['success']}")
            print(f"  Requirements processed: {execution_result['requirements_count']}")
            
            return execution_result
            
        except Exception as e:
            error_result = {
                'execution_id': execution_id,
                'success': False,
                'agent_identifier': agent_identifier,
                'error': str(e),
                'error_type': type(e).__name__,
                'metadata': {
                    'executor_version': '1.0.0',
                    'execution_timestamp': self._current_timestamp(),
                    'failed_step': 'See error message'
                }
            }
            
            print(f"\nEXECUTION FAILED")
            print(f"  Error: {e}")
            print(f"  Type: {type(e).__name__}")
            
            return error_result
    
    def _wrap_result(self, raw_result: Any) -> Dict[str, Any]:
        """
        Wrap raw function result in standard format.
        
        Args:
            raw_result: Raw result from agent function
            
        Returns:
            Standardized result dict
        """
        if isinstance(raw_result, dict):
            # Already a dict, ensure it has basic structure
            if 'success' not in raw_result:
                raw_result['success'] = True
            return raw_result
        else:
            # Wrap non-dict results
            return {
                'success': True,
                'raw_data': raw_result,
                'wrapped_at': self._current_timestamp(),
                'data_type': type(raw_result).__name__
            }
    
    def _current_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    
    def test_execution(self, agent_identifier: str = None) -> Dict[str, Any]:
        """
        Test the executor with a known agent.
        
        Args:
            agent_identifier: Optional agent to test (default: philosophical_pattern_finder_v1)
            
        Returns:
            Test results
        """
        print("=" * 60)
        print("MINIMAL AGENT EXECUTOR - SELF TEST")
        print("=" * 60)
        
        if agent_identifier is None:
            agent_identifier = "philosophical_pattern_finder_v1"
        
        test_context = {
            "test_mode": True,
            "analysis_depth": "basic",
            "focus_area": "metaphysics",
            "description": "Minimal executor self-test"
        }
        
        print(f"Testing with agent: {agent_identifier}")
        print(f"Test context: {test_context}")
        
        result = self.execute_agent(agent_identifier, test_context)
        
        print("\n" + "=" * 60)
        print("TEST RESULTS")
        print("=" * 60)
        
        if result['success']:
            print("TEST PASSED")
            print(f"   Execution ID: {result['execution_id']}")
            print(f"   Agent Type: {result['agent_type']}")
            print(f"   Function: {result['function_executed']}")
            print(f"   Requirements: {result['requirements_count']}")
            
            # Show a snippet of the wrapped result
            wrapped = result.get('wrapped_result', {})
            if 'concepts_analyzed' in wrapped:
                print(f"   Concepts Analyzed: {wrapped.get('concepts_analyzed')}")
            if 'connections' in wrapped:
                print(f"   Connections Found: {len(wrapped.get('connections', []))}")
        else:
            print("TEST FAILED")
            print(f"   Error: {result.get('error')}")
            print(f"   Error Type: {result.get('error_type')}")
        
        return result

# Command-line interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Minimal Agent Executor - Execute AgentNode specifications',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('agent', nargs='?', help='Agent CID or human_id to execute')
    parser.add_argument('--test', action='store_true', help='Run self-test')
    parser.add_argument('--context', type=str, help='JSON context string')
    parser.add_argument('--raw', action='store_true', help='Return raw function result')
    
    args = parser.parse_args()
    
    executor = MinimalAgentExecutor()
    
    if args.test:
        # Run self-test
        result = executor.test_execution()
        
    elif args.agent:
        # Execute specific agent
        context = {}
        if args.context:
            try:
                context = json.loads(args.context)
            except json.JSONDecodeError as e:
                print(f"ERROR: Invalid context JSON: {e}")
                exit(1)
        
        result = executor.execute_agent(args.agent, context, args.raw)
        
        # Print summary
        print("\n" + "=" * 60)
        print("EXECUTION SUMMARY")
        print("=" * 60)
        print(f"Agent: {args.agent}")
        print(f"Success: {result['success']}")
        
        if result['success']:
            wrapped = result.get('wrapped_result', {})
            if wrapped and 'concepts_analyzed' in wrapped:
                print(f"Concepts Analyzed: {wrapped['concepts_analyzed']}")
            if wrapped and 'connections' in wrapped:
                print(f"Connections Found: {len(wrapped['connections'])}")
            
            # Save full result
            import time
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            output_file = f"execution_result_{timestamp}.json"
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"Full results saved to: {output_file}")
        else:
            print(f"Error: {result.get('error')}")
        
    else:
        # No arguments - show help and test
        parser.print_help()
        print("\n" + "=" * 60)
        print("QUICK TEST MODE (no agent specified)")
        print("=" * 60)
        
        test_agent = "philosophical_pattern_finder_v1"
        print(f"Running quick test with: {test_agent}")
        
        test_result = executor.test_execution(test_agent)
        
        if test_result['success']:
            print("\nExecutor is operational and ready")
        else:
            print("\nExecutor test failed - check implementation")
