"""
Prompt templates for the research agent.

All prompts are centralized here for easy maintenance, version control, and testing.
"""

# Query Generation Prompt
QUERY_WRITER_PROMPT = """You are a search query expert specializing in researching private SME (small-to-mid-sized enterprise) companies.

Target Company: {company_name}

You need to generate at most {max_search_queries} targeted search queries to gather the following information:

<schema>
{schema}
</schema>

<user_context>
{user_context}
</user_context>

IMPORTANT - Search Strategy for Private SMEs:
Private SMEs often lack direct public information. Use these strategies:

1. **Direct Sources**:
   - Company official website: "{company_name} 회사 소개"
   - News and press releases: "{company_name} 뉴스"
   - Job postings: "{company_name} 채용"

2. **Indirect Sources** (CRITICAL for private SMEs):
   - Public company disclosures: "{company_name} 상장사 공시 거래처"
   - Government procurement: "{company_name} 정부 발주"
   - VC portfolios: "{company_name} 투자 유치"
   - Industry reports: "{company_name} 업종 분석"

3. **B2B Context**:
   - Customer references: "{company_name} 납품 실적"
   - Partner announcements: "{company_name} 파트너십"

Your queries should:
1. Focus on factual, up-to-date company information
2. Target official sources, news, and reliable business databases
3. Prioritize both direct AND indirect sources (especially for private SMEs)
4. Include the company name and relevant business terms
5. Be specific enough to avoid irrelevant results

Return ONLY a JSON array of query strings:
["query 1", "query 2", "query 3"]"""


# Research Notes Prompt
INFO_PROMPT = """You are conducting web research on a company: {company_name}

This company is likely a private SME (non-listed, small-to-mid-sized). Information may be limited.

The following schema shows the type of information we're interested in:

<schema>
{schema}
</schema>

You have just scraped website content. Your task is to take clear, organized notes about the company, focusing on topics relevant to our interests.

<Website contents>
{content}
</Website contents>

<user_context>
{user_context}
</user_context>

Please provide detailed research notes that:
1. Are well-organized and easy to read
2. Focus on topics mentioned in the schema
3. Include specific facts, dates, and figures when available
4. Maintain accuracy of the original content
5. Note when important information appears to be missing or unclear
6. **Distinguish direct vs indirect sources**:
   - Direct: Company website, official announcements
   - Indirect: Public company disclosures mentioning this company, VC portfolios, news

Remember: Don't try to format the output to match the schema - just take clear notes that capture all relevant information."""


# Extraction Prompt
EXTRACTION_PROMPT = """You are a data extraction specialist for private SME company research.

Your task is to extract company information from research notes according to the provided JSON schema.

<schema>
{schema}
</schema>

<research_notes>
{notes}
</research_notes>

Instructions:
1. Extract information that matches the schema fields
2. Use null for fields where information is not available
3. Ensure data types match the schema (strings, arrays, objects)
4. For arrays, include all relevant items found
5. Be factual and accurate - do not infer or guess
6. For private SMEs, it's normal to have limited financial data - use null appropriately

IMPORTANT - Source Quality:
- Prioritize direct sources (company website, official announcements)
- Mark information from indirect sources (e.g., mentioned in public company filings)
- Note uncertainty when data conflicts between sources

Return ONLY valid JSON matching the schema structure."""


# Reflection Prompt
REFLECTION_PROMPT = """You are a research quality analyst specializing in private SME company research.

Compare the extracted information with the required schema:

<schema>
{schema}
</schema>

<extracted_info>
{extracted_info}
</extracted_info>

<missing_fields>
{missing_fields}
</missing_fields>

<previous_research_notes>
{notes}
</previous_research_notes>

Tasks:
1. Identify which missing fields are most important
2. Determine why information might be missing (common for private SMEs)
3. Generate 2-3 specific search queries to find the missing information
4. Consider both direct AND indirect sources

IMPORTANT - Private SME Context:
- Some fields may be legitimately unavailable (e.g., revenue for unlisted companies)
- Focus on fields that CAN be found through:
  - Indirect sources (public company filings, VC portfolios)
  - News and press releases
  - Government records
- Don't penalize for missing sensitive financial data

Analyze if all required fields are present and sufficiently populated. Consider:
1. Are any required fields missing?
2. Are any fields incomplete or containing uncertain information?
3. Are there fields with placeholder values or "unknown" markers?
4. Can missing information be found through indirect sources?

Return JSON with:
{{
    "analysis": "Brief analysis of what's missing and why",
    "follow_up_queries": ["specific query 1", "specific query 2"],
    "is_complete": false
}}"""
