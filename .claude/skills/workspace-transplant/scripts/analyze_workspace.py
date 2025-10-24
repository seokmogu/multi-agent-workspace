#!/usr/bin/env python3
"""
Analyze workspace structure and identify reusable patterns.

This script scans a multi-agent workspace to identify:
- Directory structure
- Core architecture patterns (6 patterns)
- Reusable components
- Dependencies
- Migration opportunities

Usage:
    python analyze_workspace.py [--workspace PATH] [--output FILE]

Example:
    python analyze_workspace.py --workspace /path/to/project --output analysis.md
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Set, Any
from collections import defaultdict


# Pattern signatures to detect
PATTERN_SIGNATURES = {
    "prompts_centralization": {
        "files": ["prompts.py"],
        "indicators": ["PROMPT", "_PROMPT", "template"],
        "description": "Centralized LLM prompt templates"
    },
    "rate_limiting": {
        "files": ["llm.py"],
        "indicators": ["RateLimiter", "rate_limiter", "requests_per_second"],
        "description": "API rate limiting implementation"
    },
    "state_management": {
        "files": ["state.py"],
        "indicators": ["TypedDict", "State", "ResearchState"],
        "description": "TypedDict-based state management"
    },
    "pydantic_config": {
        "files": ["configuration.py", "config.py"],
        "indicators": ["BaseModel", "Field", "Annotated"],
        "description": "Pydantic configuration with validation"
    },
    "utils_module": {
        "files": ["utils.py"],
        "indicators": ["deduplicate", "format", "calculate"],
        "description": "Reusable utility functions"
    },
    "multi_agent": {
        "files": ["graph.py"],
        "indicators": ["StateGraph", "add_node", "add_edge"],
        "description": "Multi-agent orchestration with LangGraph"
    }
}

COMPONENT_TYPES = {
    "agents": ["research", "extraction", "reflection", "coordinator"],
    "common": ["utils", "llm", "prompts", "state", "configuration"],
    "a2a": ["app.py", "agent.json", "Dockerfile"],
    "examples": ["basic_", "custom_", "streaming_"],
}


def find_python_files(workspace: Path) -> List[Path]:
    """Find all Python files in workspace."""
    return list(workspace.rglob("*.py"))


def find_imports(file_path: Path) -> Set[str]:
    """Extract imports from a Python file."""
    imports = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('import '):
                    imports.add(line.split()[1].split('.')[0])
                elif line.startswith('from '):
                    parts = line.split()
                    if len(parts) >= 2:
                        imports.add(parts[1].split('.')[0])
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}")
    return imports


def detect_pattern(file_path: Path, pattern_name: str, pattern_def: Dict) -> bool:
    """Detect if a pattern exists in a file."""
    # Check filename match
    if any(pf in file_path.name for pf in pattern_def["files"]):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Check for indicators
                if any(indicator in content for indicator in pattern_def["indicators"]):
                    return True
        except Exception:
            pass
    return False


def analyze_directory_structure(workspace: Path) -> Dict[str, Any]:
    """Analyze directory structure."""
    structure = {
        "root": str(workspace),
        "directories": [],
        "key_files": []
    }

    # Find key directories
    for item in workspace.rglob("*"):
        if item.is_dir():
            rel_path = item.relative_to(workspace)
            if not any(part.startswith('.') for part in rel_path.parts):
                structure["directories"].append(str(rel_path))

    # Find key files
    key_patterns = ["*.py", "*.md", "*.yml", "*.yaml", "Dockerfile", "requirements.txt"]
    for pattern in key_patterns:
        for item in workspace.rglob(pattern):
            rel_path = item.relative_to(workspace)
            if not any(part.startswith('.') for part in rel_path.parts):
                structure["key_files"].append(str(rel_path))

    structure["directories"].sort()
    structure["key_files"].sort()

    return structure


def detect_patterns(workspace: Path) -> Dict[str, Any]:
    """Detect architecture patterns in workspace."""
    python_files = find_python_files(workspace)

    detected = {}
    for pattern_name, pattern_def in PATTERN_SIGNATURES.items():
        detected[pattern_name] = {
            "present": False,
            "files": [],
            "description": pattern_def["description"]
        }

        for py_file in python_files:
            if detect_pattern(py_file, pattern_name, pattern_def):
                detected[pattern_name]["present"] = True
                detected[pattern_name]["files"].append(
                    str(py_file.relative_to(workspace))
                )

    return detected


def identify_components(workspace: Path) -> Dict[str, List[str]]:
    """Identify reusable components."""
    components = defaultdict(list)

    for category, patterns in COMPONENT_TYPES.items():
        for pattern in patterns:
            # Find files matching pattern
            if pattern.endswith("_"):
                # Prefix match (e.g., "basic_")
                for file_path in workspace.rglob(f"{pattern}*.py"):
                    rel_path = str(file_path.relative_to(workspace))
                    components[category].append(rel_path)
            else:
                # Exact match (e.g., "utils.py")
                for file_path in workspace.rglob(f"*{pattern}*"):
                    if file_path.is_file():
                        rel_path = str(file_path.relative_to(workspace))
                        components[category].append(rel_path)

    return dict(components)


def analyze_dependencies(workspace: Path) -> Dict[str, Set[str]]:
    """Analyze external dependencies."""
    all_imports = set()
    python_files = find_python_files(workspace)

    for py_file in python_files:
        imports = find_imports(py_file)
        all_imports.update(imports)

    # Filter to known external packages
    external_packages = {
        pkg for pkg in all_imports
        if pkg in ['langchain', 'langchain_anthropic', 'langchain_core',
                   'langgraph', 'anthropic', 'pydantic', 'fastapi',
                   'uvicorn', 'requests', 'tavily', 'google']
    }

    return {
        "external": sorted(list(external_packages)),
        "total_unique_imports": len(all_imports)
    }


def generate_report(workspace: Path, analysis: Dict[str, Any], output_file: str = None):
    """Generate analysis report in Markdown format."""
    report = []

    report.append("# Workspace Analysis Report\n")
    report.append(f"**Workspace**: `{workspace}`\n")
    report.append(f"**Generated**: {Path.cwd()}\n\n")

    # Summary
    report.append("## Summary\n")
    patterns_detected = sum(1 for p in analysis["patterns"].values() if p["present"])
    report.append(f"- **Patterns Detected**: {patterns_detected}/6\n")
    report.append(f"- **Components Found**: {sum(len(v) for v in analysis['components'].values())}\n")
    report.append(f"- **External Dependencies**: {len(analysis['dependencies']['external'])}\n")
    report.append(f"- **Total Directories**: {len(analysis['structure']['directories'])}\n")
    report.append(f"- **Total Key Files**: {len(analysis['structure']['key_files'])}\n\n")

    # Patterns
    report.append("## Detected Patterns\n")
    for name, info in analysis["patterns"].items():
        status = "✅" if info["present"] else "❌"
        report.append(f"### {status} {name.replace('_', ' ').title()}\n")
        report.append(f"**Description**: {info['description']}\n\n")
        if info["present"]:
            report.append("**Found in**:\n")
            for file_path in info["files"]:
                report.append(f"- `{file_path}`\n")
        report.append("\n")

    # Components
    report.append("## Reusable Components\n")
    for category, files in analysis["components"].items():
        if files:
            report.append(f"### {category.title()}\n")
            for file_path in sorted(files):
                report.append(f"- `{file_path}`\n")
            report.append("\n")

    # Dependencies
    report.append("## Dependencies\n")
    report.append(f"**Total unique imports**: {analysis['dependencies']['total_unique_imports']}\n\n")
    report.append("**External packages**:\n")
    for pkg in analysis["dependencies"]["external"]:
        report.append(f"- `{pkg}`\n")
    report.append("\n")

    # Directory Structure
    report.append("## Directory Structure\n")
    report.append("```\n")
    for dir_path in analysis["structure"]["directories"][:20]:  # Limit to 20
        depth = len(Path(dir_path).parts)
        indent = "  " * (depth - 1)
        name = Path(dir_path).name
        report.append(f"{indent}├── {name}/\n")
    if len(analysis["structure"]["directories"]) > 20:
        report.append("  ... (truncated)\n")
    report.append("```\n\n")

    # Recommendations
    report.append("## Recommendations\n")
    if patterns_detected >= 4:
        report.append("✅ **Strong foundation**: This workspace has {patterns_detected}/6 core patterns. ")
        report.append("Excellent candidate for transplantation.\n\n")
    else:
        report.append(f"⚠️ **Limited patterns**: Only {patterns_detected}/6 patterns detected. ")
        report.append("Consider implementing missing patterns before transplantation.\n\n")

    # A2A Migration
    has_a2a = "a2a" in analysis["components"] and len(analysis["components"]["a2a"]) > 0
    if has_a2a:
        report.append("✅ **A2A Ready**: A2A agent structure detected. Ready for distributed deployment.\n\n")
    else:
        report.append("💡 **A2A Opportunity**: Consider migrating to A2A for 480x performance improvement.\n\n")

    # Generate output
    report_text = "".join(report)

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_text)
        print(f"Report written to: {output_file}")
    else:
        print(report_text)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze workspace structure and identify reusable patterns"
    )
    parser.add_argument(
        "--workspace",
        type=str,
        default=".",
        help="Path to workspace directory (default: current directory)"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file for report (default: print to stdout)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON instead of Markdown report"
    )

    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()

    if not workspace.exists():
        print(f"Error: Workspace not found: {workspace}", file=sys.stderr)
        sys.exit(1)

    print(f"Analyzing workspace: {workspace}")

    # Run analysis
    analysis = {
        "structure": analyze_directory_structure(workspace),
        "patterns": detect_patterns(workspace),
        "components": identify_components(workspace),
        "dependencies": analyze_dependencies(workspace)
    }

    # Generate output
    if args.json:
        output = json.dumps(analysis, indent=2, default=str)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"JSON written to: {args.output}")
        else:
            print(output)
    else:
        generate_report(workspace, analysis, args.output)


if __name__ == "__main__":
    main()
