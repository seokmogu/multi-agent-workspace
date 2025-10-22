# Agile Master Skill

Complete end-to-end agile project management assistant for Claude.

## What It Does

Guides you through the entire agile development lifecycle:

```
Feature Idea → PRD → Jira Epic → User Stories → Tasks → PR → Deployment
```

## Quick Start

### 1. Setup Jira Integration

See [SETUP.md](./SETUP.md) for complete Jira MCP configuration.

Quick version:
```json
{
  "mcpServers": {
    "jira": {
      "command": "npx",
      "args": ["-y", "@orengrinker/jira-mcp-server"],
      "env": {
        "JIRA_BASE_URL": "https://your-company.atlassian.net",
        "JIRA_EMAIL": "your-email@company.com",
        "JIRA_API_TOKEN": "your-api-token"
      }
    }
  }
}
```

### 2. Invoke the Skill

```
/skill agile-master
"I want to add OAuth authentication"
```

### 3. Follow Interactive Prompts

The skill will guide you through:
1. PRD creation
2. Epic creation in Jira
3. User Story breakdown
4. Task generation
5. Team assignment

## Features

- ✅ **Interactive PRD Creation** - Guided questionnaire
- ✅ **Jira Epic Generation** - Automatic Epic ticket creation
- ✅ **Story Breakdown** - Smart feature decomposition
- ✅ **Acceptance Criteria** - Given-When-Then format
- ✅ **Task Assignment** - Auto-assign by role
- ✅ **Progress Tracking** - Monitor ticket status
- ✅ **Document Templates** - PRD, TDD, Test Plans
- ✅ **Team Workflow** - Epic → Story → Task hierarchy

## Use Cases

### New Feature Development
```
"Add two-factor authentication"
→ PRD + Epic + 3 Stories + 12 Tasks
```

### API Changes
```
"Migrate REST API to GraphQL"
→ Migration strategy + phased Stories
```

### Sprint Planning
```
"Plan sprint with Epic PROJ-123"
→ Capacity analysis + Story assignment
```

## What You Get

After running this skill:

1. **Documentation**
   - Comprehensive PRD
   - Technical Design Document
   - Test Plan

2. **Jira Structure**
   - Epic ticket (e.g., PROJ-123)
   - User Story tickets (e.g., PROJ-124, 125, 126)
   - Implementation Tasks (e.g., PROJ-127-140)

3. **Team Alignment**
   - Clear acceptance criteria
   - Assigned tasks
   - Sprint-ready backlog

## Requirements

- Jira Cloud or Server/Data Center
- Jira MCP server configured (see SETUP.md)
- Project key and API token

## Documentation

- [SKILL.md](./SKILL.md) - Complete skill guide
- [SETUP.md](./SETUP.md) - Jira MCP setup instructions
- [README.md](./README.md) - This file

## Examples

### Example 1: Full Feature

```
User: /skill agile-master
      "Add payment processing with Stripe"

AI: [Interactive session]
    ... Q&A for PRD ...

    ✅ PRD Created: docs/prd/payment-processing-2024-10.md
    ✅ Epic Created: PROJ-200
    ✅ Stories Created: 4 stories (22 story points)
    ✅ Tasks Created: 16 tasks assigned to team

    Ready for sprint planning!
```

### Example 2: Progress Tracking

```
User: /skill agile-master
      "Track PROJ-200"

AI: Epic: Payment Processing (PROJ-200)
    Status: In Progress (65% complete)

    ✅ Done: 2/4 stories
    🚧 In Progress: 1/4 stories
    📋 To Do: 1/4 stories

    Recent: PR #123 merged (Stripe integration)
```

## Best Practices

1. **Start with PRD** - Don't skip the "why"
2. **Keep Stories Small** - 1-8 story points
3. **Clear AC** - Testable, specific criteria
4. **Link Everything** - PRD ↔ Epic ↔ Story ↔ Task
5. **Update as You Learn** - PRD is a living document

## Troubleshooting

**Issue**: "Jira MCP not available"
- **Fix**: See SETUP.md for configuration

**Issue**: "Cannot create Epic"
- **Fix**: Check Jira project has Epic issue type enabled

**Issue**: "Story points not showing"
- **Fix**: Configure custom field ID (I'll ask during setup)

## Support

For setup help:
1. Read [SETUP.md](./SETUP.md)
2. Check Jira API token is valid
3. Verify MCP configuration
4. Test with: "Search Jira for issues in PROJ"

## Contributing

Ideas to extend this skill:
- GitHub MCP integration for PR linking
- Slack notifications on ticket updates
- Auto-estimation based on historical data
- Sprint velocity tracking
- Burndown chart generation

## License

This skill is part of the Claude Code skills library.

---

**Ready to transform feature ideas into actionable work!**

Start with: `/skill agile-master "your feature idea"`
