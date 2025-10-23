# 배포 가이드 - Multi-Agent Workspace

> LangGraph 멀티 에이전트 시스템 배포 전략

---

## 🎯 개요

Multi-Agent Workspace에서 개발한 에이전트를 프로덕션 환경에 배포하는 방법을 설명합니다.

---

## 📋 배포 옵션

### 옵션 비교

| 배포 방식 | 난이도 | 비용 | 확장성 | 추천 용도 |
|----------|--------|------|--------|----------|
| **로컬 서버** | ⭐ | 무료 | ⭐ | 개발/테스트 |
| **Docker** | ⭐⭐ | 저렴 | ⭐⭐⭐ | 소규모 프로덕션 |
| **LangGraph Cloud** | ⭐ | 중간 | ⭐⭐⭐⭐⭐ | 프로덕션 (공식) |
| **AWS/GCP/Azure** | ⭐⭐⭐ | 변동 | ⭐⭐⭐⭐⭐ | 대규모 프로덕션 |
| **Kubernetes** | ⭐⭐⭐⭐ | 변동 | ⭐⭐⭐⭐⭐ | 엔터프라이즈 |

---

## 🚀 방법 1: 로컬 서버 (개발/테스트)

### 설정

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. 환경 변수 설정
cp .env.example .env
# .env 편집

# 3. 에이전트 실행
python examples/basic_research.py
```

### 장점
- ✅ 설정 간단
- ✅ 무료
- ✅ 빠른 개발 사이클

### 단점
- ❌ 확장성 제한
- ❌ 안정성 낮음
- ❌ 외부 접근 어려움

---

## 🐳 방법 2: Docker (추천 - 소규모)

### 설정

```bash
# 1. Docker 이미지 빌드
docker-compose build

# 2. 컨테이너 실행
docker-compose up -d

# 3. 로그 확인
docker-compose logs -f workspace

# 4. 에이전트 테스트
docker-compose exec workspace python examples/basic_research.py
```

### 프로덕션 배포 (Docker Compose)

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  agent:
    build: .
    image: multi-agent-workspace:latest
    restart: always
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - TAVILY_API_KEY=${TAVILY_API_KEY}
    volumes:
      - ./logs:/workspace/logs
    networks:
      - agent-network

  # (선택) PostgreSQL
  db:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_DB: agents
      POSTGRES_USER: agent_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - agent-network

  # (선택) Redis (캐싱/큐)
  redis:
    image: redis:7-alpine
    restart: always
    networks:
      - agent-network

volumes:
  postgres-data:

networks:
  agent-network:
```

실행:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 장점
- ✅ 일관된 환경
- ✅ 쉬운 배포
- ✅ 격리된 실행
- ✅ 로컬 → 클라우드 이동 용이

### 단점
- ❌ 리소스 오버헤드
- ❌ 오케스트레이션 별도 필요

---

## ☁️ 방법 3: LangGraph Cloud (추천 - 프로덕션)

### 개요

LangGraph Cloud는 LangGraph 에이전트를 위한 공식 배포 플랫폼입니다.

### 설정

```bash
# 1. LangGraph CLI 설치
pip install langgraph-cli

# 2. 프로젝트 초기화
langgraph init

# 3. langgraph.json 설정
{
  "dependencies": ["."],
  "graphs": {
    "company_research": "./src/agents/company_research/graph.py:build_research_graph"
  },
  "env": ".env"
}

# 4. 배포
langgraph deploy
```

### 기능

- ✅ **자동 스케일링**
- ✅ **Streaming 지원**
- ✅ **Checkpoint 관리**
- ✅ **모니터링 내장**
- ✅ **Human-in-the-loop**

### 가격

- 기본: $0.25/1000 토큰
- 추가: 스토리지, 컴퓨팅 사용량 기반

자세한 정보: https://langchain-ai.github.io/langgraph/cloud/

---

## 🌐 방법 4: AWS/GCP/Azure

### AWS Lambda + API Gateway

```yaml
# serverless.yml
service: multi-agent-workspace

provider:
  name: aws
  runtime: python3.11
  region: us-east-1
  timeout: 900  # 15분 (에이전트 실행 시간)
  memorySize: 2048

functions:
  researchAgent:
    handler: src/agents/company_research/handler.lambda_handler
    events:
      - http:
          path: research
          method: post
    environment:
      ANTHROPIC_API_KEY: ${env:ANTHROPIC_API_KEY}
      TAVILY_API_KEY: ${env:TAVILY_API_KEY}

# 배포
sls deploy
```

### GCP Cloud Run

```bash
# 1. Docker 이미지 빌드
docker build -t gcr.io/PROJECT_ID/multi-agent-workspace .

# 2. GCP에 푸시
docker push gcr.io/PROJECT_ID/multi-agent-workspace

# 3. Cloud Run 배포
gcloud run deploy multi-agent-workspace \
  --image gcr.io/PROJECT_ID/multi-agent-workspace \
  --platform managed \
  --region us-central1 \
  --timeout 900 \
  --memory 2Gi \
  --set-env-vars ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
```

### Azure Container Instances

```bash
# 리소스 그룹 생성
az group create --name multi-agent-rg --location eastus

# 컨테이너 인스턴스 생성
az container create \
  --resource-group multi-agent-rg \
  --name multi-agent-workspace \
  --image your-registry.azurecr.io/multi-agent-workspace \
  --cpu 2 --memory 4 \
  --environment-variables \
    ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY} \
    TAVILY_API_KEY=${TAVILY_API_KEY}
```

### 장점
- ✅ 자동 스케일링
- ✅ 관리형 서비스
- ✅ 높은 가용성

### 단점
- ❌ 비용 높음
- ❌ 벤더 종속
- ❌ 복잡한 설정

---

## ⚙️ 방법 5: Kubernetes

### Deployment 설정

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: multi-agent-workspace
spec:
  replicas: 3
  selector:
    matchLabels:
      app: multi-agent
  template:
    metadata:
      labels:
        app: multi-agent
    spec:
      containers:
      - name: agent
        image: your-registry/multi-agent-workspace:latest
        env:
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: agent-secrets
              key: anthropic-key
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
---
apiVersion: v1
kind: Service
metadata:
  name: multi-agent-service
spec:
  selector:
    app: multi-agent
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

배포:
```bash
kubectl apply -f k8s/
```

---

## 📊 FastAPI 서버 추가 (API 제공)

에이전트를 HTTP API로 노출하려면:

```python
# src/server.py
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from src.agents.company_research import Configuration, build_research_graph

app = FastAPI(title="Multi-Agent API")

class ResearchRequest(BaseModel):
    company_name: str
    max_queries: int = 3

@app.post("/research")
async def research(request: ResearchRequest):
    config = Configuration(max_search_queries=request.max_queries)
    graph = build_research_graph(config)

    result = await graph.ainvoke({
        "company_name": request.company_name,
        # ... state 초기화
    })

    return {"result": result["extracted_data"]}

@app.get("/health")
def health():
    return {"status": "ok"}
```

실행:
```bash
uvicorn src.server:app --host 0.0.0.0 --port 8000
```

Dockerfile 업데이트:
```dockerfile
# 마지막 줄 수정
CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 💰 비용 최적화

### 1. API 비용 절감

```python
# Google ADK (무료) + Tavily (유료) 하이브리드
config = Configuration(
    search_provider="hybrid",  # 50% 비용 절감
    max_search_queries=3       # 쿼리 수 제한
)
```

### 2. 캐싱

```python
# Redis 캐싱
import redis
import hashlib

cache = redis.Redis(host='localhost', port=6379)

def get_cached_result(company_name):
    key = hashlib.md5(company_name.encode()).hexdigest()
    cached = cache.get(key)
    if cached:
        return json.loads(cached)
    return None

def cache_result(company_name, result):
    key = hashlib.md5(company_name.encode()).hexdigest()
    cache.setex(key, 86400, json.dumps(result))  # 24시간
```

### 3. Rate Limiting

```python
# slowapi로 요청 제한
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/research")
@limiter.limit("5/minute")  # 분당 5회 제한
async def research(request: ResearchRequest):
    # ...
```

---

## 📈 모니터링

### LangSmith (추천)

```python
# 환경 변수 설정
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_API_KEY=your-key
LANGCHAIN_PROJECT=multi-agent-production
```

### Prometheus + Grafana

```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

---

## 🔒 보안

### 1. API 키 관리

```bash
# AWS Secrets Manager
aws secretsmanager create-secret \
  --name multi-agent/anthropic-key \
  --secret-string "${ANTHROPIC_API_KEY}"

# GCP Secret Manager
echo -n "${ANTHROPIC_API_KEY}" | \
  gcloud secrets create anthropic-key --data-file=-
```

### 2. 네트워크 보안

```yaml
# docker-compose에서 내부 네트워크만
networks:
  agent-network:
    internal: true  # 외부 접근 차단
```

### 3. 인증/인가

```python
# FastAPI에 JWT 인증 추가
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.post("/research")
async def research(request: ResearchRequest, token: str = Depends(security)):
    # 토큰 검증
    verify_token(token)
    # ...
```

---

## 📚 배포 체크리스트

### 배포 전

- [ ] 환경 변수 설정 확인
- [ ] API 키 보안 확인
- [ ] 의존성 버전 고정 (requirements.txt)
- [ ] 테스트 실행 (`pytest`)
- [ ] 로깅 설정
- [ ] 에러 핸들링 검증

### 배포 후

- [ ] Health check 엔드포인트 확인
- [ ] 모니터링 설정
- [ ] 알림 설정 (Slack, Email 등)
- [ ] 백업 전략
- [ ] 롤백 계획
- [ ] 문서 업데이트

---

## 🎯 배포 전략 추천

### 스타트업/개인

**추천**: Docker + GCP Cloud Run
- 저렴한 비용
- 자동 스케일링
- 관리 부담 낮음

```bash
# 빠른 배포
docker build -t gcr.io/PROJECT/agent .
docker push gcr.io/PROJECT/agent
gcloud run deploy agent --image gcr.io/PROJECT/agent
```

### 중소기업

**추천**: LangGraph Cloud
- 공식 플랫폼
- LangGraph 최적화
- 통합 모니터링

```bash
langgraph deploy
```

### 엔터프라이즈

**추천**: Kubernetes + AWS/GCP
- 완전한 제어
- 높은 확장성
- 기존 인프라 통합

---

## 🔗 참고 자료

- [LangGraph Cloud](https://langchain-ai.github.io/langgraph/cloud/)
- [Docker Documentation](https://docs.docker.com/)
- [AWS Lambda](https://aws.amazon.com/lambda/)
- [GCP Cloud Run](https://cloud.google.com/run)
- [Kubernetes](https://kubernetes.io/)

---

**다음**: [모니터링 가이드](MONITORING.md) | [Getting Started](GETTING_STARTED.md)
