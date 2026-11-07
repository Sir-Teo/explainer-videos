from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs54.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, bar_chart, code_block, load, mono, tag_box

TRIANGLE = ["def triangle(a, b, c):",
            "    if a <= 0 or b <= 0 or c <= 0:",
            "        return \"invalid\"",
            "    if a + b <= c or a + c <= b or b + c <= a:",
            "        return \"invalid\"",
            "    if a == b and b == c:",
            "        return \"equilateral\"",
            "    if a == b or b == c or a == c:",
            "        return \"isosceles\"",
            "    return \"scalene\""]

INSERT = ["def insert(xs, x):          # xs is sorted",
          "    i = 0",
          "    while i < len(xs) - 1 and xs[i] < x:",
          "        i += 1",
          "    return xs[:i] + [x] + xs[i:]"]


def list_boxes(xs, color=DATA, size=20):
    """A Python list drawn as a row of boxes (an empty list as a bracket pair)."""
    if not xs:
        return mono("[]", size=size, color=color)
    return VGroup(*[tag_box(str(v), color=color, size=size, w=0.75, h=0.5) for v in xs]).arrange(RIGHT, buff=0.08)


def py(v) -> str:
    return str(v).replace("'", "")


class Testing(VoiceoverScene):
    def construct(self):
        self.card()
        self.coverage()
        self.blind()
        self.mutation()
        self.properties()
        self.fuzzing()
        self.symbolic()

    def card(self):
        card = chapter_card(13, r"Testing as science", r"What does a passing test tell us?", lit=(1990, 2000),
                            extra=((1990, r"Miller: \ random input to Unix utilities"),
                                   (2000, r"QuickCheck")), part=PART)
        with self.voiceover("Chapter thirteen. Testing as science."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def coverage(self):
        tri = load("coverage")["triangle_random"]
        assert [s.strip() for s in tri["missed_source"]] == ['return "invalid"', 'return "equilateral"']
        head = label(r"Coverage: \ where the tests have been", font_size=36).to_edge(UP, buff=0.3)
        code = code_block(TRIANGLE, size=19).next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.5)
        # the instrument numbers lines from the def, with a docstring on line 1; our listing has no docstring
        missed = {m - 1 for m in tri["missed_lines"]}
        marks = VGroup()
        for k, ln in enumerate(code):
            if k == 0:
                continue
            col = NO if k in missed else YES
            marks.add(Rectangle(width=0.14, height=ln.height + 0.06, stroke_width=0, fill_color=col,
                                fill_opacity=0.9).next_to(code, LEFT, buff=0.12).set_y(ln.get_y()))
        kinds = dict(tri["kinds"])
        names = ["invalid", "scalene", "isosceles", "equilateral"]
        vals = [kinds.get(k, 0) for k in names]
        chart = bar_chart([max(v, 0.001) for v in vals], names, [GREY_B, DATA, LAM, NO], height=2.4, bar_w=0.6,
                          gap=0.5, vmax=max(vals), fmt_=lambda v: f"{v:.0f}", font_size=18)
        chart.move_to([3.9, 0.9, 0])
        cap = label(rf"{tri['tests']} random tests, \ sides 1 to 100", font_size=19, color=GREY_A).next_to(
            chart, UP, buff=0.3)
        stats = VGroup(
            label(rf"lines: \ {tri['lines_hit']} of {tri['lines']} \ ({100 * tri['line_coverage']:.0f}\%)",
                  font_size=21, color=YES),
            label(rf"branch outcomes: \ {tri['branches_hit']} of {tri['branches']} \ "
                  rf"({100 * tri['branch_coverage']:.0f}\%)", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(chart, DOWN, buff=0.45)
        why = wrapped_label(r"no side was ever $\le 0$; \ three equal sides come up once in 10,000 draws", 5.6,
                            font_size=19, color=NO).next_to(stats, DOWN, buff=0.3)
        cite = note(r"Myers, \ \textit{The Art of Software Testing} \ (1979)", font_size=17).next_to(code, DOWN,
                                                                                                buff=0.35)
        cite.align_to(code, LEFT)
        with self.voiceover(
            "Coverage measures where the tests have been. <bookmark mark='a'/> Glenford Myers's triangle classifier, "
            "from his 1979 book on testing, takes three sides and names the triangle. <bookmark mark='b'/> Run three "
            "hundred random tests, with sides from one to a hundred. <bookmark mark='c'/> They reach seven of the "
            "nine lines, and six of the eight branch outcomes. <bookmark mark='d'/> Two lines never ran. No side was "
            "ever zero or negative, and no triangle was equilateral: with random sides, all three agree once in ten "
            "thousand draws. Coverage points at exactly what the tests missed."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(code), FadeIn(cite))
            vo.wait_until("b")
            self.play(FadeIn(cap), FadeIn(chart[0]),
                      LaggedStart(*[AnimationGroup(GrowFromEdge(b, DOWN), FadeIn(v), FadeIn(n))
                                    for b, v, n in zip(chart.bars, chart.vals, chart.names)], lag_ratio=0.3),
                      run_time=2)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.1), FadeIn(stats))
            vo.wait_until("d")
            self.play(*[Indicate(code[k], color=NO) for k in sorted(missed)], FadeIn(why))
        self.wait(0.4)
        self.clear_scene()

    def blind(self):
        ins = load("coverage")["insert_unit"]
        prop = ins["property"]
        assert ins["unit_tests_pass"] and ins["line_coverage"] == 1.0 and not prop["ok"]
        xs, x = prop["shrunk"]
        head = label(r"What coverage cannot see", font_size=36).to_edge(UP, buff=0.3)
        code = code_block(INSERT, size=20).next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.7)
        marks = VGroup(*[Rectangle(width=0.14, height=ln.height + 0.06, stroke_width=0, fill_color=YES,
                                   fill_opacity=0.9).next_to(code, LEFT, buff=0.12).set_y(ln.get_y())
                         for ln in code[1:]])
        units = [([1, 3, 5], 4), ([], 2), ([2, 4], 1)]
        tests = VGroup(*[mono(f"insert({py(a)}, {b}) == {py(sorted(a + [b]))}", size=19, color=WHITE)
                         for a, b in units]).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        ticks = VGroup(*[label(r"pass", font_size=18, color=YES).next_to(t, RIGHT, buff=0.3) for t in tests])
        ut = VGroup(tests, ticks).next_to(code, DOWN, buff=0.5).align_to(code, LEFT)
        cov = label(rf"lines {ins['lines_hit']}/{ins['lines']}, \ branch outcomes {ins['branches_hit']}/"
                    rf"{ins['branches']}: \ 100\% coverage", font_size=21, color=YES).next_to(ut, DOWN, buff=0.35)
        cov.align_to(code, LEFT)
        law = MathTex(r"\mathit{sorted}(\mathit{insert}(xs, x))", r"\;\wedge\;",
                      r"\mathit{insert}(xs, x) \sim xs + [x]", font_size=28, color=HEAD)
        lawl = label(r"the property: \ ordered, \ and the right elements", font_size=18, color=HEAD)
        got = buggy_insert(xs, x)
        ce = VGroup(label(rf"fails on random input {prop['trials']}: \ {py(prop['original'])}", font_size=19,
                          color=NO),
                    label(rf"shrunk: \ \texttt{{insert({py(xs)}, {x})}} returns \texttt{{{py(got)}}}", font_size=21,
                          color=NO))
        right = VGroup(law, lawl, ce.arrange(DOWN, buff=0.2, aligned_edge=LEFT)).arrange(DOWN, buff=0.25)
        right.to_edge(DOWN, buff=0.45).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Full coverage proves less than it seems. <bookmark mark='a'/> This insert puts a number into a sorted "
            "list, and its scan stops one element early. <bookmark mark='b'/> Three unit tests pass, <bookmark "
            "mark='c'/> and between them they run every line and both outcomes of the loop test: full coverage. "
            "<bookmark mark='d'/> A property test checks that the output is ordered and holds the right elements. It "
            "fails on its ninth random input, shrunk to inserting one into the list holding zero, and the answer "
            "comes out one, zero. Coverage says where tests have been, not that what they saw was right."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(code))
            self.play(Indicate(code[2], color=NO))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(t), FadeIn(k)) for t, k in zip(tests, ticks)],
                                  lag_ratio=0.4))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.15), FadeIn(cov))
            vo.wait_until("d")
            self.play(FadeIn(law), FadeIn(lawl))
            self.play(FadeIn(ce[0]))
            self.play(FadeIn(ce[1]))
        self.wait(0.4)
        self.clear_scene()

    def mutation(self):
        head = label(r"Testing the tests: \ mutation", font_size=36).to_edge(UP, buff=0.3)
        orig = mono("while i < len(xs) and xs[i] < x:", size=20, color=WHITE)
        ol = label(r"the correct loop test", font_size=18, color=GREY_A)
        og = VGroup(orig, ol).arrange(RIGHT, buff=0.4).next_to(head, DOWN, buff=0.4)
        # worked by hand against the three unit tests of the last slide
        muts = [("i < len(xs) - 1", r"survives: \ it \textit{is} the bug of the last slide", NO),
                ("xs[i] <= x", r"survives, \ but \textbf{equivalent}: \ no test can kill it", GREY_B),
                ("xs[i] > x", r"\textbf{killed} by 2 of the 3 tests", YES),
                ("i += 2", r"survives; \ \texttt{insert([1, 3], 2)} would kill it", NO)]
        rows = VGroup()
        for k, (m, verdict, col) in enumerate(muts):
            tag = label(rf"M{k + 1}", font_size=19, color=HEAD)
            code = mono(m, size=20, color=col)
            v = label(verdict, font_size=19, color=col)
            rows.add(VGroup(tag, code, v))
        for r in rows:
            r[1].next_to(r[0], RIGHT, buff=0.35)
            r[2].next_to(r[1], RIGHT, buff=0.5)
        rows.arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(og, DOWN, buff=0.5).to_edge(LEFT, buff=0.8)
        vx = max(r[1].get_right()[0] for r in rows) + 0.5
        for r in rows:
            r[2].next_to(r[1], RIGHT, buff=0.5).set_x(vx, direction=LEFT)
        score = VGroup(
            MathTex(r"\text{score}", r"=", r"\frac{\text{killed}}{\text{mutants} - \text{equivalent}}", font_size=32),
            MathTex(r"\text{score}", r"=", r"\frac{1}{4 - 1}", font_size=32),
            MathTex(r"\text{score}", r"=", r"\frac{1}{3}", font_size=32, color=NO),
        ).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.75)
        ill = note(r"illustrative: \ four mutants, \ worked by hand against the three unit tests", font_size=17
                   ).to_edge(DOWN, buff=0.2)
        cite = note(r"DeMillo, \ Lipton and Sayward \ (1978)", font_size=17).next_to(og, DOWN, buff=0.08)
        with self.voiceover(
            "Mutation testing, proposed by Richard DeMillo, Richard Lipton and Frederick Sayward in 1978, asks "
            "whether the tests would notice a bug. <bookmark mark='a'/> Make small changes to the correct program: "
            "each is a mutant. <bookmark mark='b'/> Stopping the scan one early survives the unit tests; it is the "
            "very bug they missed. <bookmark mark='c'/> Less-or-equal survives too, but no test could kill it: "
            "inserting before or after an equal element gives the same list. It is an equivalent mutant. <bookmark "
            "mark='d'/> Greater-than is killed by two tests. <bookmark mark='e'/> Stepping by two survives. <bookmark"
            " mark='f'/> The score is killed over non-equivalent mutants: one in three. The tests are weak, and now "
            "we know where."
        ) as vo:
            self.play(FadeIn(head), FadeIn(og), FadeIn(cite), FadeIn(ill))
            for k, mk in enumerate("abcde"):
                vo.wait_until(mk)
                if k == 0:
                    self.play(*[FadeIn(r[0]) for r in rows], *[FadeIn(r[1], shift=RIGHT * 0.2) for r in rows])
                else:
                    self.play(FadeIn(rows[k - 1][2]))
            self.play(FadeIn(rows[3][2]))
            vo.wait_until("f")
            self.play(FadeIn(score[0]))
            self.play(TransformMatchingTex(score[0].copy(), score[1]))
            self.play(TransformMatchingTex(score[1].copy(), score[2]))
        self.wait(0.4)
        self.clear_scene()

    def properties(self):
        r = load("pbt")["sort_dedup"]
        assert not r["ok"]
        steps = r["steps"]
        head = label(r"Properties, \ and shrinking", font_size=36).to_edge(UP, buff=0.3)
        law = MathTex(r"\forall xs.\ ", r"\mathit{ordered}(\mathit{sort}(xs))", r"\;\wedge\;",
                      r"\mathit{sort}(xs) \sim xs", font_size=34, color=HEAD).next_to(head, DOWN, buff=0.4)
        lawl = label(r"a law, \ not an example: \ in order, \ and a rearrangement of the input", font_size=19,
                     color=HEAD).next_to(law, DOWN, buff=0.12)
        impl = mono("def sort(xs): return sorted(set(xs))", size=20, color=WHITE).next_to(lawl, DOWN, buff=0.35)
        cur = list_boxes(steps[0], NO).move_to([0, -0.4, 0])
        cl = label(rf"random input {r['trials']} fails", font_size=19, color=NO).next_to(cur, DOWN, buff=0.25)
        labels_ = [r"remove the first element: \ still fails", r"remove the last: \ still fails",
                   r"shrink both copies toward zero together: \ still fails"]
        hist = VGroup(*[list_boxes(s, GREY_B, size=18) for s in steps[:-1]]).arrange(RIGHT, buff=0.5)
        hist.to_edge(DOWN, buff=1.1)
        hl = label(r"the shrinking steps", font_size=17, color=GREY_B).next_to(hist, UP, buff=0.15)
        out = label(rf"{r['candidates_tried']} candidates tried: \ \texttt{{sort({py(steps[-1])})}} returns "
                    rf"\texttt{{{py(sorted(set(steps[-1])))}}}: \ the duplicate is lost", font_size=21,
                    color=YES).to_edge(DOWN, buff=0.4)
        cite = note(r"Claessen and Hughes, \ QuickCheck \ (2000)", font_size=17).to_corner(UR, buff=0.35)
        assert len(steps) == 4
        with self.voiceover(
            "Property-based testing replaces examples with laws; Koen Claessen and John Hughes's QuickCheck made it "
            "practical in 2000. <bookmark mark='a'/> The law for a sort: the output is in order, and rearranges the "
            "input. <bookmark mark='b'/> Random lists come small ones first. This sort goes through a set, and the "
            "twenty-seventh list breaks it: three, minus three, minus three, one. <bookmark mark='c'/> Then it "
            "shrinks. Without the three, still failing. <bookmark mark='d'/> Without the one, still failing. "
            "<bookmark mark='e'/> Both copies of minus three move toward zero together: zero, zero. <bookmark "
            "mark='f'/> After eleven candidates the report is the smallest failing case: sorting zero, zero returns "
            "one zero."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite))
            vo.wait_until("a")
            self.play(FadeIn(law), FadeIn(lawl))
            vo.wait_until("b")
            self.play(FadeIn(impl))
            self.play(FadeIn(cur, shift=UP * 0.2), FadeIn(cl))
            self.play(FadeIn(hl))
            for k, mk in enumerate("cde"):
                vo.wait_until(mk)
                nxt = list_boxes(steps[k + 1], NO).move_to(cur)
                cap = label(labels_[k], font_size=19, color=GREY_A).move_to(cl)
                self.play(FadeIn(hist[k]), ReplacementTransform(cur, nxt), Transform(cl, cap))
                cur = nxt
            vo.wait_until("f")
            self.play(FadeIn(out), Transform(cur, list_boxes(steps[-1], YES).move_to(cur)))
        self.wait(0.4)
        self.clear_scene()

    def fuzzing(self):
        head = label(r"Coverage-guided fuzzing", font_size=36).to_edge(UP, buff=0.3)
        code = code_block(["if buf[0] == 'F':", "    if buf[1] == 'U':", "        if buf[2] == 'Z':",
                           "            crash()"], size=20)
        code.next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.6)
        ill = note(r"illustrative", font_size=17).next_to(code, DOWN, buff=0.15).align_to(code, LEFT)
        rnd = MathTex(r"P(\text{reach}) = 256^{-3}", r"=", r"1/16{,}777{,}216", font_size=30, color=NO)
        rndl = label(r"pure random bytes: \ all three at once", font_size=18, color=NO)
        rg = VGroup(rnd, rndl).arrange(DOWN, buff=0.1).next_to(ill, DOWN, buff=0.45).align_to(code, LEFT)
        # the corpus: inputs kept because each reached a new branch
        corpus = [("AAAA", 0), ("FAAA", 1), ("FUAA", 2), ("FUZA", 3)]
        chips = VGroup(*[tag_box(s, color=[GREY_B, DATA, LAM, NO][d], size=20, w=1.4, h=0.55) for s, d in corpus])
        chips.arrange(RIGHT, buff=0.55).move_to([2.9, 1.4, 0])
        arr = VGroup(*[Arrow(chips[k].get_right(), chips[k + 1].get_left(), buff=0.06, color=GREY_B,
                             stroke_width=2, max_tip_length_to_length_ratio=0.25) for k in range(3)])
        tags = VGroup(*[label(t, font_size=16, color=GREY_A).next_to(c, DOWN, buff=0.12)
                        for t, c in zip([r"seed", r"new branch", r"new branch", r"crash"], chips)])
        cl = label(r"the corpus: \ inputs kept because they reached a new branch", font_size=18,
                   color=HEAD).next_to(chips, UP, buff=0.3)
        tries = MathTex(r"\approx 3 \times 256", r"\text{ tries}", font_size=30, color=YES).next_to(tags, DOWN,
                                                                                                   buff=0.4)
        tl = label(r"one byte at a time: \ each found by mutating the last kept input", font_size=18,
                   color=YES).next_to(tries, DOWN, buff=0.1)
        notes = wrapped_label(r"Miller \ (1990): \ random input crashed or hung about a quarter to a third of Unix "
                              r"utilities. \ AFL \ (Zalewski, \ 2013) \ added branch coverage as the guide; \ "
                              r"OSS-Fuzz \ (Google, \ 2016) \ runs fuzzers on open-source projects continuously", 6.0,
                              font_size=19, color=GREY_A).next_to(tl, DOWN, buff=0.5)
        notes.align_to(chips, LEFT)
        if notes.get_right()[0] > 6.85:
            notes.shift(LEFT * (notes.get_right()[0] - 6.85))
        with self.voiceover(
            "In 1990 Barton Miller's students fed random characters to Unix utilities, and crashed or hung about a "
            "quarter to a third of them. <bookmark mark='a'/> But pure random input rarely gets deep. To reach this "
            "crash it must guess three bytes at once, about one chance in seventeen million. <bookmark mark='b'/> "
            "Michał Zalewski's American Fuzzy Lop, in 2013, watches which branches each input takes. <bookmark "
            "mark='c'/> An input that reaches a new branch is kept, and mutated further. The F is found, then the U, "
            "then the Z, a few hundred tries each. <bookmark mark='d'/> Since 2016 Google's OSS-Fuzz has run such "
            "fuzzers continuously on open-source projects."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(rg))
            vo.wait_until("b")
            self.play(FadeIn(cl), FadeIn(chips[0]), FadeIn(tags[0]))
            vo.wait_until("c")
            for k in range(3):
                self.play(GrowArrow(arr[k]), FadeIn(chips[k + 1]), FadeIn(tags[k + 1]),
                          Indicate(code[k], color=[DATA, LAM, NO][k]), run_time=0.9)
            self.play(FadeIn(tries), FadeIn(tl))
            vo.wait_until("d")
            self.play(FadeIn(notes))
        self.wait(0.4)
        self.clear_scene()

    def symbolic(self):
        head = label(r"Symbolic and concolic execution", font_size=36).to_edge(UP, buff=0.3)
        conds = ["a<=0 or b<=0 or c<=0", "a+b<=c or a+c<=b or b+c<=a", "a==b and b==c", "a==b or b==c or a==c"]
        leaves = ["invalid", "invalid", "equilateral", "isosceles"]
        ds = VGroup(*[tag_box(c, color=GREY_B, size=16, h=0.5) for c in conds]).arrange(DOWN, buff=0.45)
        ds.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.5)
        for d in ds:
            d.align_to(ds, LEFT)
        lv = VGroup(*[tag_box(t, color=NO if t == "invalid" else (YES if t == "equilateral" else LAM), size=16,
                              h=0.45) for t in leaves])
        for leaf, d in zip(lv, ds):
            leaf.next_to(d, RIGHT, buff=0.7).set_x(ds.get_right()[0] + 0.8, direction=LEFT)
        last = tag_box("scalene", color=LAM, size=16, h=0.45).next_to(ds[-1], DOWN, buff=0.45).align_to(ds, LEFT)
        t_arr = VGroup(*[Arrow(d.get_right(), leaf.get_left(), buff=0.06, color=GREY_B, stroke_width=1.8,
                               max_tip_length_to_length_ratio=0.2) for d, leaf in zip(ds, lv)])
        xl = ds.get_left()[0] + 0.45
        f_arr = VGroup(*[Arrow([xl, ds[k].get_bottom()[1], 0], [xl, (ds[k + 1] if k < 3 else last).get_top()[1], 0],
                               buff=0.05, color=GREY_B, stroke_width=1.8, max_tip_length_to_length_ratio=0.3)
                         for k in range(4)])
        tf = VGroup(label(r"true $\rightarrow$", font_size=16, color=GREY_B).next_to(t_arr[0], UP, buff=0.05),
                    label(r"false $\downarrow$", font_size=16, color=GREY_B).next_to(f_arr[0], RIGHT, buff=0.1))
        pcs = VGroup(MathTex(r"\neg(a \le 0 \vee b \le 0 \vee c \le 0)", font_size=28),
                     MathTex(r"\wedge\ \neg(a + b \le c \vee a + c \le b \vee b + c \le a)", font_size=28),
                     MathTex(r"\wedge\ a = b \wedge b = c", font_size=28)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        pcl = label(r"the path condition for \texttt{equilateral}", font_size=19, color=HEAD)
        pg = VGroup(pcl, pcs).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([3.4, 1.4, 0])
        if pg.get_right()[0] > 6.85:
            pg.shift(LEFT * (pg.get_right()[0] - 6.85))
        simp = MathTex(r"a = b = c", r"\;\wedge\;", r"a > 0", font_size=32, color=YES)
        model = MathTex(r"\text{solver: } a = b = c = 1", font_size=32, color=YES)
        sg = VGroup(simp, model).arrange(DOWN, buff=0.25).next_to(pg, DOWN, buff=0.4)
        sl = label(r"the test that 300 random ones missed", font_size=18, color=YES).next_to(sg, DOWN, buff=0.1)
        notes = wrapped_label(r"KLEE \ (Cadar, \ Dunbar and Engler, \ 2008): \ symbolic execution of real C "
                              r"programs; \ DART \ (2005): \ \textbf{concolic}, \ run concretely, \ then solve for the "
                              r"branch not taken. \ The limit: \ paths multiply with every branch and loop", 5.6,
                              font_size=19, color=GREY_A).next_to(sl, DOWN, buff=0.35)
        notes.align_to(pg, LEFT)
        if notes.get_right()[0] > 6.85:
            notes.shift(LEFT * (notes.get_right()[0] - 6.85))
        with self.voiceover(
            "Symbolic execution runs the program on symbols instead of numbers. <bookmark mark='a'/> At each branch "
            "the path splits, and each path collects a condition. <bookmark mark='b'/> To reach equilateral, no side "
            "may be zero or negative, <bookmark mark='c'/> the sides must make a real triangle, <bookmark mark='d'/> "
            "and they must be equal. <bookmark mark='e'/> Simplified: three equal, positive sides. A solver returns "
            "one, one, one, the test that three hundred random ones missed. <bookmark mark='f'/> KLEE, in 2008, did "
            "this for real C programs. Concolic testing, from DART in 2005, runs concretely, then solves for the "
            "branch not taken. The limit is the number of paths, which multiplies with every branch and loop."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in ds], lag_ratio=0.2), Create(f_arr), Create(t_arr),
                      FadeIn(lv), FadeIn(last), FadeIn(tf), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(pcl), FadeIn(pcs[0]), f_arr[0].animate.set_color(HEAD), ds[0][0].animate.set_stroke(HEAD))
            vo.wait_until("c")
            self.play(FadeIn(pcs[1]), f_arr[1].animate.set_color(HEAD), ds[1][0].animate.set_stroke(HEAD))
            vo.wait_until("d")
            self.play(FadeIn(pcs[2]), t_arr[2].animate.set_color(YES), ds[2][0].animate.set_stroke(HEAD),
                      Indicate(lv[2], color=YES))
            vo.wait_until("e")
            self.play(ReplacementTransform(pcs.copy(), simp))
            self.play(FadeIn(model), FadeIn(sl))
            vo.wait_until("f")
            self.play(FadeIn(notes))
        self.wait(0.4)
        self.clear_scene()


def buggy_insert(xs, x):
    """The insert on screen (Part 54's ``testing.buggy_insert``), to print what it returns."""
    i = 0
    while i < len(xs) - 1 and xs[i] < x:
        i += 1
    return xs[:i] + [x] + xs[i:]


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
