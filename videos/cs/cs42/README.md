# Computer Science, Built — Part 42: The Browser and the Web

Part 42 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the third part of Act VIII, *Building Software*. A browser is a parser that never
rejects its input, a constraint solver, a GPU compositor, a JIT compiler and an operating system for untrusted code,
held together by one event loop with a 16.7 ms deadline. We build the pieces small enough to read, and run them
together as a toy browser that renders this series' own README.

The instruments are in `explainer/cs/web/` (tested in `tests/test_cs42_web.py`):
* `html.py`: a tokenizer written as a state machine with error recovery (character references decoded), and a tree
  builder with an open-element stack that closes `<p>` and `<li>` implicitly, ignores stray end tags and reopens
  misnested formatting (a simplified adoption agency); a Markdown converter for this repository's READMEs.
* `css.py`: selectors (tag, class, id, descendant), specificity as (a, b, c), the cascade with inheritance and inline
  styles, right-to-left matching with counted element tests, and a synthetic deep page.
* `layout.py`: block and inline layout with greedy line breaking, font fallback for CJK text and spacing taken from
  the source; Knuth–Plass line breaking by dynamic programming; the flexbox grow/shrink algorithm; nested intrinsic
  sizing with and without a cache; a PIL painter with real fonts; `render_markdown`, the whole browser.
* `events.py`: the HTML event loop (tasks, microtasks, rendering steps, `requestAnimationFrame`, async functions) as a
  small interpreter; a frame timeline with a long task, and the same work in chunks.
* `js.py`: hidden classes with transitions, inline caches (monomorphic, polymorphic, megamorphic), type feedback and
  deoptimization.
* `vdom.py`: a reconciler with React's heuristics (keyed and unkeyed), the fewest moves by a longest increasing
  subsequence, Zhang–Shasha tree edit distance, and signals as a dependency graph.
* `platform.py`: the WCAG contrast ratio from sRGB, origins and CORS decisions, an HTTP cache with revalidation and
  stale-while-revalidate, the critical rendering path, Cumulative Layout Shift, and an LTE radio-energy model.

## Chapters

* **Hook.** What happens when you type a URL, layer by layer (Parts 30, 36, 37). Five machines in one program. Our
  toy browser's rendering of the README: 146 nodes, 23 blocks, 786 words.
* **1. Thirty years of the web.** CERN 1989–91, Mosaic, Netscape, JavaScript in ten days, CSS, the browser wars,
  AJAX, Chrome and V8, WHATWG and the living standard.
* **2. Parsing HTML.** The tokenizer as a state machine consuming `<p class=note>Hi <b>there</p>`; six malformed
  inputs and the trees they become; why HTML is not parsed by a grammar; the open-element stack; the adoption agency.
* **3. The cascade.** Specificity as a lexicographic order; a cascade worked through, with inheritance; right-to-left
  matching: on a 2,000-element page of mean depth 21, ten selectors cost 34,193 element tests right to left against
  118,685 left to right (on the shallow README the two are about equal); the render tree.
* **4. Layout.** The box model and normal flow; flex items growing and shrinking; grid; greedy against Knuth–Plass
  on Darcy's letter in *Pride and Prejudice* (worst line 77.8 px short against 54.8; badness 2.40 against 1.86; better
  on 284 of 300 paragraphs, median ratio 0.68); the breakpoint graph of the novel's first sentence; incremental
  relayout (22 of 786 words re-broken).
* **5. Paint, layers and the frame.** Display lists, layers and compositing; the 16.7 ms budget; a 120 ms task drops
  7 frames, the same work in 8 ms chunks drops none.
* **6. The event loop.** Tasks, microtasks and rendering; four orderings computed; async/await; run-to-completion;
  workers.
* **7. JavaScript engines.** Tiers, hidden classes and inline caches (1, 1.5, 2.5 shape checks per access; a
  dictionary lookup every time when megamorphic); deoptimization at calls 5 and 9; generational GC.
* **8. UI frameworks.** Tree edit distance against React's heuristics; keyed lists (prepend: 3 nodes touched against
  103; swap two: React's pass moves 99 rows, the LIS 2); signals as a dependency graph.
* **9. Caches, offline and local-first.** An HTTP cache over an afternoon; content-hashed assets; service workers;
  local-first software and CRDTs (Part 39).
* **10. Web performance.** The critical rendering path (345 ms against 245 ms, illustrative); Core Web Vitals; CLS
  computed; compression measured; HTTP/2 and HTTP/3.
* **11. The security model.** Origins, CORS decisions, an injected handler parsed by our parser, CSP, cookies and
  CSRF, site isolation after Spectre, WebAssembly.
* **12. Accessibility and mobile.** The accessibility tree and ARIA; the WCAG contrast ratio derived (black on white
  21; #767676 the lightest passing grey on white; this series' palette checked); radio power states: ten requests 20 s
  apart cost about 130 J against 16.5 J batched.
* **13. Our toy browser.** Each stage on the README; block boxes and the painted page; each stage timed (about
  150 ms in all in Python, against a 16.7 ms frame); what a real engine adds.
* **14. Frontier: layout, engines and proofs.** Nested intrinsic sizing: 2,097,151 layouts at depth 20 without a
  cache, 41 with one; Cassius and VizAssert; parallel layout; the JIT as an attack surface; formal models of web
  security (Akhawe et al., Featherweight Firefox, the Web Infrastructure Model, WebSpec). Four open problems and the
  ★ research problem.
* **Outro.** Recap, payoffs, practice, problems, next part.

## Build

```bash
python -m videos.cs.cs42.compute
python -m unittest tests.test_cs42_web
python tools/build.py cs42
```

## Problems, with solutions

1. **Specificity.** Show that specificity is a total preorder on selectors, and give two selectors with equal
   specificity whose order in the stylesheet decides the style.

   *Solution.* Specificity maps a selector to a triple (a, b, c) of counts of ids, of classes (and attributes and
   pseudo-classes), and of type selectors; triples are compared lexicographically, which is a total order on ℕ³.
   Pulled back to selectors it is reflexive, transitive and total, but not antisymmetric, since different selectors
   share a triple: a total preorder. `.note p` and `p.lead` both have (0, 1, 1); for `<div class=note><p class=lead>`
   both match, and the later rule in the stylesheet wins, which is why the cascade's last key is source order.

2. **Knuth–Plass.** Prove that the dynamic program finds an optimal set of breaks in O(nw) time for n words and at
   most w words per line, and that greedy is optimal when only the number of lines counts.

   *Solution.* Let best(j) be the least total cost of setting words 1..j with a break after j. A line ending at j
   starts after some break i < j, and the cost is additive over lines, so best(j) = min over feasible i of
   best(i) + cost(i, j): an optimal setting of 1..j ends with an optimal setting of 1..i (exchange argument).
   Feasible i are those whose line fits, at most w of them, so the table costs O(nw). For the number of lines:
   by induction, after k lines greedy has placed at least as many words as any setting does in k lines (greedy's
   k-th line starts no later, and then takes as many words as fit), so it never needs more lines.

3. **Event-loop orderings.** Give the output order of a program mixing `setTimeout`, promises and `await`, and justify
   each step from the event loop's rules.

   *Solution.* For `log("A"); setTimeout(() => log("B")); Promise.resolve().then(() => log("C")); log("D")`: the script
   is one task and runs to completion, logging A and D; the `then` callback was queued as a microtask and the timer as
   a task. After the task the microtask queue drains (C), and only then does the loop take the next task (B): A, D, C,
   B. An async function runs synchronously until its first `await`, and the rest of it is queued as a microtask, so
   `log("before"); f(); log("after")` with `async function f() { log("f starts"); await null; log("f resumes") }`
   prints before, f starts, after, f resumes.

4. **Contrast.** Derive the contrast ratio's range, 1 to 21, and find the lightest grey with ratio 4.5 on white.

   *Solution.* Relative luminance L lies in [0, 1] (0 for black, 1 for white), and the ratio is
   (L₁ + 0.05)/(L₂ + 0.05) with L₁ ≥ L₂: at least 1 (equal colours) and at most 1.05/0.05 = 21. On white
   (L = 1) we need L ≤ 1.05/4.5 − 0.05 ≈ 0.1833. A grey v/255 has L equal to its linearised value; solving
   ((c + 0.055)/1.055)^2.4 ≤ 0.1833 gives c ≤ 0.4653, so v ≤ 118.7. The lightest integer grey is 118 = #767676,
   with ratio 4.54; #777777 gives 4.48 and fails.

5. **Build.** Add a flexbox container to our toy browser, and render a navigation bar that shrinks as the window
   narrows.

   *Solution sketch.* Give `layout` a `display: flex` branch: measure each child's basis as its max-content width (the
   sum of its word widths), call `flex(container, items)` to get the sizes, place the children left to right at those
   widths, and lay each child's text inside its own width; the line height of the bar is the tallest child's.
   Rendering the bar at 900, 600 and 400 px shows the grow and shrink cases; below the sum of the minimum
   (longest-word) widths, real flexbox overflows rather than shrinking further, and a complete answer clamps there.

6. **★ Research.** Find a flex-layout algorithm with intrinsic sizing whose relayout cost is bounded by the size of
   the change, with a matching lower bound.

   *Discussion.* Open. Engines cache layout results by (box, constraints), which makes a full layout linear in
   practice, but a change deep in a nested flex tree can change intrinsic sizes all the way up and the free space at
   every level on the way down. A good answer would define the size of a change (the boxes whose computed geometry
   differs), give an algorithm whose work is within a polylogarithmic factor of it, and prove that no algorithm can do
   asymptotically better on some family of pages; partial results for normal flow alone, or for flex without
   wrapping, would already be new.

## 习题与解答

1. **特异性。** 证明特异性是选择器上的一个全预序，并给出两个特异性相等、由样式表中的顺序决定样式的选择器。

   *解答。* 特异性把选择器映射到三元组 (a, b, c)：id 的个数、类（以及属性和伪类）的个数、类型选择器的个数；三元组按字典序比较，
   这是 ℕ³ 上的全序。拉回到选择器上，它是自反、传递且完全的，但不是反对称的，因为不同的选择器可以有同一个三元组：所以是全预序。
   `.note p` 和 `p.lead` 都是 (0, 1, 1)；对 `<div class=note><p class=lead>` 两者都匹配，样式表中靠后的规则胜出，这正是层叠的最后
   一个键是源顺序的原因。

2. **Knuth–Plass。** 证明这个动态规划在 O(nw) 时间内找到最优断行（n 个词，每行至多 w 个词），并证明只计行数时贪心是最优的。

   *解答。* 设 best(j) 为排好第 1..j 个词、且在 j 之后断行的最小总代价。以 j 结尾的一行从某个断点 i < j 之后开始，代价按行可加，
   所以 best(j) = 对所有可行 i 取 best(i) + cost(i, j) 的最小值：1..j 的最优排法以 1..i 的最优排法结尾（交换论证）。可行的 i 是那些
   使该行放得下的 i，至多 w 个，所以整张表的代价是 O(nw)。关于行数：归纳地，排完 k 行后，贪心放下的词至少和任何排法在 k 行里放下的
   一样多（贪心的第 k 行开始得不更晚，然后放下尽可能多的词），所以它从不需要更多的行。

3. **事件循环中的顺序。** 给出一个混合 `setTimeout`、promise 和 `await` 的程序的输出顺序，并用事件循环的规则说明每一步。

   *解答。* 对 `log("A"); setTimeout(() => log("B")); Promise.resolve().then(() => log("C")); log("D")`：脚本是一个任务，运行到底，输出
   A 和 D；`then` 的回调排进了微任务队列，定时器排进了任务队列。任务结束后先清空微任务队列（C），然后循环才取下一个任务（B）：
   A、D、C、B。async 函数同步运行到它的第一个 `await`，其余部分作为微任务排队，所以 `log("before"); f(); log("after")`，其中
   `async function f() { log("f starts"); await null; log("f resumes") }`，输出 before、f starts、after、f resumes。

4. **对比度。** 推导对比度的取值范围 1 到 21，并求出在白底上对比度为 4.5 的最浅灰色。

   *解答。* 相对亮度 L 在 [0, 1] 之间（黑为 0，白为 1），对比度为 (L₁ + 0.05)/(L₂ + 0.05)，L₁ ≥ L₂：至少为 1（颜色相同），至多为
   1.05/0.05 = 21。在白底（L = 1）上需要 L ≤ 1.05/4.5 − 0.05 ≈ 0.1833。灰色 v/255 的 L 等于它线性化后的值；解
   ((c + 0.055)/1.055)^2.4 ≤ 0.1833 得 c ≤ 0.4653，即 v ≤ 118.7。最浅的整数灰度是 118 = #767676，对比度 4.54；#777777 为 4.48，
   不达标。

5. **动手。** 给我们的玩具浏览器加上 flexbox 容器，渲染一个随窗口变窄而收缩的导航栏。

   *解答要点。* 给 `layout` 加一个 `display: flex` 分支：把每个子元素的基础尺寸量为它的 max-content 宽度（各词宽度之和），调用
   `flex(container, items)` 得到尺寸，按这些宽度从左到右放置子元素，并在各自宽度内排它们的文字；导航栏的行高取最高的子元素。
   在 900、600 和 400 像素下渲染，可以看到伸展和收缩两种情形；当宽度小于各子元素最小（最长单词）宽度之和时，真正的 flexbox 会溢出
   而不再收缩，完整的答案应在那里截断。

6. **★ 研究。** 求一个带固有尺寸的 flex 布局算法，其重新布局的代价受变化大小的约束，并给出相匹配的下界。

   *讨论。* 尚未解决。引擎按（盒子，约束）缓存布局结果，使完整布局在实践中是线性的；但深层嵌套的 flex 树中的一处改动，可能一路向上
   改变固有尺寸，再一路向下改变每一层的剩余空间。好的答案应定义变化的大小（计算出的几何发生改变的盒子），给出工作量在其多对数因子
   之内的算法，并证明在某一族页面上没有算法能渐近地做得更好；仅对常规流，或仅对不换行的 flex 的部分结果，就已经是新的。

## Glossary additions

* **tokenizer, tree builder, open-element stack, adoption agency** — the HTML parser's two stages; the elements open
  at the current point; the repair for misnested formatting.
* **DOM, CSSOM, render tree** — the document's tree; the stylesheets' object model; the styled tree layout uses.
* **cascade, origin, specificity, inheritance** — how a property's value is chosen among rules.
* **box model, normal flow, block and inline boxes, line box** — content, padding, border, margin; how boxes stack
  and flow.
* **flexbox, flex basis, grow and shrink factors, grid, fr** — one- and two-dimensional distributions of space.
* **greedy (first-fit) and total-fit line breaking, badness** — breaking each line as soon as it is full; minimizing a
  cost over the whole paragraph.
* **paint, display list, layer, compositing, raster** — drawing commands; independently drawn surfaces; combining
  them on the GPU; turning them into pixels.
* **frame budget, jank, requestAnimationFrame** — 16.7 ms at 60 Hz; missed frames; a callback before the next frame.
* **event loop, task, microtask, run-to-completion** — the browser's scheduler and its units of work.
* **hidden class (shape, map), inline cache, deoptimization** — an object layout shared by objects; a per-site cache
  of layouts; falling back from optimized code.
* **virtual DOM, reconciliation, key, signal** — a tree diffed to update the page; matching children; a reactive
  value with dependents.
* **HTTP cache, max-age, ETag, 304, stale-while-revalidate, service worker** — caching and revalidating responses;
  a script that intercepts a page's requests.
* **critical rendering path, LCP, INP, CLS** — what first paint waits for; Core Web Vitals.
* **origin, same-origin policy, CORS, preflight, CSP, XSS, CSRF, SameSite** — the browser's security boundaries and
  the attacks across them.
* **site isolation, sandbox, WebAssembly** — a process per site; confining a process; a portable compiled format.
* **accessibility tree, ARIA, relative luminance, contrast ratio** — what assistive technology reads; roles and
  states; the WCAG formulas.
* **radio resource control (RRC) states, tail energy** — a phone radio's power states; energy spent before idling.

## Sources

* P. Panchekha and C. Harrelson, *Web Browser Engineering* (2025); I. Grigorik, *High Performance Browser
  Networking* (2013); T. Garsiel and P. Irish, "How Browsers Work" (2011).
* WHATWG, *HTML Living Standard* (§13.2, parsing; §8.1.7, event loops); W3C CSS Cascading and Inheritance Level 4,
  CSS Flexible Box Layout Level 1; WCAG 2.2 (2023).
* D. Knuth and M. Plass, "Breaking paragraphs into lines", Software: Practice and Experience 1981.
* K. Zhang and D. Shasha, "Simple fast algorithms for the editing distance between trees", SIAM J. Comput. 1989.
* L. Meyerovich and R. Bodík, "Fast and parallel webpage layout", WWW 2010; P. Panchekha and E. Torlak,
  "Automated reasoning for web page layout", OOPSLA 2016; P. Panchekha et al., "Verifying that web pages have
  accessible layout", PLDI 2018.
* D. Akhawe, A. Barth, P. Lam, J. Mitchell and D. Song, "Towards a formal foundation of web security", CSF 2010;
  A. Bohannon and B. Pierce, "Featherweight Firefox", WebApps 2010; D. Fett, R. Küsters and G. Schmitz, "A
  comprehensive formal security analysis of OAuth 2.0", CCS 2016; L. Veronese et al., "WebSpec", S&P 2023.
* J. Huang et al., "A close examination of performance and power characteristics of 4G LTE networks", MobiSys 2012.
* M. Kleppmann, A. Wiggins, P. van Hardenberg and M. McGranaghan, "Local-first software", Onward! 2019.
