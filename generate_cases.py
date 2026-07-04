#!/usr/bin/env python3
"""generate deterministic C string-copy footgun cases"""
import json, pathlib
cases = []
def add(cid, category, fake_name, input_str, dest_cap=None, count_arg=None,
        operation="", expected="success", expected_obs="", notes=""):
    cases.append({
        "id": cid,
        "category": category,
        "fake_name": fake_name,
        "input_str": input_str,
        "input_len": len(input_str.encode()),
        "dest_capacity": dest_cap,
        "count_arg": count_arg,
        "operation": operation,
        "expected": expected,
        "expected_obs": expected_obs,
        "notes": notes
    })

# strcpy
add("c01_strcpy_ok", "strcpy_policy", "fake_name", "hello", 16, None, "strcpy", "success", "strcpy valid exact copy", "")
add("c02_strcpy_empty", "strcpy_policy", "demo_path", "", 8, None, "strcpy", "success", "strcpy empty string", "")
add("c03_strcpy_embedded_nul", "strcpy_policy", "synthetic_header", "ab\x00cd", 16, None, "strcpy", "success", "strcpy stops at first NUL", "")
add("c04_strcpy_toosmall", "strcpy_policy", "toy_buffer", "toolonginput", 5, None, "strcpy", "skip", "strcpy too-small destination not run UB", "UB not run")
add("c05_strcpy_overlap", "strcpy_policy", "example_label", "overlap", 16, None, "strcpy", "skip", "strcpy overlapping buffers not run UB", "UB not run")
add("c06_strcpy_no_nul", "strcpy_policy", "sample_field", "nonul", 16, None, "strcpy", "skip", "strcpy source-without-NUL not run UB", "UB not run")
add("c07_strcpy_retval", "strcpy_policy", "fake_config_key", "ret", 16, None, "strcpy", "success", "strcpy return-value-is-dest", "")

# strncpy
add("c08_strncpy_short_pad", "strncpy_policy", "demo_record", "hi", 16, 10, "strncpy", "success", "strncpy short source zero-padding", "")
add("c09_strncpy_exact_no_nul", "strncpy_policy", "synthetic_token", "abcd", 16, 4, "strncpy", "success", "strncpy exact-count no-terminator", "")
add("c10_strncpy_long_trunc", "strncpy_policy", "toy_message", "longertext", 16, 5, "strncpy", "success", "strncpy long source truncates-without-NUL", "")
add("c11_strncpy_zero", "strncpy_policy", "fictional_user", "xyz", 16, 0, "strncpy", "success", "strncpy count-zero", "")
add("c12_strncpy_retval", "strncpy_policy", "fake_host", "abc", 16, 8, "strncpy", "success", "strncpy return-value-is-dest-not-status", "")
add("c13_strncpy_fixed_width", "strncpy_policy", "sample_suffix", "id42", 20, 20, "strncpy", "success", "strncpy fixed-width field", "fixed_width_field_policy")
add("c14_strncpy_not_safer", "strncpy_policy", "padded_id", "toolong", 16, 4, "strncpy", "success", "strncpy not safer-strcpy", "")

# strcat / strncat
add("c15_strcat_ok", "strcat_policy", "fake_name", "world", 32, None, "strcat", "success", "strcat valid append", "")
add("c16_strcat_no_nul_dest", "strcat_policy", "demo_path", "x", 16, None, "strcat", "skip", "strcat destination-without-NUL not run UB", "UB not run")
add("c17_strcat_toosmall", "strcat_policy", "synthetic_header", "toolongappend", 8, None, "strcat", "skip", "strcat too-small destination not run UB", "UB not run")
add("c18_strncat_ok", "strncat_policy", "toy_buffer", "abc", 32, 3, "strncat", "success", "strncat valid bounded append", "")
add("c19_strncat_count_meaning", "strncat_policy", "example_label", "12345", 32, 2, "strncat", "success", "strncat count-does-not-mean-destination-size", "")
add("c20_strncat_capacity", "strncat_policy", "sample_field", "hi", 32, 5, "strncat", "success", "strncat destination-capacity-policy", "")

# snprintf
add("c21_snprintf_ok", "snprintf_policy", "fake_config_key", "val=%d", 64, None, "snprintf", "success", "snprintf valid formatting", "")
add("c22_snprintf_trunc", "snprintf_policy", "demo_record", "abcdefghij", 5, None, "snprintf", "success", "snprintf truncation-detected-by-return", "")
add("c23_snprintf_zero_size", "snprintf_policy", "synthetic_token", "test", 0, None, "snprintf", "success", "snprintf zero-size-return-only", "")
add("c24_snprintf_exact", "snprintf_policy", "toy_message", "abcd", 5, None, "snprintf", "success", "snprintf exact-fit", "")
add("c25_snprintf_unchecked", "snprintf_policy", "fictional_user", "longstring", 4, None, "snprintf", "success", "snprintf unchecked-return naive failure", "naive_fail")

# memcpy / memmove
add("c26_memcpy_known", "memcpy_policy", "fake_host", "copyme", 16, 6, "memcpy", "success", "memcpy known-length copy", "")
add("c27_memcpy_nul_explicit", "memcpy_policy", "sample_suffix", "data", 16, 4, "memcpy", "success", "memcpy explicit-NUL-after-copy", "")
add("c28_memcpy_overlap", "memcpy_policy", "padded_id", "overlapme", 16, 5, "memcpy", "skip", "memcpy overlap not run UB", "UB not run")
add("c29_memmove_overlap", "memmove_policy", "fake_name", "overlap_ok", 32, 5, "memmove", "success", "memmove overlap allowed", "")

# strlen
add("c30_strlen_ok", "strlen_policy", "demo_path", "hello", None, None, "strlen", "success", "strlen valid string length", "")
add("c31_strlen_embedded", "strlen_policy", "synthetic_header", "a\x00bc", None, None, "strlen", "success", "strlen embedded-NUL length", "")
add("c32_strlen_nonterm", "strlen_policy", "toy_buffer", "nonterm", None, None, "strlen", "skip", "strlen nonterminated not run UB", "UB not run")

# wrapper
add("c33_wrapper_success", "wrapper_policy", "example_label", "ok", 16, None, "wrapper_copy", "success", "manual wrapper copy_success", "")
add("c34_wrapper_reject_trunc", "wrapper_policy", "sample_field", "toolonginputstring", 8, None, "wrapper_copy", "error", "manual wrapper rejects_truncation", "")
add("c35_wrapper_clear_fail", "wrapper_policy", "fake_config_key", "failcase", 4, None, "wrapper_copy", "error", "manual wrapper clears_destination_on_failure", "")
add("c36_wrapper_needed_size", "wrapper_policy", "demo_record", "needs_size", 4, None, "wrapper_copy", "error", "manual wrapper reports_needed_size", "")

# policy markers
add("c37_truncation_policy", "truncation_caveat", "synthetic_token", "trunc", 4, None, "policy", "success", "truncation_policy_marker", "")
add("c38_fail_copy_policy", "truncation_caveat", "toy_message", "fail", 4, None, "policy", "success", "fail_copy_policy_marker", "")
add("c39_length_known", "memcpy_policy", "fictional_user", "lenknown", 16, 8, "policy", "success", "length_known_policy_marker", "")
add("c40_nul_term_policy", "nul_termination_caveat", "fake_host", "nulterm", 16, None, "policy", "success", "nul_termination_policy_marker", "")
add("c41_zero_pad_policy", "zero_padding_caveat", "sample_suffix", "pad", 16, 8, "policy", "success", "zero_padding_policy_marker", "")
add("c42_fixed_width_policy", "fixed_width_field_caveat", "padded_id", "fixed", 20, 20, "policy", "success", "fixed_width_field_policy_marker", "")

# portability / scope markers
add("c43_strlcpy_context", "portability_not_tested", "fake_name", "strlcpy", None, None, "strlcpy", "skip", "strlcpy_context_not_iso_c", "portability")
add("c44_strlcpy_avail", "portability_not_tested", "demo_path", "x", None, None, "strlcpy", "skip", "local_strlcpy_availability_not_required", "portability")
add("c45_annex_k", "portability_not_tested", "synthetic_header", "k", None, None, "annex_k", "skip", "Annex_K_optional_not_required", "portability")
add("c46_posix_context", "portability_not_tested", "toy_buffer", "posix", None, None, "policy", "skip", "POSIX_context_not_local_truth", "portability")
add("c47_compiler_warning", "compiler_caveat", "example_label", "warn", None, None, "policy", "success", "compiler_warning_not_safety_proof", "")
add("c48_ai_analyzer", "analyzer_caveat", "sample_field", "ai", None, None, "policy", "success", "AI_static_analysis_hallucination_marker", "")
add("c49_c_abi", "abi_caveat", "fake_config_key", "abi", None, None, "policy", "success", "C_ABI_context_marker", "")
add("c50_string_slice", "parser_design_scope", "demo_record", "slice", None, None, "policy", "skip", "string_slice_context_not_tested", "not_tested")
add("c51_unicode", "parser_design_scope", "synthetic_token", "unicode", None, None, "policy", "skip", "Unicode_locale_not_tested", "not_tested")
add("c52_prod_parser", "parser_design_scope", "toy_message", "parser", None, None, "policy", "skip", "production_parser_not_tested", "not_tested")
add("c53_safety_caveat", "safety_scope", "fictional_user", "safe", None, None, "policy", "success", "safety_caveat marker", "")

pathlib.Path("cases.json").write_text(json.dumps(cases, indent=2))
print(f"Wrote {len(cases)} cases to cases.json")
