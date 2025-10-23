# Multi-Agent Workspace

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

> LangGraph 기반 멀티 에이전트 개발을 위한 완전한 워크스페이스

**용도**: LangGraph/Google ADK 멀티 에이전트 시스템 개발
**대상**: Claude Code vibe coding 개발자
**철학**: 공식 레퍼런스 + 재사용 가능한 스킬 + 예제 에이전트

---

## 🎯 이 워크스페이스는 무엇인가요?

**Multi-Agent Workspace**는 Claude Code로 멀티 에이전트 시스템을 빠르게 개발할 수 있도록 설계된 프로젝트 템플릿입니다.

### 핵심 구성 요소

1. **🤖 Claude Code 스킬 컬렉션** (9개)
   - Agile 워크플로우 자동화
   - 멀티 에이전트 시스템 구축
   - 기업 리서치 자동화
   - 브라우저 자동화 테스트
   - 모니터링 & 데이터베이스

2. **📚 공식 레퍼런스 문서** (`.claude/references/`)
   - Google ADK 전체 가이드 (llms.txt, llms-full.txt)
   - LangGraph 멀티 에이전트 아키텍처
   - Claude가 직접 참조하는 LLM 최적화 문서

3. **📦 예제 에이전트 구현**
   - Company Research Agent (Research-Extraction-Reflection)
   - 추가 예제 추가 예정

---

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# Python 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정 (필요시)
cp .env.example .env
```

### 2. Claude Code 스킬 사용

```bash
# Agile 워크플로우
/skill agile-product "새 기능 아이디어"
/skill agile-stories --prd=docs/prd/feature.md
/skill agile-jira --import docs/stories/

# 멀티 에이전트 시스템 구축
/skill langgraph-multi-agent

# 딥 리서치 자동화
/skill deep-research
```

### 3. 레퍼런스 참조

Claude Code에게 명시적으로 요청:
```
"langgraph-multi-agent.md 참고해서 Supervisor 패턴으로 구현해줘"
"google-adk-llms.txt에서 Tool 정의 방법 찾아서 적용해줘"
```

---

## 📁 프로젝트 구조

```
multi-agent-workspace/
├── .claude/                        # Claude Code 전용
│   ├── skills/                     # 🤖 Claude Code 스킬 (7개)
│   │   ├── agile-product/          # PRD 작성
│   │   ├── agile-stories/          # User Story 생성
│   │   ├── agile-jira/             # Jira 통합
│   │   ├── langgraph-multi-agent/  # 멀티 에이전트 시스템
│   │   ├── deep-research/          # 웹 딥리서치 (8개 검색 API)
│   │   ├── database-designer/      # DB 설계 & 선택 (15개 DB 비교)
│   │   ├── playwright-skill/       # 브라우저 자동화
│   │   └── skill-creator/          # 스킬 제작 가이드
│   │
│   ├── references/                 # 📚 공식 레퍼런스 (LLM 최적화)
│   │   ├── README.md              # 레퍼런스 가이드
│   │   ├── google-adk-llms.txt    # Google ADK 요약 (40KB)
│   │   ├── google-adk-llms-full.txt # Google ADK 전체 (3.1MB)
│   │   ├── langgraph-README.md
│   │   ├── langgraph-multi-agent.md # ⭐ 필수
│   │   ├── langgraph-agentic-concepts.md
│   │   └── langgraph-concepts-low-level.md
│   │
│   ├── AGILE_SKILLS_V2.md         # Agile 워크플로우 가이드
│   └── SKILLS_COLLECTION.md       # 전체 스킬 컬렉션 문서
│
├── src/                            # 에이전트 구현 (예제)
│   └── agent/                      # Company Research Agent
│       ├── graph.py
│       ├── state.py
│       ├── prompts.py
│       └── ...
│
├── examples/                       # 사용 예제
│   ├── basic_research.py
│   ├── custom_schema.py
│   └── streaming_example.py
│
├── docs/                           # 📚 개발 문서 (Company Research 관련)
│
├── requirements.txt                # Python 의존성
└── README.md                       # 이 파일
```

---

## 🤖 포함된 Claude Code 스킬

### Agile 워크플로우 자동화

| 스킬 | 역할 | 사용 시점 |
|------|------|----------|
| **agile-product** | PM - PRD 작성 | 새 기능 기획 시작 |
| **agile-stories** | PO - User Story 생성 | PRD → 구현 스토리 변환 |
| **agile-jira** | Dev - Jira 티켓 생성 | 스토리 → Jira 업로드 (REST API) |

**워크플로우**: PRD 작성 → User Stories 생성 → Jira 티켓 생성

---

### 멀티 에이전트 시스템

| 스킬 | 용도 | 사용 시점 |
|------|------|----------|
| **langgraph-multi-agent** | 멀티 에이전트 시스템 구축 | 여러 에이전트 협업 필요 시 |
| **deep-research** | 웹 리서치 자동화 (8가지 검색 API 지원) | 기업/제품/인물 정보 자동 수집 |
| **database-designer** | 데이터베이스 설계 & 선택 | DB 기술 선택, 스키마 설계 |

---

### 개발 도구

| 스킬 | 용도 | 사용 시점 |
|------|------|----------|
| **playwright-skill** | 브라우저 자동화 | E2E 테스트, UI 검증 |
| **skill-creator** | 스킬 제작 가이드 | 새 스킬 만들기 |

---

## 📚 공식 레퍼런스 활용

### `.claude/references/` 디렉토리

Claude Code가 vibe coding 시 자동 참조하는 공식 문서들:

#### Google Agent Development Kit (ADK)

- **`google-adk-llms.txt`** (40KB) - 요약본, 빠른 참조
- **`google-adk-llms-full.txt`** (3.1MB) - 전체 레퍼런스

**포함 내용**:
- Agent 아키텍처 (LLM-driven, Workflow-based)
- Multi-agent 패턴 (Coordinator/Dispatcher)
- Tool 생태계
- Context & State 관리

#### LangGraph

- **`langgraph-multi-agent.md`** (35KB) - ⭐ 필수! 5가지 아키텍처
- **`langgraph-agentic-concepts.md`** - Agent 핵심 개념
- **`langgraph-concepts-low-level.md`** - 저수준 API
- **`langgraph-README.md`** - 빠른 시작

**사용 예시**:
```
"langgraph-multi-agent.md 참고해서 Hierarchical 패턴으로 구현해줘"
"google-adk-llms.txt에서 Session 관리 방법 찾아줘"
```

자세한 가이드: [.claude/references/README.md](.claude/references/README.md)

---

## 🎓 사용 시나리오

### 시나리오 1: 새 기능 개발 (Agile 워크플로우)

```bash
# 1. PRD 작성
/skill agile-product "OAuth 인증 추가"
→ docs/prd/oauth-authentication-2024-10-23.md 생성

# 2. User Stories 생성
/skill agile-stories --prd=docs/prd/oauth-authentication-2024-10-23.md
→ docs/stories/ 에 3개 스토리 생성

# 3. Jira 티켓 생성
/skill agile-jira --import docs/stories/
→ Jira에 Epic + Story 티켓 자동 생성
```

---

### 시나리오 2: 멀티 에이전트 시스템 구축

```bash
# 1. 레퍼런스 확인
cat .claude/references/langgraph-multi-agent.md

# 2. Claude에게 요청
"langgraph-multi-agent.md의 Supervisor 패턴으로
 연구자, 작성자, 검토자 에이전트가 협업하는 시스템 만들어줘"
```

---

### 시나리오 3: 기업 리서치 자동화

```bash
# 1. 리서치 에이전트 구축
/skill deep-research

# 2. 데이터베이스 설정
/skill database-designer

# 3. 실행
python examples/basic_research.py
```

---

## 🛠️ 새 에이전트 만들기

### 방법 1: 스킬 활용

```bash
/skill langgraph-multi-agent
# Claude가 대화형으로 에이전트 구축 안내
```

### 방법 2: 레퍼런스 참조

```
"langgraph-multi-agent.md에서 Network 아키텍처 읽고
 Customer Support 멀티 에이전트 시스템 만들어줘"
```

### 방법 3: 예제 복사

```bash
# Company Research Agent 코드 참고
cp -r src/agent src/agents/my_new_agent
# 수정 후 사용
```

---

## 💡 Vibe Coding 팁

### 1. 레퍼런스 명시

❌ "멀티 에이전트 만들어줘"
✅ "langgraph-multi-agent.md의 Supervisor 패턴으로 만들어줘"

### 2. 스킬 적극 활용

❌ 직접 Jira API 코딩
✅ `/skill agile-jira --import docs/stories/`

### 3. 컨텍스트 크기 고려

- 빠른 조회: `google-adk-llms.txt` (40KB)
- 상세 구현: `google-adk-llms-full.txt` (3.1MB)

### 4. 검색 활용

```bash
grep -r "StateGraph" .claude/references/
grep -r "handoff" .claude/references/
```

---

## 📋 요구사항

### 필수

- Python 3.10+
- Claude Code CLI
- Anthropic API 키 (에이전트 실행 시)

### 선택 (용도별)

- Tavily API 키 - 웹 검색 에이전트용
- Jira API 토큰 - agile-jira 스킬용

---

## 🎯 예제 에이전트: Company Research

현재 포함된 예제:

**Company Research Agent** - Research-Extraction-Reflection 패턴
- 자동 웹 검색 + 구조화된 데이터 추출
- 비상장 중소기업 특화
- Tavily/Google ADK 멀티 검색 제공자

실행:
```bash
python examples/basic_research.py
```

자세한 문서: [docs/README_DEEP_RESEARCH.md](docs/README_DEEP_RESEARCH.md)

---

## 🔬 딥리서치 커스터마이징 가이드

**핵심 개념: Schema만 바꾸면 어떤 도메인이든 리서치 가능!**

Company Research Agent는 **범용 웹 리서치 엔진**입니다. `extraction_schema`만 변경하면 회사, 제품, 인물, 논문 등 어떤 도메인이든 자동 리서치할 수 있습니다.

### 커스터마이징 3단계

```python
# 1. Schema 정의 (무엇을 추출할지)
custom_schema = {
    "title": "Product Analysis",
    "type": "object",
    "properties": {
        "product_name": {"type": "string"},
        "price": {"type": "string"},
        "features": {"type": "array", "items": {"type": "string"}},
        "reviews_summary": {"type": "string"}
    }
}

# 2. 검색 제공자 선택 (무료 or 유료)
config = Configuration(
    search_provider="serper",  # 무료 2,500 쿼리
    max_search_queries=3
)

# 3. 실행!
result = await graph.ainvoke({
    "company_name": "iPhone 15 Pro",  # 리서치 대상
    "extraction_schema": custom_schema,
    "user_context": "Focus on camera features and battery life"
})
```

**그게 전부입니다!** 나머지 코드(Research-Extraction-Reflection 루프)는 완전히 재사용됩니다.

---

### 8가지 웹 검색 API 비교

다양한 무료/유료 옵션 제공. 자세한 내용은 [deep-research 스킬](.claude/skills/deep-research/references/WEB_SEARCH_APIS.md) 참조.

| Provider | Free Tier | Quality | Best For |
|----------|-----------|---------|----------|
| **Jina AI Reader** | 200 RPM 무료 | ⭐⭐⭐ | 개발/테스트, URL→텍스트 변환 |
| **Serper.dev** | 2,500 lifetime | ⭐⭐⭐⭐ | **무료 프로덕션 최고** |
| **Tavily** | 1,000/월 | ⭐⭐⭐⭐⭐ | 프로덕션 품질 |
| **Exa** | $10 credit or 1k/월 | ⭐⭐⭐⭐ | AI 네이티브 시맨틱 검색 |
| **Brave** | 무료 티어 | ⭐⭐⭐ | 프라이버시 중시 |
| **DuckDuckGo** | 무제한 무료 | ⭐⭐ | 테스트용 (느림) |
| **SerpAPI** | 100/월 | ⭐⭐⭐⭐ | 구글 결과 스크래핑 |
| **Google ADK** | Gemini 2.0+ 무료 | ⭐⭐⭐⭐ | Gemini 사용자 |

**추천:**
- 시작: **DuckDuckGo** (완전 무료, API 키 불필요)
- 프로덕션: **Serper.dev** (2,500 무료 쿼리) 또는 **Tavily** (최고 품질)
- 시맨틱 검색: **Exa** (AI 네이티브)

---

### 빠른 커스터마이징 예제

#### 예제 1: 제품 리서치

```python
PRODUCT_SCHEMA = {
    "title": "Product Research",
    "properties": {
        "product_name": {"type": "string"},
        "manufacturer": {"type": "string"},
        "price_range": {"type": "string"},
        "key_features": {"type": "array", "items": {"type": "string"}},
        "pros": {"type": "array", "items": {"type": "string"}},
        "cons": {"type": "array", "items": {"type": "string"}},
        "user_rating": {"type": "string"},
        "competitors": {"type": "array", "items": {"type": "string"}}
    }
}

config = Configuration(search_provider="serper")  # 무료
result = await graph.ainvoke({
    "company_name": "Sony WH-1000XM5",  # 제품명
    "extraction_schema": PRODUCT_SCHEMA
})
```

#### 예제 2: 인물 리서치 (LinkedIn 프로필 대안)

```python
PERSON_SCHEMA = {
    "title": "Professional Profile",
    "properties": {
        "full_name": {"type": "string"},
        "current_position": {"type": "string"},
        "company": {"type": "string"},
        "education": {"type": "array", "items": {"type": "string"}},
        "work_history": {"type": "array", "items": {"type": "string"}},
        "publications": {"type": "array", "items": {"type": "string"}},
        "social_media": {"type": "object"}
    }
}

result = await graph.ainvoke({
    "company_name": "Dario Amodei",  # 인물명
    "extraction_schema": PERSON_SCHEMA,
    "user_context": "Focus on AI research and Anthropic role"
})
```

#### 예제 3: 학술 논문 리서치

```python
PAPER_SCHEMA = {
    "title": "Research Paper Analysis",
    "properties": {
        "title": {"type": "string"},
        "authors": {"type": "array", "items": {"type": "string"}},
        "publication_date": {"type": "string"},
        "abstract_summary": {"type": "string"},
        "key_findings": {"type": "array", "items": {"type": "string"}},
        "methodology": {"type": "string"},
        "citations_count": {"type": "string"},
        "related_papers": {"type": "array", "items": {"type": "string"}}
    }
}

result = await graph.ainvoke({
    "company_name": "Attention Is All You Need",
    "extraction_schema": PAPER_SCHEMA,
    "user_context": "Focus on transformer architecture"
})
```

#### 예제 4: 경쟁사 분석

```python
COMPETITOR_SCHEMA = {
    "title": "Competitor Analysis",
    "properties": {
        "company_name": {"type": "string"},
        "market_position": {"type": "string"},
        "key_products": {"type": "array", "items": {"type": "string"}},
        "pricing_strategy": {"type": "string"},
        "strengths": {"type": "array", "items": {"type": "string"}},
        "weaknesses": {"type": "array", "items": {"type": "string"}},
        "recent_news": {"type": "array", "items": {"type": "string"}},
        "funding": {"type": "string"}
    }
}

config = Configuration(
    search_provider="tavily",  # 고품질
    max_search_queries=5  # 더 많은 정보
)

result = await graph.ainvoke({
    "company_name": "OpenAI",
    "extraction_schema": COMPETITOR_SCHEMA
})
```

---

### 검색 제공자별 설정 예제

```python
# 완전 무료 (테스트용)
config_free = Configuration(search_provider="duckduckgo")

# 무료 프로덕션 (2,500 쿼리)
config_prod_free = Configuration(search_provider="serper")

# 최고 품질 (유료)
config_premium = Configuration(search_provider="tavily")

# AI 시맨틱 검색
config_semantic = Configuration(search_provider="exa")

# 하이브리드 (비용 절감)
config_hybrid = Configuration(
    search_provider="hybrid"  # Tavily + 무료 조합
)
```

---

### 실전 팁

1. **Schema 설계**
   - 플랫하게 유지 (깊은 중첩 피하기)
   - 각 필드에 명확한 `description` 추가
   - 필수 필드는 최소화

2. **검색 제공자 선택**
   - 개발: DuckDuckGo (무료, 느림)
   - 프로덕션: Serper (2,500 무료) → Tavily (품질)
   - 시맨틱 검색 필요: Exa

3. **비용 최적화**
   - `max_search_queries=3` 으로 시작
   - `max_reflection_steps=1` 으로 제한
   - 무료 티어 모니터링 (Serper 2,500 쿼리)

4. **품질 향상**
   - `user_context`로 검색 방향 제어
   - 구체적인 schema descriptions 작성
   - reflection 활성화 (`max_reflection_steps=2`)

---

### 다음 단계

1. **커스텀 Schema 작성**: `.claude/skills/deep-research/SKILL.md` 참조
2. **API 키 설정**: [WEB_SEARCH_APIS.md](.claude/skills/deep-research/references/WEB_SEARCH_APIS.md) 참조
3. **예제 실행**: `examples/custom_schema.py` 수정 후 실행

**모든 도메인에 적용 가능한 범용 리서치 엔진입니다!** 🚀

---

## 🤝 기여

새 스킬, 에이전트 예제, 레퍼런스 문서 추가를 환영합니다!

### 추가할 만한 것들

- [ ] 더 많은 멀티 에이전트 예제
- [ ] RAG 에이전트 스킬
- [ ] SQL 에이전트 스킬
- [ ] 커스텀 Tool 라이브러리
- [ ] 배포 가이드

---

## 📄 라이선스

MIT License

---

## 🔗 참고 자료

### 공식 문서
- [Google ADK](https://google.github.io/adk-docs/)
- [LangGraph](https://langchain-ai.github.io/langgraph/)
- [Claude Code](https://docs.claude.com/claude-code)

### 커뮤니티
- [LangGraph Examples](https://github.com/langchain-ai/langgraph)
- [Agent Service Toolkit](https://github.com/JoshuaC215/agent-service-toolkit)
- [Claude Code Skills](https://github.com/anthropics/skills)

---

## 🎉 시작하기

1. **레퍼런스 읽기**: `.claude/references/README.md`
2. **스킬 둘러보기**: `.claude/skills/`
3. **예제 실행**: `python examples/basic_research.py`
4. **Claude에게 요청**: "langgraph-multi-agent.md 참고해서 새 에이전트 만들어줘"

**Happy vibe coding! 🚀**

---

**Multi-Agent Workspace** v1.0.0
*For Claude Code vibe coders*
