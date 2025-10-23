# 예제 코드

멀티 에이전트 워크스페이스 컴포넌트 사용 예제 모음입니다.

## Company Research Agent

기업 정보 자동 추출을 위한 딥 리서치 자동화 에이전트입니다.

| 예제 | 설명 | 사용 사례 |
|------|------|----------|
| **[basic_research.py](./basic_research.py)** | 기본 스키마로 간단한 사용법 | 빠른 시작, 단일 기업 조사 |
| **[custom_schema.py](./custom_schema.py)** | 커스텀 추출 스키마 | 테크 스타트업 분석, 특화된 필드 |
| **[streaming_example.py](./streaming_example.py)** | 실시간 스트리밍 출력 | 실시간 모니터링, 진행 상황 추적 |
| **[hybrid_search_example.py](./hybrid_search_example.py)** | Tavily + DuckDuckGo 하이브리드 | 최대 커버리지, 폴백 전략 |
| **[google_adk_example.py](./google_adk_example.py)** | Google ADK 통합 | 구글 생태계, 비용 비교 |
| **[free_research_duckduckgo.py](./free_research_duckduckgo.py)** | 100% 무료 (API 키 불필요) | 테스트, 개발, 예산 제약 |

### 빠른 시작

```bash
# 의존성 설치
pip install -r requirements.txt

# 환경 설정
cp .env.example .env
# .env 파일에 API 키 입력

# 기본 예제 실행
python examples/basic_research.py

# 무료 예제 실행 (API 키 불필요)
python examples/free_research_duckduckgo.py
```

---

## Agile 워크플로우 (Claude Code 스킬)

> **참고**: Agile 워크플로우 예제는 `.claude/skills/agile-*/` 디렉토리에 있습니다.
> 각 SKILL.md 파일을 참조하세요.

- **agile-product**: PRD (제품 요구사항 문서) 생성
- **agile-stories**: PRD에서 User Story 생성
- **agile-jira**: Jira 티켓 가져오기 및 관리

**워크플로우**:
```bash
# 1. PRD 생성
/skill agile-product "OAuth 인증"

# 2. User Stories 생성
/skill agile-stories --prd=docs/prd/oauth-authentication-*.md

# 3. Jira로 가져오기
/skill agile-jira --import docs/stories/
```

---

## 디렉토리 구조

```
examples/
├── README.md                          # 이 파일
│
├── basic_research.py                  # Company Research 예제
├── custom_schema.py
├── streaming_example.py
├── hybrid_search_example.py
├── google_adk_example.py
└── free_research_duckduckgo.py
```

향후 예제는 `<컴포넌트>_<기능>.py` 네이밍 규칙을 따릅니다.

---

**최종 업데이트**: 2025-10-23
