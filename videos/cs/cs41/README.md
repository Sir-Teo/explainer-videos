# Computer Science, Built — Part 41: Version Control, Builds and Dependencies

Part 41 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the second part of Act VIII, *Building Software*. Every change to modern software
passes through three machines. The version-control system is secretly a content-addressed Merkle graph; the build
system is an incremental computation over a dependency graph; the package manager is a satisfiability solver, because
choosing versions is NP-complete. Above them, continuous integration and delivery turn a change into running software
a little at a time. Where we can, we measure this repository itself.

The instruments are in `explainer/cs/vcs/` (tested in `tests/test_cs41_vcs.py`):
* `git.py`: an object store in git's own formats (blob, tree and commit ids checked against git 2.43); Merkle
  ripples and corruption detection; random histories, merge bases with criss-cross cases, bisection; three-way merge
  over Myers' diff (Part 21); Myers' edit graph; deltas over every committed version of a file in this repository; the
  size of this repository's history.
* `build.py`: a synthetic C-like project (sources, headers, objects, a library, a test report) built by make's
  timestamps, by verifying traces with early cutoff and by constructive traces with a shared cache; a drawable
  twelve-file project; work, span and greedy scheduling of a clean build.
* `deps.py`: package universes encoded as SAT and solved with Part 26's CDCL; the diamond; the 3-SAT reduction
  (Di Cosmo et al. 2006); a backtracking resolver's trace; solver work at the satisfiability threshold.
* `ci.py`: a merge queue that tests batches and bisects failures; canary analysis by a two-proportion test.

## Chapters

* **Hook.** SCCS to Subversion; BitKeeper and April 2005. Our object store and git 2.43 give identical names to the
  same three files, their tree and their commit.
* **1. Git's objects.** Blobs, trees, commits, tags; nothing overwritten; SHA-1 to SHA-256. The Merkle graph: editing
  one file renames 4 of 6 objects, every one on its path; 2 are shared. One flipped bit ("novdls") is caught by
  rehashing; SHAttered. Branches, HEAD, the index, checkout, the reflog; the three trees and `reset`.
* **2. Merging and bisecting.** Merge bases as best common ancestors; a criss-cross with two (1 and 2); recursive and
  ort; how git paints the graph to find them. Myers' edit graph for ABCABBA → CBABAC (D = 5, four letters kept). A
  three-way merge that keeps both sides' changes, and one that conflicts; rerere. Merge against rebase,
  cherry-pick. Bisect: commit 637 of 1,000 in 10 tests; a million commits in 20.
* **3. Storing history.** Forty versions of this series' syllabus: 4.2 MB stored whole, 154 KB as deltas. This
  repository: 159 commits, 17,440 objects, 861 MB of current files, 888 MB of objects ever, 695 MB packed. The delta
  window and depth. Google's monorepo; shallow, partial and sparse clones. Patch theory (Darcs, Pijul); CRDTs.
* **4. Build systems.** Make (1976) and topological order. On 202 targets: a comment edit costs make 3 rebuilds and a
  hashing build 1; a fresh checkout costs make 202 and the hashing build 0. Recursive make considered harmful. A
  twelve-file project lit up: one header change rebuilds 8 targets. Build systems à la carte. A shared cache: a second
  machine runs 0 of 202 tasks. Work 235 s, span 34 s: one worker 235 s, eight 54 s, beyond 32 no faster. Hermetic and
  reproducible builds; Nix store paths.
* **5. Dependencies.** Semantic versioning, and how often it is kept (a third of Maven releases break something). The
  diamond: app, A, B 1.0/1.1, C 1–3; resolved to B 1.1 and C 2; a resolver's seven steps. The 3-SAT reduction on
  screen and drawn as packages; installable iff satisfiable. Solver conflicts at the threshold: 6, 43, 183, 416 for
  20–80 variables. PubGrub; Go's minimal version selection. npm against pip; left-pad; lockfile hashes. The supply
  chain: event-stream, SolarWinds, xz; signatures, SBOMs, SLSA; vendoring.
* **6. Continuous integration.** Trunk-based development, pre- and post-submit tests, flaky tests. A merge queue on
  20,000 changes: with 1% bad changes, batches of 64 need 0.125 test runs per change; with 10% bad, batches of 4 are
  best (0.61). Test selection over this repository's import graph: the KWIC module reaches 1 test module, the
  assembler 22, the narration engine 71 of 200; the median library module 1%.
* **7. Continuous delivery.** Blue/green, canaries, progressive rollout, feature flags; shadow traffic, dark launches
  and kill switches. A canary that must detect a doubled 0.1% error rate: caught 1%, 7%, 32%, 80% and 100% of the time
  at 1,000 to 100,000 requests (α = 0.01). Expand–contract migrations. Knight Capital (2012). Roll back or roll
  forward. The Job's change, end to end.
* **8. Frontier: merging and building, correctly.** Structured merge (semistructured merge, Spork, Mergiraf); build
  correctness and minimality; complete version solving; reproducibility at scale; authors that are programs. Four open
  problems, and the ★ research problem.
* **Outro.** Recap, payoffs, practice, problems, next part.

## Build

```bash
python -m videos.cs.cs41.compute
python -m unittest tests.test_cs41_vcs
python tools/build.py cs41
```

## Problems, with solutions

1. **Merkle ripples.** Show that changing one file changes exactly the ids of the trees on its path and the commit,
   and that two snapshots share every other object.

   *Solution.* A blob's id is the hash of its content, so the edited file's blob changes and no other blob does.
   A tree's id is the hash of its entries (mode, name, child id); the tree containing the file has one entry with a new
   child id, so its own id changes (with overwhelming probability, by collision resistance); inductively every
   ancestor tree up to the root changes. A tree not on the path has entries whose child ids are all unchanged, so its
   content and id are unchanged; the same holds for every blob off the path. The commit names the root tree, so it
   changes. In our example: 4 objects changed (a blob, two trees, the root), 2 shared.

2. **Two merge bases.** Give a history with two merge bases, and show that merging against either one alone can
   give a different result.

   *Solution.* The criss-cross: 0 → 1 and 0 → 2; 3 merges 1 and 2; 4 merges 2 and 1; 5 extends 3, 6 extends 4. The
   common ancestors of 5 and 6 are {0, 1, 2}; 0 is an ancestor of 1, so the best are 1 and 2. Let line L be "x" in 0,
   "y" in 1 and unchanged in 2, and let the merge at 3 keep "y" while the merge at 4 resolved the same conflict as
   "z". Merging 5 and 6 with base 1 sees L unchanged on side 5 ("y") and changed on side 6 ("z"), and takes "z"
   silently; with base 2 (where L is "x") both sides changed it differently: a conflict. Git's recursive strategy
   first merges 1 and 2 into a virtual base, so that the answer does not depend on an arbitrary choice.

3. **Bisection.** Prove that ⌈log₂ n⌉ tests suffice on a linear history and that none fewer suffice in the worst case.

   *Solution.* With a known good and a known bad commit, n candidates remain for the first bad one. Testing the middle
   one leaves at most ⌈n/2⌉, so ⌈log₂ n⌉ tests reduce the candidates to one. Conversely each test has two outcomes,
   so k tests distinguish at most 2ᵏ cases; to identify one of n candidates requires 2ᵏ ≥ n.

4. **Build correctness.** Show that verifying traces are correct when every task is deterministic and declares all its
   inputs, and give a timestamp scenario that makes Make incorrect.

   *Solution.* By induction in topological order. A task that is skipped has the same input hashes as when it was
   last run; if every input it reads is declared and it is deterministic, rerunning it would produce the same
   output, so the stored output equals what a clean build would produce. A task that runs produces the clean-build
   output by determinism, given that its inputs are by induction the clean-build values. For Make: restore an older
   version of a source file from a backup, keeping its old modification time, which is older than the object built
   from the newer version; Make sees the object as newer than its source and does not rebuild it, so the build
   output corresponds to a source that no longer exists.

5. **Build.** Add constructive traces to our build engine and measure a second machine's build.

   *Solution sketch.* Key every output by (target, hashes of its inputs) in a cache shared between engines; before
   running a task, look its key up and download on a hit. Our implementation (`build_cached`): machine A's clean build
   runs 202 tasks; machine B, at the same commit, runs 0 and downloads 202; after a header change A runs 41 and B
   downloads those 41.

6. **★ Research.** Find the merge-queue policy that maximizes throughput when each change has its own learned failure
   probability.

   *Discussion.* Open. With equal probabilities p, the expected test runs per change for a batch of b with
   binary-splitting is minimized near b ≈ 1/√p for small p (our table: 64 at 1%, 4 at 10%). With heterogeneous,
   predicted pᵢ, natural policies batch low-risk changes together and test high-risk ones alone, and order
   bisection by risk; the problem becomes adaptive group testing with priors, latency constraints and prediction
   error. A good answer would give a policy, bounds against the optimum, and an evaluation on real CI logs.

## 习题与解答

1. **Merkle 涟漪。** 证明修改一个文件恰好改变其路径上各个树对象和提交的标识，而两个快照共享其余全部对象。

   *解答。* blob 的标识是其内容的哈希，所以被编辑文件的 blob 改变，其他 blob 不变。树的标识是其条目（模式、名字、子对象标识）
   的哈希；包含该文件的树有一个条目的子标识变了，所以它自己的标识也变（由抗碰撞性，以压倒性概率）；归纳地，直到根的每个祖先
   树都变。不在路径上的树，其条目的子标识都没变，所以内容和标识不变；路径外的每个 blob 也一样。提交指向根树，所以提交也变。
   在我们的例子里：改变了 4 个对象（一个 blob、两个树、根），共享 2 个。

2. **两个合并基。** 给出一个有两个合并基的历史，并说明只用其中任一个合并，结果可能不同。

   *解答。* 交叉合并：0 → 1、0 → 2；3 合并 1 和 2；4 合并 2 和 1；5 接在 3 后，6 接在 4 后。5 和 6 的公共祖先是 {0, 1, 2}；
   0 是 1 的祖先，所以最佳的是 1 和 2。设第 L 行在 0 中是 "x"，在 1 中是 "y"，在 2 中未变；3 处的合并保留 "y"，而 4 处的合并把
   同一冲突解决成 "z"。以 1 为基合并 5 和 6：5 一侧 L 未变（"y"），6 一侧变成 "z"，于是悄悄取 "z"；以 2 为基（L 为 "x"），两侧都
   以不同方式改了它：冲突。git 的递归策略先把 1 和 2 合并成一个虚拟基，答案就不依赖于一个任意的选择。

3. **二分。** 证明在线性历史上 ⌈log₂ n⌉ 次测试足够，且最坏情况下不能更少。

   *解答。* 已知一个好的和一个坏的提交时，第一个坏提交有 n 个候选。测试中间那个，最多剩 ⌈n/2⌉ 个，所以 ⌈log₂ n⌉ 次测试把候选
   减到一个。反过来，每次测试只有两种结果，k 次测试最多区分 2ᵏ 种情况；要从 n 个候选中确定一个，必须 2ᵏ ≥ n。

4. **构建的正确性。** 证明当每个任务都是确定性的且声明了全部输入时，验证型追踪是正确的；并给出一个让 Make 出错的时间戳场景。

   *解答。* 按拓扑序归纳。被跳过的任务，其输入哈希与上次运行时相同；若它读的每个输入都已声明且它是确定性的，重跑会得到同样的
   输出，所以存下的输出等于干净构建的输出。被运行的任务，由确定性和（归纳得到的）输入都是干净构建的值，产出干净构建的输出。对
   Make：从备份恢复某源文件的旧版本并保留其旧修改时间，它早于由新版本编译出的目标文件；Make 认为目标比源新而不重建，于是构建产物
   对应的是一个已不存在的源文件。

5. **动手。** 给我们的构建引擎加上构造型追踪，并测量第二台机器的构建。

   *解答要点。* 把每个输出按（目标，其输入的哈希）存入一个在多个引擎间共享的缓存；运行任务前先查键，命中就下载。我们的实现
   （`build_cached`）：机器 A 干净构建运行 202 个任务；机器 B 在同一提交上运行 0 个、下载 202 个；改了一个头文件后，A 运行 41 个，
   B 下载这 41 个。

6. **★ 研究。** 当每个变更都有自己学习得到的失败概率时，求使吞吐量最大的合并队列策略。

   *讨论。* 尚未解决。失败概率都等于 p 时，用二分拆分的大小为 b 的批次，每个变更的期望测试次数在 p 较小时于 b ≈ 1/√p 附近最小
   （我们的表：1% 时为 64，10% 时为 4）。若概率各异且为预测值 pᵢ，自然的策略是把低风险变更一起批量测试、高风险的单独测试，并按
   风险安排二分顺序；问题变成带先验、延迟约束和预测误差的自适应组测试。好的答案应给出策略、与最优解的差距界，以及在真实 CI 日志
   上的评估。

## Glossary additions

* **content addressing, object id** — naming data by the hash of its content.
* **blob, tree, commit, tag** — git's four object kinds: bytes, a directory, a snapshot with parents, a named commit.
* **Merkle graph (DAG)** — a graph whose node names are hashes covering their children.
* **ref, branch, HEAD, index, reflog** — mutable names; the current branch; the staged next tree; ref history.
* **merge base, criss-cross merge** — a best common ancestor; a history with more than one.
* **three-way merge, conflict, rerere** — merging two sides against a base; a region both changed differently;
  replaying a recorded resolution.
* **rebase, cherry-pick, bisect** — replaying commits on a new base; applying one commit's diff; binary search for a
  bad commit.
* **packfile, delta, window, depth** — compressed storage of objects as differences; search width; chain length.
* **shallow, partial, sparse clone** — less history; contents on demand; some directories.
* **build target, rule, topological order** — a file to make, how to make it, an order respecting dependencies.
* **dirty bit, verifying traces, constructive traces, early cutoff** — rebuild markers; recorded input hashes; cached
  outputs; stopping when an output is unchanged.
* **hermetic, reproducible build** — sees only declared inputs; bit-identical outputs.
* **semantic versioning, lockfile, vendoring** — MAJOR.MINOR.PATCH; pinned versions and hashes; copied dependencies.
* **diamond dependency, version resolution** — two paths requiring incompatible versions; choosing compatible
  versions (NP-complete).
* **SBOM, SLSA** — a list of a build's components; levels of build provenance.
* **trunk-based development, pre-/post-submit, merge queue** — short-lived branches on one main line; tests before and
  after landing; batched, ordered testing before merging.
* **test selection** — running only the tests a change can affect.
* **blue/green, canary, progressive rollout, feature flag, kill switch** — release strategies.
* **shadow traffic, dark launch** — testing with real requests without exposing results.
* **expand–contract migration** — changing a schema in reversible steps.

## Sources

* S. Chacon and B. Straub, *Pro Git* (2nd ed., 2014); git documentation (`gitformat-pack`, `git-merge-base`).
* R. Merkle, "A digital signature based on a conventional encryption function", CRYPTO 1987; M. Stevens et al.,
  "The first collision for full SHA-1", CRYPTO 2017.
* E. Myers, "An O(ND) difference algorithm and its variations", Algorithmica 1986.
* R. Potvin and J. Levenberg, "Why Google stores billions of lines of code in a single repository", CACM 2016.
* D. Roundy, Darcs (2003); Pijul; M. Kleppmann et al., "Local-first software", 2019.
* S. Feldman, "Make — a program for maintaining computer programs", 1979; P. Miller, "Recursive make considered
  harmful", 1997.
* A. Mokhov, N. Mitchell and S. Peyton Jones, "Build systems à la carte", ICFP 2018 (and JFP 2020); S. Spall,
  N. Mitchell and S. Tobin-Hochstadt, "Build scripts with perfect dependencies", OOPSLA 2020.
* E. Dolstra, *The Purely Functional Software Deployment Model* (thesis, 2006).
* R. Di Cosmo et al., "Managing the complexity of large free and open source package-based software distributions",
  ASE 2006; N. Weizenbaum, "PubGrub: next-generation version solving", 2018; R. Cox, "Minimal version selection", 2018.
* S. Raemaekers, A. van Deursen and J. Visser, "Semantic versioning versus breaking changes: a study of the Maven
  repository", SCAM 2014.
* S. Ananthanarayanan et al., "Keeping master green at scale", EuroSys 2019 (SubmitQueue).
* J. Humble and D. Farley, *Continuous Delivery* (2010); B. Beyer et al., *Site Reliability Engineering* (2016);
  T. Winters, T. Manshreck and H. Wright, *Software Engineering at Google* (2020), chs. 16–24.
* SEC, *In the Matter of Knight Capital Americas LLC*, 2013.
* S. Apel et al., "Semistructured merge: rethinking merge in revision control systems", ESEC/FSE 2011; S. Larsén et
  al., "Spork: structured merge for Java with formatting preservation", TSE 2022.
