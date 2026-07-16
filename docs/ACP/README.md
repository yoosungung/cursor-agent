# ACP (Agent Client Protocol) 조사

에디터↔코딩 에이전트 연결 표준 ACP를 이 프로젝트에 접목하기 전에 검토한 연구 노트다. 구현 계약은 `ARCHITECTURE.md`가 정본이며, 이 디렉터리는 프로토콜·하네스 호환·접목 판단 근거만 담는다.

## 조사 기준

- 조사일: 2026-07-16
- 프로토콜 정본: <https://agentclientprotocol.com>
- 스키마 저장소: <https://github.com/agentclientprotocol/agent-client-protocol> (stable protocol version `1`, release ~v1.4.0)
- 공동 주도: Zed Industries + JetBrains
- 조사 방법: 공식 문서·스키마, JetBrains/Cursor/Hermes 문서, 커뮤니티 어댑터 저장소, 현재 `cursor-agent` 코드·문서 교차 검토

## 한 줄 결론

ACP는 멀티 하네스(IDE·CLI 에이전트)를 하나의 클라이언트로 묶을 때 적합한 계층이다. 이 저장소는 현재 `@cursor/sdk` local HTTP runner에 계약이 고정되어 있어, Cursor 단일 경로를 유지할 때는 SDK가 더 직접적이고, 하네스 교체·병행이 목표가 되면 ACP 클라이언트(또는 `acpx`류 통합 CLI)를 runner에 두는 경로를 검토한다.

## 문서 목록

1. `01-overview.md` — ACP 정의, 전송, 세션 흐름, MCP와의 관계
2. `02-harness-compatibility.md` — Claude / Cursor / Codex / Antigravity / Hermes 등 호환 표
3. `03-gap-with-cursor-agent.md` — 현재 프로젝트와의 접점·갭·접목 옵션
4. `sources.md` — 고정 링크와 참고 자료

## 읽는 순서

프로토콜 자체는 `01` → 하네스 선택은 `02` → 이 저장소 판단은 `03`을 먼저 읽는다.
