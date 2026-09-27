# jira-bugfix

Orchestrator **fix bug theo ticket Jira, test-first, end-to-end** cho ứng dụng **PySide6/Qt desktop**. Bạn đưa vào một mô tả lỗi + một Jira key; skill chạy **8 phase có gate**, mỗi phase **gọi lại một skill dev-fcd có sẵn** và mang artifact của phase trước sang phase sau — không viết lại logic của bất kỳ stage nào.

Skill này là một **driver**: nó *invoke* [jira-fetch](../jira-fetch/README.md), [devcycle-e2e](../devcycle-e2e/SKILL.md), [devcycle-debug](../devcycle-debug/SKILL.md), [devcycle-bugfix](../devcycle-bugfix/SKILL.md), [devcycle-security](../devcycle-security/SKILL.md) và [devcycle-audit](../devcycle-audit/SKILL.md). Chi tiết đầy đủ các gate và anti-pattern nằm trong [SKILL.md](./SKILL.md).

## Khi nào dùng

**Dùng** khi một bug **đã được track trên Jira** cần fix test-first end-to-end: "fix this Jira bug", "sửa bug theo ticket", "fix PROJ-123", "jira-bugfix".

**Không dùng** (`SKIP`) khi:
- Bug **không có Jira key** → dùng [devcycle-bugfix](../devcycle-bugfix/SKILL.md).
- Chỉ **chẩn đoán**, chưa fix → [devcycle-debug](../devcycle-debug/SKILL.md).
- Đây là **feature mới** → [devcycle](../devcycle/SKILL.md) / [devcycle-tdd](../devcycle-tdd/SKILL.md).
- Hỏi đáp / nghiên cứu.

## Luồng 8 phase

```
Phase 1 fetch Jira  → Phase 2 E2E reproduce (case RED) → Phase 3 PLAN (root cause)
   → Phase 4 unit/regression test (RED) → Phase 5 code minimal fix
   → Phase 6 E2E verify ──FAIL──▶ quay lại Phase 3 (re-plan trên bug còn lại)
        └─PASS─▶ Phase 7 impact + security ──Critical/High──▶ quay lại Phase 3
                     └─clean─▶ Phase 8 limitations + hướng phát triển tiếp
```

| Phase | Bước | Skill được gọi | Gate để qua phase |
|-------|------|----------------|-------------------|
| 1 Fetch | lấy Description ticket | [jira-fetch](../jira-fetch/README.md) | đọc được type/status/Description |
| 2 Reproduce | E2E mô phỏng bug | [devcycle-e2e](../devcycle-e2e/SKILL.md) | case E2E **FAIL** đúng vì bug |
| 3 Plan | tìm root cause + lên plan | [devcycle-debug](../devcycle-debug/SKILL.md) | root cause **được chứng minh** từ `APP_LOG_PATH` |
| 4 Unit test | viết test thất bại | [devcycle-bugfix](../devcycle-bugfix/SKILL.md) | test chạy **RED** đúng lý do bug |
| 5 Fix | code fix tối thiểu | [devcycle-bugfix](../devcycle-bugfix/SKILL.md) | regression test **GREEN**, suite unit xanh |
| 6 Verify | E2E đánh giá đã fix chưa | [devcycle-e2e](../devcycle-e2e/SKILL.md) | **PASS** → Phase 7; **FAIL** → Phase 3 |
| 7 Security | impact + security review | [devcycle-security](../devcycle-security/SKILL.md) | **0** Critical/High → Phase 8; có → Phase 3 |
| 8 Audit | limitation + hướng tiếp theo | [devcycle-audit](../devcycle-audit/SKILL.md) | viết `docs/audit/<jira-key>.md`, ledger sạch |

Hai **vòng lặp hội tụ** (đúng yêu cầu nghiệp vụ): E2E ở Phase 6 còn FAIL → quay về **Phase 3** re-plan; security ở Phase 7 có Critical/High → quay về **Phase 3** với một acceptance criterion mới + regression riêng.

## Nguyên tắc cốt lõi

Không fix khi chưa có đủ:
1. **Description Jira** làm nguồn chân lý cho hành vi mong đợi (Phase 1).
2. **Bug đã được tái hiện** — một case E2E FAIL đúng vì bug (Phase 2) **và** root cause được log chứng minh (Phase 3).
3. **Regression test RED trước fix, GREEN sau fix** (Phase 4 trước Phase 5).

Fix mà bỏ qua các điều trên là phỏng đoán, không có gì chặn bug âm thầm quay lại.

## Yêu cầu cấu hình trước khi chạy

| Cần gì | Cho phase nào | Ghi chú |
|--------|---------------|---------|
| [`.claude/.env`](../../.env) với `JIRA_DOMAIN` / `JIRA_API_TOKEN` | Phase 1 | xem [jira-fetch/README.md](../jira-fetch/README.md) |
| `.env.dev` ở repo gốc (`APP_LAUNCH_CMD`, `APP_WINDOW_TITLE`, `APP_USERNAME/PASSWORD`, `APP_LOG_PATH`) | Phase 2, 3, 6 | hợp đồng đầy đủ: [devcycle/ENV-FORMAT.md](../devcycle/ENV-FORMAT.md) |
| `.venv` + `pip install pywinauto pytest pytest-qt` | Phase 2–6 | E2E giả định stack **PySide6/Qt + pywinauto** trên Windows |
| `graphify-out/` (code map) | Phase 3, 7 | dùng `graphify path/query` để đánh giá impact |

> `.env.dev` và `.claude/.env` chứa credential thật → **phải** git-ignore. Skill **không bao giờ** bịa credential: thiếu `.env.dev` thì hoãn Phase E2E và ghi nhận, không tự chế. Không in `APP_PASSWORD` / token Jira.

## Cách dùng

```
/jira-bugfix "login bị treo khi sai mật khẩu PROJ-123"
/jira-bugfix "export CSV ra file rỗng FCD-456"
```

Skill tự trích Jira key trong prompt. Nếu không có key, nó sẽ hỏi — **không đoán key**.

Mỗi lượt trả lời được prefix bằng phase hiện tại, ví dụ `[Jira-fix 3 · plan]` hoặc `[Jira-fix 6 · verify→plan]`, để bạn luôn biết đang ở đâu trong luồng.

## Điều kiện hoàn thành (convergence)

Chỉ "xong" khi **tất cả** đúng: hành vi mong đợi trong Description Jira đã đạt · case E2E Phase 2 giờ **PASS** · regression test Phase 4 **GREEN** · suite unit + widget xanh · Phase 7 **không** còn Critical/High chưa xử lý · ledger `docs/debug/root-causes.md` sạch. Bất kỳ E2E FAIL hay Critical/High mới đều mở lại vòng lặp tại Phase 3.

## Artifact sinh ra

- `tests/e2e/cases.csv` + test pywinauto (Phase 2/6) — báo cáo E2E bền vững.
- Regression test trong `tests/unit/` hoặc `tests/widget/` (Phase 4).
- `docs/debug/root-causes.md` — ledger root cause (Phase 3/6/7).
- `docs/security/<date>-report.md` (Phase 7).
- `docs/audit/<jira-key>.md` — limitation + hướng phát triển tiếp (Phase 8).

## Liên quan

- [jira-fetch](../jira-fetch/README.md) — Phase 1 độc lập.
- [devcycle](../devcycle/SKILL.md) — orchestrator full lifecycle cho **feature mới** (không xuất phát từ ticket bug).
- [devcycle-bugfix](../devcycle-bugfix/SKILL.md) — vòng fix bug TDD **không cần Jira**.
