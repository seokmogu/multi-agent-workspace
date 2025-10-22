---
name: Agile Documentation Framework
description: Establish comprehensive documentation structure for agile squads including PRD, Technical Design, User Stories, Acceptance Criteria, and QA frameworks. Use this when setting up documentation for new features, establishing team documentation standards, or when team members need guidance on what documents to create and how they connect. Optimized for product development with continuous delivery and quality assurance integration.
allowed-tools: Write, Edit, Read, Glob, AskUserQuestion
---

# Agile Documentation Framework

This skill helps you establish a professional, end-to-end documentation structure for agile development teams. It covers the complete flow from product requirements through technical implementation to QA validation.

## When to Use This Skill

- Setting up documentation for a new feature or epic
- Establishing team documentation standards and templates
- Onboarding new team members to documentation practices
- Ensuring traceability from requirements to implementation to testing
- Creating QA-ready documentation with clear acceptance criteria
- Building documentation that maintains context and purpose across sprints

## Documentation Hierarchy

```
PRD (Product Requirements Document)
  └─ Why are we building this? Business value, user needs, success metrics
      │
      ├─ Technical Design Document
      │   └─ How will we build it? Architecture, APIs, data models, alternatives
      │
      ├─ Epic / Feature Breakdown
      │   └─ What are the major components?
      │       │
      │       └─ User Stories (Tickets)
      │           ├─ What specific functionality?
      │           ├─ Acceptance Criteria (AC)
      │           │   └─ How do we verify it works? (QA testable)
      │           ├─ Technical Approach (for complex stories)
      │           │   └─ Implementation notes, API changes, impact
      │           └─ Definition of Done
      │               └─ Code review, tests, QA approved, deployed
      │
      └─ Test Plan / Test Cases
          └─ How does QA validate the entire feature?
```

## Core Documents

### 1. PRD (Product Requirements Document)

**Purpose**: Define WHAT we're building and WHY
**Owner**: Product Manager
**Audience**: Entire squad (PM, Engineering, Design, QA)
**When**: Before epic/feature kickoff

**Key Sections**:

```markdown
# PRD: [Feature Name]

## Executive Summary
- One paragraph: what this is and why it matters

## Problem Statement
- What user problem are we solving?
- What pain points exist today?
- Who is affected?

## Goals & Success Metrics
- Business objectives
- User outcomes
- Measurable KPIs (e.g., "Reduce checkout time by 30%")

## User Personas & Use Cases
- Who will use this?
- Primary and secondary use cases
- User journeys

## Scope
### In Scope
- What features are included
- MVP requirements

### Out of Scope
- What we're NOT doing (and why)
- Future considerations

## Requirements
### Functional Requirements
- FR-1: System must allow users to...
- FR-2: Users can...

### Non-Functional Requirements
- Performance targets (response time, throughput)
- Security requirements
- Scalability expectations
- Compliance needs

## User Stories (High-Level)
- Epic-level stories that will be broken down into tickets

## Dependencies & Constraints
- Technical dependencies
- Team dependencies
- Timeline constraints
- Budget constraints

## Risks & Mitigations
- What could go wrong?
- How do we mitigate each risk?

## Timeline & Milestones
- Key dates
- Release plan

## Open Questions
- Decisions still needed
- Areas requiring more research

## Appendix
- Mockups, wireframes
- Market research
- Competitive analysis
```

### 2. Technical Design Document (TDD)

**Purpose**: Define HOW we'll build it
**Owner**: Engineering Lead / Architect
**Audience**: Engineering team, with PM/QA awareness
**When**: After PRD approval, before sprint planning

**Key Sections**:

```markdown
# Technical Design: [Feature Name]

## Overview
- Brief summary of what we're building
- Link to PRD

## Goals & Non-Goals
### Goals
- Technical objectives
- Performance targets

### Non-Goals
- What we're explicitly not solving

## Current State
- Existing architecture relevant to this feature
- Current limitations or tech debt

## Proposed Solution

### Architecture Overview
- High-level system diagram
- Component interactions
- Data flow

### API Design
```
# New Endpoints
POST /api/v1/resource
GET /api/v1/resource/{id}

# Request/Response schemas
{
  "field": "type",
  "description": "purpose"
}
```

### Data Model Changes
```sql
-- New tables or schema changes
CREATE TABLE resource (
  id UUID PRIMARY KEY,
  ...
);
```

### Key Components
- Component A: Responsibility
- Component B: Responsibility
- How they interact

### Security Considerations
- Authentication/authorization changes
- Data protection
- Potential vulnerabilities

### Performance Considerations
- Expected load
- Caching strategy
- Database query optimization

### Scalability
- How does this scale?
- Bottlenecks and mitigation

## Alternative Approaches Considered

### Alternative 1: [Approach Name]
- Pros: ...
- Cons: ...
- Why rejected: ...

### Alternative 2: [Approach Name]
- Pros: ...
- Cons: ...
- Why rejected: ...

## Implementation Plan

### Phase 1: Foundation
- [ ] Task 1
- [ ] Task 2

### Phase 2: Core Features
- [ ] Task 3
- [ ] Task 4

### Phase 3: Polish & Optimization
- [ ] Task 5

## Testing Strategy
- Unit testing approach
- Integration testing needs
- Performance testing plan
- Test data requirements

## Migration & Rollout
- Deployment steps
- Feature flags
- Rollback plan
- Monitoring & alerting

## Dependencies
- External services
- Other team deliverables
- Infrastructure requirements

## Risks & Mitigation
- Technical risks
- How we'll address each

## Timeline Estimate
- Estimated effort per phase
- Critical path items

## Open Questions
- Technical decisions still needed
- Research required

## References
- Relevant documentation
- Similar implementations
- External resources
```

### 3. User Story (Ticket)

**Purpose**: Specific, implementable unit of work
**Owner**: Product Manager (with engineering input)
**Audience**: Developer implementing, QA testing
**When**: Sprint planning

**Template**:

```markdown
# [TICKET-123] User Story Title

## User Story
As a [user type]
I want to [action]
So that [benefit/value]

## Context
Why this story matters. Link to PRD/Epic.

## Acceptance Criteria (AC)
- [ ] AC-1: Given [context], when [action], then [expected outcome]
- [ ] AC-2: Given [context], when [action], then [expected outcome]
- [ ] AC-3: Edge case: [scenario] should [behavior]

## Technical Approach (for complex stories)
Brief implementation notes:
- API endpoints affected: POST /api/v1/...
- Database changes: Add field `status` to `orders` table
- Impact: Requires cache invalidation for...

## Definition of Done
- [ ] Code complete
- [ ] Unit tests written (>80% coverage)
- [ ] Code reviewed and approved
- [ ] QA testing completed
- [ ] Documentation updated
- [ ] Deployed to staging
- [ ] PM approved

## Test Scenarios (for QA)
1. Happy path: User does X, system responds with Y
2. Edge case: User does Z, system handles gracefully
3. Negative case: Invalid input X returns error Y

## Dependencies
- Blocked by: [TICKET-122]
- Blocks: [TICKET-124]

## Estimates
Story Points: 5

## Design / Mockups
[Attach or link to design assets]
```

### 4. Acceptance Criteria (AC) Guidelines

**Purpose**: Define testable conditions for "done"
**Format**: Given-When-Then (Gherkin style)

**Good AC Example**:
```markdown
## Acceptance Criteria

### AC-1: User Login Success
Given a user with valid credentials
When they enter username "john@example.com" and password "correct123"
Then they should be redirected to the dashboard
And they should see "Welcome, John" message

### AC-2: User Login Failure
Given a user enters invalid credentials
When they submit the login form
Then they should see error message "Invalid username or password"
And they should remain on the login page
And the password field should be cleared

### AC-3: Password Reset Link
Given a user clicks "Forgot Password"
When they enter their email "john@example.com"
Then they should receive a password reset email within 5 minutes
And the email should contain a valid reset link that expires in 24 hours
```

**Bad AC Example** (too vague):
```markdown
- User should be able to login
- Error messages should be shown
- Password reset should work
```

### 5. Test Plan / Test Cases

**Purpose**: Comprehensive QA validation strategy
**Owner**: QA Lead
**Audience**: QA team, Engineering (for test automation)
**When**: During/after development, before release

**Template**:

```markdown
# Test Plan: [Feature Name]

## Test Summary
- Feature: [Name]
- PRD: [Link]
- Test Owner: [Name]
- Test Timeline: [Dates]

## Scope

### In Scope
- Functional testing of user stories [TICKET-123, TICKET-124]
- Integration testing with [System X]
- Regression testing of [Related Features]

### Out of Scope
- Performance testing (separate test plan)
- Security testing (handled by security team)

## Test Environment
- Environment: Staging
- Test Data: [Source/setup instructions]
- Test Accounts: [Credentials location]

## Test Cases

### TC-1: User Registration Flow
**Priority**: High
**Prerequisites**:
- User not already registered
- Email service is operational

**Steps**:
1. Navigate to /register
2. Enter valid email "test@example.com"
3. Enter valid password "Test123!@#"
4. Click "Register"

**Expected Result**:
- User account created in database
- Confirmation email sent
- User redirected to email verification page

**AC Mapping**: AC-1, AC-2 from [TICKET-123]

---

### TC-2: Email Verification
**Priority**: High
**Prerequisites**: TC-1 completed

**Steps**:
1. Open verification email
2. Click verification link
3. Observe result

**Expected Result**:
- User account status changed to "verified"
- User redirected to login page
- Success message displayed

**AC Mapping**: AC-3 from [TICKET-123]

---

### TC-3: Registration with Existing Email (Negative)
**Priority**: Medium
**Prerequisites**: User "test@example.com" already exists

**Steps**:
1. Navigate to /register
2. Enter existing email "test@example.com"
3. Click "Register"

**Expected Result**:
- Error message: "Email already registered"
- User remains on registration page
- No duplicate account created

**AC Mapping**: AC-4 from [TICKET-123]

## Regression Test Cases
- [ ] Existing login flow still works
- [ ] Password reset unchanged
- [ ] User profile features unaffected

## Test Metrics
- Total Test Cases: 15
- Automated: 10
- Manual: 5
- Pass Criteria: 100% of critical tests pass, 95% overall

## Risks
- Risk 1: Email service downtime affects TC-1, TC-2
- Mitigation: Test with email service stub

## Sign-off
- [ ] QA Lead approval
- [ ] Engineering verification
- [ ] PM acceptance
```

## Agile Squad Workflow

### Sprint 0 / Planning Phase
1. **PM creates PRD** → Squad reviews and approves
2. **Engineering creates TDD** → Technical review and approval
3. **Squad breaks down into Epics/Stories** → Backlog grooming

### Sprint N / Execution Phase
1. **Developer picks story** → Marks in progress
2. **Developer reads AC** → Understands what to build and how it will be tested
3. **Developer implements** → Follows technical approach
4. **Developer creates PR** → References story, explains implementation
5. **Code review** → Engineering approval
6. **QA tests against AC** → Uses test cases from story
7. **PM validates** → Confirms meets PRD goals
8. **Story marked done** → Moves to done column

### Sprint Review / Retrospective
1. **Demo completed stories** → Show against PRD goals
2. **Review documentation** → Update outdated docs
3. **Identify doc debt** → Add to backlog

## PR Template for Context Continuity

```markdown
# PR: [Feature/Fix Name]

## Related Tickets
- Closes: [TICKET-123]
- Related: [TICKET-124]
- PRD: [Link]

## What / Why
Brief description of what this PR does and why.

Link to original user story/AC.

## How
Implementation approach:
- Changed X to use Y
- Added new endpoint Z
- Updated database schema for...

## Testing
How this was tested:
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manually tested scenarios:
  - Scenario 1: ...
  - Scenario 2: ...

## QA Notes
What QA should focus on:
- Test AC-1: Verify that...
- Test AC-2: Check edge case...
- Regression: Ensure existing feature X still works

## Screenshots / Demo
[If UI changes]

## Deployment Notes
- [ ] Database migration required
- [ ] Environment variables: `NEW_VAR=value`
- [ ] Feature flag: `feature_x` (default: disabled)

## Risks / Concerns
Potential issues and how they're mitigated.

## Checklist
- [ ] Code follows team standards
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No secrets committed
- [ ] Backward compatible (or migration plan)
```

## Best Practices

### For PRDs
1. **Write before coding starts** - Not after the fact
2. **Link user research** - Real user pain points
3. **Define success metrics** - How you'll measure if this worked
4. **Keep updated** - PRD evolves based on learnings

### For Technical Designs
1. **Consider alternatives** - Show you evaluated options
2. **Explain trade-offs** - Why you chose this approach
3. **Diagram complex systems** - A picture is worth 1000 words
4. **Review with team** - Catch issues early

### For User Stories
1. **Keep atomic** - One story = one vertical slice
2. **Make AC testable** - QA can verify without asking questions
3. **Include context** - Link to PRD for "why"
4. **Estimate realistically** - 1-5 story points ideal

### For QA
1. **Test against AC** - AC is the contract
2. **Think beyond happy path** - Edge cases, errors, failures
3. **Automate when possible** - Regression testing
4. **Document bugs well** - Steps to reproduce, expected vs actual

## Common Pitfalls to Avoid

1. **Missing PRD** → Team doesn't understand "why", makes wrong trade-offs
2. **Vague AC** → QA can't verify, lots of back-and-forth
3. **No technical design** → Rework, inconsistent approaches
4. **Stories too large** → Can't finish in sprint, hard to test
5. **Disconnected docs** → Can't trace requirement to implementation to test
6. **Stale documentation** → Becomes useless, nobody trusts it

## Implementation Checklist

When starting a new feature:
- [ ] PRD written and approved by squad
- [ ] Technical design reviewed and approved
- [ ] Epic created in issue tracker
- [ ] Stories broken down with clear AC
- [ ] QA test plan drafted
- [ ] All docs linked together (traceability)
- [ ] Definition of Done agreed upon
- [ ] Kickoff meeting with full squad

## Templates Available

This skill can generate:
1. **PRD Template** - Markdown format for Confluence/Notion
2. **Technical Design Template** - Engineering-focused
3. **User Story Template** - For issue tracker (Jira/Linear)
4. **Test Case Template** - For QA documentation
5. **PR Template** - For GitHub/GitLab
6. **ADR Template** - Architecture Decision Record

## Usage Instructions

When you invoke this skill, I will:

1. **Assess Your Needs**
   - Ask about your project context
   - Understand your team structure
   - Identify which documents you need

2. **Provide Customized Templates**
   - Generate templates tailored to your project
   - Include examples specific to your domain
   - Adapt formality level to your team size

3. **Create Documentation**
   - Write actual PRDs, TDDs, or stories for your features
   - Ensure all documents are linked and traceable
   - Follow best practices for your tech stack

4. **Establish Processes**
   - Suggest documentation workflow for your squad
   - Recommend tools and integrations
   - Provide onboarding materials for team

## Quick Start

Typical invocations:
- "Set up documentation structure for a new authentication feature"
- "Create a PRD template for our team"
- "Generate user stories with AC for [feature description]"
- "Help me write a technical design for [architectural change]"
- "What documentation do I need before starting sprint planning?"

## References & Resources

- **PRD Best Practices**: [Product School PRD Guide](https://productschool.com/blog/product-management-2/how-to-write-product-requirements-document/)
- **Agile User Stories**: [Mike Cohn's User Story Guide](https://www.mountaingoatsoftware.com/agile/user-stories)
- **Acceptance Criteria**: [Gherkin Syntax](https://cucumber.io/docs/gherkin/)
- **Technical Design**: [Google Design Docs](https://www.industrialempathy.com/posts/design-docs-at-google/)
- **ADRs**: [Architecture Decision Records](https://adr.github.io/)

---

Ready to establish professional documentation practices for your agile squad!
