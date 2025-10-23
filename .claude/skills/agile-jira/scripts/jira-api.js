#!/usr/bin/env node

/**
 * Jira REST API Client
 *
 * Direct REST API calls to Jira (no MCP server needed)
 * Based on playwright-skill pattern
 *
 * Usage:
 *   node jira-api.js import ../../../docs/stories/
 *   node jira-api.js create-epic --title="Feature" --description="..."
 *   node jira-api.js create-story --epic="KAN-123" --title="..." --ac="..."
 *   node jira-api.js search --jql="project = KAN"
 *   node jira-api.js track --epic="KAN-123"
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// ============================================================================
// Configuration Loading
// ============================================================================

function loadConfig() {
  // Priority 1: Environment variables
  if (process.env.JIRA_BASE_URL) {
    return {
      baseUrl: process.env.JIRA_BASE_URL.replace(/\/$/, ''),
      email: process.env.JIRA_EMAIL,
      apiToken: process.env.JIRA_API_TOKEN,
      projectKey: process.env.JIRA_PROJECT_KEY || 'PROJ'
    };
  }

  // Priority 2: .jira-config.json (in skill directory)
  const configPath = path.join(__dirname, '../.jira-config.json');
  if (fs.existsSync(configPath)) {
    try {
      const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      config.baseUrl = config.baseUrl.replace(/\/$/, '');
      return config;
    } catch (e) {
      console.error('Error reading .jira-config.json:', e.message);
    }
  }

  // Priority 3: Project root .env
  const envPath = path.join(__dirname, '../../../../.env');
  if (fs.existsSync(envPath)) {
    try {
      const envContent = fs.readFileSync(envPath, 'utf8');
      const config = {};

      envContent.split('\n').forEach(line => {
        const trimmed = line.trim();
        if (!trimmed || trimmed.startsWith('#')) return;

        const [key, ...valueParts] = trimmed.split('=');
        const value = valueParts.join('=').replace(/^["']|["']$/g, '');

        if (key === 'JIRA_BASE_URL') config.baseUrl = value.replace(/\/$/, '');
        if (key === 'JIRA_EMAIL') config.email = value;
        if (key === 'JIRA_API_TOKEN') config.apiToken = value;
        if (key === 'JIRA_PROJECT_KEY') config.projectKey = value;
      });

      if (config.baseUrl && config.email && config.apiToken) {
        return config;
      }
    } catch (e) {
      // Silent fail, will show error below
    }
  }

  throw new Error(`
╔════════════════════════════════════════════════════════════╗
║  Jira Configuration Not Found                              ║
╚════════════════════════════════════════════════════════════╝

Please configure Jira credentials using one of these methods:

1️⃣  Environment Variables (Recommended):
   export JIRA_BASE_URL="https://your-company.atlassian.net"
   export JIRA_EMAIL="your-email@company.com"
   export JIRA_API_TOKEN="your-api-token"
   export JIRA_PROJECT_KEY="PROJ"

2️⃣  Create .jira-config.json:
   cd .claude/skills/agile-jira
   cp .jira-config.example.json .jira-config.json
   # Edit with your details

3️⃣  Add to project .env file:
   JIRA_BASE_URL=https://your-company.atlassian.net
   JIRA_EMAIL=your-email@company.com
   JIRA_API_TOKEN=your-token
   JIRA_PROJECT_KEY=PROJ

Get API Token: https://id.atlassian.com/manage-profile/security/api-tokens
`);
}

let config;
try {
  config = loadConfig();
} catch (e) {
  console.error(e.message);
  process.exit(1);
}

// ============================================================================
// Jira REST API Client
// ============================================================================

function jiraRequest(method, endpoint, data = null) {
  return new Promise((resolve, reject) => {
    const auth = Buffer.from(`${config.email}:${config.apiToken}`).toString('base64');
    const url = new URL(endpoint, config.baseUrl);

    const options = {
      hostname: url.hostname,
      port: url.port || 443,
      path: url.pathname + url.search,
      method: method,
      headers: {
        'Authorization': `Basic ${auth}`,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      }
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          try {
            resolve(body ? JSON.parse(body) : {});
          } catch (e) {
            resolve(body);
          }
        } else {
          reject(new Error(`Jira API Error ${res.statusCode}: ${body}`));
        }
      });
    });

    req.on('error', (e) => reject(new Error(`Network Error: ${e.message}`)));

    if (data) {
      req.write(JSON.stringify(data));
    }

    req.end();
  });
}

// ============================================================================
// Core Operations
// ============================================================================

async function createEpic(title, description, options = {}) {
  const issueData = {
    fields: {
      project: { key: config.projectKey },
      summary: title,
      description: {
        type: 'doc',
        version: 1,
        content: [{
          type: 'paragraph',
          content: [{ type: 'text', text: description }]
        }]
      },
      issuetype: { name: 'Epic' }
    }
  };

  // Epic Name field (Company-managed projects only)
  // Team-managed projects don't require this field
  // Custom field ID varies by Jira instance (commonly customfield_10008 or customfield_10011)
  // Set JIRA_EPIC_NAME_FIELD env var to override
  const epicNameField = process.env.JIRA_EPIC_NAME_FIELD || 'customfield_10011';

  // Try to set Epic Name, but don't fail if field doesn't exist (Team-managed projects)
  if (options.setEpicName !== false) {
    issueData.fields[epicNameField] = title;
  }

  if (options.labels) issueData.fields.labels = options.labels;
  if (options.priority) issueData.fields.priority = { name: options.priority };

  try {
    const result = await jiraRequest('POST', '/rest/api/3/issue', issueData);
    return result;
  } catch (error) {
    // If Epic Name field fails, retry without it (Team-managed projects)
    if (error.message.includes(epicNameField) || error.message.includes('cannot be set')) {
      delete issueData.fields[epicNameField];
      console.log(`   ℹ️  Retrying Epic creation without Epic Name field (Team-managed project)`);
      const result = await jiraRequest('POST', '/rest/api/3/issue', issueData);
      return result;
    }
    throw error;
  }
}

async function createStory(epicKey, title, description, acceptanceCriteria, options = {}) {
  const fullDescription = `${description}\n\n## Acceptance Criteria\n\n${acceptanceCriteria}`;

  const issueData = {
    fields: {
      project: { key: config.projectKey },
      summary: title,
      description: {
        type: 'doc',
        version: 1,
        content: [{
          type: 'paragraph',
          content: [{ type: 'text', text: fullDescription }]
        }]
      },
      issuetype: { name: 'Story' },
      parent: { key: epicKey }
    }
  };

  // Story Points field (custom field ID varies by Jira instance)
  // Common IDs: customfield_10016, customfield_10026, etc.
  // Set JIRA_STORY_POINTS_FIELD env var to override
  if (options.storyPoints) {
    const storyPointsField = process.env.JIRA_STORY_POINTS_FIELD || 'customfield_10016';
    issueData.fields[storyPointsField] = options.storyPoints;
  }

  if (options.labels) issueData.fields.labels = options.labels;
  if (options.assignee) issueData.fields.assignee = { accountId: options.assignee };

  const result = await jiraRequest('POST', '/rest/api/3/issue', issueData);
  return result;
}

async function searchIssues(jql, options = {}) {
  const params = new URLSearchParams({
    jql: jql,
    maxResults: options.maxResults || 50,
    fields: options.fields || 'summary,status,assignee,parent'
  });

  // Updated to use /search/jql endpoint (2025 API change)
  // Old endpoint /rest/api/3/search was deprecated and removed
  // See: https://developer.atlassian.com/changelog/#CHANGE-2046
  const result = await jiraRequest('GET', `/rest/api/3/search/jql?${params}`);
  return result;
}

async function getIssue(issueKey) {
  const result = await jiraRequest('GET', `/rest/api/3/issue/${issueKey}`);
  return result;
}

// ============================================================================
// Story File Parsing
// ============================================================================

function parseStoryFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');

  // Extract title from # User Story: [Title]
  const titleMatch = content.match(/^#\s+(?:User Story:\s*)?(.+?)$/m);
  const title = titleMatch ? titleMatch[1].trim() : path.basename(filePath, '.md');

  // Extract Epic name
  const epicMatch = content.match(/\*\*Epic\*\*:\s*(.+?)$/m);
  const epicName = epicMatch ? epicMatch[1].trim() : null;

  // Extract Story section
  const storyMatch = content.match(/##\s+Story\s*\n([\s\S]*?)(?=\n##|$)/);
  const story = storyMatch ? storyMatch[1].trim() : '';

  // Extract Acceptance Criteria
  const acMatch = content.match(/##\s+Acceptance Criteria\s*\n([\s\S]*?)(?=\n##|$)/);
  const acceptanceCriteria = acMatch ? acMatch[1].trim() : '';

  // Extract Story Points
  const pointsMatch = content.match(/\*\*(\d+)\s+points?\*\*/i);
  const storyPoints = pointsMatch ? parseInt(pointsMatch[1]) : null;

  // Extract Labels
  const labelsMatch = content.match(/##\s+Labels\s*\n(.+?)$/m);
  const labels = labelsMatch ? labelsMatch[1].split(',').map(l => l.trim()) : [];

  return {
    title,
    epicName,
    story,
    acceptanceCriteria,
    storyPoints,
    labels,
    filePath
  };
}

// ============================================================================
// High-Level Operations
// ============================================================================

async function importStories(storiesDir) {
  console.log(`\n📁 Reading stories from: ${storiesDir}\n`);

  // Get all .md files
  const files = fs.readdirSync(storiesDir)
    .filter(f => f.endsWith('.md'))
    .map(f => path.join(storiesDir, f));

  if (files.length === 0) {
    console.log('❌ No .md files found in directory');
    return;
  }

  // Parse all stories
  const stories = files.map(parseStoryFile);

  // Group by Epic
  const epicGroups = {};
  stories.forEach(story => {
    const epic = story.epicName || 'No Epic';
    if (!epicGroups[epic]) epicGroups[epic] = [];
    epicGroups[epic].push(story);
  });

  console.log(`Found ${stories.length} stories in ${Object.keys(epicGroups).length} epic(s)\n`);

  // Create Epics and Stories
  const results = [];

  for (const [epicName, storyList] of Object.entries(epicGroups)) {
    if (epicName === 'No Epic') {
      console.log('⚠️  Skipping stories without Epic');
      continue;
    }

    console.log(`\n📊 Epic: ${epicName}`);

    // Create Epic
    try {
      const epic = await createEpic(epicName, `Epic for ${epicName}`);
      console.log(`   ✅ Epic created: ${epic.key}`);
      console.log(`   🔗 ${config.baseUrl}/browse/${epic.key}`);

      // Create Stories under this Epic
      for (const story of storyList) {
        try {
          const storyResult = await createStory(
            epic.key,
            story.title,
            story.story,
            story.acceptanceCriteria,
            {
              storyPoints: story.storyPoints,
              labels: story.labels
            }
          );
          console.log(`   ✅ Story created: ${storyResult.key} - ${story.title}`);
          console.log(`      Points: ${story.storyPoints || 'not set'}`);

          results.push({ epic: epic.key, story: storyResult.key });
        } catch (e) {
          console.log(`   ❌ Failed to create story: ${story.title}`);
          console.log(`      Error: ${e.message}`);
        }
      }
    } catch (e) {
      console.log(`   ❌ Failed to create Epic: ${epicName}`);
      console.log(`      Error: ${e.message}`);
    }
  }

  console.log(`\n\n✅ Import complete: ${results.length} stories created\n`);
  return results;
}

async function trackEpic(epicKey) {
  console.log(`\n📊 Tracking Epic: ${epicKey}\n`);

  // Get Epic details
  const epic = await getIssue(epicKey);
  console.log(`Epic: ${epic.fields.summary} (${epicKey})`);
  console.log(`Status: ${epic.fields.status.name}`);

  // Get all stories in this Epic
  const jql = `parent = ${epicKey} ORDER BY created ASC`;
  const result = await searchIssues(jql);

  const stories = result.issues;
  const total = stories.length;
  const done = stories.filter(s => s.fields.status.name === 'Done').length;
  const inProgress = stories.filter(s => s.fields.status.name === 'In Progress').length;
  const todo = total - done - inProgress;

  console.log(`\nProgress: ${done}/${total} stories complete (${Math.round(done/total*100)}%)`);
  console.log(`   ✅ Done: ${done}`);
  console.log(`   🚧 In Progress: ${inProgress}`);
  console.log(`   📋 To Do: ${todo}`);

  console.log('\nStories:');
  stories.forEach(story => {
    const status = story.fields.status.name;
    const icon = status === 'Done' ? '✅' : status === 'In Progress' ? '🚧' : '📋';
    console.log(`   ${icon} ${story.key}: ${story.fields.summary} (${status})`);
  });

  console.log('');
}

// ============================================================================
// CLI Interface
// ============================================================================

if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];

  (async () => {
    try {
      if (command === 'create-epic') {
        const title = args.find(a => a.startsWith('--title='))?.split('=')[1];
        const description = args.find(a => a.startsWith('--description='))?.split('=')[1];

        if (!title || !description) {
          console.error('Usage: create-epic --title="..." --description="..."');
          process.exit(1);
        }

        const result = await createEpic(title, description);
        console.log('✅ Epic created:', result.key);
        console.log('🔗', `${config.baseUrl}/browse/${result.key}`);
      }

      else if (command === 'create-story') {
        const epicKey = args.find(a => a.startsWith('--epic='))?.split('=')[1];
        const title = args.find(a => a.startsWith('--title='))?.split('=')[1];
        const description = args.find(a => a.startsWith('--description='))?.split('=')[1];
        const ac = args.find(a => a.startsWith('--ac='))?.split('=')[1];
        const pointsArg = args.find(a => a.startsWith('--points='));
        const points = pointsArg ? parseInt(pointsArg.split('=')[1]) : null;

        if (!epicKey || !title || !description || !ac) {
          console.error('Usage: create-story --epic=KEY --title="..." --description="..." --ac="..." [--points=N]');
          process.exit(1);
        }

        const result = await createStory(epicKey, title, description, ac, {
          storyPoints: points
        });
        console.log('✅ Story created:', result.key);
        console.log('🔗', `${config.baseUrl}/browse/${result.key}`);
      }

      else if (command === 'search') {
        const jqlArg = args.find(a => a.startsWith('--jql='));
        const jql = jqlArg ? jqlArg.substring('--jql='.length) : null;

        if (!jql) {
          console.error('Usage: search --jql="project = PROJ"');
          process.exit(1);
        }

        const result = await searchIssues(jql);
        console.log(`\nFound ${result.issues.length} issues${result.isLast ? '' : ' (more available)'}:\n`);
        result.issues.forEach(issue => {
          console.log(`  ${issue.key}: ${issue.fields.summary} (${issue.fields.status.name})`);
        });
        console.log('');
      }

      else if (command === 'track') {
        const epicKey = args.find(a => a.startsWith('--epic='))?.split('=')[1];

        if (!epicKey) {
          console.error('Usage: track --epic=KEY');
          process.exit(1);
        }

        await trackEpic(epicKey);
      }

      else if (command === 'import') {
        const storiesDir = args[1];

        if (!storiesDir) {
          console.error('Usage: import <path-to-stories-directory>');
          console.error('Example: import ../../../docs/stories/');
          process.exit(1);
        }

        if (!fs.existsSync(storiesDir)) {
          console.error(`Directory not found: ${storiesDir}`);
          process.exit(1);
        }

        await importStories(storiesDir);
      }

      else {
        console.log(`
╔════════════════════════════════════════════════════════════╗
║  Jira REST API Client                                      ║
╚════════════════════════════════════════════════════════════╝

Commands:

  import <dir>           Import user stories from markdown files
                         Example: import ../../../docs/stories/

  create-epic            Create Epic ticket
                         --title="..." --description="..."

  create-story           Create Story ticket
                         --epic=KEY --title="..." --description="..."
                         --ac="..." [--points=N]

  search                 Search issues via JQL
                         --jql="project = PROJ AND status != Done"

  track                  Track Epic progress
                         --epic=KEY

  get                    Get issue details
                         --issue=KEY

Examples:

  # Import stories
  node jira-api.js import ../../../docs/stories/

  # Create Epic
  node jira-api.js create-epic \\
    --title="OAuth Authentication" \\
    --description="Add OAuth login"

  # Create Story
  node jira-api.js create-story \\
    --epic="KAN-123" \\
    --title="Google OAuth" \\
    --description="As a user..." \\
    --ac="Given...When...Then..." \\
    --points=5

  # Track Epic progress
  node jira-api.js track --epic="KAN-123"

Configuration: ${config.baseUrl} (${config.projectKey})
        `);
      }
    } catch (error) {
      console.error('\n❌ Error:', error.message);
      process.exit(1);
    }
  })();
}

// Export for use as module
module.exports = {
  createEpic,
  createStory,
  searchIssues,
  getIssue,
  importStories,
  trackEpic
};
