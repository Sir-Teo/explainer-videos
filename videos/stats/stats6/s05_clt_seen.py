from __future__ import annotations

import numpy as np
from scipy import stats as st

from videos.stats.stats6.common import *  # noqa: F403


class CLTSeen(VoiceoverScene):
    def construct(self):
        self.card()
        self.convolution()
        self.cumulants()
        self.board()
        self.universal()

    def card(self):
        card = chapter_card(4, r"The central limit theorem, seen", r"Why the bell curve, \ from almost anything", lit=(1733, 1810),
                            part=PART)
        with self.voiceover("Chapter four. The central limit theorem, seen."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def convolution(self):
        d = load("lopsided")
        mu, var = d["mu"], d["var"]
        A = axes([-3.6, 3.6], [0, 1.1], x_length=8.4, y_length=4.4, xlabel=r"standardized sum \ $(S_n - n\mu)/(\sigma\sqrt{n})$",
                 xticks=[-3, -2, -1, 0, 1, 2, 3], yticks=[0, 0.5, 1], center=[-1.6, -0.6, 0])
        ax = A.ax

        def bars(n):
            p = d["pmf"][str(n)]
            z, pr = np.asarray(p["z"]), np.asarray(p["p"])
            w = 1 / np.sqrt(n * var)  # spacing of the lattice in z
            dens = pr / w
            g = VGroup()
            for zz, hh in zip(z, dens):
                if -3.6 <= zz <= 3.6:
                    lo, hi = ax.c2p(zz - 0.42 * w, 0), ax.c2p(zz + 0.42 * w, hh)
                    g.add(Rectangle(width=max(0.01, hi[0] - lo[0]), height=max(1e-3, hi[1] - lo[1]), stroke_width=0,
                                    fill_color=SIM, fill_opacity=0.8).move_to([(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, 0]))
            return g
        xs = np.linspace(-3.6, 3.6, 200)
        nrm = curve(ax, xs, normal_pdf(xs), EXACT, 3)
        law = MathTex(r"P(X = k):\ \tfrac12,\ \tfrac15,\ \tfrac1{20},\ \tfrac1{50},\ \tfrac1{50},\ \tfrac{21}{100} \quad (k = 0, \dots, 5)",
                      font_size=26, color=SIM).to_edge(UP, buff=0.4)
        nl = MathTex(r"n = 1", font_size=40).move_to([4.6, 1.6, 0])
        sup = MathTex(rf"\sup |F_n - \Phi| = {d['sup']['1']:.3f}", font_size=26, color=GREY_A).next_to(nl, DOWN, buff=0.3)
        note_ = label(r"exact: \ Part 2's engine, \ in fractions", font_size=22, color=GREY_B).move_to([4.6, -0.2, 0])
        cur = bars(1)
        with self.voiceover(
            "Start with a lopsided law: a variable that's zero half the time, five a fifth of the time, and "
            "occasionally something in between. <bookmark mark='a'/> Its distribution looks nothing like a bell: "
            "two spikes at the ends. <bookmark mark='b'/> Add two independent copies, and compute the distribution of "
            "the sum exactly, by convolution, with Part 2's engine. Rescale it to mean zero and standard deviation "
            "one. <bookmark mark='c'/> Three copies. Five. <bookmark mark='d'/> Ten. <bookmark mark='e'/> Thirty. "
            "The gold curve is the standard normal density. The shape we started with is gone, and the bell has "
            "taken its place. The number on the right, the largest gap between the two CDFs, falls steadily as n grows; unlike a continuity-corrected comparison, this checks both sides of every discrete CDF jump."
        ) as vo:
            self.play(FadeIn(A), FadeIn(law))
            vo.wait_until("a")
            self.play(FadeIn(cur), FadeIn(nl), FadeIn(sup), FadeIn(note_))
            for n, m in ((2, "b"), (3, "c"), (5, None), (10, "d"), (30, "e")):
                if m:
                    vo.wait_until(m)
                new = bars(n)
                self.play(Transform(cur, new), Transform(nl, MathTex(rf"n = {n}", font_size=40).move_to(nl)),
                          Transform(sup, MathTex(rf"\sup |F_n - \Phi| = {d['sup'][str(n)]:.3f}", font_size=26,
                                                 color=GREY_A).move_to(sup)), run_time=1.2)
                if n == 3:
                    self.play(Create(nrm))
        self.clear_scene()

    def cumulants(self):
        rows = [
            cmath(r"\kappa_r(S_n)", r"=", r"n\,\kappa_r(X)", r"\qquad \text{cumulants add (Part 3)}", font_size=32),
            cmath(r"\text{skewness}(S_n)", r"=", r"\frac{n\,\kappa_3}{(n\,\kappa_2)^{3/2}}", r"=", r"\frac{\text{skewness}(X)}{\sqrt n}",
                  font_size=32),
            cmath(r"\text{excess kurtosis}(S_n)", r"=", r"\frac{n\,\kappa_4}{(n\,\kappa_2)^{2}}", r"=", r"\frac{\text{excess kurtosis}(X)}{n}",
                  font_size=32),
            cmath(r"\kappa_r\Big(\frac{S_n - n\mu}{\sqrt n\,\sigma}\Big)", r"\to", r"0 \quad (r \ge 3)", font_size=32),
        ]
        rows[1][4].set_color(S.ACCENT)
        rows[2][4].set_color(S.ACCENT)
        rows[3][2].set_color(EXACT)
        whys = [why(r"independent sums: \ the cumulant generating functions add"), why(r"asymmetry fades like $1/\sqrt n$"),
                why(r"heavy shoulders fade like $1/n$"), why(r"only the normal has every cumulant beyond the second zero")]
        intro = label('Cumulants explain the shape under moment assumptions', font_size=36)
        with self.voiceover(
            "For laws with an MGF near zero, Part 3 gives an explanation using cumulants. More general laws need the characteristic-function proof. <bookmark mark='a'/> For a sum of independent "
            "variables, every cumulant adds: the r-th cumulant of the sum is n times that of one variable. "
            "<bookmark mark='b'/> Now standardize. Skewness is the third cumulant over the variance to the power "
            "three halves; for the sum it's the original skewness divided by root n. <bookmark mark='c'/> Excess "
            "kurtosis, the fourth, is divided by n. <bookmark mark='d'/> Every cumulant beyond the second dies away, "
            "the higher ones faster. And the only distribution whose third, fourth and all higher cumulants are zero "
            "is the normal. That's the mechanism behind the theorem in this setting, and also a warning: skewness is the "
            "last feature to disappear, at the slow rate of one over root n."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.2, buff=0.58, edge=6.9)
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
        self.clear_scene()

    def board(self):
        d = load("board")
        rows_, balls = d["rows"], d["balls"]
        B = GaltonBoard(rows=rows_, center=[-2.4, -0.2, 0], dx=0.42, dy=0.27, bin_height=2.8, ball_color=SIM)
        hc = history_card(1873, r"Francis Galton's quincunx", r"built in 1873; \ described in "
                          r"\emph{Natural Inheritance} (1889): \ ``the Law of Frequency of Error \dots reigns with serenity''",
                          color=S.MUSEUM, width=5.0, font_size=20).move_to([4.2, 2.2, 0])
        bits = np.asarray(d["bits"])
        counts = np.asarray(d["counts"], float)
        rows = VGroup(
            label(r"each peg: \ left or right, \ chance $\tfrac12$", font_size=24),
            label(r"bin $k$ = number of rights: \ $\mathrm{Binomial}(12, \tfrac12)$", font_size=24),
            label(r"a sum of 12 coin flips", font_size=24, color=SIM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.2, 0.0, 0])
        built = label(r"Built: \ the Galton board", font_size=24, color=S.ACCENT).to_corner(DR, buff=0.4)
        with self.voiceover(
            "Francis Galton built a machine to show this, which he called the quincunx. <bookmark mark='a'/> Here's "
            "ours. Balls fall through twelve rows of pegs. At each peg a ball bounces left or right, with equal "
            "chance, independently. <bookmark mark='b'/> The bin it lands in counts its rightward bounces, so the bin "
            "is a sum of twelve coin flips: a binomial. Watch the first few. <bookmark mark='c'/> Most balls take a "
            "mixed route and land near the middle; to reach an end bin, a ball must bounce the same way twelve times "
            "running, which happens once in four thousand and ninety-six for each end. <bookmark mark='d'/> Six hundred balls, "
            "and the pile takes the shape of the bell. Galton wrote that the law of error reigns with serenity in "
            "the midst of the wildest confusion."
        ) as vo:
            self.play(FadeIn(B.mobjects()), FadeIn(built))
            vo.wait_until("a")
            self.play(FadeIn(hc))
            vo.wait_until("b")
            self.play(FadeIn(rows[:2]))
            first = B.drops(self, bits[:6], run_time=1.8, lag=0.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            more = B.drops(self, bits[6:40], run_time=1.2, lag=0.08)
            vo.wait_until("d")
            scale = B.bin_height * 0.9 / counts.max()
            bars = B.bars(counts, scale=scale, opacity=0.7)
            self.play(FadeOut(first), FadeOut(more), FadeIn(bars), run_time=1.5)
            sd = np.sqrt(rows_ / 4)
            exp_curve = B.curve(lambda k: balls * normal_pdf(k, rows_ / 2, sd), scale, color=EXACT)
            self.play(Create(exp_curve))
        self.clear_scene()

    def universal(self):
        n = 30
        panels = VGroup()
        specs = [("uniform", r"uniform on $(0, 1)$", lambda z: st.norm.pdf(z), None),
                 ("exp", r"exponential", None, None), ("lop", r"the lopsided law", None, None)]
        xs = np.linspace(-3.5, 3.5, 300)
        g = np.random.Generator(np.random.PCG64(30))
        draws = {"uniform": g.random((20000, n)).sum(1), "exp": g.exponential(size=(20000, n)).sum(1)}
        lop_vals = np.array([0, 1, 2, 3, 4, 5])
        lop_p = np.array([0.5, 0.2, 0.05, 0.02, 0.02, 0.21])
        draws["lop"] = g.choice(lop_vals, size=(20000, n), p=lop_p).sum(1)
        mus = {"uniform": n / 2, "exp": n, "lop": n * float(lop_vals @ lop_p)}
        sds = {"uniform": np.sqrt(n / 12), "exp": np.sqrt(n),
               "lop": np.sqrt(n * float(((lop_vals - lop_vals @ lop_p) ** 2) @ lop_p))}
        one = {"uniform": (np.linspace(-0.2, 1.2, 100), lambda x: ((x >= 0) & (x <= 1)).astype(float)),
               "exp": (np.linspace(0, 5, 100), lambda x: np.exp(-x))}
        for k, (key, nm, _, _) in enumerate(specs):
            cx = -4.4 + 4.4 * k
            A = axes([-3.6, 3.6], [0, 0.5], x_length=3.6, y_length=2.2, xticks=[-2, 0, 2], center=[cx, -1.2, 0])
            z = (draws[key] - mus[key]) / sds[key]
            ed = np.linspace(-3.6, 3.6, 37) if key != "lop" else (np.arange(draws[key].min() - 0.5, draws[key].max() + 1.5)
                                                                   - mus[key]) / sds[key]
            ed = ed[(ed >= -3.6) & (ed <= 3.6)]
            h = hist_bars(A.ax, ed, np.histogram(z, ed)[0] / (len(z) * np.diff(ed)), color=SIM, opacity=0.7)
            cv = curve(A.ax, xs, normal_pdf(xs), EXACT, 2.5)
            t = label(nm, font_size=24).move_to([cx, 2.6, 0])
            if key in one:
                xx, f = one[key]
                B = axes([xx[0], xx[-1]], [0, 1.2], x_length=2.6, y_length=1.2, center=[cx, 1.5, 0])
                top = VGroup(B, curve(B.ax, xx, f(xx), GREY_A, 2.5))
            else:
                B = axes([-0.6, 5.6], [0, 0.55], x_length=2.6, y_length=1.2, center=[cx, 1.5, 0])
                top = VGroup(B, pmf_bars(B.ax, lop_vals, lop_p, GREY_A, width=0.5))
            arrow = Arrow([cx, 0.75, 0], [cx, 0.15, 0], buff=0, color=GREY_B, stroke_width=3)
            panels.add(VGroup(t, top, arrow, A, h, cv))
        cap = MathTex(r"\text{sums of } n = 30", font_size=26, color=GREY_A).move_to([-6.0, 0.45, 0])
        take = label(r"i.i.d. ingredients, finite positive variance: an asymptotic statement", font_size=26, color=S.ACCENT).to_edge(DOWN, buff=0.3)
        tag = note(r"simulated: 20,000 sums each").to_corner(UR, buff=0.25)
        intro = label('Independent sums, one limiting shape', font_size=36)
        with self.voiceover(
            "The remarkable thing is that the ingredient hardly matters. <bookmark mark='a'/> Flat, uniform "
            "numbers; <bookmark mark='b'/> steeply skewed exponential waiting times; <bookmark mark='c'/> our "
            "lopsided law. <bookmark mark='d'/> Sum thirty of any of them, standardize, and the histogram follows "
            "the same gold curve. Abraham de Moivre found the bell in 1733 for coin tosses; Pierre-Simon Laplace "
            "saw in 1810 that it holds for sums of almost anything. <bookmark mark='e'/> Almost: the summands must be independent and identically distributed with finite positive variance; no universal finite sample size guarantees a close normal approximation. Chapter ten shows what happens when it isn't."
        ) as vo:
            self.play(FadeIn(intro))
            self.play(FadeIn(tag))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(panels[k][:3]))
            vo.wait_until("d")
            self.play(*[FadeIn(p[3:]) for p in panels], FadeIn(cap))
            vo.wait_until("e")
            self.play(FadeIn(take))
        self.clear_scene()
