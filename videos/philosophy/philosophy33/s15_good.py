from __future__ import annotations

from videos.philosophy.philosophy33.common import *  # noqa: F403

ACOL = {"no umbrella": MONEY, "stay in": PREF, "umbrella": EVID}


class Good(VoiceoverScene):
    def construct(self):
        card = chapter_card(14, r"The value of information", r"Can it be rational to refuse to look?", lit=(1967,),
                            part=PART)
        with self.voiceover("Chapter fourteen. The value of information."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.envelope()
        self.proof()
        self.checked()
        self.fails()

    def envelope(self):
        d = load("voi")
        head = label(r"Good's theorem, \ drawn", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["prior"] == 0.4 and d["accuracy"] == 0.8 and d["act_now"] == "no umbrella"
        assert (d["q_rain"], d["q_dry"], d["p_says_rain"]) == (0.7273, 0.1429, 0.44)
        assert (d["now"], d["after"], d["voi"]) == (0.6, 0.722, 0.122)
        ax = Axes(x_range=[0, 1, 0.2], y_range=[0, 1, 0.2], x_length=6.6, y_length=4.8, tips=False,
                  axis_config={"color": GREY_B, "font_size": 16, "include_numbers": True,
                               "decimal_number_config": {"num_decimal_places": 1}}).move_to([-2.6, -0.5, 0])
        xl = label(r"$q = P(\text{rain})$", font_size=18, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.4)
        lines = VGroup()
        for a, (r, dr) in d["acts"].items():
            ln = Line(ax.c2p(0, dr), ax.c2p(1, r), color=ACOL[a], stroke_width=2.5)
            nudge = {"umbrella": UP * 0.1, "stay in": DOWN * 0.12, "no umbrella": ORIGIN}[a]
            lines.add(VGroup(ln, label(a, font_size=16, color=ACOL[a]).next_to(ax.c2p(1, r), RIGHT, buff=0.1).shift(
                nudge)))

        def env(q):
            return max(q * r + (1 - q) * dr for r, dr in d["acts"].values())
        qs = np.linspace(0, 1, 201)
        envl = VMobject(color=WHITE, stroke_width=5).set_points_as_corners([ax.c2p(q, env(q)) for q in qs])
        q0, q1, q2 = d["prior"], d["q_dry"], d["q_rain"]
        p0 = Dot(ax.c2p(q0, d["now"]), radius=0.08, color=BAD)
        p1, p2 = Dot(ax.c2p(q1, d["v_dry"]), radius=0.08, color=OK), Dot(ax.c2p(q2, d["v_rain"]), radius=0.08,
                                                                          color=OK)
        chord = Line(p1.get_center(), p2.get_center(), color=OK, stroke_width=3)
        pa = Dot(ax.c2p(q0, d["after"]), radius=0.08, color=OK)
        gap = Line(p0.get_center(), pa.get_center(), color=GOAL, stroke_width=5)
        vl = VGroup(DashedLine(ax.c2p(q1, 0), ax.c2p(q1, d["v_dry"]), color=GREY_C),
                    DashedLine(ax.c2p(q2, 0), ax.c2p(q2, d["v_rain"]), color=GREY_C),
                    DashedLine(ax.c2p(q0, 0), ax.c2p(q0, d["now"]), color=GREY_C))
        side = stack([(r"each act's expected utility is a straight line in $q$", GREY_A),
                      (r"choosing the best: \ the upper envelope, \ which is convex", WHITE),
                      (r"now, \ $q = 0.4$: \ go without the umbrella, \ $0.600$", BAD),
                      (r"a forecast, \ right 80\% of the time: \ $q$ becomes $0.143$ or $0.727$, \ averaging $0.4$",
                       OK),
                      (r"choosing after looking: \ $0.722$ \ on average; \ the gap, \ $0.122$, \ is the value of "
                       r"the information", GOAL)], font_size=18, aligned_edge=LEFT, width=4.6, buff=0.25).move_to(
            [4.2, -0.3, 0])
        with self.voiceover(
            "In 1967 I. J. Good proved that free information never hurts. The proof is a picture. "
            "<bookmark mark='a'/>Two states, rain or dry, and three acts: take an umbrella, go without, or stay in. "
            "Each act's expected utility is a straight line in the probability of rain. <bookmark mark='b'/>If you "
            "choose the best act, your expected utility is the upper envelope of the lines, and an upper envelope "
            "of lines is always convex. <bookmark mark='c'/>Now your probability of rain is point four, and the best "
            "act is to go without the umbrella, point six. <bookmark mark='d'/>A forecast that is right eighty "
            "percent of the time will move your probability either down to point one four or up to point seven "
            "three, and the average of those posteriors, weighted by how likely each forecast is, is exactly the "
            "prior. <bookmark mark='e'/>After looking, you choose the best act at whichever posterior you get. "
            "The average of the envelope at the two posteriors lies on the chord, and because the envelope is "
            "convex, the chord lies above it: point seven two two against point six. The gap is the value of the "
            "information, and convexity guarantees it is never negative."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.3), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(envl), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(vl[2]), FadeIn(p0), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(vl[0]), Create(vl[1]), FadeIn(p1), FadeIn(p2), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(chord))
            self.play(FadeIn(pa), Create(gap), FadeIn(side[4]))
        self.clear_scene()

    def proof(self):
        head = label(r"The proof in one line", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        f1 = MathTex(r"\max_a \mathbb{E}[u(a)] \;=\; \max_a \sum_e P(e)\,\mathbb{E}[u(a) \mid e]", font_size=32,
                     color=PREF)
        f2 = MathTex(r"\;\le\; \sum_e P(e)\,\max_a \mathbb{E}[u(a) \mid e]", font_size=32, color=OK)
        g = VGroup(f1, f2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([0, 1.2, 0])
        rows = stack([(r"left: \ choose now; \ right: \ look at the evidence $e$, \ then choose", GREY_A),
                      (r"a maximum of averages is at most the average of the maxima", GOAL),
                      (r"equality exactly when no possible $e$ would change the choice", PREF),
                      (r"it needs expected utility, \ free evidence, \ and acts that cannot change the evidence",
                       RISK)], font_size=20, buff=0.25).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "In symbols it is one line. <bookmark mark='a'/>The value of choosing now is the maximum, over acts, of "
            "the expected utility, which can be split up by the evidence you might see. <bookmark mark='b'/>The "
            "value of looking first is the average, over the evidence, of the best act given that evidence. "
            "<bookmark mark='c'/>A maximum of averages is never more than the average of the maxima. "
            "<bookmark mark='d'/>The two are equal exactly when no possible evidence would change your choice. "
            "<bookmark mark='e'/>The theorem assumes three things: that you maximize expected utility, that the "
            "information is free, and that your choosing to look does not change the evidence."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f1))
            vo.wait_until("b")
            self.play(Write(f2), FadeIn(rows[0]))
            for mk, r in zip("cde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def checked(self):
        d = load("good")
        head = label(r"Two thousand problems, \ checked", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["problems"] == 2000 and d["negative"] == 0 and d["positive"] == 569
        n = d["problems"]
        cols, size = 50, 0.115
        rng = np.random.default_rng(1967)
        order = rng.permutation(n)
        pos = set(order[:d["positive"]].tolist())
        grid = VGroup(*[Square(size * 0.82, stroke_width=0, fill_opacity=0.9,
                               fill_color=OK if k in pos else GREY_D).move_to(
            [(k % cols - cols / 2) * size, -(k // cols) * size, 0]) for k in range(n)])
        grid.move_to([-2.4, -0.5, 0])
        side = stack([(r"random utilities, \ priors and tests: \ 2 states, \ 3 acts", GREY_A),
                      (r"569: \ looking strictly helps", OK),
                      (r"1431: \ the test could not change the choice: \ value 0", GREY_B),
                      (r"0: \ looking hurts", BAD)], font_size=19, aligned_edge=LEFT, width=4.0, buff=0.3).move_to(
            [4.8, -0.3, 0])
        with self.voiceover(
            "The Reasoner checks the theorem on two thousand random problems: random utilities for three acts in "
            "two states, a random prior, and a test of random accuracy. <bookmark mark='a'/>In five hundred and "
            "sixty nine, looking strictly helps. <bookmark mark='b'/>In the other one thousand four hundred and "
            "thirty one, no result of the test could change the best act, so the value of looking is exactly zero. "
            "<bookmark mark='c'/>In none does looking hurt."
        ) as vo:
            self.play(FadeIn(head), FadeIn(side[0]))
            self.play(FadeIn(grid), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def fails(self):
        d = load("good")
        head = label(r"When looking hurts", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        ce = d["reu_counterexample"]
        assert ce == {"prior": 0.198, "accuracy": 0.947, "reu_now": 0.4574, "reu_look": 0.4046}
        rows = [(r"risk-weighted agents", rf"Buchak \ (2010): \ the Reasoner finds one with prior {ce['prior']:.3f} "
                                          rf"and a test of accuracy {ce['accuracy']:.3f}: \ REU {ce['reu_now']:.4f} "
                                          rf"now, \ {ce['reu_look']:.4f} by looking first", RISK),
                (r"Newcomb-like cases", r"if the predictor reacts to whether you will look, \ looking changes the "
                                        r"states", EVID),
                (r"games", r"if others know that you know, \ knowing can be a liability: \ a threat you can no "
                           r"longer ignore", AGENT),
                (r"AI", r"the off-switch game \ (Hadfield-Menell et al., \ 2017): \ a robot uncertain of our "
                        r"aims values our decision as information, \ and lets us switch it off", GOAL)]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.6)
        with self.voiceover(
            "Each assumption can fail. <bookmark mark='a'/>Lara Buchak showed in 2010 that risk-weighted agents "
            "sometimes do better by not looking. The Reasoner finds such a case: with a prior of point two and a "
            "test that is ninety five percent accurate, the agent's risk-weighted utility is point four five seven "
            "now, and only point four zero five if it plans to look first. A risk-avoidant agent can rationally "
            "refuse free evidence; to her critics, that is a reason to doubt the theory. <bookmark mark='b'/>In "
            "Newcomb-like cases, if the predictor reacts to whether you will look, then looking changes the states "
            "themselves. <bookmark mark='c'/>In games, knowledge can be a liability: once others know that you know, "
            "a threat can no longer be ignored. <bookmark mark='d'/>And Good's theorem appears in the design of "
            "artificial agents. In the off-switch game of Dylan Hadfield-Menell and colleagues, a robot uncertain "
            "of what its human wants treats the human's decision to switch it off as information, and so, by "
            "Good's reasoning, lets itself be switched off. The more certain it is, the weaker that reason becomes."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
