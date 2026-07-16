---
name: git-ship
description: >-
  Pod 봇 에이전트가 리뷰 핸드오프 전에 commit·push·PR을 수행한다.
  리뷰 요청, Review 상태, PR 생성, git push, gh pr create, 핸드오프 시 적용한다.
---

# Git ship (리뷰 전 배송)

봇 runner Pod에는 **사람이 없다**. 리뷰어가 diff를 보려면 원격에 push된 커밋과 PR이 있어야 한다. **push·PR은 반드시 에이전트가 수행**한다. 실패해도 사람에게 "로컬에서 push 해주세요"라고 하지 않는다.

## Definition of Ready for Review

아래를 모두 만족한 뒤에만 Leantime Review 핸드오프한다.

1. 테스트·문서(TDD·ARCHITECTURE 등) 반영 완료
2. `git status` clean 또는 의도된 변경만 스테이징
3. `git commit` (의미 있는 메시지)
4. `git push` (feature branch 또는 정책에 맞는 브랜치) — **`git push --force` / `git reset --hard` 금지**
5. PR 열림 — 없으면 `gh pr create`; 있으면 기존 PR 갱신
6. Leantime: 상태 Review, assignee → **메인 리뷰어 candy**, `add_comment`에 PR URL·요약·검증 방법·`@candy` 멘션

허용 범위: `local_write`(커밋) + `external_write`(push/PR/티켓 코멘트). destructive(force-push, hard reset, secret 변경)는 ship에 포함되지 않는다.

## 절차

```bash
cd /workspace/repo   # Pod WORKSPACE
git status
git checkout -b feature/<ticket>-<slug>   # main 직접 push 금지가 repo 정책이면
git add <files>
git commit -m "..."
git push -u origin HEAD
gh pr create --title "..." --body "$(cat <<'EOF'
## Summary
...

## Test plan
- [ ] ...

EOF
)"
```

- 저장소 기본 브랜치·PR 규칙은 repo `AGENTS.md` / `README.md`를 따른다.
- `gh`·`git`은 Pod 시작 시 `GH_TOKEN`으로 인증된다.

## 실패 시 (push·PR·인증)

1. **사람에게 push 요청 금지**
2. 티켓에 `add_comment`로 blocker 기록 (에러 메시지·필요 권한)
3. 플랫폼 담당자 **eric** `@mention` — `GH_TOKEN` scope·repo 접근 점검 요청
4. 추가 구현은 멈추고 피드백·재배정까지 대기

## 리뷰 후

리뷰어 피드백이 오면 `get_comments`로 읽고 수정·재push·코멘트 응답. 승인 후 merge는 리뷰어 또는 repo 정책에 따른다.
