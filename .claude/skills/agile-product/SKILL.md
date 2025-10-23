---
name: agile-product
description: Product Manager skill for writing comprehensive PRDs (Product Requirements Documents). Interactive Q&A-driven PRD creation with business goals, success metrics, user stories, and scope definition. Use when starting new features, defining product requirements, or creating feature specifications. Outputs PRD as Markdown in docs/prd/.
allowed-tools: Write, Read, AskUserQuestion, Bash
version: 1.0.0
---

# Agile Product (PRD Writing)

Product Manager's assistant for creating comprehensive Product Requirements Documents through interactive guided workflow.

## Quick Start

```
User: /skill agile-product "Add OAuth authentication"

AI: Let's create a PRD. I'll ask some key questions...

Q1: What problem are you solving?
Q2: Who are your users?
Q3: What are success metrics?
...

→ PRD created: docs/prd/oauth-authentication-2024-10-23.md
→ Ready for team review!
```

## When to Use

Use this skill when:
- **Starting new features** requiring product definition
- **Defining product requirements** before development
- **Creating feature specifications** for stakeholder alignment
- **Documenting product decisions** for team clarity

Skip this skill for:
- Bug fixes (too small)
- Simple code refactoring
- Documentation-only changes

## How It Works

### Step 1: Feature Context

I'll ask you about your feature idea:
- What are you building?
- Why are you building it?
- What's the business case?

### Step 2: Problem Definition

Guided questions to define:
- Current pain points (with data)
- Affected users (who and how many)
- Business impact (cost of NOT solving)
- Evidence (user research, metrics)

### Step 3: Goals & Metrics

Define measurable success:
- Primary goal (single objective)
- Success metrics (2-4 KPIs with targets)
- Measurement plan (how and when)

### Step 4: User Personas & Use Cases

Identify:
- Primary and secondary users
- Pain points and goals
- User journeys and scenarios

### Step 5: Requirements

Document:
- Functional requirements (FR-1, FR-2, etc.)
- Non-functional requirements (performance, security, etc.)
- Must-have vs nice-to-have

### Step 6: Scope Definition

Explicitly define:
- **In Scope**: MVP features
- **Out of Scope**: Future features (with reasons)
- Dependencies and constraints

### Step 7: Timeline & Risks

Plan:
- Milestones and timeline
- Identified risks with mitigations
- Open questions needing decisions

### Step 8: Generate PRD

Output PRD to: `docs/prd/{feature-name}-{date}.md`

## Output Structure

```
docs/
└── prd/
    └── oauth-authentication-2024-10-23.md
```

**PRD Contents**:
1. Executive Summary
2. Problem Statement
3. Goals & Success Metrics
4. User Personas & Use Cases
5. Requirements (Functional + Non-Functional)
6. Scope (In/Out)
7. User Stories (High-Level)
8. Timeline & Milestones
9. Risks & Mitigations
10. Open Questions
11. Appendix

## Example PRD

See `references/prd-example.md` for a complete example.

## Usage Modes

### Interactive Mode (Default)

```
/skill agile-product "feature description"

→ I'll ask questions and build PRD together
→ Review each section before moving forward
```

### Quick Mode (With Context)

```
/skill agile-product --quick "feature description" \
  --problem="users abandon signup at password step" \
  --metric="increase signup rate from 55% to 80%" \
  --users="new B2B trial users"

→ I'll generate PRD with provided context
→ You review and refine
```

### Update Mode

```
/skill agile-product --update docs/prd/existing-prd.md

→ I'll help you update an existing PRD
```

## Best Practices

### Do's ✅

1. **Start with "Why"** - Business case before solution
2. **Use Data** - "45% abandon signup" not "users complain"
3. **Measurable Goals** - "30% improvement" not "better UX"
4. **Real Examples** - Actual user scenarios
5. **Define Success** - How will you know it worked?

### Don'ts ❌

1. **Don't solution too early** - Problem first, solution second
2. **Don't skip "why"** - If you can't explain why, reconsider
3. **Don't be vague** - Specific requirements only
4. **Don't forget users** - Engineering-first PRDs fail
5. **Don't write and forget** - PRD is living document

## Next Steps

After PRD creation:

1. **Team Review** - Share PRD for feedback (Git PR)
2. **Stakeholder Approval** - PM, Engineering, Design sign-off
3. **User Story Breakdown** - Use `/skill agile-stories`
4. **Technical Design** - Engineering creates TDD
5. **Sprint Planning** - Add stories to backlog

## Integration

### With Other Skills

**agile-product** (this skill):
- Creates PRD in `docs/prd/`

↓

**agile-stories**:
- Reads PRD
- Generates User Stories in `docs/stories/`

↓

**agile-jira**:
- Creates Jira tickets from Stories

### Workflow

```bash
# 1. Create PRD
/skill agile-product "OAuth authentication"

# 2. Review PRD
git add docs/prd/
git commit -m "Add OAuth PRD"
gh pr create --title "PRD: OAuth Authentication"

# 3. After approval, create stories
/skill agile-stories --prd=docs/prd/oauth-authentication-2024-10-23.md

# 4. Create Jira tickets
/skill agile-jira --import=docs/stories/
```

## Reference

For detailed PRD writing guidance, see:
- `references/prd-guide.md` - Complete PRD structure guide
- `references/prd-example.md` - Full example PRD
- `references/prd-checklist.md` - Review checklist

## Troubleshooting

**Issue**: "I don't know the success metrics yet"

**Solution**: That's a red flag! If you can't define success, you're not ready to build. Do user research first.

**Issue**: "Requirements keep changing"

**Solution**: PRD is a living document. Update it as you learn. Version control in Git shows evolution.

**Issue**: "PRD is too long (>10 pages)"

**Solution**: You might be solving too many problems. Consider splitting into multiple PRDs/features.

## Tips

1. **Write for Future You** - 6 months from now, will you understand why?
2. **Link Evidence** - User research, analytics, competitive analysis
3. **Be Specific** - "30% faster" not "improve performance"
4. **Invite Collaboration** - Mark open questions, request feedback
5. **Keep Updated** - Update PRD as decisions are made

---

**Ready to create product requirements that drive successful features!**

Start with: `/skill agile-product "your feature description"`
