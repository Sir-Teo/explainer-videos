# Part 3 tail Chinese caption proposals

Prepared 42 new entries from 38 handed-off caption calls (55 individual component strings): 29 exact static captions and 13 finite numeric prototype templates. Existing translations for the other 13 contextual strings are retained. The shared global caption table was not edited.

Every dynamic prototype number is a translation fixture, not a measured result. This includes 95% confidence and delta 0.05. Each field has its exact source expression, numeric role, formatting and fixture value recorded in the companion JSON. Fixed mathematical quantities, number order and uniquely supported reorderings are preserved.

The actual frozen scene ASTs match all 38 handed-off call locations. Eighty-one translator checks pass: exact proposed/existing captions, numeric-slot substitution in isolation, and numeric substitution against the current global table plus proposals merged only in memory. No production data/cache loader, compute or render was invoked.

Merge input: `/workspace/runtime/ai3-tail-caption-add.json`. Detailed source hashes, all 55 components, numeric fields, checks and deferred list: `/workspace/runtime/ai3-tail-caption-proposal-handoff.json`. No dynamic nonnumeric expressions occur in this scoped inventory, so none are deferred. Nonfinite numeric outputs, any extra captions outside the 38-call handoff, and actual capture/layout validation remain pending.
