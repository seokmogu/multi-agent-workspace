# 기업 탐색 에이전트 - 능력 분석 및 도메인 전문화

## 현재 구현 능력 분석

### ✅ 가능한 것

#### 1. 공개 정보 수집
- **기본 회사 정보**: 설립연도, 본사 위치, 산업
- **제품/서비스**: 주요 제품 목록
- **핵심 인물**: CEO, 임원진 (공개된 정보)
- **웹사이트 정보**: 공식 사이트, SNS
- **최근 뉴스**: 언론 보도 내용

#### 2. 구조화된 데이터 추출
```json
{
  "company_name": "Anthropic",
  "founded": "2021",
  "headquarters": "San Francisco, CA",
  "industry": "Artificial Intelligence",
  "products": ["Claude", "Constitutional AI"],
  "key_people": [
    {"name": "Dario Amodei", "role": "CEO"}
  ]
}
```

#### 3. 반복적 품질 개선
- 누락된 필드 자동 감지
- 추가 검색 쿼리 생성
- 1-2회 반복으로 완성도 향상

### ❌ 한계점

#### 1. 데이터 소스 제한
- **웹 검색만 가능**: Tavily API 기반
- **페이월 콘텐츠 접근 불가**: 유료 리포트, 구독 서비스
- **실시간 데이터 제한**: 주가, 실시간 지표

#### 2. 깊이 있는 분석 부족
- **표면적 정보**: 깊이 있는 인사이트 부족
- **정량 분석 제한**: 재무 비율 계산 등 불가
- **추론 능력**: 단순 정보 수집, 전문가 수준 분석 아님

#### 3. 검증 능력 제한
- **사실 확인**: 여러 소스 교차 검증 미흡
- **최신성**: 오래된 정보 포함 가능
- **신뢰도**: 출처 신뢰도 평가 부족

---

## 현실적인 정보 수집 수준

### Level 1: 기본 프로필 (현재 90% 가능)

```
✅ 회사명, 설립연도, 위치
✅ 산업, 비즈니스 모델
✅ 주요 제품/서비스
✅ CEO 및 주요 임원
✅ 공식 웹사이트
```

### Level 2: 상세 정보 (현재 70% 가능)

```
⚠️ 펀딩 히스토리 (공개 정보만)
⚠️ 직원 수 (대략적 추정)
⚠️ 최근 뉴스 (지난 6개월)
⚠️ 경쟁사 목록
⚠️ 기술 스택 (공개된 것만)
```

### Level 3: 전문 분석 (현재 30% 가능)

```
❌ 상세 재무 분석
❌ 조직 문화 평가
❌ M&A 적합성 분석
❌ 인재 채용 트렌드
❌ 시장 포지셔닝 전략
```

---

## 도메인별 전문가 요구사항

### 1. M&A 전문가 🤝

**필요 정보:**
```yaml
재무 정보:
  - 매출 및 성장률 (YoY)
  - EBITDA, 영업이익률
  - 부채비율, 현금흐름
  - 밸류에이션 (시가총액, EV/EBITDA)

전략 정보:
  - 사업 포트폴리오
  - 시장 점유율
  - 경쟁 우위
  - 시너지 기회

리스크:
  - 법적 이슈
  - 규제 리스크
  - 핵심 인력 의존도
  - 고객 집중도
```

**현재 능력: 40%**
- ✅ 기본 재무 정보 (공개 기업만)
- ⚠️ 성장률 (뉴스 기반 추정)
- ❌ 상세 재무 비율 계산
- ❌ 밸류에이션 분석

### 2. HR/인사 전문가 👥

**필요 정보:**
```yaml
조직 정보:
  - 조직 규모 및 구조
  - 주요 부서 및 팀
  - 리더십 배경
  - 이직률

채용 정보:
  - 현재 채용 중인 직무
  - 평균 연봉 범위
  - 복리후생 패키지
  - 리모트 정책

문화 정보:
  - 기업 문화 특성
  - 직원 리뷰/평점
  - 워라벨 평가
  - 성장 기회
```

**현재 능력: 50%**
- ✅ 조직 규모 (대략)
- ✅ 리더십 배경
- ⚠️ 채용 정보 (공개 JD)
- ❌ 연봉 정보
- ❌ 직원 만족도 (Glassdoor 미연동)

### 3. 투자자 (VC/PE) 💰

**필요 정보:**
```yaml
성장성:
  - 매출 성장률 (3-5년)
  - 시장 규모 및 성장률
  - 고객 증가율
  - 제품 로드맵

경쟁력:
  - 차별화 요소
  - 기술적 우위
  - 네트워크 효과
  - 전환 비용

재무 건전성:
  - Burn rate
  - Runway
  - Unit economics
  - CAC/LTV 비율
```

**현재 능력: 45%**
- ⚠️ 매출 성장률 (뉴스 기반)
- ✅ 시장 정보 (일반적)
- ⚠️ 차별화 요소 (마케팅 자료)
- ❌ Unit economics
- ❌ CAC/LTV

### 4. 영업/BD 전문가 📊

**필요 정보:**
```yaml
고객 정보:
  - 주요 고객사 목록
  - 타겟 고객 프로필
  - 고객 세그먼트
  - 성공 사례

제품 정보:
  - 제품 포지셔닝
  - 가격 정책
  - 주요 기능
  - 경쟁사 비교

파트너십:
  - 전략적 파트너
  - 유통 채널
  - 시스템 통합
```

**현재 능력: 60%**
- ✅ 주요 고객 (공개 정보)
- ✅ 제품 정보
- ⚠️ 가격 정책 (일부)
- ✅ 파트너십
- ❌ 상세 경쟁 분석

---

## 개선 방안

### 단기 개선 (즉시 가능)

#### 1. 도메인별 전문 스키마 제공

**구현 예시:**

```python
# schemas/ma_schema.py
MA_EXPERT_SCHEMA = {
    "title": "M&A Due Diligence Profile",
    "properties": {
        "financial_overview": {
            "revenue_last_3_years": "array",
            "revenue_growth_rate": "string",
            "profitability_metrics": "object",
            "funding_history": "array"
        },
        "market_position": {
            "market_share": "string",
            "competitive_advantages": "array",
            "market_trends": "array"
        },
        "risk_factors": {
            "legal_issues": "array",
            "regulatory_risks": "array",
            "key_person_dependencies": "array"
        }
    }
}

# schemas/hr_schema.py
HR_EXPERT_SCHEMA = {
    "title": "HR Research Profile",
    "properties": {
        "organization": {
            "total_employees": "string",
            "organizational_structure": "array",
            "leadership_team": "array"
        },
        "hiring": {
            "open_positions": "array",
            "hiring_trends": "array",
            "tech_stack": "array"
        },
        "culture": {
            "company_values": "array",
            "work_environment": "string",
            "employee_reviews": "array",
            "benefits": "array"
        }
    }
}
```

#### 2. 페르소나 기반 프롬프트

**Research Phase에 페르소나 추가:**

```python
PERSONA_PROMPTS = {
    "ma_expert": """You are an M&A analyst conducting due diligence.
    Focus on financial health, market position, synergies, and risks.
    Generate search queries that uncover:
    - Financial performance and trends
    - Strategic positioning and competitive moats
    - Potential red flags and liabilities
    """,

    "hr_expert": """You are an HR professional researching potential employers.
    Focus on organizational culture, employee satisfaction, and growth opportunities.
    Generate search queries that uncover:
    - Company culture and values
    - Employee reviews and ratings
    - Career development and benefits
    """,

    "investor": """You are a venture capital investor evaluating a potential investment.
    Focus on growth metrics, market opportunity, and team quality.
    Generate search queries that uncover:
    - Revenue growth and traction
    - Market size and dynamics
    - Founder backgrounds and team composition
    """
}
```

#### 3. 특화된 검색 쿼리 생성

```python
def generate_domain_queries(company_name, domain):
    """도메인별 최적화된 검색 쿼리"""

    domain_templates = {
        "ma_expert": [
            f"{company_name} revenue growth financial performance",
            f"{company_name} valuation funding rounds investors",
            f"{company_name} market share competitors analysis",
            f"{company_name} risks legal issues challenges"
        ],
        "hr_expert": [
            f"{company_name} company culture employee reviews",
            f"{company_name} careers hiring interview process",
            f"{company_name} benefits compensation glassdoor",
            f"{company_name} work life balance remote policy"
        ],
        "investor": [
            f"{company_name} growth metrics traction customers",
            f"{company_name} founders team background",
            f"{company_name} market opportunity total addressable market",
            f"{company_name} competitive advantage moat"
        ]
    }

    return domain_templates.get(domain, [])
```

### 중기 개선 (1-2개월)

#### 1. 다중 데이터 소스 통합

```python
class MultiSourceResearcher:
    def __init__(self):
        self.sources = {
            'web': TavilySearch(),
            'news': NewsAPIClient(),
            'financial': AlphaVantageAPI(),  # 재무 데이터
            'reviews': GlassdoorScraper(),   # 직원 리뷰
            'social': LinkedInAPI(),         # 조직 정보
        }

    async def research(self, company, domain):
        # 도메인별 최적 소스 선택
        if domain == "ma_expert":
            results = await self.sources['financial'].get_data(company)
        elif domain == "hr_expert":
            results = await self.sources['reviews'].get_data(company)
        # ...
```

#### 2. 도메인별 분석 에이전트

```python
class DomainAnalysisAgent:
    """도메인 전문 분석 에이전트"""

    def __init__(self, domain, llm):
        self.domain = domain
        self.llm = llm
        self.persona = PERSONA_PROMPTS[domain]

    async def analyze(self, extracted_data):
        """추출된 데이터를 도메인 관점에서 분석"""

        prompt = f"""{self.persona}

        Analyze this company data from a {self.domain} perspective:

        {extracted_data}

        Provide:
        1. Key insights
        2. Red flags or concerns
        3. Recommendations
        4. Information gaps
        """

        analysis = await self.llm.ainvoke(prompt)
        return analysis
```

### 장기 개선 (3-6개월)

#### 1. 전문 데이터베이스 통합

- **Crunchbase**: 스타트업 정보, 펀딩
- **PitchBook**: M&A, PE/VC 데이터
- **Bloomberg Terminal**: 재무 데이터
- **Glassdoor API**: 직원 리뷰
- **LinkedIn Sales Navigator**: B2B 정보

#### 2. 자동 분석 및 인사이트

```python
class InsightGenerator:
    """자동 인사이트 생성"""

    def generate_ma_insights(self, data):
        """M&A 관점 인사이트"""
        return {
            "valuation_range": self.calculate_valuation(data),
            "synergy_opportunities": self.identify_synergies(data),
            "integration_risks": self.assess_risks(data),
            "deal_structure_recommendation": self.recommend_structure(data)
        }

    def generate_hr_insights(self, data):
        """HR 관점 인사이트"""
        return {
            "culture_fit_score": self.assess_culture(data),
            "talent_quality_index": self.rate_talent(data),
            "compensation_competitiveness": self.benchmark_comp(data),
            "retention_risk": self.predict_retention(data)
        }
```

---

## 실전 예시: 도메인별 출력

### M&A 전문가용 출력

```json
{
  "company_profile": {
    "name": "TechStartup Inc",
    "valuation": "$500M (Series C)",
    "revenue_2023": "$50M ARR",
    "growth_rate": "150% YoY"
  },
  "financial_health": {
    "burn_rate": "$5M/month",
    "runway": "18 months",
    "gross_margin": "75%"
  },
  "strategic_fit": {
    "synergy_score": 8.5,
    "integration_complexity": "Medium",
    "cultural_alignment": "High"
  },
  "risks": [
    "Customer concentration (top 3 = 60%)",
    "Founder retention required",
    "Regulatory uncertainty in EU"
  ],
  "recommendation": "Strong acquisition candidate. Valuation reasonable at 10x ARR. Recommend earnout structure."
}
```

### HR 전문가용 출력

```json
{
  "company_profile": {
    "name": "TechStartup Inc",
    "size": "250 employees",
    "growth": "Hiring 50 roles in Q1"
  },
  "culture": {
    "glassdoor_rating": 4.2,
    "work_life_balance": "4.0/5",
    "values": ["Innovation", "Transparency", "Growth mindset"]
  },
  "opportunities": {
    "open_roles": ["Senior Engineers", "Product Managers"],
    "career_paths": "Clear IC and management tracks",
    "learning_budget": "$2000/year"
  },
  "concerns": [
    "Rapid growth may strain culture",
    "Some reports of long hours during sprints"
  ],
  "recommendation": "Great for ambitious mid-career professionals. Strong engineering culture."
}
```

---

## 제안: 페르소나 기반 리서치 모드

### 사용법

```python
from src.agent import build_research_graph, Configuration
from src.schemas import MA_EXPERT_SCHEMA, HR_EXPERT_SCHEMA

# M&A 전문가 모드
config = Configuration(
    persona="ma_expert",
    max_search_queries=5,
    include_analysis=True
)

graph = build_research_graph(config)

result = await graph.ainvoke({
    "company_name": "Anthropic",
    "extraction_schema": MA_EXPERT_SCHEMA,
    "analysis_required": True
})

# 출력: M&A 관점의 상세 분석 + 리스크 평가
```

---

## 결론

### 현재 능력 요약

| 도메인 | 정보 수집 능력 | 분석 능력 | 전문성 |
|--------|--------------|-----------|--------|
| **기본 프로필** | 90% | 60% | ⭐⭐⭐ |
| **M&A** | 40% | 20% | ⭐ |
| **HR** | 50% | 30% | ⭐⭐ |
| **투자** | 45% | 25% | ⭐ |
| **영업** | 60% | 40% | ⭐⭐ |

### 핵심 개선 포인트

1. **즉시 구현 가능** (코드 수정만)
   - ✅ 도메인별 스키마
   - ✅ 페르소나 프롬프트
   - ✅ 특화 검색 쿼리

2. **단기 구현** (외부 API 통합)
   - 📊 재무 데이터 API
   - 👥 HR 데이터 (Glassdoor)
   - 📰 뉴스 API

3. **장기 구현** (전문 분석)
   - 🤖 도메인별 분석 AI
   - 📈 자동 인사이트 생성
   - ✅ 팩트 체크 시스템

**도메인별 전문 스키마를 지금 바로 구현해볼까요?**
