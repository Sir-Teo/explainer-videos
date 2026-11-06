from __future__ import annotations

from videos.philosophy.philosophy31.common import *  # noqa: F403


class Aaronson(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Counterexamples to IIT", r"Can a theory of consciousness be refuted by a grid?",
                            lit=(2014,), part=PART)
        with self.voiceover("Chapter eleven. Counterexamples to integrated information."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.expander()
        self.unfolding()
        self.letter()

    def expander(self):
        d = load("aaronson")
        head = label(r"$\Phi$ rewards being hard to cut, \ not doing anything", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        hc = history_card(2014, r"Scott Aaronson", r"`Why I Am Not an Integrated Information Theorist'", width=6.2,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = {r["name"]: r for r in d["rows"]}
        assert d["adder_adds"]
        assert [rows[k]["phi"] for k in ("a 2-bit adder", "a ring of ten XORs", "a 2-by-5 torus of XORs",
                                          "random XOR expanders")] == [0.0, 2.0, 6.0, 4.167]
        assert rows["random XOR expanders"]["phis"] == [6.0, 2.0, 3.0, 4.0, 6.0, 4.0]
        hd = [r"\text{system}", r"\text{gates}", r"\text{what it does}", r"\Phi \text{ (simplified)}"]
        what = {"a 2-bit adder": r"adds two numbers, \ correctly, \ every time",
                "a ring of ten XORs": r"nothing in particular",
                "a 2-by-5 torus of XORs": r"nothing in particular",
                "random XOR expanders": r"nothing in particular \ (mean of 6 draws)"}
        cells = [[label(k, font_size=19, color=WHITE), label(str(r["n"]), font_size=19, color=GREY_A),
                  label(what[k], font_size=18, color=OK if k == "a 2-bit adder" else GREY_A),
                  label(f"{r['phi']:g}", font_size=21, color=BAD if r["phi"] > 0 else GREY_B)]
                 for k, r in rows.items()]
        grid = ValueGrid(hd, cells, col_w=[3.8, 1.3, 4.6, 2.6], cell_h=0.6, font_size=19).move_to([0, -0.3, 0])
        foot = stack([(r"Aaronson: \ suitable XOR expanders have $\Phi$ growing without bound with their size", BAD),
                      (r"Tononi's reply: \ accept it: \ a large enough grid of XOR gates would be conscious", GOAL)],
                     font_size=19, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In 2014 the computer scientist Scott Aaronson asked what phi actually rewards. "
            "<bookmark mark='a'/>The Reasoner compares four systems under the simplified measure. A two-bit adder, "
            "eight gates, which adds two numbers correctly every time: it is feedforward, and its phi is zero. "
            "<bookmark mark='b'/>A ring of ten XOR gates, doing nothing in particular: two bits. A two-by-five "
            "torus of XOR gates: six. Random networks of XOR gates, each reading three others, averaged over six "
            "draws: four point one seven. <bookmark mark='c'/>Phi rewards structure that is hard to cut, whatever "
            "it computes. Aaronson gave constructions, expanders of XOR gates, whose phi grows without bound "
            "as they grow, so a simple lattice of parity gates could be vastly more conscious than any human brain. "
            "<bookmark mark='d'/>Tononi bit the bullet. In his reply he accepted that a large enough grid of XOR "
            "gates would be conscious. For the theory, that is a prediction; for its critics, a reductio."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(*[FadeIn(c) for c in grid.cell[0]])
            vo.wait_until("b")
            for r in range(1, 4):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.6)
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def unfolding(self):
        d = load("unfolding")
        head = label(r"The unfolding argument, \ computed", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert (d["loop_phi"], d["unrolled_phi"], d["nodes"], d["steps"], d["match"]) == (1.0, 0.0, 12, 3, 8)
        # the loop
        names = [r"\text{OR}", r"\text{AND}", r"\text{XOR}"]
        lp = [np.array([-4.6, 1.2, 0]), np.array([-5.6, -0.4, 0]), np.array([-3.6, -0.4, 0])]
        loop = VGroup(*[VGroup(Circle(radius=0.38, color=FUNC, fill_opacity=0.15), MathTex(n, font_size=18,
                                                                                         color=FUNC)).move_to(p)
                        for n, p in zip(names, lp)])
        for i in range(3):
            for j in range(3):
                if i != j:
                    v = (lp[i] - lp[j]) / np.linalg.norm(lp[i] - lp[j])
                    nrm = np.array([-v[1], v[0], 0]) * 0.07
                    loop.add(Arrow(lp[j] + v * 0.4 + nrm, lp[i] - v * 0.4 + nrm, buff=0, color=GREY_B,
                                   stroke_width=2, max_tip_length_to_length_ratio=0.15))
        ll = MathTex(rf"\Phi = {d['loop_phi']:g}", font_size=30, color=OK).next_to(loop, DOWN, buff=0.35)
        # the unrolled network: four layers of three
        layers = VGroup()
        xs = [-0.6, 1.2, 3.0, 4.8]
        for t, x in enumerate(xs):
            col = VGroup(*[VGroup(Circle(radius=0.3, color=PRED if t else GREY_B, fill_opacity=0.12),
                                  MathTex(names[i] if t else r"x_{%d}" % i, font_size=15,
                                          color=PRED if t else GREY_B)).move_to([x, 1.0 - 0.9 * i, 0])
                           for i in range(3)])
            layers.add(col)
        wires = VGroup()
        for t in range(1, 4):
            for i in range(3):
                for j in range(3):
                    if i != j:
                        wires.add(Line(layers[t - 1][j].get_right(), layers[t][i].get_left(), color=GREY_D,
                                       stroke_width=1.5))
        ul = MathTex(rf"\Phi = {d['unrolled_phi']:g}", font_size=30, color=BAD).next_to(layers, DOWN, buff=0.35)
        tl = label(r"the loop, \ unrolled three steps: \ 12 gates, \ no feedback", font_size=18,
                   color=GREY_A).next_to(layers, UP, buff=0.25)
        foot = stack([(r"from all 8 starting states, \ the last layer matches the loop after three steps", OK),
                      (r"same behaviour, \ opposite verdicts: \ Doerig, \ Schurger, \ Hess and Herzog \ (2019)",
                       BAD),
                      (r"so either $\Phi$ is not about anything we can test, \ or behaviour is not the test", GOAL)],
                     font_size=19, buff=0.18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "A second objection uses IIT's own central claim. <bookmark mark='a'/>Take the loop of three gates from "
            "the last chapter, with phi of one bit. <bookmark mark='b'/>Now unroll it in time: a layer that holds "
            "the starting state, then one layer of OR, AND and XOR gates for each step, each reading the layer "
            "before. Twelve gates, and no feedback at all. <bookmark mark='c'/>From every one of the eight starting "
            "states, the last layer of the unrolled network ends exactly where the loop does after three steps. "
            "<bookmark mark='d'/>But it is feedforward, so its phi is zero. <bookmark mark='e'/>Adrien Doerig and "
            "colleagues made this the unfolding argument in 2019: for any recurrent network there is a feedforward "
            "one with the same input-output behaviour. If phi says one is conscious and the other is not, then no "
            "experiment on behaviour or report could ever tell which theory is right. Either phi is about nothing "
            "testable, or behaviour is not the test, and IIT's defenders take the second horn."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(loop), FadeIn(ll))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in layers], lag_ratio=0.3), Create(wires), FadeIn(tl),
                      run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(ul))
            vo.wait_until("e")
            self.play(FadeIn(foot[1]))
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def letter(self):
        head = label(r"Science, \ or pseudoscience?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"panpsychist?", r"IIT implies that simple systems with feedback have some consciousness, \ and "
                                  r"that feedforward systems have none, \ however they behave", GREY_A),
                (r"September 2023", r"an open letter signed by 124 researchers calls IIT `pseudoscience'", BAD),
                (r"the reply", r"many, \ including critics of IIT, \ call the label unjustified and damaging", OK),
                (r"what remains", r"its core claims are hard to test, \ though some of its predictions were tested: "
                                  r"\ chapter 13", GOAL)]
        g = rows_table(rows, top=1.6, gap=0.5)
        with self.voiceover(
            "These consequences led to an unusually public fight. <bookmark mark='a'/>IIT implies that some very "
            "simple systems with feedback have a little consciousness, and that feedforward systems have none, "
            "however intelligently they behave. <bookmark mark='b'/>In September 2023, after the theory was widely "
            "reported as having passed an experimental test, an open letter signed by one hundred and twenty four "
            "researchers called it pseudoscience. <bookmark mark='c'/>Many others, including critics of IIT, "
            "replied that the label was unjustified and damaging to the field. <bookmark mark='d'/>What remains is "
            "a theory whose core claims are hard to test, though some of its predictions can be, as chapter "
            "thirteen shows."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
