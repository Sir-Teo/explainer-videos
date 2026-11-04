from __future__ import annotations

import numpy as np

from videos.stats.stats6.common import *  # noqa: F403


class Floods(VoiceoverScene):
    def construct(self):
        self.card()
        self.flood()
        self.data()
        self.fit()
        self.levels()
        self.profile()
        self.dantzig()

    def card(self):
        card = chapter_card(13, r"Floods and return levels", r"Predicting the worst from what we have seen", part=PART)
        with self.voiceover("Chapter thirteen. Floods and return levels."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def flood(self):
        hc = history_card(1953, r"the North Sea flood, \ night of 31 January -- 1 February",
                          r"a storm surge on a spring tide breaches the dikes of Zeeland and South Holland: \ 1,836 dead in the "
                          r"Netherlands, \ more than 300 in England", color=S.MUSEUM, width=8.4, font_size=24).move_to([0, 1.5, 0])
        rows = VGroup(label(r"the Delta Committee: \ how high must the dikes be?", font_size=26),
                      label(r"its mathematician, David van Dantzig: \ an economic answer (1956)", font_size=26, color=GREY_A),
                      label(r"the standard adopted for central Holland: \ fail at most once in 10,000 years", font_size=26,
                            color=S.ACCENT)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(hc, DOWN, buff=0.6)
        with self.voiceover(
            "On the night of the thirty-first of January 1953, a storm surge driven down the North Sea arrived with a "
            "spring tide. <bookmark mark='a'/> The dikes of the south-west Netherlands broke in dozens of places. "
            "Eighteen hundred and thirty-six people died in the Netherlands, and more than three hundred in "
            "England. <bookmark mark='b'/> The Dutch government set up the Delta Committee to decide how high the "
            "defences must be. <bookmark mark='c'/> Its mathematician, David van Dantzig, treated it as a problem of "
            "statistics and economics together. <bookmark mark='d'/> The standard that emerged for the heart of "
            "Holland: the defences should fail, on average, at most once in ten thousand years. To set a height for "
            "that, you must estimate a sea level that no one has ever seen."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m in enumerate("bcd"):
                vo.wait_until(m)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def data(self):
        d = load("portpirie")
        x, yrs = np.asarray(d["x"]), np.asarray(d["years"])
        A = axes([1920, 1990], [3.4, 4.8], x_length=9.6, y_length=4.4, xlabel=r"year", ylabel=r"annual maximum sea level (m)",
                 xticks=[1930, 1950, 1970, 1990], yticks=[3.5, 4.0, 4.5], center=[-0.6, -0.6, 0])
        ax = A.ax
        stems = VGroup(*[Line(ax.c2p(y, 3.4), ax.c2p(y, v), color=DATA, stroke_width=2.5, stroke_opacity=0.7) for y, v in zip(yrs, x)])
        tops = VGroup(*[Dot(ax.c2p(y, v), radius=0.045, color=DATA) for y, v in zip(yrs, x)])
        mx = Dot(ax.c2p(d["max_year"], d["max"]), radius=0.1, color=BOUND)
        ml = MathTex(rf"{d['max']:.2f}\ \text{{m}},\ {d['max_year']}", font_size=26, color=BOUND).next_to(mx, UR, buff=0.08)
        tag = historical_tag(r"Port Pirie, South Australia, \ 1923--1987 (Coles 2001)", corner=DR)
        with self.voiceover(
            "We'll use a record that statisticians have studied for decades. <bookmark mark='a'/> Port Pirie, a "
            "harbour town in South Australia: the highest sea level of each year from 1923 to 1987, sixty-five "
            "values. These are maxima, each the largest of a whole year of tides, so the law of maxima says they "
            "should follow a generalized extreme value distribution. <bookmark mark='b'/> The highest in the record, "
            "four point six nine metres, came in 1934."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(s) for s in stems], lag_ratio=0.03), FadeIn(tops, lag_ratio=0.03), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(mx), FadeIn(ml))
        self.clear_scene()

    def fit(self):
        d = load("portpirie")
        x = np.asarray(d["x"])
        mu, s, xi = d["mu"], d["sigma"], d["xi"]
        A = axes([3.4, 4.9], [0, 2.4], x_length=6.4, y_length=4.0, xlabel=r"annual maximum (m)", xticks=[3.5, 4.0, 4.5],
                 yticks=[0, 1, 2], center=[-2.8, -0.6, 0])
        ax = A.ax
        ed = np.linspace(3.5, 4.8, 14)
        h = hist_bars(ax, ed, np.histogram(x, ed, density=True)[0], color=DATA, opacity=0.5)
        xs = np.linspace(3.4, 4.9, 200)
        t = 1 + xi * (xs - mu) / s
        pdf = (1 / s) * t ** (-1 / xi - 1) * np.exp(-t ** (-1 / xi))
        cv = curve(ax, xs, pdf, EXACT, 3)
        rows = [
            cmath(r"\ell(\mu, \sigma, \xi)", r"=", r"\sum_{i=1}^{65} \log g(x_i;\ \mu, \sigma, \xi)", font_size=30),
            cmath(r"(\hat\mu, \hat\sigma, \hat\xi)", r"=", rf"({mu:.3f},\ {s:.3f},\ {xi:.3f})", font_size=32),
        ]
        rows[1][2].set_color(EXACT)
        whys = [why(r"maximum likelihood: \ Part 9 builds it; \ here, a numerical search"),
                why(r"$\hat\xi$ slightly negative: \ a light, \ almost Gumbel tail")]
        tag = historical_tag(r"Port Pirie, \ 1923--1987", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> Fit the three parameters, location, scale and shape, by maximum likelihood: find "
            "the values that make the observed maxima most probable. Part 9 builds that method; here a computer "
            "simply searches. <bookmark mark='b'/> The estimates: a location of three point eight seven metres, a "
            "scale of about twenty centimetres, and a shape of minus point oh five, slightly negative, so very close "
            "to the Gumbel. These match the published analysis in Stuart Coles's textbook. <bookmark mark='c'/> The "
            "fitted density, in gold, over the histogram of the sixty-five maxima."
        ) as vo:
            self.play(FadeIn(A), FadeIn(h), FadeIn(tag))
            step = ladder(self, rows, whys, keep=2, top=2.4, x=3.2, buff=0.9, edge=6.9)
            vo.wait_until("a")
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            self.play(Create(cv))
        self.clear_scene()

    def levels(self):
        d = load("portpirie")
        mu, s, xi = d["mu"], d["sigma"], d["xi"]
        A = axes([0, 4], [3.5, 5.5], x_length=7.0, y_length=4.4, xlabel=r"return period $T$ (years, log scale)",
                 ylabel=r"return level (m)", xticks=[0, 1, 2, 3, 4], yticks=[3.5, 4.0, 4.5, 5.0, 5.5],
                 xfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.4, -0.5, 0])
        ax = A.ax
        Ts = np.logspace(np.log10(1.1), 4, 200)
        yp = -np.log(1 - 1 / Ts)
        z = mu - s / xi * (1 - yp ** (-xi))
        cv = curve(ax, np.log10(Ts), z, EXACT, 3)
        emp = VGroup(*[Dot(ax.c2p(np.log10(t), v), radius=0.045, color=DATA) for t, v in zip(d["emp_T"], d["sorted"])])
        marks = VGroup()
        for T, c in ((100, SIM), (10000, BOUND)):
            zz = float(mu - s / xi * (1 - (-np.log(1 - 1 / T)) ** (-xi)))
            marks.add(VGroup(DashedLine(ax.c2p(np.log10(T), 3.5), ax.c2p(np.log10(T), zz), color=c, stroke_width=1.5),
                             Dot(ax.c2p(np.log10(T), zz), radius=0.08, color=c),
                             MathTex(rf"{zz:.2f}\ \text{{m}}", font_size=26, color=c).next_to(ax.c2p(np.log10(T), zz), UL, buff=0.1)))
        rows = [
            cmath(r"P(\text{annual max} > z_T)", r"=", r"\frac1T", font_size=30),
            cmath(r"z_T", r"=", r"\mu - \frac{\sigma}{\xi}\Big(1 - \big(-\log(1 - \tfrac1T)\big)^{-\xi}\Big)", font_size=28),
        ]
        rows[1][2].set_color(EXACT)
        whys = [why(r"the $T$-year return level"), why(r"invert the GEV's CDF")]
        rk = label(r"a 100-year level in the next 30 years: \ $1 - 0.99^{30} = 26\%$", font_size=22, color=GREY_A).to_corner(DR, buff=0.4)
        with self.voiceover(
            "Engineers speak of return levels. <bookmark mark='a'/> The T-year return level is the height exceeded in "
            "any one year with probability one over T. <bookmark mark='b'/> Inverting the fitted distribution gives "
            "a formula. <bookmark mark='c'/> Plotted against the return period on a log scale, it's a gently bending "
            "curve; the white dots are the sixty-five observed maxima at their empirical return periods. "
            "<bookmark mark='d'/> The hundred-year level: four point six nine metres, the height of the 1934 "
            "record. <bookmark mark='e'/> The ten-thousand-year level: five point three four. Note what a hundred-year "
            "level does not mean: the chance of seeing one in the next thirty years is twenty-six percent."
        ) as vo:
            step = ladder(self, rows, whys, keep=2, top=2.8, x=3.4, buff=0.9, edge=6.9)
            vo.wait_until("a")
            step(0, transform=False)
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            self.play(FadeIn(A), Create(cv), FadeIn(emp))
            vo.wait_until("d")
            self.play(FadeIn(marks[0]))
            vo.wait_until("e")
            self.play(FadeIn(marks[1]), FadeIn(rk))
        self.clear_scene()

    def profile(self):
        d = load("portpirie")
        zs, prof = np.asarray(d["zs"]), np.asarray(d["prof"])
        A = axes([4.4, 5.4], [0, 4.8], x_length=6.6, y_length=4.2, xlabel=r"100-year return level $z_{100}$ (m)",
                 ylabel=r"profile log-likelihood $+\,c$", xticks=[4.5, 4.75, 5.0, 5.25], yticks=[0, 2, 4],
                 center=[-2.6, -0.5, 0])
        ax = A.ax
        base = prof.max() - 4.6
        cv = curve(ax, zs, prof - base, S.PRIOR, 3)
        cut = DashedLine(ax.c2p(4.4, d["cut"] - base), ax.c2p(5.4, d["cut"] - base), color=GREY_B, stroke_width=1.5)
        lo, hi = d["ci100"]
        seg = Line(ax.c2p(lo, 0.15), ax.c2p(hi, 0.15), color=S.ACCENT, stroke_width=6)
        rows = VGroup(
            MathTex(rf"\hat z_{{100}} = {d['rl'][5]:.2f}\ \text{{m}}", font_size=30, color=EXACT),
            MathTex(rf"95\%\ \text{{interval: }} [{lo:.2f},\ {hi:.2f}]", font_size=30, color=S.ACCENT),
            label(r"lopsided: \ the data rule out low levels better than high ones", font_size=22, color=GREY_A),
            label(r"65 years of data, \ asked about 100: \ and the Delta Committee asked about 10,000", font_size=22,
                  color=BOUND),
            label(r"the profile likelihood: \ Part 22", font_size=22, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        for r in rows:
            if r.width > 5.6:
                r.width = 5.6
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([3.9, 0.3, 0])
        with self.voiceover(
            "How sure can we be? <bookmark mark='a'/> For each candidate hundred-year level, refit the other two "
            "parameters as well as possible and record the best log-likelihood: the profile likelihood, which Part 22 "
            "develops. <bookmark mark='b'/> Levels where it falls less than about two units below its peak are "
            "plausible. <bookmark mark='c'/> That gives an interval from about four point four nine to five point two "
            "six metres: lopsided, because the data rule out low values more firmly than high ones. "
            "<bookmark mark='d'/> Sixty-five years of data asked about a hundred is already a stretch. The Delta "
            "Committee needed ten thousand. Extrapolation is where extreme-value statistics earns its keep, and "
            "where it's most humble."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(cv), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cut))
            vo.wait_until("c")
            self.play(Create(seg), FadeIn(rows[1:3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3:]))
        self.clear_scene()

    def dantzig(self):
        rows = [
            cmath(r"P(\text{level} > h)", r"\approx", r"p_0\, e^{-\alpha(h - h_0)}", font_size=32),
            cmath(r"C(h)", r"=", r"\underbrace{I_0 + k(h - h_0)}_{\text{build}}", r"+", r"\underbrace{\frac{V}{\delta}\, p_0\, "
                  r"e^{-\alpha(h - h_0)}}_{\text{expected losses, discounted}}", font_size=30),
            cmath(r"C'(h) = 0:\quad h^*", r"=", r"h_0 + \frac{1}{\alpha}\log\frac{\alpha V p_0}{\delta k}", font_size=32),
        ]
        rows[2][2].set_color(S.ACCENT)
        whys = [why(r"a Gumbel tail: \ the exceedance chance falls exponentially with height"),
                why(r"$V$: \ what a flood destroys; \ $\delta$: \ the discount rate; \ $k$: \ cost per metre"),
                why(r"the optimal height: \ worth raising until the next metre costs more than it saves")]
        hc = note(r"D. van Dantzig, \ ``Economic decision problems for flood prevention'', \ \emph{Econometrica} 24 (1956)")
        hc.to_edge(DOWN, buff=0.45)
        tail = label(r"statistics as decision-making: \ Part 45", font_size=24, color=GREY_A).next_to(hc, UP, buff=0.3)
        with self.voiceover(
            "Van Dantzig's own contribution was to turn the question into a decision. <bookmark mark='a'/> Above the "
            "current dike height, the chance that the sea goes over falls roughly exponentially with each extra "
            "metre: a Gumbel tail. <bookmark mark='b'/> The total cost of a height h is the cost of building, which "
            "grows with h, plus the expected flood losses for ever after, discounted, which fall with h. "
            "<bookmark mark='c'/> Set the derivative to zero, and the best height has a closed form: worth raising "
            "until the next metre costs more than the flood damage it prevents. The ten-thousand-year standard came "
            "out of reasoning like this, which is statistics as decision-making, the subject of Part 45."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.6, x=-1.0, buff=1.0, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                step(k, transform=False)
            self.play(FadeIn(tail), FadeIn(hc))
        self.clear_scene()
