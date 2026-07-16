# ROADMAP.md

## 현황 (2026-07-08)

M0–M3 코드·K8s·이미지 배포 완료. **5 agent Pod Running**, bridge.json 5명 동기화, Leantime Pod에 플러그인 파일 복사됨. **My Apps 활성화·실 SDK E2E**만 남음.

---

## M0 — 계약·스파이크 ✅ / 🟡

- [x] ARCHITECTURE.md, bridge.json 스키마
- [x] Comment 훅, agent-runner mock E2E
- [ ] 실 SDK 스파이크 (`AGENT_RUNNER_MOCK=0`, 티켓당 토큰 측정)

## M1 — Plugin + agent-runner ✅ / 🟡

- [x] Listener, Router, SessionStore, RunnerClient, ResilientRunnerClient
- [x] SQLite 파일 영속화, 재시도 큐, `scripts/flush-retries.sh`
- [x] 티켓 뮤텍스 (Router + agent-runner)
- [x] TypeScript `@cursor/sdk` agent-runner, JSON 상관 로그
- [x] `bridge.json` ↔ `agents.yaml` (5 agent)
- [x] Leantime Pod 배포 + **My Apps 등록·활성화** (`composer.json version`, `Services/CursorBridge.php`)

## M2 — K8s ✅

- [x] bot만 StatefulSet (`cursor-agent-{name}`); `type: human`/`openai`는 Pod 미배포; `type` = `human`\|`sessions`\|`openai`
- [x] Secret `cursor-api-key`, `ghcr-pull`
- [x] 이미지 `ghcr.io/yoosungung/cursor-agent-runner:latest` (amd64)
- [x] **5/5 Pod Running**, `/healthz` OK

## M3 — 워크플로 ✅ (코드)

- [x] assignee 핸드오프, status_prompts, @mention
- [x] Leantime 실환경 E2E (티켓 → runner → 코멘트, `LEANTIME_ACCESS_TOKEN_{name}` PAT 등록 후 작성자 검증)

## M4 — 운영 (미결)

- [ ] PVC chat retention CronJob
- [ ] CURSOR_API_KEY spend 알림
- [x] retry queue 주기 flush (`cursorbridge-flush-retries` CronJob, 5분)
- [x] agent 공통/개별 `schedules[]` (`agents.yaml` → `bridge.json`, `cursorbridge-schedule-tick` CronJob)
- [x] agent-runner SDK worker pool (auth 격리·pre-lease recycle·auth-stale retire)
- [x] Goose A안(보수): docs + runner `budget`/`policy` preamble·로그, `success_checks`, context summary, tool-class/delegation prompt (`docs/goose/06-gap-with-cursor-agent.md`)
- [x] Goose A안 Phase 2: `success_checks` hard 검증(SDK `status=finished` AND 마지막 Leantime mutation) + 같은 session 제한 재시도(`success_retry.max_attempts`) → `verification_failed` (`agent-runner/src/success-verify.ts`)

---

## 다음 수동 작업

1. Leantime **My Apps → CursorBridge 활성화**
2. 티켓 assignee=agent → 코멘트/상태 변경으로 E2E 검증
3. `git commit` + `git push` (변경분 다수 unstaged)
