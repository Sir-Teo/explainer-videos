# Part 29: scoped Belief visual follow-up

This independent layout/timing correction does not recover the old handoff.
The reviewed public base is `bf7efa5d54687f3a45094dc968f69c707664a3a9`.
The worker's local review base `dae11926e3cb6b5e3e2c6978066c0d5b4dea28ec`
has the identical tree; it is not itself claimed to be a published commit.

Actual pre-fix English frames showed the observation label crossing the POMDP
card and the action label crossing its arrow. Both labels now sit inside the
loop. Their text and arrows are unchanged.

In the corridor's fast section, negative observations were invisible and
positive observations faded in only to be immediately removed. Every fast step
now shows its actual door/no-door cue at full opacity during the compressed
update, followed by a short full-opacity hold. The numerical arrays, update
order, posterior, entropy and robot positions are unchanged. Target timing is
0.24 seconds of animation plus 0.16 seconds of hold per fast step (rendered
frame quantization applies), rather than a 0.32-second fade-only cue. Existing
English/Chinese door/no-door translations are reused; narration is unchanged.

Validation scope is `Belief.define()` and `Belief.corridor()` only, using one
fresh, independently checked belief product: seed 2005, 40 cells, 40 steps, doors
3/8/19/33, motion probability 0.8, hit probability 0.9, false positive 0.05.
The private product is not included in source. No re-computation, implicit
cache generation, other numerical products or TTS is allowed in these excerpts.

The initial cold-TeX preparation reached its original 10-minute cap; a single
explicitly authorized cumulative 30-minute pre-fix budget permitted a warm-cache
continuation, without resetting the original deadline. Completed content-addressed
TeX glyph pairs were retained; native image evidence was never substituted.
Host memory and disk reserves were guarded. Cgroup memory was not measurable
in this sandbox, and no cgroup-reserve claim is made.

Synthetic unit fixtures check cue sequencing, both sensor outcomes and label
placement contracts; they are not scientific or rendered acceptance data.
Native endpoints and selected transition frames establish only scoped English
visual QA. Chinese rendering, audio/listening, continuous playback and all other
Belief/Part 29 methods remain outside this acceptance.
