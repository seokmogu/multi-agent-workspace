# Agile Master - Jira MCP Setup Guide

This guide will help you set up the Jira MCP server integration for the Agile Master skill.

## Prerequisites

- Node.js 18+ installed
- Jira Cloud account (or Jira Server/Data Center)
- Admin access to create API tokens

## Option 1: Quick Setup with OrenGrinker's Jira MCP (Recommended)

This is the easiest and most feature-complete option.

### Step 1: Get Jira API Token

1. Go to [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click **"Create API token"**
3. Give it a name (e.g., "Claude Agile Master")
4. Copy the token (you won't see it again!)

### Step 2: Get Your Jira Information

You'll need:
- **JIRA_BASE_URL**: Your Jira URL (e.g., `https://your-company.atlassian.net`)
- **JIRA_EMAIL**: Your Atlassian account email
- **JIRA_API_TOKEN**: The token from Step 1
- **PROJECT_KEY**: Your Jira project key (e.g., "PROJ", "DEV", "TEAM")

### Step 3: Configure MCP Settings

#### For Claude Desktop (Mac)

Edit: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "jira": {
      "command": "npx",
      "args": ["-y", "@orengrinker/jira-mcp-server"],
      "env": {
        "JIRA_BASE_URL": "https://your-company.atlassian.net",
        "JIRA_EMAIL": "your-email@company.com",
        "JIRA_API_TOKEN": "your-api-token-here"
      }
    }
  }
}
```

#### For Claude Desktop (Windows)

Edit: `%APPDATA%\Claude\claude_desktop_config.json`

(Same JSON structure as above)

#### For Claude Desktop (Linux)

Edit: `~/.config/Claude/claude_desktop_config.json`

(Same JSON structure as above)

#### For Claude Code CLI

If using Claude Code CLI, you may need to set up MCP differently. Check your MCP configuration location:

```bash
# Common locations:
~/.config/mcp/mcp_config.json
~/.mcp/config.json
```

Or set environment variables directly:
```bash
export JIRA_BASE_URL="https://your-company.atlassian.net"
export JIRA_EMAIL="your-email@company.com"
export JIRA_API_TOKEN="your-api-token-here"
```

### Step 4: Restart Claude

After editing the config file, restart Claude Desktop or Claude Code for changes to take effect.

### Step 5: Verify Connection

Test the connection:

```
User: "Can you search for Jira issues in project PROJ?"

Claude: [Should be able to connect and search]
```

Or directly test MCP tools are available:
```
User: "List available MCP tools"
Claude: [Should show jira_search_issues, jira_create_issue, etc.]
```

## Option 2: Setup with Cosmix's Jira MCP

This option supports both Jira Cloud and Server/Data Center.

### Step 1: Install with Bun

```bash
# Clone the repository
git clone https://github.com/cosmix/jira-mcp.git
cd jira-mcp

# Install Bun if you don't have it
curl -fsSL https://bun.sh/install | bash

# Install dependencies
bun install

# Build
bun run build
```

### Step 2: Configure MCP Settings

```json
{
  "mcpServers": {
    "jira": {
      "command": "node",
      "args": ["/path/to/jira-mcp/dist/index.js"],
      "env": {
        "JIRA_BASE_URL": "https://your-company.atlassian.net",
        "JIRA_USER_EMAIL": "your-email@company.com",
        "JIRA_API_TOKEN": "your-api-token",
        "JIRA_TYPE": "cloud",
        "JIRA_AUTH_TYPE": "basic"
      }
    }
  }
}
```

**For Jira Server/Data Center:**
```json
{
  "env": {
    "JIRA_BASE_URL": "https://jira.your-company.com",
    "JIRA_USER_EMAIL": "username",
    "JIRA_API_TOKEN": "password-or-pat",
    "JIRA_TYPE": "server",
    "JIRA_AUTH_TYPE": "bearer"
  }
}
```

### Step 3: Restart and Verify

Same as Option 1, Step 4-5.

## Option 3: Official Atlassian Remote MCP

Atlassian offers an official remote MCP server.

**Note**: This is in beta and may have limited features.

Visit: [Atlassian Remote MCP](https://www.atlassian.com/blog/announcements/remote-mcp-server)

Follow official Atlassian instructions for setup.

## Verifying Your Setup

After setup, test these commands:

### Test 1: Search Issues
```
User: "Search for open issues in project PROJ"

Expected: Claude uses jira_search_issues tool and returns results
```

### Test 2: Create Test Issue
```
User: "Create a test task in PROJ with title 'MCP Test'"

Expected: Claude creates a Jira issue and returns the issue key
```

### Test 3: Invoke Agile Master
```
User: /skill agile-master
      "Test setup"

Expected: Skill loads and confirms Jira connection
```

## Troubleshooting

### Issue: "Jira MCP not available"

**Cause**: MCP server not running or misconfigured

**Solutions**:
1. Check config file syntax (valid JSON)
2. Verify API token is correct
3. Ensure Jira URL doesn't have trailing slash
4. Restart Claude completely
5. Check Claude logs for MCP errors

**Logs location**:
- Mac: `~/Library/Logs/Claude/`
- Windows: `%APPDATA%\Claude\logs\`
- Linux: `~/.config/Claude/logs/`

### Issue: "Authentication failed"

**Cause**: Invalid API token or email

**Solutions**:
1. Regenerate API token in Atlassian
2. Verify email matches Atlassian account
3. Check for extra spaces in token/email
4. For Jira Server, verify password/PAT is correct

### Issue: "Cannot create Epic"

**Cause**: Jira project doesn't have Epic issue type enabled

**Solutions**:
1. Check your Jira project settings
2. Ensure "Epic" issue type exists
3. Verify you have permission to create Epics
4. Try creating as "Story" instead (configure in skill)

### Issue: "Custom field 'story points' not found"

**Cause**: Story points is a custom field in your Jira

**Solutions**:
1. Find the custom field ID in Jira settings
2. Configure it in the skill (I'll ask during first run)
3. Or skip story points (optional)

### Issue: MCP command not found

**Cause**: npx or node not in PATH

**Solutions**:
1. Ensure Node.js is installed: `node --version`
2. Add Node.js to PATH
3. Use full path to node/npx in config
4. Reinstall Node.js

## Project-Specific Configuration

When you first use the Agile Master skill, I'll ask for project-specific settings:

### Configuration Questions:

**Q1: What's your Jira project key?**
```
Example: "PROJ", "DEV", "TEAM"
```

**Q2: Default assignees for different roles?**
```
Backend: john.doe
Frontend: jane.smith
QA: bob.tester
DevOps: alice.ops
```

**Q3: Story point scale?**
```
Options:
- Fibonacci (1, 2, 3, 5, 8, 13)
- T-shirt (XS, S, M, L, XL)
- Linear (1, 2, 3, 4, 5)
```

**Q4: Sprint length?**
```
Typical: 2 weeks
```

**Q5: Custom field IDs (if needed)?**
```
Story Points: customfield_10016
Epic Name: customfield_10011
Sprint: customfield_10020
```

### Finding Custom Field IDs

If you need custom field IDs:

1. Go to any Jira issue in your browser
2. Click "..." → "View in JSON"
3. Search for the field name (e.g., "Story Points")
4. Note the `customfield_XXXXX` ID

Or use Jira REST API:
```bash
curl -u your-email@company.com:your-api-token \
  https://your-company.atlassian.net/rest/api/3/field \
  | grep -i "story points"
```

## Security Best Practices

1. **Never commit API tokens** to git
2. **Use environment variables** for CI/CD
3. **Rotate tokens regularly** (quarterly)
4. **Limit token scope** to minimum needed permissions
5. **Use separate tokens** for different tools/users

## Environment Variables (Alternative to Config File)

Instead of config file, you can set environment variables:

```bash
# In your shell profile (~/.zshrc, ~/.bashrc)
export JIRA_BASE_URL="https://your-company.atlassian.net"
export JIRA_EMAIL="your-email@company.com"
export JIRA_API_TOKEN="your-api-token"
```

Then configure MCP to use them:
```json
{
  "mcpServers": {
    "jira": {
      "command": "npx",
      "args": ["-y", "@orengrinker/jira-mcp-server"],
      "env": {
        "JIRA_BASE_URL": "${JIRA_BASE_URL}",
        "JIRA_EMAIL": "${JIRA_EMAIL}",
        "JIRA_API_TOKEN": "${JIRA_API_TOKEN}"
      }
    }
  }
}
```

## Team Setup

For team-wide adoption:

### 1. Create Shared Documentation

Document your team's setup:
```markdown
# Team Jira MCP Setup

Jira URL: https://our-company.atlassian.net
Project Key: TEAM

Each developer should:
1. Create their own API token
2. Configure MCP with their credentials
3. Test with "/skill agile-master"
```

### 2. Create API Token Guide

Provide step-by-step screenshots for your team.

### 3. Define Standards

Agree on:
- Story point scale
- Issue naming conventions
- Labels to use
- Sprint cadence

### 4. Template Configuration

Share a template config (without tokens!):
```json
{
  "mcpServers": {
    "jira": {
      "command": "npx",
      "args": ["-y", "@orengrinker/jira-mcp-server"],
      "env": {
        "JIRA_BASE_URL": "https://our-company.atlassian.net",
        "JIRA_EMAIL": "YOUR-EMAIL-HERE",
        "JIRA_API_TOKEN": "YOUR-TOKEN-HERE"
      }
    }
  }
}
```

## Advanced: Multiple Jira Instances

If you work with multiple Jira instances:

```json
{
  "mcpServers": {
    "jira-company": {
      "command": "npx",
      "args": ["-y", "@orengrinker/jira-mcp-server"],
      "env": {
        "JIRA_BASE_URL": "https://company.atlassian.net",
        "JIRA_EMAIL": "you@company.com",
        "JIRA_API_TOKEN": "token1"
      }
    },
    "jira-client": {
      "command": "npx",
      "args": ["-y", "@orengrinker/jira-mcp-server"],
      "env": {
        "JIRA_BASE_URL": "https://client.atlassian.net",
        "JIRA_EMAIL": "you@client.com",
        "JIRA_API_TOKEN": "token2"
      }
    }
  }
}
```

Then specify which to use:
```
User: "Use jira-client to create Epic in PROJECT"
```

## Getting Help

If you're stuck:

1. **Check Claude logs** for MCP errors
2. **Test Jira API directly** with curl:
   ```bash
   curl -u your-email:your-token \
     https://your-company.atlassian.net/rest/api/3/myself
   ```
3. **Verify MCP server is running**:
   - Look for MCP process in task manager
   - Check if npx can run the package
4. **Ask in the skill**: "Help me troubleshoot Jira MCP connection"

## Resources

- [Jira REST API Docs](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/)
- [Atlassian API Tokens](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [OrenGrinker Jira MCP](https://github.com/OrenGrinker/jira-mcp-server)
- [Cosmix Jira MCP](https://github.com/cosmix/jira-mcp)

---

**Once setup is complete, you're ready to use Agile Master!**

Test it:
```
/skill agile-master
"Test Jira connection"
```

The skill will verify everything is working and guide you through your first feature setup.
