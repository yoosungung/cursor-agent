# ACP 개요

## 무엇인가

Agent Client Protocol(ACP)은 **코드 에디터(클라이언트)** 와 **코딩 에이전트** 사이의 통신을 표준화한다. LSP가 언어 서버를 에디터에 붙인 것과 같이, 에이전트마다 에디터별 플러그인을 만들지 않고 동일 인터페이스로 연결한다.

- 클라이언트: Zed, JetBrains IDEs, Neovim 플러그인, VS Code ACP Client, 커스텀 호스트 등
- 에이전트: CLI/런타임이 ACP agent surface를 구현한 프로세스 (또는 브리지 어댑터)

## 전송과 메시지

| 항목 | 값 |
|------|-----|
| Envelope | JSON-RPC 2.0 |
| Framing | newline-delimited JSON (NDJSON), 메시지당 한 줄 |
| 기본 전송 | stdio — 클라이언트가 에이전트를 subprocess로 spawn |
| 방향 | 클라이언트 → stdin 요청/알림, 에이전트 → stdout 응답/알림; 로그는 stderr |
| Protocol version | stable `1` (initialize 시 협상) |

원격(HTTP/WebSocket) 시나리오도 문서·생태계에서 언급되나, IDE 통합의 기준 경로는 stdio다.

## 핵심 흐름

전형적인 세션:

1. `initialize` — protocol version·capability 교환
2. `authenticate` — 에이전트가 광고한 `methodId` (예: Cursor의 `cursor_login`)
3. `session/new` 또는 `session/load` / `session/resume`
4. `session/prompt` — 사용자 프롬프트
5. `session/update` 알림 — 스트리밍 텍스트·tool call·diff 등
6. `session/request_permission` — 민감 작업 승인 (클라이언트가 결정 응답)
7. 선택: `session/cancel`, `session/set_mode`, config option 갱신

에이전트 쪽 스키마(요청)와 클라이언트 쪽 스키마(fs/terminal/permission 콜백)는 양방향이다. 파일 읽기·쓰기·터미널을 **클라이언트가 대리 실행**할지, 에이전트가 자체 도구로 할지 capacity negotiation으로 나뉜다.

## ACP vs MCP

| | ACP | MCP |
|--|-----|-----|
| 축 | 에디터 ↔ 에이전트 | 에이전트 ↔ 도구/데이터 |
| 목적 | UI·세션·권한·스트리밍 UX | 외부 도구·리소스 연결 |
| 관계 | 직교 — 동시에 사용 가능 | ACP 세션 안에서도 MCP 서버를 넘길 수 있음 |

이 프로젝트의 Leantime MCP는 MCP 축이고, ACP는 별도(에디터/호스트 연결) 축이다.

## SDK / Registry

공식·준공식 SDK: Rust (`agent-client-protocol`), TypeScript (`@agentclientprotocol/sdk`), Python, Java, Kotlin 등.

에이전트 배포·발견: [ACP Registry](https://agentclientprotocol.com) / JetBrains·Zed의 registry 흐름. 커스텀 에이전트는 registry 없이 `command` + `args`로 spawn해도 된다.
