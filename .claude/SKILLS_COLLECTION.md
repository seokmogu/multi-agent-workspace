# Nexus Realty - Claude Code Skills Collection

> 풀스택 웹 개발을 위한 바이브 코딩 스킬 모음

**Last Updated**: 2025-10-28
**Total Skills**: 8
**Project**: Nexus Realty (Office Property Search Platform)
**Development Style**: 🤖 100% Vibe Coding with Claude Code

---

## 🎯 Skills Overview

Nexus Realty는 **FastAPI + Next.js 15** 풀스택 개발을 위한 8개 스킬을 제공합니다.

### Skills by Category

| Category | Skills | Purpose |
|----------|--------|---------|
| **Agile (3)** | agile-product, agile-stories, agile-jira | PRD → User Stories → Jira 자동화 |
| **Frontend (1)** | fullstack-frontend | Next.js 14 템플릿 생성 |
| **Testing (1)** | playwright-skill | E2E 테스트 자동화 |
| **Utilities (3)** | skill-creator, workspace-transplant | 스킬 관리, 코드 이식 |

---

## 📝 Agile Skills (Product Management)

### 1. agile-product (PM Role)

**Purpose**: Product Manager를 위한 PRD(Product Requirements Document) 작성

**Key Features**:
- 인터랙티브 Q&A 기반 PRD 생성
- 비즈니스 목표 및 성공 지표 정의
- 사용자 페르소나 및 사용 사례
- 기능/비기능 요구사항
- 범위 정의 (In/Out of Scope)

**Output**:
```
docs/prd/매물-검색-필터링-2025-10-28.md
```

**Usage**:
```bash
/skill agile-product "매물 검색 및 필터링 기능"
```

**Files**:
- `SKILL.md` - 핵심 워크플로우
- `references/prd-guide.md` - 상세 가이드
- `references/prd-example.md` - 전체 예제

**When to Use**:
- 새로운 기능 개발 시작 전
- 요구사항 명확화 필요 시
- 팀 커뮤니케이션용 문서 필요 시

---

### 2. agile-stories (PO/Scrum Master Role)

**Purpose**: PRD를 User Stories로 분해 (Given-When-Then 형식)

**Key Features**:
- PRD 파일 자동 읽기 및 분석
- Epic 구조 식별
- User Story 생성 (Acceptance Criteria 포함)
- Story Points 추정 (Fibonacci)
- Definition of Done 작성

**Output**:
```
docs/stories/
├── 매물-지역-검색.md (5 points)
├── 매물-가격-필터링.md (3 points)
└── 매물-지도-표시.md (8 points)
```

**Usage**:
```bash
/skill agile-stories
# PRD 경로 자동 감지 또는 대화형 선택
```

**Files**:
- `SKILL.md` - 워크플로우
- `references/user-story-guide.md` - AC 작성 예제
- `references/story-template.md` - 템플릿

**When to Use**:
- PRD 작성 완료 후
- Sprint Planning 전
- 백로그 준비 시

---

### 3. agile-jira (Developer/PM Role)

**Purpose**: User Stories를 Jira 티켓으로 자동 생성

**Key Features**:
- Epic/Story/Task 자동 생성
- Jira REST API 직접 호출
- 팀원 자동 할당
- Story Points 연동
- Progress Tracking

**Output**:
```
Jira Project: NEXUS
├── Epic: 매물 검색 기능
│   ├── Story: NEXUS-101 (지역 검색)
│   ├── Story: NEXUS-102 (가격 필터)
│   └── Story: NEXUS-103 (지도 표시)
```

**Usage**:
```bash
/skill agile-jira
# docs/stories/ 디렉토리 자동 스캔
```

**Requirements**:
- `.env` 파일에 Jira 설정 필요:
  ```bash
  JIRA_BASE_URL=https://your-domain.atlassian.net
  JIRA_EMAIL=your-email@example.com
  JIRA_API_TOKEN=your_token
  JIRA_PROJECT_KEY=NEXUS
  ```

**Files**:
- `SKILL.md` - API 통합 워크플로우
- `references/jira-api-reference.md` - Jira REST API 문서

**When to Use**:
- User Stories 완성 후
- Sprint 시작 전
- 백로그를 Jira로 동기화할 때

---

## 🎨 Frontend Development

### 4. fullstack-frontend (Next.js 14)

**Purpose**: Next.js 14 + shadcn/ui 프론트엔드 템플릿 생성

**Key Features**:
- **Next.js 14 App Router** - 최신 파일 기반 라우팅
- **shadcn/ui** - Radix UI + Tailwind CSS 컴포넌트
- **TypeScript** - 타입 안전성
- **React Query** - 데이터 페칭 및 캐싱
- **Vercel 배포 최적화**

**Template Structure**:
```
nexus-frontend/
├── app/
│   ├── layout.tsx          # Root Layout
│   ├── page.tsx            # Home Page
│   ├── properties/         # 매물 페이지
│   └── admin/              # 관리자 페이지
├── components/
│   ├── ui/                 # shadcn/ui 컴포넌트
│   └── features/           # 기능별 컴포넌트
├── lib/
│   ├── api.ts              # API 클라이언트
│   └── utils.ts            # 유틸리티
└── types/
    └── index.ts            # TypeScript 타입
```

**Usage**:
```bash
# 1. 템플릿 복사
/skill fullstack-frontend

# 2. 프로젝트 이름 입력 (대화형)
→ "nexus-frontend"

# 3. 자동 실행:
#    - 디렉토리 생성
#    - npm 패키지 설치
#    - shadcn/ui 초기화
#    - .env.local 생성
```

**Generated Files**:
- `package.json` - Next.js 15, React 19, Tailwind CSS
- `tsconfig.json` - TypeScript 설정
- `next.config.js` - Next.js 설정
- `tailwind.config.ts` - Tailwind 커스터마이징
- `components.json` - shadcn/ui 설정

**API Integration**:
- `lib/api.ts`에 FastAPI 엔드포인트 설정:
  ```typescript
  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  ```

**When to Use**:
- 프로젝트 초기 Frontend 구조 생성 시
- 백엔드 API 준비 완료 후
- 프로토타입 빠르게 만들 때

**References**:
- `references/api-integration.md` - FastAPI 연동 가이드
- `references/deployment.md` - Vercel 배포 가이드

---

## 🧪 Testing

### 5. playwright-skill (E2E Testing)

**Purpose**: Playwright 기반 브라우저 자동화 및 E2E 테스트

**Key Features**:
- 개발 서버 자동 감지
- 깔끔한 테스트 스크립트 생성 (`/tmp` 저장)
- 크로스 브라우저 테스트 (Chrome, Firefox, Safari)
- 스크린샷 캡처
- 반응형 디자인 검증
- 로그인 플로우 테스트

**Use Cases**:
- 웹사이트 테스트
- 폼 자동 입력
- UX 검증
- 링크 체크
- 반응형 검증

**Usage**:
```bash
# 1. 매물 목록 페이지 테스트
/skill playwright-skill

→ "Test property listing page with filters"

# 2. 생성된 테스트 실행
node /tmp/test-property-listing.js
```

**Example Output**:
```javascript
// /tmp/test-property-listing.js
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  await page.goto('http://localhost:3000/properties');
  await page.fill('input[name="location"]', '강남구');
  await page.click('button[type="submit"]');
  await page.waitForSelector('.property-card');

  console.log('✅ Test passed: Property filtering works');

  await browser.close();
})();
```

**When to Use**:
- UI 개발 완료 후
- 중요한 사용자 플로우 검증
- 배포 전 통합 테스트
- 회귀 테스트 자동화

**Files**:
- `SKILL.md` - 워크플로우
- `API_REFERENCE.md` - Playwright API
- `ANALYSIS.md` - 테스트 전략

---

## 🛠️ Utilities

### 6. skill-creator

**Purpose**: 새로운 Claude Code 스킬 생성 도구

**Key Features**:
- 스킬 템플릿 자동 생성
- Skill-Creator 패턴 준수
- Progressive Disclosure 구조
- References 및 Assets 디렉토리 자동 생성

**Usage**:
```bash
/skill skill-creator "database-query-builder"
```

**When to Use**:
- 반복적인 작업을 스킬로 만들 때
- 팀 표준 워크플로우 자동화
- 커스텀 개발 도구 필요 시

---

### 7. workspace-transplant

**Purpose**: 멀티에이전트 워크스페이스 패턴 이식

**Key Features**:
- LangGraph 에이전트 패턴 분석
- A2A 프로토콜 마이그레이션
- 프롬프트 중앙화
- Rate Limiting 패턴 이식

**Use Cases**:
- 멀티에이전트 아키텍처 마이그레이션
- 재사용 가능한 컴포넌트 추출
- A2A 시스템 전환

**When to Use**:
- 기존 에이전트 코드 재사용
- 아키텍처 패턴 참고
- 분산 시스템 설계 시

**Note**: Nexus Realty는 단일 모놀리식 구조로, 현재는 참고용

---

## 🚀 Recommended Workflow

### Phase 1: Planning (Agile Skills)
```bash
# 1. PRD 작성
/skill agile-product "매물 검색 API"

# 2. User Stories 생성
/skill agile-stories

# 3. Jira 티켓 생성
/skill agile-jira
```

### Phase 2: Frontend Setup
```bash
# Next.js 프로젝트 생성
/skill fullstack-frontend
```

### Phase 3: Development
```bash
# (수동) Backend API 개발 (FastAPI)
# (수동) Frontend 페이지 개발 (Next.js)
```

### Phase 4: Testing
```bash
# E2E 테스트 작성
/skill playwright-skill
```

---

## 📊 Skills Summary

| Skill | Type | Frequency | Automation Level |
|-------|------|-----------|------------------|
| agile-product | Planning | 매 기능마다 | 🤖🤖🤖🤖⚪ 80% |
| agile-stories | Planning | 매 기능마다 | 🤖🤖🤖🤖🤖 100% |
| agile-jira | Planning | 매 Sprint마다 | 🤖🤖🤖🤖🤖 100% |
| fullstack-frontend | Setup | 프로젝트 초기 | 🤖🤖🤖🤖⚪ 80% |
| playwright-skill | Testing | 주요 기능마다 | 🤖🤖🤖⚪⚪ 60% |
| skill-creator | Utility | 필요시 | 🤖🤖🤖🤖⚪ 80% |
| workspace-transplant | Utility | 거의 없음 | 🤖🤖⚪⚪⚪ 40% |

---

## 🗂️ Archived Skills

다음 스킬들은 Nexus Realty 프로젝트에 불필요하여 아카이브되었습니다:

**문서 처리 (4개)**:
- `docx` - Word 문서 처리
- `pdf` - PDF 생성/변환
- `pptx` - PowerPoint 처리
- `xlsx` - Excel 처리

**멀티에이전트 (3개)**:
- `database-designer` - DB 스키마 자동 설계
- `deep-research` - 웹 검색 기반 리서치
- `langgraph-multi-agent` - LangGraph 멀티에이전트 패턴

**위치**: `archive/multi-agent-workspace/.claude/skills/`

---

## 📖 Additional Resources

### Internal Guides
- `.claude/AGILE_SKILLS_V2.md` - Agile 3종 상세 가이드
- `CLAUDE.md` - Nexus Realty 기술 문서
- `README.md` - 프로젝트 개요

### External References
- [Next.js 15 Docs](https://nextjs.org/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [shadcn/ui](https://ui.shadcn.com/)
- [Playwright](https://playwright.dev/)

---

**Last Updated**: 2025-10-28 by Claude Code
**Nexus Realty** v1.0.0
