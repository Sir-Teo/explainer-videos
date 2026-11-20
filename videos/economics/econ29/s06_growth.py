from __future__ import annotations

from videos.economics.econ29.common import *  # noqa: F403


class Growth(VoiceoverScene):
    def construct(self):
        card(self, 5, r"The stochastic growth model", r"What should an economy save when its luck changes?",
             "Chapter five. The stochastic growth model.", lit={1972: r"Brock and Mirman", 1986: r"Tauchen"},
             scale=("nation",), horizon=("a year", "a century"))
        self.model()
        self.chains()
        self.grid()

    def model(self):
        B = load("bm")
        p = B["path"]
        T = 100
        z = 100 * np.array(p["z"])[:T]
        y = np.log(np.array(p["y"])[:T])
        y = 100 * (y - y.mean())
        eq = MathTex(r"V(k, z) = \max_{k'}\ \Big\{ \log\big(z k^{\alpha} - k'\big) + \beta\, "
                     r"\mathbb{E}\big[ V(k', z') \mid z \big] \Big\}", font_size=32).to_edge(UP, buff=0.35)
        sol = MathTex(r"k' = \alpha\beta\, z k^{\alpha}", r"\qquad c = (1 - \alpha\beta)\, z k^{\alpha}",
                      font_size=32, color=POLICY).next_to(eq, DOWN, buff=0.3)
        ax = plane([0, T], [-20, 20], center=LEFT * 1.9 + DOWN * 1.35, x_length=8.6, y_length=3.4,
                   xticks=[0, 25, 50, 75, 100], yticks=[-15, 0, 15], xlabel=r"year",
                   ylabel=r"\% from average", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        zero = seg(ax, 0, 0, T, 0, GREY_D, 1.2)
        zl = path(ax, np.arange(T), np.clip(z, -20, 20), TECH, 2, smooth=False)
        yl = path(ax, np.arange(T), np.clip(y, -20, 20), OUTPUT, 3, smooth=False)
        side = VGroup(
            label(r"Brock and Mirman, \ 1972: \\ log utility, \ capital used up \\ in a year: \ a closed form",
                  font_size=18, color=E.ACCENT),
            label(rf"save $\alpha\beta = {B['saving_rate']:.2f}$ of output, \\ whatever happens", font_size=18,
                  color=POLICY),
            label(r"red: \ technology $z$", font_size=18, color=TECH),
            label(r"green: \ output, \ more persistent: \\ capital carries good years forward",
                  font_size=18, color=OUTPUT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3).shift(DOWN * 1.1)
        tag = published_tag(r"Brock and Mirman, \ \emph{Journal of Economic Theory} 4(3) (1972); \ the Island: \ "
                            r"simulated", corner=DR, font_size=12)
        with self.voiceover(
            "Now replace the cake with an economy. Output is made from capital, k, with a technology level, z, that "
            "changes at random. <bookmark mark='a'/> Each year the economy splits output between eating and next "
            "year's capital, and the Bellman equation now has two states, capital and technology, and an expectation "
            "over next year's luck. <bookmark mark='b'/> William Brock and Leonard Mirman studied this model in "
            "1972. With log utility and capital that is used up within the year, it has a closed form: "
            f"<bookmark mark='c'/> save a share alpha beta of output, {B['saving_rate']:.2f}, whatever happens, and "
            "eat the rest. <bookmark mark='d'/> Here is a century of it on the Island. In red, technology. "
            "<bookmark mark='e'/> In green, output. A good year raises output, and because a fixed share is saved, "
            "it also raises next year's capital, so output's swings last longer than technology's. Capital is the "
            "model's propagation mechanism."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(eq), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(Write(sol), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(ax), FadeIn(zero), Create(zl), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("e")
            self.play(Create(yl), FadeIn(side[3]), run_time=1.5)
        self.clear_scene()

    def _matrix(self, P, color, size=0.32):
        P = np.array(P)
        n = len(P)
        g = VGroup()
        for i in range(n):
            for j in range(n):
                g.add(Square(side_length=size, stroke_color=GREY_D, stroke_width=0.6, fill_color=color,
                             fill_opacity=float(np.clip(P[i, j], 0, 1) ** 0.6)).move_to(
                    RIGHT * j * size + DOWN * i * size))
        return g

    def chains(self):
        C = load("chains")
        lo, hi = (C["chains"][f"{r:g}"] for r in C["rhos"])
        mats = VGroup()
        for row, r in ((lo, C["rhos"][0]), (hi, C["rhos"][1])):
            for name, col in (("tauchen", TECH), ("rouwenhorst", VALUE)):
                m = self._matrix(row[name]["P"], col)
                t = label(rf"{name.capitalize()}, \ $\rho = {r}$", font_size=18, color=col).next_to(m, UP,
                                                                                                    buff=0.12)
                mats.add(VGroup(m, t))
        mats.arrange_in_grid(rows=2, cols=2, buff=(0.7, 0.55)).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        t_lo, r_lo = lo["tauchen"], lo["rouwenhorst"]
        side = VGroup(
            label(r"seven states for technology; \\ row: \ today; \ column: \ tomorrow", font_size=19,
                  color=GREY_A),
            label(rf"$\rho = {C['rhos'][0]}$: \ the truth: \ s.d.\ {100 * lo['sd_true']:.2f}\%, \ autocorrelation "
                  rf"{C['rhos'][0]}", font_size=19, color=WHITE),
            label(rf"Tauchen: \ {100 * t_lo['sd']:.2f}\% \ and \ {t_lo['rho']:.3f}", font_size=19, color=TECH),
            label(rf"Rouwenhorst: \ {100 * r_lo['sd']:.2f}\% \ and \ {r_lo['rho']:.3f}", font_size=19,
                  color=VALUE),
            label(rf"$\rho = {C['rhos'][1]}$: \ Tauchen's chain never moves \\ (it stays put with probability "
                  rf"{np.min(np.diag(hi['tauchen']['P'])):.4f}); \\ Rouwenhorst's stays exact", font_size=19,
                  color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).to_edge(RIGHT, buff=0.4)
        tag = published_tag(r"Tauchen, \ \emph{Economics Letters} 20 (1986); \ Rouwenhorst (1995); \ Kopecky and "
                            r"Suen, \ \emph{RED} 13 (2010)", corner=DR, font_size=12)
        head = label(r"luck on a computer: \ a Markov chain", font_size=26, color=E.ACCENT).to_edge(UP, buff=0.35)
        with self.voiceover(
            "A computer cannot hold a continuous random variable, so technology is squeezed onto a few values, with "
            "a table of probabilities for moving between them: a Markov chain. <bookmark mark='a'/> Here are four "
            "such tables, each with seven states. A row is today's state, a column tomorrow's, and a brighter square "
            "a likelier move. <bookmark mark='b'/> The aim is to copy a process with persistence "
            f"{C['rhos'][0]}, whose true standard deviation is {100 * lo['sd_true']:.2f} percent. "
            "<bookmark mark='c'/> George Tauchen's method of 1986, the old standard, gets "
            f"{100 * t_lo['sd']:.2f} percent and a persistence of {t_lo['rho']:.3f}: close, but off. "
            "<bookmark mark='d'/> The method of Geert Rouwenhorst, revived by Kopecky and Suen in 2010, matches "
            "both exactly. <bookmark mark='e'/> And when persistence is very high, at "
            f"{C['rhos'][1]}, Tauchen's chain breaks altogether: its states are so far apart that it never moves, "
            "while Rouwenhorst's is still exact. Small numerical choices like this decide whether a solved model "
            "means anything."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in mats], lag_ratio=0.3), FadeIn(side[0]), run_time=2)
            for mk, r_ in zip("bcde", side[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def grid(self):
        B = load("bm")
        F, P = B["full"], B["part"]
        k = np.array(P["k"])
        kp = np.array(P["kprime"])
        lo, hi = float(k[0]), float(k[-1])
        ax = plane([lo, hi], [-0.45, 0.45], center=LEFT * 2.6 + DOWN * 0.3, x_length=6.0, y_length=4.8,
                   xticks=[2.5, 3.5, 4.5, 5.5], yticks=[-0.4, -0.2, 0, 0.2, 0.4], xlabel=r"capital today, \ $k$",
                   ylabel=r"net investment, \ $k' - k$", xfmt=lambda v: f"{v:.1f}",
                   yfmt=lambda v: f"{v:+.1f}" if abs(v) > 1e-9 else "0", font_size=15)
        zero = seg(ax, lo, 0, hi, 0, GREY_C, 2, dashed=True)
        cols = [interpolate_color(ManimColor(TECH), ManimColor(OUTPUT), j / 4) for j in range(5)]
        lines = VGroup(*[path(ax, k, kp[j] - k, cols[j], 2.5, smooth=False, yr=(-0.45, 0.45)) for j in range(5)])
        cross = VGroup(*[dot(ax, float(k[np.argmin(np.abs(kp[j] - k))]), 0, cols[j], 0.07) for j in range(5)])
        side = VGroup(
            label(rf"capital used up each year: \ the grid's policy \\ is within {100 * F['max_rel_err']:.2f}\% of "
                  rf"Brock and Mirman's formula \\ (one grid step is {100 * F['step_rel']:.2f}\%)", font_size=18,
                  color=POLICY),
            label(r"now let capital last: \ 10\% wears out a year; \\ no formula exists", font_size=18,
                  color=GREY_A),
            label(r"five lines: \ how much capital grows \\ in each of five technology states, \\ bad (red) to "
                  r"good (green)", font_size=18, color=E.ACCENT),
            label(r"dots: \ where capital would stay put; \\ good luck, \ a bigger target", font_size=18,
                  color=OUTPUT),
            label(rf"{P['iterations']} iterations; \ the method \\ does not care that no formula exists",
                  font_size=18, color=VALUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Now solve the growth model the way the computer solved the cake: a grid for capital, a chain for "
            "technology, and value function iteration. <bookmark mark='a'/> First the test. With capital used up "
            "each year, the grid's policy is within "
            f"{100 * F['max_rel_err']:.2f} percent of Brock and Mirman's formula, less than one step of the grid. "
            "<bookmark mark='b'/> Then the real case: capital lasts, with a tenth wearing out each year, and there "
            "is no formula. <bookmark mark='c'/> Here is how much capital grows, against how much there is, one "
            "line for each of five technology states, from bad in red to good in green. <bookmark mark='d'/> Each "
            "line crosses zero where capital would stay the same: with good luck the economy builds towards more "
            "capital, with bad luck it runs capital down towards less. <bookmark mark='e'/> The computer took "
            f"{P['iterations']} iterations and did not care that no formula exists. That is the power of the method."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(ax), Create(zero))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3), FadeIn(side[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromCenter(d) for d in cross], lag_ratio=0.2), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
