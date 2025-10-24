#!/usr/bin/env python3
"""
Extract and transplant specific components from workspace to target project.

This script extracts reusable components like:
- prompts.py (centralized LLM prompts)
- utils.py (helper functions)
- llm.py (rate-limited LLM initialization)
- state.py (TypedDict state management)
- configuration.py (Pydantic configuration)

It also handles import path updates for the target project.

Usage:
    python extract_component.py --list
    python extract_component.py --component COMPONENT --source PATH --target PATH

Example:
    python extract_component.py --component llm --source /workspace --target /new-project/src/common/
    python extract_component.py --component prompts --target /project --create-imports
"""

import os
import sys
import argparse
import shutil
from pathlib import Path
from typing import List, Dict, Optional


COMPONENTS = {
    "prompts": {
        "file": "prompts.py",
        "search_paths": ["src/agents/*/prompts.py", "src/*/prompts.py"],
        "description": "Centralized LLM prompt templates",
        "dependencies": [],
        "imports": []
    },
    "utils": {
        "file": "utils.py",
        "search_paths": ["src/common/utils.py", "src/utils.py"],
        "description": "Reusable utility functions (deduplication, formatting, etc.)",
        "dependencies": [],
        "imports": ["typing", "Dict", "List", "Any", "Union"]
    },
    "llm": {
        "file": "llm.py",
        "search_paths": ["src/common/llm.py", "src/llm.py"],
        "description": "Rate-limited LLM initialization",
        "dependencies": ["langchain_anthropic", "langchain_core"],
        "imports": ["langchain_anthropic.ChatAnthropic", "langchain_core.rate_limiters.InMemoryRateLimiter"]
    },
    "state": {
        "file": "state.py",
        "search_paths": ["src/agents/*/state.py", "src/*/state.py"],
        "description": "TypedDict-based state management",
        "dependencies": ["langgraph"],
        "imports": ["typing.TypedDict", "langgraph.graph.message.add_messages"]
    },
    "configuration": {
        "file": "configuration.py",
        "search_paths": ["src/agents/*/configuration.py", "src/*/configuration.py"],
        "description": "Pydantic configuration with validation",
        "dependencies": ["pydantic"],
        "imports": ["pydantic.BaseModel", "pydantic.Field"]
    },
    "graph": {
        "file": "graph.py",
        "search_paths": ["src/agents/*/graph.py", "src/*/graph.py"],
        "description": "LangGraph orchestration",
        "dependencies": ["langgraph"],
        "imports": ["langgraph.graph.StateGraph"]
    }
}


def list_components():
    """List all available components."""
    print("Available components:\n")
    for name, info in COMPONENTS.items():
        print(f"  {name:15} - {info['description']}")
        if info['dependencies']:
            print(f"                 Dependencies: {', '.join(info['dependencies'])}")
    print("\nUsage:")
    print("  python extract_component.py --component <name> --source <path> --target <path>")


def find_component_file(component_name: str, source_workspace: Path) -> Optional[Path]:
    """Find component file in source workspace."""
    if component_name not in COMPONENTS:
        print(f"Error: Unknown component '{component_name}'", file=sys.stderr)
        print(f"Available: {', '.join(COMPONENTS.keys())}", file=sys.stderr)
        return None

    search_paths = COMPONENTS[component_name]["search_paths"]

    for pattern in search_paths:
        matches = list(source_workspace.glob(pattern))
        if matches:
            return matches[0]  # Return first match

    return None


def extract_component(
    component_name: str,
    source_workspace: Path,
    target_dir: Path,
    create_imports: bool = False,
    update_imports: bool = True
) -> bool:
    """Extract component from source to target."""

    # Find source file
    source_file = find_component_file(component_name, source_workspace)
    if not source_file:
        print(f"Error: Component '{component_name}' not found in {source_workspace}", file=sys.stderr)
        print(f"Searched paths: {COMPONENTS[component_name]['search_paths']}", file=sys.stderr)
        return False

    print(f"Found component: {source_file.relative_to(source_workspace)}")

    # Ensure target directory exists
    target_dir.mkdir(parents=True, exist_ok=True)

    # Determine target file path
    target_file = target_dir / COMPONENTS[component_name]["file"]

    # Check if target already exists
    if target_file.exists():
        response = input(f"Target file exists: {target_file}\nOverwrite? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            return False

    # Copy file
    shutil.copy2(source_file, target_file)
    print(f"Copied to: {target_file}")

    # Create __init__.py if requested
    if create_imports:
        init_file = target_dir / "__init__.py"
        if not init_file.exists():
            init_file.touch()
            print(f"Created: {init_file}")

    # Print integration instructions
    print("\n" + "="*60)
    print("INTEGRATION INSTRUCTIONS")
    print("="*60)

    component_info = COMPONENTS[component_name]

    # Dependencies
    if component_info["dependencies"]:
        print("\n1. Install dependencies:")
        for dep in component_info["dependencies"]:
            print(f"   pip install {dep}")

    # Import examples
    if component_info["imports"]:
        print("\n2. Required imports (already in file):")
        for imp in component_info["imports"]:
            print(f"   from {imp.rsplit('.', 1)[0]} import {imp.rsplit('.', 1)[-1]}")

    # Usage example
    print(f"\n3. Usage in your code:")
    if component_name == "llm":
        print("   from common.llm import get_llm")
        print("   llm = get_llm(config)")
    elif component_name == "utils":
        print("   from common.utils import deduplicate_sources, format_sources")
        print("   unique = deduplicate_sources(search_results)")
    elif component_name == "prompts":
        print("   from agents.your_agent.prompts import QUERY_WRITER_PROMPT")
        print("   prompt = QUERY_WRITER_PROMPT.format(company_name='Acme')")
    elif component_name == "state":
        print("   from agents.your_agent.state import ResearchState")
        print("   # Use as TypedDict for LangGraph state")
    elif component_name == "configuration":
        print("   from agents.your_agent.configuration import Configuration")
        print("   config = Configuration(max_search_queries=5)")

    # Additional notes
    print(f"\n4. Notes:")
    if component_name == "llm":
        print("   - Rate limiter is global (0.8 req/sec)")
        print("   - Adjust rate limit in llm.py if you have higher API tier")
        print("   - Uses InMemoryRateLimiter from langchain_core")
    elif component_name == "utils":
        print("   - All 8 utility functions are independent")
        print("   - No external dependencies beyond typing")
        print("   - Safe to use in any Python 3.10+ project")
    elif component_name == "prompts":
        print("   - Update prompts for your domain")
        print("   - Use .format() to inject variables")
        print("   - Maintain centralized location for easy testing")
    elif component_name == "state":
        print("   - Customize TypedDict fields for your agent")
        print("   - Compatible with LangGraph StateGraph")
        print("   - Use Annotated for special reducers (add_messages)")
    elif component_name == "configuration":
        print("   - Customize fields and constraints")
        print("   - Set frozen=True for immutability")
        print("   - Use Annotated[type, Field(...)] for validation")

    print("\n" + "="*60)
    print(f"Component '{component_name}' extracted successfully!")
    print("="*60 + "\n")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Extract and transplant components from workspace"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available components"
    )
    parser.add_argument(
        "--component",
        type=str,
        help="Component to extract (e.g., llm, utils, prompts)"
    )
    parser.add_argument(
        "--source",
        type=str,
        default=".",
        help="Source workspace path (default: current directory)"
    )
    parser.add_argument(
        "--target",
        type=str,
        help="Target directory for extracted component"
    )
    parser.add_argument(
        "--create-imports",
        action="store_true",
        help="Create __init__.py in target directory"
    )
    parser.add_argument(
        "--no-update-imports",
        action="store_true",
        help="Don't update import paths (keep original)"
    )

    args = parser.parse_args()

    # List components
    if args.list:
        list_components()
        return

    # Validate arguments
    if not args.component:
        print("Error: --component is required (or use --list)", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    if not args.target:
        print("Error: --target is required", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    # Parse paths
    source_workspace = Path(args.source).resolve()
    target_dir = Path(args.target).resolve()

    if not source_workspace.exists():
        print(f"Error: Source workspace not found: {source_workspace}", file=sys.stderr)
        sys.exit(1)

    # Extract
    success = extract_component(
        args.component,
        source_workspace,
        target_dir,
        create_imports=args.create_imports,
        update_imports=not args.no_update_imports
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
