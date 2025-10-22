# 웹 스크래핑 Arsenal - 전방위 도구 비교 및 폴백 전략

> 모든 상황에 대비한 스크래핑 도구 종합 가이드

**철학**: "한 가지 도구로 모든 것을 할 수 없다. 상황에 따라 최적의 도구를 선택하고, 실패 시 다음 도구로 폴백한다."

---

## 📋 목차

1. [도구 전체 비교표](#도구-전체-비교표)
2. [카테고리별 분류](#카테고리별-분류)
3. [폴백 체인 전략](#폴백-체인-전략)
4. [상황별 최적 도구](#상황별-최적-도구)
5. [구현 예시](#구현-예시)

---

## 도구 전체 비교표

### 무료/오픈소스 계층

| 도구 | 타입 | 가격 | JavaScript | Anti-Bot | LLM 추출 | 크롤링 | 속도 | GitHub Stars |
|------|------|------|-----------|---------|----------|--------|------|--------------|
| **Jina AI** | API | 무료 (100만 토큰) | ⚠️ 부분 | ❌ | ❌ | ❌ | ⚡⚡⚡ | - |
| **Crawl4AI** | 오픈소스 | 무료 | ✅ | ⚠️ 기본 | ✅ | ✅ | ⚡⚡⚡ | 10K+ |
| **ScrapeGraphAI** | 오픈소스 | 무료 | ✅ | ⚠️ 기본 | ✅✅ | ✅ | ⚡⚡ | 20K+ |
| **Scrapy** | 프레임워크 | 무료 | ⚠️ 추가 | ❌ | ❌ | ✅✅ | ⚡⚡⚡ | 52K+ |
| **BeautifulSoup** | 라이브러리 | 무료 | ❌ | ❌ | ❌ | ❌ | ⚡⚡⚡ | - |
| **Playwright** | 브라우저 | 무료 | ✅✅ | ⚠️ 수동 | ❌ | ⚠️ | ⚡ | 65K+ |

### 유료 API 계층

| 도구 | 가격/월 | JavaScript | Anti-Bot | LLM 추출 | 크롤링 | 성공률 | Proxy |
|------|---------|-----------|---------|----------|--------|--------|-------|
| **Firecrawl** | $16-83 | ✅✅ | ⚠️ 기본 | ✅✅ | ✅✅ | ~90% | ⚠️ |
| **ScraperAPI** | $49+ | ✅✅ | ✅✅ | ❌ | ⚠️ | 99.99% | ✅✅ |
| **Apify** | $49+ | ✅✅ | ✅ | ⚠️ | ✅✅ | ~95% | ✅ |
| **Bright Data** | $500+ | ✅✅ | ✅✅✅ | ✅ | ✅✅ | 99.9% | ✅✅✅ |
| **ZenRows** | $69+ | ✅✅ | ✅✅ | ❌ | ⚠️ | ~98% | ✅✅ |
| **Oxylabs** | $99+ | ✅✅ | ✅✅ | ✅ | ✅ | ~98% | ✅✅ |

### 특수 목적 도구

| 도구 | 전문 분야 | 가격 | 특징 |
|------|-----------|------|------|
| **Jina Embeddings** | 멀티모달 임베딩 | API 요금 | Text + Image 임베딩 |
| **Jina Reranker** | 검색 결과 재정렬 | API 요금 | 정확도 향상 |
| **Whisper** | 오디오 전사 | 무료/API | YouTube, 팟캐스트 |
| **Unstructured** | 문서 파싱 | 무료/API | PDF, Word, Excel |

---

## 카테고리별 분류

### Tier 1: 무료 고성능 (1차 시도)

```
🥇 Jina AI Reader
   ✅ 완전 무료 (100만 토큰)
   ✅ 초고속 (2-3초)
   ✅ 이미지 자동 캡셔닝
   ✅ Search API 내장
   ❌ 크롤링 불가
   ❌ JavaScript 제한
   Use Case: 뉴스, 블로그, 단순 페이지

🥈 Crawl4AI
   ✅ 완전 무료 (오픈소스)
   ✅ 초고속
   ✅ LLM-friendly 출력
   ✅ 크롤링 지원
   ⚠️ Anti-bot 기본만
   Use Case: 대량 크롤링, 로컬 실행

🥉 ScrapeGraphAI
   ✅ 무료 (오픈소스)
   ✅ 프롬프트 기반 추출
   ✅ 멀티 LLM 지원
   ⚠️ 속도 느림
   Use Case: 복잡한 구조화 추출
```

### Tier 2: 저비용 유료 (2차 폴백)

```
🥇 Firecrawl
   💰 $16-83/월
   ✅ LLM Extract 강력
   ✅ 전체 사이트 크롤링
   ✅ Screenshot
   ⚠️ Anti-bot 보통
   Use Case: IR 페이지, 구조화 추출

🥈 Apify
   💰 $49+/월
   ✅ 1,600+ 사전 구축 스크래퍼
   ✅ 플랫폼 생태계
   ✅ 자동화 워크플로우
   ⚠️ 비용 증가 빠름
   Use Case: 특정 사이트 (LinkedIn, Amazon)
```

### Tier 3: Anti-Bot 전문 (3차 폴백)

```
🥇 ScraperAPI
   💰 $49+/월 (성공 요청만 과금)
   ✅ 99.99% 성공률
   ✅ Cloudflare, DataDome 우회
   ✅ CAPTCHA 자동 해결
   ✅ Residential IP 수백만 개
   Use Case: 보호된 사이트

🥈 Bright Data
   💰 $500+/월 (엔터프라이즈)
   ✅ 최강 Anti-bot
   ✅ 7,200만+ IP
   ✅ 전용 스크래핑 브라우저
   Use Case: 대규모 엔터프라이즈
```

### Tier 4: DIY/커스텀 (최후 수단)

```
🥇 Playwright + Proxy
   ✅ 완전한 제어
   ✅ 브라우저 자동화
   ⚠️ 느림
   ⚠️ 관리 부담
   Use Case: 특수 케이스

🥈 Scrapy + Rotating Proxy
   ✅ 대량 크롤링
   ✅ 커스터마이징
   ⚠️ Anti-bot 수동 대응
   Use Case: 정적 사이트 대량 수집
```

---

## 폴백 체인 전략

### 지능형 폴백 시스템

```python
class SmartScraperWithFallback:
    """
    자동 폴백 웹 스크래퍼

    실패 시 다음 도구로 자동 전환
    """

    def __init__(self):
        # Tier 1: 무료
        self.jina = JinaReader()
        self.crawl4ai = Crawl4AIClient()

        # Tier 2: 저비용
        self.firecrawl = FirecrawlApp(api_key="...")
        self.apify = ApifyClient(token="...")

        # Tier 3: Anti-bot
        self.scraperapi = ScraperAPIClient(api_key="...")

        # Tier 4: DIY
        self.playwright = PlaywrightBrowser()

        # 통계
        self.stats = {
            "jina": {"success": 0, "failure": 0},
            "crawl4ai": {"success": 0, "failure": 0},
            "firecrawl": {"success": 0, "failure": 0},
            "scraperapi": {"success": 0, "failure": 0},
            "playwright": {"success": 0, "failure": 0}
        }

    async def scrape(self, url: str, options: dict = None) -> dict:
        """
        폴백 체인을 통한 스크래핑

        Args:
            url: 대상 URL
            options: {
                'task_type': 'news' | 'website' | 'protected',
                'require_javascript': bool,
                'require_structure': bool,
                'max_cost': float
            }

        Returns:
            {
                'success': bool,
                'content': str,
                'tool_used': str,
                'cost': float,
                'attempts': list
            }
        """

        options = options or {}
        task_type = options.get('task_type', 'general')
        attempts = []

        # 폴백 체인 정의
        chain = self._build_fallback_chain(url, options)

        for tool_name, scraper_func in chain:
            try:
                print(f"🔄 Trying {tool_name}...")

                result = await scraper_func(url, options)

                # 성공 확인
                if self._validate_result(result):
                    self.stats[tool_name]["success"] += 1
                    attempts.append({
                        "tool": tool_name,
                        "status": "success"
                    })

                    return {
                        "success": True,
                        "content": result["content"],
                        "tool_used": tool_name,
                        "cost": result.get("cost", 0),
                        "attempts": attempts
                    }

            except Exception as e:
                self.stats[tool_name]["failure"] += 1
                attempts.append({
                    "tool": tool_name,
                    "status": "failed",
                    "error": str(e)
                })
                print(f"❌ {tool_name} failed: {e}")
                continue

        # 모두 실패
        return {
            "success": False,
            "content": None,
            "tool_used": None,
            "cost": 0,
            "attempts": attempts
        }

    def _build_fallback_chain(self, url: str, options: dict) -> list:
        """
        URL과 옵션에 따라 최적의 폴백 체인 구성

        Returns:
            [(tool_name, scraper_function), ...]
        """

        task_type = options.get('task_type')
        require_js = options.get('require_javascript', False)
        require_anti_bot = self._detect_anti_bot(url)
        max_cost = options.get('max_cost', 100)  # 최대 허용 비용

        chain = []

        # 뉴스/검색 → Jina AI 우선
        if task_type == 'news' or task_type == 'search':
            chain.append(('jina', self._scrape_with_jina))

        # 일반 웹사이트 → 무료 도구 우선
        if not require_anti_bot:
            chain.append(('jina', self._scrape_with_jina))
            if require_js:
                chain.append(('crawl4ai', self._scrape_with_crawl4ai))

        # 구조화 필요 → Firecrawl
        if options.get('require_structure'):
            if max_cost >= 0.016:  # Firecrawl 1 credit
                chain.append(('firecrawl', self._scrape_with_firecrawl))

        # Anti-bot 감지 → 전문 도구
        if require_anti_bot:
            if max_cost >= 1:  # ScraperAPI ~$1/1000 requests
                chain.append(('scraperapi', self._scrape_with_scraperapi))

        # 최후 수단 → DIY
        chain.append(('playwright', self._scrape_with_playwright))

        return chain

    def _detect_anti_bot(self, url: str) -> bool:
        """
        URL에서 Anti-bot 시스템 감지

        Returns:
            True if anti-bot detected
        """

        # 알려진 보호 시스템이 있는 도메인
        protected_domains = [
            'cloudflare',
            'datadome',
            'perimeterx',
            'akamai'
        ]

        # 간단한 GET 요청으로 확인
        try:
            response = requests.get(url, timeout=5)

            # Cloudflare 감지
            if 'cf-ray' in response.headers:
                return True

            # DataDome 감지
            if 'datadome' in response.text.lower():
                return True

            # CAPTCHA 감지
            if 'captcha' in response.text.lower():
                return True

        except:
            pass

        return False

    def _validate_result(self, result: dict) -> bool:
        """
        스크래핑 결과 검증

        Returns:
            True if result is valid
        """

        if not result or not result.get("content"):
            return False

        content = result["content"]

        # 최소 길이 확인
        if len(content) < 100:
            return False

        # 에러 페이지 감지
        error_keywords = [
            "access denied",
            "403 forbidden",
            "404 not found",
            "rate limit",
            "captcha"
        ]

        content_lower = content.lower()
        for keyword in error_keywords:
            if keyword in content_lower:
                return False

        return True

    # 각 도구별 래퍼 함수
    async def _scrape_with_jina(self, url: str, options: dict) -> dict:
        """Jina AI로 스크래핑"""
        result = self.jina.read(url)
        return {
            "content": result["markdown"],
            "cost": 0
        }

    async def _scrape_with_crawl4ai(self, url: str, options: dict) -> dict:
        """Crawl4AI로 스크래핑"""
        result = await self.crawl4ai.arun(url)
        return {
            "content": result.markdown,
            "cost": 0
        }

    async def _scrape_with_firecrawl(self, url: str, options: dict) -> dict:
        """Firecrawl로 스크래핑"""

        if options.get('require_structure'):
            result = await self.firecrawl.scrape_url(
                url,
                params={
                    'formats': ['extract'],
                    'extract': {'schema': options.get('schema')}
                }
            )
        else:
            result = await self.firecrawl.scrape_url(
                url,
                params={'formats': ['markdown']}
            )

        return {
            "content": result["markdown"],
            "cost": 0.016  # 1 credit
        }

    async def _scrape_with_scraperapi(self, url: str, options: dict) -> dict:
        """ScraperAPI로 스크래핑"""

        api_url = f"http://api.scraperapi.com/?api_key={self.scraperapi.api_key}&url={url}"

        if options.get('require_javascript'):
            api_url += "&render=true"

        response = requests.get(api_url)

        return {
            "content": response.text,
            "cost": 0.001  # ~$1/1000 requests
        }

    async def _scrape_with_playwright(self, url: str, options: dict) -> dict:
        """Playwright로 스크래핑 (최후 수단)"""

        async with self.playwright as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            await page.goto(url, wait_until="networkidle")
            content = await page.content()

            await browser.close()

        return {
            "content": content,
            "cost": 0  # 서버 비용만
        }

    def print_stats(self):
        """통계 출력"""
        print("\n📊 Scraping Statistics:")
        for tool, stats in self.stats.items():
            total = stats["success"] + stats["failure"]
            if total > 0:
                success_rate = stats["success"] / total * 100
                print(f"  {tool}: {stats['success']}/{total} ({success_rate:.1f}% success)")
```

---

## 상황별 최적 도구

### 시나리오 1: 한국 뉴스 수집

```
목표: 네이버 뉴스 1,000개 기사 수집

폴백 체인:
1. Jina AI Search (무료) ← 1순위
2. Naver Search API (무료) ← 2순위
3. Crawl4AI (무료) ← 3순위

예상 비용: $0
```

### 시나리오 2: 회사 웹사이트 분석

```
목표: 회사 웹사이트 About, IR, 채용 페이지

폴백 체인:
1. Jina AI Reader (무료) ← 빠른 개요
2. Firecrawl (유료) ← 상세 분석 (10 페이지)
3. Playwright (무료) ← JavaScript 필요시

예상 비용: ~$0.16 (Firecrawl 10 credits)
```

### 시나리오 3: LinkedIn 프로필 수집

```
목표: 임원 100명 LinkedIn 프로필

Anti-bot: ✅ (LinkedIn은 강력)

폴백 체인:
1. Apify LinkedIn Scraper (유료) ← 전문
2. ScraperAPI (유료) ← Anti-bot 우회
3. Bright Data (유료) ← 최후 수단

예상 비용: $5-10 (Apify actor)
```

### 시나리오 4: DART 재무제표 (PDF)

```
목표: 사업보고서 PDF 파싱

Anti-bot: ❌

폴백 체인:
1. DART API (무료) ← XML/JSON으로 바로
2. Unstructured (무료) ← PDF 파싱
3. PyPDF2 + GPT-4V (유료) ← OCR

예상 비용: ~$0.05 (GPT-4V)
```

### 시나리오 5: YouTube IR 영상

```
목표: IR 프레젠테이션 영상 분석

폴백 체인:
1. YouTube Transcript API (무료) ← 자막 있으면
2. Whisper (무료/API) ← 자막 없으면
3. GPT-4V (유료) ← 화면 분석

예상 비용: $0-0.10
```

---

## 도구별 상세 스펙

### 1. Jina AI

**강점**:
- 완전 무료 (100만 토큰)
- 초고속 (2-3초)
- 이미지 자동 캡셔닝
- Search API 내장

**약점**:
- 크롤링 불가
- JavaScript 렌더링 제한
- Anti-bot 없음

**최적 사용**:
```python
# 뉴스, 블로그, 단순 웹페이지
jina.read("https://news.article.com")
jina.search("삼성전자 M&A")
```

### 2. Crawl4AI

**강점**:
- 완전 무료 (오픈소스)
- 초고속 (멀티스레딩)
- LLM 친화적 출력
- 로컬 LLM 지원

**약점**:
- Anti-bot 기본만
- 셀프 호스팅 필요

**최적 사용**:
```python
# 대량 크롤링, 빠른 속도
from crawl4ai import AsyncWebCrawler

async with AsyncWebCrawler() as crawler:
    result = await crawler.arun(
        url="https://company.com",
        word_count_threshold=10
    )
```

### 3. ScrapeGraphAI

**강점**:
- 프롬프트 기반 추출
- 멀티 LLM (GPT-4, Claude, Gemini)
- 자동 구조 인식

**약점**:
- 속도 느림
- LLM 비용 증가

**최적 사용**:
```python
# 복잡한 구조화 추출
from scrapegraphai.graphs import SmartScraperGraph

graph = SmartScraperGraph(
    prompt="Extract product names, prices, ratings",
    source="https://shop.com",
    config={"llm": {"model": "gpt-4"}}
)

result = graph.run()
```

### 4. Firecrawl

**강점**:
- LLM Extract 강력
- 전체 사이트 크롤링
- Screenshot 지원

**약점**:
- 유료 ($16-83/월)
- Anti-bot 보통

**최적 사용**:
```python
# IR 페이지, 구조화 추출
firecrawl.scrape_url(
    "https://company.com/ir",
    params={
        'formats': ['extract'],
        'extract': {'schema': FINANCIAL_SCHEMA}
    }
)
```

### 5. ScraperAPI

**강점**:
- 99.99% 성공률
- Cloudflare, DataDome 우회
- 성공 요청만 과금

**약점**:
- 비용 증가 가능
- LLM 추출 없음

**최적 사용**:
```python
# 보호된 사이트
import requests

url = f"http://api.scraperapi.com/?api_key={API_KEY}&url=https://protected-site.com&render=true"
response = requests.get(url)
```

### 6. Apify

**강점**:
- 1,600+ 사전 구축 스크래퍼
- LinkedIn, Amazon, Google Maps 등
- 워크플로우 자동화

**약점**:
- 비용 증가 빠름
- Lock-in 위험

**최적 사용**:
```python
# LinkedIn, 특정 플랫폼
from apify_client import ApifyClient

client = ApifyClient("YOUR_TOKEN")

run = client.actor("apify/linkedin-profile-scraper").call(
    run_input={"profiles": ["https://linkedin.com/in/..."]}
)

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

---

## 비용 시뮬레이션

### 시나리오: 월 100개 중소기업 리서치

| 태스크 | 도구 | 횟수 | 단가 | 비용 |
|--------|------|------|------|------|
| 뉴스 검색 | Jina AI | 200 | $0 | **$0** |
| 웹사이트 스캔 | Jina AI | 100 | $0 | **$0** |
| 재무 데이터 | DART API | 100 | $0 | **$0** |
| IR 상세 | Firecrawl | 50 | $0.016 | **$0.80** |
| LinkedIn | Apify | 20 | $0.25 | **$5** |
| 보호 사이트 | ScraperAPI | 10 | $0.001 | **$0.01** |
| LLM 분석 | Claude | 100 | $0.50 | **$50** |
| **Total** | | | | **$55.81** |

**기존 (Firecrawl만)**: $83/월
**절감**: $27.19 (33% 절감)

---

## 최종 권장 Arsenal

### 핵심 3종 세트 (필수)

```
1. Jina AI (무료)
   - 모든 일반 스크래핑
   - 뉴스, 검색, 웹사이트

2. DART/EDINET API (무료)
   - 한국/일본 공식 데이터

3. Firecrawl ($16/월)
   - IR 상세 분석
   - 구조화 추출
```

**월 비용**: $16
**커버리지**: 90%

### 확장 5종 세트 (권장)

```
+ 4. Crawl4AI (무료)
     - 대량 크롤링
     - 로컬 실행

+ 5. ScraperAPI ($49/월)
     - Anti-bot 사이트
     - 보호된 페이지
```

**월 비용**: $65
**커버리지**: 98%

### 엔터프라이즈 세트 (최대)

```
+ 6. Apify ($49/월)
     - LinkedIn, Amazon
     - 특수 플랫폼

+ 7. Bright Data ($500+/월)
     - 최강 Anti-bot
     - 대규모 운영
```

**월 비용**: $614
**커버리지**: 99.9%

---

## 다음 단계

### 1. 무료 도구 테스트 (오늘)

```bash
# Jina AI
curl https://r.jina.ai/https://www.samsung.com

# Crawl4AI
pip install crawl4ai
crawl4ai-setup
```

### 2. 폴백 시스템 구현 (1주)

```python
# smart_scraper.py 구현
scraper = SmartScraperWithFallback()
result = await scraper.scrape("https://company.com")
```

### 3. 프로덕션 배포 (1개월)

```python
# 모든 도구 통합
# 통계 수집
# 비용 최적화
```

**지금 바로 무료 도구부터 테스트해볼까요?**
