# ACP 조사 참고 자료

조사일: 2026-07-16. 링크는 당시 접근 가능한 정본·문서·구현이다.

## 프로토콜·스키마

- <https://agentclientprotocol.com> — 공식 사이트
- <https://agentclientprotocol.com/protocol/v1/schema> — v1 스키마
- <https://github.com/agentclientprotocol/agent-client-protocol> — 스키마/프로토콜 저장소
- <https://www.jetbrains.com/acp/> — JetBrains + Zed 공동 소개·에이전트/클라이언트 목록

## 벤더·하네스 문서

- Cursor ACP: <https://cursor.com/docs/cli/acp>
- Hermes ACP: <https://hermes-agent.nousresearch.com/docs/user-guide/features/acp>
- Hermes programmatic integration (ACP vs TUI gateway vs API): <https://hermes-agent.nousresearch.com/docs/developer-guide/programmatic-integration>
- Hermes ACP feature issue (배경): <https://github.com/NousResearch/hermes-agent/issues/569>

## 어댑터·통합

- Claude agent ACP: agentclientprotocol / Zed 계열 `claude-agent-acp` (GitHub org `agentclientprotocol` 또는 이전 `zed-industries` 경로)
- Codex ACP: `codex-acp` (동상 org)
- 통합 CLI: <https://github.com/openclaw/acpx>
- Antigravity 커뮤니티 예: <https://github.com/hicder/agy-acp>, <https://github.com/joel-jcs/antigravity-acp>

## 해설·2차 자료

- Morph ACP 설명 (ACP vs MCP, 에디터/에이전트 표): <https://www.morphllm.com/agent-client-protocol>
- 생태계 현황 글 (클라이언트/에이전트 표, 시점 주의): <https://tobias-weiss.org/content/ai/agent-client-protocol/>

## 이 저장소 교차 참조

- `ARCHITECTURE.md` — Cursor SDK local + Leantime 계약
- `agent-runner/DESIGN.md` — HTTP runner·worker pool
- `docs/goose/` — Goose 분석; Desktop ACP(`goose serve`) 언급은 `01-architecture.md`
