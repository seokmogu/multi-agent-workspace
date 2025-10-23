# Claude Code Skills Collection

Complete collection of skills for this project, following Anthropic's Skill-Creator best practices.

**Last Updated**: 2025-10-23 (v2 - Skill-Creator Optimized)
**Total Skills**: 8 (7 production + 1 reference)
**Recently Updated**: deep-research (v2), database-designer (v2), langgraph-multi-agent (v2)

---

## Production Skills (7)

### 1. 🎯 agile-master
**Path**: `.claude/skills/agile-master/`
**Type**: Project Management & Automation
**Status**: Production (v1)

**What It Does**:
End-to-end agile project management from PRD writing to Jira ticket creation. Interactive workflow for Epic → User Story → Implementation Task → PR → Deployment lifecycle.

**Key Features**:
- Interactive PRD creation (guided Q&A)
- Jira Epic/Story/Task auto-generation
- Acceptance Criteria in Given-When-Then format
- Team member assignment
- Progress tracking

**When to Use**:
- Starting new features or epics
- Sprint planning sessions
- Creating comprehensive Jira workflows

**Integrations**:
- Requires: Jira MCP (`.mcp.json`)
- Works with: GitHub MCP (PR linking)

**Files**:
- SKILL.md (2,803 words)
- README.md, SETUP.md

**Related**: See agile-master-v2 for Skill-Creator optimized version

---

### 2. 🎯 agile-master-v2
**Path**: `.claude/skills/agile-master-v2/`
**Type**: Project Management & Automation
**Status**: Testing (v2 - Skill-Creator Optimized)

**What It Does**:
Same as agile-master v1, but restructured following Skill-Creator progressive disclosure pattern.

**Key Differences from v1**:
- 59% smaller SKILL.md (1,151 vs 2,803 words)
- Detailed guides in `references/` (4,200+ words for PRD, 2,800+ for User Stories)
- Reusable templates in `assets/templates/`
- Progressive disclosure (loads only what's needed)

**Structure**:
```
agile-master-v2/
├── SKILL.md (1,151 words - core overview)
├── references/
│   ├── prd-guide.md (4,200+ words)
│   └── user-story-guide.md (2,800+ words)
└── assets/
    └── templates/
        └── user-story-template.md
```

**Performance**:
- 2.4x more context-efficient for common tasks
- 10x more comprehensive guidance for deep dives

**Recommendation**: Use v2 for production after testing

---

### 3. 📚 agile-docs-framework
**Path**: `.claude/skills/agile-docs-framework/`
**Type**: Documentation Templates & Guidelines
**Status**: Production

**What It Does**:
Comprehensive documentation framework for agile teams. Provides templates, best practices, and structure for PRD, Technical Design, User Stories, Test Plans.

**Key Features**:
- Document hierarchy guidance (PRD → TDD → Story → AC)
- Complete templates for all doc types
- QA integration patterns
- Traceability best practices

**When to Use**:
- Establishing team documentation standards
- Creating new feature documentation
- Onboarding team members to doc practices

**Complements**:
- agile-master (provides the automation)
- agile-docs-framework (provides the guidance)

**Files**:
- SKILL.md (17K - comprehensive guide)

---

### 4. 🔍 deep-research
**Path**: `.claude/skills/deep-research/`
**Type**: AI Research Agent (LangGraph + 8 Web Search APIs)
**Status**: Production (Skill-Creator Optimized)

**What It Does**:
Universal web research engine with LangGraph. Change schema to research any domain: companies, products, people, papers, competitors. Iterative research → extract → reflect loop with quality evaluation.

**Architecture**:
```
Research Phase → Extraction Phase → Reflection Phase
     ↑                                       ↓
     └──────── Loop if incomplete ──────────┘
```

**Key Features**:
- **8 web search APIs** with free tiers (Jina, Serper, Tavily, Exa, Brave, DuckDuckGo, SerpAPI, Bing)
- Custom JSON schema extraction (any domain)
- Iterative quality improvement
- Optimized for private SME research

**When to Use**:
- Company/product/person profiling
- Market research automation
- Competitive analysis
- Academic paper research
- **Any structured web research task**

**Tech Stack**:
- LangGraph (workflow orchestration)
- LangChain Anthropic (Claude integration)
- Multiple search providers (see references/WEB_SEARCH_APIS.md)
- Pydantic (schema validation)

**New Structure (v2)**:
```
deep-research/
├── SKILL.md (346 lines - concise guide)
└── references/
    ├── WEB_SEARCH_APIS.md (8 providers, pricing, LangChain code)
    └── PRIVATE_SME_RESEARCH.md (SME research strategies)
```

**Free Options**:
- DuckDuckGo: Unlimited (slow)
- Jina AI: 200 RPM free
- Serper.dev: 2,500 lifetime free ⭐ Best free production
- Tavily: 1,000/month
- Exa: $10 credit or 1k/month

---

### 5. 🗄️ database-designer
**Path**: `.claude/skills/database-designer/`
**Type**: Database Architecture & Selection
**Status**: Production (Skill-Creator Optimized)

**What It Does**:
Universal database design tool for ANY project. Analyze PRD → Select database → Design schema → Implement. Supports 15+ database options from SaaS to self-hosted.

**Key Features**:
- **15+ database options** with free tier comparison (Supabase, PlanetScale, Neon, Firebase, PostgreSQL, MongoDB, etc.)
- Database selection decision framework
- 10+ common schema design patterns (User Auth, E-commerce, Blog, Multi-tenancy, etc.)
- Migration strategies between databases

**When to Use**:
- Choosing database for new project
- Designing data models from requirements
- Migrating between databases
- Optimizing existing schemas
- Evaluating SaaS vs self-hosted options

**Structure**:
```
database-designer/
├── SKILL.md (concise selection guide)
└── references/
    ├── DATABASE_OPTIONS.md (15 DBs: pricing, pros/cons, setup)
    └── SCHEMA_DESIGN_PATTERNS.md (10 patterns with SQL examples)
```

**Database Options**:
- **SaaS**: Supabase ⭐, PlanetScale, Neon, Firebase, MongoDB Atlas
- **Cloud**: AWS RDS/Aurora, Google Cloud SQL, Azure Database
- **Self-hosted**: PostgreSQL, MySQL, MongoDB, SQLite
- **Special**: Redis (cache), ClickHouse (analytics)

**All with generous free tiers!**

---

### 6. 🤖 langgraph-multi-agent
**Path**: `.claude/skills/langgraph-multi-agent/`
**Type**: Multi-Agent System Architecture
**Status**: Production

**What It Does**:
Framework for building collaborative multi-agent systems with LangGraph. Researcher → Writer → Reviewer sequential workflow with conditional routing.

**Architecture**:
```
Researcher Agent → Writer Agent → Reviewer Agent
                        ↓
                  [Good] → Complete
                  [Needs Revision] → Loop to Writer
```

**Key Features**:
- Multi-agent collaboration patterns
- Conditional routing
- State management across agents
- Sequential workflow orchestration

**When to Use**:
- Document generation workflows
- Report writing with review loops
- Any multi-step AI workflow

**Example Use Case**:
- Research topic → Write report → Review quality → Revise if needed

---

### 7. 🎭 playwright-skill
**Path**: `.claude/skills/playwright-skill/`
**Type**: Browser Automation & Testing
**Status**: Production (v4.0.0)
**Source**: https://github.com/lackeyjb/playwright-skill (Community)

**What It Does**:
Complete browser automation with Playwright. Auto-detects dev servers, writes clean test scripts, executes E2E tests, takes screenshots, validates UX.

**Key Features**:
- **Model-invoked** (Claude decides when to use)
- Auto-detects running localhost servers
- Visible browser by default (easier debugging)
- 7 common patterns (responsive, login, forms, links, screenshots)
- Helper library (`lib/helpers.js`)

**Common Patterns**:
1. Responsive design testing (mobile, tablet, desktop)
2. Login flow automation
3. Form filling & submission
4. Link validation
5. Screenshot capture
6. Visual regression testing
7. Custom automation

**When to Use**:
- Web application E2E testing
- Automated form filling
- Screenshot capture across viewports
- Link checking
- Any browser automation task

**Critical Workflow**:
1. Auto-detect dev servers
2. Write scripts to `/tmp`
3. Use visible browser (headless: false)
4. Execute via `run.js`

**Structure**:
```
playwright-skill/
├── SKILL.md (12.7k - core workflow)
├── run.js (universal executor)
├── lib/helpers.js (utilities)
├── API_REFERENCE.md (15.5k - full Playwright API)
├── package.json
└── ANALYSIS.md (our detailed analysis)
```

**Performance**:
- Simple tests: SKILL.md only (~3.2k tokens)
- Complex: SKILL.md + API_REFERENCE (~7.2k tokens)
- Progressive disclosure for efficiency

**Integration Ideas**:
- Test user stories from agile-master
- Automated QA for feature implementations
- Visual regression in CI/CD

**Setup**:
```bash
cd .claude/skills/playwright-skill
npm run setup  # Installs Playwright + Chromium
```

---

## Reference Skills (1)

### 8. 📖 skill-creator
**Path**: `.claude/skills/skill-creator/`
**Type**: Meta-Skill (Skill Development Guide)
**Status**: Reference (Anthropic Official)
**Source**: https://github.com/anthropics/skills

**What It Does**:
Official Anthropic guide for creating effective skills. Comprehensive framework for skill development following best practices.

**Key Principles**:
1. **Progressive Disclosure** (3-tier loading)
   - Metadata (always)
   - SKILL.md (when triggered)
   - Bundled resources (when needed)

2. **6-Step Creation Process**:
   - Understanding (gather examples)
   - Planning (identify reusable content)
   - Initializing (create structure)
   - Editing (write SKILL.md + resources)
   - Packaging (validate)
   - Iterating (refine)

3. **Bundled Resources**:
   - `scripts/` - Executable code
   - `references/` - Detailed docs (loaded as needed)
   - `assets/` - Templates, files (not loaded to context)

**When to Use**:
- Creating new skills
- Improving existing skills
- Understanding skill architecture
- Following Anthropic best practices

**Files**:
- SKILL.md (209 lines - complete guide)

---

## Skills Summary Table

| Skill | Type | Size | Files | Integrations | Status |
|-------|------|------|-------|--------------|--------|
| **agile-master** | PM/Automation | 2.8k words | 3 | Jira MCP | Production v1 |
| **agile-master-v2** | PM/Automation | 1.1k + refs | 4 | Jira MCP | Testing v2 |
| **agile-docs-framework** | Documentation | 17k | 1 | - | Production |
| **deep-research** | AI Research | 346 lines + refs | 3 | 8 Search APIs, LangGraph | Production v2 |
| **database-designer** | DB Architecture | refs | 3 | 15 Databases | Production v2 |
| **langgraph-multi-agent** | Multi-Agent | 174 lines + refs | 5 | LangGraph | Production v2 |
| **playwright-skill** | Testing | 12.7k + 15.5k ref | 6 | Playwright | Production |
| **skill-creator** | Reference | 209 lines | 1 | - | Reference |

---

## Skill Architecture Patterns

### Pattern 1: Monolithic (Original)

**Example**: agile-master v1

```
skill/
└── SKILL.md (all content in one file)
```

**Pros**: Simple, everything in one place
**Cons**: Large context load, hard to maintain

---

### Pattern 2: Progressive Disclosure (Skill-Creator)

**Example**: agile-master-v2, playwright-skill

```
skill/
├── SKILL.md (lean core)
├── references/ (detailed guides)
├── assets/ (templates)
└── scripts/ (executables)
```

**Pros**: Context-efficient, scalable, maintainable
**Cons**: More complex structure

**Recommendation**: Use for production skills

---

### Pattern 3: Reference-Heavy

**Example**: deep-research

```
skill/
├── SKILL.md (comprehensive guide)
└── [References to src/agents/ implementation]
```

**Pros**: Complete documentation, real code examples
**Cons**: Large SKILL.md

---

## Integration Map

```
┌─────────────────────────────────────────────────────────┐
│                    Development Workflow                  │
└─────────────────────────────────────────────────────────┘

    agile-master
         │
         ├─ Creates PRD
         ├─ Generates User Stories with AC
         └─ Creates Jira Tickets
              │
              ├─ [Developer Implements Feature]
              │
              ├─ playwright-skill
              │    └─ Tests AC automatically
              │
              ├─ [QA Manual Testing]
              │
              └─ [Deploy]

┌─────────────────────────────────────────────────────────┐
│                    Research Workflow                     │
└─────────────────────────────────────────────────────────┘

    deep-research
         │
         ├─ Searches web (8 APIs: Jina, Serper, Tavily, Exa, etc.)
         ├─ Extracts structured data (any domain)
         └─ Reflects on quality
              │
              └─ database-designer
                   └─ Designs DB schema for storing results

┌─────────────────────────────────────────────────────────┐
│                    Documentation Workflow                │
└─────────────────────────────────────────────────────────┘

    agile-docs-framework
         │
         └─ Provides templates & guidance
              │
              └─ agile-master
                   └─ Uses templates to generate docs
```

---

## Quick Start Guide

### Using Agile Master

```bash
# Ensure Jira MCP is configured
ls .mcp.json

# Use the skill
/skill agile-master
"Add OAuth authentication to login page"

# Follow interactive prompts
```

### Using Playwright Skill

```bash
# Setup (first time only)
cd .claude/skills/playwright-skill
npm run setup

# Use the skill (no explicit invocation needed)
"Test if the login form works on localhost:3000"
```

### Using Deep Research

```bash
# Use the skill
/skill deep-research
"Research Anthropic company information"
```

---

## Maintenance

### Adding New Skills

1. Create skill directory in `.claude/skills/`
2. Follow skill-creator pattern (SKILL.md + bundled resources)
3. Document in this collection
4. Test with sample tasks
5. Add to git

### Updating Existing Skills

1. Edit specific files (SKILL.md or references/)
2. Update version in SKILL.md metadata
3. Document changes
4. Test thoroughly
5. Commit to git

### Removing Skills

1. Move to `.claude/skills/archive/`
2. Update this collection document
3. Notify team

---

## Best Practices

### From Official skill-creator

1. **Progressive Disclosure**: Keep SKILL.md <5k words, move details to references/
2. **Bundled Resources**: Use scripts/, references/, assets/ effectively
3. **Clear Workflows**: Provide step-by-step critical workflows
4. **Helper Functions**: Extract common patterns
5. **Path Independence**: Handle multiple installation locations

### From Community (playwright-skill)

6. **Visible by Default**: Easier debugging (headless: false)
7. **Auto-Detection**: Find dev servers automatically
8. **Safe Execution**: Write to /tmp, not project directories
9. **Common Patterns**: Provide 7-10 ready-to-use examples
10. **Complete API Reference**: Separate file, loaded when needed

### From Our Experience

11. **Integration First**: Design skills to work together
12. **Version Control**: Keep skills in git
13. **Documentation**: Comprehensive ANALYSIS.md for complex skills
14. **Testing**: Verify skills work before committing

---

## Resources

### Official

- **Anthropic Skills Repo**: https://github.com/anthropics/skills
- **Claude Code Docs**: https://docs.claude.com/en/docs/claude-code/skills
- **Skill Best Practices**: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices

### Community

- **playwright-skill**: https://github.com/lackeyjb/playwright-skill
- **Awesome Claude Skills**: https://github.com/travisvn/awesome-claude-skills

### Our Documentation

- **Skills Comparison**: `.claude/SKILLS_COMPARISON.md` (Official vs Our)
- **Version Comparison**: `.claude/SKILL_VERSIONS_COMPARISON.md` (v1 vs v2)
- **MCP Setup**: `.claude/MCP_SETUP.md` (Jira integration)

---

## Future Skills to Consider

### High Priority

1. **github-integration-skill** - Auto-create PRs, link to Jira
2. **code-review-skill** - Automated code review with best practices
3. **deployment-automation-skill** - CI/CD workflow automation

### Medium Priority

4. **api-testing-skill** - API endpoint testing (Postman/Insomnia-like)
5. **database-migration-skill** - Schema migration automation
6. **security-audit-skill** - Security vulnerability scanning

### Low Priority

7. **performance-testing-skill** - Load testing, benchmarking
8. **accessibility-testing-skill** - WCAG compliance checking
9. **i18n-management-skill** - Translation and localization

---

**Total Lines of Documentation**: ~100,000+
**Total Functionality**: Project Management + AI Research + Testing + Monitoring + Multi-Agent Systems
**Integration Level**: High (skills work together seamlessly)

**Next Review**: Monthly or when new skills are added
