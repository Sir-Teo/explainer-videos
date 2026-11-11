from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs40.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, grid_table, load)


class Mutation(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.result()
        self.survivors()
        self.criteria()

    def card(self):
        card = chapter_card(6, r"Testing the tests", r"How good is a test suite?", lit=(1978, 2011),
                            extra=((1978, r"DeMillo, Lipton and Sayward: \ mutation testing"),
                                   (2011, r"Jia and Harman: \ a survey")), part=PART)
        with self.voiceover("Chapter six. Testing the tests."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def idea(self):
        head = label(r"Mutants", font_size=36).to_edge(UP, buff=0.3)
        orig = code_block(["if op == \".word\":", "    return 4 * len(args)"], size=19)
        mut = code_block(["if op == \".word\":", "    return 5 * len(args)"], size=19, color=NO)
        pair = VGroup(VGroup(label(r"the assembler, \ as written", font_size=19, color=GREY_A), orig).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15), VGroup(label(r"a mutant: \ one constant changed", font_size=19,
                                                              color=NO), mut).arrange(DOWN, aligned_edge=LEFT,
                                                                                      buff=0.15)).arrange(
            RIGHT, buff=1.2).next_to(head, DOWN, buff=0.6)
        lines = VGroup(
            wrapped_label(r"\textbf{coverage} asks which lines the tests ran; \ it cannot tell a test that checks the "
                          r"result from one that only runs the code", 12.4, font_size=22, color=WHITE),
            wrapped_label(r"\textbf{mutation testing} \ (DeMillo, Lipton and Sayward, 1978): \ make many small "
                          r"wrong versions, \ one change each \ (a $<$ for a $\le$, \ a $+$ for a $-$, \ a constant "
                          r"off by one), \ and run the tests on each", 12.4, font_size=22, color=HEAD),
            wrapped_label(r"a mutant the tests reject is \textbf{killed}; \ one they accept \textbf{survives}: \ a "
                          r"wrong program the suite cannot tell apart", 12.4, font_size=22, color=YES),
            wrapped_label(r"some survivors are \textit{equivalent} \ --- \ they behave exactly like the original \ "
                          r"--- \ and deciding which is undecidable \ (Rice, Part 25)", 12.4, font_size=22,
                          color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(pair, DOWN, buff=0.5)
        with self.voiceover(
            "Tests check the code; what checks the tests? <bookmark mark='a'/> The usual answer is coverage: the "
            "fraction of lines the tests run. But running a line is not checking it. A test that calls a function "
            "and ignores the answer covers every line it touches. <bookmark mark='b'/> In 1978 Richard DeMillo, "
            "Richard Lipton and Fred Sayward proposed a sharper measure. Make many small wrong versions of the "
            "program, mutants, each with one deliberate change: a less-than for a less-or-equal, a plus for a minus, "
            "a constant off by one. Then run the tests on each. <bookmark mark='c'/> If the tests fail, the mutant "
            "is killed. If they pass, it survives: a wrong program the suite cannot tell from the right one. "
            "<bookmark mark='d'/> A few survivors are equivalent, behaving exactly as the original does, and deciding "
            "which ones are is, by Rice's theorem from Part 25, undecidable in general."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pair))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()

    def result(self):
        d = load("mutation")
        m, c = d["mutation"], d["coverage"]
        head = label(r"Our assembler, \ measured", font_size=36).to_edge(UP, buff=0.3)
        n = m["mutants"]
        cols = 20
        squares = VGroup()
        surv_lines = [s["line"] for s in m["survivors"]]
        killed = n - len(surv_lines)
        order = [("killed", YES)] * killed + [("survived, line run", NO) if s["covered"] else
                                              ("survived, line never run", KERN) for s in m["survivors"]]
        order = [(k, col) for k, col in order]
        for i, (_, col) in enumerate(order):
            x, y = i % cols, i // cols
            squares.add(Square(0.26, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                [-6.0 + x * 0.32, 2.2 - y * 0.32, 0]))
        key = VGroup(label(rf"killed: \ {killed}", font_size=20, color=YES),
                     label(rf"survived on lines the tests never ran: \ {len(surv_lines) - m['survivors_covered']}",
                           font_size=20, color=KERN),
                     label(rf"survived on lines the tests did run: \ {m['survivors_covered']}", font_size=20,
                           color=NO)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(squares, DOWN, buff=0.35)
        key.align_to(squares, LEFT)
        stats = VGroup(
            label(r"\texttt{explainer/cs/pebble/asm.py} \ against \texttt{tests/test\_cs\_pebble\_core.py}",
                  font_size=18, color=GREY_A),
            label(rf"statement coverage: \ {c['coverage'] * 100:.0f}\%", font_size=26, color=HEAD),
            label(rf"mutation score: \ {m['score'] * 100:.0f}\%", font_size=26, color=NO),
            label(rf"{m['mutants']} mutants, \ one change each", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.4, 1.0, 0])
        with self.voiceover(
            "We turned this on a real module of this repository: the assembler for Pebble, from Part 6, and its "
            "unit tests, which all pass. <bookmark mark='a'/> Our mutation tool rewrote the assembler's syntax tree "
            "one site at a time, comparisons, arithmetic, logic and integer constants, a hundred and forty-six "
            "mutants in all, and ran the tests on each. <bookmark mark='b'/> The tests run seventy-seven percent of "
            "the assembler's statements, which sounds respectable. But they kill only sixty-two percent of the "
            "mutants. <bookmark mark='c'/> Most survivors live on lines the tests never run: error paths and "
            "directives nobody tested. Ten are worse. They change lines the tests do run, and the tests still pass."
        ) as vo:
            self.play(FadeIn(head), FadeIn(stats[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in squares], lag_ratio=0.01), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(stats[1]), FadeIn(stats[3]))
            self.play(FadeIn(stats[2]), FadeIn(key[0]))
            vo.wait_until("c")
            self.play(FadeIn(key[1]), FadeIn(key[2]))
        self.wait(0.4)
        self.clear_scene()

    def survivors(self):
        d = load("mutation")
        m = d["mutation"]
        head = label(r"What the passing tests cannot see", font_size=36).to_edge(UP, buff=0.3)
        picks = [s for s in m["survivors"] if s["covered"]]
        seen, rows = set(), []
        for s in picks:
            if s["line"] in seen:
                continue
            seen.add(s["line"])
            rows.append(s)
        items = VGroup()
        for s in rows[:5]:
            items.add(VGroup(label(rf"line {s['line']}: \ {s['mutation'].replace('->', r'$\to$')}", font_size=19,
                                   color=NO),
                             code_block([s["code"][:70]], size=16)).arrange(DOWN, aligned_edge=LEFT, buff=0.08))
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.7)
        notes = VGroup(
            wrapped_label(r"a \texttt{.word} that reserves 5 bytes instead of 4: \ the tests use \texttt{.word} but "
                          r"never check an address after one", 4.8, font_size=19, color=WHITE),
            wrapped_label(r"\texttt{j} and \texttt{ret} that overwrite the return register: \ no test reads it "
                          r"afterwards", 4.8, font_size=19, color=WHITE),
            wrapped_label(r"each survivor is a test to write: \ assert on the effect, \ not just that the code ran",
                          4.8, font_size=20, color=YES),
            wrapped_label(r"Google runs mutation analysis in code review, \ showing only a few relevant survivors "
                          r"per change \ (Petrovi\'c and Ivankovi\'c, 2018)", 4.8, font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([4.2, -0.2, 0])
        with self.voiceover(
            "The ten are worth reading. <bookmark mark='a'/> One makes a dot-word directive reserve five bytes per "
            "word instead of four. The tests use dot-word, but never check an address that comes after one, so a "
            "broken assembler passes. <bookmark mark='b'/> Others make the jump and return pseudo-instructions "
            "overwrite the return-address register; no test looks at it afterwards. <bookmark mark='c'/> Each "
            "survivor is a missing test, and the remedy is to assert on effects rather than merely run code. "
            "<bookmark mark='d'/> Mutation testing used to be too slow for industry. Google now runs it inside code "
            "review, showing developers a few relevant surviving mutants on each change, and many of them write the "
            "missing test."
        ) as vo:
            self.play(FadeIn(head), FadeIn(items))
            for mk, n in zip("abcd", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n))
        self.wait(0.4)
        self.clear_scene()

    def criteria(self):
        head = label(r"How much testing is enough?", font_size=36).to_edge(UP, buff=0.3)
        code = code_block(["if (altitude_ok and speed_ok) or override:", "    deploy()"], size=20).next_to(
            head, DOWN, buff=0.5)
        rows = [[r"statement", r"every line runs", r"1"],
                [r"branch", r"every decision both ways", r"2"],
                [r"MC/DC", r"each condition shown to flip the decision on its own", r"4 \ ($n + 1$)"],
                [r"all combinations", r"every assignment of the conditions", r"8 \ ($2^n$)"]]
        tab = grid_table([r"criterion", r"requires", r"tests for this line"], rows, widths=[3.0, 6.8, 2.6],
                         row_h=0.5, font_size=20, mono_cols=())
        tab.next_to(code, DOWN, buff=0.45).set_x(0)
        tab.cells[3][0].set_color(HEAD)
        lines = VGroup(
            wrapped_label(r"\textbf{MC/DC} \ (modified condition/decision coverage) \ is required for the most "
                          r"critical airborne software \ (DO-178C, level A): \ linear in the number of conditions, \ "
                          r"yet it exercises each one", 12.4, font_size=21, color=YES),
            wrapped_label(r"coverage measures what was run; \ mutation measures what was checked: \ use the first "
                          r"to find untested code, \ the second to find tests that check nothing", 12.4,
                          font_size=21, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "Coverage criteria form a ladder. <bookmark mark='a'/> Take one line with three conditions. Statement "
            "coverage needs a single test that runs it. Branch coverage needs the decision to go both ways: two "
            "tests. All combinations of the conditions would need eight, and in general two to the n. "
            "<bookmark mark='b'/> Between them sits MC/DC, modified condition and decision coverage: for each "
            "condition, a pair of tests in which only that condition changes and the decision changes with it. That "
            "needs only n plus one tests, here four, yet shows that every condition matters. Aviation's standard "
            "requires it for the most critical flight software. <bookmark mark='c'/> Coverage says what ran; "
            "mutation says what was checked. Use the first to find code nobody tested, and the second to find "
            "tests that check nothing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[0])), Create(tab.rule),
                      *[FadeIn(VGroup(*tab.cells[k])) for k in (1, 2, 4)])
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[3])), FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA, KERN)
