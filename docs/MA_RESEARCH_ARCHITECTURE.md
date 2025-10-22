# M&A 리서치 펌 수준 에이전트 - 엔터프라이즈 아키텍처

> 한국/일본 중소·중견기업 대상 전방위 데이터 수집 및 분석 시스템

**목표**: 웹에서 찾을 수 있는 거의 모든 공개 정보를 수집하여 M&A 리서치 펌 수준의 분석 제공

---

## 📋 목차

1. [연구 결과 요약](#연구-결과-요약)
2. [엔터프라이즈 아키텍처](#엔터프라이즈-아키텍처)
3. [데이터 소스 맵](#데이터-소스-맵)
4. [멀티모달 수집 시스템](#멀티모달-수집-시스템)
5. [에이전트 구조](#에이전트-구조)
6. [기술 스택](#기술-스택)
7. [구현 로드맵](#구현-로드맵)

---

## 연구 결과 요약

### GitHub에서 발견한 핵심 프로젝트

#### 1. 심층 리서치 에이전트

| 프로젝트 | 스타 | 핵심 특징 |
|---------|------|-----------|
| [**GPT-Researcher**](https://github.com/assafelovic/gpt-researcher) | 30.5K ⭐ | Multi-agent 리서치, 인용 포함 보고서 생성 |
| [**DeepResearchAgent**](https://github.com/SkyworkAI/DeepResearchAgent) | - | 계층적 멀티에이전트, 태스크 분해 |
| [**open_deep_research**](https://github.com/langchain-ai/open_deep_research) | - | LangChain 공식, MCP 서버 지원 |

**GPT-Researcher 멀티 에이전트 구조**:
```
Chief Editor (조율)
├── GPT Researcher (심층 조사)
├── Reviewer (검증)
├── Reviser (수정)
└── Writer (보고서 작성)
```

#### 2. M&A Due Diligence 전문

| 프로젝트 | 특징 |
|---------|------|
| [**DiligenceAI**](https://github.com/ChesterCaii/DiligenceAI) | Market/Competitors/Team/Technical 분석 에이전트 |
| [**company-research-agent**](https://github.com/guy-hartstein/company-research-agent) | LangGraph + Tavily, Gemini/GPT-4 |

**DiligenceAI 에이전트 구조**:
```
- Market Analysis Agent
- Competitors Agent
- Team Evaluation Agent
- Technical Due Diligence Agent
- Due Diligence Report Agent
- Final Decision Agent
```

#### 3. 멀티모달 데이터 추출

| 프로젝트 | 기능 |
|---------|------|
| [**Firecrawl**](https://github.com/firecrawl/firecrawl) | 웹사이트 → LLM-ready markdown/구조화 데이터 |
| [**MultimodalOCR**](https://github.com/Yuliang-Liu/MultimodalOCR) | OCR 벤치마크, LMM 평가 |
| [**ollama-ocr**](https://github.com/dwqs/ollama-ocr) | Vision LLM OCR (LLaVA, Llama Vision) |

**Firecrawl 주요 기능**:
- LLM Extract (스키마 기반 추출)
- Screenshot 지원
- 멀티페이지 크롤링
- Markdown 변환

#### 4. 한국 데이터 소스

| 프로젝트 | API | 특징 |
|---------|-----|------|
| [**dart-fss**](https://github.com/josw123/dart-fss) | Open DART | 재무제표 추출 |
| [**OpenDartReader**](https://github.com/FinanceData/OpenDartReader) | Open DART | DataFrame 변환 |
| [**dart_reports**](https://github.com/seoweon/dart_reports) | Open DART | 사업보고서 일괄 다운로드 |

**DART API 제공 정보**:
- 사업보고서, 감사보고서
- 재무제표 (상세)
- 공시 정보
- 대주주 변동

#### 5. 일본 데이터 소스

| 프로젝트 | API | 특징 |
|---------|-----|------|
| [**edinet-tools**](https://github.com/matthelmer/edinet-tools) | EDINET v2 | 11,000+ 기업, XBRL 파싱 |
| [**xbrr**](https://github.com/chakki-works/xbrr) | EDINET | 유가증권보고서 |
| [**edinet2dataset**](https://github.com/SakanaAI/edinet2dataset) | EDINET | 10년치 4,000개 기업 데이터셋 |

**EDINET API 제공 정보**:
- 유가증권보고서
- 재무 데이터 (XBRL)
- 임원 정보
- M&A 정보

#### 6. Multi-Agent 프레임워크

| 프레임워크 | GitHub Stars | 특징 |
|-----------|--------------|------|
| **CrewAI** | 30K+ | Role-based 에이전트, 1M+ 다운로드 |
| **LangGraph** | - | LangChain 공식, 유연한 그래프 |
| **AutoGen** | 30K+ | Microsoft, 멀티 에이전트 대화 |

**CrewAI vs LangGraph**:
- CrewAI: 고수준, 빠른 프로토타입
- LangGraph: 저수준, 완전한 커스터마이징

---

## 엔터프라이즈 아키텍처

### 전체 시스템 개요

```
┌──────────────────────────────────────────────────────────────────┐
│                    USER INTERFACE LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Web UI     │  │  API Client  │  │   Mobile     │          │
│  │  (Next.js)   │  │  (Swagger)   │  │    App       │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
└─────────┼──────────────────┼──────────────────┼──────────────────┘
          │                  │                  │
          └──────────────────┴──────────────────┘
                             │
┌──────────────────────────────────────────────────────────────────┐
│                   ORCHESTRATION LAYER                            │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │          Chief Orchestrator Agent                       │    │
│  │  - Task decomposition                                   │    │
│  │  - Agent coordination                                   │    │
│  │  - Progress tracking                                    │    │
│  └───────┬─────────────────────────────────────────┬───────┘    │
└──────────┼─────────────────────────────────────────┼────────────┘
           │                                         │
           ↓                                         ↓
┌──────────────────────────────────────────────────────────────────┐
│                  SPECIALIZED AGENT LAYER                         │
│                                                                  │
│  ┌───────────────┐  ┌───────────────┐  ┌────────────────┐     │
│  │   Financial   │  │    Market     │  │  Competitors   │     │
│  │    Agent      │  │    Agent      │  │     Agent      │     │
│  │  - DART API   │  │  - Industry   │  │  - Benchmarks  │     │
│  │  - EDINET API │  │  - Trends     │  │  - Analysis    │     │
│  └───────┬───────┘  └───────┬───────┘  └────────┬───────┘     │
│          │                  │                    │             │
│  ┌───────────────┐  ┌───────────────┐  ┌────────────────┐     │
│  │   Legal &     │  │   Technical   │  │     Team       │     │
│  │  Compliance   │  │  Diligence    │  │   Analysis     │     │
│  │    Agent      │  │    Agent      │  │    Agent       │     │
│  └───────┬───────┘  └───────┬───────┘  └────────┬───────┘     │
│          │                  │                    │             │
│  ┌───────────────┐  ┌───────────────┐  ┌────────────────┐     │
│  │   News &      │  │   Social      │  │    ESG &       │     │
│  │   Media       │  │   Media       │  │  Reputation    │     │
│  │    Agent      │  │    Agent      │  │    Agent       │     │
│  └───────┬───────┘  └───────┬───────┘  └────────┬───────┘     │
└──────────┼──────────────────┼──────────────────────┼────────────┘
           │                  │                      │
           ↓                  ↓                      ↓
┌──────────────────────────────────────────────────────────────────┐
│               DATA COLLECTION & EXTRACTION LAYER                 │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │           Multi-Modal Data Collectors                   │   │
│  │                                                          │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐       │   │
│  │  │   Web      │  │   Image    │  │   Video    │       │   │
│  │  │  Scraper   │  │   OCR      │  │  Transcript│       │   │
│  │  │ (Firecrawl)│  │ (Vision LLM│  │ (Whisper)  │       │   │
│  │  └────────────┘  └────────────┘  └────────────┘       │   │
│  │                                                          │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐       │   │
│  │  │ Document   │  │   PDF      │  │   Excel    │       │   │
│  │  │  Parser    │  │  Extractor │  │  Analyzer  │       │   │
│  │  │(Unstructure│  │ (PyPDF2)   │  │ (Pandas)   │       │   │
│  │  └────────────┘  └────────────┘  └────────────┘       │   │
│  └─────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
           │                  │                      │
           ↓                  ↓                      ↓
┌──────────────────────────────────────────────────────────────────┐
│                    DATA SOURCE LAYER                             │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Korean     │  │   Japanese   │  │  Web Search  │         │
│  │   Sources    │  │   Sources    │  │              │         │
│  │  - DART API  │  │ - EDINET API │  │  - Tavily    │         │
│  │  - Naver     │  │ - Yahoo JP   │  │  - SerpAPI   │         │
│  │  - 사람인    │  │ - Recruit    │  │  - Bing      │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   YouTube    │  │   LinkedIn   │  │   GitHub     │         │
│  │  Transcripts │  │  Company Page│  │  Org Repos   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└──────────────────────────────────────────────────────────────────┘
           │                  │                      │
           ↓                  ↓                      ↓
┌──────────────────────────────────────────────────────────────────┐
│                     STORAGE & KNOWLEDGE LAYER                    │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  PostgreSQL  │  │  Vector DB   │  │   Neo4j      │         │
│  │  (Supabase)  │  │  (Pinecone)  │  │  Knowledge   │         │
│  │  Raw Data    │  │  Embeddings  │  │    Graph     │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐                            │
│  │     S3       │  │    Redis     │                            │
│  │   Documents  │  │    Cache     │                            │
│  └──────────────┘  └──────────────┘                            │
└──────────────────────────────────────────────────────────────────┘
```

---

## 데이터 소스 맵

### 한국 기업 데이터 소스

#### 1. 공식 공시 (필수)

| 소스 | API | 데이터 |
|------|-----|--------|
| **전자공시(DART)** | Open DART API | 사업보고서, 재무제표, 공시 |
| **금융감독원** | - | 감사보고서, IR 자료 |
| **공정거래위원회** | - | 기업집단 현황, 계열사 |
| **특허청** | KIPRIS API | 특허, 상표, 디자인 |

**구현 도구**:
```python
from dart_fss import OpenDartReader
from opendartreader import OpenDartReader as ODR

api_key = "YOUR_API_KEY"
dart = OpenDartReader(api_key)

# 재무제표
df = dart.finstate("005930", 2023)  # 삼성전자

# 공시 검색
disclosures = dart.list(corp="005930", start="2024-01-01")
```

#### 2. 뉴스 & 미디어

| 소스 | API | 특징 |
|------|-----|------|
| **네이버 뉴스** | Naver Search API | 한국 최대 뉴스 플랫폼 |
| **한국경제** | - | 경제 뉴스 전문 |
| **매일경제** | - | 기업 심층 분석 |
| **조선비즈** | - | 비즈니스 뉴스 |

**구현 예시**:
```python
import requests

def search_naver_news(company_name, client_id, client_secret):
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    params = {"query": company_name, "display": 100}

    response = requests.get(url, headers=headers, params=params)
    return response.json()
```

#### 3. HR & 채용

| 소스 | 데이터 |
|------|--------|
| **사람인** | 채용공고, 기업정보 |
| **잡코리아** | 직무, 연봉 정보 |
| **LinkedIn** | 직원 프로필, 조직 구조 |

#### 4. 평판 & 리뷰

| 소스 | 데이터 |
|------|--------|
| **잡플래닛** | 직원 리뷰, 평점 |
| **크레딧잡** | 재무 건전성, 신용등급 |
| **블라인드** | 익명 직원 의견 |

### 일본 기업 데이터 소스

#### 1. 공식 공시 (필수)

| 소스 | API | 데이터 |
|------|-----|--------|
| **EDINET** | EDINET API v2 | 유가증권보고서, 재무데이터 |
| **J-Patent** | - | 특허 정보 |
| **TSR** | - | 신용 조사 |

**구현 도구**:
```python
from edinet_tools import EdinetClient

client = EdinetClient()

# 기업 검색
companies = client.search_companies("トヨタ")

# 보고서 다운로드
docs = client.get_documents(
    company_code="7203",  # Toyota
    from_date="2024-01-01"
)
```

#### 2. 뉴스 & 미디어

| 소스 | 특징 |
|------|------|
| **Yahoo! Japan** | 일본 최대 뉴스 |
| **Nikkei** | 경제 전문 |
| **Reuters Japan** | 국제 뉴스 |

#### 3. HR & 리뷰

| 소스 | 데이터 |
|------|--------|
| **Recruit** | 채용 정보 |
| **Vorkers** | 직원 리뷰 |
| **OpenWork** | 평판 정보 |

### 글로벌 소스 (공통)

| 소스 | 데이터 | API |
|------|--------|-----|
| **YouTube** | 기업 채널, IR 영상 | YouTube Data API |
| **LinkedIn** | 직원, 조직도 | LinkedIn API |
| **GitHub** | 기술 스택, 오픈소스 | GitHub API |
| **Crunchbase** | 펀딩, M&A | Crunchbase API |
| **Twitter/X** | 소셜 미디어 | X API |

---

## 멀티모달 수집 시스템

### 데이터 타입별 처리

```
┌─────────────────────────────────────────────────────────┐
│              INPUT DATA TYPES                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  📄 Text        🖼️ Images      🎥 Videos               │
│  ├─ HTML       ├─ Screenshots  ├─ YouTube              │
│  ├─ PDF        ├─ Charts       ├─ Company Intro        │
│  ├─ Word       ├─ Diagrams     └─ IR Presentations     │
│  └─ Excel      └─ Infographics                         │
│                                                         │
│  🎤 Audio       📊 Structured   🌐 Web                  │
│  ├─ Podcasts   ├─ JSON         ├─ Websites             │
│  └─ Calls      ├─ XML/XBRL     ├─ Blogs                │
│                └─ CSV          └─ SNS                   │
└─────────────────────────────────────────────────────────┘
          │              │              │
          ↓              ↓              ↓
┌─────────────────────────────────────────────────────────┐
│           EXTRACTION & PROCESSING LAYER                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  🔧 Text Processing                                     │
│  ├─ Firecrawl (Web → Markdown)                         │
│  ├─ Unstructured (Documents → Chunks)                  │
│  ├─ PyPDF2 / pdfplumber (PDF → Text)                   │
│  └─ pandas (Excel → DataFrame)                         │
│                                                         │
│  🖼️ Vision Processing                                   │
│  ├─ GPT-4 Vision (Image → Description)                 │
│  ├─ Claude 3 Vision (Charts → Data)                    │
│  ├─ Tesseract OCR (Image → Text)                       │
│  └─ LayoutParser (Document Layout → Structure)         │
│                                                         │
│  🎥 Video/Audio Processing                              │
│  ├─ Whisper (Audio → Transcript)                       │
│  ├─ YouTube Transcript API (Video → Text)              │
│  ├─ FFmpeg (Video → Frames)                            │
│  └─ GPT-4V (Frames → Scene Description)                │
│                                                         │
│  🌐 Web Scraping                                        │
│  ├─ Playwright (Dynamic Pages)                         │
│  ├─ BeautifulSoup (HTML Parsing)                       │
│  ├─ Scrapy (Large-scale Crawling)                      │
│  └─ Selenium (JavaScript-heavy Sites)                  │
└─────────────────────────────────────────────────────────┘
          │              │              │
          ↓              ↓              ↓
┌─────────────────────────────────────────────────────────┐
│              UNIFIED DATA FORMAT                        │
│                                                         │
│     Markdown + Metadata + Embeddings                    │
│                                                         │
│  {                                                      │
│    "content": "...",                                    │
│    "source": "DART/EDINET/Web",                        │
│    "type": "financial/news/video",                     │
│    "timestamp": "2024-01-01",                          │
│    "embedding": [...],                                  │
│    "metadata": {...}                                    │
│  }                                                      │
└─────────────────────────────────────────────────────────┘
```

### 구현 예시

#### 1. Web Scraping (Firecrawl)

```python
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="YOUR_API_KEY")

# 단일 페이지 스크랩
result = app.scrape_url(
    "https://www.company-website.com",
    params={
        'formats': ['markdown', 'html', 'screenshot'],
        'onlyMainContent': True
    }
)

# LLM Extract (구조화된 데이터)
extract_result = app.scrape_url(
    "https://www.company-website.com/about",
    params={
        'formats': ['extract'],
        'extract': {
            'schema': {
                'type': 'object',
                'properties': {
                    'company_name': {'type': 'string'},
                    'founded_year': {'type': 'string'},
                    'employees': {'type': 'string'},
                    'revenue': {'type': 'string'}
                }
            }
        }
    }
)

# 전체 사이트 크롤링
crawl_result = app.crawl_url(
    "https://www.company-website.com",
    params={
        'limit': 100,
        'scrapeOptions': {'formats': ['markdown']}
    }
)
```

#### 2. Image OCR (Vision LLM)

```python
from openai import OpenAI
import base64

client = OpenAI()

def analyze_financial_chart(image_path):
    """재무 차트 이미지 분석"""

    # 이미지 인코딩
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """Analyze this financial chart and extract:
                        1. Chart type (bar, line, pie)
                        2. Title and labels
                        3. Key data points
                        4. Trends and insights
                        Return as structured JSON."""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=1000
    )

    return response.choices[0].message.content
```

#### 3. YouTube Transcript

```python
from youtube_transcript_api import YouTubeTranscriptApi

def get_company_video_transcript(video_id):
    """유튜브 영상 자막 추출"""

    # 자막 가져오기 (한국어/일본어 우선)
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=['ko', 'ja', 'en']
        )
    except:
        # 자동 생성 자막
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=['ko', 'ja', 'en'],
            preserve_formatting=True
        )

    # 텍스트로 변환
    full_text = " ".join([item['text'] for item in transcript])

    return {
        "video_id": video_id,
        "transcript": full_text,
        "language": transcript[0].get('language', 'unknown'),
        "duration": sum([item['duration'] for item in transcript])
    }
```

#### 4. PDF Financial Reports

```python
import pdfplumber
from langchain_community.document_loaders import UnstructuredPDFLoader

def extract_financial_report(pdf_path):
    """재무보고서 PDF 추출"""

    # pdfplumber로 테이블 추출
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_tables = page.extract_tables()
            tables.extend(page_tables)

    # Unstructured로 텍스트 추출
    loader = UnstructuredPDFLoader(pdf_path)
    documents = loader.load()

    return {
        "text": documents,
        "tables": tables,
        "metadata": {
            "pages": len(pdf.pages),
            "has_tables": len(tables) > 0
        }
    }
```

---

## 에이전트 구조

### 계층적 멀티 에이전트 시스템

```
                  ┌─────────────────────┐
                  │  Chief Orchestrator │
                  │  (LangGraph Master) │
                  └──────────┬──────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ↓                    ↓                    ↓
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  Data Mining  │    │   Analysis    │    │  Reporting    │
│  Supervisor   │    │  Supervisor   │    │  Supervisor   │
└───────┬───────┘    └───────┬───────┘    └───────┬───────┘
        │                    │                    │
┌───────┴────────┐   ┌───────┴────────┐   ┌──────┴───────┐
│                │   │                │   │              │
↓                ↓   ↓                ↓   ↓              ↓
```

### Phase 1: Data Mining Supervisor

**Sub-Agents**:

1. **Web Scraper Agent**
   ```python
   class WebScraperAgent:
       """웹사이트 크롤링"""
       tools = [
           FirecrawlTool(),
           PlaywrightTool(),
           BeautifulSoupTool()
       ]

       def execute(self, company_name, target_urls):
           # 회사 웹사이트, 블로그, IR 페이지 크롤링
           pass
   ```

2. **Official Data Agent**
   ```python
   class OfficialDataAgent:
       """공식 공시 데이터"""
       tools = [
           DARTAPITool(),    # 한국
           EDINETAPITool(),  # 일본
           SECAPITool()      # 미국 (참고)
       ]

       def execute(self, company_code):
           # 재무제표, 사업보고서 수집
           pass
   ```

3. **News Collector Agent**
   ```python
   class NewsCollectorAgent:
       """뉴스 수집"""
       tools = [
           NaverNewsTool(),
           YahooJapanTool(),
           TavilyTool()
       ]

       def execute(self, company_name, date_range):
           # 최근 뉴스, 공시 기사 수집
           pass
   ```

4. **Media Analyzer Agent**
   ```python
   class MediaAnalyzerAgent:
       """멀티미디어 분석"""
       tools = [
           YouTubeTranscriptTool(),
           ImageOCRTool(),
           VideoAnalysisTool()
       ]

       def execute(self, media_urls):
           # YouTube, 이미지, 영상 분석
           pass
   ```

5. **Social Intelligence Agent**
   ```python
   class SocialIntelligenceAgent:
       """소셜 미디어 분석"""
       tools = [
           LinkedInTool(),
           TwitterTool(),
           GitHubTool()
       ]

       def execute(self, company_name):
           # 직원 정보, 기술 스택, 평판 수집
           pass
   ```

### Phase 2: Analysis Supervisor

**Sub-Agents**:

1. **Financial Analyst Agent**
   ```python
   class FinancialAnalystAgent:
       """재무 분석"""

       def execute(self, financial_data):
           """
           분석 항목:
           - 매출/이익 성장률
           - 재무비율 (유동비율, 부채비율, ROE, ROA)
           - 현금흐름 분석
           - Valuation (PER, PBR, EV/EBITDA)
           """
           pass
   ```

2. **Market Analyst Agent**
   ```python
   class MarketAnalystAgent:
       """시장 분석"""

       def execute(self, market_data):
           """
           분석 항목:
           - 시장 규모 및 성장률
           - 시장 점유율
           - 경쟁 구도
           - 트렌드 및 기회
           """
           pass
   ```

3. **Competitor Analyst Agent**
   ```python
   class CompetitorAnalystAgent:
       """경쟁사 분석"""

       def execute(self, competitors_data):
           """
           분석 항목:
           - 주요 경쟁사 리스트
           - 경쟁 우위 비교
           - 벤치마킹
           - SWOT 분석
           """
           pass
   ```

4. **Team Evaluator Agent**
   ```python
   class TeamEvaluatorAgent:
       """조직/팀 평가"""

       def execute(self, team_data):
           """
           분석 항목:
           - 경영진 배경
           - 핵심 인재
           - 조직 문화
           - 이직률
           """
           pass
   ```

5. **Risk Assessor Agent**
   ```python
   class RiskAssessorAgent:
       """리스크 평가"""

       def execute(self, all_data):
           """
           분석 항목:
           - 재무 리스크
           - 법적 리스크
           - 규제 리스크
           - 평판 리스크
           - ESG 리스크
           """
           pass
   ```

### Phase 3: Reporting Supervisor

**Sub-Agents**:

1. **Report Writer Agent**
   ```python
   class ReportWriterAgent:
       """보고서 작성"""

       def execute(self, analysis_results):
           """
           섹션:
           - Executive Summary
           - Company Overview
           - Financial Analysis
           - Market & Competitive Position
           - Team & Organization
           - Risk Assessment
           - Valuation & Recommendation
           """
           pass
   ```

2. **Fact Checker Agent**
   ```python
   class FactCheckerAgent:
       """팩트 체크"""

       def execute(self, report):
           """
           검증:
           - 수치 정확성
           - 출처 확인
           - 모순 검사
           - 최신성 확인
           """
           pass
   ```

3. **Quality Reviewer Agent**
   ```python
   class QualityReviewerAgent:
       """품질 검토"""

       def execute(self, report):
           """
           검토:
           - 완성도
           - 논리성
           - 가독성
           - M&A 관점 적합성
           """
           pass
   ```

---

## 기술 스택

### Core Framework

| 레이어 | 기술 |
|--------|------|
| **Agent Framework** | LangGraph (유연성) + CrewAI (빠른 프로토타입) |
| **LLM** | Claude 3.5 Sonnet (주), GPT-4 (보조) |
| **Vision** | GPT-4 Vision, Claude 3 Vision |
| **Embeddings** | OpenAI ada-002, Cohere multilingual |

### Data Collection

| 목적 | 도구 |
|------|------|
| **Web Scraping** | Firecrawl (주), Playwright, Scrapy |
| **OCR** | GPT-4V, Tesseract, PaddleOCR |
| **Document Parsing** | Unstructured, pdfplumber, python-docx |
| **Video/Audio** | Whisper, YouTube Transcript API |

### Data Sources

| 지역 | API/도구 |
|------|----------|
| **한국** | dart-fss, OpenDartReader, Naver API |
| **일본** | edinet-tools, xbrr |
| **글로벌** | Tavily, SerpAPI, Crunchbase |

### Storage & DB

| 목적 | 기술 |
|------|------|
| **Relational DB** | Supabase PostgreSQL |
| **Vector DB** | Pinecone, Weaviate |
| **Graph DB** | Neo4j (관계 매핑) |
| **Cache** | Redis |
| **Object Storage** | S3, Supabase Storage |

### Infrastructure

| 컴포넌트 | 서비스 |
|----------|---------|
| **Backend** | GCP Cloud Run (Python FastAPI) |
| **Frontend** | Vercel (Next.js) |
| **Queue** | GCP Cloud Tasks, BullMQ |
| **Monitoring** | Sentry, LangSmith |

---

## 구현 로드맵

### Phase 1: MVP (1-2개월)

**목표**: 기본 데이터 수집 + 간단한 분석

- [ ] Week 1-2: 인프라 구축
  - GCP Cloud Run 배포
  - Supabase DB 설정
  - 기본 API 구조

- [ ] Week 3-4: 데이터 수집 (한국 우선)
  - DART API 통합
  - Naver 뉴스 크롤링
  - Firecrawl 웹 스크래핑

- [ ] Week 5-6: 기본 분석 에이전트
  - Financial Analyst
  - Market Analyst
  - Report Writer

- [ ] Week 7-8: 통합 및 테스트
  - End-to-end 워크플로우
  - 10개 샘플 기업 테스트

**Deliverable**: 한국 중소기업 기본 리서치 리포트

### Phase 2: 고도화 (2-3개월)

**목표**: 멀티모달 + 일본 지원 + 고급 분석

- [ ] Month 3: 멀티모달 수집
  - YouTube transcript
  - Image OCR
  - PDF 재무제표 파싱

- [ ] Month 4: 일본 기업 지원
  - EDINET API 통합
  - 일본어 NLP
  - Yahoo Japan 뉴스

- [ ] Month 5: 고급 분석
  - Competitor deep dive
  - Team evaluation
  - Risk assessment

**Deliverable**: 한국+일본 기업 종합 M&A 리포트

### Phase 3: 엔터프라이즈 (3-6개월)

**목표**: 프로덕션 배포 + 자동화 + 확장

- [ ] Month 6-7: 자동화
  - 스케줄링 (주기적 업데이트)
  - 알림 시스템
  - 대시보드

- [ ] Month 8-9: Knowledge Graph
  - Neo4j 관계 매핑
  - 기업 간 연결 분석
  - 계열사 추적

- [ ] Month 10-12: 확장
  - 동남아시아 지원
  - API 서비스화
  - 엔터프라이즈 기능

**Deliverable**: SaaS 서비스 출시

---

## 예상 비용 (월간)

### MVP Phase

| 항목 | 비용 |
|------|------|
| GCP Cloud Run | $20-50 |
| Supabase (Pro) | $25 |
| OpenAI API | $100-200 |
| Anthropic API | $50-100 |
| Tavily API | $130 |
| Firecrawl | $100 |
| **Total** | **$425-630/월** |

### Production Phase

| 항목 | 비용 |
|------|------|
| Infrastructure | $200-500 |
| LLM APIs | $500-1000 |
| Data APIs | $300-500 |
| Vector DB (Pinecone) | $70+ |
| **Total** | **$1,070-2,070/월** |

---

## 다음 단계

### 즉시 시작 가능

1. **DART API 테스트**
   ```bash
   pip install dart-fss
   python test_dart_integration.py
   ```

2. **Firecrawl 프로토타입**
   ```bash
   pip install firecrawl-py
   python test_web_scraping.py
   ```

3. **기본 에이전트 구현**
   ```bash
   # Financial Analyst Agent부터 시작
   python agents/financial_analyst.py
   ```

**MVP 구현을 지금 시작할까요?**
