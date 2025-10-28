# Company-Researcher vs Current Project - 비교 분석

**분석일**: 2025-10-22
**비교 대상**: langchain-ai/company-researcher vs 현재 프로젝트

---

## 1. 아키텍처 비교

### Graph 구조

| 측면 | company-researcher | 현재 프로젝트 | 평가 |
|------|-------------------|--------------|------|
| **노드 분리** | generate_queries 별도 노드 | research 노드에 통합 | ⚠️ company-researcher가 더 세밀 |
| **워크플로우** | START → generate_queries → research → extract → reflect → (loop/END) | START → research → extract → reflect → (loop/END) | ⚠️ company-researcher가 명확 |
| **State 타입** | @dataclass (InputState, OverallState, OutputState) | TypedDict (ResearchState) | ⚠️ dataclass가 더 안전 |

**권장**: generate_queries를 별도 노드로 분리하여 재사용성 향상

---

## 2. Configuration 관리

### company-researcher
```python
@dataclass(kw_only=True)
class Configuration:
    max_search_queries: int = 3
    max_search_results: int = 3
    max_reflection_steps: int = 0
    include_search_results: bool = False

    @classmethod
    def from_runnable_config(cls, config: Optional[RunnableConfig] = None):
        # 환경 변수 + RunnableConfig 통합
```

### 현재 프로젝트
```python
class Configuration(BaseModel):
    max_search_queries: int = 3
    max_search_results: int = 3
    max_reflection_steps: int = 1
    llm_model: str = "claude-sonnet-4-5-20250929"
    temperature: float = 0.7
```

**차이점**:
- ✅ 현재 프로젝트: Pydantic 검증 + llm_model/temperature 설정
- ⚠️ company-researcher: `from_runnable_config` 메서드 (더 유연)
- ⚠️ company-researcher: `include_search_results` 옵션 (출력 제어)

**권장**: `from_runnable_config` 패턴 + `include_search_results` 추가

---

## 3. Prompts 관리

### company-researcher
- **별도 파일**: `prompts.py`에 모든 프롬프트 분리
- **상수화**: `EXTRACTION_PROMPT`, `QUERY_WRITER_PROMPT`, `INFO_PROMPT`, `REFLECTION_PROMPT`
- **장점**: 프롬프트 버전 관리 용이, 테스트 가능, 재사용성

### 현재 프로젝트
- **인라인 프롬프트**: 각 노드 함수 내부에 직접 작성
- **단점**: 중복 가능, 관리 어려움

**권장**: ✅ 프롬프트를 `prompts.py`로 분리 (최우선 개선사항)

---

## 4. Utility Functions

### company-researcher
```python
# utils.py
def deduplicate_sources(search_response) -> list[dict]
def format_sources(sources_list, include_raw_content=True, max_tokens_per_source=1000) -> str
def format_all_notes(completed_notes: list[str]) -> str
```

**기능**:
- URL 기반 중복 제거
- 토큰 제한 (max_tokens_per_source=1000)
- 출처 포맷팅 (title, URL, content, raw_content 구분)

### 현재 프로젝트
```python
# research.py 내부
def format_search_results(results: List[Dict[str, Any]]) -> str
```

**차이점**:
- ⚠️ 중복 제거 로직 없음
- ⚠️ 토큰 제한 없음 (LLM 컨텍스트 오버플로우 위험)
- ⚠️ raw_content 활용 안 함

**권장**: ✅ `utils.py` 생성하여 유틸리티 함수 분리

---

## 5. Rate Limiting

### company-researcher
```python
from langchain_core.rate_limiters import InMemoryRateLimiter

rate_limiter = InMemoryRateLimiter(
    requests_per_second=4,
    check_every_n_seconds=0.1,
    max_bucket_size=10,
)
claude_3_5_sonnet = ChatAnthropic(
    model="claude-3-5-sonnet-latest",
    temperature=0,
    rate_limiter=rate_limiter
)
```

**장점**:
- API rate limit 보호
- 비용 제어
- 프로덕션 안정성

### 현재 프로젝트
- ❌ Rate limiting 없음

**권장**: ✅ Rate limiter 추가 (특히 프로덕션 환경)

---

## 6. State 관리 패턴

### company-researcher (3-tier State)
```python
@dataclass(kw_only=True)
class InputState:          # 사용자 입력 인터페이스
    company: str
    extraction_schema: dict[str, Any]
    user_notes: Optional[dict[str, Any]]

@dataclass(kw_only=True)
class OverallState:        # 내부 상태 (모든 필드)
    company: str
    extraction_schema: dict[str, Any]
    user_notes: str
    search_queries: list[str]
    search_results: list[dict]
    completed_notes: Annotated[list, operator.add]
    info: dict[str, Any]
    is_satisfactory: bool
    reflection_steps_taken: int

@dataclass(kw_only=True)
class OutputState:         # 출력 인터페이스
    info: dict[str, Any]
    search_results: list[dict]
```

**장점**:
- 명확한 입출력 인터페이스
- 내부 구현 숨김 (캡슐화)
- API 버전 관리 용이

### 현재 프로젝트 (단일 State)
```python
class ResearchState(TypedDict):
    company_name: str
    extraction_schema: Dict[str, Any]
    user_context: str
    research_queries: List[str]
    search_results: List[Dict[str, Any]]
    research_notes: str
    extracted_data: Dict[str, Any]
    reflection_count: int
    missing_fields: List[str]
    follow_up_queries: List[str]
    is_complete: bool
    messages: Annotated[List[BaseMessage], add_messages]
```

**권장**: ⚠️ 3-tier State 패턴 고려 (API 제공 시 유용)

---

## 7. Research Notes 누적

### company-researcher
```python
completed_notes: Annotated[list, operator.add] = field(default_factory=list)
```
- **Annotated[list, operator.add]**: 여러 검색 결과를 누적
- Reflection 후 재검색 시 이전 노트 보존

### 현재 프로젝트
```python
research_notes: str
```
- **덮어쓰기**: Reflection 후 이전 노트 손실

**권장**: ✅ 누적 패턴 적용 (operator.add)

---

## 8. Error Handling

### 현재 프로젝트 (양호)
```python
try:
    extracted = await chain.ainvoke({...})
except Exception as e:
    print(f"Extraction error: {e}")
    # Fallback: return empty structure
    extracted = {...}
```

### company-researcher (비슷)
- 거의 동일한 수준

**권장**: ⚠️ Logging 강화 (print → logger), Retry 로직 추가 (tenacity)

---

## 9. LLM 호출 패턴

### company-researcher
```python
structured_llm = claude_3_5_sonnet.with_structured_output(Queries)
```
- Pydantic 모델 기반 구조화 출력

### 현재 프로젝트
```python
parser = JsonOutputParser()
chain = prompt | llm | parser
```
- JsonOutputParser 사용

**차이점**: 둘 다 유효하지만, Pydantic 모델이 더 안전 (타입 검증)

---

## 10. Schema 설계 비교

### company-researcher (단순)
```python
DEFAULT_EXTRACTION_SCHEMA = {
    "company_name": {"type": "string"},
    "founding_year": {"type": "integer"},
    "founder_names": {"type": "array", "items": {"type": "string"}},
    "product_description": {"type": "string"},
    "funding_summary": {"type": "string"},
    "required": ["company_name"]
}
```

### 현재 프로젝트 (상세)
```python
DEFAULT_SCHEMA = {
    "company_name": {...},
    "founded": {...},
    "headquarters": {...},
    "industry": {...},
    "description": {...},
    "products": {...},
    "key_people": {  # 중첩 객체!
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "name": {...},
                "role": {...}
            }
        }
    },
    "revenue": {...},
    "employee_count": {...},
    "website": {...},
    "required": ["company_name", "description"]
}
```

**차이점**:
- ✅ 현재 프로젝트: 더 상세하고 실용적 (industry, products, revenue 등)
- ⚠️ 중첩 객체 (key_people): company-researcher README 경고 "LLMs have challenges with nested objects"

**권장**: 현재 스키마 유지, 하지만 중첩 깊이 제한

---

## 11. Reflection 로직

### company-researcher
```python
class ReflectionOutput(BaseModel):
    is_satisfactory: bool
    missing_fields: list[str]
    search_queries: list[str]
    reasoning: str

# LLM이 구조화된 Reflection 반환
```

### 현재 프로젝트
```python
def evaluate_completeness(extracted, schema) -> tuple[List[str], float]:
    # 프로그래매틱 평가
    ...

# + LLM 기반 follow-up 쿼리 생성
```

**차이점**:
- ✅ 현재 프로젝트: 프로그래매틱 + LLM 하이브리드 (더 안정적)
- ⚠️ company-researcher: 순수 LLM 판단 (비용 증가)

**권장**: 현재 패턴 유지 (하이브리드가 우수)

---

## 12. Tavily Search 활용

### company-researcher
```python
await tavily_async_client.search(
    query,
    max_results=max_search_results,
    include_raw_content=True,
    topic="general",
)

# raw_content를 max_tokens_per_source=1000으로 제한
```

### 현재 프로젝트
```python
search_tool = TavilySearchResults(
    max_results=config.max_search_results,
    search_depth="advanced",
    include_raw_content=True
)
```

**차이점**:
- ✅ 현재: `search_depth="advanced"` (더 깊은 검색)
- ⚠️ company-researcher: 토큰 제한 로직 (컨텍스트 오버플로우 방지)

**권장**: ✅ 토큰 제한 추가

---

## 📋 개선 우선순위

### 🔴 High Priority (즉시 적용)

1. **프롬프트 분리** (`prompts.py`)
2. **유틸리티 함수 추가** (`utils.py`: deduplicate_sources, format_sources)
3. **Rate Limiter 추가**
4. **토큰 제한** (max_tokens_per_source=1000)
5. **Research Notes 누적** (operator.add)

### 🟡 Medium Priority (1-2주)

6. **generate_queries 노드 분리**
7. **Configuration.from_runnable_config** 메서드 추가
8. **include_search_results** 옵션 추가
9. **Logging 강화** (print → logger)
10. **Retry 로직** (tenacity)

### 🟢 Low Priority (선택사항)

11. **3-tier State 패턴** (InputState, OverallState, OutputState)
12. **Pydantic 모델 기반 구조화 출력** (Queries, ReflectionOutput)

---

## 🎯 현재 프로젝트 강점 (유지)

- ✅ 더 상세한 스키마 (industry, products, revenue, key_people)
- ✅ Pydantic Configuration (검증 강화)
- ✅ 하이브리드 Reflection (프로그래매틱 + LLM)
- ✅ search_depth="advanced" (Tavily)
- ✅ 명확한 문서화 (CLAUDE.md, README 등)

---

## 🔄 적용 계획

1. **Phase 1**: 프롬프트 분리 + 유틸리티 함수 (30분)
2. **Phase 2**: Rate Limiter + 토큰 제한 (20분)
3. **Phase 3**: Research Notes 누적 + generate_queries 분리 (40분)
4. **Phase 4**: Configuration 개선 + Logging (30분)

**총 예상 시간**: ~2시간

---

**결론**: company-researcher는 프로덕션 안정성과 모듈화에 강점, 현재 프로젝트는 기능 풍부함과 분석 깊이에 강점. 두 장점을 결합하면 최적의 시스템 구축 가능.
