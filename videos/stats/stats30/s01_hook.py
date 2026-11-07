from __future__ import annotations

import numpy as np

from videos.stats.stats30.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.rejection()
        self.duel()
        self.curve()
        self.newcomb()
        self.estimates()
        self.stigler()
        self.lesson()
        self.objectives()

    def story(self):
        tl = timeline(lit=(1960,)).to_edge(UP, buff=0.35)
        hc = history_card(1960, r"John Tukey, \ `A survey of sampling from contaminated distributions'",
                          r"which estimates the spread of a sample better, \ the standard deviation or the mean "
                          r"absolute deviation? \ For normal data the standard deviation, \ by 12\%. \ Now let one "
                          r"observation in a few hundred come from a wider normal",
                          color=PATH, width=11.0, font_size=23).move_to([0, 1.0, 0])
        rows = fit_rows(VGroup(
            label(r"Fisher (1920) had settled it for normal data: \ $s$ wins", font_size=24),
            label(r"Tukey asked what happens when the data are \emph{almost} normal", font_size=24, color=PATH),
        ), 12.0, 0.35, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1920 Fisher settled an argument with Arthur Eddington: for normal data, the standard "
            "deviation estimates spread better than the mean absolute deviation, about twelve percent better. "
            "<bookmark mark='b'/> In 1960 John Tukey asked what happens when the data are almost normal: most observations "
            "from one normal, and now and then one from a normal three times as wide, a gross error. "
            "<bookmark mark='c'/> His answer reshaped statistics."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(rows[1]))
            vo.wait_until("c")
        self.clear_scene()

    def duel(self):
        rows = [
            cmath(r"F_\varepsilon", r"=", r"(1 - \varepsilon) N(\mu, \sigma^2) + \varepsilon N(\mu, 9\sigma^2)", font_size=30),
            cmath(r"s", r"=", r"\sqrt{\tfrac{1}{n-1}\textstyle\sum (x_i - \bar x)^2}", font_size=30),
            cmath(r"d", r"=", r"\tfrac1n \textstyle\sum |x_i - \bar x|", font_size=30),
            cmath(r"\text{ARE}(d : s)", r"=", r"\dfrac{(\mu_4/\sigma^4 - 1)/4}{\sigma^2/\delta^2 - 1}", font_size=30),
        ]
        rows[3][2].set_color(PATH)
        whys = [why(r"the contaminated normal"), why(r"squares magnify the far points"), why(r"absolute values don't, \ as much"),
                why(r"both coefficients of variation, \ asymptotically; \ $\delta = E|X - \mu|$")]
        with self.voiceover(
            "<bookmark mark='a'/> Tukey's model: a share epsilon of the observations comes from a normal with three "
            "times the standard deviation, the rest from the main normal. <bookmark mark='b'/> The standard deviation"
            " squares each deviation, which magnifies the far points. <bookmark mark='c'/> The mean absolute "
            "deviation doesn't, as much. <bookmark mark='d'/> Compare them by the ratio of their squared coefficients"
            " of variation: the kurtosis minus one, divided by four, against variance divided by mean absolute "
            "deviation squared, minus one."
        ) as vo:
            intro=label('A small wider-normal component changes relative precision',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def curve(self):
        d = load("tukey")
        eps, are = np.asarray(d["eps"]), np.asarray(d["are"])
        A = axes([0, 0.1], [0.8, 2.2], x_length=7.4, y_length=4.4, xlabel=r"share of gross errors $\varepsilon$",
                 ylabel=r"efficiency of $d$ relative to $s$", xticks=[0, 0.02, 0.05, 0.1], yticks=[1, 1.5, 2],
                 xfmt=lambda v: f"{v:g}", center=[-2.0, 0.3, 0])
        ax = A.ax
        c = polyline(ax, eps, are, PATH, 3.5)
        one = DashedLine(ax.c2p(0, 1), ax.c2p(0.1, 1), color=GREY_B, stroke_width=2)
        cross = Dot(ax.c2p(d["cross"], 1), radius=0.08, color=RES)
        rows = fit_rows(VGroup(
            label(rf"$\varepsilon = 0$: \ {d['are0']:.3f}: \ $s$ wins by 12\%", font_size=22),
            label(rf"break-even at $\varepsilon = {d['cross']:.4f}$: \ 1 in {1 / d['cross']:.0f}", font_size=22, color=RES),
            label(rf"$\varepsilon = 0.01$: \ $d$ is {d['are_001']:.2f} times as efficient", font_size=22, color=PATH),
            label(rf"$\varepsilon = 0.05$: \ {d['are_005']:.2f} times", font_size=22, color=PATH),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> At epsilon zero, the standard deviation wins, as Fisher said: the mean deviation is"
            " only eighty-eight percent as efficient. <bookmark mark='b'/> But the curve rises fast. They break even "
            "at epsilon of point oh oh one eight: one gross error in five hundred and seventy observations. <bookmark"
            " mark='c'/> At one in a hundred, the crude mean deviation is forty-four percent more efficient. "
            "<bookmark mark='d'/> At one in twenty, twice as efficient. This shows sensitivity to one specific "
            "wider-normal mixture, rather than a measured universal rate of errors in real data. An optimal procedure"
            " for a model can perform poorly nearby."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), Create(one))
            vo.wait_until("a")
            self.play(Create(c), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(cross), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def newcomb(self):
        d = load("newcomb")
        x = np.asarray(d["x"])
        A = axes([-50, 45], [0, 12], x_length=10.4, y_length=3.6, xlabel=r"passage time $-$ 24,800 ns",
                 ylabel=r"count", xticks=[-40, -20, 0, 20, 40], yticks=[0, 5, 10], center=[-0.4, 0.6, 0])
        ax = A.ax
        edges = np.arange(-50, 46, 2.0)
        cnt = np.histogram(x, edges)[0]
        bars = hist_bars(ax, edges, cnt, color=DATA, opacity=0.75)
        tru = DashedLine(ax.c2p(d["true"], 0), ax.c2p(d["true"], 11.5), color=TRUE, stroke_width=3)
        rows = fit_rows(VGroup(
            label(r"Simon Newcomb, \ 1882: \ the time light takes to cross the Potomac and back, \ 66 times", font_size=22),
            label(rf"two strays: \ {d['outliers'][0]:g} and {d['outliers'][1]:g}", font_size=22, color=RES),
            label(rf"gold: \ the modern value, \ {d['true']}", font_size=22, color=TRUE),
        ), 12.0, 0.22, [0, -2.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Real data, with a known answer. In 1882 Simon Newcomb timed light crossing the "
            "Potomac to a mirror and back, in a series of sixty-six measurements. Stephen Stigler used his "
            "measurements in 1977 to test estimators against the truth. <bookmark mark='b'/> Most cluster in the "
            "twenties and thirties; two stray far below, at minus forty-four and minus two. <bookmark mark='c'/> The "
            "modern value of the speed of light corresponds to thirty-three point oh two on this scale."
        ) as vo:
            self.add(newcomb_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.02), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Indicate(VGroup(bars[3], bars[24]), color=RES), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(tru), FadeIn(rows[2]))
        self.clear_scene()

    def estimates(self):
        d = load("newcomb")
        a, c = d["all"], d["clean"]
        hdr = [r"\textbf{estimate}", r"\textbf{all 66}", r"\textbf{without the two strays}"]
        spec = (("mean", r"mean"), ("median", r"median"), ("trim10", r"10\% trimmed mean"), ("hl", r"Hodges--Lehmann"),
                ("huber", r"Huber"), ("biweight", r"biweight"))
        body = [[t, f"{a[k]['est']:.2f}", f"{c[k]['est']:.2f}"] for k, t in spec]
        tb = table_rows([hdr] + body, font_size=26, col_buff=1.0, row_buff=0.28, colors=[GREY_A, MEANC, MEDC, TRIMC, HLC, HUBC, BIWC])
        tb.move_to([0, 0.7, 0])
        foot = fit_rows(VGroup(
            label(r"the mean moves by 1.5 when the strays go; \ the others by 0.5 or less", font_size=22),
            label(rf"and none comes near {d['true']}: \ robustness fixes outliers, \ not systematic error", font_size=22, color=RES),
        ), 12.0, 0.22, [0, -2.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Six estimates of the centre. The mean of all sixty-six is twenty-six point two; "
            "drop the two strays and it jumps to twenty-seven point seven five. <bookmark mark='b'/> The median, the "
            "trimmed mean, Hodges–Lehmann, Huber's and the biweight barely notice: the robust estimates range from "
            "about twenty-seven to twenty-seven point seven across these analyses. That is robustness. <bookmark "
            "mark='c'/> And not one of them reaches thirty-three. The remaining discrepancy suggests a systematic "
            "component that these location estimators do not remove; Stigler's real lesson was that robustness "
            "protects against stray points, not against bias."
        ) as vo:
            self.add(newcomb_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(tb[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tb[2:]], lag_ratio=0.3), FadeIn(foot[0]), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"optimal under the model is not good near the model", font_size=26),
            label(r"efficiency: \ how much you lose when the model is true", font_size=26, color=HLC),
            label(r"influence and breakdown: \ how much a few bad points can do", font_size=26, color=RES),
            label(r"the goal: \ lose little when all is well, \ and fail gracefully when it isn't", font_size=26, color=PATH),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The lesson: an estimator that is optimal when the model is exactly true can be poor when "
            "the model is nearly true. <bookmark mark='b'/> This part measures estimators in two ways: efficiency, how much "
            "we lose when the model holds; <bookmark mark='c'/> and influence and breakdown, how much damage a few bad points "
            "can do. <bookmark mark='d'/> The goal is to lose little when all is well, and to fail gracefully when it isn't."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 30", font_size=34, color=GREY_B), label(r"Robust Statistics", font_size=60)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"Pitman efficiency: \ Wilcoxon bound in a regular location model",
            r"Hodges--Lehmann; \ influence functions; \ breakdown",
            r"Huber's minimax M-estimator; \ robust scale",
            r"robust regression and covariance: \ LTS, \ MM, \ MCD",
            r"heavy-tailed means: \ median of means; \ contamination on the World",
        ], color=HLC, font_size=26)
        prereq = note(r"prerequisites: \ Parts 16, \ 22 and 23").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.robust}; \ the estimator rail").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part thirty: robust statistics. <bookmark mark='b'/> We'll derive the efficiency of"
            " rank methods and prove the Wilcoxon local asymptotic bound under a regular continuous symmetric "
            "location model with finite variance; build the Hodges–Lehmann estimator; measure influence and "
            "breakdown; derive Huber's minimax estimator; estimate scale robustly; fit regressions and covariances "
            "that refuse to be dragged; estimate means of heavy-tailed data; and test it all on contaminated samples "
            "from the World."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()

    def stigler(self):
        rows = [
            cmath(r"\text{Stigler (1977)}", r":", r"\text{24 historical data sets with known answers}", font_size=30),
            cmath(r"\text{best}", r":", r"\text{light trimming was competitive}", font_size=30),
            cmath(r"\text{the mean}", r":", r"\text{surprisingly close behind}", font_size=30),
            cmath(r"\text{heavy robustness}", r":", r"\text{does not remove a common systematic error}", font_size=30),
        ]
        rows[2][2].set_color(PATH)
        whys = [why(r"Cavendish, \ Michelson, \ Newcomb"), why(r"light trimming"), why(r"most real errors were modest"),
                why(r"`Do robust estimators deal with real data?'")]
        with self.voiceover(
            "<bookmark mark='a'/> Stigler did this for twenty-four historical data sets with known answers: "
            "Cavendish's density of the earth, Michelson's and Newcomb's speeds of light. <bookmark mark='b'/> "
            "Lightly trimmed means were competitive in this historical comparison. <bookmark mark='c'/> The plain "
            "mean was surprisingly close behind. <bookmark mark='d'/> Aggressive resistance to isolated outliers does"
            " not remove a common systematic measurement error. Our Newcomb calculation illustrates that limitation; "
            "it does not establish a universal ranking of estimators. Robustness is insurance, not a cure."
        ) as vo:
            intro=label('Resistance to isolated points does not remove a common systematic shift',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def rejection(self):
        rows = [
            cmath(r"\text{Peirce (1852)}", r":", r"\text{a criterion for rejecting doubtful observations}", font_size=28),
            cmath(r"\text{Chauvenet (1863)}", r":", r"\text{reject if } n\, P(|Z| > z_i) < \tfrac12", font_size=30),
            cmath(r"\text{Newcomb (1886)}", r":", r"\text{model the errors as a mixture of normals}", font_size=30),
            cmath(r"\text{the problem}", r":", r"\text{rules use the mean and SD the outliers distort}", font_size=30),
        ]
        rows[2][2].set_color(PATH)
        whys = [why(r"astronomers first"), why(r"a rule of thumb, \ widely taught"), why(r"Tukey's model, \ 74 years early"),
                why(r"masking: \ chapter six")]
        with self.voiceover(
            "<bookmark mark='a'/> The problem is old. Astronomers argued about discarding doubtful observations for a century: "
            "Benjamin Peirce proposed a criterion in 1852, <bookmark mark='b'/> and William Chauvenet's rule of 1863, reject "
            "a point if fewer than half an observation that extreme is expected, was taught for generations. "
            "<bookmark mark='c'/> Newcomb himself, in 1886, modelled measurement errors as a mixture of normals with "
            "different spreads, Tukey's model seventy-four years early. <bookmark mark='d'/> The rules' weakness is that they "
            "judge points by the mean and standard deviation that the outliers themselves distort."
        ) as vo:
            intro=label('Classical rejection rules can be distorted by the points they judge',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
