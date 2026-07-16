# Goose 분석

`aaif-goose/goose`의 자율 에이전트 구조를 이 프로젝트에 접목하기 전에 검토한 분석 노트다. 구현 계약은 `ARCHITECTURE.md`가 정본이며, 이 디렉터리는 외부 프로젝트 연구와 접목 판단 근거만 담는다.

## 조사 기준

- 대상 저장소: <https://github.com/aaif-goose/goose>
- 기준 브랜치: `main`
- 기준 커밋: `6ccabb0f6ca26a564f7097a5a2676b12e5427755` (2026-07-15)
- 공식 문서: <https://goose-docs.ai>
- 조사 방법: GitHub 소스, 공식 문서, 관련 discussion/PR, 현재 `cursor-agent` 코드·문서 교차 검토

## 한 줄 결론

Goose는 그대로 교체하기보다 `context compaction`, `max_turns`, `recipe retry`, `child session subagent`, `tool inspection -> permission` 같은 실행 제어 패턴을 선별적으로 가져오는 편이 현재 Leantime 중심 아키텍처와 맞다.

## 문서 목록

1. `01-architecture.md` — Goose 패키지 지도와 진입점
2. `02-agent-loop.md` — 에이전트 루프와 자율 실행 흐름
3. `03-session-context.md` — 세션, 대화, context 관리
4. `04-tools-permissions.md` — MCP/extension/tool dispatch/권한
5. `05-recipes-subagents-scheduler.md` — Recipe, subagent, scheduler, retry
6. `06-gap-with-cursor-agent.md` — 현재 프로젝트와의 접점·갭·접목 옵션
7. `sources.md` — 고정 링크와 참고 자료

## 읽는 순서

Goose 자체 구조를 먼저 보려면 `01`부터 `05`까지 읽는다. 현재 프로젝트에 무엇을 가져올지 판단하려면 `06-gap-with-cursor-agent.md`를 먼저 읽고 필요한 세부 근거를 역추적한다.
