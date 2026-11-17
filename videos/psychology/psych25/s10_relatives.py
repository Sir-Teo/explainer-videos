from __future__ import annotations

from videos.psychology.psych25.common import *  # noqa: F403


class Relatives(VoiceoverScene):
    def construct(self):
        self.card()
        self.lba()
        self.lca()
        self.urgency()

    def card(self):
        card = chapter_card(9, r"Relatives: \ races, \ leaks and urgency", r"Is diffusion the only way to add up?",
                            lit={2001: r"Usher \& McClelland", 2006: r"Bogacz et al.", 2008: r"Brown \& Heathcote",
                                 2015: r"Hawkins et al."},
                            part=PART, scale=("mind",), marr=("how",))
        with self.voiceover("Chapter nine. Relatives: races, leaks and urgency."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def lba(self):
        d = load("lba")
        head = heading(r"The linear ballistic accumulator")
        A = axes([0, 1.6], [0, 1.15], x_length=4.4, y_length=3.2, xticks=[0, 0.8, 1.6], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}", xlabel=r"time after $t_0$, \ s",
                 ylabel=r"evidence", center=[-4.5, -0.1, 0], font_size=15)
        b, Aw = d["b"], d["A"]
        thr = DashedLine(A.ax.c2p(0, b), A.ax.c2p(1.6, b), color=BOUND, stroke_width=2)
        band = Rectangle(width=0.18, height=abs(A.ax.c2p(0, Aw)[1] - A.ax.c2p(0, 0)[1]), stroke_width=0,
                         fill_color=GREY_C, fill_opacity=0.5).move_to(A.ax.c2p(0, Aw / 2), aligned_edge=RIGHT)
        rng = np.random.default_rng(12)
        lines = VGroup()
        for k, (v, c) in enumerate(zip(d["vs"], (MODEL, LOST))):
            for _ in range(3):
                st = rng.random() * Aw
                rate = max(0.15, v + d["s"] * rng.standard_normal())
                t_end = min((b - st) / rate, 1.6)
                lines.add(Line(A.ax.c2p(0, st), A.ax.c2p(t_end, st + rate * t_end), color=c, stroke_width=2.5))
        lab = VGroup(label(r"grey band: \ the start, \ anywhere in $[0, A]$", font_size=16, color=GREY_A).move_to(
            A.ax.c2p(1.0, 0.12)), label(r"threshold $b$", font_size=16, color=BOUND).next_to(thr, UP, buff=0.04))
        B = axes([0.2, 2.5], [0, 2.2], x_length=4.0, y_length=3.2, xticks=[0.5, 1.5, 2.5], yticks=[0, 1, 2],
                 xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}", xlabel=r"response time, \ s",
                 ylabel=r"density", center=[0.3, -0.1, 0], font_size=15)
        mids = (d["edges"][:-1] + d["edges"][1:]) / 2
        w = float(np.diff(d["edges"])[0]) * 0.9
        h0 = bars(B.ax, mids, d["h0"], MODEL, width=w, opacity=0.3)
        h1 = bars(B.ax, mids, d["h1"], LOST, width=w, opacity=0.3)
        f0 = curve_in(B.ax, d["t"], d["f0"], MODEL, 3)
        f1 = curve_in(B.ax, d["t"], d["f1"], LOST, 3)
        assert max(d["f0"].max(), d["h0"].max()) < 2.2
        rows = rows_of([
            (r"Brown \& Heathcote, \ 2008: \ one accumulator per answer, \ racing; \ no noise within a trial", WHITE),
            (r"each starts at random below $A$ and rises in a straight line, \ its rate drawn afresh each trial", MODEL),
            (r"the first to reach $b$ answers: \ densities in closed form \ (curves), \ simulation \ (bars)", BOUND),
            (r"it fits most data as well as diffusion, \ and extends to any number of answers", GREY_A),
        ], 3.6, 20, 0.32).move_to([5.0, 0.0, 0])
        tag = psyche_tag(r"\texttt{decide.lba\_defective}, \ \texttt{lba\_simulate}; \ Brown \& Heathcote (2008)")
        with self.voiceover(
            "Diffusion isn't the only way to accumulate. <bookmark mark='a'/> In 2008 Scott Brown and Andrew "
            "Heathcote stripped the idea to its bones. Give each answer its own accumulator and let them race, with "
            "no noise within a trial at all. <bookmark mark='b'/> Each accumulator starts at a random height below A "
            "and rises in a straight line, at a rate drawn afresh on every trial. <bookmark mark='c'/> The first to "
            "reach the threshold b gives the answer. Because the lines are straight, the densities have a closed "
            "form, and Psyche's curves match its simulation. <bookmark mark='d'/> This linear ballistic accumulator "
            "fits most data about as well as diffusion does, and it extends to any number of answers. The "
            "variability between trials, not the noise within them, does the work."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(B))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(band), FadeIn(lab[0]), LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.2),
                      FadeIn(rows[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(thr), FadeIn(lab[1]), FadeIn(h0), FadeIn(h1), Create(f0), Create(f1), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def lca(self):
        head = heading(r"Leaky, \ competing accumulators")
        n1 = Circle(radius=0.6, color=MODEL, fill_opacity=0.15).move_to([-4.6, 0.6, 0])
        n2 = Circle(radius=0.6, color=LOST, fill_opacity=0.15).move_to([-1.8, 0.6, 0])
        l1 = label(r"$x_1$", font_size=30, color=MODEL).move_to(n1)
        l2 = label(r"$x_2$", font_size=30, color=LOST).move_to(n2)
        i1 = Arrow([-4.6, -1.3, 0], n1.get_bottom(), buff=0.05, color=GREY_B)
        i2 = Arrow([-1.8, -1.3, 0], n2.get_bottom(), buff=0.05, color=GREY_B)
        il = VGroup(label(r"$I_1$", font_size=24, color=GREY_A).next_to(i1, DOWN, buff=0.05),
                    label(r"$I_2$", font_size=24, color=GREY_A).next_to(i2, DOWN, buff=0.05))
        inh = VGroup(CurvedArrow(n1.get_right() + UP * 0.2, n2.get_left() + UP * 0.2, angle=-0.6, color=TIME),
                     CurvedArrow(n2.get_left() + DOWN * 0.2, n1.get_right() + DOWN * 0.2, angle=-0.6, color=TIME))
        inl = label(r"inhibition $\beta$", font_size=20, color=TIME).next_to(inh, UP, buff=0.15)
        leak = VGroup(CurvedArrow(n1.get_top() + LEFT * 0.25, n1.get_top() + RIGHT * 0.25, angle=-2.5, color=BOUND),
                      CurvedArrow(n2.get_top() + LEFT * 0.25, n2.get_top() + RIGHT * 0.25, angle=-2.5, color=BOUND))
        lkl = label(r"leak $k$", font_size=20, color=BOUND).next_to(leak[0], LEFT, buff=0.15)
        eq = MathTex(r"dx_i = \big(I_i - k\,x_i - \beta\, x_{j}\big)\,dt + \sigma\, dW_i", font_size=34,
                     color=WHITE).move_to([-3.2, -2.5, 0])
        rows = rows_of([
            (r"Usher \& McClelland, \ 2001: \ accumulators that leak, \ like neurons, \ and inhibit each other", WHITE),
            (r"leak forgets old evidence; \ inhibition makes the race a contest", BOUND),
            (r"Bogacz, \ Brown, \ Moehlis, \ Holmes \& Cohen, \ 2006: \ when leak and inhibition balance, \ "
             r"the difference $x_1 - x_2$ is a diffusion: \ the same model, \ in neurons", MODEL),
            (r"with many accumulators racing, \ a bound high enough for fixed accuracy gives Hick's logarithm \ "
             r"(chapter one)", EVIDENCE),
        ], 5.6, 22, 0.34).move_to([3.6, 0.0, 0])
        tag = published_tag(r"Usher \& McClelland (2001); \ Bogacz et al. (2006)")
        with self.voiceover(
            "Brains, though, are noisy, and neurons forget. <bookmark mark='a'/> In 2001 Marius Usher and Jay "
            "McClelland proposed accumulators that leak, as neurons do, and that inhibit each other. "
            "<bookmark mark='b'/> The leak lets old evidence fade. The inhibition turns the race into a contest: "
            "as one rises, it pushes the other down. <bookmark mark='c'/> In 2006 Rafal Bogacz and colleagues "
            "showed what ties these models together. When leak and inhibition balance, the difference between the "
            "two accumulators behaves exactly like a diffusion. The diffusion model may be what such a circuit "
            "computes. <bookmark mark='d'/> And with many accumulators, the bound that keeps accuracy fixed has to "
            "rise with the number of rivals, which is where chapter one's logarithm came from."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(n1), FadeIn(n2), FadeIn(l1), FadeIn(l2), GrowArrow(i1),
                      GrowArrow(i2), FadeIn(il))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Write(eq))
            vo.wait_until("b")
            self.play(Create(leak), FadeIn(lkl), Create(inh), FadeIn(inl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def urgency(self):
        d = load("urgency")
        head = heading(r"Should the bound fall as time passes?")
        A = axes([0, 2.5], [0, 1.1], x_length=4.4, y_length=2.4, xticks=[0, 1, 2], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", xlabel=r"time, \ s", ylabel=r"bound",
                 center=[-4.4, 1.35, 0], font_size=15)
        bf = curve(A.ax, d["tb"], d["bound_fixed"], BOUND, 3)
        bc = curve(A.ax, d["tb"], d["bound_collapse"], TIME, 3)
        B = axes([0.2, 3.0], [0, 2.4], x_length=4.4, y_length=2.4, xticks=[0.5, 1.5, 2.5], yticks=[0, 1, 2],
                 xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}", xlabel=r"response time, \ s",
                 ylabel=r"density", center=[-4.4, -2.15, 0], font_size=15)
        mids = (d["edges"][:-1] + d["edges"][1:]) / 2
        hf = curve(B.ax, mids, d["fixed_hist"], BOUND, 3)
        hc = curve(B.ax, mids, d["collapsing_hist"], TIME, 3)
        assert d["collapsing_skew"] < d["fixed_skew"] and d["collapsing_mean"] < d["fixed_mean"]
        assert max(d["fixed_hist"].max(), d["collapsing_hist"].max()) < 2.4
        key = legend([(BOUND, r"fixed"), (TIME, r"collapsing")], font_size=17).next_to(A, RIGHT, buff=0.25)
        rows = rows_of([
            (r"Cisek, \ Puskas \& El-Murr, \ 2009: \ an \emph{urgency} signal that grows with time; \ "
             r"equivalently, \ a bound that falls", WHITE),
            (r"Drugowitsch and colleagues, \ 2012: \ when time is costly or hard trials are mixed with easy ones, "
             r"\ a falling bound is the optimal policy", MODEL),
            (rf"it trims the slow tail: \ skew {d['fixed_skew']:.1f} becomes {d['collapsing_skew']:.1f}, \ "
             rf"and accuracy falls from {pct(d['fixed_acc'])} to {pct(d['collapsing_acc'])}", TIME),
            (r"Hawkins, \ Forstmann, \ Wagenmakers, \ Ratcliff \& Brown, \ 2015: \ across humans and monkeys, \ "
             r"the data mostly favour fixed bounds, \ with exceptions in long-trained monkeys", BOUND),
        ], 6.4, 21, 0.32).move_to([3.2, -0.3, 0])
        tag = psyche_tag(r"\texttt{decide.simulate\_bound}; \ drift 0.8, \ 30{,}000 trials each")
        with self.voiceover(
            "One more relative changes the bound itself. <bookmark mark='a'/> Paul Cisek and colleagues argued in "
            "2009 that an urgency signal grows as a trial goes on, so that less and less evidence is needed: a bound "
            "that falls with time. <bookmark mark='b'/> Jan Drugowitsch and colleagues showed in 2012 that a "
            "falling bound is actually the best policy when time costs something, or when hard and easy trials are "
            "mixed and a slow trial is probably a hopeless one. <bookmark mark='c'/> A collapsing bound trims the "
            "slow tail of the distribution and makes it less skewed, at some cost in accuracy. "
            "<bookmark mark='d'/> But do people do it? In 2015 Guy Hawkins and colleagues compared fixed and "
            "collapsing bounds on data from humans and monkeys in three kinds of task. The data mostly favoured "
            "fixed bounds, with exceptions in monkeys trained for a long time. Urgency is optimal under some "
            "conditions, and those are not the ones most experiments create."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(B))
            vo.wait_until("a")
            self.play(Create(bf), Create(bc), FadeIn(key), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(hf), Create(hc), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
