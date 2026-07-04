# c-stdlib-string-copy-footgun-lab

Toy local correctness lab about C string-copying APIs, driven by a real Hacker News thread.

HN thread: https://news.ycombinator.com/item?id=46433029 — "No strcpy either" (curl removing strcpy)

## Hacker News thread access

The Hacker News thread was read using the Hacker News API CLI (`hackernews` skill, Firebase API) **before writing this README**. 146 comments were fetched (thread id 46433029).

Committed evidence artifacts:
- `hn_thread_evidence.md` – auditable summary with comment IDs and sentiment themes
- `hn_comments_sanitized.txt` – full comment text dump (146 comments, HTML stripped, ~52KB)
- `hn_nodes_sanitized.json` – raw HN API node data (~80KB)

This README reflects actual HN discussion themes, not just the linked blog post. Do NOT treat the linked article or cppreference docs alone as sufficient – the HN thread is the primary sentiment source.

## What HN users were actually debating

Summary of sentiments from the HN thread (paraphrased, not direct quotes unless marked):

- **strcpy is only locally safe when the caller has already proved the destination is large enough.** Multiple commenters agreed with the curl blog post's core point: strcpy itself isn't evil, but the size check being separate from the call site means those checks can drift away over time through refactoring. Enforcing checks "close to code" came up repeatedly.
- **strncpy is NOT a safer strcpy.** This was a dominant theme. strncpy was originally created for non-NUL-terminated fixed-width file-name fields (PDP/V7 directory entries, 14-byte arrays, zero-padded, NUL-terminated only if space permitted). It produces null-padded fixed-width character sequences rather than reliably NUL-terminated strings. If the source is >= count, the result is NOT NUL-terminated. Static analyzers recommending strncpy instead of strcpy was called out as the real problem starting point.
- **strlcpy came up frequently, with mixed sentiment.** Some commenters suggested strlcpy as the safer solution. Others criticized it for truncation semantics – "it is almost never desirable to truncate a string passed into strXcpy", and strlcpy "still has problems", "doesn't actually solve the real problem". strlcpy is a BSD-ism, now in POSIX (Issue 8), but NOT ISO C. Several commenters said "just vendor it, it's tiny" – others pointed out truncation policy is still the core issue.
- **snprintf as a truncating / formatting alternative.** Commenters suggested replacing strncpy calls with snprintf for NUL-terminated truncation cases. But return-value checking came up – you MUST check snprintf's return to detect truncation.
- **memcpy when length and capacity are already known.** Once you've validated sizes, strcpy's NUL-scanning is wasteful – just use memcpy. Multiple commenters noted that on modern CPUs, strcpy's byte-by-byte NUL scan with data-dependent branches is bad for performance; strlen + memcpy is often faster. "You start off with some atomics and build up from there."
- **"just use memcpy" is not enough context.** You need the source length and destination capacity first. That's the whole problem strcpy was trying to paper over.
- **truncation versus fail-the-copy came up as a policy choice.** The curl wrapper discussed in the article truncates to empty string (dest[0] = '\0') and returns void. HN commenters objected: "I'm really not sold on that being the best way … I'd think that's an error case that should be signaled with a non-zero return, leaving the destination buffer alone." Truncation is a policy choice, not automatic safety.
- **project-local wrappers came up repeatedly.** Many commenters said they write their own copy function – "it's not a novel concept". Wrapper APIs that take dst, dst_size, src, src_len and return success/failure were discussed. Return-value design (success/fail? bytes written? needed_size?) was bikeshedded.
- **Annex K strcpy_s / strncpy_s came up but should not be assumed available.** Optional Annex K, not portable. Marked as portability context only in this lab.
- **null-terminated strings versus length-carrying strings.** Strong sentiment that C's NUL-terminated string design was a mistake born from "every byte was precious" era. Multiple commenters argued for ptr+size / string slices. "as you ponder the situation you inevitably come to the conclusion that it would have been better if strings brought along their own length parameter … and you've just re-invented slices." C ABI constraints keep NUL-terminated strings entrenched for FFI.
- **C ABI and interop came up.** "Given that the C ABI is basically the standard for how arbitrary languages interact … arguably it can come up when any two languages interact at all, even if neither are C." An agreed ABI for slices would help cross-language FFI.
- **fixed-width padded fields and old file formats came up.** strncpy's original purpose – fixed-size struct fields, on-disk formats, username[20] with NUL padding. Still visible in old file formats.
- **compiler warnings and banned-function lists came up.** `-Wstringop-truncation` was mentioned. But warnings do NOT prove safety.
- **AI / static-analysis hallucinated vulnerability reports came up heavily.** The curl article's closing point – "strcpy in source code is like a honey pot for generating hallucinated vulnerability claims" – was a major thread theme. Commenters debated AI-powered analyzers (ZeroPath, Aisle Research) sending bug reports to curl, some real, some bogus. "Why even bother to run AI checking on C code if the AI flags strcpy() as a problem without caveat?" / "people overestimate AI". The initial HackerOne report that started curl's strcpy removal was noted as actually being right (commenter linked https://hackerone.com/reports/2298307).
- **C versus the C standard library came up.** Multiple commenters distinguished "C the language" from "C standard library string ergonomics". "I find C elegant and I think 90% of my errors are in string handling so therefore if it had a decent string handling library it would be enormously better."
- **"this call is locally safe" vs "this API is generally hard to misuse".** Core tension in the thread. strcpy CAN be safe in a specific call site with proven bounds, but the API makes it easy to misuse later when code evolves.

The thread also touched on: performance of strcpy vs memcpy on modern CPUs, rep movs / rep scasb, strlen-then-memcpy pattern, stpcpy, C2y/C29 string library proposals (n3306), Rust slices / borrow checker preventing overlap footguns, Zig strings as sized byte slices, valgrind/sanitizers, far pointers / memory protection history, and why better string libraries haven't made it into ISO C yet ("the committee is not organizationally set up for major library overhauls").

## Lab scope

This is a **toy local correctness lab, NOT** a production string library, libc conformance suite, curl reproduction, OpenBSD/POSIX strlcpy test, CLI/config/network parser, fuzzing target, sanitizer lab, or static analyzer.

- Deterministic synthetic byte strings only, fake labels like fake_name, demo_path, synthetic_header, etc.
- No real files, credentials, command-line arguments, protocol inputs, downloaded corpora, or external parsers.
- No apt/sudo/root, no Docker, no external C libraries, no libbsd, no OpenBSD/glibc source, no curl source, no build systems (cmake/make/meson/ninja), no Rust/Go/node, no fuzzers, no sanitizers, no static analyzers.
- Python stdlib only for orchestration.
- **C harness source is committed** (`c_string_copy_footgun_harness.c`), demonstrating strcpy/strncpy/strcat/strncat/snprintf/memcpy/memmove/strlen + project-local `copy_result_t` wrapper. **In the recorded no-compiler sandbox run, the harness was NOT compiled or executed** – see `RESULTS.md` / `VERIFY.md` for honest compiler availability reporting.
- When a compiler IS available, `run_lab.py` discovers it in order: zig cc, cc, clang, gcc – records compiler path, version, compile command, and harness run output.
- UB cases (strcpy too-small dest, overlap, nonterminated source; strcat bad dest; memcpy overlap; strlen nonterminated) are **marked skip / not_run, never executed**.

The point: test the HN debate in a tiny reproducible way – strcpy local safety vs API misuse risk, strncpy NOT being safer strcpy, snprintf return-value checking, memcpy length-known prerequisite, memmove overlap semantics, truncation as policy choice, wrapper API design, and clear boundaries between HN discussion, ISO C, POSIX/BSD, Annex K, and local libc observations.

**Claim precision:** the 416 pass / 4 expected naive fail / 481 skip counts in `RESULTS.md` are **Python policy-observer results**, not compiler-backed C execution results. The C harness source is committed but was not compiler-validated in the no-compiler sandbox run recorded in `RESULTS.md` / `VERIFY.md`.

## Running

```bash
python3 -m py_compile generate_cases.py run_lab.py
python3 generate_cases.py   # writes cases.json, 53 cases
python3 run_lab.py          # compiler discovery → harness compile (if compiler found) → policy observations → RESULTS.md
```

If no compiler is found, `run_lab.py` records that honestly (`compile_ok: false`) and continues with Python-side policy observations. **Do NOT claim the C harness was validated if compilation did not occur.** See `RESULTS.md` and `VERIFY.md` for the recorded compiler availability status.

## Repository layout

- `generate_cases.py` – deterministic fake C string-copy cases (53 cases)
- `run_lab.py` – compiler discovery, harness compile/run (if compiler available), policy observers, writes RESULTS.md + results_rows.csv/json
- `c_string_copy_footgun_harness.c` – C harness source demonstrating strcpy/strncpy/strcat/strncat/snprintf/memcpy/memmove/strlen + project-local `copy_result_t` wrapper. **Committed as source only; not compiler-validated in the no-compiler sandbox run recorded in RESULTS.md/VERIFY.md.**
- `cases.json` – generated
- `RESULTS.md` – summary tables, skip matrix, compiler availability status, honest conclusions. **Pass/fail counts are Python policy-observer results, not C execution results.**
- `results_rows.csv` / `results_rows.json` – per-case/per-method artifact
- `hn_thread_evidence.md` – HN thread evidence summary with comment IDs
- `hn_comments_sanitized.txt` – full HN comment text dump (146 comments, ~52KB)
- `hn_nodes_sanitized.json` – raw HN API node data (~80KB)
- `VERIFY.md` – fresh-clone verification transcript with compiler availability status

## Case coverage (53 cases)

strcpy valid, empty, embedded NUL, too-small (UB not run), overlap (UB not run), no-NUL source (UB not run), return-value-is-dest; strncpy short zero-pad, exact-count no-terminator, long trunc no-NUL, count-zero, retval-is-dest-not-status, fixed-width field, not-safer-strcpy; strcat valid, dest-no-NUL (UB not run), too-small (UB not run); strncat valid, count≠dest_size, capacity-policy; snprintf valid, truncation-detected, zero-size, exact-fit, unchecked-return naive fail; memcpy known-len, explicit-NUL, overlap (UB not run); memmove overlap allowed; strlen valid, embedded-NUL, nonterminated (UB not run); wrapper copy_success, rejects_truncation, clears_destination_on_failure, reports_needed_size; truncation_policy, fail_copy_policy, length_known_policy, nul_termination_policy, zero_padding_policy, fixed_width_field_policy; strlcpy_context_not_iso_c, local_strlcpy_availability_not_required, Annex_K_optional_not_required, POSIX_context_not_local_truth, compiler_warning_not_safety_proof, AI_static_analysis_hallucination_marker, C_ABI_context_marker, string_slice_context_not_tested, Unicode_locale_not_tested, production_parser_not_tested, safety_caveat.

## Methods compared

preserve_original_case_baseline, compiler_discovery_checker, c_harness_compile_checker, strcpy_policy_observer, strncpy_policy_observer, strcat_strncat_policy_observer, snprintf_policy_observer, memcpy_memmove_policy_observer, strlen_policy_observer, wrapper_policy_marker, strlcpy_portability_marker, annex_k_portability_marker, parser_design_scope_marker, safety_scope_marker, copy_size_timing_marker, naive_string_copy_marker, external_truth_not_tested_marker.

Naive method intentionally assumes strncpy always NUL-terminates, ignores snprintf return, assumes truncation is always OK, assumes memcpy is string-aware, assumes strlen is safe on every char array, assumes strlcpy is ISO C, assumes compiler warnings prove safety – and fails expected cases.

## What this lab does NOT prove

- Does NOT prove production input safety
- Does NOT prove curl's wrapper is correct
- Does NOT prove POSIX strlcpy behavior locally
- Does NOT prove libc conformance
- Does NOT prove Unicode / locale behavior
- Does NOT prove strncpy is always unsafe (it's correct for fixed-width padded fields – that's its original purpose)
- Does NOT prove any wrapper is production-ready
- Does NOT test real CLI/config/network parsing
- Does NOT test sanitizers, fuzzers, static analyzers, AI scanners

Safe claims distinguish: HN commenter sentiments vs linked article claims vs ISO C guarantees vs POSIX/BSD APIs vs local libc behavior vs toy lab observations.

---

License: public domain / CC0 – toy lab.
