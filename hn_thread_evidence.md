# HN thread evidence – c-stdlib-string-copy-footgun-lab

Thread: "No strcpy either"
URL: https://news.ycombinator.com/item?id=46433029
Article: https://daniel.haxx.se/blog/2025/12/29/no-strcpy-either/
Fetched: 2026-07-04 via Hacker News API CLI (Firebase)
Tool: `hackernews` skill – `python3 ./hackernews get-item --id 46433029`

- Story score: 265
- Descendants: 145
- Comments fetched: 146

## Key comment IDs (for audit)

- 46434944 (Tharre) – strcpy performance footgun on modern CPUs, NUL scan branch prediction
- 46433746 (t43562) – every C string routine has huge caveats, need ptr+size library
- 46435007 (ahoka) – "strncpy() is a weird function with a crappy API", originally for non null-terminated strings, static analyzers recommending strncpy over strcpy was the real problem, real alternative was snprintf, now strlcpy
- 46433731 (loeg) – Annex-K like API discussion, destination buffer size includes NUL but source size doesn't
- 46433512 (Scubabear68) – strcpy as honey pot for hallucinated AI vulnerability claims
- 46434787 (zahlman) – curl wrapper critique: truncates to empty string, returns void, should signal error with non-zero return instead
- 46442629 (rf15) – off-by-one buffer size vs string length ergonomics
- 46433360 (snvzz) – AI chatbot vulnerability reports
- 46448927 (juliangmp) – string handling despised, ptr+size type missing from C, snprintf replaces strncpy for trimming+null-termination, enable -Wstringop-truncation
- 46435289 (amelius) – move away from null-terminated strings
- 46435816 (Someone) – strncpy invented for 14-byte file names, zero terminated only if space permitted
- 46433866 (formerly_proven) – strncpy is for fixed-width strings / on-disk formats, char username[20] with NUL padding, links https://man.archlinux.org/man/string_copying.7.en
- 46433973 (kccqzy) – long analysis: strlcpy tries to improve but still has problems, truncation is almost never desirable, strncpy got truncation behavior needing to tell programmer where data was truncated, strlcpy adopted same behavior as drop-in replacement, "dumb idea from the start", strcpy has best interface but only safe after external verification, then you can just use memcpy, strings should carry length – re-invented slices, C committee string library proposal n3306, C2y expected C29
- strlcpy POSIX discussion: comment 46435377 – "strlcpy is in POSIX now" with link https://pubs.opengroup.org/onlinepubs/9799919799/functions/strlcpy.html
- AI analyzer discussion: multiple comments, 46433584 links https://daniel.haxx.se/blog/2025/12/23/a-curl-2025-review/ – "A new breed of AI-powered high quality code analyzers, primarily ZeroPath and Aisle Research"
- C ABI discussion: 46435377 – "Given that the C ABI is basically the standard for how arbitrary languages interact"
- Rust/Zig string discussion: 46442588 – Rust safe subset eliminates UB, borrow checker prevents overlap footguns, Zig strings as sized byte slices

## Sentiment themes extracted (used in README)

1. strcpy locally safe only after external size checks; checks drift from call site
2. strncpy NOT safer strcpy; null-padded fixed-width fields; unterminated output
3. strlcpy suggested but criticized for truncation semantics; BSD/POSIX not ISO C
4. snprintf as truncating alternative, must check return value
5. memcpy when length/capacity known; "just use memcpy" needs context
6. memmove vs memcpy overlap policy
7. truncation vs fail-the-copy = policy choice
8. project-local wrappers common
9. Annex K optional, do not assume
10. NUL-terminated vs length-carrying strings / slices
11. C ABI / interop constraints
12. fixed-width padded fields / old file formats
13. compiler warnings / banned-function lists ≠ safety proof
14. AI / static-analysis hallucinated vulnerability reports
15. C vs C standard library ergonomics
16. "locally safe call" ≠ "API hard to misuse"

Full comment dump saved at build time: `/tmp/hn_comments.txt` (146 comments, ~full text, HTML stripped).

This file exists to make the HN-thread-reading step auditable. The README sentiment summary is derived from the above API-fetched comments, not from web search or the linked article alone.
