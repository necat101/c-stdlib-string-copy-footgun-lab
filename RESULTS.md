# c-stdlib-string-copy-footgun-lab RESULTS

**Claim precision:** pass/fail/skip counts below are **compiler-backed C execution results**.

compiler_selected: zig cc
compiler_path: /tmp/zig-x86_64-linux-0.14.1/zig
compiler_version: zig 0.14.1
compile_command: /tmp/zig-x86_64-linux-0.14.1/zig cc -std=c11 -Wall -Wextra -O2 -o ./c_harness c_string_copy_footgun_harness.c
compile_ok: True
compile_elapsed: 0.1158s
harness_elapsed: 0.0053s

**C harness status: compiled and executed.**

case_count: 53
method_count: 17
pass_count: 416  # C execution passes
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
- compiled binary: 13648 bytes
- results_rows.csv / results_rows.json

## environment
- python: 3.12.3
- platform: Linux-6.17.0-1009-aws-x86_64-with-glibc2.39
- timing: time.perf_counter
- tracemalloc current: 1030592, peak: 4861290
- total_elapsed: 0.4828s
- subprocess_count: compile + run

## scope / honesty
- HN-thread-access: yes, via Hacker News API CLI, thread id 46433029, 146 comments fetched
  - committed evidence: `hn_thread_evidence.md`, `hn_comments_sanitized.txt` (~52KB), `hn_nodes_sanitized.json` (~80KB)
- network/API/package-manager during benchmark: none, except HN fetch beforehand
- undefined-behavior-not-run: yes – strcpy/strcat/strlen UB cases marked skip, not executed
- string-copy-scope: toy local lab, Python policy observers + C harness execution
- portability-not-tested: strlcpy, Annex K, POSIX – marked not_tested
- production-parser-not-tested: CLI/config/network/Unicode/locale – marked not_tested
- no libbsd, no curl source, no fuzzing, no sanitizers, no static analyzers
- no apt/sudo/root package installs, no downloaded toolchains

## conclusions

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
- naive methods assuming strncpy always NUL-terminates, ignoring snprintf return, etc., fail expected cases.
- this toy lab does NOT prove production input safety, curl correctness, libc conformance, Unicode handling, etc.
