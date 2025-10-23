# Playwright Skill Analysis

**Source**: https://github.com/lackeyjb/playwright-skill
**Version**: 4.0.0
**Author**: @lackeyjb (Community)
**Type**: Browser Automation & Testing

---

## Overview

A production-ready Claude Code skill for automated browser testing using Playwright. This skill enables Claude to autonomously write and execute browser automation code for testing, screenshots, form filling, and any web interaction task.

## Key Features

### 1. Model-Invoked Automation

**Claude decides when to use this skill** based on user requests like:
- "Test if the login form works"
- "Take a screenshot of the homepage at different screen sizes"
- "Check if all links on the page work"
- "Fill out the registration form automatically"

No explicit `/skill playwright` invocation needed!

### 2. Progressive Disclosure Architecture

Follows Anthropic's Skill-Creator best practices:

```
playwright-skill/
├── SKILL.md (12.7k - core workflow)
├── run.js (universal executor script)
├── lib/
│   └── helpers.js (reusable utilities)
├── API_REFERENCE.md (15.5k - full Playwright API)
├── package.json (dependencies)
└── README.md (user guide)
```

**Context Efficiency**:
- SKILL.md: Loaded when skill triggers (~13k)
- API_REFERENCE.md: Loaded only when complex tasks need full API (~16k)
- Result: 2-tier loading for optimal context usage

### 3. Critical Workflow (3-Step Process)

**Step 1: Auto-detect Dev Servers**
```bash
# Automatically finds running localhost servers
node -e "require('./lib/helpers').detectDevServers()"

# Returns: http://localhost:3000, http://localhost:8080, etc.
```

**Step 2: Write Scripts to /tmp**
- Never clutters project directory
- Scripts: `/tmp/playwright-test-*.js`
- Auto-cleaned by OS

**Step 3: Visible Browser by Default**
- `headless: false` - watch tests run
- Easier debugging
- User-requested headless mode supported

### 4. Common Patterns Provided

**7 Ready-to-Use Patterns**:

1. **Responsive Design Testing**
   ```javascript
   const viewports = [
     { width: 375, height: 667, name: 'iPhone' },
     { width: 768, height: 1024, name: 'iPad' },
     { width: 1920, height: 1080, name: 'Desktop' }
   ];
   ```

2. **Login Flow Automation**
   ```javascript
   await page.fill('#username', 'testuser');
   await page.fill('#password', 'password123');
   await page.click('button[type="submit"]');
   ```

3. **Form Filling & Submission**
   - Text fields, checkboxes, radio buttons
   - Dropdowns, file uploads

4. **Link Validation**
   - Check all links on page
   - Verify no 404s

5. **Screenshot Capture**
   - Full page, specific elements
   - Multiple viewports

6. **Responsive Breakpoint Testing**
   - Test across device sizes

7. **Custom Automation**
   - Any browser task

### 5. Helper Functions

**`lib/helpers.js` provides**:

```javascript
// Auto-detect running dev servers
detectDevServers()

// Safe element interaction (waits for element)
safeClick(page, selector)
safeFill(page, selector, value)

// Screenshot utilities
takeScreenshot(page, path, options)

// Cookie management
setCookies(page, cookies)
getCookies(page)

// Table extraction
extractTableData(page, selector)
```

### 6. Execution Pattern

**How Claude uses this skill**:

1. User: "Test if google.com loads"

2. Claude (thinking):
   - This is a browser testing task
   - Use playwright-skill
   - Detect if localhost server needed (no, external URL)
   - Write Playwright script to /tmp

3. Claude (action):
   ```javascript
   // /tmp/playwright-test-123.js
   const { chromium } = require('playwright');

   (async () => {
     const browser = await chromium.launch({ headless: false });
     const page = await browser.newPage();

     await page.goto('https://google.com');
     console.log('✅ Google homepage loaded');
     console.log(`Title: ${await page.title()}`);

     await browser.close();
   })();
   ```

4. Claude (execute):
   ```bash
   cd .claude/skills/playwright-skill
   node run.js /tmp/playwright-test-123.js
   ```

5. Claude (report):
   "✅ Google homepage successfully loaded. Page title: 'Google'"

## Skill-Creator Compliance

### ✅ Follows Best Practices

**Progressive Disclosure**:
- SKILL.md: Core workflow (13k)
- API_REFERENCE.md: Full API docs (16k) - loaded when needed
- Two-tier context loading

**Bundled Resources**:
- ✅ `scripts/` - run.js executor
- ✅ `lib/` - Helper functions
- ✅ `references/` - API_REFERENCE.md (implicit reference)

**Clear Metadata**:
```yaml
name: Playwright Browser Automation
description: Complete browser automation... Test pages, fill forms...
version: 4.0.0
tags: [testing, automation, browser, e2e]
```

**Workflow Guidance**:
- CRITICAL WORKFLOW section (step-by-step)
- Common patterns (7 examples)
- Troubleshooting section

### ✅ Production Quality

**Path Resolution**:
- Handles multiple installation locations
- Auto-detects skill directory
- No hardcoded paths

**Safety**:
- Scripts in /tmp (not project directory)
- Auto-cleanup (OS handles /tmp)
- Visible browser by default (easier debugging)

**Error Handling**:
- Safe element interaction (waits for elements)
- Dev server detection
- Clear error messages

## Use Cases

### 1. Web Application Testing

**Example**: Test user registration flow

```
User: "Test the registration form on localhost:3000"

Claude:
1. Detects dev server at localhost:3000
2. Writes Playwright script:
   - Fill email field
   - Fill password field
   - Click submit
   - Verify success message
3. Executes and reports results
```

### 2. Responsive Design Validation

**Example**: Check homepage on different devices

```
User: "Check if homepage looks good on mobile, tablet, desktop"

Claude:
- Tests 375px (mobile), 768px (tablet), 1920px (desktop)
- Takes screenshots of each
- Reports layout issues
```

### 3. Visual Regression Testing

**Example**: Compare before/after screenshots

```
User: "Take screenshots of all pages for visual regression testing"

Claude:
- Navigates to each page
- Captures full-page screenshots
- Saves to project directory
- Returns paths to screenshots
```

### 4. Form Automation

**Example**: Fill complex multi-step form

```
User: "Fill out the job application form with test data"

Claude:
- Steps through multi-page form
- Fills all fields with realistic test data
- Submits form
- Verifies confirmation
```

### 5. Link Checking

**Example**: Validate all links

```
User: "Check if all links on the documentation site work"

Claude:
- Crawls all pages
- Checks each link
- Reports broken links (404s)
- Provides list of working links
```

## Integration with Our Project

### How It Fits

**Complements Our Skills**:

1. **agile-master** - Creates user stories
   → **playwright-skill** - Tests implemented features

2. **company-research** - Researches companies
   → **playwright-skill** - Scrapes company websites for data

3. **Skills in general** - Build features
   → **playwright-skill** - Automated QA testing

### Use in Development Workflow

```
Feature Development Flow:

1. [agile-master] Create User Stories with AC
2. [Developer] Implements feature
3. [playwright-skill] Automated testing of AC
4. [QA] Manual verification
5. [Deploy]

Example:
User Story AC: "User can log in with email/password"
playwright-skill: Auto-tests login flow, verifies success
```

## Setup for Our Project

### Installation (Already Done)

✅ Copied to `.claude/skills/playwright-skill/`

### First-Time Setup

```bash
cd .claude/skills/playwright-skill
npm run setup

# Installs:
# - playwright (v1.48.0+)
# - chromium browser
```

### Usage

**No explicit invocation needed!** Just ask Claude:

```
"Test the login form"
"Take screenshots of homepage at mobile/desktop sizes"
"Check if all navigation links work"
"Fill out the contact form with test data"
```

Claude will automatically use playwright-skill when appropriate.

## Comparison: Official vs Community

### Anthropic Official Skills

**webapp-testing** (from anthropics/skills):
- Part of official skill collection
- Likely similar Playwright integration
- Official support and updates

### lackeyjb/playwright-skill (Community)

**Advantages**:
- ✅ Production-ready (v4.0.0)
- ✅ Active maintenance (recent commits)
- ✅ Comprehensive documentation
- ✅ Helper library included
- ✅ 7 common patterns
- ✅ Dev server auto-detection

**Differences**:
- Community-maintained (not official)
- More opinionated (visible browser by default, /tmp for scripts)
- Includes helper functions (official may not)

## File Structure Details

```
playwright-skill/
├── SKILL.md (12,780 bytes)
│   - Core workflow
│   - Common patterns
│   - Setup instructions
│   - Troubleshooting
│
├── run.js (5,179 bytes)
│   - Universal executor
│   - Runs Playwright scripts
│   - Module resolution
│   - Error handling
│
├── lib/
│   └── helpers.js
│       - detectDevServers()
│       - safeClick(), safeFill()
│       - Screenshot utilities
│       - Cookie management
│       - Table extraction
│
├── API_REFERENCE.md (15,534 bytes)
│   - Complete Playwright API
│   - Reference docs
│   - Loaded when needed
│
├── package.json (652 bytes)
│   - Dependencies:
│     - playwright: ^1.48.0
│   - Scripts:
│     - setup: Install playwright
│
└── README.md (7,140 bytes)
    - User-facing documentation
    - Installation guide
    - Usage examples
```

## Best Practices from This Skill

### 1. Path Resolution

**Problem**: Skills can be installed in different locations

**Solution**:
```markdown
**IMPORTANT - Path Resolution:**
Determine the skill directory based on where you loaded this SKILL.md file,
and use that path in all commands below. Replace `$SKILL_DIR` with actual path.

Common installation paths:
- Plugin system: ~/.claude/plugins/...
- Manual global: ~/.claude/skills/...
- Project-specific: <project>/.claude/skills/...
```

**Lesson**: Always handle multiple installation locations

### 2. Critical Workflow Section

**Problem**: Complex skills need clear step-by-step guidance

**Solution**:
```markdown
**CRITICAL WORKFLOW - Follow these steps in order:**

1. Auto-detect dev servers FIRST
2. Write scripts to /tmp
3. Use visible browser by default
4. Parameterize URLs
```

**Lesson**: Provide explicit numbered steps for critical workflows

### 3. Helper Library

**Problem**: Repetitive code patterns in automation

**Solution**: Provide `lib/helpers.js` with common utilities

**Lesson**: Extract common patterns into reusable helpers

### 4. Visible by Default

**Problem**: Headless testing is hard to debug

**Solution**: `headless: false` by default, allow override

**Lesson**: Default to debuggable, offer performance mode as option

## Performance Characteristics

### Context Usage

| Scenario | Context Loaded | Tokens (approx) |
|----------|----------------|-----------------|
| Simple test | SKILL.md only | ~3,200 tokens |
| Complex automation | SKILL.md + API_REFERENCE.md | ~7,200 tokens |
| Using helpers | SKILL.md + lib/helpers.js | ~3,500 tokens |

**Efficient**: Two-tier loading keeps common tasks lightweight

### Execution Speed

- Browser launch: ~2-3 seconds
- Simple page test: <5 seconds total
- Complex multi-step: Varies with task

**Note**: Visible browser slightly slower than headless, but worth it for debugging

## Recommendations

### When to Use

✅ Web application testing (E2E, integration)
✅ Automated form filling
✅ Screenshot capture (responsive testing)
✅ Link validation
✅ Visual regression testing
✅ Any browser automation task

### When NOT to Use

❌ API-only testing (use API clients instead)
❌ Performance benchmarking (use dedicated tools like k6, Lighthouse)
❌ Static code analysis (use linters)

### Best Used With

- **agile-master**: Test user stories automatically
- **CI/CD pipelines**: Run tests on every PR
- **QA workflows**: Automated regression testing

## Conclusion

**playwright-skill** is a **production-quality, well-architected** browser automation skill that:

✅ Follows Skill-Creator best practices (progressive disclosure, bundled resources)
✅ Provides real value (7 common patterns, helper library, dev server detection)
✅ Well-documented (SKILL.md + API_REFERENCE.md + README.md)
✅ Production-ready (v4.0.0, active maintenance)

**Perfect addition to our skill collection** for automated web testing!

---

## Next Steps

1. ✅ Added to `.claude/skills/playwright-skill/`
2. ⏳ Run `npm run setup` to install Playwright
3. ⏳ Test with simple automation task
4. ⏳ Integrate with agile-master workflow (test user stories)
5. ⏳ Document in main skills collection

## Resources

- **GitHub**: https://github.com/lackeyjb/playwright-skill
- **Playwright Docs**: https://playwright.dev/
- **Our Skills**: `.claude/skills/`
