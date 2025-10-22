---
name: Agile Master
description: Complete end-to-end agile project management from PRD writing to Jira ticket creation. Manages Epic → User Story → Implementation Task → PR → Deployment lifecycle with interactive guidance. Use this when starting new features, planning sprints, creating Jira tickets, or managing squad workflows. Integrates with Jira MCP for automated ticket creation and tracking.
allowed-tools: Write, Edit, Read, AskUserQuestion, Bash, Glob, Grep
---

# Agile Master

Your comprehensive agile project assistant that guides you from initial product requirements through Jira ticket creation, implementation tracking, and deployment coordination.

## What This Skill Does

This skill provides **interactive, step-by-step guidance** through the complete agile development lifecycle:

1. **PRD Creation** - Write comprehensive Product Requirements Documents
2. **Jira Epic Creation** - Automatically create Epic tickets linked to PRD
3. **Feature Decomposition** - Break down features into User Stories
4. **User Story Generation** - Create Story tickets with clear Acceptance Criteria
5. **Task Breakdown** - Generate implementation tasks for each Story
6. **Progress Tracking** - Monitor ticket status and coordinate deployment

## Workflow Overview

```
User: "I want to add OAuth authentication"
  ↓
[1] PRD Creation
    → Ask key questions (users, metrics, scope)
    → Generate comprehensive PRD document
    → Review and refine with user
    ✓ docs/prd/oauth-authentication-2024-10.md created

[2] Jira Epic Creation
    → Check Jira MCP connection
    → Create Epic ticket with PRD link
    → Set Epic metadata (labels, components)
    ✓ PROJ-123 Epic created

[3] Feature Decomposition
    → Analyze PRD and break into Stories
    → Prioritize Stories
    → Review breakdown with user
    ✓ 3 User Stories planned

[4] User Story Generation
    → For each Story:
      • Write clear description
      • Define Acceptance Criteria (Given-When-Then)
      • Set story points
      • Link to Epic
    ✓ PROJ-124, PROJ-125, PROJ-126 created

[5] Implementation Tasks
    → For each User Story:
      • Create backend/frontend/test tasks
      • Assign to team members
      • Set task relationships
    ✓ 9 Tasks created and assigned

[6] Progress Tracking
    → Monitor Task completion
    → Link PRs when tasks complete
    → Track deployment status
    → Close Epic when all done
```

## When to Use This Skill

### Perfect For:
- Starting new features or epics
- Sprint planning sessions
- Creating comprehensive Jira ticket structures
- Onboarding new features with full documentation
- Ensuring traceability from requirements to implementation

### Not Suitable For:
- Quick bug fixes (just create a ticket directly)
- Documentation-only tasks
- Simple one-off tasks that don't need decomposition

## Prerequisites

### Required Setup

**1. Jira MCP Server**

This skill requires a Jira MCP server. We recommend `@orengrinker/jira-mcp-server`.

See `SETUP.md` in this skill directory for complete installation guide.

Quick check if installed:
```bash
# Skill will automatically check and guide you if not set up
```

**2. Project Information**

You'll need to know:
- Jira Project Key (e.g., "PROJ")
- Project name
- Team member names for task assignment

## Interactive Workflow

When you invoke this skill, I'll guide you through a conversational process:

### Phase 1: PRD Creation

I'll ask you targeted questions to build a comprehensive PRD:

```
AI: Let's create a PRD for your feature. I'll ask some questions.

Q1: What problem are you solving?
    → User's pain point
    → Current workarounds
    → Who is affected

Q2: What are your success metrics?
    → How will you measure success?
    → Target KPIs (e.g., "30% faster checkout")
    → Timeline for measuring

Q3: Who are your users?
    → B2B or B2C?
    → Primary and secondary personas
    → Use cases

Q4: What's in scope for MVP?
    → Must-have features
    → Nice-to-have (future)
    → Explicit non-goals

Q5: Any constraints or dependencies?
    → Technical limitations
    → Timeline requirements
    → Team dependencies
```

**Output**: `docs/prd/{feature-name}-{date}.md`

### Phase 2: Jira Epic Creation

```
AI: Great! Now let's create a Jira Epic.

   PRD Summary:
   - Feature: OAuth Authentication
   - Goal: 30% reduction in signup friction
   - Scope: Google + GitHub OAuth

   I'll create an Epic ticket with:
   - Title: "OAuth Authentication Integration"
   - Description: [Summary from PRD]
   - PRD Link: docs/prd/oauth-authentication-2024-10.md
   - Labels: authentication, oauth
   - Project: PROJ

   Proceed? (Y/n)
```

**If Jira MCP not configured**: I'll provide setup instructions and pause.

**Output**: Epic ticket (e.g., `PROJ-123`)

### Phase 3: Feature Decomposition

```
AI: Let's break this Epic into User Stories.

   Based on your PRD, I suggest 3 Stories:

   Story 1: Google OAuth Integration
   - Implement Google OAuth 2.0 flow
   - User can sign up/login with Google
   - Priority: High
   - Estimate: 8 points

   Story 2: GitHub OAuth Integration
   - Implement GitHub OAuth flow
   - User can sign up/login with GitHub
   - Priority: High
   - Estimate: 5 points

   Story 3: Account Linking for Existing Users
   - Allow existing users to link OAuth accounts
   - Merge accounts on OAuth login
   - Priority: Medium
   - Estimate: 5 points

   Total: 18 story points

   Would you like to:
   - Adjust priorities?
   - Split/merge stories?
   - Add more stories?
   - Proceed as-is?
```

### Phase 4: User Story Generation

For each approved story:

```
AI: Creating Story 1/3: Google OAuth Integration

   User Story:
   As a new user
   I want to sign up using my Google account
   So that I can quickly create an account without filling forms

   Acceptance Criteria:
   AC-1: OAuth Flow
   Given a user on the signup page
   When they click "Sign up with Google"
   Then they should be redirected to Google OAuth consent screen
   And after approval, redirected back to the app
   And their account should be created with Google email

   AC-2: Login with Existing Google Account
   Given a user with a Google-linked account
   When they click "Login with Google" and approve
   Then they should be logged in automatically

   AC-3: Error Handling
   Given Google OAuth fails (user denies, network error)
   When the OAuth flow is interrupted
   Then the user should see a clear error message
   And be able to retry or use alternative signup

   Story Points: 8
   Link to Epic: PROJ-123

   Create this Story ticket? (Y/n)
```

**Output**: User Story tickets (e.g., `PROJ-124`, `PROJ-125`, `PROJ-126`)

### Phase 5: Implementation Tasks

For each User Story:

```
AI: Creating Tasks for Story PROJ-124: Google OAuth Integration

   Backend Tasks:
   PROJ-127: Set up Google OAuth credentials
   - Create Google Cloud project
   - Configure OAuth consent screen
   - Get client ID and secret
   Assigned to: [Backend dev name]
   Estimate: 2 hours

   PROJ-128: Implement OAuth callback endpoint
   - Create /auth/google/callback route
   - Exchange code for tokens
   - Create or link user account
   Assigned to: [Backend dev name]
   Estimate: 4 hours

   Frontend Tasks:
   PROJ-129: Add "Sign up with Google" button
   - Design button component
   - Integrate Google OAuth library
   - Handle redirect flow
   Assigned to: [Frontend dev name]
   Estimate: 2 hours

   PROJ-130: Error handling and loading states
   - Show loading during OAuth flow
   - Display error messages
   - Retry mechanism
   Assigned to: [Frontend dev name]
   Estimate: 2 hours

   QA Tasks:
   PROJ-131: Test Google OAuth flows
   - Test Case 1: Successful signup
   - Test Case 2: Successful login
   - Test Case 3: Error scenarios
   - Test Case 4: Account linking
   Assigned to: [QA name]
   Estimate: 3 hours

   Who should I assign these tasks to?
```

**Output**: Implementation Task tickets (e.g., `PROJ-127` through `PROJ-131`)

### Phase 6: Progress Tracking

```
AI: Epic PROJ-123 is now set up!

   📊 Summary:
   - Epic: PROJ-123 (OAuth Authentication)
   - User Stories: 3 (PROJ-124, 125, 126)
   - Implementation Tasks: 15
   - Total Estimate: 35 hours

   📁 Documentation:
   - PRD: docs/prd/oauth-authentication-2024-10.md
   - Technical Design: docs/tech-design/oauth-implementation.md

   🎯 Next Steps:
   1. Sprint Planning: Add Stories to sprint backlog
   2. Development: Team starts on Tasks
   3. Track progress: Use "/agile track PROJ-123"

   I'll monitor your tickets and notify you when:
   - Tasks are completed
   - PRs are created
   - Stories are ready for QA
   - Epic is ready to close
```

## Commands & Usage

### Starting a New Feature

```
User: /skill agile-master
      "I want to add two-factor authentication"

AI: [Starts Phase 1: PRD Creation]
```

### Tracking Progress

```
User: /skill agile-master
      "Track progress on PROJ-123"

AI: Fetching Epic PROJ-123 status...

   Epic: OAuth Authentication (PROJ-123)
   Status: In Progress (60% complete)

   ✅ Completed (2/3 Stories):
   - PROJ-124: Google OAuth Integration (Done)
   - PROJ-125: GitHub OAuth Integration (Done)

   🚧 In Progress (1/3 Stories):
   - PROJ-126: Account Linking (In Progress)
     ├─ PROJ-132: Backend API (Done)
     ├─ PROJ-133: Frontend UI (In Review)
     └─ PROJ-134: Testing (To Do)

   🔗 Recent Activity:
   - PR #456 merged (PROJ-132)
   - PR #457 pending review (PROJ-133)
```

### Sprint Planning

```
User: /skill agile-master
      "Plan sprint with PROJ-123 stories"

AI: Sprint Planning for OAuth Authentication Epic

   Available capacity: 40 hours
   Epic total estimate: 35 hours

   Recommended for Sprint:
   ✓ PROJ-124: Google OAuth (8 pts) - High priority
   ✓ PROJ-125: GitHub OAuth (5 pts) - High priority
   ✓ PROJ-126: Account Linking (5 pts) - Medium priority

   All stories fit in sprint. Add to sprint? (Y/n)
```

## Document Templates Generated

### 1. PRD Template

```markdown
# PRD: [Feature Name]

## Executive Summary
[One paragraph overview]

## Problem Statement
**Current Pain Point:**
[What problem exists today]

**Affected Users:**
[Who experiences this problem]

**Business Impact:**
[Why this matters to the business]

## Goals & Success Metrics
**Primary Goal:**
[Main objective]

**Success Metrics:**
- Metric 1: [e.g., 30% reduction in signup time]
- Metric 2: [e.g., 50% increase in signup conversion]

**Measurement Plan:**
[How and when we'll measure]

## User Personas & Use Cases
**Primary Persona:**
- Who: [User type]
- Pain Point: [Current problem]
- Goal: [Desired outcome]

**Use Cases:**
1. [Use case 1]
2. [Use case 2]

## Requirements

### Functional Requirements
- FR-1: System must allow...
- FR-2: Users can...

### Non-Functional Requirements
- Performance: [Response time targets]
- Security: [Security requirements]
- Scalability: [Scale expectations]

## Scope

### In Scope (MVP)
- Feature 1
- Feature 2

### Out of Scope (Future)
- Feature X (reason: ...)
- Feature Y (reason: ...)

## User Stories (High-Level)
1. As a [user], I want to [action], so that [benefit]
2. As a [user], I want to [action], so that [benefit]

## Technical Considerations
[High-level technical notes, dependencies]

## Timeline & Milestones
- Sprint 1: [Goals]
- Sprint 2: [Goals]

## Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk 1] | High | [How to mitigate] |

## Open Questions
- [ ] Question 1
- [ ] Question 2

## Appendix
[Mockups, research, references]
```

### 2. User Story Template (Jira)

```
Title: [User action in present tense]

Story:
As a [user type]
I want to [action]
So that [benefit/value]

Context:
[Why this story matters, link to PRD/Epic]

Acceptance Criteria:
□ AC-1: Given [context], when [action], then [outcome]
□ AC-2: Given [context], when [action], then [outcome]
□ AC-3: Edge case: [scenario] should [behavior]

Technical Notes:
- API changes: [Endpoints affected]
- Database: [Schema changes]
- Dependencies: [External dependencies]

Definition of Done:
□ Code complete
□ Unit tests (>80% coverage)
□ Code reviewed
□ QA testing passed
□ Documentation updated
□ Deployed to staging

Story Points: [1, 2, 3, 5, 8, 13]
Epic Link: [EPIC-KEY]
Labels: [relevant-labels]
```

### 3. Task Template (Jira)

```
Title: [Specific implementation task]

Description:
[What needs to be done]

Parent Story: [STORY-KEY]

Subtasks (if needed):
- [ ] Step 1
- [ ] Step 2

Acceptance Criteria:
□ [Specific done criteria]

Estimate: [Hours]
Assigned: [Developer name]
```

## Best Practices

### When Creating PRDs
1. **Ask clarifying questions** - Don't assume requirements
2. **Define metrics early** - How will you know it's successful?
3. **Keep scope realistic** - MVP mindset
4. **Link to user research** - Real user needs, not assumptions

### When Creating Stories
1. **Keep atomic** - One story = one vertical slice
2. **Make AC testable** - QA can verify without asking
3. **Include context** - Link to PRD for "why"
4. **Estimate realistically** - 1-8 points ideal (larger = split)

### When Creating Tasks
1. **Break down by discipline** - Backend, Frontend, QA, DevOps
2. **Make tasks < 1 day** - 2-6 hours ideal
3. **Clear ownership** - One assignee per task
4. **Dependencies explicit** - Block/blocked-by relationships

### Documentation
1. **Living documents** - Update PRD as you learn
2. **Link everything** - PRD ↔ Epic ↔ Story ↔ Task ↔ PR
3. **Version control** - Store PRDs in git
4. **Team access** - Ensure everyone can access docs

## Jira MCP Integration

This skill uses Jira MCP to:
- ✅ Create Epic tickets
- ✅ Create User Story tickets
- ✅ Create Task tickets (subtasks)
- ✅ Link tickets (Epic → Story, Story → Task)
- ✅ Assign tickets to team members
- ✅ Search tickets by JQL
- ✅ Update ticket status
- ✅ Add comments to tickets

### Available Jira Operations

```typescript
// Epic Creation
create_issue({
  project: "PROJ",
  issuetype: "Epic",
  summary: "Feature Name",
  description: "...",
  customFields: {
    epicName: "Feature Name"
  }
})

// User Story Creation
create_issue({
  project: "PROJ",
  issuetype: "Story",
  summary: "...",
  description: "...",
  epicLink: "PROJ-123",
  labels: ["authentication"]
})

// Task Creation
create_issue({
  project: "PROJ",
  issuetype: "Task",
  summary: "...",
  parent: "PROJ-124",
  assignee: "john.doe"
})

// Linking
link_issues({
  inwardIssue: "PROJ-124",
  outwardIssue: "PROJ-123",
  type: "relates to"
})

// Search
search_issues({
  jql: "project = PROJ AND epic = PROJ-123"
})
```

## Troubleshooting

### Jira MCP Not Connected

```
Error: Jira MCP server not available

Solution:
1. Check that Jira MCP is configured in your MCP settings
2. Verify your API token is valid
3. See SETUP.md for configuration guide
```

### Epic Creation Failed

```
Error: Cannot create Epic - custom field not found

Solution:
1. Verify your Jira project supports Epic issue type
2. Check that epic name custom field exists
3. Try creating a regular Issue type instead
```

### Story Points Not Showing

```
Issue: Story points field not available

Solution:
Story points may be a custom field in your Jira.
I'll ask for the custom field ID during setup.
```

## Advanced Features

### Custom Workflows

You can customize the workflow:

```
User: "Use our team's workflow: Epic → Feature → Task"

AI: Noted! I'll use:
   - Epic (instead of Epic)
   - Feature (instead of User Story)
   - Task (same)
```

### Integration with GitHub

```
User: "Link PRs to tasks automatically"

AI: I can add GitHub PR links to tasks when PRs are created.
   Set up GitHub MCP for automatic linking.
```

### Sprint Auto-Planning

```
User: "Auto-assign stories to next sprint"

AI: I'll analyze team velocity and automatically:
   - Calculate available capacity
   - Prioritize stories
   - Assign to sprint
   - Notify team
```

## Examples

### Example 1: Authentication Feature

```
User: /skill agile-master
      "Add social login - Google, GitHub, Twitter"

AI: [PRD Creation Phase]
   ... Q&A session ...

   [Epic Created: PROJ-200]

   [Stories Created]
   - PROJ-201: Google OAuth (8 pts)
   - PROJ-202: GitHub OAuth (5 pts)
   - PROJ-203: Twitter OAuth (5 pts)
   - PROJ-204: Account Linking (3 pts)

   [Tasks Created - 12 tasks total]

   ✅ Complete! Ready for sprint planning.
```

### Example 2: API Redesign

```
User: /skill agile-master
      "Redesign REST API to GraphQL"

AI: This is a large initiative. Let me help break it down.

   [PRD Created with migration strategy]

   [Epic: PROJ-300]

   [Stories - Migration Phases]
   - PROJ-301: GraphQL server setup (5 pts)
   - PROJ-302: User queries migration (8 pts)
   - PROJ-303: Product queries migration (8 pts)
   - PROJ-304: REST API deprecation (3 pts)

   Total: 24 pts over 3 sprints

   Proceed? (Y/n)
```

## Skill Invocation Modes

### Mode 1: Full Workflow (Default)

```
/skill agile-master
"Feature description here"
```

Runs all 6 phases interactively.

### Mode 2: PRD Only

```
/skill agile-master
"Just help me write a PRD for [feature]"
```

Stops after PRD creation.

### Mode 3: Jira Only

```
/skill agile-master
"Create Jira tickets from this PRD: [path]"
```

Skips PRD creation, creates Jira structure.

### Mode 4: Tracking

```
/skill agile-master
"Track PROJ-123"
```

Shows Epic progress and status.

## Configuration

The skill will prompt you for:
- Jira project key
- Default assignees for roles (Backend, Frontend, QA)
- Story point scale (Fibonacci or T-shirt sizes)
- Sprint length (weeks)

These preferences are saved for future use.

## Success Metrics

After using this skill, you'll have:
- ✅ Comprehensive PRD documenting "why"
- ✅ Jira Epic with clear ownership
- ✅ User Stories with testable AC
- ✅ Implementation Tasks assigned to team
- ✅ Complete traceability from PRD → Task
- ✅ Ready-to-start sprint backlog

## Next Steps After Completion

1. **Sprint Planning**: Review Story priorities with team
2. **Estimation Session**: Validate story points
3. **Design Review**: If UI changes, review mockups
4. **Technical Kickoff**: Review Technical Design with engineers
5. **QA Prep**: Share Test Plan with QA team
6. **Sprint Start**: Begin implementation

## References

- PRD Best Practices: [Product School](https://productschool.com)
- Agile User Stories: [Mike Cohn](https://www.mountaingoatsoftware.com)
- Jira Best Practices: [Atlassian Guides](https://www.atlassian.com/agile/project-management)

---

**Ready to transform your feature ideas into actionable, tracked, and documented work!**

To get started:
1. Ensure Jira MCP is configured (see SETUP.md)
2. Invoke this skill with your feature idea
3. Follow the interactive prompts
4. Watch your Jira fill with well-structured tickets!
