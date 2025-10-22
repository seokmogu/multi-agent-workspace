# LLM 및 클라우드 서비스 가격 비교 (2025년 10월 기준)

> **최종 업데이트**: 2025-10-22 (공식 가격 페이지 직접 확인 완료)
> **목적**: 기업 데이터 수집 에이전트를 위한 비용 효율적인 LLM 및 클라우드 인프라 선택
> **출처**:
> - OpenAI: https://openai.com/api/pricing/ (2025-10-22 확인)
> - Anthropic: https://docs.claude.com/en/docs/about-claude/models (2025-10-22 확인)
> - Google Gemini: https://ai.google.dev/gemini-api/docs/pricing (2025-10-22 확인)

---

## 📊 목차

1. [LLM 모델 가격 비교](#llm-모델-가격-비교)
2. [클라우드 서비스 가격 비교](#클라우드-서비스-가격-비교)
3. [비용 효율 분석](#비용-효율-분석)
4. [권장 조합](#권장-조합)

---

## LLM 모델 가격 비교

### 1️⃣ OpenAI (2025년 10월) - Standard Tier

| 모델 | 입력 ($/1M tokens) | 출력 ($/1M tokens) | 특징 |
|------|-------------------|-------------------|------|
| **gpt-5** | $1.25 | $10.00 | 최신 플래그십 모델 |
| **gpt-5-mini** | $0.25 | $2.00 | 비용 효율적 |
| **gpt-5-nano** | $0.05 | $0.40 | 초경량 모델 |
| **gpt-4.1** | $2.00 | $8.00 | GPT-4 시리즈 최신 |
| **gpt-4.1-mini** | $0.40 | $1.60 | 경량 버전 |
| **gpt-4.1-nano** | $0.10 | $0.40 | 초경량 버전 |
| **gpt-4o** | $2.50 | $10.00 | 멀티모달 (이미지, 오디오) |
| **gpt-4o-mini** | $0.15 | $0.60 | **가장 저렴한 멀티모달** ⭐ |
| **o4-mini** | $1.10 | $4.40 | 추론 최적화 |
| **o3** | $2.00 | $8.00 | 추론 모델 |
| **o3-mini** | $1.10 | $4.40 | 추론 경량 |
| **o1** | $15.00 | $60.00 | 고급 추론 |

**캐싱 가격 (Cached Input):**
- gpt-5: $0.125 (90% 할인)
- gpt-4o: $1.25 (50% 할인)
- gpt-4o-mini: $0.075 (50% 할인)

**출처**: https://openai.com/api/pricing/

**권장 모델:**
- **범용 + 최저가**: gpt-4o-mini ($0.15/$0.60)
- **품질 우선**: gpt-5 ($1.25/$10.00)
- **멀티모달**: gpt-4o ($2.50/$10.00)
- **추론**: o4-mini ($1.10/$4.40)

---

### 2️⃣ Anthropic Claude (2025년 10월)

| 모델 | 입력 ($/1M tokens) | 출력 ($/1M tokens) | 특징 |
|------|-------------------|-------------------|------|
| **Claude Sonnet 4.5** | $3.00 | $15.00 | 최신 모델, 코딩/에이전트 최적화 ⭐ |
| **Claude Haiku 4.5** | $1.00 | $5.00 | 가장 빠른 모델 |
| **Claude Opus 4.1** | $15.00 | $75.00 | 최고 성능 추론 |
| **Claude Sonnet 4** | $3.00 | $15.00 | 이전 세대 (레거시) |
| **Claude Sonnet 3.7** | $3.00 | $15.00 | Extended thinking 지원 |
| **Claude Haiku 3.5** | $0.80 | $4.00 | 레거시 |
| **Claude Haiku 3** | $0.25 | $1.25 | 레거시 |

**출처**: https://docs.claude.com/en/docs/about-claude/models

**컨텍스트 윈도우:**
- Claude Sonnet 4.5: 200K tokens (기본), 1M tokens (베타)
- Claude Haiku 4.5: 200K tokens
- Claude Opus 4.1: 200K tokens

**프롬프트 캐싱 & 배치 처리:**
- 프롬프트 캐싱: 최대 90% 절감
- 배치 API: 50% 할인

**권장 모델:**
- **메인 작업**: Claude Sonnet 4.5 ($3/$15) + 프롬프트 캐싱
- **빠른 응답**: Claude Haiku 4.5 ($1/$5)
- **최고 품질**: Claude Opus 4.1 ($15/$75)

---

### 3️⃣ Google Gemini (2025년 10월)

| 모델 | 입력 ($/1M tokens) | 출력 ($/1M tokens) | 특징 |
|------|-------------------|-------------------|------|
| **Gemini 2.5 Pro** | $1.25-2.50 | $10.00-15.00 | 최고 성능 |
| **Gemini 2.5 Flash** | $0.30 | $2.50 | Thinking 기본 활성화 |
| **Gemini 2.5 Flash-Lite** | $0.10 | $0.40 | 경량 모델 |
| **Gemini 2.0 Flash** | $0.10 | $0.40 | **범용, 추천** ⭐ |
| **Gemini 2.0 Flash-Lite** | $0.075 | $0.30 | 초경량 |

**출처**: https://ai.google.dev/gemini-api/docs/pricing

**멀티모달 가격:**
- 텍스트, 이미지, 비디오: 동일 가격
- 오디오: 추가 $0.70-1.00/1M tokens

**추가 서비스:**
- Batch API: 50% 할인
- 무료 티어: 제한된 사용량

**주요 특징:**
- **google_search 도구**: 무료 웹 검색 (Gemini 2+ 전용, Google ADK 필요)
- **VertexAiSearchTool**: 기업 데이터 검색

**권장 모델:**
- **비용 최우선**: Gemini 2.0 Flash ($0.10/$0.40)
- **멀티모달**: Gemini 2.5 Flash ($0.30/$2.50)

---

## 클라우드 서비스 가격 비교

### 1️⃣ Google Cloud Run

**가격:**
- CPU: $0.00002400/vCPU-초
- 메모리: $0.00000250/GiB-초
- 요청: $0.40/1M

**예상 비용 (1,000개 기업, 각 5분):**
- CPU (2 vCPU): $14.40
- 메모리 (4GB): $3.00
- 요청: $0.40
- **총계: ~$18/월**

**장점:**
- Scale to Zero (비용 없음)
- Google ADK 네이티브 통합
- google_search 무료

---

### 2️⃣ AWS Lambda

**무료 티어:**
- 월 1M 요청
- 400,000 GB-초

**유료:**
- 요청: $0.20/1M
- 컴퓨팅: 메모리 기반
- Graviton2 (ARM): 34% 저렴

**예상 비용 (1,000개 기업, 각 10분):**
- **총계: ~$20/월** (무료 티어 내)

---

### 3️⃣ Modal (AI 특화)

**무료 크레딧: $30/월**
- CPU 사용량 기반
- GPU: $6.25/시간 (B200)

**예상 비용:**
- 소규모: **$30 이하** (무료 크레딧)

---

### 4️⃣ Railway

**플랜:**
- Trial: $5 크레딧 (1회)
- Starter: $5/월

**자동 슬립:**
- 10분 비활성 → Sleep
- 슬립 중 비용 없음

---

## 비용 효율 분석

### 시나리오: 월 1,000개 기업 조사

**가정:**
- 기업당 10개 웹 검색
- 평균 처리 시간: 5분
- 입력: 20k tokens, 출력: 5k tokens
- Reflection 1회

---

### 조합 1: **Gemini 2.0 Flash + Cloud Run** (최저가)

| 항목 | 비용 |
|------|------|
| LLM (Gemini 2.0 Flash) | 1,000 × (20k×$0.10 + 5k×$0.40)/1M = **$4.00** |
| 웹 검색 (google_search) | **$0** (무료) |
| Cloud Run | **$18** |
| **총계** | **$22/월** ⭐ |

---

### 조합 2: **GPT-4o-mini + Lambda** (OpenAI 최저가)

| 항목 | 비용 |
|------|------|
| LLM (GPT-4o-mini) | 1,000 × (20k×$0.15 + 5k×$0.60)/1M = **$6.00** |
| 웹 검색 (Tavily) | 10,000 × $0.005 = **$50** |
| AWS Lambda | **$20** |
| **총계** | **$76/월** |

---

### 조합 3: **Claude Sonnet 4.5 + Modal** (품질 우선)

| 항목 | 비용 |
|------|------|
| LLM (Claude Sonnet 4.5) | 1,000 × (20k×$3 + 5k×$15)/1M = **$135** |
| 프롬프트 캐싱 (-90%) | **$13.50** |
| 웹 검색 (Tavily) | **$50** |
| Modal | **$30** (무료 크레딧) |
| **총계** | **$93.50/월** |

---

### 조합 4: **하이브리드** (추천)

| 항목 | 비용 |
|------|------|
| Claude Sonnet 4.5 (메인 추론, 캐싱) | **$20** |
| Gemini 2.0 Flash (멀티모달) | **$2** |
| google_search (웹 검색) | **$0** |
| Cloud Run | **$18** |
| **총계** | **$40/월** ⭐⭐ |

---

## 권장 조합

### 🥇 **최저가: Gemini 2.0 Flash Only** - $22/월

```yaml
LLM: Gemini 2.0 Flash ($0.10/$0.40)
웹 검색: google_search (무료)
멀티모달: Gemini 2.5 Flash
배포: Google Cloud Run

비용: $22/월
```

**적합:**
- 예산 최우선
- 웹 검색 무료 필요
- 품질 타협 가능

---

### 🥈 **균형: 하이브리드** - $40/월

```yaml
메인 LLM: Claude Sonnet 4.5 (프롬프트 캐싱 -90%)
멀티모달: Gemini 2.0 Flash
웹 검색: google_search (무료)
배포: Google Cloud Run

비용: $40/월
```

**적합:**
- 품질과 비용 균형
- 프롬프트 캐싱 활용
- 멀티모달 필요

---

### 🥉 **OpenAI: GPT-4o-mini** - $76/월

```yaml
LLM: GPT-4o-mini ($0.15/$0.60)
웹 검색: Tavily API
배포: AWS Lambda

비용: $76/월
```

**적합:**
- OpenAI 생태계 선호
- 간단한 통합

---

### 🏆 **품질 우선: Claude** - $94/월

```yaml
LLM: Claude Sonnet 4.5 (프롬프트 캐싱)
웹 검색: Tavily API
배포: Modal

비용: $94/월
```

**적합:**
- 품질이 최우선
- 복잡한 추론 작업

---

## 실전 구현 예시

### 하이브리드 아키텍처

```python
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from google.adk.tools import google_search

# 메인 LLM: Claude Sonnet 4.5 (추론)
claude = ChatAnthropic(
    model="claude-sonnet-4-5-20250929",  # 최신 모델
    temperature=0.3,
)

# 멀티모달: Gemini
gemini = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0
)

# 웹 검색: google_search (무료)
from google.adk.agents import Agent
search_agent = Agent(
    model="gemini-2.0-flash",
    tools=[google_search]
)
```

### 프롬프트 캐싱 (Claude)

```python
from anthropic import Anthropic

client = Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "기업 분석 전문가 역할...",  # 반복되는 긴 프롬프트
            "cache_control": {"type": "ephemeral"}  # 90% 절감
        }
    ],
    messages=[
        {"role": "user", "content": f"Analyze {company}"}
    ]
)
```

---

## 결론 및 다음 단계

### 🎯 최종 권장사항

| 우선순위 | 조합 | 월 비용 | 적합 시나리오 |
|---------|------|--------|-------------|
| **1위** | Gemini Only | $22 | 초기 PoC, 예산 제한 |
| **2위** | 하이브리드 (Claude+Gemini) | $40 | 프로덕션 (품질+비용) |
| **3위** | GPT-4o-mini | $76 | OpenAI 생태계 |
| **4위** | Claude Only | $94 | 최고 품질 필요 |

### 단계별 전략

**Phase 1: PoC (1개월)**
- Gemini 2.0 Flash + google_search
- 50개 기업 파일럿
- 비용: ~$5-10

**Phase 2: MVP (3개월)**
- 하이브리드 (Claude + Gemini)
- 프롬프트 캐싱 구현
- 비용: ~$40/월

**Phase 3: 프로덕션 (6개월+)**
- 최적화된 하이브리드
- 배치 API 활용
- 비용: ~$30/월 (최적화 후)

---

## 모델 비교표 (요약)

### 비용 효율 순위

| 순위 | 모델 | 입력/출력 ($/1M) | 용도 |
|-----|------|-----------------|------|
| 1 | Gemini 2.0 Flash-Lite | $0.075 / $0.30 | 초경량 |
| 2 | **Gemini 2.0 Flash** | $0.10 / $0.40 | **범용 추천** ⭐ |
| 3 | **gpt-4o-mini** | $0.15 / $0.60 | OpenAI 최저가 |
| 4 | gpt-5-nano | $0.05 / $0.40 | 초경량 |
| 5 | Claude Haiku 4.5 | $1.00 / $5.00 | 빠른 응답 |
| 6 | **Claude Sonnet 4.5** | $3.00 / $15.00 | **품질 우선** ⭐ |

### 품질 순위

| 순위 | 모델 | 입력/출력 ($/1M) | 특징 |
|-----|------|-----------------|------|
| 1 | **Claude Opus 4.1** | $15 / $75 | 최고 추론 |
| 2 | **Claude Sonnet 4.5** | $3 / $15 | 코딩/에이전트 최적화 |
| 3 | gpt-5 | $1.25 / $10 | 최신 플래그십 |
| 4 | o1 | $15 / $60 | 고급 추론 |
| 5 | gpt-4o | $2.50 / $10 | 멀티모달 |

---

**참고 자료:**
- [OpenAI Pricing](https://openai.com/api/pricing/)
- [Anthropic Models](https://docs.claude.com/en/docs/about-claude/models)
- [Google Gemini Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Google ADK Docs](https://google.github.io/adk-docs/)

**주의사항:**
- 모든 가격은 2025년 10월 22일 기준 공식 페이지에서 확인
- 가격은 변경될 수 있으므로 공식 페이지 재확인 필요
- 실제 비용은 사용 패턴에 따라 달라질 수 있음
- OpenAI는 Batch, Flex, Priority 등 다양한 Tier 제공 (본 문서는 Standard 기준)
