from __future__ import annotations

import numpy as np

from videos.stats.stats29.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.histograms()
        self.bandwidths()
        self.critical()
        self.test()
        self.lesson()
        self.objectives()

    def story(self):
        tl = timeline(lit=(1981,)).to_edge(UP, buff=0.35)
        hc = history_card(1981, r"Bernard Silverman, \ \emph{JRSS B}",
                          r"`Using kernel density estimates to investigate multimodality.' \ How many humps does a "
                          r"distribution have? \ Smooth the data less and less until a new hump appears, \ and ask "
                          r"whether noise alone could have made it appear that soon",
                          color=PATH, width=11.0, font_size=23).move_to([0, 1.0, 0])
        rows = fit_rows(VGroup(
            label(r"Old Faithful, \ Yellowstone: \ 272 eruptions, \ R\texttt{ datasets::faithful}", font_size=24),
            label(r"how long does an eruption last?", font_size=24, color=PATH),
        ), 12.0, 0.35, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Old Faithful, in Yellowstone, erupts every hour or so. The R faithful data contain "
            "two hundred and seventy-two eruption durations and waits to the next eruption. We use the documented "
            "data without attributing an unverified collection date. <bookmark mark='b'/> How long does an eruption "
            "last? Not a mean and a standard deviation: the answer is a whole distribution, and the question this "
            "part asks is how to estimate a curve. <bookmark mark='c'/> In 1981 Bernard Silverman asked a sharper "
            "version: how many humps does the distribution have?"
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(hc, shift=UP * 0.2))
        self.clear_scene()

    def histograms(self):
        d = load("faithful")
        x = np.asarray(d["x"])
        A = axes([1, 6], [0, 0.9], x_length=7.4, y_length=4.4, xlabel=r"eruption length (minutes)", ylabel=r"density",
                 xticks=[2, 3, 4, 5], yticks=[0, 0.4, 0.8], center=[-2.0, 0.3, 0])
        ax = A.ax
        hs = {}
        for key in ("0.5_0", "0.5_0.125", "0.5_0.25", "0.5_0.375", "0.25_0", "0.25_0.125"):
            h = d["hist"][key]
            e = np.asarray(h["edges"])
            dens = np.asarray(h["dens"])
            hs[key] = hist_bars(ax, e, dens, color=HISTC, opacity=0.75)
        rg = rug(ax, x)
        rows = fit_rows(VGroup(
            label(rf"{d['n']} eruptions; \ {100 * d['short_share']:.0f}\% shorter than 3 minutes", font_size=22),
            label(r"bins 0.5 minutes wide, \ starting at 1.0", font_size=22, color=HISTC),
            label(r"the same bins, \ shifted: \ the shape changes", font_size=22, color=HISTC),
            label(r"bins 0.25 wide: \ a third hump?", font_size=22, color=RES),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The rug along the bottom shows the eruptions: about a third last two minutes or less, the "
            "rest four or more. <bookmark mark='b'/> A histogram with half-minute bins shows two humps. <bookmark mark='c'/> "
            "Slide the same bins a little to the right, and the shape changes: the tops move, a shoulder comes and goes. "
            "<bookmark mark='d'/> Halve the bin width, and the long eruptions seem to split into two. Is that third hump "
            "real, or the noise of two hundred and seventy-two observations?"
        ) as vo:
            self.add(faithful_tag())
            self.play(FadeIn(A), FadeIn(rg))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in hs["0.5_0"]], lag_ratio=0.05), FadeIn(rows[1]))
            vo.wait_until("c")
            cur = hs["0.5_0"]
            for key in ("0.5_0.125", "0.5_0.25", "0.5_0.375"):
                self.play(ReplacementTransform(cur, hs[key]), run_time=1.2)
                cur = hs[key]
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(ReplacementTransform(cur, hs["0.25_0"]), FadeIn(rows[3]), run_time=1.5)
        self.clear_scene()

    def bandwidths(self):
        d = load("faithful")
        g = np.asarray(d["grid"])
        A = axes([1, 6], [0, 0.9], x_length=7.4, y_length=4.4, xlabel=r"eruption length (minutes)", ylabel=r"density",
                 xticks=[2, 3, 4, 5], yticks=[0, 0.4, 0.8], center=[-2.0, 0.3, 0])
        ax = A.ax
        cs = {k: clip_curve(ax, g, np.asarray(d["kde"][k]), KDEC, 3, ymin=0, ymax=0.9) for k in ("h0.05", "h0.1", "h0.25", "h1")}
        m = d["modes"]
        rows = fit_rows(VGroup(
            label(r"a kernel estimate: \ a bump on every eruption, \ width $h$", font_size=22),
            label(rf"$h = 0.05$: \ {m['h0.05']} modes", font_size=22, color=KDEC),
            label(rf"$h = 0.1$: \ {m['h0.1']}", font_size=22, color=KDEC),
            label(rf"$h = 0.25$: \ {m['h0.25']}", font_size=22, color=KDEC),
            label(rf"$h = 1$: \ {m['h1']}", font_size=22, color=KDEC),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Part 16's kernel estimate removes the bin edges: put a small normal bump on every eruption "
            "and add them up. One choice remains, the bumps' width h. <bookmark mark='b'/> At h of point oh five the curve "
            "has twelve modes, one for every little clump. <bookmark mark='c'/> At point one, three. <bookmark mark='d'/> At "
            "a quarter of a minute, two. <bookmark mark='e'/> At a full minute, one: everything is smoothed into a single "
            "lump. The number of humps is a function of the bandwidth, so the question becomes: how much smoothing is too "
            "little?"
        ) as vo:
            self.add(faithful_tag())
            self.play(FadeIn(A), FadeIn(rug(ax, d["x"])))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            cur = None
            for k, (key, m_) in enumerate((("h0.05", "b"), ("h0.1", "c"), ("h0.25", "d"), ("h1", "e"))):
                vo.wait_until(m_)
                if cur is None:
                    self.play(Create(cs[key]), FadeIn(rows[k + 1]))
                else:
                    self.play(ReplacementTransform(cur, cs[key]), FadeIn(rows[k + 1]), run_time=1.5)
                cur = cs[key]
        self.clear_scene()

    def critical(self):
        d = load("faithful")
        c = d["critical"]
        rows = [
            cmath(r"h_k", r"=", r"\min\{h : \hat f_h \text{ has at most } k \text{ modes}\}", font_size=30),
            cmath(r"h_1", r"=", rf"{c['1']:.3f}", font_size=34),
            cmath(r"h_2", r"=", rf"{c['2']:.3f}", font_size=34),
            cmath(r"h_3", r"=", rf"{c['3']:.3f}", font_size=34),
        ]
        rows[1][2].set_color(RES)
        whys = [why(r"the critical bandwidth: \ modes only vanish as $h$ grows"), why(r"one hump needs a lot of smoothing"),
                why(r"two humps need far less"), why(r"a third appears just below")]
        with self.voiceover(
            "<bookmark mark='a'/> Silverman's key fact: with a normal kernel, modes can only disappear as h grows, never "
            "appear. So for each k there is a critical bandwidth, the smallest h at which the estimate has at most k modes. "
            "<bookmark mark='b'/> To squeeze Old Faithful into one hump takes h of point eight three, a huge amount of "
            "smoothing. <bookmark mark='c'/> Two humps need only point one three. <bookmark mark='d'/> And a third appears "
            "just below, at point oh nine. A large critical bandwidth is evidence against k modes, if we know how large it "
            "would be by chance."
        ) as vo:
            self.add(faithful_tag())
            intro=label('Gaussian KDE mode counts decrease with bandwidth in one dimension',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def test(self):
        d = load("faithful")
        t = d["tests"]
        hdr = [r"\textbf{$H_0$: at most $k$ modes}", r"\textbf{critical} $h_k$", r"\textbf{bootstrap $p$-value (500)}", r"\textbf{verdict}"]
        body = [[f"$k = {k}$", f"{t[k]['h']:.3f}", f"{t[k]['p']:.3f}", v] for k, v in
                (("1", r"rejected"), ("2", r"not rejected"), ("3", r"not rejected"))]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.9, row_buff=0.32, colors=[GREY_A, RES, HIT, HIT])
        tb.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"smoothed bootstrap from $\hat f_{h_k}$, \ rescaled to the sample variance", font_size=22),
            label(r"two humps, \ short and long eruptions: \ no compelling evidence for a third mode", font_size=22, color=PATH),
        ), 12.0, 0.22, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Silverman's test: simulate from the k-mode estimate itself, by resampling the data "
            "and adding kernel noise, and see how often the simulated data need more smoothing than h k to reach k "
            "modes. <bookmark mark='b'/> One mode: never, in five hundred tries. Rejected. <bookmark mark='c'/> Two "
            "modes: half the time, so this calculation does not reject at most two modes. <bookmark mark='d'/> Three:"
            " ninety-three percent. The two broad humps are clear; the test supplies no compelling evidence for an "
            "additional mode. These are raw smoothed-bootstrap results, whose nominal levels need calibration; "
            "non-rejection does not prove the number of modes. Getting there needed every idea in this part: how a "
            "curve estimate's error depends on its smoothing."
        ) as vo:
            self.add(faithful_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(foot[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(tb[k + 1]))
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"a curve has infinitely many parameters: \ no finite family is obliged to contain it", font_size=26),
            label(r"every curve estimate smooths: \ bins, \ bandwidths, \ penalties", font_size=26, color=KDEC),
            label(r"too little: \ noise; \ \ too much: \ bias", font_size=26, color=RES),
            label(r"the right amount: \ a rate, \ $n^{-4/5}$, \ and it decays with dimension", font_size=26, color=PATH),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Part 28 chose among models with a fixed number of parameters. A curve has "
            "infinitely many, and no finite family need contain it. <bookmark mark='b'/> Every method in this part "
            "smooths: by bin width, bandwidth or penalty. <bookmark mark='c'/> Too little smoothing and you see "
            "noise; too much and you flatten real structure. <bookmark mark='d'/> For a twice-smooth density class, "
            "optimal worst-case integrated squared error has rate n to the minus four fifths. The rate depends on "
            "smoothness and deteriorates with dimension."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 29", font_size=34, color=GREY_B), label(r"Smoothing", font_size=60)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"histograms and kernel estimates: \ bias, \ variance, \ rates",
            r"choosing the bandwidth; \ the curse of dimensionality",
            r"local polynomials; \ smoothing splines; \ GCV and REML",
            r"kernels and the representer theorem; \ wavelets",
            r"additive models; \ honest intervals for curves; \ shape constraints",
        ], color=KDEC, font_size=26)
        prereq = note(r"prerequisites: \ Parts 16, \ 23 and 25").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.smooth}; \ the spline spectrum").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part twenty-nine: smoothing. <bookmark mark='b'/> We'll derive the error of histograms and "
            "kernel estimates and their optimal rates; choose bandwidths from the data; meet the curse of dimensionality; fit "
            "regression curves by local polynomials and smoothing splines, and choose their smoothness by GCV and REML; see "
            "why kernels and splines are the same idea; denoise with wavelets; fit additive models; build intervals for "
            "curves that are honest about bias; and estimate curves known only to be monotone."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
