# Nexus Realty - 기술 문서

> 사무실 매물 검색 플랫폼 (네이버 부동산 스타일)

**최종 업데이트**: 2025-10-28
**현재 버전**: v1.0.0 (초기 개발)
**프로젝트**: 바이브 코딩 기반 풀스택 웹서비스
**개발 방식**: 🤖 Claude Code 단독 개발 (바이브 코딩 100%)

---

## ⚠️ 핵심 개발 원칙

**바이브 코딩 (Vibe Coding) 우선**:
- 모든 개발은 **Claude Code로만** 진행
- 수동 코딩 최소화, AI 기반 자동화 최대화
- Agile 스킬 활용한 체계적 백로그 관리
- 빠른 프로토타이핑 → 점진적 개선

---

## 📋 목차

1. [Executive Summary](#executive-summary)
2. [프로젝트 개요](#프로젝트-개요)
3. [기술 스택](#기술-스택)
4. [시스템 아키텍처](#시스템-아키텍처)
5. [데이터베이스](#데이터베이스)
6. [개발 환경](#개발-환경)
7. [배포 전략](#배포-전략)
8. [참고 문서](#참고-문서)

---

## Executive Summary

### 프로젝트 목표

**사무실 매물 검색 플랫폼**: 기업 담당자를 위한 스마트 오피스 매칭 서비스

**타겟 사용자**:
- 🏢 기업 담당자 (사무실을 찾는 고객)
- 👨‍💼 사무실 관리 직원 (매물 관리)
- 👑 플랫폼 관리자 (시스템 운영)

### 핵심 기능

1. **매물 검색 및 조회** (네이버 부동산 스타일)
   - 지역/면적/가격 기반 검색
   - 상세 필터링 (교통, 편의시설 등)
   - 지도 기반 검색

2. **사용자 관리**
   - 기업 회원가입/로그인
   - 관심 매물 즐겨찾기
   - 문의/상담 요청

3. **관리자 기능**
   - 매물 관리 (등록/수정/삭제)
   - 사용자 관리
   - 통계 및 분석

### 개발 방식

**🤖 100% 바이브 코딩**:
- Claude Code로만 개발 (수동 코딩 금지)
- Agile 스킬로 PRD → User Story → Jira 티켓 자동화
- fullstack-frontend 스킬로 Next.js 템플릿 자동 생성
- 빠른 프로토타이핑 → 점진적 개선

---

## 프로젝트 개요

### 비즈니스 모델

**B2B 매물 매칭 플랫폼**:
- 네이버 부동산 크롤링 데이터 활용
- 기업 고객 대상 사무실 매물 제공
- 중개 수수료 기반 수익 모델

### 차별점

- 🎯 **기업 특화**: 일반 주거용이 아닌 사무실 전문
- 📊 **스마트 매칭**: 기업 규모/업종 기반 추천
- 🗺️ **입지 분석**: 교통/편의시설 접근성 분석

---

## 기술 스택

### v1.0 (현재 계획)

**프론트엔드**:
| 기술 | 선택 이유 |
|------|----------|
| **Next.js 15** | SSR/SSG, App Router, 성능 최적화 |
| **React 19** | 최신 기능 활용 |
| **TypeScript** | 타입 안정성 |
| **Tailwind CSS** | 빠른 UI 개발 |
| **Shadcn UI** | 고품질 컴포넌트 |

**백엔드**:
| 기술 | 선택 이유 |
|------|----------|
| **FastAPI** | Python 기반 고성능 API |
| **Pydantic** | 데이터 검증 |
| **SQLAlchemy** | ORM |
| **PostgreSQL** | 기존 DB 활용 |

**인프라**:
| 기술 | 선택 이유 |
|------|----------|
| **Docker** | 컨테이너화 |
| **Docker Compose** | 로컬 개발 환경 |
| **Vercel** | Frontend 배포 (예정) |
| **AWS/Cloud** | Backend 배포 (예정) |

---

## 시스템 아키텍처

### 전체 구조 (모노레포)

```
nexus-realty/
├── nexus-api/              # Backend (FastAPI)
│   ├── app/
│   │   ├── api/           # API 엔드포인트
│   │   ├── models/        # SQLAlchemy 모델
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
│   ├── types/             # TypeScript 타입
│   └── package.json
│
├── docker-compose.yml     # 로컬 개발 환경
├── package.json           # 루트 통합 스크립트
└── README.md
```

### API 설계

**목표**: 기존 DB에 RESTful API 레이어 추가

**주요 엔드포인트**:
```
# 매물 (Properties)
GET    /api/properties              # 목록 조회 (페이징, 필터링)
GET    /api/properties/{id}         # 상세 조회
POST   /api/properties/search       # 고급 검색 (지역, 면적, 가격 등)

# 인증 (Auth)
POST   /api/auth/register           # 기업 회원가입
POST   /api/auth/login              # 로그인 (JWT)
POST   /api/auth/logout             # 로그아웃

# 사용자 (Users)
GET    /api/users/me                # 내 정보
GET    /api/users/favorites         # 즐겨찾기 목록
POST   /api/users/favorites/{id}    # 즐겨찾기 추가
DELETE /api/users/favorites/{id}    # 즐겨찾기 삭제

# 문의 (Inquiries)
POST   /api/inquiries               # 문의 등록
GET    /api/inquiries               # 내 문의 목록
GET    /api/inquiries/{id}          # 문의 상세

# 관리자 (Admin)
GET    /api/admin/properties        # 매물 관리
POST   /api/admin/properties        # 매물 등록
PUT    /api/admin/properties/{id}   # 매물 수정
DELETE /api/admin/properties/{id}   # 매물 삭제
GET    /api/admin/users             # 사용자 관리
GET    /api/admin/stats             # 통계 대시보드
```

---

## 데이터베이스

### ✅ 기존 DB 활용

**중요**: 네이버 부동산 매물 데이터가 **이미 PostgreSQL DB에 존재**합니다.

**현황**:
- ✅ 매물 데이터 크롤링 완료 (네이버 부동산)
- ⚠️ 이전 프로젝트 스키마로 구성됨
- 🔧 Nexus Realty에 맞게 일부 테이블 수정 필요
- 🎯 **목표**: 기존 데이터에 API 레이어 추가

### 주요 테이블 (예상 구조)

```sql
-- 매물 정보
properties
├── id (PK)
├── title
├── address
├── area_sqm
├── monthly_rent
├── deposit
├── latitude
├── longitude
└── ...

-- 사용자
users
├── id (PK)
├── email
├── company_name
├── role (customer, staff, admin)
└── ...

-- 즐겨찾기
favorites
├── id (PK)
├── user_id (FK)
├── property_id (FK)
└── created_at

-- 문의
inquiries
├── id (PK)
├── user_id (FK)
├── property_id (FK)
├── message
└── status
```

---

## 개발 환경

### 로컬 개발 (Docker Compose)

```bash
# 전체 스택 실행
docker-compose up

# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# DB: PostgreSQL:5432
```

### 환경 변수 (.env)

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/nexus_realty

# JWT
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256

# CORS
CORS_ORIGINS=http://localhost:3000

# API
API_PREFIX=/api
```

---

## 배포 전략

### ⚡ 프론트엔드/백엔드 분리 배포

**Frontend 배포 (Vercel)**:
```bash
cd nexus-frontend
vercel --prod
# URL: https://nexus-realty.vercel.app
```

**Backend 배포 (클라우드)**:
- 배포 플랫폼은 운영 문서 확인 (docs/ 디렉토리)
- 옵션: AWS ECS, Google Cloud Run, Railway, Render 등
- Docker 컨테이너 기반 배포 권장

**로컬 개발**:
```bash
# 전체 스택 실행 (Frontend + Backend + DB)
docker-compose up
```

---

## 개발 워크플로우 (바이브 코딩)

### 🤖 Claude Code 스킬 활용

**1. Agile 워크플로우** (자동화):
```bash
# PRD 작성
/skill agile-product "매물 검색 필터링 기능"

# User Stories 자동 생성
/skill agile-stories

# Jira 티켓 자동 생성
/skill agile-jira
```

**2. 프론트엔드 개발** (자동화):
```bash
# Next.js 14 템플릿 자동 생성
/skill fullstack-frontend

# 컴포넌트/페이지 자동 생성
# (스킬 내부 기능 활용)
```

**3. E2E 테스트** (자동화):
```bash
# Playwright 테스트 자동 생성
/skill playwright-skill
```

**활용 가능한 스킬** (총 12개):
| 카테고리 | 스킬 | 용도 |
|---------|------|------|
| **Agile** | agile-product | PRD 작성 |
| | agile-stories | User Story 생성 |
| | agile-jira | Jira 통합 |
| **개발** | fullstack-frontend | Next.js 템플릿 |
| | playwright-skill | E2E 테스트 |
| **문서** | docx, pdf, pptx, xlsx | 문서 처리 |
| **기타** | skill-creator | 새 스킬 생성 |
| | workspace-transplant | 코드 이식 |

---

## 프로젝트 로드맵

### Phase 1: 기반 구축 (1주)
- [ ] 기존 DB 구조 분석 및 스키마 확인
- [ ] Backend API 기본 구조 (FastAPI)
- [ ] Frontend 기본 구조 (Next.js - fullstack-frontend 스킬)
- [ ] Docker Compose 환경 구축

### Phase 2: 핵심 기능 - 매물 API (2주)
- [ ] 매물 조회 API (목록, 상세)
- [ ] 매물 검색 API (필터링)
- [ ] Frontend: 매물 목록 페이지
- [ ] Frontend: 매물 상세 페이지
- [ ] 지도 기반 검색 (Kakao/Naver Map API)

### Phase 3: 사용자 기능 (2주)
- [ ] 인증 시스템 (JWT)
- [ ] 회원가입/로그인 UI
- [ ] 즐겨찾기 API 및 UI
- [ ] 문의 API 및 UI

### Phase 4: 관리자 기능 (1주)
- [ ] Admin 페이지 레이아웃
- [ ] 매물 관리 (CRUD)
- [ ] 사용자 관리
- [ ] 기본 통계 대시보드

### Phase 5: 배포 (1주)
- [ ] Frontend: Vercel 배포
- [ ] Backend: 클라우드 배포
- [ ] 환경 변수 설정
- [ ] 프로덕션 테스트

**총 기간**: 7주

---

## 참고 문서

### 프로젝트 문서
| 문서 | 설명 |
|------|------|
| [README.md](./README.md) | 프로젝트 개요 및 빠른 시작 |
| [GETTING_STARTED.md](./docs/GETTING_STARTED.md) | 로컬 개발 환경 설정 |
| [DEPLOYMENT_GUIDE.md](./docs/DEPLOYMENT_GUIDE.md) | 배포 가이드 |

### 참고 프로젝트
- **nexus-platform**: 모노레포 구조 참고 (FastAPI + Next.js)
- **네이버 부동산**: UI/UX 참고
- **직방**: 검색 필터링 참고

---

## 기술 부채 및 개선 계획

### 현재 이슈
- ⚠️ DB 스키마 미정의
- ⚠️ API 명세 미작성
- ⚠️ 인증/권한 미구현

### 향후 개선 사항
- 🔄 GraphQL API 고려 (필요시)
- 🔄 실시간 알림 (WebSocket)
- 🔄 AI 기반 매물 추천
- 🔄 모바일 앱 (React Native)

---

## 보안 고려사항

### v1.0 보안 체크리스트
- [ ] JWT 인증 구현
- [ ] HTTPS/TLS 적용
- [ ] SQL Injection 방어 (SQLAlchemy ORM)
- [ ] XSS 방어 (React 기본 제공)
- [ ] CORS 설정
- [ ] 환경 변수 관리 (비밀키 분리)
- [ ] Rate Limiting (API 호출 제한)

---

## 결론

### v1.0 목표

- ✅ **바이브 코딩 환경 완성**: Claude Code로 빠르게 개발
- ✅ **MVP 출시**: 핵심 검색/조회 기능 완성
- ✅ **확장 가능한 구조**: 점진적 기능 추가 가능

### 다음 액션

1. **즉시**: 구조 설계 확정 (nexus-api, nexus-frontend)
2. **1주차**: DB 스키마 정의 및 Backend API 기본 구조
3. **2주차**: Frontend 기본 UI 구현
4. **3주차**: 매물 검색/조회 기능 완성

---

**작성**: 2025-10-28
**버전**: v1.0.0 (초안)
**개발자**: Claude Code Vibe Coder
**라이선스**: MIT

---

**Ready to Build!** 🚀
