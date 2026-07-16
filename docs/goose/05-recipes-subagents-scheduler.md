# Recipes, Subagents, Scheduler

## Recipe

Goose recipe는 재사용 가능한 실행 단위다. 기준 커밋의 `Recipe` 구조는 다음 필드를 중심으로 한다.

| 필드 | 의미 |
|------|------|
| `title`, `description` | recipe 식별과 설명 |
| `instructions` | system/task instruction |
| `prompt` | session 시작 user prompt |
| `extensions` | 활성화할 extension 목록 |
| `settings` | provider, model, temperature, `max_turns` |
| `parameters` | template 입력값 |
| `response` | JSON schema 등 structured final output |
| `sub_recipes` | child recipe 목록 |
| `retry` | success check, max retries, on_failure |

현재 프로젝트의 persona bundle(`MEMORY.md`, rules, skills, MCP 설정)과 `bridge.json` prompts는 Goose 관점에서 recipe와 extension 설정으로 나눠볼 수 있다. 다만 Leantime ticket scope와 assignee/handoff 규칙은 `ARCHITECTURE.md` 계약이므로 recipe로 흡수하면 안 된다.

## Retry

Recipe retry는 success check가 실패하면 conversation을 초기 상태로 되돌리고 재시도한다. check는 shell command 기반이며, `on_failure` command와 timeout을 가질 수 있다.

이 프로젝트에서는 PR 생성 전 테스트, lint, Leantime 상태 확인 같은 완료 조건을 retry check로 모델링할 수 있다. 다만 현재 runner는 Cursor SDK run을 외부에서 제어하므로, Goose retry 구현을 그대로 쓰기보다 "완료 검증 prompt + runner 재시도 정책"으로 분리하는 편이 현실적이다.

## Subagent

Goose subagent는 child session을 만들고 별도 Agent를 실행한다. `TaskConfig`는 provider, model config, parent session id, working dir, extension, max turns를 담는다. 기본 `GOOSE_SUBAGENT_MAX_TURNS`는 25다.

`summon` platform extension은 지식 로드와 delegation을 제공한다. child agent는 recursive delegation이나 extension/schedule 관리 같은 일부 기능을 막아 parent와 권한 경계를 둔다. async subagent 결과는 notification/session message로 parent 흐름에 연결된다.

현재 프로젝트에서는 이미 bot Pod가 여러 개이고 Leantime ticket/comment가 협업 채널이다. Goose subagent를 그대로 복제하기보다 "같은 티켓에서 다른 bot에게 task를 위임하고 결과를 코멘트로 회수"하는 형태가 더 자연스럽다.

## Scheduler

Goose scheduler는 cron으로 recipe를 실행하고 session을 남긴다. `ScheduledJob`은 id, source, cron, last_run, currently_running, current_session_id, parameters, recipe_base_dir 등을 가진다.

중요한 현행 차이: scheduler의 job 실행은 `AgentManager`를 통하지 않고 `Agent::new()`를 직접 사용한다. 따라서 interactive session과 scheduled session의 lifecycle/extension 복원/정책 적용이 완전히 같은 경로라고 보면 안 된다.

현재 프로젝트는 K8s CronJob `cursorbridge-schedule-tick`이 Leantime plugin의 due schedule을 깨우고, plugin이 runner `/sessions`를 호출한다. 정본은 `deploy/k8s/agents.yaml`의 `settings.schedules` → `bridge.json` 동기화다. 이 구조는 Leantime 오케스트레이션 계약과 잘 맞으므로 Goose scheduler로 교체할 필요성은 낮다.

## 접목 후보

- `settings.max_turns`와 `GOOSE_SUBAGENT_MAX_TURNS` 같은 명시적 turn budget
- recipe `retry`의 success check 개념
- subagent를 parent/child session lineage로 추적하는 모델
- scheduled run도 일반 session 기록으로 남기는 관측성

## 결합 위험

- scheduler와 interactive execution lifecycle이 다른 Goose 현행 구조를 그대로 가져오면 정책 불일치가 생길 수 있다.
- async subagent 상태가 process memory에 의존하면 runner 재시작 시 결과 회수가 어렵다.
- recipe가 persona, prompt, extension, retry를 모두 담으면 현재 `ARCHITECTURE.md`의 계약과 중복될 수 있다.
