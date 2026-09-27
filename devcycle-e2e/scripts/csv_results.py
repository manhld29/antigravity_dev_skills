"""Read/scaffold the E2E test-case CSV and write run results back into it.

Used by tests/e2e/conftest.py (to record results) and as a CLI (to scaffold or
validate cases.csv, or print a summary). Results are matched to planned rows by
`case_id`, so re-runs overwrite the same rows in place.

CLI:
    python csv_results.py --scaffold tests/e2e/cases.csv   # create with header
    python csv_results.py --check    tests/e2e/cases.csv   # validate columns
    python csv_results.py --summary  tests/e2e/cases.csv   # pass/fail counts
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

COLUMNS = [
    "case_id",
    "title",
    "preconditions",
    "steps",
    "test_data",
    "expected_result",
    "status",
    "actual_result",
    "screenshot",
    "run_at",
]
RESULT_COLUMNS = {"status", "actual_result", "screenshot", "run_at"}


def scaffold(path: Path) -> None:
    """Create the CSV with just the header if it doesn't exist."""
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerow(COLUMNS)


def load_cases(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def check(path: Path) -> list[str]:
    """Return a list of problems; empty list means valid."""
    problems: list[str] = []
    if not path.is_file():
        return [f"{path} not found"]
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        header = reader.fieldnames or []
        missing = [c for c in COLUMNS if c not in header]
        if missing:
            problems.append(f"missing columns: {', '.join(missing)}")
        ids: set[str] = set()
        for i, row in enumerate(reader, start=2):
            cid = (row.get("case_id") or "").strip()
            if not cid:
                problems.append(f"row {i}: empty case_id")
            elif cid in ids:
                problems.append(f"row {i}: duplicate case_id {cid}")
            else:
                ids.add(cid)
    return problems


def write_result(
    path: Path,
    case_id: str,
    status: str,
    actual_result: str = "",
    screenshot: str = "",
    run_at: str = "",
) -> bool:
    """Update the row for `case_id` with run results, in place. Returns True if
    a matching row was found and written."""
    if not path.is_file():
        return False
    rows = load_cases(path)
    found = False
    for row in rows:
        if (row.get("case_id") or "").strip() == case_id:
            row["status"] = status
            row["actual_result"] = _clip(actual_result)
            row["screenshot"] = screenshot
            row["run_at"] = run_at
            # ensure all expected columns exist on the row
            for col in COLUMNS:
                row.setdefault(col, "")
            found = True
            break
    if not found:
        return False
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    return True


def summary(path: Path) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in load_cases(path):
        key = (row.get("status") or "NOT_RUN").strip() or "NOT_RUN"
        counts[key] = counts.get(key, 0) + 1
    return counts


def _clip(text: str, limit: int = 4000) -> str:
    """Keep CSV cells sane; actual_result can carry a log tail."""
    text = (text or "").strip()
    return text if len(text) <= limit else text[: limit - 3] + "..."


def main() -> int:
    ap = argparse.ArgumentParser(description="devcycle E2E cases.csv helper")
    ap.add_argument("--scaffold", metavar="CSV", help="create CSV with header if missing")
    ap.add_argument("--check", metavar="CSV", help="validate columns and case_ids")
    ap.add_argument("--summary", metavar="CSV", help="print status counts")
    args = ap.parse_args()
    if args.scaffold:
        scaffold(Path(args.scaffold))
        print(f"OK: {args.scaffold} ready")
        return 0
    if args.check:
        problems = check(Path(args.check))
        if problems:
            print("INVALID:")
            for p in problems:
                print(f"  - {p}")
            return 1
        print("OK: cases.csv valid")
        return 0
    if args.summary:
        for status, n in sorted(summary(Path(args.summary)).items()):
            print(f"{status}: {n}")
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
