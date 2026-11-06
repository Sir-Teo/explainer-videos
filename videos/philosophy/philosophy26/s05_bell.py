from __future__ import annotations

from videos.philosophy.philosophy26.common import *  # noqa: F403


class Bell(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Bell's theorem", r"Could the values have been there all along?", lit=(1964, 1969),
                            part=PART)
        with self.voiceover("Chapter four. Bell's theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.model()
        self.derive()
        self.quantum()
        self.curve()
        self.mermin()

    def model(self):
        hc = history_card(1964, r"John Stewart Bell", r"`On the Einstein Podolsky Rosen Paradox'", width=6.0,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = stack([(r"take EPR at its word: \ each particle carries predetermined answers", CLASS),
                      (r"Alice chooses one of two settings, \ $a$ or $a'$; \ Bob, \ $b$ or $b'$", WHITE),
                      (r"each answer is $\pm 1$, \ and depends only on the local setting \ (locality)", CLASS),
                      (r"local hidden variables: \ $A(a, \lambda)$, \ $B(b, \lambda)$, \ with $\lambda$ shared at the "
                       r"source", ABS),
                      (r"Bell asked: \ what correlations can such a model produce?", GOAL)], font_size=22,
                     aligned_edge=LEFT, width=11.6, buff=0.32).move_to([0, -0.4, 0])
        with self.voiceover(
            "In 1964 John Bell took EPR at its word. <bookmark mark='a'/>Suppose each particle carries, from the "
            "source, predetermined answers to every question it might be asked. <bookmark mark='b'/>Alice chooses "
            "between two settings, a and a prime; Bob between b and b prime. <bookmark mark='c'/>Each answer is plus "
            "or minus one, and depends only on the local setting: what Bob chooses cannot change Alice's answer. "
            "<bookmark mark='d'/>A local hidden-variable model, in other words, with some shared variable lambda "
            "set at the source. <bookmark mark='e'/>Bell's question: what correlations can any such model "
            "produce?"
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def derive(self):
        d = load("chsh")
        head = label(r"The CHSH inequality, \ derived", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        lines = VGroup(
            MathTex(r"S = A_a B_b + A_a B_{b'} + A_{a'} B_b - A_{a'} B_{b'}", font_size=34),
            MathTex(r"= A_a\,(B_b + B_{b'}) \;+\; A_{a'}\,(B_b - B_{b'})", font_size=34),
            MathTex(r"B_b, B_{b'} = \pm 1:\quad \text{one bracket is } 0, \text{ the other } \pm 2", font_size=30,
                    color=CLASS),
            MathTex(r"\Rightarrow\; S = \pm 2 \text{ for every } \lambda \;\Rightarrow\; |\langle S \rangle| \le 2",
                    font_size=34, color=GOAL)).arrange(DOWN, buff=0.4).move_to([-1.6, 0.0, 0])
        side = stack([(rf"the Reasoner enumerates all 16 local deterministic strategies: \ $S \in "
                       rf"\{{{', '.join(str(v) for v in d['local_values'])}\}}$", OK),
                      (r"averaging over $\lambda$ cannot leave $[-2, 2]$", ABS),
                      (r"Clauser, \ Horne, \ Shimony and Holt \ (1969)", HIST)], font_size=20, aligned_edge=LEFT,
                     width=4.2, buff=0.35).move_to([4.8, -0.2, 0])
        with self.voiceover(
            "The answer, in the form John Clauser, Michael Horne, Abner Shimony and Richard Holt gave it in 1969. "
            "<bookmark mark='a'/>For one run, form this sum of products of the answers: S. "
            "<bookmark mark='b'/>Group it: A a times the sum of Bob's two answers, plus A a prime times their "
            "difference. <bookmark mark='c'/>Bob's answers are each plus or minus one, so either they are equal, "
            "and the difference is zero and the sum is plus or minus two, or they are opposite, and the sum is zero. "
            "Either way, one bracket vanishes and the other is plus or minus two. <bookmark mark='d'/>So S is plus or "
            "minus two on every run, and its average over runs lies between minus two and two. "
            "<bookmark mark='e'/>The Reasoner checks all sixteen ways of fixing four answers: S is always two or "
            "minus two."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(Write(l))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(s) for s in side], lag_ratio=0.3))
        self.clear_scene()

    def quantum(self):
        d = load("chsh")
        head = label(r"What quantum mechanics predicts", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        f = MathTex(r"E(a, b) = \langle \Psi^- |\, \sigma_a \otimes \sigma_b \,| \Psi^- \rangle = -\cos(a - b)",
                    font_size=34, color=WAVE).next_to(head, DOWN, buff=0.35)
        angs = VGroup(*[MathTex(t, font_size=28) for t in (r"a = 0^\circ", r"a' = 90^\circ", r"b = 45^\circ",
                                                           r"b' = -45^\circ")]).arrange(RIGHT, buff=0.6).next_to(
            f, DOWN, buff=0.35)
        E = d["E"]
        hd = [r"\text{pair}", r"E"]
        rows = [[MathTex(k.replace("'", r"'"), font_size=26), MathTex(f"{v:+.4f}", font_size=26, color=ALICE)]
                for k, v in E.items()]
        grid = ValueGrid(hd, rows, col_w=[2.0, 2.4], cell_h=0.48, font_size=22).move_to([-3.2, -1.6, 0])
        side = stack([(rf"$|S| = {d['abs_S']:.4f} = 2\sqrt2$", BAD),
                      (r"above the local bound of 2", BAD),
                      (rf"Tsirelson \ (1980): \ no quantum state does better; \ the Reasoner's search over angles "
                       rf"tops out at {d['grid_best']:.4f}", ABS)], font_size=22, aligned_edge=LEFT, width=6.0,
                     buff=0.32).move_to([3.2, -1.6, 0])
        assert abs(d["abs_S"] - 2 * math.sqrt(2)) < 1e-3
        with self.voiceover(
            "Now ask quantum mechanics. <bookmark mark='a'/>For the singlet, the correlation between Alice's answer "
            "at angle a and Bob's at angle b is minus the cosine of the angle between them. "
            "<bookmark mark='b'/>Choose Alice's settings at zero and ninety degrees, Bob's at plus and minus "
            "forty-five. <bookmark mark='c'/>The four correlations come out at minus or plus one over root two, "
            "<bookmark mark='d'/>and S has size two root two, about two point eight three: well above the bound "
            "that any local hidden-variable model must obey. <bookmark mark='e'/>Boris Tsirelson proved in 1980 "
            "that no quantum state does better, and the Reasoner's search over angles finds the same ceiling. "
            "Quantum mechanics breaks Bell's bound, but not by an unlimited amount."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("b")
            self.play(FadeIn(angs))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.4)
            vo.wait_until("d")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("e")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def curve(self):
        d = load("chsh")
        head = label(r"Correlation against angle", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 180, 45], y_range=[-1, 1, 0.5], x_length=7.0, y_length=4.2,
                  axis_config={"color": GREY_B, "font_size": 18, "include_numbers": True}).move_to([-2.4, -0.5, 0])
        xl = label(r"angle between the settings (degrees)", font_size=18, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        yl = label(r"correlation $E$", font_size=18, color=GREY_A).next_to(ax.y_axis, UP, buff=0.1).align_to(
            ax, LEFT)
        pts = [c for c in d["curve"] if c["angle_deg"] <= 180]
        q = series_plot(ax, [c["quantum"] for c in pts], WAVE, xs=[c["angle_deg"] for c in pts], width=4)
        lin = DashedVMobject(series_plot(ax, [c["linear"] for c in pts], CLASS, xs=[c["angle_deg"] for c in pts],
                                         width=3), num_dashes=30)
        side = stack([(r"blue: \ quantum, \ $-\cos\theta$", WAVE),
                      (r"dashed: \ the best a simple local model can match", CLASS),
                      (r"the gap at $45^\circ$ and $135^\circ$ is what CHSH measures", BAD)], font_size=20,
                     aligned_edge=LEFT, width=4.4, buff=0.3).move_to([4.5, -0.4, 0])
        dot45 = Dot(ax.c2p(45, -math.cos(math.radians(45))), radius=0.09, color=BAD)
        dot135 = Dot(ax.c2p(135, -math.cos(math.radians(135))), radius=0.09, color=BAD)
        with self.voiceover(
            "Picture it. <bookmark mark='a'/>The quantum correlation, minus cosine of the angle, in blue. "
            "<bookmark mark='b'/>Dashed, the straight line that the simplest local model, with answers fixed by a "
            "hidden direction, can reproduce: perfect anticorrelation at zero, perfect correlation at a hundred and "
            "eighty, and a straight line between. <bookmark mark='c'/>They agree at the ends and the middle. They "
            "differ most at forty-five and a hundred and thirty-five degrees, exactly the angles the CHSH "
            "combination uses. The cosine bulges beyond what local answers can follow."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(q), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(lin), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(dot45), FadeIn(dot135), FadeIn(side[2]))
        self.clear_scene()

    def mermin(self):
        d = load("mermin")
        head = label(r"Mermin's device", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        src = Dot([0, 1.7, 0], radius=0.13, color=PART_C)
        sl = label(r"source", font_size=17, color=PART_C).next_to(src, UP, buff=0.12)

        def detector(x, col, name):
            box = RoundedRectangle(width=2.0, height=1.1, corner_radius=0.12, color=col).move_to([x, 1.7, 0])
            dial = VGroup(*[label(str(k), font_size=18, color=GREY_A) for k in (1, 2, 3)]).arrange(
                RIGHT, buff=0.3).move_to(box.get_center() + DOWN * 0.22)
            lights = VGroup(Circle(0.12, color=BAD, fill_opacity=0.7), Circle(0.12, color=OK, fill_opacity=0.7)
                            ).arrange(RIGHT, buff=0.3).move_to(box.get_center() + UP * 0.25)
            nm = label(name, font_size=18, color=col).next_to(box, DOWN, buff=0.1)
            return VGroup(box, dial, lights, nm)

        L, Rt = detector(-4.6, ALICE, r"Alice"), detector(4.6, BOB, r"Bob")
        facts = stack([(r"same settings: \ always the same colour", OK),
                       (r"all runs: \ the same colour half the time", WAVE)], font_size=21, aligned_edge=LEFT,
                      width=5.4, buff=0.25).move_to([0, 0.35, 0])
        sets = d["sets"]
        assert d["worst_agree_of_9"] == 5 and sorted(s_["agree_of_9"] for s_ in sets) == [5] * 6 + [9] * 2
        cards = VGroup()
        for s_ in sets:
            cols = VGroup(*[Circle(0.1, color=(BAD if ch == "R" else OK), fill_opacity=0.85) for ch in s_["set"]]
                          ).arrange(RIGHT, buff=0.12)
            n = MathTex(rf"\tfrac{{{s_['agree_of_9']}}}{{9}}", font_size=26,
                        color=(OK if s_["agree_of_9"] == 9 else PART_C))
            box = RoundedRectangle(width=1.3, height=1.05, corner_radius=0.1, color=GREY_C, stroke_width=1.5)
            VGroup(cols, n).arrange(DOWN, buff=0.15).move_to(box)
            cards.add(VGroup(box, cols, n))
        cards.arrange(RIGHT, buff=0.15).move_to([0, -1.2, 0])
        ctag = label(r"the eight instruction sets, \ and the share of the 9 setting pairs on which they agree",
                     font_size=18, color=GREY_A).next_to(cards, UP, buff=0.15)
        q, runs = d["quantum_rate"], f"{d['runs']:,}".replace(",", r"\,")
        assert round(q, 2) == 0.51 and d["same_setting_rate"] == 1.0
        res = stack([(r"instructions, \ in any mix: \ agreement $\ge \tfrac59 \approx 0.556$", CLASS),
                     (rf"quantum, \ settings $120^\circ$ apart: \ $\tfrac13 \cdot 1 + \tfrac23 \cdot \tfrac14 = "
                      rf"\tfrac12$; \ simulated over {runs} runs: \ {q:.3f}", WAVE)],
                    font_size=21, aligned_edge=LEFT, width=12.0, buff=0.25).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "David Mermin made the argument concrete in 1981, with a device anyone can picture. "
            "<bookmark mark='a'/>A source sends a particle to each of two detectors. Each detector has a switch "
            "with three settings, set at random for each run, and flashes red or green. <bookmark mark='b'/>Two "
            "facts. When the switches agree, the lights always flash the same colour. And over all runs, the colours "
            "agree just half the time. <bookmark mark='c'/>The natural explanation of the first fact is that each "
            "particle carries instructions: a colour for each setting, the same for both. <bookmark mark='d'/>There "
            "are eight instruction sets. The Reasoner counts, for each, how many of the nine pairs of settings give "
            "the same colour. Two sets agree on all nine; the other six agree on five. <bookmark mark='e'/>So "
            "instructions give agreement at least five times in nine, whatever their mix. <bookmark mark='f'/>The "
            "quantum device, with settings a hundred and twenty degrees apart, agrees exactly half the time; "
            "simulated over nine thousand runs, zero point five one. No instructions can do it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(src), FadeIn(sl), FadeIn(L), FadeIn(Rt))
            vo.wait_until("b")
            self.play(FadeIn(facts[0]))
            self.play(FadeIn(facts[1]))
            vo.wait_until("c")
            self.play(Indicate(src, color=PART_C, scale_factor=1.6))
            vo.wait_until("d")
            self.play(FadeIn(ctag), LaggedStart(*[FadeIn(c) for c in cards], lag_ratio=0.15), run_time=2)
            vo.wait_until("e")
            self.play(FadeIn(res[0]))
            vo.wait_until("f")
            self.play(FadeIn(res[1]))
        self.clear_scene()
