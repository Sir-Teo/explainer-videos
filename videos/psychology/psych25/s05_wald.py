from __future__ import annotations

from videos.psychology.psych25.common import *  # noqa: F403


class Wald(VoiceoverScene):
    def construct(self):
        self.card()
        self.test()
        self.payoff()
        self.to_mind()

    def card(self):
        card = chapter_card(4, r"Wald's test", r"When should you stop collecting evidence?",
                            lit={1945: r"Wald", 1948: r"Wald \& Wolfowitz", 1960: r"Stone", 1968: r"Laming"},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter four. Wald's test."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def test(self):
        d = load("sprt")
        head = heading(r"Derivation: \ the sequential probability ratio test")
        path = d["path"]
        n = len(path) - 1
        A = axes([0, 40], [-3.6, 3.6], x_length=6.4, y_length=4.2, xticks=[0, 10, 20, 30, 40], yticks=[-3, 0, 3],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"shots fired",
                 ylabel=r"log likelihood ratio", center=[-3.2, -0.3, 0], font_size=16)
        up = DashedLine(A.ax.c2p(0, d["A"]), A.ax.c2p(40, d["A"]), color=BOUND, stroke_width=2)
        lo = DashedLine(A.ax.c2p(0, d["B"]), A.ax.c2p(40, d["B"]), color=BOUND, stroke_width=2)
        ul = label(r"accept $p = 0.7$", font_size=17, color=BOUND).next_to(up, UP, buff=0.05).align_to(up, RIGHT)
        ll = label(r"accept $p = 0.5$", font_size=17, color=BOUND).next_to(lo, DOWN, buff=0.05).align_to(lo, RIGHT)
        walk = VMobject(color=EVIDENCE, stroke_width=3).set_points_as_corners(
            [A.ax.c2p(k, float(v)) for k, v in enumerate(path)])
        stop = Dot(A.ax.c2p(n, float(path[-1])), radius=0.09, color=MODEL)
        sl = label(rf"stop at shot {n}", font_size=18, color=MODEL).next_to(stop, RIGHT, buff=0.15).shift(DOWN * 0.35)
        eqs = VGroup(
            MathTex(r"\Lambda_n = \sum_{i=1}^{n} \log \frac{P(x_i \mid p = 0.7)}{P(x_i \mid p = 0.5)}", font_size=30,
                    color=EVIDENCE),
            MathTex(r"\text{hit: } +\log\tfrac{0.7}{0.5} = +0.34 \qquad \text{miss: } \log\tfrac{0.3}{0.5} = -0.51",
                    font_size=26, color=WHITE),
            MathTex(r"A = \log\frac{1-\beta}{\alpha} = 2.94, \qquad B = \log\frac{\beta}{1-\alpha} = -2.94",
                    font_size=26, color=BOUND),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([3.5, 1.4, 0])
        assert abs(d["A"] - 2.944) < 1e-3 and d["decision"] == 1
        rows = rows_of([
            (r"two hypotheses about a shell: \ it hits 70\% of the time, \ or only 50\%; \ errors allowed: "
             r"$\alpha = \beta = 0.05$", WHITE),
            (r"after each shot, \ add its log likelihood ratio; \ stop the moment the sum leaves the band", EVIDENCE),
            (r"this run, \ the median of 101 with $p = 0.7$, \ stopped at shot " + str(n), MODEL),
        ], 6.0, 22, 0.3).move_to([3.5, -1.5, 0])
        tag = psyche_tag(r"\texttt{decide.sprt\_bernoulli}; \ Wald (1945)")
        with self.voiceover(
            "Here is Wald's idea, worked on a simple case. <bookmark mark='a'/> A new shell either hits seventy "
            "percent of the time, or only fifty, and we'll accept a five percent chance of each kind of mistake. "
            "<bookmark mark='b'/> After every shot, add the log of how much more likely that shot was under one "
            "hypothesis than the other. A hit adds a third; a miss takes away about a half. <bookmark mark='c'/> And "
            "set two lines. Wald showed that stopping where the ratio first reaches nineteen to one, either way, "
            "keeps both error rates near five percent. In logs, plus and minus two point nine four. "
            f"<bookmark mark='d'/> Here's a run with a seventy percent shell, the median of a hundred and one. The "
            f"sum wanders, drifts upward, and leaves the band at shot {n}. Decision: the better shell."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Write(eqs[0]), Write(eqs[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Write(eqs[2]), Create(up), Create(lo), FadeIn(ul), FadeIn(ll))
            vo.wait_until("d")
            self.play(Create(walk), run_time=4, rate_func=linear)
            self.play(FadeIn(stop), FadeIn(sl), FadeIn(rows[2]))
        self.clear_scene()

    def payoff(self):
        d = load("sprt")
        head = heading(r"Half the shots")
        A = axes([0.4, 0.8], [0, 75], x_length=6.4, y_length=4.0, xticks=[0.4, 0.5, 0.6, 0.7, 0.8],
                 yticks=[0, 25, 50, 75], xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.0f}",
                 xlabel=r"the shell's true hit rate", ylabel=r"shots needed", center=[-3.2, -0.2, 0], font_size=16)
        fixed = Line(A.ax.c2p(0.4, d["fixed_n"]), A.ax.c2p(0.8, d["fixed_n"]), color=LOST, stroke_width=3)
        fl = label(rf"a fixed test: \ {d['fixed_n']} shots, \ always", font_size=18, color=LOST).next_to(
            A.ax.c2p(0.6, d["fixed_n"]), UP, buff=0.08)
        asn = curve(A.ax, d["ps"], d["asn"], EVIDENCE, 3)
        sims = scatter(A.ax, d["sim_p"], d["sim_mean_n"], MODEL, 0.09, 1)
        key = legend([(EVIDENCE, r"Wald's approximation \ (no overshoot)"), (MODEL, r"20{,}000 simulated tests each")],
                     font_size=17).move_to(A.ax.c2p(0.66, 12))
        n0, n1, nf = d["asn_h0"], d["asn_h1"], d["fixed_n"]
        assert max(n0, n1) < 0.5 * nf and np.all(np.abs(d["sim_accept"] - [0.05, 0.5, 0.95]) < 0.02)
        assert np.all(d["sim_mean_n"] > np.interp(d["sim_p"], d["ps"], d["asn"]))  # the overshoot adds shots
        rows = rows_of([
            (rf"to guarantee the same error rates, \ a test fixed in advance needs {nf} shots", LOST),
            (rf"Wald's test needs about {n0:.0f} on average when the shell is poor, \ {n1:.0f} when it is good",
             EVIDENCE),
            (r"the price: \ the hardest case, \ a shell in between, \ takes longest, \ and any one run can be long",
             BOUND),
            (r"Wald \& Wolfowitz, \ 1948: \ no test with these error rates needs fewer shots on average, \ under "
             r"either hypothesis", MODEL),
        ], 5.6, 23, 0.36).move_to([3.6, 0.0, 0])
        tag = psyche_tag(r"\texttt{decide.sprt\_oc\_asn}, \ \texttt{fixed\_n}, \ \texttt{sprt\_simulate}")
        with self.voiceover(
            "What does stopping early buy? <bookmark mark='a'/> To get the same error rates from a test whose "
            f"length is fixed in advance, you need {nf} shots, every time. <bookmark mark='b'/> Wald's test needs "
            f"about {n0:.0f} on average when the shell is the poor one, and about {n1:.0f} when it's the good one: "
            "less than half. The dots are twenty thousand simulated tests each. They run a few shots above Wald's "
            "formula, which ignores how far the sum overshoots the line on its last step. "
            "<bookmark mark='c'/> There's a price. The hardest shells, in between the two hypotheses, take longest, "
            "and any single test can run long. <bookmark mark='d'/> And in 1948 Wald and Jacob Wolfowitz proved "
            "that no test with these error rates needs fewer shots on average, under either hypothesis. The "
            "military kept the method secret until the war was over."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(fixed), FadeIn(fl), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(asn), FadeIn(sims), FadeIn(key), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def to_mind(self):
        d = load("ddm")
        head = heading(r"From shells to seeing")
        A = axes([0, 1.0], [0, 1.2], x_length=6.0, y_length=3.4, xticks=[0, 0.5, 1.0], yticks=[0, 0.6, 1.2],
                 xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}", xlabel=r"time, \ s",
                 ylabel=r"evidence", center=[-3.2, -0.3, 0], font_size=16)
        rng = np.random.default_rng(8)
        coarse = np.concatenate([[0.6], 0.6 + np.cumsum(rng.choice([0.12, -0.12], 8, p=[0.62, 0.38]))])
        tc = np.linspace(0, 0.8, 9)
        cpath = VMobject(color=GREY_B, stroke_width=3).set_points_as_corners(
            [A.ax.c2p(t, min(max(v, 0), 1.2)) for t, v in zip(tc, coarse)])
        k = int(np.argsort(d["path_len"], kind="stable")[len(d["path_len"]) // 2])
        p = d["paths"][k][: d["path_len"][k]]
        tf = np.arange(len(p)) * d["dt"]
        keep = tf <= 1.0
        fpath = VMobject(color=EVIDENCE, stroke_width=2.5).set_points_as_corners(
            [A.ax.c2p(t, v) for t, v in zip(tf[keep], p[keep])])
        bnd = VGroup(DashedLine(A.ax.c2p(0, d["a"]), A.ax.c2p(1.0, d["a"]), color=BOUND, stroke_width=2),
                     DashedLine(A.ax.c2p(0, 0), A.ax.c2p(1.0, 0), color=BOUND, stroke_width=2))
        rows = rows_of([
            (r"Stone, \ 1960; \ Laming, \ 1968: \ perhaps a person choosing also adds up samples of evidence "
             r"until a bound", WHITE),
            (r"make the steps smaller and more frequent, \ and the walk becomes a diffusion: \ a steady drift plus "
             r"noise", EVIDENCE),
            (r"Wald's bounds become the person's caution; \ the drift, \ the quality of what they see", BOUND),
            (r"Ratcliff, \ 1978: \ the diffusion model of choice, \ the subject of the next chapter", MODEL),
        ], 5.6, 23, 0.36).move_to([3.6, 0.0, 0])
        tag = published_tag(r"Stone (1960); \ Laming (1968); \ Ratcliff (1978)")
        with self.voiceover(
            "Psychologists soon wondered whether minds work this way. <bookmark mark='a'/> Mervyn Stone in 1960 and "
            "Donald Laming in 1968 proposed that a person choosing between two answers adds up samples of evidence "
            "until the total reaches a bound. <bookmark mark='b'/> In a brain, evidence doesn't arrive in shots. "
            "Make the steps smaller and more frequent, and the random walk becomes a diffusion: a steady drift, the "
            "quality of the evidence, plus noise. <bookmark mark='c'/> Wald's two lines become the person's "
            "caution. <bookmark mark='d'/> That's the diffusion model, proposed by Roger Ratcliff in 1978, and the "
            "subject of the next chapter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(cpath), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(fpath), FadeIn(rows[1]), run_time=3)
            vo.wait_until("c")
            self.play(Create(bnd), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
