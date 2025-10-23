# Jira REST API v3 Reference

Complete reference for Jira Cloud REST API v3 endpoints used in this skill.

**Official Documentation**: https://developer.atlassian.com/cloud/jira/platform/rest/v3/

---

## Table of Contents

1. [2025 API Changes](#2025-api-changes)
2. [Authentication](#authentication)
3. [Search API](#search-api)
4. [Issue Creation](#issue-creation)
5. [Epic Management](#epic-management)
6. [Custom Fields](#custom-fields)
7. [JQL Queries](#jql-queries)
8. [Error Handling](#error-handling)

---

## 2025 API Changes

### Search Endpoint Migration (CRITICAL)

**Deprecated** (Removed Oct 31, 2025):
```
GET /rest/api/3/search
```

**New Endpoint** (Use this):
```
GET /rest/api/3/search/jql
```

**Timeline**:
- **May 1, 2025**: Old API deprecated, still functional
- **May 5 - July 31, 2025**: Performance improvements, eventual consistency
- **August 1 - October 31, 2025**: Progressive shutdown
- **November 1, 2025**: Old API completely disabled ❌

**Migration Guide**: https://developer.atlassian.com/changelog/#CHANGE-2046

**Response Structure Changed**:

```javascript
// OLD Response
{
  "total": 100,
  "startAt": 0,
  "maxResults": 50,
  "issues": [...]
}

// NEW Response
{
  "issues": [...],
  "isLast": true,
  "nextPageToken": "abc123"  // Pagination token
}
```

**Pagination Changed**:
- **Old**: Offset-based (`startAt` parameter)
- **New**: Token-based (`nextPageToken` in response)

---

## Authentication

### Basic Authentication

All requests require HTTP Basic Authentication:

```bash
# Header
Authorization: Basic <base64(email:api_token)>
```

**Example**:
```bash
EMAIL="your-email@example.com"
TOKEN="your-api-token"
AUTH=$(echo -n "$EMAIL:$TOKEN" | base64)

curl -H "Authorization: Basic $AUTH" \
     -H "Accept: application/json" \
     https://your-domain.atlassian.net/rest/api/3/project/KAN
```

**Get API Token**: https://id.atlassian.com/manage-profile/security/api-tokens

---

## Search API

### Search Issues via JQL

**Endpoint**: `GET /rest/api/3/search/jql`

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `jql` | string | Yes | JQL query string |
| `maxResults` | integer | No | Max results per page (default: 50, max: 100) |
| `fields` | string | No | Comma-separated field list |
| `nextPageToken` | string | No | Token from previous response |

**Example Request**:
```bash
curl -X GET \
  'https://your-domain.atlassian.net/rest/api/3/search/jql?jql=project=KAN&maxResults=10&fields=summary,status' \
  -H 'Authorization: Basic <auth>' \
  -H 'Accept: application/json'
```

**Example Response**:
```json
{
  "issues": [
    {
      "id": "10000",
      "key": "KAN-1",
      "fields": {
        "summary": "First issue",
        "status": {
          "name": "To Do"
        }
      }
    }
  ],
  "isLast": true
}
```

**Pagination**:
```javascript
// First page
GET /rest/api/3/search/jql?jql=project=KAN&maxResults=50

// Response includes nextPageToken if more results exist
{
  "issues": [...],
  "isLast": false,
  "nextPageToken": "abc123"
}

// Next page
GET /rest/api/3/search/jql?jql=project=KAN&maxResults=50&nextPageToken=abc123
```

---

## Issue Creation

### Create Issue

**Endpoint**: `POST /rest/api/3/issue`

**Request Body**:
```json
{
  "fields": {
    "project": {
      "key": "PROJ"
    },
    "summary": "Issue title",
    "description": {
      "type": "doc",
      "version": 1,
      "content": [
        {
          "type": "paragraph",
          "content": [
            {
              "type": "text",
              "text": "Issue description"
            }
          ]
        }
      ]
    },
    "issuetype": {
      "name": "Task"
    }
  }
}
```

**Response**:
```json
{
  "id": "10000",
  "key": "PROJ-123",
  "self": "https://your-domain.atlassian.net/rest/api/3/issue/10000"
}
```

### Issue Types

Common issue types:
- `Task` - Standard task
- `Story` - User story (Scrum/Kanban)
- `Epic` - Epic (collection of stories)
- `Bug` - Bug report
- `Subtask` - Subtask (child of another issue)

**Note**: Issue types vary by project template (Scrum, Kanban, etc.)

---

## Epic Management

### Creating Epics

Epics require different approaches for **Company-managed** vs **Team-managed** projects.

#### Company-Managed Projects

Require **Epic Name** custom field:

```json
{
  "fields": {
    "project": { "key": "PROJ" },
    "summary": "Epic Title",
    "description": { /* ... */ },
    "issuetype": { "name": "Epic" },
    "customfield_10011": "Epic Name"  // Required!
  }
}
```

**Finding Epic Name Field ID**:
```bash
curl -X GET \
  'https://your-domain.atlassian.net/rest/api/3/field' \
  -H 'Authorization: Basic <auth>' \
  | grep -i "epic name"

# Output: "customfield_10011": "Epic Name"
```

Common Epic Name field IDs:
- `customfield_10008`
- `customfield_10011`
- `customfield_10000`

#### Team-Managed Projects

**Do NOT require** Epic Name field:

```json
{
  "fields": {
    "project": { "key": "PROJ" },
    "summary": "Epic Title",
    "description": { /* ... */ },
    "issuetype": { "name": "Epic" }
    // NO Epic Name field!
  }
}
```

**Error Handling**:
```javascript
try {
  // Try with Epic Name field
  createIssue({ ..., customfield_10011: "Epic Name" });
} catch (error) {
  if (error.message.includes("customfield_10011") ||
      error.message.includes("cannot be set")) {
    // Team-managed project, retry without Epic Name
    createIssue({ /* without customfield_10011 */ });
  }
}
```

### Linking Issues to Epics

Use **parent** field (Team-managed and modern Company-managed):

```json
{
  "fields": {
    "project": { "key": "PROJ" },
    "summary": "Story under Epic",
    "issuetype": { "name": "Story" },
    "parent": {
      "key": "PROJ-123"  // Epic key
    }
  }
}
```

**Legacy Company-managed** (deprecated):
Use Epic Link custom field instead:
```json
{
  "fields": {
    "customfield_10014": "PROJ-123"  // Epic Link field
  }
}
```

---

## Custom Fields

### Finding Custom Field IDs

**List All Fields**:
```bash
curl -X GET \
  'https://your-domain.atlassian.net/rest/api/3/field' \
  -H 'Authorization: Basic <auth>' \
  -H 'Accept: application/json'
```

**Search Specific Fields**:
```bash
# Epic Name
curl ... /rest/api/3/field | grep -i "epic name"

# Story Points
curl ... /rest/api/3/field | grep -i "story point"

# Sprint
curl ... /rest/api/3/field | grep -i "sprint"
```

**Response Structure**:
```json
[
  {
    "id": "customfield_10016",
    "name": "Story Points",
    "custom": true,
    "schema": {
      "type": "number"
    }
  },
  {
    "id": "customfield_10011",
    "name": "Epic Name",
    "custom": true,
    "schema": {
      "type": "string"
    }
  }
]
```

### Common Custom Fields

| Field | Common IDs | Type | Use Case |
|-------|------------|------|----------|
| Epic Name | customfield_10008, 10011 | string | Epic creation (Company-managed) |
| Story Points | customfield_10016, 10026 | number | Estimation |
| Sprint | customfield_10020 | array | Sprint assignment |
| Epic Link | customfield_10014 | string | Link to Epic (legacy) |

**Environment Variables**:
```bash
# Override default field IDs
JIRA_EPIC_NAME_FIELD=customfield_10008
JIRA_STORY_POINTS_FIELD=customfield_10026
```

---

## JQL Queries

### JQL (Jira Query Language)

**Basic Syntax**:
```
field OPERATOR value
```

**Common Queries**:

```jql
# All issues in project
project = KAN

# Open issues
project = KAN AND status != Done

# Assigned to me
assignee = currentUser()

# Created recently
created >= -7d

# Stories in current sprint
project = KAN AND issuetype = Story AND sprint in openSprints()

# Issues under Epic
parent = KAN-123

# Complex query
project = KAN AND issuetype = Story AND status = "In Progress" AND assignee = currentUser() ORDER BY priority DESC
```

**Operators**:
- `=`, `!=` - Equals, not equals
- `>`, `>=`, `<`, `<=` - Comparison
- `~`, `!~` - Contains, not contains
- `IN`, `NOT IN` - List membership
- `IS`, `IS NOT` - Null checks

**Functions**:
- `currentUser()` - Current authenticated user
- `openSprints()` - Active sprints
- `startOfDay()`, `endOfDay()` - Date functions
- `now()` - Current timestamp

**Special Fields**:
- `project`, `summary`, `description`, `status`, `assignee`
- `created`, `updated`, `resolved`
- `priority`, `issuetype`, `labels`
- `parent` - Epic relationship

**Order By**:
```jql
project = KAN ORDER BY created DESC
project = KAN ORDER BY priority DESC, created ASC
```

---

## Error Handling

### Common HTTP Status Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 200 | Success | - |
| 201 | Created | Issue successfully created |
| 204 | No Content | Delete/update successful |
| 400 | Bad Request | Check request body, JQL syntax |
| 401 | Unauthorized | Verify API token, email |
| 403 | Forbidden | Check permissions |
| 404 | Not Found | Verify project key, issue key |
| 410 | Gone | **API deprecated** - update endpoint |

### Error Response Format

```json
{
  "errorMessages": [
    "Issue type 'Epic' not found"
  ],
  "errors": {
    "customfield_10011": "Field cannot be set"
  }
}
```

### Common Errors

#### 1. "API has been removed" (410)

```json
{
  "errorMessages": [
    "요청된 API가 삭제되었습니다. /rest/api/3/search/jql API로 마이그레이션하세요."
  ]
}
```

**Solution**: Update to `/rest/api/3/search/jql`

#### 2. "Field cannot be set"

```json
{
  "errors": {
    "customfield_10011": "Field 'customfield_10011' cannot be set. It is not on the appropriate screen, or unknown."
  }
}
```

**Solution**:
- Team-managed project: Remove Epic Name field
- Company-managed: Find correct field ID via `/rest/api/3/field`

#### 3. JQL Syntax Error

```json
{
  "errorMessages": [
    "JQL 쿼리 오류: 쿼리 종료 전 연산자 예측."
  ]
}
```

**Solution**: Check JQL syntax, escape special characters

#### 4. Authentication Failed (401)

```json
{
  "errorMessages": [
    "Client must be authenticated to access this resource."
  ]
}
```

**Solution**:
- Verify API token is correct
- Check email matches Atlassian account
- Regenerate token if needed

---

## Code Examples

### Node.js (HTTPS)

```javascript
const https = require('https');

function jiraRequest(method, endpoint, data = null) {
  return new Promise((resolve, reject) => {
    const auth = Buffer.from(`${email}:${apiToken}`).toString('base64');
    const url = new URL(endpoint, baseUrl);

    const options = {
      hostname: url.hostname,
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
          resolve(JSON.parse(body));
        } else {
          reject(new Error(`Jira API Error ${res.statusCode}: ${body}`));
        }
      });
    });

    req.on('error', reject);
    if (data) req.write(JSON.stringify(data));
    req.end();
  });
}

// Usage
const result = await jiraRequest('GET', '/rest/api/3/search/jql?jql=project=KAN');
```

### cURL

```bash
# Search issues
curl -X GET \
  'https://your-domain.atlassian.net/rest/api/3/search/jql?jql=project=KAN' \
  -u 'email@example.com:api_token' \
  -H 'Accept: application/json'

# Create issue
curl -X POST \
  'https://your-domain.atlassian.net/rest/api/3/issue' \
  -u 'email@example.com:api_token' \
  -H 'Content-Type: application/json' \
  -d '{
    "fields": {
      "project": {"key": "KAN"},
      "summary": "New task",
      "issuetype": {"name": "Task"}
    }
  }'
```

---

## Additional Resources

### Official Documentation

- **REST API v3**: https://developer.atlassian.com/cloud/jira/platform/rest/v3/
- **JQL Reference**: https://support.atlassian.com/jira-software-cloud/docs/use-advanced-search-with-jira-query-language-jql/
- **API Changelog**: https://developer.atlassian.com/changelog/
- **Custom Fields**: https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-fields/

### Migration Guides

- **Search API Migration**: https://developer.atlassian.com/changelog/#CHANGE-2046
- **Epic Link Deprecation**: https://community.atlassian.com/t5/Jira-questions/Epic-Link-vs-Parent/qaq-p/1409874

### Community

- **Atlassian Community**: https://community.atlassian.com/
- **Developer Community**: https://developer.atlassian.com/community/

---

**Last Updated**: 2025-10-23
**API Version**: REST API v3
**Skill Version**: 1.0.0
