# Rejection-sampling envelope validator correction

The first actual Part5 queue completed13items and stopped on draws: its producer returns rejection heights in density units[0,M], while the new validator incorrectly required[0,1]. The repaired contract requires finitepositiveM, proposal coordinates[0,1], heights[0,M] and aligned boolean acceptance flags. A tiny fixture with height1.5/M2.5 passes; values aboveM and malformed inputs fail. This corrects units rather than relaxing an observed scientific result.

All26first-run payload files were preserved before editing. All13items were then actually regenerated under the new strict source recipe: every numeric JSON body and every NPZ byte equals its preserved baseline, and all13current checks pass. Metadata was not rewritten to pretend an old producer used the new validator. Raw old/new hashes and original runtime paths remain inspectable.

The new complete suite passes489tests in47.551seconds,exit0, at1,490identical before/after source/configuration files. This is separate from the historical488suite and later Hook appearance work. Default experiments, rendered inspection and audio approval are separate gates.
