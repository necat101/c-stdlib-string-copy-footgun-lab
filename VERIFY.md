# VERIFY.md – fresh clone verification

This documents a clean run from a fresh checkout.

## Environment

- python: 3.12.3
- platform: Linux-6.17.0-1009-aws-x86_64-with-glibc2.39
- compiler: **zig cc 0.14.1** (`/tmp/zig-x86_64-linux-0.14.1/zig`)
  - zig cc wraps clang 19.1.7, target x86_64-unknown-linux-musl
- date: 2026-07-04

## Transcript

```sh
$ python3 -m py_compile generate_cases.py run_lab.py
py_compile_exit=0

$ python3 generate_cases.py
Wrote 53 cases to cases.json

$ python3 run_lab.py
compiler: zig cc /tmp/zig-x86_64-linux-0.14.1/zig zig 0.14.1
loaded 53 cases
compile: /tmp/zig-x86_64-linux-0.14.1/zig cc -std=c11 -Wall -Wextra -O2 -o ./c_harness c_string_copy_footgun_harness.c
compile_ok True elapsed 0.1158s
harness run elapsed 0.0053s
wrote RESULTS.md, results_rows.csv/json
{'pass_count': 416, 'fail_count': 4, 'skip_count': 481, 'naive_expected_fail_count': 4, 'case_count': 53, 'method_count': 17, 'compiler': 'zig cc', 'compile_ok': True}

$ ./c_harness cases.json
{"harness":"c_string_copy_footgun","observations":[
  {"case_id":"c01_strcpy_ok","c_harness":"ok"},
  {"case_id":"c02_strcpy_empty","c_harness":"ok"},
  ...
  {"case_id":"c53_safety_caveat","c_harness":"ok"}
]}
```

## Observations

- py_compile passes for generate_cases.py and run_lab.py
- generate_cases.py produces cases.json (53 cases)
- run_lab.py:
  - compiler discovery: **zig cc 0.14.1 found**, compile_ok=True
  - **C harness compiled successfully:** `zig cc -std=c11 -Wall -Wextra -O2 -o ./c_harness c_string_copy_footgun_harness.c`
  - **C harness executed successfully** – 53/53 cases observed, harness elapsed ~5ms
  - C harness demonstrates: strcpy, strncpy, strcat, strncat, snprintf, memcpy, memmove, strlen, and project-local `copy_result_t` wrapper – all safe calls, UB cases NOT run
  - policy observers ran (Python + C harness observations)
  - strcpy/strncpy/strcat/strncat/snprintf/memcpy/memmove/strlen observations completed
  - wrapper_policy observations completed
  - UB cases correctly marked skip / not_run, never executed
  - naive_string_copy_marker failed 4 expected cases (strncpy exact_no_nul, strncpy_long_trunc, strncpy_not_safer, snprintf_unchecked)
  - output: RESULTS.md, results_rows.csv, results_rows.json
- No network calls during benchmark
- No real corpora, no real parser input, no UB execution
- HN thread access: yes, via Hacker News API CLI (thread 46433029, 146 comments)
  - committed evidence: `hn_thread_evidence.md`, `hn_comments_sanitized.txt` (~52KB), `hn_nodes_sanitized.json` (~80KB)

## Artifacts

- cases.json – 53 cases
- `c_string_copy_footgun_harness.c` – 2322 bytes – **compiled and executed with zig cc 0.14.1**
- compiled binary `c_harness` – ~16KB (not committed, reproducible via `zig cc`)
- RESULTS.md – summary + compiler-backed validation status
- results_rows.csv / results_rows.json – per-case/per-method (901 rows = 53 cases × 17 methods)
- `hn_thread_evidence.md`, `hn_comments_sanitized.txt`, `hn_nodes_sanitized.json` – HN audit trail

## Compiler note

C harness validated with **zig cc 0.14.1** (clang 19.1.7 backend, musl target):

```sh
zig cc -std=c11 -Wall -Wextra -O2 -o c_harness c_string_copy_footgun_harness.c
./c_harness cases.json
```

All 53 cases observed by C harness. UB cases (strcpy too-small/overlap/no-NUL, strcat bad dest, memcpy overlap, strlen nonterminated) are marked skip / not_run in the case data and are never passed to the C string functions – the harness only executes safe, defined calls.

run_lab.py discovers compilers in order: zig cc → cc → clang → gcc. Zig was used here per lab preference.

## Result

Fresh-clone tested: **YES – with compiler-backed C harness validation.**

- py_compile, generate_cases.py, run_lab.py all ran end-to-end
- **C harness compiled with zig cc 0.14.1, executed successfully, 53/53 cases observed**
- RESULTS.md and per-case artifacts produced
- HN evidence committed, audit trail complete
- No UB, no network, no package manager during benchmark (zig was pre-downloaded for validation)
