# Session과 Context 관리

## SessionManager

Goose의 세션 영속성은 `crates/goose/src/session/session_manager.rs`가 담당한다. `SessionManager`는 session 생성, 조회, message 추가, conversation 교체, usage 기록, export/import, conversation truncate, chat history search를 제공한다.

세션에는 다음 정보가 묶인다.

| 항목 | 설명 |
|------|------|
| conversation | user/assistant/tool message 목록 |
| provider/model | 세션별 provider와 model config |
| usage | 토큰과 비용 누적 |
| recipe | 실행에 사용한 recipe metadata |
| schedule | scheduler가 만든 session 연결 |
| parent_session_id | subagent/child session lineage |
| working_dir | 도구 실행 기준 디렉터리 |

현재 `cursor-agent`의 `cursorbridge_sessions`는 `ticket_id -> Cursor agent_id` 포인터만 보관한다. Goose는 대화 본문과 usage까지 자체 DB에 저장하므로, 상태 소유권이 훨씬 두껍다.

## Conversation visibility

Goose message는 사용자에게 보이는 내용과 agent에게 보이는 내용을 분리한다. compaction 후 원본 메시지는 user-visible로 남기고 agent-visible에서는 빼며, summary message는 agent-only로 넣을 수 있다.

이 방식은 `cursor-agent`에도 참고할 수 있다. Leantime 티켓 코멘트는 사람용 감사 로그로 남기고, runner 내부 agent context는 요약된 agent-only 상태로 관리하는 모델이 가능하다.

## Auto compaction

`crates/goose/src/context_mgmt/mod.rs`의 `check_if_compaction_needed`는 provider가 자체 context를 관리하지 않는 경우 context limit 대비 사용량을 계산한다. 기본 임계치는 `GOOSE_AUTO_COMPACT_THRESHOLD=0.8`이다.

`compact_messages`는 현재 conversation을 요약하고, 계속 진행할 수 있도록 continuation message를 넣는다. non-manual compaction에서는 최근 user message를 보존해 agent가 원래 요청을 잃지 않게 한다.

## Progressive tool response reduction

요약 자체가 context 초과로 실패할 때 Goose는 tool response를 중간부터 단계적으로 제거해 요약 입력을 줄인다. 오래된 tool request/response pair는 별도 tool-pair summarization 대상이 될 수 있다.

장점은 장기 세션을 유지하기 쉽다는 점이다. 단점은 tool 결과의 세부 근거가 summary에 흡수되며, 이후 리뷰·감사에서 원문을 다시 확인해야 할 수 있다는 점이다.

## 현재 프로젝트 접목 후보

- 티켓별 Cursor session 장기화에 대비한 자동 요약 정책
- runner 로그와 Leantime 코멘트는 원본 감사 로그로 유지하고 agent context만 압축
- `ticket_id`별 토큰/비용 추적 후 compaction threshold를 운영값으로 조정
- tool 결과 요약 시 PR 링크, commit SHA, Leantime 상태 변경 같은 핵심 증거는 보존 규칙으로 분리

## 주의점

Goose compaction은 provider와 conversation format에 강하게 연결되어 있다. Cursor SDK session 내부 context를 직접 교체할 수 없다면 같은 구현을 그대로 가져오기는 어렵다. 이 프로젝트에서는 "요약 메시지를 다음 prompt에 넣는 외부 compaction" 또는 "새 session으로 handoff하며 summary를 주입"하는 방식부터 검토해야 한다.
