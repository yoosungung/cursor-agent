# Tools, Extensions, Permissions

## Extension 모델

Goose tool은 `ExtensionManager`를 통해 노출된다. extension 종류는 stdio MCP, streamable HTTP, builtin, platform, frontend 등으로 나뉜다. tool 이름은 extension prefix와 함께 모델에 제공되거나, 일부 platform extension은 unprefixed tool로 노출된다.

주요 platform extension은 다음과 같다.

| Extension | 역할 |
|-----------|------|
| `developer` | 파일 편집, shell 실행 |
| `analyze` | tree-sitter 기반 코드 구조 분석 |
| `todo` | 세션 내 todo 관리 |
| `summon` | 지식 로드와 subagent delegation |
| `skills` | filesystem/builtin skill discovery |
| `chatrecall` | 과거 대화 검색 |
| `orchestrator` | agent session 관리. hidden/default off |
| `tom` | turn마다 top-of-mind context 주입 |

## Tool dispatch

`Agent::reply_internal`은 provider 응답에서 tool request를 분리한다. frontend tool은 UI 응답을 기다리고, backend tool은 inspection과 permission 단계를 거친 뒤 `dispatch_tool_call`로 실행된다.

tool 실행 결과는 tool response message로 conversation에 추가된다. MCP notification, action-required event, elicitation도 tool stream 경계에서 처리된다.

## Permission pipeline

Goose는 tool 실행 전에 inspector chain을 통과시킨다. security finding, permission store, egress/adversary/repetition inspector가 tool call을 허용·거부·승인 필요로 분류한다. 승인 필요 tool은 confirmation router를 통해 사용자 결정을 기다린다.

권한 모드는 공식 문서상 `auto`, `approve`, `smart_approve` 등이 있다. 기준 구현에서 기본 `Auto`는 넓게 허용하는 쪽이며, `SmartApprove`는 MCP annotation이나 LLM 판정에 의존한다.

## Sandbox와 보안 한계

Goose의 sandbox 문서는 macOS Desktop의 선택적 `sandbox-exec`와 egress proxy 중심이다. K8s headless runner 환경에서 같은 보안 경계를 기대하면 안 된다.

현재 `cursor-agent`는 Secret, PAT, K8s RBAC, persona별 MCP 설정으로 권한을 제한한다. Goose식 tool permission을 접목하려면 다음 질문을 먼저 풀어야 한다.

- Leantime 이벤트로 시작한 headless run에서 누가 tool approval을 할 것인가?
- `git push`, `gh pr create`, `kubectl logs`, Leantime write를 어떤 policy로 분류할 것인가?
- auto mode를 허용할 ticket/status/persona 범위는 어디까지인가?
- 승인 대기 상태를 Leantime 코멘트/상태로 표현할 것인가, runner 내부 queue로 표현할 것인가?

## 현재 프로젝트 접목 후보

가장 현실적인 후보는 Goose 전체 permission UI가 아니라 "tool class 정책"이다.

| Tool class | 예시 | 기본 정책 후보 |
|------------|------|----------------|
| read | `get_ticket`, `get_comments`, `git diff`, `kubectl logs` | allow |
| local write | 파일 수정, 테스트 실행 | allow within workspace |
| external write | `add_comment`, status 변경, PR 생성 | allow with audit log |
| destructive | force push, delete, reset, secret 변경 | deny 또는 human approval |

이 정책은 `agent-runner` prompt/persona만으로는 약하므로, 장기적으로는 MCP wrapper 또는 runner-side command policy로 강제하는 편이 낫다.
