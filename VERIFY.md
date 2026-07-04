# VERIFY.md – fresh clone verification

This documents a clean run from a fresh checkout.

**Claim precision:** pass/fail/skip counts below are **Python policy-observer results**, NOT compiler-backed C execution results. The C harness source is committed but was NOT compiler-validated in this run.

## Environment

- python: 3.12.3
- platform: Linux-6.17.0-1009-aws-x86_64-with-glibc2.39
- compiler discovery: zig cc / cc / clang / gcc – **none found in sandbox** (recorded honestly)
- date: 2026-07-04

## Transcript

```sh
$ python3 -m py_compile generate_cases.py run_lab.py
py_compile_exit=0

$ python3 generate_cases.py
Wrote 53 cases to cases.json

$ python3 run_lab.py
compiler: None None None
loaded 53 cases
skipping harness run
wrote RESULTS.md, results_rows.csv/json
{'pass_count': 416, 'fail_count': 4, 'skip_count': 481, 'naive_expected_fail_count': 4, 'case_count': 53, 'method_count': 17, 'compiler': None, 'compile_ok': False}
```

## Observations

- py_compile passes for generate_cases.py and run_lab.py
- generate_cases.py produces cases.json (53 cases, 17534 bytes)
- run_lab.py:
  - compiler discovery ran – no compiler found (zig/cc/clang/gcc all absent), compile_ok=False, recorded honestly
  - **C harness compile SKIPPED – no compiler available**
  - **C harness run SKIPPED – no compiled binary**
  - policy observers ran in Python
  - strcpy/strncpy/strcat/strncat/snprintf/memcpy/memmove/strlen observations completed via Python policy observers (NOT C execution)
  - wrapper_policy observations completed (Python)
  - UB cases correctly marked skip / not_run, never executed
  - naive_string_copy_marker failed 4 expected cases (strncpy exact_no_nul, strncpy_long_trunc, strncpy_not_safer, snprintf_unchecked) – **Python policy-observer result**
  - output: RESULTS.md, results_rows.csv, results_rows.json
  - **pass/fail/skip counts (416 / 4 / 481) are Python policy-observer results, NOT C execution results**
- No network calls during benchmark
- No real corpora, no real parser input, no UB execution
- No apt/sudo/root package installs, no downloaded toolchains
- HN thread access: yes, via Hacker News API CLI beforehand (thread 46433029, 146 comments)
  - committed evidence: `hn_thread_evidence.md`, `hn_comments_sanitized.txt` (~52KB), `hn_nodes_sanitized.json` (~80KB)

## Artifacts

- cases.json – 53 cases
- `c_string_copy_footgun_harness.c` – 2322 bytes – **source committed only, NOT compiler-validated in this no-compiler run**
- RESULTS.md – summary + compiler availability status + honest scope notes (Python policy-observer results clearly labeled)
- results_rows.csv / results_rows.json – per-case/per-method (901 rows = 53 cases × 17 methods) – **Python policy-observer results**
- `hn_thread_evidence.md` – HN thread evidence summary with comment IDs
- `hn_comments_sanitized.txt` – full HN comment text (146 comments, ~52KB)
- `hn_nodes_sanitized.json` – raw HN API nodes (~80KB)

## Compiler note

The sandbox environment used for CI/verification did NOT have zig, cc, clang, or gcc installed. This is allowed per lab scope ("if no usable compiler exists, say exactly what failed … do not claim the C harness was validated").

- **C harness compile status: NOT validated – no compiler available**
- **C harness run status: NOT executed – no compiled binary**
- **Pass/fail/skip counts are Python policy-observer results, NOT C execution results**

The C harness source (`c_string_copy_footgun_harness.c`) is committed and should compile with `-std=c11 -Wall -Wextra` on a normal system with any of: zig cc, cc, clang, or gcc. In an environment with a compiler, run_lab.py will find it in order: zig cc → cc → clang → gcc, record version + compile command, and run the harness. No apt/sudo/root installs are required or allowed per lab scope – use an environment where a compiler is already present.

To test with a compiler locally (if available):
```sh
cc -std=c11 -Wall -Wextra -O2 -o c_harness c_string_copy_footgun_harness.c
./c_harness cases.json
```

Then update RESULTS.md and VERIFY.md with the actual compiler path, version, compile command, harness output, and mark C validation as complete.

## Result

Fresh-clone tested: YES – py_compile, generate_cases.py, run_lab.py all ran end-to-end, producing RESULTS.md and per-case artifacts.

**Validation scope: Python policy observers only. C harness source committed but NOT compiler-validated (no compiler available in test environment). Claims are scoped accordingly in README.md, RESULTS.md, and VERIFY.md.**
