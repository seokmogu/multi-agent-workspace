---
name: agile-jira
description: Jira integration skill for creating Epic/Story/Task tickets via REST API. Reads User Story markdown files and creates Jira tickets directly (no MCP server needed). Supports Epic creation, Story import, task assignment, progress tracking. Use when importing stories to Jira, creating tickets, or tracking sprint progress.
allowed-tools: Write, Read, Bash
version: 1.0.0
---

# Agile Jira (Jira Ticket Creation)

Direct Jira REST API integration for creating and managing tickets from User Story documents.

**No MCP server required** - Uses REST API directly via `scripts/jira-api.js`

## Quick Start

```bash
# 1. Setup (first time only)
# Add to your project's .env file:
JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your_jira_api_token_here
JIRA_PROJECT_KEY=PROJ
# Get API token: https://id.atlassian.com/manage-profile/security/api-tokens

# 2. Import stories to Jira
/skill agile-jira --import docs/stories/

→ Analyzing 3 story files...
→ Creating Epic: OAuth Authentication (PROJ-123)
→ Creating Story: Google OAuth (PROJ-124)
→ Creating Story: GitHub OAuth (PROJ-125)
→ Creating Story: Account Linking (PROJ-126)
✅ Created 4 tickets in Jira
```

## When to Use

Use this skill when:
- **Importing User Stories to Jira** after approval
- **Creating Epic structure** in Jira
- **Bulk ticket creation** from markdown files
- **Tracking sprint progress** via Jira API

Skip this skill for:
- Writing PRDs (use agile-product)
- Creating User Stories (use agile-stories)
- Manual single-ticket creation (use Jira UI)

## How It Works

### Path Resolution

**IMPORTANT**: This skill can be installed in different locations. The skill will auto-detect its directory from where SKILL.md is loaded.

Common paths:
- Project: `<project>/.claude/skills/agile-jira`
- Global: `~/.claude/skills/agile-jira`

Replace `$SKILL_DIR` with actual path in commands below.

### Configuration

**Three ways to configure** (in priority order):

#### Option 1: Project .env File (Recommended) ⭐

Add to your project's `.env` file:

```bash
# In project root .env file
# Required:
JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your_jira_api_token_here
JIRA_PROJECT_KEY=PROJ

# Optional (custom field IDs - varies by Jira instance):
# JIRA_EPIC_NAME_FIELD=customfield_10011  # Company-managed only
# JIRA_STORY_POINTS_FIELD=customfield_10016
```

**Why this is best**:
- ✅ Consistent with other API keys (ANTHROPIC_API_KEY, TAVILY_API_KEY, etc.)
- ✅ Already in `.gitignore` (secure by default)
- ✅ Per-project configuration (different Jira per project)
- ✅ Works automatically with skill scripts
- ✅ Auto-detects Team-managed vs Company-managed projects

#### Option 2: Shell Environment Variables

```bash
export JIRA_BASE_URL="https://your-domain.atlassian.net"
export JIRA_EMAIL="your-email@example.com"
export JIRA_API_TOKEN="your-api-token"
export JIRA_PROJECT_KEY="PROJ"
```

**Use case**: CI/CD environments, temporary overrides

#### Option 3: .jira-config.json

```bash
cd $SKILL_DIR
cp .jira-config.example.json .jira-config.json

# Edit .jira-config.json:
{
  "baseUrl": "https://your-domain.atlassian.net",
  "email": "your-email@example.com",
  "apiToken": "your-token-here",
  "projectKey": "PROJ"
}
```

**Note**: Add `.jira-config.json` to `.gitignore`!
**Use case**: Skill-specific overrides

### Get Jira API Token

1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Give it a name (e.g., "Claude Agile Jira")
4. Copy the token (you won't see it again!)

## Usage

### Import Stories to Jira

```bash
# Import all stories from directory
cd $SKILL_DIR && node scripts/jira-api.js import ../../../docs/stories/

# Or via skill invocation
/skill agile-jira --import docs/stories/
```

**Process**:
1. Reads all `.md` files in `docs/stories/`
2. Extracts: Title, Description, AC, Story Points
3. Creates Epic (if doesn't exist)
4. Creates Story tickets linked to Epic
5. Returns ticket keys (PROJ-124, PROJ-125, etc.)

### Create Single Epic

```bash
cd $SKILL_DIR && node scripts/jira-api.js create-epic \
  --title="OAuth Authentication" \
  --description="Enable users to login with Google and GitHub"
```

### Create Single Story

```bash
cd $SKILL_DIR && node scripts/jira-api.js create-story \
  --epic="KAN-123" \
  --title="Google OAuth Login" \
  --description="As a user, I want to..." \
  --ac="Given...When...Then..." \
  --points=5
```

### Search Issues

```bash
cd $SKILL_DIR && node scripts/jira-api.js search \
  --jql="project = KAN AND status = 'To Do'"
```

### Track Epic Progress

```bash
cd $SKILL_DIR && node scripts/jira-api.js track \
  --epic="KAN-123"
```

**Returns**:
```
Epic: OAuth Authentication (KAN-123)
Status: In Progress (60% complete)

✅ Done (2/3 stories):
- KAN-124: Google OAuth (Done)
- KAN-125: GitHub OAuth (Done)

🚧 In Progress (1/3 stories):
- KAN-126: Account Linking (In Progress)
```

## Story File Format

User story markdown files should follow this format:

```markdown
# User Story: [Title]

**Epic**: [Epic Name]
**PRD**: docs/prd/feature.md

## Story

As a [user]
I want to [action]
So that [benefit]

## Acceptance Criteria

### AC-1: [Title]
**Given** [context]
**When** [action]
**Then** [outcome]

## Story Points

**X points**
```

The import script parses these fields automatically.

## Jira API Operations

### Available via scripts/jira-api.js

All operations use Jira REST API v3:

```bash
# Epic
create-epic --title="..." --description="..."

# Story
create-story --epic=KEY --title="..." --description="..." --ac="..." --points=N

# Task (subtask)
create-task --story=KEY --title="..." --description="..." --assignee=ID

# Search
search --jql="project = PROJ"

# Get issue
get --issue=KEY

# Track progress
track --epic=KEY

# Import from files
import ../../../docs/stories/
```

## Workflow Integration

### Complete Feature Flow

```bash
# 1. Create PRD
/skill agile-product "OAuth authentication"
→ docs/prd/oauth-authentication-2024-10-23.md

# 2. Generate User Stories
/skill agile-stories --prd=docs/prd/oauth-authentication-2024-10-23.md
→ docs/stories/oauth-google.md
→ docs/stories/oauth-github.md
→ docs/stories/account-linking.md

# 3. Review & Approve (Git PR)
git add docs/
git commit -m "Add OAuth PRD and stories"
gh pr create

# 4. Import to Jira
/skill agile-jira --import docs/stories/
→ KAN-123 (Epic)
→ KAN-124, 125, 126 (Stories)

# 5. Sprint Planning in Jira UI
# 6. Development starts
# 7. Track progress
/skill agile-jira --track KAN-123
```

## API Reference

For complete Jira REST API documentation, see:
- `references/jira-api-reference.md` - Full API docs
- Jira Official: https://developer.atlassian.com/cloud/jira/platform/rest/v3/

## Troubleshooting

### "Jira configuration not found"

**Solution**: Set environment variables or create `.jira-config.json`

```bash
# Check if config exists
ls .claude/skills/agile-jira/.jira-config.json

# Or check environment
echo $JIRA_BASE_URL
```

### "Authentication failed (401)"

**Solution**:
1. Verify API token is correct
2. Regenerate token if needed
3. Check email matches Atlassian account

### "Cannot create Epic (404)"

**Solution**:
1. Verify project key is correct
2. Check project has Epic issue type enabled
3. Verify you have permission to create Epics

### "Custom field not found"

**Solution**:
Custom field IDs vary by Jira instance. Find your field IDs:

```bash
# Get all fields
curl -u email:token \
  https://your-domain.atlassian.net/rest/api/3/field \
  | grep -i "epic\|story point"

# Example output:
# "customfield_10011": "Epic Name"
# "customfield_10016": "Story Points"
```

Then set in your `.env` file:

```bash
JIRA_EPIC_NAME_FIELD=customfield_10011
JIRA_STORY_POINTS_FIELD=customfield_10016
```

**Note**: Team-managed projects don't require Epic Name field. The script auto-detects and retries without it.

## Security Best Practices

1. **Never commit API tokens** to git
2. **Add .jira-config.json to .gitignore**
3. **Use environment variables** for CI/CD
4. **Rotate tokens** quarterly
5. **Use separate tokens** for different projects/users

## Advanced

### Bulk Import

```bash
# Import multiple story directories
cd $SKILL_DIR && node scripts/jira-api.js import \
  ../../../docs/stories/oauth/ \
  ../../../docs/stories/search/ \
  ../../../docs/stories/dashboard/
```

### Custom Field Mapping

Edit `scripts/jira-api.js` to customize field mapping:

```javascript
// Map story points to your custom field ID
const STORY_POINTS_FIELD = 'customfield_10016'; // Update this

// Map epic name field
const EPIC_NAME_FIELD = 'customfield_10011'; // Update this
```

### JQL Templates

Common JQL queries:

```bash
# My open issues
--jql="assignee = currentUser() AND status != Done"

# Stories in current sprint
--jql="project = KAN AND issuetype = Story AND sprint in openSprints()"

# High priority bugs
--jql="project = KAN AND issuetype = Bug AND priority = High"
```

## Tips

1. **Review Before Import** - Always review story files before importing
2. **Use Git PRs** - Get team approval before creating Jira tickets
3. **Track in Docs** - Keep story files in git even after Jira import
4. **Batch Operations** - Import multiple stories at once
5. **Version Control** - Story files show evolution over time

---

**Ready to import your stories to Jira!**

Setup: Add Jira config to `.env` file (see Configuration section above)

Import: `/skill agile-jira --import docs/stories/`
