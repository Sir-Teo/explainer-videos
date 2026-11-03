# Part 29: independent scientific source repair, phase 1

Base: `58619da21b11b0e9f1202bb99d0a27a6606f6ad0`.
This is a new implementation, not recovery of an earlier unavailable patch.
This source packet contains no numerical products or media. No complete Part29 numerical,
rendering, speech, publication or production acceptance is claimed.

## Changes and bounded validation

- Charge every checker reread as an actual tool call, including correct initial lookups;
  reject unfinished checks at the call budget.
- Isolate CPU Torch RNG during evaluation, snapshots and reward diagnostics. Changing their
  frequency must not alter training. Count transitions rather than initial observations.
- Preserve the Catch state corresponding to returned landing-frame pixels before resetting
  the next ball; do not change the environment transition/observation protocol.
- Detect closed-segment/disk intersections (including tangencies), stop at first contact,
  honor the exact step budget, and count only true forward centre-line crossings.
  Non-crossing trajectories belong to neither above nor below; rates use all trials.
- Declare every integer in a symmetric training-defined FAST alphabet with reserved
  headroom, not just observed training symbols. Out-of-range held-out values fail rather
  than enlarging the alphabet from test data or being silently clipped.
- Derive the warehouse display fit from retained success arrays with its original free
  intercept and selection mask. Draw amplitude times exponential decay only over measured
  horizons; distinguish effective decay from measured single-step reliability in EN/ZH.
- Compute expert-state error separately for each horizon in the imitation bound. Qualify
  quadratic worst-case and DAgger no-regret claims in English and Chinese.

`tests/test_ai29_independent_science.py` contains synthetic regression fixtures. Its only
optimizer exercise is two tiny updates per run, comparing diagnostic schedules. It does
not establish the full learning curves or any published numerical claim. Tests compile
unchanged numerical source with only the optional rendering-cache import substituted;
cache locking itself is the real implementation. Additional reader tests execute the actual
Cache JSON/NPZ loader and verify replacement detection plus rejection of metadata shadowing.

Validation on the candidate: 19 focused tests passed; 7 shared caption-input tests passed;
143/143 narration source expressions are covered by translation templates. Changed saved EN/ZH narration records match their templates and bookmark order; the new
no-regret caption and three effective-decay labels resolve through the actual shared Chinese
lookup. The measured warehouse narration is evaluated from the retained accepted product. These checks do not establish timing.
A bounded independent source reviewer rechecked cache atomicity, collision stopping and
caption completeness after corrections and found no further blocking issue in that scope.

The final open-loop diagnostic also uses separate NumPy action/environment generators and
a fixed CPU Torch fork. It no longer depends on the training RNG state at completion.

## Cache compatibility

Exactly six products require `independent-20261103-v1` recipe markers: `agent`, `lane`,
`dreamer`, `klbal`, `detour`, `fast`. Dreamer/KL partial checkpoints also carry the recipe
version, preventing resume from old stochastic protocols. Explicit producers add markers;
render readers reject legacy results instead of relabelling them. For these six products,
NPZ arrays cannot shadow any JSON field or reserved recipe/parameter metadata; validation
and loading share the same reentrant item lock. Unaffected readers retain existing merging. Existing numeric result
schemas remain except for added lane epsilon-by-horizon arrays and FAST alphabet metadata.

`belief`, `horizon`, `metr`, `world`, `symlog`, `randomize` retain valid reader paths; they are
not invalidated merely because the containing source file changed. Broad external source
fingerprints may nevertheless become stale and must be assessed separately. All scene-level
cache misses now fail closed under the cache lock rather than implicitly computing/training.

No private v2 artifact is required by an unrelated scene. There are no corrected datasets
in this source candidate. The README's historical outcomes and saved numeric narration are
not measurements of the new recipes, except the measured warehouse narration updated from
the separately approved isolated agent run. Fresh approved generation must update and reconcile
those numbers, all derived EN/ZH narration, and affected layouts.

## Scoped measured-figure visual check

The actual `Compound.measured()` method was exercised with only the separately validated
agent product; a strict provider rejected all other keys and all TTS/producer calls were
blocked. Native 1920×1080 endpoint and 24 selected frames around legend/fit reveals were
reviewed. The first attempt exposed insufficient clearance between the green legend and
last green point; raising the legend from y=1.2 to y=1.6 resolved it in the refreshed frames.
No frame clipping was found. The 2.15 calls-per-step value is verified narration text, not
an on-screen label. These are timing-only silent frames, not continuous playback or audio
synchronization evidence. Chinese rendering remains blocked by the environment's missing
compatible xeCJK; source/template checks do not substitute for Chinese rendered acceptance.

## Remaining gates

1. Independently approve bounded generation plans for affected numerical products; do not
   infer new results from historical outcomes or synthetic unit fixtures.
2. Verify METR primary snapshot precision separately; no download or precision change here.
3. Review remaining scientific qualifications, including free-KL, flow conditioning and
   FAST quantization error wording. The warehouse fit now retains its amplitude and qualified
   effective-decay interpretation. A data-backed EN measured-only native endpoint and
   selected animation frames passed scoped review after moving the legend upward to
   clear the final green point. Broader visual acceptance is still pending.
4. Native and low-resolution motion QA in both languages for all affected figures, including
   earlier reported clipping, highlight occlusion, Dreamer overlap and bookmark timing.
5. Complete playback/listening/synchronization remains unassessed. Production stays canceled.

The shared-caption delta is four additive entries: the no-regret learner qualification and
three numeric-template-compatible effective-decay labels.
Integrators must merge it by key, not replace the shared table wholesale.
