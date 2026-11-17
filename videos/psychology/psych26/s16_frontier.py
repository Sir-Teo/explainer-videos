from __future__ import annotations

from videos.psychology.psych26.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.machines()
        self.rational()
        self.trait()

    def card(self):
        card = chapter_card(15, r"Frontier: \ theories found by machines", r"What comes after prospect theory?",
                            lit={2017: r"Frey et al.", 2018: r"Lieder et al.", 2020: r"Lieder \& Griffiths",
                                 2021: r"Peterson et al."},
                            part=PART, scale=("mind",), marr=("what", "why"))
        with self.voiceover("Chapter fifteen. Frontier: theories found by machines."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def machines(self):
        d = load("c13k")
        head = heading(r"Theories found by machines")
        steps = VGroup()
        for t, c in [(r"collect choices at scale: \ thirteen thousand problems", DATA),
                     (r"fit the classic theories, \ and unconstrained neural networks", MODEL),
                     (r"find where the networks beat the theories, \ and why", HEUR),
                     (r"write down the better theory", GAIN)]:
            box = RoundedRectangle(corner_radius=0.1, width=3.0, height=1.5, stroke_color=c, stroke_width=2,
                                   fill_color=BLACK, fill_opacity=0.5)
            steps.add(VGroup(box, wrapped_label(t, 2.6, 20, c).move_to(box)))
        steps.arrange(RIGHT, buff=0.45).move_to([0, 1.3, 0])
        arrows = VGroup(*[Arrow(steps[k].get_right(), steps[k + 1].get_left(), buff=0.05, color=GREY_B,
                                stroke_width=3, max_tip_length_to_length_ratio=0.25) for k in range(3)])
        rows = rows_of([
            (rf"in our fit prospect theory left {100 * (1 - d['r2']['cpt']):.0f}\% of the variance across problems "
             r"unexplained", WHITE),
            (r"Peterson and colleagues, \ 2021: \ the best models let the weighting of probabilities change with the "
             r"problem; \ people seem to use different rules in different contexts", MODEL),
            (r"the machine does not replace the theory: \ it shows where the theory is wrong, \ and the people "
             r"write the next one", GAIN),
        ], 12.0, 24, 0.32).move_to([0, -1.5, 0])
        tag = published_tag(r"Peterson et al.\ (2021); \ Erev et al.\ (2017)")
        with self.voiceover(
            "Where does the field go after prospect theory? One answer is a new way of building theories. "
            "<bookmark mark='a'/> Collect choices at a scale no laboratory could, as choices thirteen k did. Fit the "
            "classic theories, and also neural networks with no theory built in. Find the problems where the "
            "networks win, and work out why. Then write down a better theory. <bookmark mark='b'/> In our fit, "
            f"prospect theory left about {100 * (1 - d['r2']['cpt']):.0f} percent of the variation between problems "
            "unexplained. <bookmark mark='c'/> Peterson and colleagues found that the best models let the "
            "weighting of probabilities itself depend on the problem, as if people switch rules with context. "
            "Ido Erev's choice prediction competitions reached a similar conclusion by a different route. "
            "<bookmark mark='d'/> The machine doesn't replace the theory. It points to where the theory is wrong, "
            "and people write the next one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in steps], lag_ratio=0.5), Create(arrows), run_time=4)
            for m, r in zip("bcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def rational(self):
        d = load("rational")
        head = heading(r"Biases as good use of limited time")
        A = axes([0, 40], [0, 1700], x_length=5.4, y_length=3.6, xticks=[0, 10, 20, 30, 40],
                 yticks=[0, 500, 1000, 1500], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                 xlabel=r"steps of adjustment away from the anchor", ylabel=r"expected cost: \ error$^2$ + time",
                 center=[-3.3, -0.3, 0], font_size=16)
        cc = curve(A.ax, d["k"], d["J_cheap"], GAIN, 4)
        cd = curve(A.ax, d["k"], d["J_dear"], LOSS, 4)
        mc = Dot(A.ax.c2p(d["k_cheap"], d["J_cheap"][d["k_cheap"]]), color=GAIN, radius=0.09)
        md = Dot(A.ax.c2p(d["k_dear"], d["J_dear"][d["k_dear"]]), color=LOSS, radius=0.09)
        key = legend([(GAIN, rf"time cheap: \ stop after {d['k_cheap']} steps"),
                      (LOSS, rf"time dear: \ stop after {d['k_dear']} steps")], font_size=18).move_to(
            A.ax.c2p(27, 1350))
        rows = rows_of([
            (r"Lieder and Griffiths: \ \emph{resource-rational analysis}, \ the best use of a limited mind", WHITE),
            (rf"start at the anchor, \ {d['D']:.0f} points from the truth; \ each step removes {100 * d['r']:.0f}\% of "
             r"what is left, \ and costs time", MODEL),
            (rf"the best stopping point leaves a bias toward the anchor: \ {d['bias_cheap']:.1f} points when time is "
             rf"cheap, \ {d['bias_dear']:.1f} when it is dear", RISKY),
            (r"so a bias can be the signature of a sensible trade, \ which predicts when it will grow: \ under time "
             r"pressure", HEUR),
        ], 5.6, 22, 0.3).move_to([3.5, -0.1, 0])
        tag = psyche_tag(r"\texttt{compute.rational}: \ after Lieder, \ Griffiths, \ Huys \& Goodman (2018)")
        with self.voiceover(
            "A second answer reconciles the two camps of this part. <bookmark mark='a'/> Falk Lieder and Tom "
            "Griffiths call it resource-rational analysis: ask what the best use of a limited mind would be, "
            "counting the cost of thinking. <bookmark mark='b'/> Take anchoring. Suppose an estimate starts at the "
            f"anchor, {d['D']:.0f} points from the truth, and each step of adjustment removes "
            f"{100 * d['r']:.0f} percent of the distance that's left, at a cost in time. "
            "<bookmark mark='c'/> The expected cost is the squared error plus the time. When time is cheap, the "
            f"best plan stops after {d['k_cheap']} steps, still {d['bias_cheap']:.1f} points from the truth; when "
            f"it's dear, after {d['k_dear']}, {d['bias_dear']:.1f} points away. A bias toward the anchor is the "
            "optimal outcome. <bookmark mark='d'/> So a bias can be the signature of a sensible trade, and the "
            "theory predicts when it should grow: under time pressure, or with distraction. Lieder and colleagues "
            "found anchoring behaves that way."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(cc), Create(cd), FadeIn(key), run_time=2)
            self.play(FadeIn(mc), FadeIn(md), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def trait(self):
        head = heading(r"Is risk preference one trait?")
        left = VGroup(label(r"stated", font_size=28, color=GAIN),
                      wrapped_label(r"questionnaires: \ ``how willing are you to take risks?'', \ in general and in "
                                    r"driving, \ money, \ health", 5.0, 22, WHITE),
                      wrapped_label(r"reliable over time, \ and sharing one general factor", 5.0, 22, GAIN)).arrange(
            DOWN, buff=0.25)
        right = VGroup(label(r"revealed", font_size=28, color=LOSS),
                       wrapped_label(r"behavioural tasks: \ lotteries, \ balloon pumping, \ gambling games", 5.0, 22,
                                     WHITE),
                       wrapped_label(r"less reliable, \ and weakly related to each other and to the questionnaires",
                                     5.0, 22, LOSS)).arrange(DOWN, buff=0.25)
        VGroup(left, right).arrange(RIGHT, buff=1.4, aligned_edge=UP).move_to([0, 0.8, 0])
        foot = rows_of([
            (r"Frey, \ Pedroni, \ Mata, \ Rieskamp and Hertwig, \ 2017: \ about 1{,}500 adults, \ dozens of "
             r"measures", WHITE),
            (r"the measurement problem of Part 3, \ returning: \ a parameter fitted to choices is a claim about a "
             r"person only if it is stable in that person \ (Part 33)", MODEL),
        ], 12.0, 23, 0.3).move_to([0, -2.1, 0])
        tag = published_tag(r"Frey et al.\ (2017)")
        with self.voiceover(
            "The last frontier is the person. Is risk preference one trait, as personality traits are? "
            "<bookmark mark='a'/> In 2017 Renato Frey, Andreas Pedroni, Rui Mata, Jorg Rieskamp and Hertwig "
            "measured about fifteen hundred adults on dozens of measures. Asked how willing they were to take "
            "risks, in general and in domains like driving or money, people gave answers that were reliable over "
            "time and shared a general factor, much like a personality trait. <bookmark mark='b'/> Measured by "
            "behaviour, with lotteries, balloon pumping and gambling games, risk preference was less reliable, and "
            "the tasks barely agreed with each other or with the questionnaires. <bookmark mark='c'/> It's the "
            "measurement problem from Part 3 returning: a parameter fitted to someone's choices is a claim about "
            "that person only if it's stable in that person. Part 33, on personality, takes it up."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(left), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()
