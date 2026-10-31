# Part2 English head endpoint review

**All160 endpoint frames across8scenes were actually viewed**, with11native854×480 followups. No additional definite clipping or persistent collision was found in these endpoints. This is not full playback QA.

| Scene | Endpoint frames viewed | Native followups |
|---|---:|---:|
| Hook | 15 | 1 |
| Turing | 21 | 2 |
| Search | 17 | 0 |
| AStar | 23 | 0 |
| Heuristics | 17 | 1 |
| Local | 24 | 3 |
| Games | 18 | 2 |
| Samuel | 25 | 2 |

## Actual observations

- **Hook:** Forecast/date comparison; historical timeline; topical bridges;31-part series roadmap and objectives viewed. Roadmap text small/dim at480p; native overview inspected, final-resolution/mobile readability untested.
- **Turing:** Incrementer/tape/rules, diagonal argument, busy-beaver illustrations, imitation-game diagram, Dartmouth/LogicTheorist/symbol-system endpoints viewed. Native diagonal proof and final historical context fit.
- **Search:** 8-puzzle successor/goal layouts, BFS depth histogram and hardest positions, BFS/DFS/iterative-deepening trees, Dijkstra map/path/region endpoints viewed.
- **AStar:** f=g+h, expanded regions/routes and cost captions, admissibility proof, consistency triangle and ladder, batch bars/work-cost captions viewed. Rendered247A*count matches new schema1grid cache.
- **Heuristics:** Relaxed-tile arrows, misplaced/Manhattan equations, dominance plots/EBF/tie caveat, censored15-puzzle plot, disjoint PDB tables and learned heuristic endpoints viewed. Native censor/unknown note and plot fit.
- **Local:** Hill/climbing markers, queen replay endpoints, Metropolis/detailed-balance derivation, annealing tour/curve snapshots, matched-budget comparison and GA/crossover/history endpoints viewed. Native derivation,bar chart note and final cards fit.
- **Games:** Minimax rules/counts, alpha-beta tree/window/cutoff bounds, best-case derivation and measured expansion plots viewed. Native root6 and cutoff≤/≥ labels fit, along with final plot/caption.
- **Samuel:** Historical evaluation, self-play/temporal target/modern-rule qualifier, weight and score plots, three-run verdicts and solved-position accuracy, DeepBlue/Chinook history endpoints viewed. Native score chart and verdict fit.

## Chinese Samuel failure

The original XeLaTeX failure is caused by the shared translated modern-rule caption containing `\（` (backslash immediately before the Chinese opening parenthesis). XeLaTeX reads that as an undefined control sequence at line25 of `af0f2434796b97c6.tex`. Root owns the shared caption table and has inserted a space after that backslash. The current table contains the safe separator. No Samuel-specific production source change is required; root owns rerender confirmation.

AStar’s247-cell count is correct: regenerated schema1grid JSON contains `astar_n=247`, `dijkstra_n=2633`, priority `f,-g,node`. The scene derives its count from that field. Root’s current table contains the exact `$247$ cells{,} \ the same optimal cost` translation. The old239entry is unused. Heuristics/Local warnings concern comma-escaped caption keys which root has also materialized. These edits do not establish successful rerendering by themselves.

## Evidence and limits

Complete frame times/reasons/text geometry, all160frame hashes,8sheet hashes, render-result hashes, worker fingerprints/input signatures, failed Samuel TeX/log hashes and current repaired caption are preserved in [ai2-en-head-endpoint-review.json](ai2-en-head-endpoint-review.json.gz).

- Endpoint frames are not full playback; intervening transitions/pacing/motion remain unreviewed.
- No audio/listening/narrated synchronization or final1080p/player/responsive validation in this task.
- No ZH endpoint visual inspection in this task; only failed Samuel TeX source/log and current repaired shared caption examined.
- Recorded QA statuses/warnings describe the original worker results; visual review does not convert them to full playback or production approval.
- Hashes captured at review report completion; parent owns subsequent rerenders and shared caption edits.

No source edits, data computations or renders were performed. No access blockers or denied operations.
