from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs41.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load)


class Ci(VoiceoverScene):
    def construct(self):
        self.card()
        self.trunk()
        self.queue()
        self.selection()
        self.savings()

    def card(self):
        card = chapter_card(6, r"Continuous integration", r"How does a busy main branch stay green?",
                            lit=(1999, 2020), extra=((1999, r"Beck: \ Extreme Programming"),
                                                     (2019, r"Uber: \ SubmitQueue")), part=PART)
        with self.voiceover("Chapter six. Continuous integration."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def queue(self):
        q = load("queue")
        head = label(r"A merge queue", font_size=36).to_edge(UP, buff=0.3)
        bs = (1, 4, 16, 64)
        rows = []
        for b in bs:
            row = [f"{b}"]
            for p in (0.01, 0.03, 0.1):
                r = next(x for x in q["rows"] if x["batch"] == b and abs(x["p_bad"] - p) < 1e-9)
                row.append(f"{r['runs_per_change']:.2f} \\ ({r['p_green'] * 100:.0f}\\% green)")
            rows.append(row)
        tab = grid_table([r"batch size", r"1\% of changes bad", r"3\% bad", r"10\% bad"], rows,
                         widths=[2.0, 3.6, 3.4, 3.4], row_h=0.5, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.55).set_x(0)
        best = {}
        for j, p in enumerate((0.01, 0.03, 0.1), 1):
            vals = [next(x for x in q["rows"] if x["batch"] == b and abs(x["p_bad"] - p) < 1e-9)["runs_per_change"]
                    for b in bs]
            k = vals.index(min(vals))
            tab.cells[k + 1][j].set_color(YES)
            best[p] = bs[k]
        lines = VGroup(
            wrapped_label(r"test runs per change: \ the queue tests a batch on top of main; \ if it fails, \ it "
                          r"bisects the batch to find the bad changes, \ and only tested combinations ever land", 12.4,
                          font_size=20, color=WHITE),
            wrapped_label(r"a batch of $b$ is green with probability $(1-p)^b$: \ large batches save runs when "
                          r"changes are rarely bad, \ and waste them when they often are", 12.4, font_size=21,
                          color=HEAD),
            wrapped_label(r"so main is always green, \ even with thousands of changes a day \ (Uber's SubmitQueue, "
                          r"\ GitHub's and GitLab's merge queues)", 12.4, font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "Continuous integration means merging into the main line at least daily, with every change tested. "
            "With hundreds of engineers, testing each change alone is too slow, and testing them separately lets two "
            "changes that each pass break main together. <bookmark mark='a'/> A merge queue tests changes in "
            "order, on top of everything ahead of them, in batches. If a batch passes, all of it lands. If not, the "
            "queue bisects the batch to find the bad changes and lands the rest. <bookmark mark='b'/> A batch of b "
            "changes is green with probability one minus p to the b. We simulated twenty thousand changes. When one "
            "change in a hundred is bad, batches of sixty-four need an eighth of a test run per change. When one in "
            "ten is bad, big batches nearly always fail, and the best batch is about four. "
            "<bookmark mark='c'/> Either way, only tested combinations ever land, so main stays green, which is how "
            "Uber's SubmitQueue and the merge queues of GitHub and GitLab let thousands of changes a day through. "
            "Uber's system goes further and predicts, from a change's history, how likely it is to fail, so that "
            "risky changes are tested alone and safe ones in large groups: the research problem at the end of this "
            "part."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()

    def selection(self):
        a = load("affected")
        head = label(r"Which tests must run?", font_size=36).to_edge(UP, buff=0.3)
        rows = [[rf"\texttt{{{r['module'].replace('_', chr(92) + '_')}}}", f"{r['modules_affected']:,}",
                 f"{r['tests_affected']} of {a['tests']}"] for r in a["rows"] if r["module"] != "explainer.cs"]
        tab = grid_table([r"change this module", r"modules that import it, \ directly or not", r"test modules to run"],
                         rows, widths=[4.4, 4.6, 3.0], row_h=0.48, font_size=19, mono_cols=())
        tab.next_to(head, DOWN, buff=0.55).set_x(0)
        lines = VGroup(
            wrapped_label(r"walk the import graph of Part 40 backwards from the changed module: \ only tests in that "
                          r"set can be affected", 12.4, font_size=21, color=WHITE),
            wrapped_label(r"a leaf module touches one test file; \ the narration engine, \ caught in Part 40's cycle "
                          r"with the library's root, \ reaches almost everything", 12.4, font_size=21, color=NO),
            wrapped_label(r"Bazel and Google's TAP do this at scale: \ a precise dependency graph is what makes "
                          r"testing every change affordable", 12.4, font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "The other way to make testing affordable is to run only the tests a change could affect. "
            "<bookmark mark='a'/> Walk the import graph of this repository, the one we measured in Part 40, backwards "
            "from the changed module: everything that imports it, directly or indirectly, could behave differently, "
            "and nothing else can. <bookmark mark='b'/> Change the module behind our KWIC experiment, and one test "
            "file must run. Change Pebble's assembler, and twenty-two test modules out of two hundred. Change the "
            "narration engine, caught in Part 40's cycle with the library's root, and the change reaches nearly two "
            "thousand modules and seventy-one test files. <bookmark mark='c'/> Google's test platform and Bazel do "
            "this at enormous scale. A precise dependency graph, and an architecture without needless cycles, is "
            "what makes testing every change affordable."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()

    def trunk(self):
        head = label(r"Trunk-based development", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"everyone commits to one main line, \ in small changes, \ at least daily; \ branches live "
                          r"hours, \ not weeks \ --- \ Part 40's simulation: \ conflicts per week of work grow with a "
                          r"branch's life", 12.4, font_size=22, color=YES),
            wrapped_label(r"\textbf{pre-submit} tests run before a change lands; \ \textbf{post-submit} tests, \ too "
                          r"slow or too broad to run on every change, \ run on the merged result, \ and a failure "
                          r"there is bisected to a culprit", 12.4, font_size=22, color=HEAD),
            wrapped_label(r"\textbf{flaky tests} are the enemy of all of it: \ a 1\% flaky test in a suite of a "
                          r"thousand fails some run almost every time; \ quarantine them, \ fix them, \ never let "
                          r"them block", 12.4, font_size=22, color=NO),
            wrapped_label(r"unfinished features ship dark, \ behind flags \ (Chapter 7), \ rather than on long "
                          r"branches", 12.4, font_size=22, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Merge queues serve a way of working. <bookmark mark='a'/> In trunk-based development everyone commits "
            "to one main line, in small changes, at least daily, and branches live for hours rather than weeks. "
            "Part 40's simulation showed why: conflicts per week of work grow with a branch's lifetime. "
            "<bookmark mark='b'/> Fast tests run before a change lands. Slower and broader ones run after, on the "
            "merged result, and when they fail, the failure is bisected to the change that caused it. "
            "<bookmark mark='c'/> Flaky tests threaten all of it. A suite of a thousand tests, each flaky one percent "
            "of the time independently, fails somewhere on almost every run, and people learn to ignore red. They "
            "must be quarantined and fixed, never allowed to block. <bookmark mark='d'/> And unfinished features "
            "ship switched off, behind flags, instead of living on long branches."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()

    def savings(self):
        s = load("selection")
        head = label(r"How much testing does selection save?", font_size=36).to_edge(UP, buff=0.3)
        top = max(s["hist"])
        bars = VGroup()
        x0, w, hmax, y0 = -6.0, 0.7, 3.4, -2.3
        for i, v in enumerate(s["hist"]):
            hh = max(0.03, hmax * v / top)
            b = Rectangle(width=w * 0.85, height=hh, stroke_width=0, fill_color=YES if i == 0 else HEAD,
                          fill_opacity=0.85).move_to([x0 + i * w, y0 + hh / 2, 0])
            t = label(f"{v}", font_size=15, color=GREY_A).next_to(b, UP, buff=0.05)
            lb = label(f"{i * 10}\\%", font_size=14, color=GREY_B).move_to([x0 + i * w, y0 - 0.22, 0])
            bars.add(VGroup(b, t, lb))
        xl = label(r"share of the test suite a change can affect", font_size=17, color=GREY_A).move_to(
            [x0 + 3.2, y0 - 0.6, 0])
        notes = VGroup(
            label(rf"each of the library's {s['modules']} modules, \ changed in turn", font_size=20, color=GREY_A),
            label(rf"median: \ {s['median'] * 100:.0f}\% of the {s['tests']} test modules", font_size=22,
                  color=YES),
            label(rf"mean: \ {s['mean'] * 100:.1f}\%; \ {s['under_5pct'] * 100:.0f}\% of modules need under 5\%",
                  font_size=20, color=WHITE),
            wrapped_label(r"the cost is a correct graph: \ a dependency that the graph misses \ (a file read at "
                          r"run time, \ a dynamic import) \ is a test that should have run and did not", 5.4,
                          font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.6, 0.3, 0])
        with self.voiceover(
            "How much does selection save in this repository? <bookmark mark='a'/> We changed each of the library's "
            "modules in turn, in imagination, and counted the test modules that could be affected. "
            "<bookmark mark='b'/> For the median module, one percent of the tests. On average, under five percent, "
            "and for nearly three quarters of the modules less than that. A full run is needed only for the few "
            "modules at the root of everything. <bookmark mark='c'/> The saving rests on the graph being right: a "
            "dependency the graph does not see, a file read at run time or an import computed from a string, is a "
            "test that should have run and did not."
        ) as vo:
            self.play(FadeIn(head), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in bars], lag_ratio=0.1), FadeIn(xl))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), FadeIn(notes[2]))
            vo.wait_until("c")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA, KERN, LAM)
