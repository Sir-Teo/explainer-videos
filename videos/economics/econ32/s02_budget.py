from __future__ import annotations

from videos.economics.econ32.common import *  # noqa: F403


class Budget(VoiceoverScene):
    def construct(self):
        card(self, 1, r"The budget constraint and r minus g", r"When does government debt grow, \ and what holds "
             r"it steady?", "Chapter one. The budget constraint and r minus g.",
             lit={1944: r"Domar"}, scale=("nation",), horizon=("a year", "decades"))
        self.algebra()
        self.paths()
        self.history()

    def algebra(self):
        rows = VGroup(
            label(r"what the government owes next year:", font_size=24, color=E.ACCENT),
            MathTex(r"B_{t+1} = (1 + r)\,B_t \;-\; \text{primary surplus}_t", font_size=40),
            label(r"divide by output, \ which grows at rate $g$:", font_size=24, color=E.ACCENT),
            MathTex(r"b_{t+1} = \frac{1 + r}{1 + g}\, b_t \;-\; s_t", font_size=42, color=DEBT),
            label(r"debt to GDP grows by itself when $r > g$, \ and shrinks by itself when $r < g$", font_size=23,
                  color=RATE),
            MathTex(r"s^{*} = \frac{r - g}{1 + g}\, b \quad \text{holds it steady}", font_size=38, color=TAX),
        ).arrange(DOWN, buff=0.36).move_to(UP * 0.1)
        tag = published_tag(r"Domar, \ \emph{AER} 34(4) (1944); \ any macroeconomics text", corner=DR, font_size=12)
        with self.voiceover(
            "Start with the budget constraint. <bookmark mark='a'/> Next year the government owes this year's "
            "debt plus interest, less whatever it collects beyond its spending on everything but interest: its "
            "primary surplus. <bookmark mark='b'/> What matters is debt relative to the economy that carries it, "
            "so divide by output. <bookmark mark='c'/> Debt to GDP is multiplied each year by one plus the "
            "interest rate over one plus the growth rate, and reduced by the primary surplus as a share of GDP. "
            "<bookmark mark='d'/> So when the interest rate r exceeds the growth rate g, debt grows by itself; when "
            "r is below g, it shrinks by itself, even with a small deficit. <bookmark mark='e'/> The surplus that "
            "holds debt steady is r minus g, over one plus g, times the debt. Evsey Domar made this point in 1944."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), FadeIn(tag))
            for mk, r_ in zip("bcde", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def paths(self):
        B = load("budget")
        yrs = np.array(B["years"])
        ax = plane([0, 40], [0, 3.6], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.8, y_length=4.8,
                   xticks=[0, 10, 20, 30, 40], yticks=[0, 1, 2, 3], xlabel=r"years", ylabel=r"debt, \ \% of GDP",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}", font_size=15)
        cols = {"plus": INFL, "zero": TAX, "minus": OUTPUT}
        lines = {k: path(ax, yrs, np.minimum(B[k]["debt"], 3.6), cols[k], 3.2, smooth=False) for k in cols}
        flat = {k: DashedVMobject(path(ax, yrs, np.minimum(B[k]["balanced"], 3.6), cols[k], 2.0, smooth=False),
                                  num_dashes=30) for k in cols}
        side = VGroup(
            label(rf"the Island: \ debt {100 * B['b0']:.0f}\% of GDP, \\ a primary deficit of "
                  rf"{100 * B['deficit']:.0f}\%, \ growth {100 * B['g']:.0f}\%", font_size=18, color=GREY_A),
            label(rf"red: \ r is 2 points above g: \\ {100 * B['plus']['debt'][-1]:.0f}\% after 40 years", font_size=18,
                  color=INFL),
            label(rf"gold: \ r equals g: \ {100 * B['zero']['debt'][-1]:.0f}\%", font_size=18, color=TAX),
            label(rf"green: \ r is 2 points below g: \\ {100 * B['minus']['debt'][-1]:.0f}\%, \ with the deficit",
                  font_size=18, color=OUTPUT),
            label(r"dashed: \ the same with a balanced \\ primary budget", font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here it is on the Island. <bookmark mark='a'/> Debt equal to a year's output, a primary deficit of two "
            "percent of output, and growth of two percent. <bookmark mark='b'/> If the interest rate is two points "
            f"above growth, debt reaches {100 * B['plus']['debt'][-1]:.0f} percent of GDP in forty years, and keeps "
            f"going. <bookmark mark='c'/> If the two are equal, {100 * B['zero']['debt'][-1]:.0f} percent: the "
            "deficits simply pile up. <bookmark mark='d'/> If the rate is two points below growth, debt settles "
            f"near {100 * B['minus']['debt'][-1]:.0f} percent, despite the deficit every year. <bookmark mark='e'/> "
            "Dashed, the same three economies with a balanced primary budget: with r above g, even that is not "
            "enough. Everything about debt sustainability is in the sign of r minus g."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=0.6)
            for mk, k, s_ in zip("bcd", ("plus", "zero", "minus"), side[1:4]):
                vo.wait_until(mk)
                self.play(Create(lines[k]), FadeIn(s_), run_time=1.6)
            vo.wait_until("e")
            self.play(*[Create(f) for f in flat.values()], FadeIn(side[4]), run_time=1.6)
        self.clear_scene()

    def history(self):
        D = load("debt")
        t = np.array(D["t"])
        ax = plane([1889, 2027], [0, 125], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.8, y_length=4.8,
                   xticks=[1900, 1925, 1950, 1975, 2000, 2025], yticks=[0, 25, 50, 75, 100, 125],
                   ylabel=r"federal debt held by the public, \ \% of GDP", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=15)
        line = path(ax, t, D["debt"], DEBT, 3, smooth=False)
        side = VGroup(
            label(rf"1916: \ {D['d1916']:.0f}\%; \ after the First World War, \ {D['d1919']:.0f}\%", font_size=18,
                  color=GREY_A),
            label(rf"1945--46: \ {D['peak']:.0f}\% \ at the peak", font_size=18, color=INFL),
            label(rf"1974: \ {D['d1974']:.0f}\% \ (deficits were small; \\ growth and inflation did the rest)",
                  font_size=18, color=OUTPUT),
            label(rf"2007: \ {D['d2007']:.0f}\%; \ 2020: \ {D['d2020']:.0f}\%; \ now {D['last']:.0f}\%", font_size=18,
                  color=DEBT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Ramey and Zubairy (to 1969); \ OMB via FRED (from 1970)", corner=DR, font_size=12)
        with self.voiceover(
            "America's own record. <bookmark mark='a'/> Federal debt held by the public was a few percent of GDP "
            f"before the First World War and {D['d1919']:.0f} percent after it. <bookmark mark='b'/> The Second "
            f"World War took it to about {D['peak']:.0f} percent. <bookmark mark='c'/> By 1974 it was "
            f"{D['d1974']:.0f} percent, mostly not because the war debt was repaid: it fell as a share of a "
            "growing economy, with interest rates held below growth and inflation, which is r below g. "
            f"<bookmark mark='d'/> Since 2007 it has risen again, to {D['last']:.0f} percent of GDP now."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.6)
            self.play(Create(line), run_time=3.0)
            for mk, s_ in zip("abcd", side):
                vo.wait_until(mk)
                self.play(FadeIn(s_))
        self.clear_scene()
