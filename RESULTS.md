# c-stdlib-string-copy-footgun-lab RESULTS

**Claim precision:** pass/fail/skip counts below are **Python policy-observer results, NOT compiler-backed C execution results**. The C harness source (`c_string_copy_footgun_harness.c`) is committed but was **NOT compiler-validated** in this run – no compiler was available in the sandbox environment.

compiler_selected: None (no compiler found – zig cc / cc / clang / gcc all absent)
compiler_path: None
compiler_version: None
compile_command: None
compile_ok: False
compile_elapsed: 0.0000s
harness_elapsed: 0.0000s

**C harness status: source committed, NOT compiler-validated – no compiler was available.**

**Do NOT claim C API observations executed.**

case_count: 53
method_count: 17
pass_count: 416  # Python policy-observer passes
fail_count: 4    # naive method expected failures
skip_count: 481
naive_expected_fail_count: 4

## counts by method
- preserve_original_case_baseline: 53
- compiler_discovery_checker: 53
- c_harness_compile_checker: 53
- strcpy_policy_observer: 53
- strncpy_policy_observer: 53
- strcat_strncat_policy_observer: 53
- snprintf_policy_observer: 53
- memcpy_memmove_policy_observer: 53
- strlen_policy_observer: 53
- wrapper_policy_marker: 53
- strlcpy_portability_marker: 53
- annex_k_portability_marker: 53
- parser_design_scope_marker: 53
- safety_scope_marker: 53
- copy_size_timing_marker: 53
- naive_string_copy_marker: 49
- external_truth_not_tested_marker: 53

## artifacts
- cases.json: 17534 bytes
- c_string_copy_footgun_harness.c: 2322 bytes
- compiled binary: 0 bytes
- results_rows.csv / results_rows.json

## environment
- python: 3.12.3
- platform: Linux-6.17.0-1009-aws-x86_64-with-glibc2.39
- timing: time.perf_counter
- tracemalloc current: 1009610, peak: 4841417
- total_elapsed: 0.2003s
- subprocess_count: compiler discovery only (no compiler found)

## scope / honesty
- HN-thread-access: yes, via Hacker News API CLI, thread id 46433029, 146 comments fetched
  - committed evidence: `hn_thread_evidence.md`, `hn_comments_sanitized.txt` (~52KB), `hn_nodes_sanitized.json` (~80KB)
- network/API/package-manager during benchmark: none, except HN fetch beforehand
- undefined-behavior-not-run: yes – strcpy/strcat/strlen UB cases marked skip, not executed
- string-copy-scope: toy local lab, Python policy observers + C harness source (NOT compiler-validated in this no-compiler run)
- **C harness compile/run status: NOT validated – no compiler available (zig cc / cc / clang / gcc all absent). Source is committed at `c_string_copy_footgun_harness.c`.**
- **pass/fail/skip counts: Python policy-observer results only, NOT C execution results**
- portability-not-tested: strlcpy, Annex K, POSIX – marked not_tested
- production-parser-not-tested: CLI/config/network/Unicode/locale – marked not_tested
- no libbsd, no curl source, no fuzzing, no sanitizers, no static analyzers
- no apt/sudo/root package installs, no downloaded toolchains

## conclusions

All conclusions below are derived from **Python policy-observer results and HN thread sentiment analysis**, NOT from compiler-backed C execution (no compiler was available in the test environment).

- strcpy is locally safe only after external size checks; checks can drift from the call site over time (HN sentiment).
- strncpy is NOT a safer strcpy; it can produce unterminated output, or zero-padded fixed-width fields (original PDP/V7 file-name use).
- snprintf is useful for bounded writes but return value MUST be checked for truncation.
- memcpy is appropriate only when length and capacity are already known; NOT string-aware.
- memmove allows overlap, memcpy does not.
- strlen requires a valid NUL-terminated string.
- truncation vs fail-the-copy is a project policy choice, not automatic safety.
- strlcpy came up in HN discussion, is now POSIX, but is NOT ISO C – not required locally.
- Annex K strcpy_s/strncpy_s are optional – do NOT assume availability.
- compiler warnings and banned-function lists do NOT prove string safety.
- AI/static-analysis hallucinated vulnerability reports were a major HN thread theme (curl context).
- C ABI / interop keeps NUL-terminated strings entrenched.
- length-carrying strings / slices came up as the real fix, out of scope for C stdlib.
- naive methods assuming strncpy always NUL-terminates, ignoring snprintf return, etc., fail expected cases (4 expected failures in Python policy observer).
- this toy lab does NOT prove production input safety, curl correctness, libc conformance, Unicode handling, etc.
- **C harness source is committed but was NOT compiler-validated in this run – claims about C API behavior are based on ISO C documentation and HN thread discussion, validated via Python policy observers only.**
