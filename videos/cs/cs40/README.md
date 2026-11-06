# Computer Science, Built — Part 40: Software Engineering

Part 40 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first part of Act VIII, *Building Software*, and the series' third review part.
What one person writes in a weekend fails differently from what a thousand people change every day. The discipline
named at the 1968 NATO conference is about managing that complexity: modules that hide decisions, interfaces that
survive change, tests that pin behaviour down, and teams whose structure becomes the system's. Wherever a claim
can be tested we test it, often on this repository itself.

The instruments are in `explainer/cs/se/` (tested in `tests/test_cs40_se.py`):
* `kwic.py`: Parnas's keyword-in-context index as real code in both decompositions (the flowchart with shared tables;
  one module per hidden decision), four of Parnas's changes applied to each, every variant run and compared, and the
  modules and lines touched counted.
* `repo.py`: this repository's Python import graph (modules, edges, Tarjan's strongly connected components, imports
  across layers, afferent and efferent coupling and Martin's instability); its git history (commits, churn) and
  logical coupling (files changed in the same commits); a trigram model's cross-entropy on its code and on the
  thirty novels.
* `testing.py`: a suite with eight planted flaky tests (asynchronous waits, a polluter and its victim, a hidden
  setter, time, unordered collections) run in random orders, retries, and bisection for the polluter; a QuickCheck-
  style property test with shrinking (Square against Rectangle); an AST mutation tool with time limits, run against
  the Pebble assembler and this repository's tests; statement coverage by tracing; a grammar-aware fuzzer for the
  assembler.
* `process.py`: Brooks' law as a simulation (coordination, ramp-up, mentoring); Monte Carlo schedules of lognormal
  tasks; Kanban work-in-progress limits and Little's law; a model of technical debt; merge conflicts against how
  often branches are integrated.

## Chapters

* **Hook.** Garmisch, October 1968: the software crisis, OS/360, Brooks' law. The software you are watching: 2,587
  Python modules, 614,570 lines, 5,564 imports, 5 import cycles, 2 imports against the layering.
* **1. Complexity, and Parnas' rule.** Essential and accidental complexity ("No Silver Bullet"). KWIC built twice
  (31 index lines, identical): storing words packed touches 3 of 5 modules (16 lines) against 1 of 6 (9 lines);
  storing shifts in full 3 against 1; sorting on demand 2 against 1; the input format 1 and 1. Information hiding;
  deep modules.
* **2. Abstraction and contracts.** Abstract data types, representation invariants and abstraction functions;
  design by contract; Square fails the Rectangle property on the first random trial, shrunk to (w, h) = (0, 1);
  Liskov and Wing's rules. Hyrum's law; semantic versioning; Python's dictionary order.
* **3. Coupling, measured.** Layers: 2,292 imports from scenes to library, 2 the wrong way
  (`explainer.ai.novels` → `videos.ai.ai1`). Instability: 1,694 modules at I ≈ 1, 232 near 0; the most depended-upon
  packages. Five cycles (one in the library's root); dependency inversion. Logical coupling in the history: the
  instructions file, the syllabus and the series plan change together because they store one fact three times.
* **4. Design.** SOLID with a counterexample for each; six patterns where the series used them; Norvig's 16 of 23;
  the expression problem; illegal states unrepresentable; a functional core in an imperative shell.
* **5. Testing.** The pyramid and test doubles. 189 tests with 8 flaky, 400 random orders: 82% of runs red, 51%
  after two retries; the victim fails 55% in the suite and never alone, the hidden dependant 51% in the suite and
  always alone; Google's 1.5% of runs and 16% of tests. Bisection finds the polluter among 159 tests in 7 runs.
  Fuzzing the assembler: of 20,000 random programs, 7,292 crash at 24 sites instead of raising `AsmError`.
* **6. Testing the tests.** Mutation testing; the assembler's tests cover 77% of its statements and kill 62% of 146
  mutants; 10 survivors sit on lines the tests run (`.word` reserving 5 bytes; `j` and `ret` overwriting `ra`);
  Google's mutation analysis in review. Statement, branch, MC/DC and exhaustive coverage.
* **7. Changing code that works.** Refactoring, characterization tests, smells. A model of technical debt over two
  years: never refactoring delivers 565, 10% 790, 20% 832, 30% 728. The 100× cost-of-delay curve against Menzies et
  al.'s 171 projects; Bossavit's leprechauns.
* **8. Review and process.** Inspections and modern review; review size. Royce's waterfall, iterations, the Agile
  Manifesto. Integration interval against merge conflicts (daily: 35% of merges, 3 conflicts per week of work; every
  two weeks: 99%, 15 per week). WIP limits: no limit, 1,309 items in progress and 840 days each; a limit of 8, 6.3
  days; Little's law. DORA's four metrics; Goodhart.
* **9. Teams.** Conway's law and the inverse manoeuvre; Windows Vista's organizational metrics. n(n − 1)/2. Brooks'
  law simulated: four people added in month 2 finish in month 17.8, in month 16 in 22.6 against 22.3 with nobody
  added; from the start, 24 people is fastest. The truck factor; xz.
* **10. Estimates.** Lognormal tasks: median 5 days, mean 6. Twenty tasks: plan 100 days; on time 27%, 12%, 4% for
  σ = 0.3, 0.6, 1.0; four parallel streams 1%. The cone of uncertainty; reference-class forecasting.
* **11. The profession.** Licenses from MIT to AGPL; open-source economics and Heartbleed. The Post Office Horizon
  scandal and the 737 MAX. Privacy by design, accessibility, Therac-25, the ACM Code.
* **12. Frontier: evidence, and machines that code.** Mining repositories; code is natural (a trigram model: 4.3
  bits per token on this repository's code, 8.0 on the novels). HumanEval's pass@k and SWE-bench; tests as an
  incomplete oracle, shown by our assembler's surviving mutants. Four open problems, and the ★ research problem.
* **Outro.** Recap, payoffs, practice, problems, next part.

## Build

```bash
python -m videos.cs.cs40.compute
python -m unittest tests.test_cs40_se
python tools/build.py cs40
```

## Problems, with solutions

1. **Parnas' modules.** For the second decomposition, list the decision each module hides, and predict which modules
   each of the four changes touches.

   *Solution.* Line Storage hides how words and lines are represented; Input hides the input format; the Circular
   Shifter hides how a shift is represented; the Alphabetizer hides when and how ordering is computed; Output hides
   the output format; Master hides the order of the calls. Packing words is a Line Storage decision, the input
   format an Input decision, storing shifts a Shifter decision, sorting on demand an Alphabetizer decision: one
   module each, as measured. In the flowchart design the word tables and the shift list are shared, so every module
   that reads them knows the representation: 3, 1, 3 and 2 modules.

2. **Behavioural subtyping.** State the rules for pre- and postconditions, and show that a stronger precondition
   breaks a client.

   *Solution.* S's method m is a valid override of T's when pre_T ⇒ pre_S (the subtype accepts at least what the
   supertype did) and post_S ⇒ post_T (it promises at least as much). Suppose T.withdraw requires 0 < a ≤ balance and
   S.withdraw requires 0 < a ≤ balance − 100. A client proved correct against T calls withdraw(balance) on an S
   object; T's precondition holds, S's fails, and the call raises (or misbehaves), so substituting S broke a correct
   client.

3. **Little's law.** Prove L = λW for a system that starts and ends empty.

   *Solution.* Let N(t) be the number in the system over [0, T], and item i spend W_i inside. The area A = ∫ N(t) dt
   counted vertically is the sum over items of their time inside, A = Σ W_i. Then A/T = (n/T)(Σ W_i / n), that is
   L = λW, with L = A/T the average number in the system, λ = n/T the throughput and W the mean time inside. In the
   Kanban table, a limit of 8 gives 5.37 items in progress at 0.796 a day, so W = 6.7 days by the law against 6.3
   measured (the difference is the warm-up period that the measurement excludes).

4. **Parallel streams.** With k independent streams, show P(on time) = ∏ P(stream i on time).

   *Solution.* The project is on time iff every stream is: {max_i T_i ≤ D} = ∩_i {T_i ≤ D}, and for independent
   streams the probability of an intersection is the product. Each of our four streams has five tasks and a plan of
   25 days; one stream meets it with probability p ≈ 0.31, so all four with p⁴ ≈ 0.009, matching the simulated 1%.

5. **Build.** Kill the ten surviving mutants on lines the tests run.

   *Solution sketch.* For `.word`: assemble `.word 1, 2` followed by a label and assert the label's address is 8. For
   `j` and `ret`: set `ra` to a known value, execute `j` (and a `call` followed by `ret`), and assert `ra` afterwards.
   For the `x + 4` constant expressions: assemble `la a0, x+4` and check the immediate. Re-running the mutation
   tool should leave only mutants on unexecuted lines, which need tests of the error paths (and expose the fuzzer's
   crashes: those lines raise `IndexError` instead of `AsmError`).

6. **★ Research.** A test-adequacy score that predicts whether an accepted patch is correct.

   *Discussion.* Open. Mutation score measures a suite's power to reject wrong programs near the original, which is
   the relevant distribution for patches; coverage does not. A research programme: generate patches with known
   correctness (mutants, and mutants of the fixed program), measure how often each suite accepts a wrong one, and
   test whether the mutation score, or a weighted version of it (by mutant type or by distance to the patch),
   predicts acceptance of wrong real patches, for example on SWE-bench tasks.

## 习题与解答

1. **Parnas 的模块。** 对第二种分解，列出每个模块隐藏的设计决策，并预测四项改动各自会触及哪些模块。

   *解答。* 行存储隐藏词与行的表示方式；输入模块隐藏输入格式；循环移位器隐藏移位的表示；排序器隐藏何时以及如何排序；输出模块
   隐藏输出格式；主控隐藏调用顺序。把词压缩存储是行存储的决策，输入格式是输入模块的决策，完整存储移位是移位器的决策，按需排序是
   排序器的决策：各只触及一个模块，与测量一致。在流程图式设计中，词表和移位列表是共享的，读取它们的每个模块都知道表示方式：
   分别触及 3、1、3、2 个模块。

2. **行为子类型。** 写出前置条件与后置条件的规则，并说明更强的前置条件会破坏调用方。

   *解答。* 当 pre_T ⇒ pre_S（子类型至少接受父类型接受的）且 post_S ⇒ post_T（它的承诺至少同样多）时，S 的方法 m 才是 T 的
   合法覆盖。设 T.withdraw 要求 0 < a ≤ 余额，而 S.withdraw 要求 0 < a ≤ 余额 − 100。一个对 T 证明正确的调用方对 S 对象调用
   withdraw(余额)：T 的前置条件成立，S 的不成立，调用出错，所以用 S 替换破坏了一个正确的调用方。

3. **Little 定律。** 对开始和结束时都为空的系统证明 L = λW。

   *解答。* 设 N(t) 为 [0, T] 内系统中的数目，第 i 件在系统内停留 W_i。面积 A = ∫ N(t) dt 按竖直方向计数，等于各件停留时间之和，
   A = Σ W_i。于是 A/T = (n/T)(Σ W_i / n)，即 L = λW，其中 L = A/T 是平均在制数，λ = n/T 是吞吐量，W 是平均停留时间。在看板
   表中，限额为 8 时在制 5.37 件、每天完成 0.796 件，由定律得 W = 6.7 天，测得 6.3 天（差别来自测量剔除的预热期）。

4. **并行的工作流。** 对 k 条相互独立的工作流，证明 P(按时) = ∏ P(第 i 条按时)。

   *解答。* 项目按时当且仅当每条工作流都按时：{max_i T_i ≤ D} = ∩_i {T_i ≤ D}，独立事件交的概率等于乘积。我们四条工作流各有
   五项任务、计划 25 天；单条按时的概率 p ≈ 0.31，四条都按时为 p⁴ ≈ 0.009，与模拟的 1% 一致。

5. **动手。** 杀死测试已执行到的那些行上存活的十个变异体。

   *解答要点。* 对 `.word`：汇编 `.word 1, 2` 后接一个标号，断言该标号地址为 8。对 `j` 和 `ret`：先把 `ra` 设为已知值，执行
   `j`（以及一次 `call` 后接 `ret`），再断言 `ra` 的值。对 `x + 4` 这类常量表达式：汇编 `la a0, x+4` 并检查立即数。重新运行变异
   工具后，应只剩下未执行行上的变异体；它们需要针对错误路径的测试（也会暴露模糊测试发现的崩溃：这些行抛出 `IndexError` 而不是
   `AsmError`）。

6. **★ 研究。** 设计一个测试充分性评分，能预测被测试接受的补丁是否真正正确。

   *讨论。* 尚未解决。变异得分衡量测试集拒绝原程序附近错误程序的能力，而这正是补丁所处的分布；覆盖率不能衡量这一点。一个研究
   方案：生成正确性已知的补丁（变异体，以及修复后程序的变异体），测量每个测试集接受错误补丁的频率，并检验变异得分或其加权版本
   （按变异类型或与补丁的距离加权）能否预测真实错误补丁被接受的情况，例如在 SWE-bench 任务上。

## Glossary additions

* **essential / accidental complexity** — difficulty inherent in the problem / introduced by the means of building.
* **information hiding, interface, secret** — a module hides one design decision; its interface is what it promises.
* **abstract data type, representation invariant, abstraction function** — a type known by its operations; which
  representations are legal; what a legal one means.
* **design by contract** — preconditions, postconditions and invariants as the terms of an interface.
* **behavioural subtyping (Liskov substitution)** — a subtype demands no more and promises no less.
* **Hyrum's law** — every observable behaviour of a widely used interface becomes depended on.
* **afferent / efferent coupling, instability** — dependents / dependencies; I = Ce / (Ca + Ce).
* **dependency inversion** — high and low levels both depend on an abstraction owned by the high level.
* **logical coupling, shotgun surgery** — files that change together; one change requiring edits in many places.
* **expression problem** — extending both data variants and operations without editing existing code.
* **test double: fake, stub, mock** — working stand-in; canned answers; recorded expectations.
* **flaky test, polluter, victim** — passes and fails on the same code; a test that leaves state; one that suffers.
* **mutation testing, mutation score, equivalent mutant** — wrong versions that tests should reject; the fraction
  rejected; a change with no observable effect.
* **MC/DC** — each condition shown to affect the decision independently.
* **fuzzing** — generating many random or mutated inputs to find crashes.
* **refactoring, characterization test, technical debt** — behaviour-preserving change; a test of current behaviour;
  the future cost of expedient design.
* **Conway's law, Brooks' law, truck factor** — systems mirror communication; adding people late delays; how few
  departures would stall a project.
* **WIP limit, lead time, cycle time** — a cap on work started; request to done; start to done.
* **DORA metrics** — deployment frequency, lead time for changes, change failure rate, time to restore.
* **planning fallacy, cone of uncertainty** — optimism about one's own plans; estimate error narrowing with decisions.
* **copyleft** — a license requiring derived works to be shared on the same terms.
* **pass@k** — the probability that at least one of k sampled programs passes the tests.

## Sources

* F. Brooks, *The Mythical Man-Month* (1975; anniversary edition with "No Silver Bullet", 1995).
* P. Naur and B. Randell (eds.), *Software Engineering: Report of a Conference Sponsored by the NATO Science
  Committee*, Garmisch, 1968 (1969).
* D. Parnas, "On the criteria to be used in decomposing systems into modules", CACM 1972.
* B. Liskov and S. Zilles, "Programming with abstract data types", 1974; B. Liskov and J. Wing, "A behavioral notion
  of subtyping", TOPLAS 1994; B. Meyer, *Object-Oriented Software Construction* (1988).
* J. Ousterhout, *A Philosophy of Software Design* (2018); R. Martin, *Agile Software Development* (2002); E. Gamma,
  R. Helm, R. Johnson and J. Vlissides, *Design Patterns* (1994); P. Wadler, "The expression problem", 1998.
* T. Winters, T. Manshreck and H. Wright, *Software Engineering at Google* (2020).
* Q. Luo, F. Hariri, L. Eloussi and D. Marinov, "An empirical analysis of flaky tests", FSE 2014; W. Lam et al.,
  "iDFlakies", ICST 2019; J. Micco, "Flaky tests at Google and how we mitigate them", 2016.
* R. DeMillo, R. Lipton and F. Sayward, "Hints on test data selection", Computer 1978; Y. Jia and M. Harman, "An
  analysis and survey of the development of mutation testing", TSE 2011; G. Petrović and M. Ivanković, "State of
  mutation testing at Google", ICSE SEIP 2018; B. Miller, L. Fredriksen and B. So, "An empirical study of the
  reliability of UNIX utilities", CACM 1990.
* W. Opdyke, *Refactoring Object-Oriented Frameworks* (thesis, 1992); M. Fowler, *Refactoring* (1999); M. Feathers,
  *Working Effectively with Legacy Code* (2004); W. Cunningham, "The WyCash portfolio management system", 1992.
* T. Menzies, W. Nichols, F. Shull and L. Layman, "Are delayed issues harder to resolve?", EMSE 2016; L. Bossavit,
  *The Leprechauns of Software Engineering* (2015).
* M. Fagan, "Design and code inspections", IBM Systems Journal 1976; A. Bacchelli and C. Bird, "Expectations,
  outcomes, and challenges of modern code review", ICSE 2013.
* W. Royce, "Managing the development of large software systems", 1970; N. Forsgren, J. Humble and G. Kim,
  *Accelerate* (2018).
* M. Conway, "How do committees invent?", Datamation 1968; N. Nagappan, B. Murphy and V. Basili, "The influence of
  organizational structure on software quality", ICSE 2008; G. Avelino et al., "A novel approach for estimating
  truck factors", ICPC 2016; H. Gall, K. Hajek and M. Jazayeri, "Detection of logical coupling based on product
  release history", ICSM 1998.
* D. Kahneman and A. Tversky, "Intuitive prediction: biases and corrective procedures", 1979; B. Boehm, *Software
  Engineering Economics* (1981); S. McConnell, *Software Estimation* (2006); B. Flyvbjerg, "From Nobel prize to
  project management", 2006.
* N. Leveson and C. Turner, "An investigation of the Therac-25 accidents", Computer 1993; *Bates v Post Office Ltd
  (No 6: Horizon Issues)*, High Court, 2019; ACM Code of Ethics and Professional Conduct (2018).
* A. Hindle, E. Barr, Z. Su, M. Gabel and P. Devanbu, "On the naturalness of software", ICSE 2012; M. Chen et al.,
  "Evaluating large language models trained on code", 2021; C. Jimenez et al., "SWE-bench", ICLR 2024.
