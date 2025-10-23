# Getting Started with Multi-Agent Workspace

> 빠른 시작 가이드 - Claude Code로 멀티 에이전트 시스템 개발하기

---

## 🎯 무엇을 할 수 있나요?

이 워크스페이스에서는:

1. **🤖 Claude Code 스킬 사용** - 9개의 즉시 사용 가능한 스킬
2. **📚 공식 레퍼런스 참조** - Google ADK & LangGraph 문서
3. **🛠️ 새 에이전트 개발** - 예제 코드와 가이드 활용

---

## 📋 전제 조건

### 필수

- **Python 3.10+**
- **Claude Code CLI** 설치됨
- **Git** (버전 관리용)

### API 키 (사용할 기능에 따라)

- `ANTHROPIC_API_KEY` - 에이전트 실행 (필수)
- `TAVILY_API_KEY` - 웹 검색 에이전트 ([무료 발급](https://tavily.com/))
- `GOOGLE_API_KEY` - Google ADK 사용 시
- `JIRA_API_TOKEN` - Jira 통합 시

---

## 🚀 5분 빠른 시작

### 1단계: 환경 설정

```bash
# 1. Python 의존성 설치
pip install -r requirements.txt

# 2. 환경 변수 설정 (선택)
cp .env.example .env
# .env 파일 편집 (필요한 API 키 추가)
```

### 2단계: 레퍼런스 문서 확인

```bash
# Claude가 참조할 공식 문서들
cat .claude/references/README.md

# 주요 레퍼런스:
# - google-adk-llms.txt (40KB) - Google ADK 요약
# - langgraph-multi-agent.md (35KB) - 멀티 에이전트 필수 가이드
```

### 3단계: 첫 번째 스킬 사용

```bash
# 예제 1: LangGraph 멀티 에이전트 시스템
/skill langgraph-multi-agent

# 예제 2: PRD 작성 (Agile 워크플로우)
/skill agile-product "OAuth 인증 추가"

# 예제 3: 딥 리서치 에이전트
/skill deep-research
```

---

## 📚 주요 디렉토리 구조

```
multi-agent-workspace/
├── .claude/
│   ├── skills/                    # 🤖 9개 스킬
│   └── references/                # 📚 공식 레퍼런스
│
├── src/agents/
│   └── company_research/          # 예제 에이전트
│
├── examples/                      # 실행 가능한 예제
└── docs/                          # 문서
    ├── GETTING_STARTED.md        # 이 파일
    └── agents/                    # 에이전트별 문서
```

---

## 🎓 학습 경로

### 초보자: Claude Code 스킬 활용

```bash
# 1. 스킬 목록 확인
cat .claude/SKILLS_COLLECTION.md

# 2. 간단한 스킬 사용
/skill agile-product "새 기능 아이디어"

# 3. 결과 확인
ls docs/prd/
```

**학습 포인트**: 스킬이 어떻게 작동하는지 이해

---

### 중급자: 레퍼런스 활용 개발

```bash
# 1. 멀티 에이전트 아키텍처 학습
cat .claude/references/langgraph-multi-agent.md

# 2. Claude에게 레퍼런스 참조 요청
"langgraph-multi-agent.md의 Supervisor 패턴으로
 Customer Support 에이전트 시스템 만들어줘"

# 3. 생성된 코드 확인 및 수정
```

**학습 포인트**: 레퍼런스 문서로 정확한 구현

---

### 고급자: 커스텀 에이전트 개발

```bash
# 1. 예제 에이전트 코드 참고
cd src/agents/company_research/
cat graph.py state.py

# 2. 새 에이전트 디렉토리 생성
mkdir -p src/agents/my_agent

# 3. Claude에게 구현 요청
"langgraph-multi-agent.md와 company_research 예제 참고해서
 src/agents/my_agent/ 에 새 에이전트 만들어줘"
```

**학습 포인트**: 구조화된 에이전트 시스템 설계

---

## 💡 실전 시나리오

### 시나리오 1: Agile 워크플로우 자동화

**목표**: 새 기능의 PRD → User Stories → Jira 티켓 생성

```bash
# 1. PRD 작성
/skill agile-product "사용자 대시보드 추가"
# → docs/prd/user-dashboard-2024-10-23.md 생성

# 2. Git 리뷰 (팀 협업)
git add docs/prd/
git commit -m "Add: User dashboard PRD"
gh pr create --title "PRD: User Dashboard"
# (PR 승인 후)

# 3. User Stories 생성
/skill agile-stories --prd=docs/prd/user-dashboard-2024-10-23.md
# → docs/stories/ 에 5개 스토리 생성

# 4. Git 리뷰
git add docs/stories/
git commit -m "Add: User stories for dashboard"
gh pr create --title "Stories: User Dashboard"
# (PR 승인 후)

# 5. Jira 티켓 생성 (1회 설정 필요)
cd .claude/skills/agile-jira
cp .jira-config.example.json .jira-config.json
# .jira-config.json 편집 (Jira 계정 정보)

# 티켓 생성
/skill agile-jira --import docs/stories/
# → Jira에 Epic + 5개 Story 티켓 자동 생성!
```

**결과**: 자동화된 Agile 워크플로우, Git 기반 협업

---

### 시나리오 2: 멀티 에이전트 시스템 구축

**목표**: Research → Write → Review 협업 에이전트

```bash
# 1. 아키텍처 결정 (레퍼런스 확인)
cat .claude/references/langgraph-multi-agent.md
# → Supervisor 패턴 선택

# 2. Claude에게 구현 요청
"langgraph-multi-agent.md의 Supervisor 패턴으로
 다음 에이전트들이 협업하는 시스템을 만들어줘:

 - ResearcherAgent: 웹에서 정보 수집
 - WriterAgent: 수집된 정보로 보고서 작성
 - ReviewerAgent: 작성된 보고서 검토

 src/agents/report_team/ 에 구현해줘"

# 3. 생성된 코드 확인
tree src/agents/report_team/

# 4. 테스트
python examples/report_team_example.py
```

**결과**: 3개 에이전트가 협업하는 시스템

---

### 시나리오 3: 기업 리서치 자동화

**목표**: 비상장 중소기업 정보 자동 수집

```bash
# 1. 환경 변수 설정
export ANTHROPIC_API_KEY="your-key"
export TAVILY_API_KEY="your-key"

# 2. 기본 리서치 실행
python examples/basic_research.py
# → Anthropic 회사 정보 자동 수집

# 3. 커스텀 스키마로 스타트업 분석
python examples/custom_schema.py
# → 펀딩, 투자자 정보 중심 수집

# 4. 비용 최적화 (하이브리드 검색)
python examples/hybrid_search_example.py
# → Tavily + Google ADK 혼합 사용 (50% 비용 절감)
```

**결과**: 자동화된 기업 리서치 파이프라인

---

## 🛠️ 문제 해결

### "ModuleNotFoundError: No module named 'langgraph'"

```bash
pip install -r requirements.txt
```

### "ANTHROPIC_API_KEY not found"

```bash
# .env 파일 생성
cp .env.example .env

# .env 편집
ANTHROPIC_API_KEY=your-key-here
```

### "스킬을 찾을 수 없습니다"

```bash
# 스킬 디렉토리 확인
ls .claude/skills/

# Claude Code가 .claude/ 디렉토리 인식하는지 확인
cd multi-agent-workspace/
/skill langgraph-multi-agent
```

### "Import 경로 오류"

```bash
# 새 구조: src.agents.company_research
from src.agents.company_research import Configuration

# 구 구조 (사용 금지): src.agent
# from src.agent import Configuration  # ❌
```

---

## 📖 다음 단계

### 더 배우기

1. **스킬 상세 가이드**
   - [Agile 워크플로우](.claude/AGILE_SKILLS_V2.md)
   - [스킬 컬렉션](.claude/SKILLS_COLLECTION.md)

2. **레퍼런스 문서**
   - [Google ADK 가이드](.claude/references/google-adk-llms.txt)
   - [LangGraph 멀티 에이전트](.claude/references/langgraph-multi-agent.md)

3. **에이전트 예제**
   - [Company Research Agent](agents/company_research/README.md)

### 기여하기

새 스킬, 에이전트, 문서 추가를 환영합니다!

```bash
# 새 스킬 만들기
/skill skill-creator

# 새 에이전트 추가
mkdir -p src/agents/my_agent
# 구현 후 문서 작성
```

---

## 🤝 커뮤니티

- [LangGraph 공식 문서](https://langchain-ai.github.io/langgraph/)
- [Google ADK](https://google.github.io/adk-docs/)
- [Claude Code](https://docs.claude.com/claude-code)

---

**Ready to build? 🚀**

다음: [새 에이전트 만들기](CREATE_AGENT.md) | [스킬 목록](.claude/SKILLS_COLLECTION.md)
