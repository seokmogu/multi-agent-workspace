# Agile Skills V2 - Role-Based Separation

**New Architecture**: 3 focused skills for Product → Stories → Jira workflow

**Replaced**: agile-master, agile-master-v2, agile-docs-framework
**Created**: 2024-10-23
**Pattern**: Skill-Creator + Playwright-skill (direct API calls)

---

## 🎯 The 3 Skills

### 1. 📝 agile-product (PM Role)

**Purpose**: Product Manager skill for writing comprehensive PRDs

**What It Does**:
- Interactive Q&A-driven PRD creation
- Business goals and success metrics
- User personas and use cases
- Functional/non-functional requirements
- Scope definition (in/out)

**Output**:
```
docs/prd/oauth-authentication-2024-10-23.md
```

**Usage**:
```bash
/skill agile-product "Add OAuth authentication"

→ Interactive Q&A session
→ PRD generated in docs/prd/
```

**Files**:
- `SKILL.md` (1,806 words - concise workflow)
- `references/prd-guide.md` (detailed guide)
- `references/prd-example.md` (complete example)

---

### 2. 👥 agile-stories (PO/Scrum Master Role)

**Purpose**: Product Owner skill for breaking down PRDs into User Stories

**What It Does**:
- Reads PRD files
- Identifies Epic structure
- Generates User Stories with AC (Given-When-Then)
- Estimates story points (Fibonacci)
- Creates Definition of Done

**Output**:
```
docs/stories/
├── oauth-google.md (5 points)
├── oauth-github.md (3 points)
└── account-linking.md (3 points)
```

**Usage**:
```bash
/skill agile-stories --prd=docs/prd/oauth-authentication-2024-10-23.md

→ Analyzes PRD
→ Generates 3 User Stories with AC
→ Total: 11 story points
```

**Files**:
- `SKILL.md` (2,089 words - workflow)
- `references/user-story-guide.md` (detailed AC examples)
- `references/story-template.md` (blank template)

---

### 3. 🎫 agile-jira (Developer/PM Role)

**Purpose**: Jira REST API integration for creating tickets

**What It Does**:
- **Reads User Story markdown files**
- **Creates Jira tickets directly** (no MCP server!)
- Creates Epic, Story, Task tickets
- Links Epic → Story → Task
- Tracks progress

**Output**:
```
Jira Tickets:
├── KAN-123 (Epic: OAuth Authentication)
├── KAN-124 (Story: Google OAuth)
├── KAN-125 (Story: GitHub OAuth)
└── KAN-126 (Story: Account Linking)
```

**Usage**:
```bash
# One-time setup
cd .claude/skills/agile-jira
cp .jira-config.example.json .jira-config.json
# Edit with your Jira credentials

# Import stories to Jira
/skill agile-jira --import docs/stories/

→ Creates Epic in Jira
→ Creates Story tickets (linked to Epic)
→ Returns ticket keys
```

**Files**:
- `SKILL.md` (4,291 words - comprehensive)
- `scripts/jira-api.js` ⭐ **Direct REST API calls**
- `.jira-config.example.json` (configuration template)

**No MCP Needed!**: Uses Node.js https module to call Jira REST API directly

---

## 🔄 Complete Workflow

### Step-by-Step Example

```bash
# ============================================
# STEP 1: Product Manager - Create PRD
# ============================================
/skill agile-product "Add OAuth authentication with Google and GitHub"

AI asks questions:
- Problem? "Users abandon signup at password step (45% dropout)"
- Success metric? "Increase signup completion 55% → 80%"
- Users? "New B2B trial users (1,200/month)"
...

→ Output: docs/prd/oauth-authentication-2024-10-23.md

# ============================================
# STEP 2: Team Review (Git PR)
# ============================================
git add docs/prd/
git commit -m "Add OAuth authentication PRD"
gh pr create --title "PRD: OAuth Authentication"

# Team reviews, PM approves, PR merged

# ============================================
# STEP 3: Product Owner - Create User Stories
# ============================================
/skill agile-stories --prd=docs/prd/oauth-authentication-2024-10-23.md

AI analyzes PRD and creates:
Story 1: Google OAuth Login (5 points)
Story 2: GitHub OAuth Login (3 points)
Story 3: Account Linking (3 points)

→ Output:
   docs/stories/oauth-google.md
   docs/stories/oauth-github.md
   docs/stories/account-linking.md

# ============================================
# STEP 4: Team Review (Git PR)
# ============================================
git add docs/stories/
git commit -m "Add user stories for OAuth"
gh pr create --title "User Stories: OAuth Authentication"

# Team reviews, refines estimates, approves

# ============================================
# STEP 5: Import to Jira
# ============================================
# One-time setup (if not done)
cd .claude/skills/agile-jira
cp .jira-config.example.json .jira-config.json
# Edit with Jira credentials

# Import
/skill agile-jira --import docs/stories/

→ Creating Epic: OAuth Authentication (KAN-123)
→ Creating Story: Google OAuth (KAN-124)
→ Creating Story: GitHub OAuth (KAN-125)
→ Creating Story: Account Linking (KAN-126)
✅ Created 4 tickets

# ============================================
# STEP 6: Sprint Planning (Jira UI)
# ============================================
# In Jira:
- Add stories to sprint backlog
- Assign to developers
- Start sprint

# ============================================
# STEP 7: Track Progress
# ============================================
/skill agile-jira --track KAN-123

→ Epic: OAuth Authentication (KAN-123)
  Progress: 2/3 stories complete (67%)
  ✅ Done: 2
  🚧 In Progress: 1
```

---

## 📦 File Structure

```
project-root/
├── .claude/
│   └── skills/
│       ├── agile-product/
│       │   ├── SKILL.md
│       │   └── references/
│       │       ├── prd-guide.md
│       │       ├── prd-example.md
│       │       └── prd-checklist.md
│       │
│       ├── agile-stories/
│       │   ├── SKILL.md
│       │   └── references/
│       │       ├── user-story-guide.md
│       │       ├── ac-examples.md
│       │       └── story-template.md
│       │
│       └── agile-jira/
│           ├── SKILL.md
│           ├── scripts/
│           │   └── jira-api.js ⭐ (Direct API)
│           └── .jira-config.example.json
│
├── docs/
│   ├── prd/                    ← PRDs stored here
│   │   └── oauth-authentication-2024-10-23.md
│   └── stories/                ← User Stories stored here
│       ├── oauth-google.md
│       ├── oauth-github.md
│       └── account-linking.md
│
├── .env                        ← (Optional) Jira config
└── .gitignore                  ← Ignores .jira-config.json
```

---

## 🔑 Key Differences from V1

### V1 (Old - Single Monolithic Skill)

```
agile-master (2.8k words)
├── PRD creation
├── Story breakdown
├── Jira integration (via MCP)
└── Everything in one file

Problems:
- Too many responsibilities
- Required MCP server
- Hard to use independently
- Confusing for team collaboration
```

### V2 (New - Role-Based Skills)

```
agile-product (1.8k words)
└── PRD creation only

agile-stories (2.1k words)
└── Story breakdown only

agile-jira (4.3k words + scripts)
└── Jira integration (no MCP!)

Benefits:
✅ Clear role separation (PM → PO → Dev)
✅ No MCP server needed (direct REST API)
✅ Can use skills independently
✅ Better team collaboration (Git PRs)
✅ Progressive disclosure (references/)
✅ Direct API control (scripts/)
```

---

## 🎨 Design Patterns Used

### 1. Skill-Creator Pattern (Progressive Disclosure)

```
SKILL.md (concise core)
└── references/ (detailed guides loaded when needed)
```

**Example**: agile-product
- SKILL.md: 1.8k words (workflow)
- references/prd-guide.md: 4.2k words (details)

**Benefit**: Loads only what's needed, saves context

### 2. Playwright-Skill Pattern (Direct API)

```
SKILL.md (workflow)
└── scripts/jira-api.js (direct Node.js REST calls)
```

**Example**: agile-jira
- No MCP server process
- Direct https.request() calls
- Self-contained in skill directory

**Benefit**: Simple setup, full control, easy debugging

### 3. Role-Based Separation

```
PM: agile-product (business focus)
PO: agile-stories (breakdown focus)
Dev: agile-jira (implementation focus)
```

**Benefit**: Each role uses what they need

---

## 🔧 Jira Configuration

### Three Ways to Configure

#### Option 1: Environment Variables (Recommended for CI/CD)

```bash
export JIRA_BASE_URL="https://nexusprj.atlassian.net"
export JIRA_EMAIL="seokmogu@gmail.com"
export JIRA_API_TOKEN="your-token"
export JIRA_PROJECT_KEY="KAN"
```

#### Option 2: .jira-config.json (Recommended for Local)

```bash
cd .claude/skills/agile-jira
cp .jira-config.example.json .jira-config.json

# Edit .jira-config.json:
{
  "baseUrl": "https://nexusprj.atlassian.net",
  "email": "seokmogu@gmail.com",
  "apiToken": "your-token",
  "projectKey": "KAN"
}
```

**Note**: `.jira-config.json` is in `.gitignore` (security!)

#### Option 3: Project .env

```bash
# In project root .env
JIRA_BASE_URL=https://nexusprj.atlassian.net
JIRA_EMAIL=seokmogu@gmail.com
JIRA_API_TOKEN=your-token
JIRA_PROJECT_KEY=KAN
```

### Get API Token

1. https://id.atlassian.com/manage-profile/security/api-tokens
2. Create API token
3. Copy (won't see it again!)

---

## 📊 Comparison Table

| Feature | V1 (agile-master) | V2 (3 skills) |
|---------|-------------------|---------------|
| **Skills** | 1 monolithic | 3 focused |
| **PRD Creation** | ✅ | ✅ agile-product |
| **Story Breakdown** | ✅ | ✅ agile-stories |
| **Jira Integration** | ✅ (via MCP) | ✅ agile-jira (direct API) |
| **MCP Server Required** | ✅ Yes | ❌ No |
| **Setup Complexity** | High | Low |
| **Role Clarity** | Unclear | Clear (PM/PO/Dev) |
| **Git Collaboration** | Difficult | Easy (PRs per step) |
| **Context Efficiency** | 2.8k always loaded | 1.8k-4.3k as needed |
| **API Control** | Via MCP abstraction | Direct control (scripts/) |
| **Debugging** | Hard (MCP layer) | Easy (direct logs) |
| **Team Adoption** | Confusing | Intuitive |

---

## 🚀 Getting Started

### Quick Start (5 minutes)

```bash
# 1. Create PRD
/skill agile-product "your feature idea"

# 2. Create Stories
/skill agile-stories --prd=docs/prd/your-feature.md

# 3. Setup Jira (one-time)
cd .claude/skills/agile-jira
cp .jira-config.example.json .jira-config.json
# Edit with your Jira details

# 4. Import to Jira
/skill agile-jira --import docs/stories/

# Done! Check your Jira
```

### Full Team Workflow

```bash
# PM: Create PRD
/skill agile-product "feature"
git add docs/prd/ && git commit -m "Add PRD"
gh pr create  # Team reviews

# PO: Create Stories (after PRD approved)
/skill agile-stories --prd=docs/prd/feature.md
git add docs/stories/ && git commit -m "Add stories"
gh pr create  # Team reviews estimates

# Dev/PM: Import to Jira (after stories approved)
/skill agile-jira --import docs/stories/

# Sprint Planning in Jira
# Development starts
# Track progress:
/skill agile-jira --track KAN-123
```

---

## 🎯 Benefits

### For Product Managers

- ✅ Focus on PRD quality (agile-product)
- ✅ Clear structure and prompts
- ✅ Best practices built-in

### For Product Owners

- ✅ Consistent story format (agile-stories)
- ✅ Given-When-Then AC
- ✅ Fibonacci estimation

### For Developers

- ✅ No MCP setup needed (agile-jira)
- ✅ Direct API control
- ✅ Easy debugging (plain Node.js)

### For Teams

- ✅ Git workflow (PRs at each step)
- ✅ Role clarity (who does what)
- ✅ Audit trail (all docs in git)
- ✅ Version control (see evolution)

---

## 📝 Example Documents

### PRD Example (docs/prd/oauth-authentication-2024-10-23.md)

```markdown
# PRD: OAuth Authentication

## Executive Summary
Add Google and GitHub OAuth to reduce signup friction by 30%...

## Problem Statement
45% of users abandon signup at password creation step...

## Goals & Success Metrics
- Primary Goal: Increase signup completion 55% → 80%
- Metric 1: Signup time: 3.2min → <1min
- Metric 2: OAuth adoption: ≥60% of new signups

[... full PRD ...]
```

### User Story Example (docs/stories/oauth-google.md)

```markdown
# User Story: Login with Google OAuth

**Epic**: OAuth Authentication
**PRD**: docs/prd/oauth-authentication-2024-10-23.md

## Story

As a new user
I want to sign up using my Google account
So that I can start using the app in under 30 seconds

## Acceptance Criteria

### AC-1: Successful OAuth Flow
**Given** a user on signup page
**When** they click "Sign up with Google"
**And** approve OAuth consent
**Then** account is created with Google email
**And** they are redirected to dashboard

[... full story with all AC ...]

## Story Points

**5 points** (2-3 days)
```

---

## 🔍 Troubleshooting

### "Jira configuration not found"

**Check priority order**:
1. Environment variables (`echo $JIRA_BASE_URL`)
2. `.jira-config.json` (`ls .claude/skills/agile-jira/.jira-config.json`)
3. Project `.env` (`grep JIRA_ .env`)

### "Authentication failed (401)"

- Verify API token is correct
- Check email matches Atlassian account
- Regenerate token if needed

### "Cannot create Epic (field not found)"

Jira Cloud uses `customfield_10011` for Epic Name.
Edit `scripts/jira-api.js` if your Jira uses different field ID.

### "Story Points not saving"

Find your Story Points field ID:
```bash
curl -u email:token \
  https://your-domain.atlassian.net/rest/api/3/field \
  | grep -i "story points"
```

Update `customfield_10016` in `scripts/jira-api.js` with correct ID.

---

## 🎓 Best Practices

### 1. Always Use Git PRs

```bash
# After each step, create PR for team review
git add docs/prd/ && git commit && gh pr create
```

### 2. Review Before Jira Import

```bash
# Never import without team approval
# Stories should be reviewed and refined first
```

### 3. Keep Docs in Sync

```bash
# Even after Jira import, keep markdown files
# They serve as documentation and audit trail
```

### 4. One Epic at a Time

```bash
# Don't mix multiple features in one import
# Keep Epic scope focused
```

### 5. Secure Your Tokens

```bash
# Never commit .jira-config.json
# Rotate API tokens quarterly
# Use separate tokens per project
```

---

## 📚 References

- **agile-product/references/** - PRD writing guides
- **agile-stories/references/** - User Story guides
- **Jira REST API v3**: https://developer.atlassian.com/cloud/jira/platform/rest/v3/
- **Skill-Creator**: `.claude/skills/skill-creator/SKILL.md`
- **Playwright-Skill**: `.claude/skills/playwright-skill/` (pattern reference)

---

**Total Skills**: 3
**Total Lines of Code**: ~600 (jira-api.js)
**MCP Servers Required**: 0
**Setup Time**: 5 minutes
**Team-Ready**: ✅

**Next**: Try it out with a real feature!
