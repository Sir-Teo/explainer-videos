from __future__ import annotations

from videos.philosophy.philosophy17.common import *  # noqa: F403


SPRINK = {"C": [-4.2, 1.6, 0], "S": [-5.4, 0.3, 0], "R": [-3.0, 0.3, 0], "W": [-4.2, -1.0, 0], "L": [-4.2, -2.3, 0]}
SPRINK_E = [("C", "S"), ("C", "R"), ("S", "W"), ("R", "W"), ("W", "L")]


class Markov(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"Markov, faithfulness, and the common cause",
                            r"What do graphs assume about probabilities?", lit=(1956, 1993), part=PART)
        with self.voiceover("Chapter eleven. Markov, faithfulness, and the common cause."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.markov()
        self.reichenbach()
        self.yule()
        self.bell()
        self.faithful()

    def markov(self):
        d = load("markov")
        hc = history_card(1993, r"Spirtes, \ Glymour and Scheines", r"\textit{Causation, Prediction, and Search}",
                          width=6.6, color=HIST).to_corner(UL, buff=0.3)
        g = CausalGraph({k: [v[0], v[1] - 0.4, 0] for k, v in SPRINK.items()}, SPRINK_E, radius=0.36, font_size=20,
                        colors={"C": HIDDEN, "W": EFFECT})
        key = label(r"cloudy, \ sprinkler, \ rain, \ wet, \ slippery", font_size=18, color=GREY_A).next_to(
            g, DOWN, buff=0.2)
        cmc = stack([(r"the causal Markov condition:", WHITE),
                     (r"each variable is independent of its non-effects, \ given its direct causes", CAUSE)],
                    font_size=22).move_to([2.6, 1.2, 0])
        fac = MathTex(r"P(c, s, r, w, l) = P(c)\,P(s \mid c)\,P(r \mid c)\,P(w \mid s, r)\,P(l \mid w)", font_size=28,
                      color=EFFECT).next_to(cmc, DOWN, buff=0.4)
        if fac.width > 7.6:
            fac.width = 7.6
        fac.set_x(2.6)
        cnt = label(r"binary variables: \ " + f"{d['params_factored']}" + r" numbers instead of " +
                    f"{d['params_full']}", font_size=21, color=OK).next_to(fac, DOWN, buff=0.35)
        mins = label(r"together with d-separation: \ every independence the graph entails holds in $P$",
                     font_size=20, color=GREY_A).next_to(cnt, DOWN, buff=0.35)
        with self.voiceover(
            "Peter Spirtes, Clark Glymour and Richard Scheines made the link between causal graphs and "
            "probability into two explicit axioms. <bookmark mark='a'/>The first is the causal Markov condition. "
            "<bookmark mark='b'/>Each variable is independent of everything except its own effects, once its "
            "direct causes are given. <bookmark mark='c'/>Equivalently, the joint distribution factorizes: one "
            "conditional probability per variable, given its parents. <bookmark mark='d'/>For five binary "
            "variables this needs eleven numbers instead of thirty-one, which is why Bayesian networks made "
            "probabilistic reasoning tractable. <bookmark mark='e'/>Combined with d-separation, the condition says "
            "every independence the graph entails holds in the data."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(g), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(cmc[0]))
            vo.wait_until("b")
            self.play(FadeIn(cmc[1]))
            vo.wait_until("c")
            self.play(Write(fac))
            vo.wait_until("d")
            self.play(FadeIn(cnt))
            vo.wait_until("e")
            self.play(FadeIn(mins))
        self.clear_scene()

    def reichenbach(self):
        hc = history_card(1956, r"Hans Reichenbach", r"\textit{The Direction of Time}", width=5.4,
                          color=HIST).to_corner(UL, buff=0.3)
        g = CausalGraph({"A": [-5.0, -0.8, 0], "B": [-2.4, -0.8, 0], "C": [-3.7, 0.9, 0]}, [("C", "A"), ("C", "B")],
                        radius=0.42, font_size=22, colors={"C": CAUSE, "A": EFFECT, "B": EFFECT})
        eqs = VGroup(
            label(r"if $A$ and $B$ are correlated, \ and neither causes the other, \ there is a common cause $C$ with",
                  font_size=21, color=WHITE),
            MathTex(r"P(A \wedge B \mid C) = P(A \mid C)\,P(B \mid C)", font_size=30, color=CAUSE),
            MathTex(r"P(A \wedge B \mid \lnot C) = P(A \mid \lnot C)\,P(B \mid \lnot C)", font_size=30, color=CAUSE),
            MathTex(r"P(A \mid C) > P(A \mid \lnot C), \qquad P(B \mid C) > P(B \mid \lnot C)", font_size=30,
                    color=GREY_A),
        ).arrange(DOWN, buff=0.28).move_to([2.0, 0.2, 0])
        if eqs[0].width > 7.6:
            eqs[0].width = 7.6
        foot = stack([(r"the common cause \textit{screens off} the correlation", OK),
                      (r"the Markov condition generalizes it to whole graphs", GREY_A)], font_size=22).to_edge(
            DOWN, buff=0.4)
        with self.voiceover(
            "The Markov condition generalizes an older idea, Hans Reichenbach's principle of the common cause. "
            "<bookmark mark='a'/>If two events are correlated and neither causes the other, there is a common cause. "
            "<bookmark mark='b'/>And it screens them off: given the cause, or given its absence, the events are "
            "independent. <bookmark mark='c'/>And the cause raises the probability of each. The barometer and the "
            "storm are correlated because air pressure drives both. <bookmark mark='d'/>The principle seems "
            "close to a law of thought. It has two famous counterexamples."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(eqs[0]))
            vo.wait_until("b")
            self.play(Write(eqs[1]), Write(eqs[2]))
            vo.wait_until("c")
            self.play(Write(eqs[3]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def yule(self):
        d = load("markov")["yule"]
        ex = d["example"]
        head = label(r"Correlation without any cause: \ Yule's nonsense correlations", font_size=28,
                     color=CONN).to_edge(UP, buff=0.3)
        lo = min(min(ex["a"]), min(ex["b"]))
        hi = max(max(ex["a"]), max(ex["b"]))
        ax = Axes(x_range=[0, d["T"], 25], y_range=[0, hi - lo + 2, 5], x_length=6.0, y_length=3.4,
                  axis_config={"color": GREY_B, "include_ticks": False}).move_to([-3.4, 0.0, 0])
        la = series_plot(ax, [v - lo + 1 for v in ex["a"]], CAUSE)
        lb = series_plot(ax, [v - lo + 1 for v in ex["b"]], EFFECT)
        cap = label(r"two \textit{independent} random walks: \ $r = " + f"{ex['r']:.2f}" + r"$; \ their steps: \ $r = " +
                    f"{ex['r_diff']:.2f}" + r"$", font_size=19, color=WHITE).next_to(ax, DOWN, buff=0.3)
        hx = Axes(x_range=[-1, 1, 0.5], y_range=[0, max(d["hist"]) * 1.1, 50], x_length=5.0, y_length=3.0,
                  axis_config={"color": GREY_B, "include_ticks": True, "font_size": 18},
                  x_axis_config={"numbers_to_include": [-1, -0.5, 0, 0.5, 1]}).move_to([3.4, 0.3, 0])
        hx.y_axis.set_opacity(0)
        bars = VGroup()
        for i, h in enumerate(d["hist"]):
            x0 = -1 + i * 0.1
            bars.add(Rectangle(width=hx.x_axis.unit_size * 0.1, height=max(1e-3, hx.y_axis.unit_size * h),
                               stroke_width=1, stroke_color=CAUSE, fill_color=CAUSE, fill_opacity=0.5).move_to(
                hx.c2p(x0 + 0.05, h / 2)))
        hl = label(r"correlation of " + f"{d['pairs']:,}".replace(",", "{,}") + r" pairs: \ " +
                   f"{100 * d['frac_abs_r_gt_0.5']:.0f}" + r"\% have $|r| > 0.5$", font_size=19,
                   color=GREY_A).next_to(hx, DOWN, buff=0.3)
        foot = label(r"Sober \ (2001): \ Venetian sea levels and British bread prices, \ both rising: \ "
                     r"correlated, \ with no common cause", font_size=20, color=BAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The first counterexample was noticed by George Udny Yule in 1926. <bookmark mark='a'/>Take two random "
            "walks, generated completely independently. These two have a correlation of point eight nine. Their "
            "individual steps are uncorrelated. <bookmark mark='b'/>The Reasoner generated two thousand such "
            "pairs. Forty percent show a correlation above one half in size. Trends produce correlation with no "
            "common cause at all. <bookmark mark='c'/>Elliott Sober's version: sea levels in Venice and bread "
            "prices in Britain have both risen for centuries. They are correlated, and nothing screens them off. "
            "Defenders reply that the principle applies to stationary processes, or to the steps, not the levels."
        ) as vo:
            self.play(FadeIn(head), Create(ax))
            vo.wait_until("a")
            self.play(Create(la), Create(lb), run_time=2)
            self.play(FadeIn(cap))
            vo.wait_until("b")
            self.play(Create(hx), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05), FadeIn(hl))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def bell(self):
        d = load("markov")["chsh"]
        head = label(r"Correlation without a common cause: \ Bell", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        src = Dot([0, 0.8, 0], radius=0.14, color=CAUSE)
        al = VGroup(RoundedRectangle(width=1.4, height=0.8, corner_radius=0.1, color=EFFECT),
                    label(r"Alice: \ $a, a'$", font_size=18, color=EFFECT)).move_to([-4.0, 0.8, 0])
        bo = VGroup(RoundedRectangle(width=1.4, height=0.8, corner_radius=0.1, color=EFFECT),
                    label(r"Bob: \ $b, b'$", font_size=18, color=EFFECT)).move_to([4.0, 0.8, 0])
        for x in (al, bo):
            x[1].move_to(x[0])
        rays = VGroup(DashedLine(src.get_center(), al.get_right(), color=CAUSE),
                      DashedLine(src.get_center(), bo.get_left(), color=CAUSE))
        lam = label(r"a common cause $\lambda$?", font_size=19, color=CAUSE).next_to(src, UP, buff=0.2)
        S = MathTex(r"S = E(a, b) + E(a, b') + E(a', b) - E(a', b')", font_size=30, color=WHITE).move_to([0, -0.5, 0])
        rows = stack([(r"any local common cause: \ $|S| \le " + f"{d['local_max']}" + r"$ \ (all " +
                       f"{d['strategies']}" + r" deterministic strategies, \ checked)", OK),
                      (r"quantum mechanics: \ $|S| = 2\sqrt{2} \approx " + f"{d['quantum']:.3f}" + r"$", BAD),
                      (r"experiments \ (Aspect, \ 1982; \ loophole-free, \ 2015): \ the quantum value", BAD),
                      (r"no common cause screens off the correlation: \ Part 26", GOAL)], font_size=21).next_to(
            S, DOWN, buff=0.35)
        with self.voiceover(
            "The second counterexample is deeper. <bookmark mark='a'/>A source sends a pair of particles to Alice "
            "and Bob, who each choose one of two measurements. Their results are correlated. Is there a common "
            "cause, some hidden variable fixed at the source? <bookmark mark='b'/>John Bell showed that common "
            "causes impose a bound. In the form of Clauser, Horne, Shimony and Holt, this combination of "
            "correlations can be at most two in size. <bookmark mark='c'/>The Reasoner checks every deterministic "
            "local strategy, sixteen in all, and so every mixture of them: the maximum is two. "
            "<bookmark mark='d'/>Quantum mechanics predicts two root two, about two point eight three. "
            "<bookmark mark='e'/>Experiments, from Alain Aspect's in 1982 to the loophole-free tests of 2015, find "
            "the quantum value. <bookmark mark='f'/>So some correlations have no screening common cause. What that "
            "means is the subject of Part twenty-six."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(src), FadeIn(al), FadeIn(bo), Create(rays), FadeIn(lam))
            vo.wait_until("b")
            self.play(Write(S))
            for mk, r in zip("cdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def faithful(self):
        head = label(r"Faithfulness", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the axiom", r"every independence in the data is entailed by the graph: \ no exact cancellations", OK),
            (r"its violation", r"Hesslow's pills \ (Chapter 4): \ two paths cancel, \ and a cause looks "
                               r"independent", BAD),
            (r"the defence", r"unfaithful parameters have measure zero \ (Meek, \ 1995): \ a coincidence of "
                             r"probability zero", EFFECT),
            (r"the worry", r"\textit{nearly} unfaithful ones are not rare, \ and no method can then be uniformly "
                           r"consistent \ (Robins, \ Scheines, \ Spirtes and Wasserman, \ 2003)", BAD),
            (r"and design", r"thermostats and bodies are built to cancel: \ homeostasis hides causes "
                            r"\ (Andersen, \ 2013)", CAUSE),
            (r"Cartwright \ (1999)", r"a factory whose one process makes a chemical and a pollutant: \ the cause "
                                     r"does not screen off its effects", GREY_A),
        ]
        g = rows_table(rows, top=1.8, gap=0.38, width=8.8, x_text=-3.0)
        with self.voiceover(
            "The second axiom is faithfulness. <bookmark mark='a'/>Every independence in the data is entailed by "
            "the graph; nothing is independent by an accident of cancelling parameters. "
            "<bookmark mark='b'/>Hesslow's pills violate it: the two paths cancel exactly, and a genuine cause "
            "looks irrelevant. <bookmark mark='c'/>The defence is that unfaithful parameter values form a set of "
            "measure zero, as Christopher Meek proved: exact cancellation is a coincidence of probability zero. "
            "<bookmark mark='d'/>The worry is that nearly cancelling parameters are not rare, and James Robins and "
            "colleagues showed that no discovery method can then be uniformly consistent: no sample size is "
            "guaranteed large enough. <bookmark mark='e'/>And Holly Andersen notes that some systems are designed "
            "to cancel: a thermostat, or the body's homeostasis, keeps the outcome constant whatever the cause. "
            "<bookmark mark='f'/>Nancy Cartwright attacked the Markov condition itself, with a factory whose single "
            "process sometimes makes both a chemical and a pollutant: knowing the process ran does not make its two "
            "products independent."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
