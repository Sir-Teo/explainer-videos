from __future__ import annotations

from videos.philosophy.philosophy33.common import *  # noqa: F403


def box(w, h, col, txt, fs=20, opaque=False):
    r = Rectangle(width=w, height=h, color=col, fill_opacity=0.85 if opaque else 0.08, stroke_width=3)
    return VGroup(r, label(txt, font_size=fs, color=WHITE if opaque else col).move_to(r))


class Newcomb(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"Newcomb's problem", r"Should you take the money that is certainly there?",
                            lit=(1969,), part=PART)
        with self.voiceover("Chapter ten. Newcomb's problem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.story()
        self.arguments()
        self.accuracy()
        self.simulated()
        self.price()

    def story(self):
        hc = history_card(1969, r"Robert Nozick, \ after William Newcomb",
                          r"``Newcomb's Problem and Two Principles of Choice''", width=6.6, color=HIST).to_corner(
            UL, buff=0.3)
        clear = box(2.4, 1.8, MONEY, r"\$1,000", fs=24).move_to([-2.4, -0.6, 0])
        opaque = box(2.4, 1.8, GREY_D, r"?", fs=40, opaque=True).move_to([1.0, -0.6, 0])
        cl = label(r"clear box: \ always \$1,000", font_size=18, color=MONEY).next_to(clear, DOWN, buff=0.2)
        ol = label(r"opaque box: \ \$1,000,000 or nothing", font_size=18, color=GREY_A).next_to(opaque, DOWN,
                                                                                               buff=0.2)
        pred = VGroup(Circle(radius=0.55, color=AGENT, fill_opacity=0.15), label(r"predictor", font_size=16,
                                                                                 color=AGENT)).move_to([4.6, -0.6, 0])
        pred[1].next_to(pred[0], DOWN, buff=0.12)
        eye = VGroup(Ellipse(width=0.7, height=0.36, color=AGENT), Dot(radius=0.09, color=AGENT)).move_to(pred[0])
        rule = stack([(r"yesterday the predictor filled the opaque box with \$1,000,000 \ if and only if it predicted "
                       r"you would take only that box", AGENT),
                      (r"it has been right about almost everyone before you", GREY_A),
                      (r"you may take the opaque box alone, \ or both", GOAL)], font_size=19, buff=0.22).to_edge(
            DOWN, buff=0.35)
        with self.voiceover(
            "In 1969 Robert Nozick published a puzzle devised by the physicist William Newcomb. "
            "<bookmark mark='a'/>In front of you are two boxes. The clear one holds a thousand dollars. The opaque "
            "one holds either a million dollars or nothing. <bookmark mark='b'/>Yesterday a predictor filled the "
            "opaque box: with the million if it predicted that you would take only the opaque box, with nothing if "
            "it predicted you would take both. <bookmark mark='c'/>It has predicted the choices of many people "
            "before you, and has almost always been right. <bookmark mark='d'/>You may take the opaque box alone, or "
            "both boxes. Nozick wrote that almost everyone finds the answer perfectly obvious; the difficulty is "
            "that they divide almost evenly about what it is."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(clear), FadeIn(cl), FadeIn(opaque), FadeIn(ol))
            vo.wait_until("b")
            self.play(FadeIn(pred), FadeIn(eye), FadeIn(rule[0]))
            vo.wait_until("c")
            self.play(FadeIn(rule[1]), Indicate(eye, color=WHITE))
            vo.wait_until("d")
            self.play(FadeIn(rule[2]))
        self.clear_scene()

    def arguments(self):
        head = label(r"Two arguments, \ both valid-looking", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"", r"\text{million in the box}", r"\text{box empty}"]
        cells = [[label(r"one box", font_size=20, color=EVID), label(r"\$1,000,000", font_size=19),
                  label(r"\$0", font_size=19)],
                 [label(r"two boxes", font_size=20, color=CAUSE), label(r"\$1,001,000", font_size=19),
                  label(r"\$1,000", font_size=19)]]
        grid = ValueGrid(hd, cells, col_w=[2.2, 3.2, 2.4], cell_h=0.65, font_size=19).move_to([-2.6, 0.9, 0])
        dom = VGroup(SurroundingRectangle(grid.cell[1][1], color=CAUSE, buff=0.06),
                     SurroundingRectangle(grid.cell[1][2], color=CAUSE, buff=0.06))
        dl = stack([(r"dominance:", CAUSE), (r"the contents are already fixed; \ whatever they are, \ two boxes "
                                             r"give \$1,000 more", GREY_A)], font_size=19, aligned_edge=LEFT,
                   width=4.6, buff=0.15).move_to([3.8, 1.0, 0])
        f1 = MathTex(r"\mathbb{E}[\text{one} \mid \text{one}] = 0.99 \times 1{,}000{,}000 = 990{,}000", font_size=28,
                     color=EVID)
        f2 = MathTex(r"\mathbb{E}[\text{two} \mid \text{two}] = 0.01 \times 1{,}000{,}000 + 1{,}000 = 11{,}000",
                     font_size=28, color=EVID)
        fs = VGroup(f1, f2).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([-1.2, -1.6, 0])
        el = stack([(r"expected value:", EVID), (r"with a 99\% predictor, \ one-boxers get rich", GREY_A)],
                   font_size=19, aligned_edge=LEFT, width=3.4, buff=0.15).move_to([4.8, -1.6, 0])
        with self.voiceover(
            "Two arguments, each of which looks decisive. <bookmark mark='a'/>The first is dominance. The money is "
            "already in the box or it is not; your choice cannot change that now. If the million is there, two "
            "boxes give you a million and a thousand rather than a million. If it is not, two boxes give a thousand "
            "rather than nothing. Whatever the state, two boxes are better by a thousand dollars. "
            "<bookmark mark='b'/>The second is expected value. If the predictor is right ninety nine times in a "
            "hundred, then those who take one box nearly always find a million, an expectation of nine hundred and "
            "ninety thousand dollars; those who take both nearly always find the opaque box empty, an expectation of "
            "eleven thousand. <bookmark mark='c'/>Dominance says take both. Expected value says take one. Both are "
            "principles of chapter three's theory; here they disagree."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            self.play(*[FadeIn(c) for row in grid.cell for c in row])
            vo.wait_until("a")
            self.play(Create(dom), FadeIn(dl))
            vo.wait_until("b")
            self.play(Write(f1), Write(f2), FadeIn(el))
            vo.wait_until("c")
            self.play(Indicate(dl[0], color=WHITE), Indicate(el[0], color=WHITE))
        self.clear_scene()

    def accuracy(self):
        d = load("newcomb")
        head = label(r"A predictor of any accuracy", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["threshold"] == 0.5005
        rows = d["rows"]
        assert [r["p"] for r in rows] == [0.5, 0.5005, 0.6, 0.9, 0.99]
        hd = [r"\text{accuracy } p", r"\mathbb{E}[\text{one box}]", r"\mathbb{E}[\text{two boxes}]"]
        cells = []
        for r in rows:
            better = r["one"] > r["two"]
            cells.append([label(f"{r['p']:g}", font_size=20, color=AGENT),
                          label(f"\\${r['one']:,.0f}", font_size=20, color=OK if better else GREY_A),
                          label(f"\\${r['two']:,.0f}", font_size=20, color=OK if r["two"] > r["one"] else GREY_A)])
        grid = ValueGrid(hd, cells, col_w=[2.6, 3.2, 3.2], cell_h=0.55, font_size=19).move_to([-2.0, 0.0, 0])
        hl = SurroundingRectangle(VGroup(*grid.cell[1]), color=GOAL, buff=0.05)
        f = MathTex(r"p \cdot 10^6 \;>\; (1-p)\cdot 10^6 + 10^3 \iff p > 0.5005", font_size=28,
                    color=GOAL).to_edge(DOWN, buff=0.9)
        side = stack([(r"at $p = 0.5$ \ (a coin), \ two boxes", CAUSE),
                      (r"at $p = 0.5005$, \ a tie", GOAL),
                      (r"any better predictor: \ expected value says one box", EVID),
                      (r"dominance says two boxes at every $p$", CAUSE)], font_size=19, aligned_edge=LEFT,
                     width=4.0, buff=0.3).move_to([4.6, 0.0, 0])
        with self.voiceover(
            "The Reasoner builds the predictor with any accuracy p. <bookmark mark='a'/>With a predictor no better "
            "than a coin, the expected values are five hundred thousand for one box and five hundred and one "
            "thousand for two: take both. <bookmark mark='b'/>The tie comes at an accuracy of point five zero zero "
            "five. <bookmark mark='c'/>Above it, by expected value, one box is better, and the gap grows to "
            "nine hundred and ninety thousand against eleven thousand at ninety nine percent. "
            "<bookmark mark='d'/>The predictor need not be supernatural. A psychologist who is right sixty percent "
            "of the time, or a program that has read your messages, would do. Dominance, meanwhile, says two boxes "
            "at every accuracy."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(*[FadeIn(c) for c in grid.cell[0]], FadeIn(side[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(c) for c in grid.cell[1]], Create(hl), FadeIn(side[1]), Write(f))
            vo.wait_until("c")
            for k in (2, 3, 4):
                self.play(*[FadeIn(c) for c in grid.cell[k]], run_time=0.5)
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def simulated(self):
        d = load("newcomb")
        head = label(r"Ten thousand players, \ simulated", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["agents"] == 10000 and d["sim_p"] == 0.9 and d["n_one"] == 5001
        assert d["one_mean"] == 906219.0 and d["two_mean"] == 102620.0
        ax = Axes(x_range=[0, 3, 1], y_range=[0, 1000000, 250000], x_length=5.0, y_length=4.2, tips=False,
                  axis_config={"color": GREY_B, "font_size": 16},
                  y_axis_config={"include_numbers": True, "decimal_number_config": {"num_decimal_places": 0,
                                                                                    "group_with_commas": True}}
                  ).move_to([-3.2, -0.6, 0])
        bars = VGroup()
        for x, v, col, nm in ((1, d["one_mean"], EVID, r"one-boxers"), (2, d["two_mean"], CAUSE, r"two-boxers")):
            b = Rectangle(width=1.1, height=ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], color=col, fill_opacity=0.6)
            b.move_to(ax.c2p(x, v / 2))
            bars.add(VGroup(b, label(f"\\${v:,.0f}", font_size=18, color=col).next_to(b, UP, buff=0.1),
                            label(nm, font_size=17, color=col).next_to(ax.c2p(x, 0), DOWN, buff=0.15)))
        side = stack([(r"5001 choose one box, \ 4999 both, \ at random", GREY_A),
                      (r"a predictor right 90\% of the time", AGENT),
                      (r"one-boxers average \$906,219", EVID),
                      (r"two-boxers average \$102,620", CAUSE),
                      (r"Lewis, \ `Why Ain'cha Rich?' \ (1981): \ the riches were reserved for those predicted to "
                       r"be irrational", GOAL)], font_size=18, aligned_edge=LEFT,
                     width=5.4, buff=0.28).move_to([3.4, -0.4, 0])
        with self.voiceover(
            "The Reasoner seats ten thousand players in front of a predictor that is right ninety percent of the "
            "time. <bookmark mark='a'/>Half of them, five thousand and one, take one box. <bookmark mark='b'/>The "
            "one-boxers average nine hundred and six thousand dollars. <bookmark mark='c'/>The two-boxers average a "
            "hundred and three thousand. <bookmark mark='d'/>One-boxers ask the two-boxer: if you're so smart, why "
            "ain't you rich? David Lewis took that question as the title of a paper in 1981, and answered it: the "
            "riches were reserved for those the predictor expected to choose irrationally. Every two-boxer, he says, did better than he would "
            "have done by taking one box, given what was in front of him."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.wait(0.3)
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1:]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1:]), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def price(self):
        d = load("tetrad")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        assert d["mus"] == [["DOM", "EV", "FIX", "REL"]]
        assert sorted(d["mcs"]) == [["DOM"], ["EV"], ["FIX"], ["REL"]]
        sv = d["survey"]
        assert (sv["two boxes"], sv["one box"]) == (0.390, 0.312)
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.6, width=3.8, font_size=19,
                       center=[0, -0.6, 0], title=r"The Price List: \ Newcomb")
        positions = [(("EV",), r"CDT: \ two boxes", r"causal decision theory: \ Gibbard and Harper; \ Lewis; \ Joyce",
                      sv["two boxes"], r"two boxes, \ PhilPapers 2020"),
                     (("DOM",), r"EDT: \ one box", r"evidential decision theory: \ Jeffrey; \ Horgan; \ Ahmed",
                      sv["one box"], r"one box, \ PhilPapers 2020"),
                     (("REL",), r"no such predictor", r"of a deliberating agent: \ Levi; \ Spohn", None, r""),
                     (("FIX",), r"FDT: \ one box", r"functional decision theory: \ the prediction tracks your policy", None,
                      r"")]
        with self.voiceover(
            "Four claims cannot all be true. <bookmark mark='a'/>If an act is better whatever the state, choose it. "
            "Choose the act with the greatest expected value, given that you perform it. The predictor is reliable. "
            "And the contents of the boxes are fixed before you choose. <bookmark mark='b'/>The first and fourth "
            "say take both; the second and third say take one. <bookmark mark='c'/>Causal decision theorists, Allan "
            "Gibbard and William Harper, Lewis and James Joyce, reject the second as stated: expected value must be "
            "computed from what your act causes, not from what it indicates. They take both boxes, with thirty nine "
            "percent of philosophers in the 2020 survey. <bookmark mark='d'/>Evidential decision theorists, after "
            "Richard Jeffrey, and Arif Ahmed today, reject dominance where acts are evidence about states. They take "
            "one, with thirty one percent. <bookmark mark='e'/>Isaac Levi and Wolfgang Spohn doubted that a "
            "deliberating agent can treat its own choice as something to be predicted. "
            "<bookmark mark='f'/>And functional decision theory, in chapter twelve, says that what the predictor "
            "responds to is your decision procedure, which you do choose. The next chapter asks which kind of "
            "expectation is right."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who, share, note) in zip("cdef", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, share=share, share_note=note, width=3.0)
                self.play(*anims)
        self.clear_scene()
