# Playwright Skill for Claude Code

**General-purpose browser automation as a Claude Skill**

A [Claude Skill](https://www.anthropic.com/news/skills) that enables Claude to write and execute any Playwright automation on-the-fly - from simple page tests to complex multi-step flows. Packaged as a [Claude Code Plugin](https://docs.claude.com/en/docs/claude-code/plugins) for easy installation and distribution.

Claude autonomously decides when to use this skill based on your browser automation needs, loading only the minimal information required for your specific task.

## Features

- **Any Automation Task** - Claude writes custom code for your specific request, not limited to pre-built scripts
- **Visible Browser by Default** - See automation in real-time with `headless: false`
- **Zero Module Resolution Errors** - Universal executor ensures proper module access
- **Progressive Disclosure** - Concise SKILL.md with full API reference loaded only when needed
- **Safe Cleanup** - Smart temp file management without race conditions
- **Comprehensive Helpers** - Optional utility functions for common tasks

## Installation

This skill can be installed via the Claude Code plugin system or manually.

### Option 1: Via Plugin System (Recommended)

```bash
# Add this repository as a marketplace
/plugin marketplace add lackeyjb/playwright-skill

# Install the plugin
/plugin install playwright-skill@playwright-skill

# Navigate to the skill directory and run setup
cd ~/.claude/plugins/marketplaces/playwright-skill/skills/playwright-skill
npm run setup
```

Verify installation by running `/help` to confirm the skill is available.

### Option 2: Manual Git Clone

Install directly from GitHub to your skills directory:

**Global Installation (Available Everywhere):**
```bash
# Navigate to your Claude skills directory
cd ~/.claude/skills

# Clone the skill
git clone https://github.com/lackeyjb/playwright-skill.git

# Navigate into the skill directory (note the nested structure)
cd playwright-skill/skills/playwright-skill

# Install dependencies and Chromium browser
npm run setup
```

**Project-Specific Installation:**
```bash
# Install in a specific project
cd /path/to/your/project
mkdir -p .claude/skills
cd .claude/skills
git clone https://github.com/lackeyjb/playwright-skill.git
cd playwright-skill/skills/playwright-skill
npm run setup
```

### Option 3: Download Release

1. Download the latest release from [GitHub Releases](https://github.com/lackeyjb/playwright-skill/releases)
2. Extract to:
   - Global: `~/.claude/skills/playwright-skill`
   - Project: `/path/to/your/project/.claude/skills/playwright-skill`
3. Navigate to the skill directory and run setup:
   ```bash
   cd playwright-skill/skills/playwright-skill
   npm run setup
   ```

### Verify Installation

Run `/help` to confirm the skill is loaded, then ask Claude to perform a simple browser task like "Test if google.com loads".

## Quick Start

After installation, simply ask Claude to test or automate any browser task. Claude will write custom Playwright code, execute it, and return results with screenshots and console output.

## Usage Examples

### Test Any Page
```
"Test the homepage"
"Check if the contact form works"
"Verify the signup flow"
```

### Visual Testing
```
"Take screenshots of the dashboard in mobile and desktop"
"Test responsive design across different viewports"
```

### Interaction Testing
```
"Fill out the registration form and submit it"
"Click through the main navigation"
"Test the search functionality"
```

### Validation
```
"Check for broken links"
"Verify all images load"
"Test form validation"
```

## How It Works

1. Describe what you want to test or automate
2. Claude writes custom Playwright code for the task
3. The universal executor (run.js) runs it with proper module resolution
4. Browser opens (visible by default) and automation executes
5. Results are displayed with console output and screenshots

## Configuration

Default settings:
- **Headless:** `false` (browser visible unless explicitly requested otherwise)
- **Slow Motion:** `100ms` for visibility
- **Timeout:** `30s`
- **Screenshots:** Saved to `/tmp/`

## Project Structure

```
playwright-skill/
├── .claude-plugin/
│   ├── plugin.json          # Plugin metadata for distribution
│   └── marketplace.json     # Marketplace configuration
├── skills/
│   └── playwright-skill/    # The actual skill (Claude discovers this)
│       ├── SKILL.md         # What Claude reads (314 lines)
│       ├── run.js           # Universal executor (proper module resolution)
│       ├── package.json     # Dependencies & setup scripts
│       └── lib/
│           └── helpers.js   # Optional utility functions
├── API_REFERENCE.md         # Full Playwright API reference (630 lines)
├── README.md                # This file - user documentation
├── CONTRIBUTING.md          # Contribution guidelines
└── LICENSE                  # MIT License
```

## Advanced Usage

Claude will automatically load `API_REFERENCE.md` when needed for comprehensive documentation on selectors, network interception, authentication, visual regression testing, mobile emulation, performance testing, and debugging.

## Dependencies

- Node.js >= 14.0.0
- Playwright ^1.48.0 (installed via `npm run setup`)
- Chromium (installed via `npm run setup`)

## Troubleshooting

**Playwright not installed?**
Navigate to the skill directory and run `npm run setup`.

**Module not found errors?**
Ensure automation runs via `run.js`, which handles module resolution.

**Browser doesn't open?**
Verify `headless: false` is set. The skill defaults to visible browser unless headless mode is requested.

**Install all browsers?**
Run `npm run install-all-browsers` from the skill directory.

## What is a Claude Skill?

[Skills](https://www.anthropic.com/news/skills) are modular capabilities that extend Claude's functionality. Unlike slash commands that you invoke manually, skills are model-invoked—Claude autonomously decides when to use them based on your request.

When you ask Claude to test a webpage or automate browser interactions, Claude discovers this skill, loads the necessary instructions, executes custom Playwright code, and returns results with screenshots and console output.

## Contributing

Contributions are welcome. Fork the repository, create a feature branch, make your changes, and submit a pull request. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Learn More

- [Claude Skills](https://www.anthropic.com/news/skills) - Official announcement from Anthropic
- [Claude Code Skills Documentation](https://docs.claude.com/en/docs/claude-code/skills)
- [Claude Code Plugins Documentation](https://docs.claude.com/en/docs/claude-code/plugins)
- [Plugin Marketplaces](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)
- [API_REFERENCE.md](API_REFERENCE.md) - Full Playwright documentation
- [GitHub Issues](https://github.com/lackeyjb/playwright-skill/issues)

## License

MIT License - see [LICENSE](LICENSE) file for details.
