# cursor-agent 접목 갭 분석

## 현재 시스템 요약

이 프로젝트는 Leantime을 오케스트레이터로 두고, `CursorBridge` 플러그인이 티켓 이벤트를 agent별 `agent-runner` HTTP API로 보낸다. runner는 Node/Hono parent + `@cursor/sdk` worker pool이며 `Agent.create` / `resume` → `send` → `wait` → `close`를 수행한다.

불변 계약은 `ARCHITECTURE.md`다. Cloud Agent 미사용, Leantime 오케스트레이션, 티켓↔Cursor session 1:1, SDK local runtime은 ACP 도입 논의에서도 전제로 둔다.

## 축별 비교

| 축 | cursor-agent (현재) | ACP | 판단 |
|----|---------------------|-----|------|
| 호스트↔에이전트 | Hono HTTP (`/sessions`, `/prompt`) | JSON-RPC stdio (또는 원격 변형) | 계약상 HTTP 유지; ACP는 대안 어댑터 |
| 실행기 | `@cursor/sdk` local | 임의 ACP agent subprocess | Cursor 단일 시 SDK가 충분 |
| 세션 포인터 | `ticket_id` → `agent_id` (플러그인 DB) | ACP `sessionId` (+ load/resume) | 매핑 계층 필요 |
| 권한 | K8s/Secret·persona·MCP 정책 | `session/request_permission` UI 콜백 | 헤드리스 bot은 auto-approve 정책 설계 필요 |
| 멀티 하네스 | Cursor만 | Claude/Codex/Hermes/agy-어댑터 등 | ACP의 주된 이득 |
| 관측 | runner 로그·Leantime 코멘트 | `session/update` 스트림 | 브리지에서 이벤트를 티켓 코멘트로 투영 가능 |

## 이식 후보

1. **ACP client shim in runner (옵션 C용)**  
   특정 persona만 `spawn(agentCmd)` + NDJSON으로 돌리고, HTTP 계약은 그대로 둔다. Cursor SDK worker와 ACP worker를 pool 타입으로 분기.

2. **통합 CLI (`acpx` 등) 경유**  
   하네스별 진입점 차이를 외부 도구에 맡기고, runner는 한 커맨드 표면만 안다.

3. **권한 정책 매핑**  
   헤드리스 K8s에서는 에디터 UI가 없으므로 `allow-once`/`allow-always`를 persona·tool class 정책으로 자동 응답하고 audit log를 남긴다.

4. **세션 바인딩**  
   `cursorbridge_sessions.agent_id`에 ACP session id를 넣거나, runner 내부 맵으로 SDK id와 ACP id를 분리 보관한다.

## 이식 비후보 또는 주의

- **ARCHITECTURE HTTP 계약 폐기 후 전면 ACP 전환**: Leantime 플러그인·재시도 큐·디바운스와 맞물려 비용이 크다.
- **Antigravity 커뮤니티 어댑터를 무핀으로 사용**: 구현이 갈라져 있어 버전 고정 없이 프로덕션 투입은 위험하다.
- **Claude/Codex 어댑터를 “네이티브”로 취급**: 업스트림 CLI 변경 시 브리지 깨짐. 릴리스를 핀한다.
- **Cursor ACP로 현재 SDK runner를 단순 치환**: ACP는 에디터/커스텀 클라이언트용 공식 경로이고, 현재 서버형 오케스트레이션에는 SDK가 이미 맞다. 치환 이득이 불명확하면 유지.

## 접목 옵션

### A. 현상 유지 (Cursor SDK only)

ACP는 문서·연구만. 멀티 하네스 요구가 생기기 전까지 runner를 바꾸지 않는다.

장점: 계약·배포 무변경.  
단점: Claude/Codex/Hermes 등을 같은 Leantime 흐름에 넣기 어렵다.

### B. 병행 PoC — persona 하나 ACP

예: Hermes 또는 `agent acp`(Cursor)만 스케줄/멘션 경로에서 ACP worker로 실행해 성공률·권한·로그를 SDK 경로와 비교한다.

장점: 계약 유지 + 실측.  
단점: pool·관측·세션 맵 이중화.

### C. 멀티 하네스 오케스트레이션

`agents.yaml`에 `runtime: sdk | acp`와 `acp: { command, args, auth }`를 두고 Leantime 라우팅은 공유한다.

장점: ACP의 본래 가치(에이전트 교체).  
단점: ARCHITECTURE·DESIGN·테스트 확장; 어댑터 핀·헤드리스 승인 정책이 필수.

## 권장

단기: **A**. 중기 실험: 요구가 “Cursor 외 하네스”로 명확해지면 **B**. 멀티 벤더가 제품 요구가 되면 **C**와 `02-harness-compatibility.md`의 핀 목록을 설계 입력으로 쓴다.
