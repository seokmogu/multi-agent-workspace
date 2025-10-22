# 최소 비용 배포 가이드

> Vercel + Supabase + GCP 무료 티어를 활용한 프로덕션 배포

**목표**: 월 $0-10 범위 내에서 실서비스 운영

---

## 📋 목차

1. [아키텍처 개요](#아키텍처-개요)
2. [무료 티어 분석](#무료-티어-분석)
3. [추천 아키텍처](#추천-아키텍처)
4. [단계별 배포 가이드](#단계별-배포-가이드)
5. [비용 최적화](#비용-최적화)
6. [모니터링](#모니터링)

---

## 아키텍처 개요

### 시스템 요구사항

```
✅ Python 백엔드 (FastAPI)
✅ 비동기 LLM 호출 (15-90초 소요)
✅ 웹 검색 API (Tavily)
✅ 결과 저장 (PostgreSQL)
✅ 사용자 인터페이스 (Web)
✅ 작업 큐 (선택적)
```

### 주요 고려사항

1. **실행 시간**: 한 번의 리서치 = 45-90초
2. **동시성**: 여러 사용자 동시 요청
3. **상태 관리**: 진행 상황 추적
4. **비용**: 최소화 필수

---

## 무료 티어 분석

### Vercel

| 항목 | 무료 티어 |
|------|-----------|
| **대역폭** | 100GB/월 |
| **실행 시간** | Serverless Functions: 100GB-시간 |
| **빌드** | 6000분/월 |
| **도메인** | 무료 (vercel.app) |
| **제한** | Function timeout 10초 (Hobby) / 60초 (Pro) |

⚠️ **문제**: Python 지원 제한적, Timeout 짧음

### Supabase

| 항목 | 무료 티어 |
|------|-----------|
| **데이터베이스** | 500MB PostgreSQL |
| **스토리지** | 1GB |
| **대역폭** | 2GB/월 |
| **Row 수** | 무제한 |
| **API 요청** | 무제한 |
| **Edge Functions** | 500K 실행/월 |

✅ **장점**: PostgreSQL + Realtime + Auth + Storage 올인원

### AWS 무료 티어 (12개월)

| 서비스 | 무료 티어 |
|--------|-----------|
| **EC2** | t2.micro 750시간/월 |
| **Lambda** | 100만 요청/월, 400,000 GB-초 |
| **RDS** | db.t2.micro 750시간/월 (20GB) |
| **S3** | 5GB 저장, 20,000 GET, 2,000 PUT |
| **API Gateway** | 100만 요청/월 |

⚠️ **문제**: 12개월 후 유료 전환

### GCP 무료 티어 (영구)

| 서비스 | 무료 티어 (영구) |
|--------|-----------------|
| **Cloud Run** | 2M 요청/월, 360,000 GB-초 CPU, 200,000 GiB-초 메모리 |
| **Cloud Functions** | 2M 호출/월 |
| **Cloud Storage** | 5GB |
| **Firestore** | 1GB 저장, 50K reads/day |
| **Cloud Build** | 120 빌드분/일 |

✅ **장점**: 영구 무료, Python 완벽 지원, Timeout 유연

---

## 추천 아키텍처

### 옵션 A: 완전 무료 (추천) ⭐

```
┌─────────────────────────────────────────────────────┐
│                    사용자                            │
└──────────────────┬──────────────────────────────────┘
                   │
                   ↓
         ┌─────────────────┐
         │  Vercel (프론트)  │ ← Next.js/React
         │  - 무료 호스팅    │ ← 100GB 대역폭
         └────────┬─────────┘
                  │ API 호출
                  ↓
         ┌─────────────────┐
         │ GCP Cloud Run    │ ← Python FastAPI
         │  (백엔드 API)     │ ← 2M 요청/월 무료
         │  - 컨테이너      │ ← Timeout 3600초
         └────────┬─────────┘
                  │
        ┌─────────┼──────────┐
        │         │          │
        ↓         ↓          ↓
   ┌────────┐ ┌─────────┐ ┌──────────┐
   │Tavily  │ │Anthropic│ │Supabase  │
   │  API   │ │  API    │ │   DB     │
   └────────┘ └─────────┘ └──────────┘
                           ↑
                      500MB 무료
```

**월 예상 비용: $0-5**

### 옵션 B: AWS Lambda (12개월 무료)

```
         ┌─────────────────┐
         │  Vercel (프론트)  │
         └────────┬─────────┘
                  │
                  ↓
         ┌─────────────────┐
         │ API Gateway      │ ← 100만 요청/월 무료
         └────────┬─────────┘
                  │
                  ↓
         ┌─────────────────┐
         │  Lambda (Python) │ ← 100만 요청/월 무료
         │  - 15분 timeout  │ ← 400,000 GB-초
         └────────┬─────────┘
                  │
                  ↓
         ┌─────────────────┐
         │  RDS PostgreSQL  │ ← 750시간/월 무료
         │   (db.t2.micro)  │ ← 20GB
         └─────────────────┘
```

**월 예상 비용: $0 (12개월), 이후 $15-25**

### 옵션 C: 하이브리드 (균형)

```
프론트: Vercel (무료)
백엔드: GCP Cloud Run (무료 2M requests)
DB: Supabase (무료 500MB)
파일: Supabase Storage (무료 1GB)
```

**월 예상 비용: $0-3**

---

## 단계별 배포 가이드

### Phase 1: GCP Cloud Run 백엔드 배포

#### 1.1 프로젝트 구조 조정

```bash
company-search-agent/
├── api/                    # FastAPI 백엔드
│   ├── main.py            # FastAPI 앱
│   ├── routers/
│   │   ├── research.py    # 리서치 엔드포인트
│   │   └── health.py      # 헬스체크
│   └── dependencies.py
│
├── src/                   # 기존 에이전트 코드
│
├── Dockerfile             # GCP Cloud Run용
├── requirements.txt
└── .dockerignore
```

#### 1.2 FastAPI 백엔드 생성

```python
# api/main.py
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from src.agent import build_research_graph, Configuration, DEFAULT_SCHEMA

app = FastAPI(title="Company Research API")

# CORS 설정 (Vercel 프론트엔드 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://*.vercel.app", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchRequest(BaseModel):
    company_name: str
    schema_type: str = "default"  # default, ma_expert, hr_expert
    max_queries: int = 3

class ResearchResponse(BaseModel):
    task_id: str
    status: str
    message: str

@app.get("/")
async def root():
    return {"message": "Company Research API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/research", response_model=ResearchResponse)
async def start_research(request: ResearchRequest, background_tasks: BackgroundTasks):
    """회사 리서치 시작"""
    import uuid

    task_id = str(uuid.uuid4())

    # 백그라운드 태스크로 실행
    background_tasks.add_task(
        run_research,
        task_id,
        request.company_name,
        request.schema_type,
        request.max_queries
    )

    return ResearchResponse(
        task_id=task_id,
        status="started",
        message=f"Research started for {request.company_name}"
    )

@app.get("/api/research/{task_id}")
async def get_research_status(task_id: str):
    """리서치 상태 조회"""
    # Supabase에서 조회
    from api.dependencies import get_supabase_client

    supabase = get_supabase_client()
    result = supabase.table('research_tasks').select('*').eq('id', task_id).execute()

    if not result.data:
        return {"error": "Task not found"}

    return result.data[0]

async def run_research(task_id: str, company_name: str, schema_type: str, max_queries: int):
    """실제 리서치 실행"""
    from api.dependencies import get_supabase_client

    supabase = get_supabase_client()

    # 상태 업데이트: 시작
    supabase.table('research_tasks').insert({
        'id': task_id,
        'company_name': company_name,
        'status': 'running',
        'created_at': 'now()'
    }).execute()

    try:
        # 리서치 실행
        config = Configuration(max_search_queries=max_queries)
        graph = build_research_graph(config)

        result = await graph.ainvoke({
            'company_name': company_name,
            'extraction_schema': DEFAULT_SCHEMA,
            # ... 초기 상태
        })

        # 상태 업데이트: 완료
        supabase.table('research_tasks').update({
            'status': 'completed',
            'result': result['extracted_data'],
            'completed_at': 'now()'
        }).eq('id', task_id).execute()

    except Exception as e:
        # 상태 업데이트: 실패
        supabase.table('research_tasks').update({
            'status': 'failed',
            'error': str(e),
            'completed_at': 'now()'
        }).eq('id', task_id).execute()
```

#### 1.3 Dockerfile 작성

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 앱 코드 복사
COPY . .

# 환경 변수
ENV PORT=8080

# Cloud Run은 PORT 환경 변수로 포트 전달
CMD exec uvicorn api.main:app --host 0.0.0.0 --port ${PORT}
```

#### 1.4 GCP 배포

```bash
# GCP 프로젝트 생성
gcloud projects create company-research-api --name="Company Research"
gcloud config set project company-research-api

# Cloud Run API 활성화
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Docker 이미지 빌드 및 배포
gcloud run deploy company-research-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --timeout 3600 \
  --max-instances 10 \
  --set-env-vars="ANTHROPIC_API_KEY=sk-ant-..." \
  --set-env-vars="TAVILY_API_KEY=tvly-..." \
  --set-env-vars="SUPABASE_URL=https://..." \
  --set-env-vars="SUPABASE_KEY=..."

# 배포 완료! URL 확인
# https://company-research-api-xxx-uc.a.run.app
```

**무료 티어 범위**:
- 2M 요청/월
- 360,000 CPU GB-초
- 200,000 메모리 GiB-초
- 월 ~2,000회 리서치 가능 (무료)

### Phase 2: Supabase 데이터베이스 설정

#### 2.1 Supabase 프로젝트 생성

1. https://supabase.com 접속
2. "New Project" 클릭
3. 프로젝트명: `company-research-db`
4. 데이터베이스 비밀번호 설정
5. 리전 선택: `Northeast Asia (Seoul)` 또는 가까운 곳

#### 2.2 테이블 생성

```sql
-- research_tasks 테이블
CREATE TABLE research_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_name TEXT NOT NULL,
    schema_type TEXT DEFAULT 'default',
    status TEXT NOT NULL DEFAULT 'pending',
    result JSONB,
    error TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- 인덱스 생성
CREATE INDEX idx_tasks_status ON research_tasks(status);
CREATE INDEX idx_tasks_created ON research_tasks(created_at DESC);

-- RLS (Row Level Security) 활성화
ALTER TABLE research_tasks ENABLE ROW LEVEL SECURITY;

-- 정책: 누구나 읽기 가능
CREATE POLICY "Anyone can read tasks"
    ON research_tasks FOR SELECT
    USING (true);

-- 정책: 누구나 생성 가능 (나중에 인증 추가)
CREATE POLICY "Anyone can create tasks"
    ON research_tasks FOR INSERT
    WITH CHECK (true);
```

#### 2.3 Python 클라이언트

```python
# api/dependencies.py
from supabase import create_client, Client
import os

_supabase_client = None

def get_supabase_client() -> Client:
    global _supabase_client

    if _supabase_client is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        _supabase_client = create_client(url, key)

    return _supabase_client
```

### Phase 3: Vercel 프론트엔드 배포

#### 3.1 Next.js 프론트엔드 생성

```bash
# 프론트엔드 디렉토리 생성
npx create-next-app@latest frontend
cd frontend
npm install axios swr
```

#### 3.2 리서치 페이지

```typescript
// pages/index.tsx
import { useState } from 'react';
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export default function Home() {
  const [companyName, setCompanyName] = useState('');
  const [loading, setLoading] = useState(false);
  const [taskId, setTaskId] = useState('');
  const [result, setResult] = useState(null);

  const startResearch = async () => {
    setLoading(true);

    try {
      // 리서치 시작
      const response = await axios.post(`${API_URL}/api/research`, {
        company_name: companyName,
        schema_type: 'default',
        max_queries: 3
      });

      const { task_id } = response.data;
      setTaskId(task_id);

      // 폴링으로 상태 확인
      pollStatus(task_id);
    } catch (error) {
      console.error(error);
      setLoading(false);
    }
  };

  const pollStatus = async (taskId: string) => {
    const interval = setInterval(async () => {
      const response = await axios.get(`${API_URL}/api/research/${taskId}`);
      const { status, result: data } = response.data;

      if (status === 'completed') {
        setResult(data);
        setLoading(false);
        clearInterval(interval);
      } else if (status === 'failed') {
        setLoading(false);
        clearInterval(interval);
        alert('Research failed');
      }
    }, 3000); // 3초마다 확인
  };

  return (
    <div className="container mx-auto p-8">
      <h1 className="text-4xl font-bold mb-8">Company Research Agent</h1>

      <div className="mb-8">
        <input
          type="text"
          value={companyName}
          onChange={(e) => setCompanyName(e.target.value)}
          placeholder="Enter company name"
          className="border p-2 w-full"
        />
        <button
          onClick={startResearch}
          disabled={loading}
          className="mt-4 bg-blue-500 text-white px-6 py-2 rounded"
        >
          {loading ? 'Researching...' : 'Start Research'}
        </button>
      </div>

      {result && (
        <div className="bg-gray-100 p-6 rounded">
          <h2 className="text-2xl font-bold mb-4">Results</h2>
          <pre className="overflow-auto">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
```

#### 3.3 환경 변수

```bash
# .env.local
NEXT_PUBLIC_API_URL=https://company-research-api-xxx-uc.a.run.app
```

#### 3.4 Vercel 배포

```bash
# Vercel CLI 설치
npm i -g vercel

# 배포
vercel

# 프로덕션 배포
vercel --prod
```

**완료**: `https://your-app.vercel.app`

---

## 비용 최적화

### 1. LLM API 비용 최소화

**Anthropic Claude 가격**:
- Input: $3 / 1M tokens
- Output: $15 / 1M tokens

**한 번 리서치당 예상**:
- Input: ~5,000 tokens = $0.015
- Output: ~2,000 tokens = $0.030
- **총: ~$0.045 / 리서치**

**최적화 방법**:
```python
# 1. 캐싱 활용
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_research(company_name):
    # 같은 회사 24시간 내 재조회 시 캐시 반환
    pass

# 2. 토큰 제한
config = Configuration(
    max_search_queries=3,  # 5개 → 3개
    max_reflection_steps=1  # 2개 → 1개
)

# 3. 저렴한 모델 사용 (일부)
# 쿼리 생성: Claude Haiku ($0.25/$1.25)
# 추출: Claude Sonnet (더 정확)
```

### 2. Tavily API 비용

**Tavily 가격**:
- 무료: 1,000 requests/month
- Pro: $130/month (10,000 requests)

**최적화**:
```python
# 검색 결과 캐싱
# 같은 쿼리 7일 내 재사용
```

### 3. 인프라 비용

| 항목 | 무료 티어 | 초과 비용 |
|------|-----------|-----------|
| GCP Cloud Run | 2M req/월 | $0.40 / 1M req |
| Supabase DB | 500MB | $25/월 (Pro) |
| Vercel | 100GB 대역폭 | $20/월 (Pro) |

**예상 월간 비용** (1,000회 리서치):
- LLM: $45
- Tavily: $0 (무료 범위)
- 인프라: $0 (무료 범위)
- **총: ~$45/월**

---

## 모니터링

### 1. GCP Cloud Run 모니터링

```python
# Logging
import logging
from google.cloud import logging as gcp_logging

client = gcp_logging.Client()
client.setup_logging()

logger = logging.getLogger(__name__)
logger.info(f"Research started: {company_name}")
```

### 2. Supabase 대시보드

- Realtime 데이터베이스 상태
- API 사용량
- 스토리지 사용량

### 3. 비용 알림

```bash
# GCP Billing Alert 설정
gcloud alpha billing budgets create \
  --billing-account=XXXXXX \
  --display-name="Monthly Budget" \
  --budget-amount=10 \
  --threshold-rule=percent=50 \
  --threshold-rule=percent=90
```

---

## 추가 개선 사항

### 1. 작업 큐 (선택적)

```python
# Supabase Realtime으로 간단히 구현
# 또는 GCP Cloud Tasks (무료 100만 작업/월)
```

### 2. 캐싱 레이어

```python
# Redis 대신 Supabase DB 활용
CREATE TABLE research_cache (
    company_name TEXT PRIMARY KEY,
    result JSONB,
    cached_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_cache_time ON research_cache(cached_at);
```

### 3. Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/research")
@limiter.limit("10/minute")
async def start_research(...):
    pass
```

---

## 결론

### 최종 추천 스택

```
✅ 프론트엔드: Vercel (Next.js) - 무료
✅ 백엔드: GCP Cloud Run (Python) - 무료 2M req
✅ 데이터베이스: Supabase PostgreSQL - 무료 500MB
✅ 파일 저장: Supabase Storage - 무료 1GB

월 예상 비용: $0-10 (인프라)
월 API 비용: $30-50 (LLM + Tavily)
총 월 비용: $30-60 (1,000회 리서치 기준)
```

### 다음 단계

1. **즉시**: GCP Cloud Run 배포
2. **1주**: Supabase 연동
3. **2주**: Vercel 프론트엔드
4. **1개월**: 모니터링 및 최적화

**배포 스크립트를 지금 생성할까요?**
