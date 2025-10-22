# MCP Configuration Setup

This directory contains Claude Code CLI configuration for Model Context Protocol (MCP) servers.

## Jira MCP Server

To use the Agile Master skill with Jira integration, you need to configure the Jira MCP server.

### Setup Steps

1. **Get Jira API Token**
   - Go to https://id.atlassian.com/manage-profile/security/api-tokens
   - Click "Create API token"
   - Give it a name (e.g., "Claude Code")
   - Copy the token

2. **Create MCP Configuration**
   ```bash
   # Copy the example file (in project root)
   cp .mcp.json.example .mcp.json

   # Edit with your credentials
   # Replace:
   # - JIRA_BASE_URL: Your Jira URL
   # - JIRA_EMAIL: Your Atlassian email
   # - JIRA_API_TOKEN: Your API token from step 1
   ```

   **Note**: The `.mcp.json` file should be in the **project root directory** (not in `.claude/`)

3. **Verify Configuration**
   ```json
   {
     "mcpServers": {
       "jira": {
         "command": "npx",
         "args": ["-y", "@orengrinker/jira-mcp-server"],
         "env": {
           "JIRA_BASE_URL": "https://nexusprj.atlassian.net",
           "JIRA_EMAIL": "your-email@company.com",
           "JIRA_API_TOKEN": "your-token-here"
         }
       }
     }
   }
   ```

4. **Test Connection**
   ```
   # In Claude Code CLI:
   "Search for issues in KAN project"
   ```

### Security Notes

- ⚠️ **Never commit `mcp.json` to git** (it's in .gitignore)
- ✅ Use `mcp.json.example` for sharing templates
- 🔄 Rotate API tokens regularly
- 🔒 Each team member should use their own API token

### Available MCP Servers

Currently configured:
- **jira**: Jira Cloud integration (@orengrinker/jira-mcp-server)

### Troubleshooting

**Issue**: MCP server not connecting

**Solution**:
1. Verify API token is valid
2. Check Jira URL (no trailing slash)
3. Ensure email matches Atlassian account
4. Try regenerating the API token

**Issue**: Permission errors

**Solution**:
- Verify you have access to the Jira project
- Check your Jira account has required permissions
- Contact Jira admin if needed

### Using with Agile Master Skill

Once configured, you can use:

```
/skill agile-master
"Add OAuth authentication feature"
```

The skill will automatically:
1. Create PRD document
2. Create Jira Epic
3. Generate User Stories
4. Create implementation Tasks
5. Assign to team members

See `.claude/skills/agile-master/` for more details.

### Resources

- [Jira MCP Server](https://github.com/OrenGrinker/jira-mcp-server)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [Atlassian API Tokens](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/)
