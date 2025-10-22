# ADK 분석 기반 개선 사항

> Google ADK 샘플 분석을 통해 도출된 실행 가능한 개선사항

**작성일**: 2025-10-22
**우선순위**: ⭐⭐⭐ (높음) → ⭐ (낮음)

---

## 즉시 적용 가능 (v2.1)

### 1. Evaluation Framework 구축 ⭐⭐⭐

**출처**: ADK samples의 `eval/` 패턴

**현재 문제**:
- 품질 측정 수동
- 개선 효과 정량화 어려움
- Reflection 효과 불명확

**구현 계획**:

```
company-search-agent/
└── eval/
    ├── __init__.py
    ├── baseline_data.json          # 10개 회사 기대 결과
    ├── test_completeness.py        # 완성도 점수
    ├── test_cost.py                # API 비용 추적
    └── test_reflection_roi.py      # Reflection 효과 측정
```

**Baseline Dataset 예시**:
```json
{
  "Anthropic": {
    "expected_fields": {
      "company_name": "Anthropic",
      "founded": "2021",
      "founders": ["Dario Amodei", "Daniela Amodei"],
      "industry": "AI Safety"
    },
    "completeness_threshold": 0.8
  }
}
```

**테스트 코드**:
```python
# eval/test_completeness.py
import pytest
from src.agent import build_research_graph, Configuration

@pytest.mark.asyncio
async def test_anthropic_completeness():
    graph = build_research_graph(Configuration())
    result = await graph.ainvoke({...})

    assert result["completeness_score"] >= 0.8
    assert "founded" in result["extracted_data"]
```

**예상 소요**: 2-3일

---

### 2. Deployment Scripts ⭐⭐

**출처**: ADK samples의 `deployment/` 패턴

**현재 문제**:
- 배포 방법 불명확
- 수동 설정 필요
- 프로덕션 준비 안됨

**구현 계획**:

```
company-search-agent/
└── deployment/
    ├── docker/
    │   ├── Dockerfile
    │   └── docker-compose.yml
    ├── api/
    │   ├── main.py                 # FastAPI server
    │   └── requirements-api.txt
    └── scripts/
        ├── deploy_cloud_run.sh
        └── test_deployment.sh
```

**FastAPI 래퍼**:
```python
# deployment/api/main.py
from fastapi import FastAPI
from src.agent import build_research_graph, Configuration

app = FastAPI()

@app.post("/research")
async def research_company(company_name: str, schema: dict = None):
    graph = build_research_graph(Configuration())
    result = await graph.ainvoke({
        "company_name": company_name,
        "extraction_schema": schema or DEFAULT_SCHEMA,
        ...
    })
    return result["extracted_data"]
```

**Dockerfile**:
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "deployment.api.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

**예상 소요**: 3-4일

---

### 3. Adaptive Rate Limiting ⭐⭐⭐

**출처**: FOMC Research의 `rate_limit_callback`

**현재 구현**:
```python
# llm.py
_rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.8,  # 고정
    ...
)
```

**개선안**:
```python
# llm.py
class AdaptiveRateLimiter:
    """429 에러 감지 시 자동으로 속도 조절"""

    def __init__(self, initial_rate=0.8, min_rate=0.2, max_rate=2.0):
        self.current_rate = initial_rate
        self.min_rate = min_rate
        self.max_rate = max_rate
        self.error_count = 0
        self.success_count = 0

    async def acquire(self):
        # Rate limit 적용
        await asyncio.sleep(1.0 / self.current_rate)

    def on_error(self, error):
        """429 에러 시 속도 절반으로"""
        if "429" in str(error) or "Resource Exhausted" in str(error):
            self.current_rate = max(self.current_rate * 0.5, self.min_rate)
            self.error_count += 1
            print(f"⚠️ Rate limit hit. Slowing down to {self.current_rate:.2f} req/sec")

    def on_success(self):
        """성공 시 점진적 회복"""
        self.success_count += 1
        if self.success_count >= 10 and self.error_count > 0:
            self.current_rate = min(self.current_rate * 1.1, self.max_rate)
            self.success_count = 0
```

**사용법**:
```python
# llm.py
_rate_limiter = AdaptiveRateLimiter()

def get_llm(config, temperature=None):
    try:
        await _rate_limiter.acquire()
        response = await llm.ainvoke(...)
        _rate_limiter.on_success()
        return response
    except Exception as e:
        _rate_limiter.on_error(e)
        raise
```

**예상 소요**: 1-2일

---

## 중기 개선 (v2.2)

### 4. 모듈 구조 개선 ⭐

**출처**: ADK samples의 `sub_agents/` 분리 패턴

**현재 구조**:
```
src/agent/
├── research.py       # 단일 파일
├── extraction.py
└── reflection.py
```

**개선안**:
```
src/agent/
├── phases/                      # Rename
│   ├── __init__.py
│   ├── research.py
│   ├── extraction.py
│   └── reflection.py
├── specialized/                 # NEW (future)
│   ├── __init__.py
│   ├── indirect_source_agent.py  # 공시자료 전문
│   ├── news_agent.py            # 뉴스 수집
│   └── social_agent.py          # SNS 크롤링
└── tools/                       # NEW
    ├── __init__.py
    ├── search_tools.py
    └── extraction_tools.py
```

**장점**:
- 책임 분리 명확
- 테스트 용이
- 확장성 향상

**예상 소요**: 2-3일

---

### 5. Logging 및 Monitoring 강화 ⭐⭐

**출처**: ADK samples의 structured logging

**현재 문제**:
- `print()` 사용
- 로그 레벨 없음
- 추적 어려움

**개선안**:
```python
# src/agent/logging_config.py
import logging
from datetime import datetime

def setup_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Console handler
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # File handler (optional)
    file_handler = logging.FileHandler(f'logs/{name}_{datetime.now():%Y%m%d}.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# research.py
logger = setup_logger("research")

async def research_node(state, config):
    logger.info(f"Starting research for {state['company_name']}")
    logger.debug(f"Queries: {queries}")
    logger.warning(f"Search failed: {e}")
```

**예상 소요**: 1일

---

## 장기 계획 (v3.0)

### 6. Google ADK 별도 버전 구현 ⭐⭐⭐

**목표**: 비용 절감 및 실험

**Phase 1: PoC (1-2주)**

```
company-search-agent-adk/        # 새 디렉토리
├── adk_agent/
│   ├── agent.py                 # Root coordinator
│   ├── sub_agents/
│   │   ├── web_search_agent.py  # Google Search (무료)
│   │   └── extraction_agent.py
│   ├── prompts.py
│   └── tools/
├── pyproject.toml               # uv 기반
├── .env.example
└── README_ADK.md
```

**검증 사항**:
1. Google Search 무료 사용 (Gemini 2.5 Flash)
2. 비용 비교 (vs LangGraph)
3. 품질 비교

**예상 비용 절감**: 85-95%

**Phase 2: Feature Parity (2-4주)**
- Reflection loop
- Custom schema
- PostgreSQL 통합

**Phase 3: ADK 고유 기능 (1-2개월)**
- Multi-modal (PDF, 비디오)
- BigQuery 통합
- Vertex AI 배포

---

### 7. Multi-modal Support ⭐

**출처**: Academic Research의 PDF 입력

**타겟 데이터**:
- 회사 발표자료 (PDF)
- YouTube 회사 소개 영상
- 웹사이트 스크린샷

**요구사항**:
- Gemini 2.5 Flash (multi-modal)
- 또는 Claude 3.5 Sonnet (vision)

**예상 구현**: v3.0 (ADK 버전)

---

## 우선순위 로드맵

### 즉시 (1-2주)

1. ✅ Evaluation Framework (3일)
2. ✅ Adaptive Rate Limiting (2일)
3. ✅ Deployment Scripts (4일)

**총 소요**: ~9일 (2주)

### 중기 (3-4주)

4. ✅ 모듈 구조 개선 (3일)
5. ✅ Logging 강화 (1일)

**총 소요**: 4일

### 장기 (2-3개월)

6. ✅ Google ADK PoC (2주)
7. ✅ ADK Feature Parity (4주)
8. ✅ Multi-modal Support (4주)

**총 소요**: 10주

---

## 비용/효과 분석

| 개선사항 | 소요 시간 | 비용 절감 | 품질 향상 | 우선순위 |
|---------|----------|----------|----------|---------|
| Evaluation Framework | 3일 | - | ⭐⭐⭐ | ⭐⭐⭐ |
| Deployment Scripts | 4일 | - | ⭐⭐ | ⭐⭐ |
| Adaptive Rate Limiting | 2일 | ⭐ | ⭐⭐ | ⭐⭐⭐ |
| Logging 강화 | 1일 | - | ⭐ | ⭐⭐ |
| 모듈 구조 개선 | 3일 | - | ⭐ | ⭐ |
| **Google ADK PoC** | **2주** | **⭐⭐⭐** | **?** | **⭐⭐⭐** |

---

## 결론

### 즉시 시작 권장

1. **Evaluation Framework** (가장 중요)
   - 품질 개선 추적 필수
   - Reflection ROI 측정

2. **Adaptive Rate Limiting**
   - 프로덕션 안정성
   - 간단한 구현

3. **Deployment Scripts**
   - 실전 사용 준비
   - Docker + FastAPI

### ADK 버전은 별도 실험

- 현재 LangGraph 버전 유지
- ADK는 비용 절감 실험용
- 양쪽 모두 장점 있음

---

**작성**: 2025-10-22
**검토 주기**: 매주
**다음 체크포인트**: Evaluation Framework 완료 후
