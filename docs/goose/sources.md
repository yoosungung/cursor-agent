# Sources

## 조사 기준

- 대상 저장소: <https://github.com/aaif-goose/goose>
- 기준 브랜치: `main`
- 기준 커밋: <https://github.com/aaif-goose/goose/commit/6ccabb0f6ca26a564f7097a5a2676b12e5427755>
- 조사일: 2026-07-15

## Goose 소스 링크

| 주제 | 링크 |
|------|------|
| README | <https://github.com/aaif-goose/goose/blob/6ccabb0f6ca26a564f7097a5a2676b12e5427755/README.md> |
| Agent module | <https://github.com/aaif-goose/goose/blob/6ccabb0f6ca26a564f7097a5a2676b12e5427755/crates/goose/src/agents/mod.rs> |
| Agent loop | <https://github.com/aaif-goose/goose/blob/6ccabb0f6ca26a564f7097a5a2676b12e5427755/crates/goose/src/agents/agent.rs> |
| Tool execution | <https://github.com/aaif-goose/goose/blob/6ccabb0f6ca26a564f7097a5a2676b12e5427755/crates/goose/src/agents/tool_execution.rs> |
| Context management | <https://github.com/aaif-goose/goose/blob/6ccabb0f6ca26a564f7097a5a2676b12e5427755/crates/goose/src/context_mgmt/mod.rs> |
| Session manager | <https://github.com/aaif-goose/goose/blob/6ccabb0f6ca26a564f7097a5a2676b12e5427755/crates/goose/src/session/session_manager.rs> |
| Recipe | <https://github.com/aaif-goose/goose/blob/6ccabb0f6ca26a564f7097a5a2676b12e5427755/crates/goose/src/recipe/mod.rs> |
| Recipe manifest | <https://github.com/aaif-goose/goose/blob/6ccabb0f6ca26a564f7097a5a2676b12e5427755/crates/goose/src/recipe/manifest.rs> |
| Subagent handler | <https://github.com/aaif-goose/goose/blob/6ccabb0f6ca26a564f7097a5a2676b12e5427755/crates/goose/src/agents/subagent_handler.rs> |
| Subagent task config | <https://github.com/aaif-goose/goose/blob/6ccabb0f6ca26a564f7097a5a2676b12e5427755/crates/goose/src/agents/subagent_task_config.rs> |
| Scheduler | <https://github.com/aaif-goose/goose/blob/6ccabb0f6ca26a564f7097a5a2676b12e5427755/crates/goose/src/scheduler.rs> |
| Retry manager | <https://github.com/aaif-goose/goose/blob/6ccabb0f6ca26a564f7097a5a2676b12e5427755/crates/goose/src/agents/retry.rs> |
| Permission module | <https://github.com/aaif-goose/goose/blob/6ccabb0f6ca26a564f7097a5a2676b12e5427755/crates/goose/src/permission/mod.rs> |
| Platform extensions | <https://github.com/aaif-goose/goose/blob/6ccabb0f6ca26a564f7097a5a2676b12e5427755/crates/goose/src/agents/platform_extensions/mod.rs> |
| CLI entry | <https://github.com/aaif-goose/goose/blob/6ccabb0f6ca26a564f7097a5a2676b12e5427755/crates/goose-cli/src/main.rs> |
| Desktop entry | <https://github.com/aaif-goose/goose/blob/6ccabb0f6ca26a564f7097a5a2676b12e5427755/ui/desktop/src/main.ts> |

## Goose 공식 문서와 discussion

- Official docs: <https://goose-docs.ai>
- Recipes: <https://goose-docs.ai/docs/guides/recipes/>
- CLI commands: <https://goose-docs.ai/docs/guides/goose-cli-commands.md>
- Environment variables: <https://goose-docs.ai/docs/guides/environment-variables.md>
- Permissions: <https://goose-docs.ai/docs/guides/goose-permissions/>
- Subagents tutorial: <https://goose-docs.ai/docs/tutorials/subagents/>
- Agent loop unrolling proposal: <https://github.com/aaif-goose/goose/discussions/9944>
- Unified execution discussion: <https://github.com/aaif-goose/goose/discussions/4389>
- Subagents as platform extension PR: <https://github.com/aaif-goose/goose/pull/6160>

## 현재 프로젝트 근거

| 주제 | 경로 |
|------|------|
| 불변 계약과 인터페이스 | `ARCHITECTURE.md` |
| 진행 현황 | `ROADMAP.md` |
| runner 설계 | `agent-runner/DESIGN.md` |
| runner API/worker pool | `agent-runner/src/` |
| Leantime plugin routing/session/retry/schedule | `leantime-plugin/` |
| 배포와 persona bundle | `deploy/k8s/`, `deploy/personas/` |

## 해석 원칙

- 현재 구현 사실은 고정 커밋의 소스 링크를 우선한다.
- 공식 문서는 사용자-facing 개념 설명으로 참고하되, 코드와 다르면 문서 드리프트로 기록한다.
- Discussion과 PR은 설계 의도와 향후 방향의 근거이며, 병합 여부를 확인하지 않은 상태에서 현행 기능으로 간주하지 않는다.
