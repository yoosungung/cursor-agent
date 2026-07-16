# cursor-agent 접목 갭 분석

## 현재 시스템 요약

현재 프로젝트는 Leantime을 협업 채널이자 오케스트레이터로 둔다. `CursorBridge` plugin이 티켓 이벤트, 코멘트, assignee 변경, mention, schedule tick을 받아 agent별 runner에 HTTP 요청을 보낸다. `agent-runner`는 Node/Hono parent와 Cursor SDK worker pool로 분리되어 `Agent.create/resume -> send -> wait -> close`를 수행한다.

불변 계약은 `ARCHITECTURE.md`다. 특히 Cloud Agent 미사용, Leantime 오케스트레이션, 티켓과 Cursor session 1:1, 읽기 우선, 자기 반향 억제, 리뷰 전 ship 필수는 Goose 접목에서도 유지해야 한다.

## 축별 비교

| 축 | cursor-agent | Goose | 판단 |
|----|--------------|-------|------|
| 오케스트레이션 | Leantime plugin이 이벤트 라우팅 | Agent/Recipe/Scheduler가 내부 실행 중심 | Leantime 유지 |
| 실행기 | Cursor SDK local worker pool | Rust Agent + provider abstraction | 단기 교체 부적합 |
| 세션 | `ticket_id -> agent_id` 포인터 + Cursor PVC | SQLite session/message/usage | usage/summary 패턴 참고 |
| 프롬프트 자산 | persona `MEMORY.md`, rules, skills, MCP | recipe, skills, extensions | 일부 recipe화 가능 |
| 스케줄 | K8s CronJob -> plugin -> runner | 내장 scheduler -> recipe session | 구조 교체보다 관측성 참고 |
| Subagent | bot 간 Leantime mention/handoff | child session Agent | ticket 기반 delegation으로 변환 |
| 권한 | Secret/PAT/RBAC/persona | permission mode + inspector | tool class policy 도입 후보 |
| Context | Cursor SDK session 내부 의존 | agent/user visibility + compaction | 외부 summary/handoff 방식 검토 |

## 이식 후보

1. **Turn budget**
   - Goose의 `GOOSE_MAX_TURNS`, recipe `settings.max_turns`, subagent max turns는 runaway run을 줄인다.
   - `agent-runner` job payload나 persona 설정에 ticket/status별 turn budget을 둔다.

2. **Context compaction**
   - 장기 ticket에서 이전 tool output과 논의를 summary로 압축한다.
   - Cursor SDK context 직접 교체가 어렵다면, summary를 다음 prompt의 ticket preamble로 주입하거나 새 session handoff 시 사용한다.

3. **Tool class policy**
   - Goose permission pipeline을 단순화해 read/write/destructive class로 나눈다.
   - `git push`, PR 생성, Leantime comment/status 변경은 audit log를 남기고 허용하되 destructive command는 deny한다.

4. **Recipe retry / success check**
   - 테스트·lint·PR URL·Leantime 상태 같은 완료 조건을 명시한다.
   - 실패 시 같은 ticket session에 "검증 실패 -> 수정" prompt를 넣는 방식으로 구현한다.

5. **Child-session lineage**
   - Goose subagent처럼 parent/child 관계를 추적한다.
   - 현재 모델에서는 Leantime ticket comment에 `delegated_from`, `delegated_to`, 목적, 결과 링크를 남기는 방식이 자연스럽다.

6. **Usage 관측성**
   - Goose는 usage ledger를 session에 붙인다.
   - 이 프로젝트도 ticket/agent/run별 토큰·비용·duration을 로그와 Leantime blocker 판단에 연결할 수 있다.

## 이식 비후보 또는 주의

- Goose `Agent` 전체 교체: 현재 계약은 Cursor SDK local runtime과 Leantime plugin을 전제로 한다.
- Goose scheduler 직접 도입: 현재 schedule 정본은 `agents.yaml`/`bridge.json`이고 Leantime plugin이 dedupe한다.
- Goose 기본 `Auto` 권한: K8s 봇에서 넓은 auto 실행은 위험하다.
- macOS sandbox 의존: runner Pod 환경과 맞지 않는다.
- monolithic loop 복제: `Agent::reply_internal`의 큰 책임을 그대로 옮기면 유지보수 비용이 커진다.
- 공식 문서만 의존: 라이선스와 실행 경로 등에서 문서 드리프트가 있으므로 고정 SHA 코드 링크를 우선한다.

## 접목 옵션

### A. Cursor SDK 유지 + Goose 패턴 선별 도입

가장 보수적인 경로다. `agent-runner`와 Leantime 계약을 유지하면서 turn budget, retry check, tool policy, summary prompt를 추가한다.

장점: 현재 배포와 계약을 깨지 않는다. 위험이 작고 TDD로 단계적 검증이 쉽다.

단점: Cursor SDK 내부 context/session 제어 한계는 남는다.

### B. Goose 실행기 교체

`agent-runner`를 Goose 기반 runner로 바꾸는 경로다.

장점: provider/tool/session/context를 더 직접 제어할 수 있다.

단점: `ARCHITECTURE.md`의 Cursor SDK local runtime 계약을 바꿔야 하고, Leantime MCP/persona/ship workflow를 다시 묶어야 한다.

### C. 병행 PoC

특정 persona나 schedule task 하나만 Goose runner로 실행해 비교한다.

장점: 실제 비용·성공률·권한 위험을 비교할 수 있다.

단점: 두 실행기의 세션·로그·권한 모델을 동시에 운영해야 한다.

## A안 상세 실행 순서

`ARCHITECTURE.md` 계약을 바꾸지 않는다. Goose runner/scheduler 교체는 하지 않는다. 실행 제어는 runner payload·prompt preamble·로그·persona 규칙으로만 얹는다.

| 용어 | 의미 |
|------|------|
| `budget` | 한 run이 얼마나 움직일 수 있는지 (`max_turns`, `timeout_ms`) |
| `policy` | 무엇을 해도 되는지 (`tool_classes`, destructive deny, audit) |
| `context_summary` | Cursor SDK context를 직접 바꾸지 않고, 다음 prompt 앞단에 붙이는 보조 문맥 |
| `success_checks` | schedule/event prompt에 붙이는 완료 검증 기준 문구(강제 shell 실행 아님) |

### Phase 0 — 문서

- 이 문서와 `agent-runner/DESIGN.md`에 A안 실행 정책을 기록한다.
- `ARCHITECTURE.md`에는 부가 정책 링크만 둔다(HTTP/세션 계약 불변).

### Phase 1 — Run budget / observability

- `POST /sessions`, `POST /sessions/{id}/prompt`가 optional `budget`/`policy`/`context_summary`를 수용한다(기존 body 호환).
- Cursor SDK가 turn hard-stop을 보장하지 않으므로 budget은 prompt preamble로 전달한다.
- `run.started` / `run.completed` 로그에 budget·duration 메타를 남긴다.

### Phase 2 — success_checks + hard 검증

- `agents.yaml`/`bridge.json`에 optional `success_checks[]`와 `success_retry.max_attempts`(기본 3)를 둔다.
- Router/ScheduleTicker가 prompt에 검증 기준을 포함하고, `success_checks`/`success_retry`를 runner body와 장애 retry queue에 함께 보존한다.
- runner는 `success_checks`가 있는 run을 **AND**로 판정한다: SDK `status=finished` **그리고** 마지막 완료 tool_call이 성공한 Leantime mutation(`add_comment`/`update_ticket`(active ticket) 또는 ticket 없는 schedule의 `create_ticket`).
- 판정은 stream tool evidence 기반이며 shell을 직접 실행하지 않는다. 실패 시 같은 SDK session에 교정 prompt를 보내고 `max_attempts` 소진 시 `verification_failed`로 종료한다.
- API read-after-write, comment ID 반환, destructive 강제 차단은 다음 강화다. 이 검증은 runner 전송 장애 queue·auth-stale retry와 별개다.

### Phase 3 — context summary preamble

- Leantime Router가 필요 시 `context_summary`를 prompt에 붙이거나 runner metadata로 넘긴다.
- summary는 원문 감사 로그(코멘트/PR)를 대체하지 않는다.

### Phase 4 — tool class / delegation lineage

- persona `MEMORY.md` / `git-ship`에 read·local-write·external-write·destructive 분류를 명시한다.
- mention/handoff prompt에 `delegated_from` / `delegated_to` / 목적을 남긴다.
- prompt-only 정책은 감사 보조다. destructive deny의 강제 장치는 MCP wrapper/runner 정책이 담당할 장기 후보다.

## 권장 다음 단계

M4 운영 안정화와 충돌하지 않게 A 경로부터 시작한다.

1. `agent-runner`에 run별 turn/time budget 정책을 문서화하고 테스트한다.
2. Leantime ticket summary prompt를 만드는 외부 compaction PoC를 설계한다.
3. destructive command deny 정책을 MCP wrapper 또는 runner command policy로 검토한다.
4. schedule retry/success check를 하나의 실사용 schedule에만 적용해 본다.
