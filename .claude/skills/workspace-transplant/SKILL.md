---
name: Workspace Transplant
description: Analyze multi-agent workspace architecture and transplant reusable patterns, components, and best practices to other projects. Specializes in LangGraph agents, A2A protocol migration, prompt centralization, rate limiting, and distributed system design. Use this when migrating multi-agent architectures, extracting reusable components, or planning A2A system transitions.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Workspace Transplant

Analyze and transplant multi-agent workspace architecture patterns to other projects, enabling reuse of battle-tested components and design patterns.

## When to Use This Skill

Use this skill when:
- Setting up a new multi-agent project based on proven patterns
- Migrating existing monolithic systems to multi-agent architecture
- Extracting specific components (prompts, utils, rate limiting, state management)
- Planning LangGraph → A2A (Agent2Agent) architecture migration
- Implementing cost optimization strategies (up to 91% reduction)
- Understanding and replicating successful agent design patterns

## Core Capabilities

### 1. Workspace Analysis
Automatically analyze workspace structure to identify:
- **6 Core Patterns**: Prompt centralization, rate limiting, state management, Pydantic configuration, TypedDict states, multi-agent orchestration
- **Reusable Components**: utils.py (8 functions), llm.py (rate limiting), prompts.py (templating)
- **Architecture Decisions**: LangGraph graph structure, agent phases, A2A migration path
- **Dependencies**: External libraries, internal module relationships

### 2. Component Extraction
Extract and transplant specific components:
- **Prompts Module**: Centralized LLM prompt templates with variable formatting
- **Utils Module**: 8 reusable functions (deduplication, formatting, completeness calculation)
- **LLM Module**: Rate-limited LLM initialization with task-specific optimization
- **State Module**: TypedDict-based state management for LangGraph
- **Configuration**: Pydantic-based type-safe configuration with validation

### 3. Agent Scaffolding
Generate new agents from templates:
- **LangGraph Agent**: 3-phase structure (research → extract → reflect)
- **A2A Agent**: FastAPI-based independent agent with Agent Card
- **Hybrid Setup**: Gradual migration wrapper for existing agents

### 4. Migration Strategies
Step-by-step migration guidance:
- **LangGraph → A2A**: Convert monolithic agents to distributed HTTP services
- **Cost Optimization**: Implement Fargate Spot + Lambda strategies (91% cost reduction)
- **Performance Scaling**: 480-1000x improvement (12 hours → 90 seconds for 1,000 items)

## Architecture Patterns Reference

The skill provides detailed guidance on these patterns:

### Pattern 1: Prompt Centralization
**File**: `prompts.py`
**Purpose**: Maintain all LLM prompts in a single module
**Benefits**:
- Easy version control and testing
- Consistent formatting with variables ({company_name}, {schema})
- Single source of truth for prompt templates

**When to use**: Any project using multiple LLM calls with repeated prompt structures.

**Implementation**: See `references/architecture_patterns.md` for detailed examples.

### Pattern 2: Rate Limiting
**File**: `llm.py`
**Purpose**: Prevent API throttling with InMemoryRateLimiter
**Configuration**:
- 0.8 requests/second (~50 requests/min)
- Task-specific temperature (research: 0.7, extraction: 0.3, reflection: 0.5)

**When to use**: Production systems with LLM API calls subject to rate limits.

**Implementation**: See `references/architecture_patterns.md` for setup.

### Pattern 3: State Management
**File**: `state.py`
**Purpose**: Type-safe state tracking with TypedDict for LangGraph
**Structure**: Input → Research → Extraction → Reflection → Output

**When to use**: Multi-phase workflows requiring state persistence.

**Implementation**: See `assets/templates/langgraph_agent/state.py`.

### Pattern 4: Pydantic Configuration
**File**: `configuration.py`
**Purpose**: Type-safe, validated, documented configuration
**Features**: Annotated types, constraints (ge, le), immutability (frozen=True)

**When to use**: Any project requiring robust configuration management.

**Implementation**: See `assets/templates/langgraph_agent/configuration.py`.

### Pattern 5: Utils Module
**File**: `utils.py`
**Purpose**: Reusable helper functions shared across agents
**Functions**:
- `deduplicate_sources()`: Remove duplicate URLs from search results
- `format_sources()`: Format with token limits (prevents overflow)
- `calculate_completeness()`: Score extraction completeness
- `truncate_text()`: Safe text truncation
- And 4 more utility functions

**When to use**: Projects with common data processing needs.

**Implementation**: See `assets/templates/utils/utils.py`.

### Pattern 6: Multi-Agent Architecture
**Structure**: 3-phase iterative loop
1. **Research**: Query generation → Web search → Note-taking
2. **Extraction**: Parse notes → JSON extraction → Validation
3. **Reflection**: Completeness check → Gap analysis → Follow-up queries

**When to use**: Complex research or data extraction tasks requiring quality assurance.

**Implementation**: See `references/architecture_patterns.md` for full workflow.

## Usage Workflows

### Workflow 1: Analyze Current Workspace

To understand the workspace structure and identify patterns:

1. Run the analysis script:
   ```bash
   python .claude/skills/workspace-transplant/scripts/analyze_workspace.py
   ```

2. Review the generated report:
   - Directory structure
   - Identified patterns (which of the 6 core patterns are present)
   - Reusable components
   - Dependencies mapping

3. Consult reference documentation:
   - Read `references/architecture_patterns.md` for pattern details
   - Check `references/component_catalog.md` for component usage

### Workflow 2: Extract Specific Component

To extract a component (e.g., rate limiting) to another project:

1. Identify the component:
   ```bash
   python .claude/skills/workspace-transplant/scripts/extract_component.py --list
   ```

2. Extract to target project:
   ```bash
   python .claude/skills/workspace-transplant/scripts/extract_component.py \
     --component llm \
     --source /path/to/workspace \
     --target /path/to/new-project
   ```

3. Follow integration instructions provided by the script.

### Workflow 3: Scaffold New Agent

To create a new agent from templates:

1. Choose template type (langgraph or a2a):
   ```bash
   python .claude/skills/workspace-transplant/scripts/scaffold_agent.py \
     --type langgraph \
     --name my_agent \
     --output /path/to/project/src/agents/
   ```

2. Review generated files:
   - `state.py`: State definition
   - `configuration.py`: Agent configuration
   - `prompts.py`: Prompt templates
   - `graph.py`: LangGraph orchestration

3. Customize for your use case (add domain-specific logic).

### Workflow 4: Plan A2A Migration

To plan migration from LangGraph monolith to A2A distributed system:

1. Read migration strategies:
   - Open `references/migration_strategies.md`
   - Understand the 4-phase migration plan

2. Generate A2A agent templates:
   ```bash
   python .claude/skills/workspace-transplant/scripts/scaffold_agent.py \
     --type a2a \
     --name research_agent \
     --output /path/to/project/src/agents/a2a/
   ```

3. Follow step-by-step guidance:
   - Phase 1: Hybrid wrapper (2 weeks)
   - Phase 2: Infrastructure setup (2 weeks)
   - Phase 3: Performance optimization (2 weeks)
   - Phase 4: Production deployment (1 week)

4. Review cost optimization:
   - Read `references/project_docs_summary.md` (Cost Optimization section)
   - Implement Fargate Spot + Lambda strategies
   - Expected result: 91% cost reduction ($5,222 → $464/month)

## Bundled Resources

### Scripts (`scripts/`)
- **`analyze_workspace.py`**: Automated workspace analysis
- **`extract_component.py`**: Component extraction and transplantation
- **`scaffold_agent.py`**: Agent scaffolding from templates

### References (`references/`)
- **`architecture_patterns.md`**: Detailed pattern explanations with code examples
- **`migration_strategies.md`**: Step-by-step LangGraph → A2A migration guide
- **`component_catalog.md`**: Complete catalog of reusable components
- **`project_docs_summary.md`**: Key insights from CLAUDE.md and architecture docs

### Assets (`assets/templates/`)
- **`langgraph_agent/`**: Complete LangGraph agent template
- **`a2a_agent/`**: A2A protocol agent with FastAPI
- **`utils/`**: Reusable utility modules

## Key Decisions and Trade-offs

### When to Use LangGraph vs A2A?

**Use LangGraph (Monolith)** when:
- Processing < 100 items at a time
- Rapid prototyping phase
- Team unfamiliar with distributed systems
- Simple, sequential workflows

**Use A2A (Distributed)** when:
- Batch processing 1,000+ items
- Need 480-1000x performance improvement
- Independent agent scaling required
- Production system with high availability needs

### Cost Optimization Strategies

The workspace implements multiple cost reduction techniques:

1. **Fargate Spot Instances**: 70% discount vs on-demand
2. **Lambda for Reflection**: Pay-per-execution for infrequent tasks
3. **Aurora Serverless v2**: Auto-scaling database (0.5 → 2 ACUs)
4. **VPC Endpoints**: Eliminate NAT Gateway costs ($32/month → $0)
5. **Caching Strategy**: 90% cache hit rate reduces API calls

**Result**: $5,222/month → $464/month (91% reduction)

See `references/project_docs_summary.md` for detailed breakdown.

## Migration Path: v2.0 (LangGraph) → v3.0 (A2A)

The workspace has a proven migration strategy:

### Current State: v2.0 (LangGraph Monolith)
- Single Python process
- In-memory state
- Sequential processing (45-90 sec/item)
- 1,920 items/day capacity

### Target State: v3.0 (A2A Distributed)
- Independent HTTP agents
- Database-backed state
- Parallel processing (90 sec/1,000 items)
- Unlimited horizontal scaling

### Migration Strategy
1. **Hybrid Wrapper** (Week 1-2): Wrap existing code with A2A interfaces
2. **Infrastructure** (Week 3-4): Deploy to AWS (ECS, Aurora, Redis)
3. **Optimization** (Week 5-6): Performance tuning and caching
4. **Production** (Week 7): Blue-green deployment

**Timeline**: 7 weeks
**ROI**: 480x faster, 91% cheaper

## Best Practices

### 1. Start with Analysis
Always run `analyze_workspace.py` first to understand what patterns exist and what can be reused.

### 2. Extract Before Creating
Check if a component already exists before writing new code. Use `extract_component.py` to reuse battle-tested implementations.

### 3. Test Templates
Generated agent templates are starting points. Customize prompts, state, and configuration for your domain.

### 4. Gradual Migration
For A2A migration, use the hybrid wrapper approach to minimize risk. Keep v2.0 running while gradually shifting traffic to v3.0.

### 5. Monitor Costs
When implementing cost optimizations, track metrics:
- API calls per hour
- Average response time
- Cache hit rate
- Monthly AWS bill

## Examples

### Example 1: New Project with Multi-Agent Architecture

**Scenario**: Starting a new document processing project, want to use proven agent patterns.

**Steps**:
1. Analyze workspace: `python scripts/analyze_workspace.py`
2. Scaffold agent: `python scripts/scaffold_agent.py --type langgraph --name document_agent`
3. Review patterns: Read `references/architecture_patterns.md`
4. Customize templates: Modify prompts.py for document-specific queries
5. Test locally: Run basic research workflow

**Time**: 1-2 hours
**Result**: Production-ready agent structure with rate limiting, prompts, and state management.

### Example 2: Extract Rate Limiting Pattern

**Scenario**: Existing project hitting API rate limits, need robust rate limiting.

**Steps**:
1. Extract LLM module: `python scripts/extract_component.py --component llm --target /path/to/project`
2. Review implementation: Check generated llm.py
3. Install dependency: `pip install langchain-anthropic`
4. Update imports: Replace existing LLM initialization with `from common.llm import get_llm`
5. Test: Verify rate limiting prevents throttling

**Time**: 30 minutes
**Result**: API-compliant rate limiting (0.8 req/sec) with task-specific LLM configuration.

### Example 3: Plan A2A Migration

**Scenario**: Current system processes 100 companies in 90 minutes, need to scale to 1,000.

**Steps**:
1. Read migration guide: Open `references/migration_strategies.md`
2. Understand current bottleneck: Sequential processing in LangGraph
3. Review A2A architecture: Check `references/project_docs_summary.md` (A2A section)
4. Generate templates: Scaffold A2A agents for research, extraction, reflection
5. Plan infrastructure: Review Terraform code in docs
6. Estimate costs: Use cost calculator from docs ($464/month for 50 items/hour)
7. Create timeline: 7-week migration plan

**Time**: 2-3 hours for planning
**Implementation**: 7 weeks
**Result**: 480x faster (90 minutes → 90 seconds for 1,000 items), 91% cost reduction.

## Troubleshooting

### Issue: Script fails with import errors
**Solution**: Ensure you're running scripts from the skill directory, and all dependencies are installed.

### Issue: Generated agent doesn't match my use case
**Solution**: Templates are starting points. Review `references/architecture_patterns.md` to understand the pattern, then customize for your domain.

### Issue: A2A migration seems too complex
**Solution**: Start with hybrid wrapper (Phase 1 only). This adds A2A interfaces without changing existing code, allowing gradual migration.

### Issue: Cost optimization doesn't match projections
**Solution**: Check cache hit rate, API call frequency, and instance types. See detailed cost breakdown in `references/project_docs_summary.md`.

## References

For detailed information, consult:

- **Architecture Patterns**: `references/architecture_patterns.md`
- **Migration Strategies**: `references/migration_strategies.md`
- **Component Catalog**: `references/component_catalog.md`
- **Project Insights**: `references/project_docs_summary.md`

## Notes

- This skill extracts patterns from the current workspace. If the workspace changes, re-run analysis.
- Templates are opinionated. Adapt to your project's coding standards.
- A2A migration is a significant undertaking (7 weeks). Ensure alignment with business goals.
- Cost savings assume AWS pricing as of 2025. Verify current rates.

---

**Version**: 1.0.0
**Last Updated**: 2025-10-24
**Maintained by**: Development Team
