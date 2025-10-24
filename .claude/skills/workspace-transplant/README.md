# Workspace Transplant - Claude Code 사용 가이드

> 🤖 Claude Code에서 이 스킬을 활용해 멀티 에이전트 아키텍처를 다른 프로젝트에 적용하는 방법

## 🎯 이 스킬이 하는 일

현재 워크스페이스의 **검증된 아키텍처 패턴**을 분석하고, 다른 프로젝트에 이식할 수 있도록 도와줍니다.

**핵심 기능**:
- ✅ 워크스페이스 자동 분석 (6가지 패턴 탐지)
- ✅ 컴포넌트 선택적 추출 (prompts, utils, llm 등)
- ✅ 새 에이전트 자동 생성 (템플릿 기반)
- ✅ A2A 마이그레이션 계획 수립

---

## 🚀 빠른 시작: Claude Code에 이렇게 말하세요

### 시나리오 1: 기존 프로젝트에 컴포넌트 추가하기

```
나 /path/to/my-project 프로젝트에 이 워크스페이스의 rate limiting 패턴을 적용하고 싶어.
어떻게 하면 돼?
```

**Claude가 할 일**:
1. 현재 워크스페이스의 `llm.py` 분석
2. 타겟 프로젝트 구조 파악
3. `llm.py` 추출 및 복사
4. 기존 코드 수정 방법 제시
5. 테스트 방법 안내

---

### 시나리오 2: 워크스페이스 분석

```
이 워크스페이스를 분석해서 어떤 패턴들이 있는지,
어떤 컴포넌트가 재사용 가능한지 리포트 만들어줘.
```

**Claude가 할 일**:
1. `analyze_workspace.py` 스크립트 실행
2. 6가지 패턴 탐지 결과 표시
3. 재사용 가능한 컴포넌트 23개 목록화
4. 의존성 분석
5. 마크다운 리포트 생성

---

### 시나리오 3: 새 프로젝트에 에이전트 추가

```
/path/to/my-project에 문서 요약 에이전트를 추가하고 싶어.
이 워크스페이스의 LangGraph 패턴을 사용해서 만들어줘.
```

**Claude가 할 일**:
1. `scaffold_agent.py` 실행
2. LangGraph 템플릿 기반 에이전트 생성
3. `state.py`, `configuration.py`, `prompts.py`, `graph.py` 생성
4. 커스터마이징 가이드 제공

---

### 시나리오 4: A2A 마이그레이션 계획

```
우리 프로젝트를 A2A 아키텍처로 전환하고 싶어.
이 워크스페이스의 마이그레이션 전략을 참고해서 계획 세워줘.
```

**Claude가 할 일**:
1. `references/migration_strategies.md` 참조
2. 7주 마이그레이션 로드맵 제시
3. Phase별 작업 내용 설명
4. 비용 절감 전략 (91%) 공유
5. Terraform 코드 예제 제공

---

## 💬 실전 대화 예제

### Example 1: 점진적으로 Utils 추가하기

**You:**
```
나 기존 프로젝트 /Users/me/document-processor가 있어.
여기에 이 워크스페이스의 utils.py를 추가하고 싶은데,
기존 코드는 최대한 건드리지 않고 싶어. 어떻게 해?
```

**Claude:**
```
좋습니다! 기존 프로젝트에 utils.py를 안전하게 추가하겠습니다.

1단계: utils.py 추출
[extract_component.py 실행]

2단계: 추출 완료
✓ /Users/me/document-processor/src/common/utils.py 생성됨
✓ /Users/me/document-processor/src/common/__init__.py 생성됨

3단계: 사용 방법
기존 코드에서 이렇게 사용할 수 있습니다:

# src/search.py에 추가
from common.utils import deduplicate_sources

def search(query):
    results = api.search(query)
    unique = deduplicate_sources(results)  # 중복 제거!
    return unique

4단계: 테스트
[테스트 코드 생성]

기존 코드는 전혀 수정하지 않았습니다.
필요한 곳에서만 import해서 사용하시면 됩니다!
```

---

### Example 2: Rate Limiting 문제 해결

**You:**
```
우리 프로젝트에서 Anthropic API rate limit 에러가 자주 나.
이 워크스페이스는 어떻게 해결했어? 같은 방식으로 적용해줘.
```

**Claude:**
```
이 워크스페이스는 InMemoryRateLimiter로 해결했습니다.
바로 적용해드리겠습니다.

1단계: llm.py 모듈 분석
[현재 워크스페이스의 llm.py 읽기]

핵심 전략:
- 0.8 req/sec로 제한 (Anthropic Tier 1 기준)
- Task별 temperature 최적화
- 전역 rate limiter 공유

2단계: 프로젝트에 적용
[llm.py를 /Users/me/project/src/common/으로 복사]

3단계: 기존 코드 수정
[기존 LLM 호출 부분 찾아서 수정]

Before:
llm = ChatAnthropic(model="claude-3-5-sonnet")

After:
from common.llm import get_llm
llm = get_llm(config)

4단계: 테스트
[rate limiting 테스트 실행]

이제 rate limit 에러가 발생하지 않습니다!
```

---

### Example 3: 새 에이전트 추가 (처음부터 베스트 프랙티스)

**You:**
```
새 프로젝트 /Users/me/legal-doc-analyzer에
계약서 분석 에이전트를 만들고 싶어.
이 워크스페이스의 패턴을 사용해서 처음부터 제대로 만들어줘.
```

**Claude:**
```
좋습니다! LangGraph 템플릿으로 contract_analyzer 에이전트를 생성하겠습니다.

1단계: 에이전트 스캐폴딩
[scaffold_agent.py 실행]

생성된 파일:
✓ src/agents/contract_analyzer/__init__.py
✓ src/agents/contract_analyzer/state.py        (TypedDict)
✓ src/agents/contract_analyzer/configuration.py (Pydantic)
✓ src/agents/contract_analyzer/prompts.py      (중앙화)
✓ src/agents/contract_analyzer/graph.py        (LangGraph)

2단계: 도메인 커스터마이징
계약서 분석에 맞게 수정하겠습니다:

[state.py 수정]
- contract_text 필드 추가
- extracted_clauses 필드 추가
- risk_analysis 필드 추가

[prompts.py 수정]
- CLAUSE_EXTRACTION_PROMPT 추가
- RISK_ANALYSIS_PROMPT 추가

[graph.py 수정]
- extract_clauses 노드 추가
- analyze_risks 노드 추가
- 워크플로우: extract → analyze → reflect

3단계: 테스트 코드 생성
[pytest 테스트 파일 생성]

4단계: 사용 예제
from agents.contract_analyzer.graph import create_graph

graph = create_graph()
result = graph.invoke({
    "contract_text": "계약서 내용...",
    "extraction_schema": {...}
})

처음부터 rate limiting, prompt 중앙화, state management가
모두 적용된 프로덕션 수준의 에이전트입니다!
```

---

## 📋 패턴별 적용 가이드

### Pattern 1: Prompts Centralization

**이렇게 말하세요:**
```
프롬프트가 코드 여기저기 흩어져 있어서 관리가 어려워.
이 워크스페이스처럼 prompts.py로 중앙화해줘.
```

**Claude가 할 일:**
1. 기존 코드에서 프롬프트 추출
2. `prompts.py` 생성
3. 변수 치환 (`.format()` 방식)
4. 기존 코드 수정

---

### Pattern 2: Rate Limiting

**이렇게 말하세요:**
```
API rate limit 에러가 나.
이 워크스페이스의 rate limiting 전략 적용해줘.
```

**Claude가 할 일:**
1. `llm.py` 추출
2. InMemoryRateLimiter 설정
3. 기존 LLM 호출 교체
4. Task별 temperature 최적화

---

### Pattern 3: Utils Module

**이렇게 말하세요:**
```
중복 제거, 포맷팅 같은 로직이 여러 곳에 중복돼.
이 워크스페이스의 utils.py를 내 프로젝트에 추가해줘.
```

**Claude가 할 일:**
1. `utils.py` 추출 (8개 함수)
2. 타겟 프로젝트에 복사
3. 사용 예제 제공
4. 기존 중복 코드 리팩토링 제안

---

### Pattern 4: State Management

**이렇게 말하세요:**
```
LangGraph 쓰는데 state가 타입 안전하지 않아.
이 워크스페이스처럼 TypedDict 기반으로 만들어줘.
```

**Claude가 할 일:**
1. 현재 state 구조 분석
2. TypedDict 기반 `state.py` 생성
3. LangGraph 통합
4. 기존 코드 마이그레이션

---

### Pattern 5: Pydantic Configuration

**이렇게 말하세요:**
```
설정 값 검증이 필요해.
이 워크스페이스의 Pydantic configuration 패턴 적용해줘.
```

**Claude가 할 일:**
1. 현재 설정 분석
2. `configuration.py` 생성 (BaseModel)
3. Field 제약조건 추가
4. 기존 dict → Pydantic 마이그레이션

---

### Pattern 6: Multi-Agent Architecture

**이렇게 말하세요:**
```
단일 phase 에이전트를 3-phase (research-extract-reflect)로 확장하고 싶어.
이 워크스페이스 구조를 참고해서 만들어줘.
```

**Claude가 할 일:**
1. `graph.py` 템플릿 기반 생성
2. 3-phase 노드 추가
3. Conditional routing 설정
4. Iteration 로직 구현

---

## 🎓 고급 시나리오

### Scenario A: A2A 마이그레이션 (전체 프로젝트)

**You:**
```
우리 프로젝트 /Users/me/company-research를
이 워크스페이스처럼 A2A 분산 시스템으로 전환하고 싶어.

현재 상황:
- LangGraph 모놀리식 (1개 프로세스)
- 1000개 회사 처리하는데 12시간 걸림
- 비용이 너무 많이 나옴

7주 마이그레이션 계획 세워줘.
```

**Claude:**
```
좋습니다! 이 워크스페이스의 v2.0 → v3.0 마이그레이션 전략을
적용해드리겠습니다.

[references/migration_strategies.md 참조]

📋 7주 마이그레이션 로드맵

Week 1-2: Hybrid Wrapper
✓ 기존 코드 그대로 유지
✓ A2A HTTP 인터페이스만 추가
✓ Docker Compose로 로컬 테스트

[research_agent/app.py 생성]
[coordinator/app.py 생성]

Week 3-4: Infrastructure
✓ AWS 인프라 구축 (Terraform)
✓ ECS Fargate Spot + Aurora Serverless
✓ ElastiCache Redis 추가

[terraform/ 코드 생성]

Week 5-6: Performance Optimization
✓ 1,000개 회사 부하 테스트
✓ 캐싱 전략 (90% hit rate)
✓ Auto-scaling 튜닝

Week 7: Production Deployment
✓ Blue-green deployment
✓ 점진적 트래픽 이동 (10% → 100%)

예상 결과:
- 처리 시간: 12시간 → 90초 (480배 빠름)
- 비용: $5,222/월 → $464/월 (91% 절감)
- 동시 처리: 1개 → 100+개

각 단계별 상세 작업을 진행할까요?
```

---

### Scenario B: 컴포넌트 선택적 이식 (Cherry-picking)

**You:**
```
전체 마이그레이션은 부담스러워.
일단 이 3가지만 적용하고 싶어:
1. Rate limiting (API 에러 해결)
2. Utils (중복 제거 로직)
3. Prompts 중앙화 (유지보수)

우선순위대로 하나씩 적용해줘.
타겟: /Users/me/my-project
```

**Claude:**
```
좋습니다! 저위험 순서대로 적용하겠습니다.

=== Step 1: Utils (충돌 위험 0%, 즉시 효과) ===

[utils.py 추출]
✓ /Users/me/my-project/src/common/utils.py

사용 예제:
from common.utils import deduplicate_sources
unique = deduplicate_sources(search_results)

테스트 실행... ✓ 통과

=== Step 2: Rate Limiting (충돌 위험 낮음) ===

[llm.py 추출]
✓ /Users/me/my-project/src/common/llm.py

기존 코드 3곳 수정:
1. src/agent.py:45 - ChatAnthropic → get_llm
2. src/processor.py:78 - ChatAnthropic → get_llm
3. src/analyzer.py:123 - ChatAnthropic → get_llm

[각 파일 수정]

테스트 실행... ✓ Rate limit 에러 없음

=== Step 3: Prompts 중앙화 ===

기존 프롬프트 발견: 5개
- RESEARCH_PROMPT (agent.py:67)
- EXTRACT_PROMPT (processor.py:89)
- ANALYZE_PROMPT (analyzer.py:134)
- REFLECT_PROMPT (evaluator.py:45)
- SUMMARY_PROMPT (reporter.py:23)

[prompts.py 생성 및 이동]

✓ 완료! 모든 프롬프트가 src/prompts.py에 통합됨

=== 적용 완료 ===

✅ Utils: 8개 함수 사용 가능
✅ Rate limiting: 0.8 req/sec (안전)
✅ Prompts: 5개 프롬프트 중앙화

기존 기능은 모두 정상 작동합니다.
다음 개선사항: State management 또는 Configuration?
```

---

## 🛠️ 트러블슈팅 가이드

### 문제 1: "이미 utils.py가 있어요"

**You:**
```
타겟 프로젝트에 이미 utils.py가 있어.
기존 utils.py를 덮어쓰지 말고,
이 워크스페이스의 함수들을 기존 파일에 추가해줘.
```

**Claude:** (기존 utils.py 읽고 → 함수 병합 → 중복 체크 → 추가)

---

### 문제 2: "import 경로가 달라요"

**You:**
```
우리 프로젝트는 src/common/이 아니라 lib/helpers/ 구조야.
이 경로에 맞게 적용해줘.
```

**Claude:** (경로 자동 조정 → import 문 수정)

---

### 문제 3: "Python 버전이 달라요"

**You:**
```
우리는 Python 3.9 쓰는데,
이 워크스페이스는 3.10+ 문법 쓰네?
호환되게 수정해줘.
```

**Claude:** (3.9 호환 문법으로 변환 → match/case 제거 → type hints 조정)

---

## 📚 참고 문서 활용

스킬 내부 문서를 참조하고 싶을 때:

**You:**
```
이 워크스페이스의 아키텍처 패턴 6가지를
상세하게 설명해줘. references/architecture_patterns.md 읽고.
```

**Claude:** (architecture_patterns.md 읽고 → 6가지 패턴 상세 설명)

---

**You:**
```
A2A 마이그레이션 비용 분석 보여줘.
v2.0과 v3.0 비용 비교해서 표로 만들어줘.
```

**Claude:** (project_docs_summary.md 읽고 → 비용 비교표 생성)

---

## 🎯 Best Practices

### ✅ DO (이렇게 요청하세요)

```
✓ "이 워크스페이스의 rate limiting 패턴을 내 프로젝트에 적용해줘"
✓ "단계별로 하나씩 적용하면서 매번 테스트해줘"
✓ "기존 코드는 최대한 건드리지 말고, 새 파일로 추가해줘"
✓ "충돌 위험 낮은 것부터 시작해줘"
```

### ❌ DON'T (이렇게 요청하지 마세요)

```
✗ "전체 워크스페이스를 복사해서 붙여넣어줘" (위험!)
✗ "기존 코드 다 지우고 새로 작성해줘" (위험!)
✗ "한 번에 다 적용해줘" (디버깅 어려움)
✗ "테스트 없이 바로 프로덕션에 배포해줘" (위험!)
```

---

## 🚦 추천 워크플로우

### Phase 1: 분석 (5분)

```
"이 워크스페이스 분석해줘.
어떤 패턴들이 있고, 내 프로젝트에 어떤 걸 적용하면 좋을지 추천해줘."
```

### Phase 2: 저위험 적용 (1-2시간)

```
"Utils 모듈만 먼저 추가해줘.
기존 코드는 안 건드리고, 새로운 파일로만."
```

### Phase 3: 중위험 적용 (반나절)

```
"Rate limiting 적용해줘.
기존 LLM 호출 부분만 교체하고, 하나씩 테스트하면서."
```

### Phase 4: 점진적 확장 (1-2주)

```
"새 에이전트 추가할 때 템플릿 사용해서 만들어줘.
기존 에이전트는 나중에 천천히 리팩토링하자."
```

---

## 📞 추가 도움이 필요하면

### 구체적인 상황 공유하기

```
상황:
- 프로젝트 경로: /Users/me/my-project
- 현재 문제: [문제 설명]
- 적용하고 싶은 패턴: [패턴 이름]
- 제약사항: [있다면]

이런 상황에서 어떻게 적용해야 할까?
```

**Claude가 맞춤형 솔루션 제공합니다!**

---

## 🎉 요약

### Claude Code에서 이 스킬 사용하는 3단계

1. **분석**: "이 워크스페이스 분석해줘"
2. **선택**: "utils랑 rate limiting만 내 프로젝트에 적용해줘"
3. **확장**: "새 에이전트는 템플릿으로 만들어줘"

### 핵심 원칙

- 🎯 **구체적으로**: "rate limiting 적용해줘" (O) vs "개선해줘" (X)
- 📍 **경로 명시**: 타겟 프로젝트 경로 제공
- 🔄 **점진적으로**: 한 번에 하나씩
- ✅ **테스트**: 각 단계마다 확인

---

**이제 바로 시작하세요!** 🚀

```
"Claude, 이 워크스페이스 분석해줘!"
```
