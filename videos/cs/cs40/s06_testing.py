from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs40.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load)


class Testing(VoiceoverScene):
    def construct(self):
        self.card()
        self.pyramid()
        self.flaky()
        self.bisect()
        self.fuzz()

    def card(self):
        card = chapter_card(5, r"Testing, \ and tests that lie", r"When a test fails, what has gone wrong?",
                            lit=(2009, 2016), extra=((2009, r"Cohn: \ the test pyramid"),
                                                     (2014, r"Luo et al.: \ flaky tests"),
                                                     (2016, r"Micco: \ flakiness at Google")), part=PART)
        with self.voiceover("Chapter five. Testing, and tests that lie."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def pyramid(self):
        head = label(r"The test pyramid", font_size=36).to_edge(UP, buff=0.3)
        levels = [(r"end-to-end: \ the whole system, \ as a user", NO, 2.6),
                  (r"integration: \ several modules, \ real dependencies", HEAD, 4.6),
                  (r"unit: \ one module, \ milliseconds each", YES, 6.6)]
        tiers = VGroup()
        for i, (t, c, w) in enumerate(levels):
            tr = Polygon([-w / 2, 0, 0], [w / 2, 0, 0], [w / 2 - 1.0, 1.0, 0], [-w / 2 + 1.0, 1.0, 0],
                         stroke_color=c, stroke_width=2, fill_color=c, fill_opacity=0.15)
            tr.move_to([-2.8, 1.4 - i * 1.1, 0])
            lb = label(t, font_size=17, color=WHITE).move_to(tr)
            if lb.width > w - 0.6:
                lb.scale_to_fit_width(w - 0.6)
            tiers.add(VGroup(tr, lb))
        notes = VGroup(
            wrapped_label(r"many fast, \ focused tests at the bottom; \ few slow, \ broad ones at the top \ (Cohn, "
                          r"2009)", 5.0, font_size=20, color=WHITE),
            wrapped_label(r"\textbf{test doubles} \ stand in for dependencies: \ a \textit{fake} works "
                          r"\ (an in-memory database), \ a \textit{stub} returns canned answers, \ a \textit{mock} "
                          r"checks that it was called", 5.0, font_size=20, color=LAM),
            wrapped_label(r"the trade-off: \ doubles make tests fast and deterministic, \ and can drift from the "
                          r"real thing they replace", 5.0, font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Tests are how a team keeps an interface from silently changing. <bookmark mark='a'/> Mike Cohn's "
            "pyramid says how to spend them: many small unit tests that each check one module in milliseconds, fewer "
            "integration tests that wire real modules together, and a handful of end-to-end tests that drive the "
            "whole system as a user would. <bookmark mark='b'/> To test a module alone, its dependencies are "
            "replaced by doubles: a fake actually works, like an in-memory database; a stub returns canned answers; "
            "a mock records how it was called. <bookmark mark='c'/> Doubles make tests fast and repeatable, at a "
            "price: they can drift away from the real thing they imitate."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in reversed(tiers)], lag_ratio=0.3),
                      FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def flaky(self):
        f = load("flaky")
        head = label(r"Flaky tests", font_size=36).to_edge(UP, buff=0.3)
        rows = [[rf"\texttt{{{r['test'].replace('_', chr(92) + '_')}}}", r["kind"], f"{r['fail_rate'] * 100:.1f}\\%",
                 f"{r['isolated_fail_rate'] * 100:.1f}\\%"] for r in f["rows"]]
        tab = grid_table([r"test", r"cause", r"fails in suite", r"fails alone"], rows, widths=[3.6, 3.6, 2.0, 1.9],
                         row_h=0.4, font_size=18, mono_cols=())
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        for k in range(1, len(rows) + 1):
            tab.cells[k][2].set_color(NO)
        stats = VGroup(
            label(rf"{f['tests']} tests, \ {len(f['rows'])} of them flaky, \ {f['runs']} runs in random orders: \ "
                  rf"{f['red_runs'] * 100:.0f}\% of runs red", font_size=21, color=NO),
            label(rf"re-run each failure {f['retries']} more times: \ still red in {f['red_after_retry'] * 100:.0f}\% "
                  r"--- \ and the order bug now hides", font_size=21, color=HEAD),
            label(r"Google, \ 2016: \ about 1.5\% of all test runs flaky; \ almost 16\% of tests flaky at some time",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A flaky test passes and fails on the same code. Qingzhou Luo and colleagues studied hundreds of them in "
            "open-source projects and found the usual causes: waiting a fixed time for something asynchronous, "
            "tests that depend on the order they run in, time and dates, and assuming an order for unordered "
            "collections. <bookmark mark='a'/> We planted eight such tests among a hundred and eighty-one sound ones "
            "and ran the suite four hundred times in random orders. The victim of a polluted cache fails more than "
            "half the time in the suite and never alone; the test that needs a setter fails half the time in the "
            "suite and always alone. <bookmark mark='b'/> Eight flaky tests out of a hundred and eighty-nine turned "
            "more than four runs in five red. Automatic re-runs hide some failures, including the order bug, and "
            "teach everyone to ignore red. <bookmark mark='c'/> At Google's scale, John Micco reported in 2016 that "
            "about one and a half percent of all test runs were flaky, and almost one test in six had been flaky "
            "at some time."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(stats[0]), FadeIn(stats[1]))
            vo.wait_until("c")
            self.play(FadeIn(stats[2]))
        self.wait(0.4)
        self.clear_scene()

    def bisect(self):
        p = load("polluter")
        head = label(r"Finding the polluter", font_size=36).to_edge(UP, buff=0.3)
        n = p["before"]
        x0, w = -6.0, 11.6
        bar = Rectangle(width=w, height=0.35, stroke_color=GREY_C, stroke_width=1).move_to([x0 + w / 2, 1.6, 0])
        cap = label(rf"the {n} tests that ran before the victim failed", font_size=19, color=GREY_A).next_to(
            bar, UP, buff=0.15)
        steps = VGroup()
        lo, hi = 0.0, 1.0
        y = 1.0
        rng_choice = [0, 1, 0, 1, 1, 0, 0]
        for k in range(p["steps"]):
            mid = (lo + hi) / 2
            keep = (lo, mid) if rng_choice[k % len(rng_choice)] == 0 else (mid, hi)
            seg = Rectangle(width=max(0.05, (keep[1] - keep[0]) * w), height=0.22, stroke_width=0,
                            fill_color=HEAD, fill_opacity=0.8).move_to([x0 + (keep[0] + keep[1]) / 2 * w, y, 0])
            steps.add(seg)
            lo, hi = keep
            y -= 0.32
        found = label(rf"\texttt{{{p['found'].replace('_', chr(92) + '_')}}}, \ after {p['steps']} runs of half the "
                      r"list plus the victim", font_size=21, color=YES).next_to(steps, DOWN, buff=0.3)
        foot = VGroup(
            wrapped_label(r"$\lceil \log_2 n \rceil$ runs instead of $n$: \ Part 16's binary search, \ applied to "
                          r"a suite \ (iDFlakies, \ Lam et al., 2019)", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"the fixes are boring: \ reset shared state in every test, \ wait for conditions instead "
                          r"of fixed times, \ inject the clock, \ sort before comparing", 12.4, font_size=20,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "When a test fails only after others, which one is to blame? <bookmark mark='a'/> In one failing order, "
            "a hundred and fifty-nine tests ran before the victim. <bookmark mark='b'/> Run the first half of them "
            "followed by the victim. If it still fails, the polluter is in that half; otherwise in the other. "
            "Halve again. <bookmark mark='c'/> Seven runs instead of a hundred and fifty-nine, and the culprit is "
            "the test that leaves an administrator in the shared cache: Part 16's binary search, applied to a test "
            "suite. <bookmark mark='d'/> The fixes are boring and effective: reset shared state in every test, wait "
            "for conditions rather than fixed times, inject the clock, and sort before comparing."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(bar), FadeIn(cap))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s) for s in steps], lag_ratio=0.35), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(found), FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.wait(0.4)
        self.clear_scene()

    def fuzz(self):
        f = load("fuzz")
        head = label(r"Random inputs: \ fuzzing", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r["error"], rf"\texttt{{{r['example'].replace('_', chr(92) + '_')}}}", f"{r['count']:,}"]
                for r in f["rows"][:6]]
        tab = grid_table([r"crash", r"smallest input", r"times hit"], rows, widths=[3.2, 4.0, 2.0], row_h=0.44,
                         font_size=19, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.6)
        for k in range(1, len(rows) + 1):
            tab.cells[k][0].set_color(NO)
        stats = VGroup(
            label(rf"{f['trials']:,} random programs", font_size=21, color=WHITE),
            label(rf"accepted: \ {f['accepted']:,}", font_size=20, color=YES),
            label(rf"rejected with a clean error: \ {f['rejected']:,}", font_size=20, color=HEAD),
            label(rf"crashed: \ {f['crashed']:,}", font_size=20, color=NO),
            label(rf"at {f['sites']} different places", font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.6, 1.0, 0])
        lines = VGroup(
            wrapped_label(r"the assembler's contract: \ assemble the program, \ or raise \texttt{AsmError} naming the "
                          r"line; \ a missing operand instead raises Python's \texttt{IndexError} from deep inside", 12.4,
                          font_size=20, color=WHITE),
            wrapped_label(r"every unit test passes; \ none had tried \texttt{add} with no operands \ --- \ fuzzing "
                          r"\ (Miller, 1990) \ finds the inputs nobody thought to write, \ and coverage-guided fuzzers "
                          r"like AFL and libFuzzer have found thousands of security bugs", 12.4, font_size=20,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Tests check the inputs someone thought of. Fuzzing tries the ones nobody did. "
            "<bookmark mark='a'/> In 1990 Barton Miller fed random characters to Unix utilities and crashed about a "
            "quarter of them. We did the same to Pebble's assembler, with a little more care: twenty thousand random "
            "programs built from real instruction names and operand shapes. <bookmark mark='b'/> Its contract is to "
            "assemble the program or reject it with an error naming the line. Most programs were rejected cleanly. "
            "But more than seven thousand crashed, at twenty-four different places in the code. "
            "<bookmark mark='c'/> The smallest examples are embarrassing: an add with no operands, a dot-equ with "
            "nothing after it. Instead of a clean error, Python raises an index error from deep inside the "
            "assembler. Every unit test passes; none of them tried this. <bookmark mark='d'/> Coverage-guided "
            "fuzzers such as AFL and libFuzzer steer the random inputs toward code not yet reached, and have found "
            "thousands of security bugs in widely used software."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(stats[0]))
            vo.wait_until("b")
            self.play(FadeIn(stats[1:]), FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(tab))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA, KERN)
