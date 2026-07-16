# 코딩 하네스 ACP 호환

상태 기준: 2026-07-16. 네이티브 = 벤더/프로젝트가 ACP agent 모드를 직접 제공. 어댑터 = 별도 브리지 프로세스가 CLI를 ACP로 감쌈. 커뮤니티 = 비공식·다중 구현 가능.

## 요약 표

| 하네스 | ACP | 진입 명령 (대표) | 비고 |
|--------|-----|------------------|------|
| **Cursor** | 네이티브 | `agent acp` | 공식 CLI 문서. JetBrains ACP 페이지·Registry에 등재. `cursor/*` 확장 메서드 |
| **Claude Code** | 어댑터 | `claude-agent-acp` | Anthropic 네이티브 미채택. Zed/`agentclientprotocol` 쪽 브리지 |
| **Codex (OpenAI)** | 어댑터 | `codex-acp` | JetBrains Registry 등재. 커뮤니티/공식 브리지 경로 |
| **Gemini CLI** | 네이티브 | `gemini` + ACP 플래그/서브커맨드 | 초기 외부 reference 구현으로 자주 인용 |
| **GitHub Copilot CLI** | 네이티브 (preview) | `… --acp` 계열 | public preview |
| **Goose** | 네이티브 | `goose --acp` / Desktop `goose serve` | 이 저장소 `docs/goose/` 참고 |
| **Hermes** | 네이티브 | `hermes acp` / `hermes-acp` | `pip install '.[acp]'`. Zed Registry·승인 UX 문서화 |
| **Antigravity (`agy`)** | 커뮤니티 어댑터 | `agy-acp`, `antigravity-acp` 등 | Google CLI 자체 ACP 없음. stdout/SQLite 브리지 |
| **Cline** | 네이티브 | (프로젝트 문서 기준) | IDE/에이전트 양쪽 생태계 |
| **OpenCode** | 네이티브 | `opencode acp` | Registry 등재 |
| **Factory Droid / Kiro / Kimi / Qwen / Mistral Vibe** | 네이티브 또는 Registry | 각 CLI ACP 모드 | JetBrains ACP ecosystem 목록 |

통합 CLI 예시: [openclaw/acpx](https://github.com/openclaw/acpx) — 여러 에이전트를 동일 커맨드 표면으로 호출 (`acpx cursor`, `acpx claude`, `acpx codex` …).

## 하네스별 메모

### Cursor

- 문서: <https://cursor.com/docs/cli/acp>
- 인증: `cursor_login` (사전 `agent login` / API key / auth token)
- 모드: `agent` / `plan` / `ask`
- 권한 응답: `allow-once` / `allow-always` / `reject-once`
- 확장(비표준이지만 상호운용 시 처리 권장): `cursor/ask_question`, `cursor/create_plan`, `cursor/update_todos`, `cursor/task`, `cursor/generate_image`
- MCP: 프로젝트/유저 `.cursor/mcp.json` 지원; 대시보드 team MCP는 ACP 모드 미지원(문서 기준)
- IDE 쪽: Neovim(avante.nvim), Zed, JetBrains 가이드 — Cursor를 **에이전트**로, 다른 에디터를 **클라이언트**로 쓰는 패턴

이 저장소의 `agent-runner`는 ACP가 아니라 `@cursor/sdk` HTTP API를 쓴다. Cursor ACP는 “다른 호스트에서 Cursor 에이전트를 돌릴 때”의 공식 경로다.

### Claude Code

- 대표 어댑터: `claude-agent-acp` (agentclientprotocol / Zed 계열)
- 권한 모드·tool call·MCP를 ACP surface로 매핑
- 네이티브 `claude acp`가 없다는 점이 운영 복잡도(어댑터 버전 고정)를 만든다

### Codex

- 대표 어댑터: `codex-acp`
- JetBrains가 Codex를 ACP ecosystem 에이전트로 소개
- OpenAI CLI를 직접 stdio ACP로 쓰기보다 브리지가 일반적

### Hermes (NousResearch)

- 공식: `hermes acp` — JSON-RPC stdio 서버
- extra: `agent-client-protocol` 의존 (`pip install 'hermes-agent[acp]'` 등)
- 에디터용 toolset `hermes-acp` (file/terminal/web/memory/skills …); 메시징·cron 등은 제외
- 승인: allow once / allow for session / allow always / deny
- VS Code ACP Client, Zed Registry, JetBrains 플러그인 경로 문서화

### Antigravity (`agy`)

- Google Antigravity CLI는 조사 시점 **네이티브 ACP 미확인**
- 커뮤니티 브리지가 CLI stdout + 로컬 conversation SQLite를 ACP `session/update`·`session/load`로 변환
- 구현이 여럿(`agy-acp`, `antigravity-acp` …)이라 **프로덕션에 쓸 경우 한 어댑터를 핀**해야 한다

## 클라이언트(에디터) 쪽

JetBrains ACP 페이지 기준 예: JetBrains IDEs, Zed, Neovim(플러그인), Emacs, Obsidian, marimo, Toad, AionUI 등.

클라이언트가 구현해야 할 최소치:

1. 에이전트 subprocess spawn + NDJSON
2. `session/update` 렌더링
3. `session/request_permission` 응답
4. (선택) fs/terminal client capability, 벤더 확장 메서드
