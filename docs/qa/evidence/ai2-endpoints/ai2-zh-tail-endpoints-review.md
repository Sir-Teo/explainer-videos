# Part2 Chinese tail endpoint review

Status: in-progress. Updated 2026-10-31T16:12:35.137178+00:00.

Endpoint stills only. Continuous playback/listening remains unverified.

| Scene | Reviewed frames | Actual native-tile sheets | Render status |
|---|---:|---:|---|
| Logic | 21 | 6 | needs-review |
| Plans | 24 | 6 | needs-review |
| SAT | 14 | 4 | failed |
| Knowledge | 21 | 6 | needs-review |
| Eliza | 13 | 4 | passed |
| Winters | 22 | 6 | needs-review |

Logic crossing-edge defect repaired in shared source; two English repaired proof endpoints visually clear. Chinese repaired proof endpoints also visually clear; motion review is separate. Baseline Plans panel is undersized; parent enlarged-panel rerender pending. SAT baseline failed after14recorded endpoints; reviewed coverage is partial.

Pending scenes: Survives, Outro.

All frame/page hashes,times,observations and source warnings are preserved in companion JSON.

## Logic

- Page 001, endpoints 0–3, 1.000000–28.864307s: Chinese chapter title/timeline, three-box inference diagram, premises and truth-table endpoint remain separated; highlighted satisfying rows align. SHA256 `b7a0c07068cd70bf3b2dc80fd6a9b81856ae33beed920f9cd823fc0a5c048f0a`.
- Page 002, endpoints 4–7, 34.806266–74.152162s: Truth-table conclusion/footer and first-order formula/history cards fit; historical cards retain separate borders and readable Chinese labels. SHA256 `db04e7158a3a987e6617cff38ceb1282c1030759ea6e78b6050969462f080582`.
- Page 003, endpoints 8–11, 84.337167–111.166597s: Resolution formula, boxed clauses, negated goal and empty-clause explanation fit without overlap; footer remains within frame. SHA256 `962fb66341f9b165ead8bc44405be35e28dffc234dc7f4db94be299e64d5c294`.
- Page 004, endpoints 12–15, 121.419950–161.559126s: Propositional proof edges connect boxed clauses to empty clause; completeness/factoring note is separate. First-order clause/substitution diagram fits screen width. SHA256 `ee809b0659db742d2219726d552f52e0d70036d2a833aa1717d410d7b0eb3e80`.
- Page 005, endpoints 16–19, 179.131700–216.531420s: First-order derivation, Prolog card and strategy comparison endpoints fit. Capped all-pairs run is explicitly distinguished from found proof. SHA256 `a84800adefb8baadd4284548e2860e49d4745bc2b507e6c7e5f99b58242f21d5`.
- Page 006, endpoints 20–20, 232.715015–232.715015s: Final strategy caption and both4000/2823bars remain within frame; no clipping. SHA256 `f1262f205fdc034b04d6a51e32ff5dcdd851a4d897be3506ede69bb354cbdf6b`.

## Plans

- Page 001, endpoints 0–3, 1.000000–18.747926s: Chinese title, Sudoku grid, clue/solution tag and CSP definition card fit; explanatory text remains separate. SHA256 `2411fb306ef5b59b0e7b2be1d98d628c4c5a249aab11870a86f65cd366deb44a`.
- Page 002, endpoints 4–7, 26.558004–65.509560s: History cards, full candidate grid and AC-3 deletion rule/counter fit; candidate digits remain contained within cells. SHA256 `e53418d77c52de78738064cfb427bbb5d64f1b387615f40b63e58b2a01ed8a16`.
- Page 003, endpoints 8–11, 74.880460–109.743682s: AC-3 search comparison bars have distinct labels/values; STRIPS facts/action lists and history card remain in separate columns. SHA256 `15a74659fc1bc8bf450e8957b08931e0e5788c5ba626776147c4e0515357c395`.
- Page 004, endpoints 12–15, 122.510390–154.101455s: STRIPS state/action/history/frame-problem panels have clear gaps; start/goal stacks stay labeled. SHA256 `86046e5fecdbff0c021956b7d001ed233ede1118eac4772fa769bb17f4c771e0`.
- Page 005, endpoints 16–19, 159.645355–190.234833s: Sussman subgoal action lists and six-step plan stay separate; historical card remains within frame. Planner coverage panel appears very small at native preview. SHA256 `d3046fc01f1203e8a140f7552715b7dd100c58a100c010c61ae01f700b55e839`.
- Page 006, endpoints 20–23, 193.739863–230.488675s: Planner plot/table/legend and matched-plan text fit; original coverage panel text is undersized and awaits the parent's enlarged-panel rerender. SHA256 `51dd7af8f2d0b4a87e2d4c8a8b431ce968bb652fc795cd954c7308c7179d06b6`.

## SAT

- Page 001, endpoints 0–3, 1.000000–21.289609s: Partial SAT title, example formula, definition/history cards fit; formula remains within horizontal margins. SHA256 `b290df1e4802795fa8640e91d41a9ffc89fab64d221c4fcec3ef410f06b1d971`.
- Page 002, endpoints 4–7, 34.181141–60.578024s: DPLL rule list, initial search node and history cards are separated; dim inactive rules are intentional emphasis. SHA256 `deaeff37526c29da85f6fa5a898f901961be6d438cbef405be6c59190375e800`.
- Page 003, endpoints 8–11, 66.553678–109.406918s: DPLL tree labels/terminal marks and SAT-probability chart endpoint fit without clipping. SHA256 `44f45b32b5f49d5834757de461aec04f0ec3eefe56c46daf2785f84703a02f10`.
- Page 004, endpoints 12–13, 125.652080–131.328058s: Four probability curves, legend, threshold/reference annotations fit; scene render failed after this endpoint, so later content unreviewed. SHA256 `62e71eb1af5d4acc958bc007b08531d27118e9e1e17fa3d92432c6b26d224f4d`.

## Knowledge

- Page 001, endpoints 0–3, 1.000000–26.514692s: Chapter title and semantic network labels/arrowheads are clear; inheritance/exception captions do not overlap nodes. SHA256 `a0988e0e5172110fce7113a54e9cceefed18de48c0a0948d5255fcb0534a7517`.
- Page 002, endpoints 4–7, 31.457435–62.823048s: Frame panel/history cards fit next to network; expert-system pipeline, facts and rule-chain endpoints remain separated. SHA256 `21958ccae0741c858b6fd21f4b040f06fe81b1623d794dde9896d15d21f896f0`.
- Page 003, endpoints 8–11, 76.450845–125.336362s: Rule chain, DENDRAL card, MYCIN example and certainty-factor calculation fit; equations and Chinese captions remain separate. SHA256 `cf03e0cea7d886e661955c03181c25ab72808df134a7a76783295bd2050740c4`.
- Page 004, endpoints 12–15, 129.426855–168.459110s: MYCIN/XCON cards and red caveat fit next to formula; knowledge-engineering pipeline has clear boxes/arrows. SHA256 `1b6976a1da7d9f482fb0afd947bc4adf72bbb1d49a118e0f38505edfa00511fc`.
- Page 005, endpoints 16–19, 183.960809–218.653495s: Brittleness/Cyc panels and historical knowledge graph remain within frame; labeled relations do not cross text. SHA256 `aa13a4c4d5e58ba6cde012b43bd364997e6d2a911345c3cf73b70f6e9d42c618`.
- Page 006, endpoints 20–20, 234.356984–234.356984s: Final knowledge graph,2012card and Chinese closing caption fit with distinct arrow labels. SHA256 `39a411a663ac5833852afd4909e725105e9c1be074443b15fa86d57f2c5b4c88`.

## Eliza

- Page 001, endpoints 0–3, 1.000000–37.785932s: Chinese title/history card and keyword→decomposition→reassembly pipeline fit. Example sentence/pattern groups remain separate. SHA256 `a0eefc510bd45875bc8c35ada6d3666a5cd46f8b2dc39fc8c055be1e4232530c`.
- Page 002, endpoints 4–7, 44.180887–97.465042s: Historical dialogue pairs retain wrapping/boxes and comparison marks; mismatch row shows tiny source reply below with no clipping. SHA256 `5a1fc26d7aa9e792707a27b855effe83013a93df7dc7f0d75ec92e566724a8de`.
- Page 003, endpoints 8–11, 121.564564–151.345727s: Fresh-input examples,history card,Chinese paraphrase and ELIZA-effect definition fit without overlap. SHA256 `935cd3201799b2d19c6c87c36b56b7ad285e01bd17ebe44b9592ed841032e6fd`.
- Page 004, endpoints 12–12, 157.251960–157.251960s: Final four-card layout and Chinese paraphrase fit within margins; small secondary provenance text stays inside cards. SHA256 `3f1e7bc60681de264f36f894207a137b1cf65ee168f5ded01ce1050607acabfb`.

## Winters

- Page 001, endpoints 0–3, 1.000000–22.410120s: Chinese chapter title/timeline and1958promise captions fit; first ALPAC/perceptron cards remain distinct. SHA256 `1b94794ab06310c7e111addfe177a8b3762180e6efd4ed52293ab6b55e0eefae`.
- Page 002, endpoints 4–7, 32.007260–66.498792s: Three first-winter cards,debate caption and funding annotations fit with separate rows. SHA256 `b5dbfab15543fbcbe80a690aa6f53a6f985b20f244bdd91d257f01dce311aadd`.
- Page 003, endpoints 8–11, 70.591363–101.761481s: 1980/1982/1983boom cards,Lisp-machine caption and decline cards preserve margins and nonoverlapping borders. SHA256 `4073621b77ebe080a5eee1d8c25a712c731288b09e4535f7fb1f874758444c3c`.
- Page 004, endpoints 12–15, 113.465082–133.236921s: Second-winter endpoint and two-column Moravec comparison preserve text gaps around divider. SHA256 `87fb624d4b300cebfd061a5f679b6efd056153d39fbc80bf2ca998022c9f56fb`.
- Page 005, endpoints 16–19, 140.954805–184.754243s: Moravec attribution and cumulative-vocabulary chart endpoints fit; log axis/callouts remain separate. SHA256 `5de5f093c0f395b88fdb0c8651e12875f441f3e7825b6fb1a087648eacfac6c7`.
- Page 006, endpoints 20–21, 191.020846–195.184254s: Vocabulary percentage callouts,rare-word totals and red unseen-word examples fit in right column without clipping. SHA256 `f7654ed22440a650aa7c62f9ee16a58eb90d497e888880b8cb38bb10f676d895`.

## Limits

- Endpoint stills only: transitions,animation,pacing,continuous playback,listening and narration alignment remain unverified.
- Each listed frame visually reviewed on native854x480 tiles; five priority frames separately viewed at native resolution.
- Source-change/stale warnings preserved; historical pixels do not establish current-source sign-off.
- Partial failed SAT render covers only14recorded endpoints; later scene content remains unreviewed until repaired rerender.
