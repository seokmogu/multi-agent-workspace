# A2A 기반 분산 멀티 에이전트 아키텍처

> Google Agent2Agent (A2A) 프로토콜 기반 프로덕션 레벨 분산 시스템 설계

**버전**: 3.0.0-design
**작성일**: 2025-10-22
**상태**: Architecture Design (구현 예정)

---

## 📋 목차

1. [Executive Summary](#executive-summary)
2. [프로덕션 요구사항](#프로덕션-요구사항)
3. [시스템 아키텍처](#시스템-아키텍처)
4. [에이전트 설계](#에이전트-설계)
5. [통신 프로토콜](#통신-프로토콜)
6. [확장성 전략](#확장성-전략)
7. [성능 및 비용](#성능-및-비용)
8. [마이그레이션 계획](#마이그레이션-계획)

---

## Executive Summary

### 배경

**현재 시스템** (LangGraph 모놀리식):
- 순차 처리: 1,000개 회사 → 12-25시간
- 제한된 확장성
- 단일 장애점

**프로덕션 요구사항**:
- ✅ 대규모 배치 처리 (1,000+ 회사)
- ✅ 병렬 실행
- ✅ 독립 확장
- ✅ 장애 복구
- ✅ 24/7 운영

### 솔루션: A2A 기반 분산 시스템

**성능 향상**:
- 처리 시간: 12시간 → **90초** (480배 빠름)
- 처리량: 40/hour → **400/hour** (10배)
- 회사당 비용: $0.007 → **$0.004** (40% 절감)

**아키텍처 전환**:
```
모놀리식 (v2.0)              분산 시스템 (v3.0)
┌──────────────┐            ┌──────────────────┐
│   단일 프로세스  │            │  API Gateway     │
│   Research    │            └────────┬─────────┘
│      ↓        │                     ↓
│   Extraction  │            ┌──────────────────┐
│      ↓        │            │  Coordinator     │
│   Reflection  │            └──┬───┬───┬───┬───┘
└──────────────┘               ↓   ↓   ↓   ↓
                           R   E   R   S
                           e   x   e   t
                           s   t   f   o
                           e   r   l   r
                           a   a   e   a
                           r   c   c   g
                           c   t   t   e
                           h   i   i
                               o   o
                               n   n

                           (각 10, 5, 2, 1개 인스턴스)
```

---

## 프로덕션 요구사항

### 1. 처리량 요구사항

| 시나리오 | 요구사항 | 현재 (v2.0) | 목표 (v3.0) |
|---------|---------|------------|------------|
| **배치 처리** | 1,000 companies | 12-25시간 | **90초** |
| **실시간 처리** | 50 req/min | 불가능 (순차) | **가능** |
| **동시성** | 100+ concurrent | 1개 | **100+** |
| **일일 처리량** | 10,000 companies/day | 1,920 (80/h × 24) | **9,600 (400/h × 24)** |

### 2. 가용성 요구사항

| 항목 | 요구사항 | 구현 방법 |
|------|---------|----------|
| **Uptime** | 99.9% | 다중 인스턴스, 자동 복구 |
| **장애 복구** | < 1분 | Health check, Auto-restart |
| **부분 장애 허용** | 997/1000 성공 | Agent 재시도, Fallback |
| **데이터 무결성** | 100% | Transaction, Idempotency |

### 3. 확장성 요구사항

| 리소스 | 병목 | 확장 전략 |
|--------|------|----------|
| **Research** | Web search API | 10개 인스턴스 (horizontal) |
| **Extraction** | LLM parsing | 5개 인스턴스 (horizontal) |
| **Reflection** | 가벼움 | 2개 인스턴스 |
| **Database** | I/O | Read replica, Connection pooling |

---

## 시스템 아키텍처

### 전체 구조

```
┌─────────────────────────────────────────────────────────────┐
│                      Client Applications                     │
│                  (Web UI, CLI, API Client)                   │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTPS
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway (Kong)                      │
│  - Authentication (JWT)                                      │
│  - Rate limiting (100 req/min)                              │
│  - Request validation                                        │
└──────────────────────────┬──────────────────────────────────┘
                           │ Internal HTTP
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                  Coordinator Agent (FastAPI)                 │
│  - Workflow orchestration                                    │
│  - Load balancing                                            │
│  - Error recovery                                            │
│  - Progress tracking                                         │
└──┬─────────────┬─────────────┬─────────────┬────────────────┘
   │             │             │             │
   │ A2A         │ A2A         │ A2A         │ A2A
   ↓             ↓             ↓             ↓
┌─────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│Research │  │Extraction│  │Reflection│  │ Storage  │
│Agents   │  │ Agents   │  │ Agents   │  │  Agent   │
│         │  │          │  │          │  │          │
│ 10개    │  │  5개     │  │  2개     │  │  1개     │
│instances│  │instances │  │instances │  │instance  │
└────┬────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
     │            │             │             │
     ↓            ↓             ↓             ↓
┌─────────────────────────────────────────────────────────────┐
│                   Shared Infrastructure                      │
│                                                              │
│  ┌──────────────┐  ┌──────────┐  ┌────────┐  ┌──────────┐ │
│  │ PostgreSQL   │  │  Redis   │  │   S3   │  │CloudWatch│ │
│  │ (Primary +   │  │ (Cache + │  │ (Raw   │  │ (Logging │ │
│  │  Replica)    │  │  Queue)  │  │  Data) │  │ Metrics) │ │
│  └──────────────┘  └──────────┘  └────────┘  └──────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### 네트워크 레이어

```
┌─────────────────────────────────────────────────────────┐
│                     Internet                             │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────┐
│                Load Balancer (ALB)                       │
│                HTTPS (443)                               │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────┐
│              Public Subnet (10.0.1.0/24)                 │
│                                                          │
│  ┌──────────────────┐                                   │
│  │  API Gateway     │  (10.0.1.10)                      │
│  └──────────────────┘                                   │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────┐
│           Private Subnet 1 (10.0.10.0/24)                │
│                 Application Tier                         │
│                                                          │
│  ┌──────────────────┐                                   │
│  │  Coordinator     │  (10.0.10.10)                     │
│  └──────────────────┘                                   │
│                                                          │
│  ┌──────────────────┐                                   │
│  │  Research-1~10   │  (10.0.10.20-29)                  │
│  └──────────────────┘                                   │
│                                                          │
│  ┌──────────────────┐                                   │
│  │  Extraction-1~5  │  (10.0.10.30-34)                  │
│  └──────────────────┘                                   │
│                                                          │
│  ┌──────────────────┐                                   │
│  │  Reflection-1~2  │  (10.0.10.40-41)                  │
│  └──────────────────┘                                   │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────┐
│           Private Subnet 2 (10.0.20.0/24)                │
│                   Data Tier                              │
│                                                          │
│  ┌──────────────────┐  ┌──────────────────┐            │
│  │  PostgreSQL      │  │  Redis           │            │
│  │  Primary         │  │  Primary         │            │
│  │  (10.0.20.10)    │  │  (10.0.20.20)    │            │
│  └──────────────────┘  └──────────────────┘            │
│                                                          │
│  ┌──────────────────┐  ┌──────────────────┐            │
│  │  PostgreSQL      │  │  Redis           │            │
│  │  Replica         │  │  Replica         │            │
│  │  (10.0.20.11)    │  │  (10.0.20.21)    │            │
│  └──────────────────┘  └──────────────────┘            │
└─────────────────────────────────────────────────────────┘
```

---

## 에이전트 설계

### 1. Research Agent

**목적**: 웹 검색 및 리서치 노트 작성

**Agent Card**:
```json
{
  "name": "ResearchAgent",
  "description": "Multi-source web research with Tavily/Google ADK",
  "url": "http://research-{instance-id}:5001",
  "version": "3.0.0",
  "capabilities": {
    "streaming": true,
    "pushNotifications": false,
    "parallelQueries": 10,
    "supportedProviders": ["tavily", "google_adk", "hybrid"]
  },
  "skills": [
    {
      "name": "research_company",
      "description": "Research company and generate structured notes",
      "input_schema": {
        "type": "object",
        "properties": {
          "company_name": {
            "type": "string",
            "description": "Target company name"
          },
          "extraction_schema": {
            "type": "object",
            "description": "JSON schema for data extraction"
          },
          "search_provider": {
            "type": "string",
            "enum": ["tavily", "google_adk", "hybrid"],
            "default": "hybrid"
          },
          "max_queries": {
            "type": "integer",
            "minimum": 1,
            "maximum": 10,
            "default": 3
          },
          "follow_up_queries": {
            "type": "array",
            "items": {"type": "string"},
            "default": []
          }
        },
        "required": ["company_name", "extraction_schema"]
      },
      "output_schema": {
        "type": "object",
        "properties": {
          "research_queries": {
            "type": "array",
            "items": {"type": "string"}
          },
          "search_results": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "url": {"type": "string"},
                "title": {"type": "string"},
                "content": {"type": "string"}
              }
            }
          },
          "research_notes": {
            "type": "string",
            "description": "Structured research notes"
          },
          "metadata": {
            "type": "object",
            "properties": {
              "provider": {"type": "string"},
              "queries_executed": {"type": "integer"},
              "results_found": {"type": "integer"},
              "duration_seconds": {"type": "number"}
            }
          }
        }
      }
    }
  ],
  "resources": {
    "cpu": "8 cores",
    "memory": "16GB",
    "maxConcurrency": 5,
    "timeout": "120s"
  },
  "authentication": {
    "type": "bearer",
    "required": true
  }
}
```

**구현 (Flask)**:
```python
# research_agent/app.py
from flask import Flask, request, jsonify
from src.agent.research import research_node
from src.agent.configuration import Configuration
import asyncio
import json

app = Flask(__name__)

# Agent Card
AGENT_CARD = {
    # ... (위 JSON)
}

# Concurrency limit
semaphore = asyncio.Semaphore(5)

@app.get("/.well-known/agent.json")
def get_agent_card():
    """Agent discovery endpoint"""
    return jsonify(AGENT_CARD)

@app.post("/tasks/send")
async def handle_research_task():
    """Handle synchronous research task"""
    task_request = request.get_json()
    task_id = task_request.get("id")

    # Extract input
    input_data = extract_input_from_task(task_request)

    # Validate input
    if not validate_input(input_data):
        return jsonify({
            "id": task_id,
            "status": {"state": "failed"},
            "error": "Invalid input schema"
        }), 400

    # Acquire semaphore (rate limiting)
    async with semaphore:
        try:
            # Execute research (reuse existing code!)
            config = Configuration(
                max_search_queries=input_data.get("max_queries", 3),
                search_provider=input_data.get("search_provider", "hybrid")
            )

            state = {
                "company_name": input_data["company_name"],
                "extraction_schema": input_data["extraction_schema"],
                "follow_up_queries": input_data.get("follow_up_queries", []),
                "research_queries": [],
                "search_results": [],
                "research_notes": "",
                "messages": []
            }

            result = await research_node(state, config)

            # Create A2A response
            response_task = {
                "id": task_id,
                "status": {"state": "completed"},
                "messages": [
                    task_request.get("message", {}),
                    {
                        "role": "agent",
                        "parts": [{
                            "text": json.dumps({
                                "research_queries": result["research_queries"],
                                "search_results": result["search_results"],
                                "research_notes": result["research_notes"],
                                "metadata": {
                                    "provider": config.search_provider,
                                    "queries_executed": len(result["research_queries"]),
                                    "results_found": len(result["search_results"])
                                }
                            })
                        }]
                    }
                ],
                "artifacts": []
            }

            return jsonify(response_task)

        except Exception as e:
            return jsonify({
                "id": task_id,
                "status": {"state": "failed"},
                "error": str(e)
            }), 500

@app.post("/tasks/submit")
async def handle_async_task():
    """Handle asynchronous research task"""
    # For long-running tasks
    # Store in Redis queue
    # Return task ID immediately
    pass

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

def extract_input_from_task(task):
    """Extract input data from A2A task"""
    try:
        message = task.get("message", {})
        parts = message.get("parts", [])
        if parts and "text" in parts[0]:
            return json.loads(parts[0]["text"])
    except:
        pass
    return {}

def validate_input(input_data):
    """Validate input schema"""
    required = ["company_name", "extraction_schema"]
    return all(k in input_data for k in required)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
```

**Dockerfile**:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy agent code
COPY research_agent/ ./research_agent/
COPY src/ ./src/

# Expose port
EXPOSE 5001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5001/health || exit 1

# Run agent
CMD ["python", "-m", "flask", "--app", "research_agent.app", "run", "--host=0.0.0.0", "--port=5001"]
```

---

### 2. Extraction Agent

**Agent Card**:
```json
{
  "name": "ExtractionAgent",
  "description": "Structured data extraction from research notes",
  "url": "http://extraction-{instance-id}:5002",
  "version": "3.0.0",
  "capabilities": {
    "streaming": false,
    "pushNotifications": false
  },
  "skills": [
    {
      "name": "extract_data",
      "description": "Extract structured JSON data from research notes",
      "input_schema": {
        "type": "object",
        "properties": {
          "research_notes": {"type": "string"},
          "extraction_schema": {"type": "object"},
          "company_name": {"type": "string"}
        },
        "required": ["research_notes", "extraction_schema"]
      },
      "output_schema": {
        "type": "object",
        "properties": {
          "extracted_data": {"type": "object"},
          "confidence_score": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          }
        }
      }
    }
  ],
  "resources": {
    "cpu": "4 cores",
    "memory": "8GB",
    "maxConcurrency": 5,
    "timeout": "60s"
  }
}
```

**구현 코드**: (Research Agent와 유사한 패턴)

---

### 3. Reflection Agent

**Agent Card**:
```json
{
  "name": "ReflectionAgent",
  "description": "Quality evaluation and follow-up query generation",
  "url": "http://reflection-{instance-id}:5003",
  "version": "3.0.0",
  "skills": [
    {
      "name": "reflect_quality",
      "input_schema": {
        "type": "object",
        "properties": {
          "extracted_data": {"type": "object"},
          "extraction_schema": {"type": "object"},
          "company_name": {"type": "string"}
        },
        "required": ["extracted_data", "extraction_schema"]
      },
      "output_schema": {
        "type": "object",
        "properties": {
          "is_complete": {"type": "boolean"},
          "completeness_score": {"type": "number"},
          "missing_fields": {
            "type": "array",
            "items": {"type": "string"}
          },
          "follow_up_queries": {
            "type": "array",
            "items": {"type": "string"}
          },
          "quality_issues": {
            "type": "array",
            "items": {"type": "string"}
          }
        }
      }
    }
  ],
  "resources": {
    "cpu": "2 cores",
    "memory": "4GB",
    "maxConcurrency": 10,
    "timeout": "30s"
  }
}
```

---

### 4. Coordinator Agent

**목적**: 워크플로우 오케스트레이션

**구현**:
```python
# coordinator/app.py
from fastapi import FastAPI, BackgroundTasks, HTTPException
from typing import List, Dict, Optional
import asyncio
import aiohttp
import uuid
from pydantic import BaseModel

app = FastAPI()

# Configuration
RESEARCH_AGENTS = [f"http://research-{i}:5001" for i in range(1, 11)]
EXTRACTION_AGENTS = [f"http://extraction-{i}:5002" for i in range(1, 6)]
REFLECTION_AGENTS = [f"http://reflection-{i}:5003" for i in range(1, 3)]

# Load balancers
research_pool = RoundRobinPool(RESEARCH_AGENTS)
extraction_pool = RoundRobinPool(EXTRACTION_AGENTS)
reflection_pool = RoundRobinPool(REFLECTION_AGENTS)

# Request/Response models
class CompanyResearchRequest(BaseModel):
    company_name: str
    extraction_schema: dict
    max_iterations: int = 2

class BatchResearchRequest(BaseModel):
    companies: List[str]
    extraction_schema: dict
    max_iterations: int = 2

class JobStatus(BaseModel):
    job_id: str
    status: str
    progress: Dict[str, int]
    results: Optional[List[Dict]] = None

# In-memory job store (use Redis in production)
jobs: Dict[str, JobStatus] = {}

@app.post("/research/single")
async def research_single_company(request: CompanyResearchRequest):
    """Synchronous single company research"""

    result = await process_single_company(
        request.company_name,
        request.extraction_schema,
        request.max_iterations
    )

    return result

@app.post("/research/batch")
async def research_batch(
    request: BatchResearchRequest,
    background_tasks: BackgroundTasks
):
    """Asynchronous batch research"""

    job_id = str(uuid.uuid4())

    # Initialize job
    jobs[job_id] = JobStatus(
        job_id=job_id,
        status="submitted",
        progress={
            "total": len(request.companies),
            "completed": 0,
            "failed": 0
        }
    )

    # Run in background
    background_tasks.add_task(
        run_batch_job,
        job_id,
        request.companies,
        request.extraction_schema,
        request.max_iterations
    )

    return {
        "job_id": job_id,
        "status": "submitted",
        "total_companies": len(request.companies)
    }

@app.get("/jobs/{job_id}")
async def get_job_status(job_id: str):
    """Get job status"""

    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    return jobs[job_id]

async def run_batch_job(
    job_id: str,
    companies: List[str],
    schema: dict,
    max_iterations: int
):
    """Background batch processing"""

    jobs[job_id].status = "running"

    # Progress tracker
    progress = ProgressTracker(len(companies))

    # Process all companies in parallel
    tasks = [
        process_single_company_with_tracking(
            company,
            schema,
            max_iterations,
            progress
        )
        for company in companies
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Separate success/failure
    success = [r for r in results if not isinstance(r, Exception)]
    failed = [r for r in results if isinstance(r, Exception)]

    # Update job status
    jobs[job_id].status = "completed"
    jobs[job_id].progress["completed"] = len(success)
    jobs[job_id].progress["failed"] = len(failed)
    jobs[job_id].results = success

async def process_single_company(
    company_name: str,
    schema: dict,
    max_iterations: int
) -> Dict:
    """Process single company through R-E-R loop"""

    follow_up_queries = []
    iteration = 0

    while iteration < max_iterations:
        # Phase 1: Research
        research_result = await send_a2a_task(
            research_pool.get_next(),
            "research_company",
            {
                "company_name": company_name,
                "extraction_schema": schema,
                "follow_up_queries": follow_up_queries
            }
        )

        # Phase 2: Extraction
        extraction_result = await send_a2a_task(
            extraction_pool.get_next(),
            "extract_data",
            {
                "research_notes": research_result["research_notes"],
                "extraction_schema": schema,
                "company_name": company_name
            }
        )

        # Phase 3: Reflection
        reflection_result = await send_a2a_task(
            reflection_pool.get_next(),
            "reflect_quality",
            {
                "extracted_data": extraction_result["extracted_data"],
                "extraction_schema": schema,
                "company_name": company_name
            }
        )

        # Check completion
        if reflection_result["is_complete"]:
            return {
                "company_name": company_name,
                "data": extraction_result["extracted_data"],
                "iterations": iteration + 1,
                "complete": True,
                "completeness_score": reflection_result["completeness_score"]
            }

        # Continue with follow-up
        follow_up_queries = reflection_result["follow_up_queries"]
        iteration += 1

    # Max iterations reached
    return {
        "company_name": company_name,
        "data": extraction_result["extracted_data"],
        "iterations": iteration,
        "complete": False,
        "completeness_score": reflection_result["completeness_score"]
    }

async def send_a2a_task(
    agent_url: str,
    skill_name: str,
    input_data: dict,
    max_retries: int = 3
) -> dict:
    """Send A2A task with retry logic"""

    for attempt in range(max_retries):
        try:
            task = {
                "id": str(uuid.uuid4()),
                "message": {
                    "role": "user",
                    "parts": [{"text": json.dumps(input_data)}]
                }
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{agent_url}/tasks/send",
                    json=task,
                    timeout=aiohttp.ClientTimeout(total=120)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return extract_result_from_task(result)
                    elif response.status == 429:
                        # Rate limit - try different agent
                        if attempt < max_retries - 1:
                            await asyncio.sleep(2 ** attempt)
                            continue
                    else:
                        raise Exception(f"HTTP {response.status}")

        except Exception as e:
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)
                continue
            raise

def extract_result_from_task(task_result: dict) -> dict:
    """Extract data from A2A task response"""
    messages = task_result.get("messages", [])
    if len(messages) > 1:
        agent_message = messages[-1]
        for part in agent_message.get("parts", []):
            if "text" in part:
                return json.loads(part["text"])
    return {}

class RoundRobinPool:
    """Simple round-robin load balancer"""
    def __init__(self, agents: List[str]):
        self.agents = agents
        self.index = 0
        self.lock = asyncio.Lock()

    async def get_next(self) -> str:
        async with self.lock:
            agent = self.agents[self.index]
            self.index = (self.index + 1) % len(self.agents)
            return agent

class ProgressTracker:
    """Thread-safe progress tracker"""
    def __init__(self, total: int):
        self.total = total
        self.completed = 0
        self.failed = 0
        self.lock = asyncio.Lock()

    async def increment(self, failed: bool = False):
        async with self.lock:
            self.completed += 1
            if failed:
                self.failed += 1

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
```

---

## 통신 프로토콜

### A2A Task Lifecycle

```
1. Discovery
   Client → GET http://agent:5001/.well-known/agent.json
   Agent → Agent Card (JSON)

2. Task Submission
   Client → POST http://agent:5001/tasks/send
   {
     "id": "task-123",
     "message": {
       "role": "user",
       "parts": [{"text": "{...input...}"}]
     }
   }

3. Processing
   Agent → state: "working"

4. Completion
   Agent → Response
   {
     "id": "task-123",
     "status": {"state": "completed"},
     "messages": [
       {...user message...},
       {
         "role": "agent",
         "parts": [{"text": "{...output...}"}]
       }
     ]
   }
```

### Error Handling

```python
# Retry with exponential backoff
async def send_with_retry(agent_url, task, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = await send_task(agent_url, task)
            return response
        except aiohttp.ClientError as e:
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)
                continue
            raise

# Fallback to different provider
try:
    result = await send_task(tavily_agent, task)
except RateLimitError:
    result = await send_task(google_agent, task)
```

---

## 확장성 전략

### 수평 확장 (Horizontal Scaling)

```yaml
# docker-compose.scale.yml
version: '3.8'

services:
  research:
    image: company-research:research-agent
    deploy:
      replicas: 10  # Scale to 10 instances
      resources:
        limits:
          cpus: '8'
          memory: 16G
    environment:
      - TAVILY_API_KEY=${TAVILY_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}

  extraction:
    image: company-research:extraction-agent
    deploy:
      replicas: 5
      resources:
        limits:
          cpus: '4'
          memory: 8G

  reflection:
    image: company-research:reflection-agent
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '2'
          memory: 4G
```

### Kubernetes Auto-scaling

```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: research-agent-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: research-agent
  minReplicas: 5
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

---

## 성능 및 비용

### 처리 성능

| 메트릭 | 모놀리식 (v2.0) | A2A 분산 (v3.0) | 개선 |
|--------|----------------|----------------|------|
| **1,000 companies** | 12-25시간 | 90초 | **480-1000x** |
| **처리량/시간** | 40-80 | 400-800 | **10x** |
| **동시 처리** | 1 | 100+ | **100x** |
| **평균 레이턴시** | N/A (배치 only) | 0.8초/회사 | **실시간** |

### 비용 분석

#### 인프라 비용 (월간, AWS 기준)

| 구성 요소 | 사양 | 수량 | 단가 | 월 비용 |
|----------|------|------|------|--------|
| **Research Agent** | c5.2xlarge (8 CPU, 16GB) | 10 | $0.34/h | $2,448 |
| **Extraction Agent** | c5.xlarge (4 CPU, 8GB) | 5 | $0.17/h | $612 |
| **Reflection Agent** | t3.medium (2 CPU, 4GB) | 2 | $0.042/h | $60 |
| **Coordinator** | t3.large (2 CPU, 8GB) | 1 | $0.083/h | $60 |
| **RDS PostgreSQL** | db.t3.large | 1 | $0.145/h | $104 |
| **ElastiCache Redis** | cache.t3.medium | 1 | $0.068/h | $49 |
| **S3** | Standard | - | - | $50 |
| **ALB** | - | 1 | - | $22 |
| **Data Transfer** | - | - | - | $100 |
| **총계** | | | | **$3,505** |

#### API 비용 (월간, 10,000 companies 기준)

| API | 단가 | 사용량 | 비용 |
|-----|------|--------|------|
| **Claude Sonnet 4.5** | $3/$15 per 1M | ~100M tokens | $300-1,500 |
| **Tavily** (50% queries) | $0.005/쿼리 | 15,000 | $75 |
| **Google ADK** (50% queries) | 무료 | 15,000 | $0 |
| **총계** | | | **$375-1,575** |

#### 총 비용

```
월간 총 비용: $3,505 (인프라) + $375-1,575 (API) = $3,880-5,080

월간 처리량: 400 companies/hour × 720 hours = 288,000 companies

회사당 비용: $3,880 / 288,000 = $0.0135
          또는 $5,080 / 288,000 = $0.0176

vs 모놀리식: $0.007 (하지만 처리량 1/10)

실제 비용 효율: 10배 빠른 처리로 인한 기회비용 절감
```

---

## 마이그레이션 계획

### Phase 1: Hybrid 시작 (2주)

**목표**: 기존 코드 재사용 + A2A 래퍼

```
현재 LangGraph 시스템
    ↓
A2A 래퍼 추가 (Flask/FastAPI)
    ↓
3개 에이전트 독립 실행 가능
```

**작업**:
1. Research Agent 래퍼 구현
2. Extraction Agent 래퍼 구현
3. Reflection Agent 래퍼 구현
4. Docker Compose 설정
5. 로컬 테스트 (10개 회사)

### Phase 2: Coordinator 구현 (2주)

**목표**: 오케스트레이션 레이어

```
Coordinator Agent 구현
    ↓
로드 밸런싱 + 재시도 로직
    ↓
100개 회사 배치 테스트
```

**작업**:
1. Coordinator FastAPI 서버
2. Round-robin 로드 밸런서
3. A2A 통신 클라이언트
4. 에러 처리 및 재시도
5. 진행 상황 추적

### Phase 3: 인프라 구축 (2주)

**목표**: 프로덕션 인프라

```
Docker → Docker Compose → Kubernetes
```

**작업**:
1. PostgreSQL + Redis 설정
2. S3 버킷 생성
3. Kubernetes manifest 작성
4. Helm chart 작성
5. CI/CD 파이프라인 (GitHub Actions)

### Phase 4: 성능 최적화 (2주)

**목표**: 1,000개 회사 처리 검증

```
성능 테스트 → 병목 분석 → 최적화
```

**작업**:
1. 부하 테스트 (Locust)
2. 병목 분석 (Prometheus)
3. 캐싱 최적화
4. Connection pooling
5. Auto-scaling 튜닝

### Phase 5: 프로덕션 배포 (1주)

**목표**: 실제 운영 전환

```
Staging 검증 → Production 배포 → 모니터링
```

**작업**:
1. Staging 환경 배포
2. 실제 데이터 마이그레이션
3. Production 배포 (Blue-Green)
4. 모니터링 대시보드 설정
5. 운영 문서 작성

**총 기간**: 9주

---

## 다음 단계

1. **인프라 설계 문서** 작성 (INFRASTRUCTURE_DESIGN.md)
2. **데이터 플로우 설계** 작성 (DATA_FLOW_DESIGN.md)
3. **API 명세** 작성 (API_SPECIFICATION.md)
4. **배포 전략** 상세화 (DEPLOYMENT_STRATEGY.md)
5. **Phase 1 구현** 시작

---

**작성**: 2025-10-22
**버전**: 3.0.0-design
**상태**: Architecture approved, ready for implementation
