# Private SME Research Strategies

**Target:** Small-to-Mid-Sized Private/Unlisted Companies (10-1,000 employees)

This document provides specialized strategies for researching private companies where structured data is scarce compared to public companies.

## Table of Contents

- [Why Private SMEs Are Different](#why-private-smes-are-different)
- [Direct Research Sources](#direct-research-sources)
- [Indirect Research Sources](#indirect-research-sources-critical)
- [Search Query Patterns](#search-query-patterns)
- [Default Schema for Private SMEs](#default-schema-for-private-smes)
- [Example Workflow](#example-workflow)

---

## Why Private SMEs Are Different

### Public Companies vs Private SMEs

| Aspect | Public Companies | Private SMEs |
|--------|------------------|--------------|
| **Financial Data** | SEC filings, investor relations | Not publicly available |
| **Company Info** | Annual reports, 10-K, 10-Q | Limited to website, news |
| **Employee Count** | Disclosed in filings | Estimated from LinkedIn, job postings |
| **Revenue** | Public filings | Not disclosed (must estimate) |
| **Customers** | Major customers disclosed | Must discover indirectly |
| **Technology** | Patent filings, tech blogs | Job postings, tech blogs |

### Key Challenge

Private companies don't file public reports, BUT:
- Public companies they do business with **must** disclose major suppliers/customers
- This reveals transaction volumes, relationship nature, and business scope

**This is the key insight for private SME research.**

---

## Direct Research Sources

### 1. Company Website & Blog
**What to look for:**
- About page → founding year, leadership, mission
- Products/services page → offerings, target market
- Case studies → customers, use cases
- Blog/news → recent developments, tech stack mentions
- Careers page → tech stack, team size hints

**Search Queries:**
```
"[Company Name] about"
"[Company Name] careers"
"[Company Name] case study"
"[Company Name] blog"
```

### 2. News Articles & Press Releases
**What to look for:**
- Product launches
- Funding announcements
- Partnership news
- Executive hires
- Awards/recognition

**Search Queries:**
```
"[Company Name] news"
"[Company Name] funding OR investment"
"[Company Name] partnership"
"[Company Name] announces"
"[Company Name]" past year  # Time filter
```

### 3. Job Postings
**What to look for:**
- Tech stack requirements → technologies used
- Team size indicators → "Join our team of 50+"
- Office locations → geographic presence
- Growth indicators → "rapidly growing," "expanding team"

**Search Queries:**
```
"[Company Name] careers"
"[Company Name] jobs"
"[Company Name]" site:linkedin.com/jobs
"[Company Name]" site:glassdoor.com
```

### 4. Industry Reports & Directories
**What to look for:**
- Market positioning
- Industry categorization
- Competitor lists

**Search Queries:**
```
"[Company Name]" industry report
"[Company Name]" market analysis
"[Industry] companies list"
```

---

## Indirect Research Sources (CRITICAL!)

These are often **more valuable** than direct sources for private companies.

### 1. Public Company Filings Mentioning the Target

**Why this matters:**
- Public companies must disclose major suppliers, customers, and partners
- This reveals:
  - **Who their customers are** (if target is a supplier)
  - **Transaction volumes** (material relationships disclosed)
  - **Business relationships** (supplier, distributor, partner)
  - **Market validation** (if public companies trust them)

**Where to find:**
- SEC filings (10-K, 10-Q, 8-K) - US companies
- DART (Korea), SEDAR (Canada), etc. - International
- Annual reports (PDF search)

**Search Queries:**
```
"[Company Name]" site:sec.gov
"[Company Name]" site:dart.fss.or.kr
"[Company Name]" annual report filetype:pdf
"[Company Name]" supplier OR vendor
"[Company Name]" customer OR client
"[Company Name]" partner OR partnership
```

**Example:**
```
Target: Small cybersecurity software company "SecureTech"
Query: "SecureTech" site:sec.gov

Found: Fortune 500 company XYZ Corp's 10-K mentions:
"We rely on SecureTech for endpoint security solutions.
 Purchases from SecureTech totaled $5M in FY2024."

→ Reveals: SecureTech has Fortune 500 clients, $5M+ revenue from one client
```

### 2. VC/Investor Portfolio Pages

**Why this matters:**
- Shows funding status
- Reveals investors and amounts
- Indicates company stage and traction

**Search Queries:**
```
"[Company Name]" venture capital OR VC OR investment
"[Company Name]" series A OR series B OR seed
"[Company Name]" funding round
"[Company Name]" portfolio site:*.vc
"[Company Name]" site:crunchbase.com
```

### 3. Government Procurement Records

**Why this matters:**
- Public contracts are disclosed
- Shows government clients
- Revenue indicators from contract values

**Search Queries:**
```
"[Company Name]" government contract
"[Company Name]" site:sam.gov  # US federal contracts
"[Company Name]" site:ted.europa.eu  # EU tenders
"[Company Name]" procurement OR tender
"[Company Name]" awarded contract
```

### 4. Partner & Customer Testimonials

**Why this matters:**
- Companies often showcase major clients
- Testimonials reveal use cases and value

**Search Queries:**
```
"[Company Name]" testimonial OR "case study"
"powered by [Company Name]"
"uses [Company Name]"
"[Company Name]" customer success
```

---

## Search Query Patterns

### Initial Discovery Queries

```python
initial_queries = [
    f"{company_name} about company",
    f"{company_name} products services",
    f"{company_name} customers clients",
    f"{company_name} news past year",
    f"{company_name} careers jobs"
]
```

### Indirect Source Queries

```python
indirect_queries = [
    f'"{company_name}" site:sec.gov',  # US public filings
    f'"{company_name}" supplier OR vendor',
    f'"{company_name}" customer OR partner',
    f'{company_name} funding OR investment OR VC',
    f'{company_name} government contract OR procurement'
]
```

### Technology Discovery Queries

```python
tech_queries = [
    f'{company_name} technology stack',
    f'{company_name} site:stackoverflow.com',
    f'{company_name} site:github.com',
    f'{company_name} engineering blog',
    f'{company_name} jobs "required skills"'
]
```

### Temporal Queries (for recent info)

```python
recent_queries = [
    f'{company_name} news "past 3 months"',
    f'{company_name} latest updates 2025',
    f'{company_name} recent announcement'
]
```

---

## Default Schema for Private SMEs

This schema is optimized for private company research:

```python
DEFAULT_SCHEMA = {
    "title": "Private Company Information",
    "description": "Structured information about a private small-to-mid-sized company",
    "type": "object",
    "properties": {
        "company_name": {
            "type": "string",
            "description": "Official company name"
        },
        "founded": {
            "type": "string",
            "description": "Year founded or established"
        },
        "headquarters": {
            "type": "string",
            "description": "Headquarters location (city, country)"
        },
        "industry": {
            "type": "string",
            "description": "Primary industry or sector (e.g., B2B SaaS, Manufacturing, IT Services)"
        },
        "description": {
            "type": "string",
            "description": "Brief company description and business model"
        },
        "products_services": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Main products or services offered"
        },
        "target_customers": {
            "type": "string",
            "description": "Target customer segments (B2B/B2C, industries served)"
        },
        "key_people": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "role": {"type": "string", "description": "CEO, CTO, Founder, etc."}
                }
            },
            "description": "CEO, founders, key executives"
        },
        "employee_count": {
            "type": "string",
            "description": "Approximate number of employees (range acceptable, e.g., '50-100')"
        },
        "funding_status": {
            "type": "string",
            "description": "Bootstrapped, angel-funded, VC-backed, Series A/B/C, etc."
        },
        "major_clients": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Notable clients or partners (from case studies, news, OR public company filings)"
        },
        "public_company_relationships": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "public_company": {
                        "type": "string",
                        "description": "Name of the public company"
                    },
                    "relationship_type": {
                        "type": "string",
                        "description": "Supplier, customer, partner, etc."
                    },
                    "details": {
                        "type": "string",
                        "description": "Details from public filings (e.g., contract value, description)"
                    }
                }
            },
            "description": "Relationships with public companies as mentioned in their SEC/DART filings"
        },
        "technology_stack": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Technologies used (from job postings, tech blogs, GitHub)"
        },
        "office_locations": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Office locations beyond HQ"
        },
        "recent_news": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Recent company news or announcements (past 6-12 months)"
        },
        "competitive_advantages": {
            "type": "string",
            "description": "What makes this company unique or competitive"
        }
    },
    "required": ["company_name", "description", "industry"]
}
```

### Key Design Decisions

1. **Flexible employee_count**: Accepts ranges ("50-100") since exact counts are rarely available
2. **public_company_relationships**: Dedicated field for indirect source discoveries
3. **funding_status**: More relevant than valuation for private companies
4. **technology_stack**: Important for B2B tech companies, discoverable via job postings
5. **competitive_advantages**: Helps LLM synthesize value proposition from scattered sources

---

## Example Workflow

### Scenario: Research a Private B2B SaaS Company

**Company:** "SecureTech Solutions" (fictional private cybersecurity company)

#### Phase 1: Initial Research

**Queries:**
1. `SecureTech Solutions about`
2. `SecureTech Solutions products`
3. `SecureTech Solutions customers`
4. `SecureTech Solutions news past year`

**Findings:**
- Founded 2018, HQ in Austin, TX
- Provides endpoint security software
- Targets mid-market enterprises
- Raised Series A in 2020

#### Phase 2: Indirect Source Discovery

**Queries:**
1. `"SecureTech Solutions" site:sec.gov`
2. `"SecureTech Solutions" supplier OR vendor`
3. `"SecureTech Solutions" partner annual report`

**Findings:**
- Fortune 500 Retailer XYZ's 10-K mentions: "SecureTech Solutions provides endpoint security for our 5,000 point-of-sale systems"
- Cloud Provider ABC's partner page lists SecureTech as "Technology Partner"
- Government contract award: "SecureTech awarded $2M contract for DHS cybersecurity"

**This is the gold!** → Major validation, revenue indicators, enterprise clients

#### Phase 3: Technology & Team Discovery

**Queries:**
1. `SecureTech Solutions careers`
2. `SecureTech Solutions site:linkedin.com/jobs`
3. `SecureTech Solutions engineering blog`

**Findings:**
- Job posting requires: Python, Kubernetes, AWS, React
- Engineering blog mentions: "Our microservices architecture on AWS"
- LinkedIn shows ~150 employees

#### Phase 4: Reflection & Follow-up

**Missing fields:** Exact funding amount, competitive advantages

**Follow-up queries:**
1. `SecureTech Solutions Series A amount funding`
2. `SecureTech Solutions vs competitors comparison`
3. `SecureTech Solutions reviews OR testimonials`

---

## Best Practices

### DO:
✅ Always include indirect source queries (public filings, VC portfolios)
✅ Use temporal filters for recent information ("past year")
✅ Search job postings for tech stack and team size
✅ Look for customer testimonials and case studies
✅ Cross-reference information from multiple sources

### DON'T:
❌ Expect financial data like public companies (revenue, profit)
❌ Skip indirect sources - they're often most valuable
❌ Assume company websites have complete info
❌ Ignore job postings - they reveal a lot
❌ Give up if first few searches return little - try indirect sources

### Query Prioritization

**High Priority (always include):**
1. Company website/about page
2. Public company filings mentioning target (`site:sec.gov`)
3. Recent news (time-filtered)
4. Job postings (tech stack, team size)

**Medium Priority:**
1. VC/funding searches
2. Government contracts
3. Industry reports
4. Customer testimonials

**Low Priority (only if schema requires):**
1. Social media
2. Conference appearances
3. Patent searches

---

## Common Pitfalls & Solutions

### Pitfall 1: "No information found"

**Solution:**
- Try indirect sources (public company filings)
- Search for industry + company type instead of company name
- Look for job postings (always exist if company is hiring)
- Search news archives

### Pitfall 2: "Conflicting information"

**Solution:**
- Prioritize primary sources (company website, official filings)
- Use most recent information
- Note uncertainty in extracted data
- Include source URLs in metadata

### Pitfall 3: "Can't find financial data"

**Solution:**
- Don't expect it for private companies
- Use proxies: funding rounds, customer mentions, employee count
- Estimate revenue ranges from indirect signals (e.g., government contract values)

### Pitfall 4: "Only old information"

**Solution:**
- Add temporal filters ("past 6 months", "2025")
- Check job postings (always recent)
- Look for recent news or blog posts
- Note data freshness in extracted information

---

## LLM Prompt Engineering for Private SME Research

### Query Generation Prompt (Template)

```
You are a research query generator for PRIVATE small-to-mid-sized companies.

Generate {max_queries} specific search queries to find information about {company_name}.

IMPORTANT - This is a PRIVATE company, not publicly traded. Focus on:

DIRECT sources:
- Company websites, news articles, job postings, press releases
- Industry reports, tech blogs, case studies
- Recent news (use time ranges like "past year")

INDIRECT sources (VERY VALUABLE!):
- Public company filings WHERE the target is mentioned as supplier/customer/partner
- VC portfolio pages (if the company raised funding)
- Government procurement records (if they have public contracts)

Example query patterns:
- "{company_name} technology stack"
- "{company_name} customers OR clients"
- "{company_name} supplier OR vendor" (find who mentions them)
- "{company_name} site:sec.gov OR site:dart.fss.or.kr" (public filings mentioning them)
- "{company_name} funding OR investment"

Generate diverse queries targeting different aspects.
Focus on queries likely to reveal: {target_fields}

Return queries as a JSON array.
```

### Extraction Prompt (Template)

```
Extract company information from these research notes according to the JSON schema.

Company: {company_name}

Schema:
{json_schema}

Research Notes:
{notes}

IMPORTANT for private companies:
- Employee counts: Use ranges if exact number unknown (e.g., "50-100")
- Revenue: Do NOT guess - only include if explicitly stated
- Funding: Include status (bootstrapped, Series A, etc.) even if amounts unknown
- Customers: Include those mentioned in public company filings or case studies
- Technology: Extract from job postings and engineering blogs

Return ONLY valid JSON matching the schema.
Use null for fields where information is not available.
Do not fabricate information.
```

---

## Conclusion

Researching private SMEs requires a different approach than public companies:

1. **Accept incomplete data** - it's normal for private companies
2. **Leverage indirect sources** - often more valuable than direct sources
3. **Use proxies** - employee count from LinkedIn, tech stack from job postings
4. **Prioritize recent data** - use temporal filters
5. **Cross-validate** - verify information across multiple sources

The key insight: **Public companies disclose relationships with private companies in their filings.** This is your secret weapon for private SME research.
