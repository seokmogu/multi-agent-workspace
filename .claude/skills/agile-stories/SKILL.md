---
name: agile-stories
description: Product Owner skill for breaking down PRDs into User Stories with Acceptance Criteria. Reads PRD, generates Epic structure, creates detailed User Stories with Given-When-Then AC, estimates story points. Use when converting PRD to implementable stories, sprint planning, or backlog grooming. Outputs stories as Markdown in docs/stories/.
allowed-tools: Write, Read, AskUserQuestion, Bash
version: 1.0.0
---

# Agile Stories (User Story Breakdown)

Product Owner's assistant for decomposing PRDs into well-structured User Stories with testable Acceptance Criteria.

## Quick Start

```
User: /skill agile-stories --prd=docs/prd/oauth-authentication-2024-10-23.md

AI: Analyzing PRD...

Found 3 main features:
1. Google OAuth
2. GitHub OAuth
3. Account Linking

→ Creating 3 User Stories with AC...
→ docs/stories/oauth-google.md
→ docs/stories/oauth-github.md
→ docs/stories/account-linking.md

Total: 18 story points
Ready for sprint planning!
```

## When to Use

Use this skill when:
- **After PRD approval** converting requirements to stories
- **Sprint planning** preparing backlog
- **Backlog grooming** refining story details
- **Epic breakdown** splitting large features

Skip this skill for:
- Writing PRDs (use agile-product)
- Creating Jira tickets (use agile-jira)
- Bug tracking (too small for story breakdown)

## How It Works

### Step 1: Read PRD

```bash
/skill agile-stories --prd=docs/prd/feature-name.md
```

I'll analyze:
- Requirements (Functional + Non-functional)
- High-level user stories
- Scope and constraints

### Step 2: Identify Epic Structure

Propose Epic breakdown:
```
Epic: OAuth Authentication
├── Story 1: Google OAuth Login
├── Story 2: GitHub OAuth Login
└── Story 3: Account Linking
```

You can adjust before proceeding.

### Step 3: Generate User Stories

For each story, create:

**User Story Format**:
```
As a [user type]
I want to [action]
So that [benefit]
```

**Acceptance Criteria** (Given-When-Then):
```
AC-1: Successful Login
Given a user with valid Google account
When they click "Login with Google"
Then they are redirected to dashboard
And session is active for 24 hours

AC-2: Failed Login
Given OAuth provider unavailable
When user attempts login
Then error message displayed
And option to retry provided
```

### Step 4: Estimate Story Points

Using Fibonacci scale (1, 2, 3, 5, 8, 13):
- 1-2: Simple (few hours to half day)
- 3-5: Moderate (1-2 days)
- 8: Complex (3-5 days)
- 13+: Too large, split it!

### Step 5: Output Stories

Generate Markdown files:
```
docs/stories/
├── oauth-google.md
├── oauth-github.md
└── account-linking.md
```

Each file contains:
- User Story
- Context (link to PRD)
- Acceptance Criteria (detailed)
- Story Points
- Technical Notes
- Definition of Done

## Output Structure

```
docs/
├── prd/
│   └── oauth-authentication-2024-10-23.md (input)
└── stories/
    ├── oauth-google.md (output)
    ├── oauth-github.md (output)
    └── account-linking.md (output)
```

## Story File Format

```markdown
# User Story: Login with Google OAuth

**Epic**: OAuth Authentication
**PRD**: docs/prd/oauth-authentication-2024-10-23.md

## Story

As a new user
I want to sign up using my Google account
So that I can start using the app in under 30 seconds without creating a password

## Context

Users abandon signup at password creation step (45% dropout rate).
OAuth reduces friction and increases conversion.

## Acceptance Criteria

### AC-1: Successful OAuth Flow
**Given** a user on signup page
**When** they click "Sign up with Google"
**And** approve OAuth consent
**Then** they are redirected to dashboard
**And** account is created with Google email
**And** profile includes name and picture from Google

### AC-2: OAuth Failure Handling
**Given** user denies OAuth consent
**When** they return to app
**Then** error message is shown: "Google login cancelled"
**And** option to retry or use email/password is provided

### AC-3: Duplicate Account Prevention
**Given** email already exists in system
**When** user signs up with Google using same email
**Then** prompt to link accounts is shown
**And** if confirmed, accounts are linked

## Technical Notes

- API: POST /auth/google/callback
- Database: Add oauth_provider field to users table
- Security: Implement CSRF protection with state parameter

## Definition of Done

- [ ] Code complete and reviewed
- [ ] Unit tests (>80% coverage)
- [ ] Integration tests for OAuth flow
- [ ] QA tested all AC
- [ ] Security review passed
- [ ] Deployed to staging

## Story Points

**5 points** (2-3 days)

**Breakdown**:
- Backend OAuth flow: 3 points
- Frontend integration: 1 point
- Testing: 1 point

## Labels

oauth, authentication, backend, frontend
```

## Story Sizing Guide

| Points | Complexity | Time | Example |
|--------|------------|------|---------|
| 1 | Trivial | 1-2 hours | Config change |
| 2 | Simple | Half day | Add form field |
| 3 | Moderate | 1 day | Simple API endpoint |
| 5 | Standard | 2-3 days | OAuth integration |
| 8 | Complex | 1 week | Account migration |
| 13 | Too Large | 2 weeks | **Split it!** |

### When to Split Stories

If story is >8 points, consider splitting:

**Bad** (13 points):
- "Implement complete OAuth system"

**Good** (3 stories of 5, 3, 3 points):
1. "Google OAuth login" (5 pts)
2. "GitHub OAuth login" (3 pts)
3. "Account linking" (3 pts)

## Usage Modes

### From PRD (Default)

```bash
/skill agile-stories --prd=docs/prd/feature.md
```

### From Description

```bash
/skill agile-stories "Add OAuth login with Google and GitHub"
```

I'll ask questions to clarify before creating stories.

### Update Existing Stories

```bash
/skill agile-stories --update docs/stories/oauth-google.md
```

### Generate Epic Summary

```bash
/skill agile-stories --epic-only --prd=docs/prd/feature.md
```

Creates Epic structure without detailed stories.

## Best Practices

### Good User Stories (INVEST)

- **I**ndependent - Can be developed separately
- **N**egotiable - Details can be refined
- **V**aluable - Delivers user value
- **E**stimable - Can estimate effort
- **S**mall - Completable in one sprint
- **T**estable - Clear AC for verification

### Writing AC

**Good** ✅:
```
Given a user clicks "Forgot Password"
When they enter email "john@example.com"
Then reset email sent within 5 minutes
And link expires in 24 hours
```

**Bad** ❌:
```
- User can reset password
- Email is sent
```

### Story Points

**Estimate based on**:
- Complexity (not just time)
- Unknowns and risks
- Testing effort
- Team experience with similar work

**Don't**:
- Convert to exact hours (use ranges)
- Compare across teams (each team's scale differs)
- Change estimates after starting (it's not actuals)

## Next Steps

After story creation:

1. **Review Stories** - Team refines AC and estimates
2. **Sprint Planning** - Select stories for sprint
3. **Create Jira Tickets** - Use `/skill agile-jira`
4. **Technical Design** - For complex stories (>5 points)
5. **Start Development** - Assign and begin work

## Integration

### Workflow

```bash
# 1. PRD exists
ls docs/prd/oauth-authentication-2024-10-23.md

# 2. Generate stories
/skill agile-stories --prd=docs/prd/oauth-authentication-2024-10-23.md

# 3. Review stories
git add docs/stories/
git commit -m "Add user stories for OAuth"
gh pr create --title "User Stories: OAuth Authentication"

# 4. After approval, create Jira tickets
/skill agile-jira --import=docs/stories/
```

### With Other Skills

**agile-product** → PRD
↓
**agile-stories** (this skill) → User Stories
↓
**agile-jira** → Jira Tickets

## Reference

For detailed guidance:
- `references/user-story-guide.md` - Complete guide
- `references/ac-examples.md` - AC examples
- `references/story-template.md` - Blank template

## Troubleshooting

**Issue**: "Story seems too large (13+ points)"

**Solution**: Split it! Break by:
- Backend vs Frontend
- Different user flows
- Different providers/integrations
- MVP vs nice-to-have

**Issue**: "Can't write clear AC"

**Solution**: That's a sign the story is too vague. Ask:
- What exactly should happen?
- How will QA verify it?
- What are edge cases?

**Issue**: "Team can't agree on estimates"

**Solution**: Use Planning Poker. Discuss outliers. Re-estimate after clarification.

## Tips

1. **One Story = One Value** - Should deliver user value independently
2. **AC = Test Cases** - QA should test without asking questions
3. **Keep < 8 Points** - Larger stories are risky and unclear
4. **Link to PRD** - Always show "why" this story matters
5. **Include Examples** - Real user scenarios in AC

---

**Ready to break down product requirements into actionable stories!**

Start with: `/skill agile-stories --prd=docs/prd/your-feature.md`
