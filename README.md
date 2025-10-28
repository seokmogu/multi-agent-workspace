# Nexus Realty

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Next.js 15](https://img.shields.io/badge/Next.js-15-black.svg)](https://nextjs.org/)

> 사무실 매물 검색 플랫폼 (네이버 부동산 스타일)

**🤖 100% Claude Code 바이브 코딩**
**프로젝트 상태**: v1.0.0 (초기 개발)

---

## 🎯 프로젝트 개요

**Nexus Realty**는 기업을 위한 사무실 매물 검색 플랫폼입니다.
네이버 부동산에서 크롤링한 매물 데이터를 기반으로 API를 제공합니다.

### 타겟 사용자
- 🏢 **기업 담당자**: 사무실을 찾는 고객
- 👨‍💼 **사무실 관리 직원**: 매물 관리
- 👑 **플랫폼 관리자**: 시스템 운영

### 핵심 기능
- 🔍 **매물 검색**: 지역/면적/가격 필터링 (네이버 부동산, 직방 스타일)
- 🗺️ **지도 검색**: 위치 기반 매물 탐색
- ⭐ **즐겨찾기**: 관심 매물 관리
- 💬 **문의**: 문의/상담 요청
- 📊 **관리자**: 매물/사용자 관리, 통계

### 데이터
- ✅ **기존 DB 활용**: 네이버 부동산 크롤링 데이터 (PostgreSQL)
- 🎯 **목표**: 기존 데이터에 RESTful API 레이어 추가

---

## 🚀 빠른 시작

### 사전 요구사항

- Python 3.10+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL (기존 DB 활용)

### 설치

```bash
# 저장소 클론
git clone https://github.com/your-username/nexus-realty.git
cd nexus-realty

# 환경 변수 설정
cp .env.example .env
# .env 파일을 열어 DB 연결 정보 등을 설정하세요

# Docker Compose로 전체 스택 실행
docker-compose up
```

### 접속

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 📁 프로젝트 구조

```
nexus-realty/
├── nexus-api/              # Backend (FastAPI)
│   ├── app/
│   │   ├── api/           # API 라우터
│   │   ├── models/        # DB 모델
│   │   ├── schemas/       # Pydantic 스키마
│   │   ├── services/      # 비즈니스 로직
│   │   └── core/          # 설정, 유틸리티
│   ├── main.py
│   └── requirements.txt
│
├── nexus-frontend/         # Frontend (Next.js)
│   ├── app/               # App Router
│   ├── components/        # React 컴포넌트
│   ├── lib/               # 유틸리티
│   └── package.json
│
├── .claude/               # Claude Code 스킬
│   ├── skills/
│   │   ├── agile-product/      # PRD 작성
│   │   ├── agile-stories/      # User Story 생성
│   │   ├── agile-jira/         # Jira 통합
│   │   └── fullstack-frontend/ # Next.js 템플릿
│   └── AGILE_SKILLS_V2.md
│
├── docs/                  # 개발 문서
│   ├── GETTING_STARTED.md
│   └── DEPLOYMENT_GUIDE.md
│
├── docker-compose.yml     # 개발 환경
├── package.json           # 루트 스크립트
├── CLAUDE.md              # 기술 문서
└── README.md              # 이 파일
```

---

## 🛠️ 기술 스택

### Frontend
- **Next.js 15**: React 프레임워크 (App Router)
- **TypeScript**: 타입 안정성
- **Tailwind CSS**: 유틸리티 CSS
- **Shadcn UI**: 고품질 컴포넌트

### Backend
- **FastAPI**: Python 고성능 웹 프레임워크
- **SQLAlchemy**: ORM
- **Pydantic**: 데이터 검증
- **PostgreSQL**: 관계형 데이터베이스

### DevOps
- **Docker**: 컨테이너화
- **Vercel**: Frontend 배포 (예정)
- **AWS/Cloud**: Backend 배포 (예정)

---

## 📚 개발 가이드

### 로컬 개발

#### Backend 단독 실행
```bash
cd nexus-api
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

#### Frontend 단독 실행
```bash
cd nexus-frontend
npm install
npm run dev
```

#### 전체 스택 실행 (Docker)
```bash
docker-compose up
```

---

## 🤖 Claude Code 스킬 활용

Nexus Realty는 바이브 코딩 최적화를 위해 Claude Code 스킬을 활용합니다.

### Agile 워크플로우

```bash
# 1. PRD 작성
/skill agile-product "매물 검색 필터링 기능"

# 2. User Stories 생성
/skill agile-stories --prd=docs/prd/search-filtering.md

# 3. Jira 티켓 생성
/skill agile-jira --import docs/stories/
```

### 사용 가능한 스킬

| 스킬 | 용도 |
|------|------|
| **agile-product** | PRD(Product Requirements Document) 작성 |
| **agile-stories** | User Story 자동 생성 |
| **agile-jira** | Jira 통합 (백로그 관리) |
| **fullstack-frontend** | Next.js 템플릿 및 컴포넌트 생성 |
| **playwright-skill** | E2E 테스트 자동화 |

---

## 📖 문서

### 프로젝트 문서
- **[CLAUDE.md](./CLAUDE.md)**: 기술 문서 (아키텍처, 로드맵, 기술 스택)
- **[GETTING_STARTED.md](./docs/GETTING_STARTED.md)**: 로컬 개발 환경 설정
- **[DEPLOYMENT_GUIDE.md](./docs/DEPLOYMENT_GUIDE.md)**: 배포 가이드

### API 문서
- FastAPI Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🗺️ 로드맵

### Phase 1: 기반 구축 (1주)
- [ ] 기존 DB 스키마 분석
- [ ] Backend API 구조 (FastAPI)
- [ ] Frontend 구조 (Next.js)
- [ ] Docker Compose 환경

### Phase 2: 매물 API (2주)
- [ ] 매물 조회/검색 API
- [ ] Frontend: 매물 목록/상세 페이지
- [ ] 지도 검색

### Phase 3: 사용자 (2주)
- [ ] 인증 (JWT)
- [ ] 즐겨찾기/문의 API

### Phase 4: 관리자 (1주)
- [ ] Admin 페이지
- [ ] 매물/사용자 관리

### Phase 5: 배포 (1주)
- [ ] Vercel (Frontend)
- [ ] 클라우드 (Backend)

**총 기간**: 7주

---

## 🔧 개발 환경 설정

### 환경 변수

`.env` 파일을 생성하고 다음 항목을 설정하세요:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/nexus_realty

# JWT
JWT_SECRET=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# API
API_PREFIX=/api
DEBUG=true
```

### 데이터베이스

**중요**: 네이버 부동산 매물 데이터가 **이미 PostgreSQL DB에 존재**합니다.

```bash
# DB 연결 확인
psql -U postgres -d nexus_realty

# 스키마 확인
\dt

# 일부 테이블은 Nexus Realty에 맞게 수정 필요
```

---

## 🤝 기여

기여를 환영합니다!

### 개발 프로세스
1. 이슈 생성 또는 기존 이슈 확인
2. Feature 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경사항 커밋 (`git commit -m 'Add amazing feature'`)
4. 브랜치 푸시 (`git push origin feature/amazing-feature`)
5. Pull Request 생성

---

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](./LICENSE) 파일을 참조하세요.

---

## 🔗 참고 자료

### 공식 문서
- [FastAPI](https://fastapi.tiangolo.com/)
- [Next.js](https://nextjs.org/)
- [Claude Code](https://docs.claude.com/claude-code)

### 참고 프로젝트
- **nexus-platform**: 모노레포 구조 참고
- **네이버 부동산**: UI/UX 참고
- **직방**: 검색 필터링 참고

---

## 📞 문의

프로젝트 관련 문의사항이 있으시면 이슈를 생성해주세요.

---

**Nexus Realty** v1.0.0
*Built with Claude Code* 🤖

---

## 🎉 시작하기

```bash
# 1. 저장소 클론
git clone https://github.com/your-username/nexus-realty.git

# 2. 환경 변수 설정
cp .env.example .env

# 3. Docker Compose로 실행
docker-compose up

# 4. 브라우저에서 확인
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

**Happy Coding!** 🚀
