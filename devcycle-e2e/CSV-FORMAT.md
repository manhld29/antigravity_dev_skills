# Test-case CSV format (`cases.csv`)

The single source of truth for the E2E run: it holds the **planned** cases
(phase 1) and, after a run, the **results** (phase 3). One row per scenario,
keyed by `case_id`. Lives at `tests/e2e/cases.csv`.

## Columns

| Column | Filled by | Meaning |
|--------|-----------|---------|
| `case_id` | phase 1 | Unique id, e.g. `TC-001`. Links the row to its test via `@pytest.mark.case("TC-001")`. |
| `title` | phase 1 | Short scenario name. |
| `preconditions` | phase 1 | App/data state before the steps (e.g. "App launched, logged out"). |
| `steps` | phase 1 | Ordered actions, `;`-separated: `1. enter user;2. click login`. |
| `test_data` | phase 1 | Inputs. Reference secrets as "`.env.dev` creds" — **never** put a real password here. |
| `expected_result` | phase 1 | The observable outcome to assert. |
| `status` | phase 3 | `PASS` / `FAIL` / `BLOCKED` / `SKIPPED` (empty = not run yet). |
| `actual_result` | phase 3 | What happened. On FAIL: assertion message + masked `APP_LOG_PATH` tail. |
| `screenshot` | phase 3 | Path to the captured image, e.g. `_artifacts/TC-001.png`. |
| `run_at` | phase 3 | ISO timestamp of the run. |

Phase 1 leaves the last four columns **empty**; phase 3 writes them in place,
matched by `case_id`, so re-runs overwrite the same rows.

## Example

```csv
case_id,title,preconditions,steps,test_data,expected_result,status,actual_result,screenshot,run_at
TC-001,Login valid,App launched logged out,"1. enter username;2. enter password;3. click Login",.env.dev creds,Dashboard greets the user by name,,,,
TC-002,Login wrong password,App launched logged out,"1. enter username;2. enter wrong password;3. click Login",username + bad password,Error label shown; dashboard not loaded,,,,
```

After a run, TC-001 might become:

```csv
TC-001,Login valid,...,...,...,Dashboard greets the user by name,PASS,Dashboard visible; greeting matched,_artifacts/TC-001.png,2026-06-09T14:03:11
```

## Authoring notes

- Quote any field containing a comma; the writer (`scripts/csv_results.py`) uses
  `csv.QUOTE_MINIMAL` and reads/writes UTF-8.
- Keep `steps` imperative and atomic — they are the spec the generated pywinauto
  code implements, and the human-readable record of what was tested.
- Cover negative/edge paths as their own rows (wrong input, cancel, offline).
- `actual_result` is masked for secrets by the harness; still never write a
  password into any column yourself.
