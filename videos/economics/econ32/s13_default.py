from __future__ import annotations

from videos.economics.econ32.common import *  # noqa: F403


class Default(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Sovereign default", r"No court can make a country pay. \ Why do countries repay at all?",
             "Chapter eleven. Sovereign default.", lit={1981: r"Eaton and Gersovitz", 2008: r"Arellano"},
             scale=("nation", "world"), horizon=("a quarter", "decades"))
        self.why()
        self.prices()
        self.sim()
        self.greece()

    def why(self):
        rows = VGroup(
            label(r"no court can seize a country's assets at home", font_size=25, color=E.ACCENT),
            label(r"Eaton and Gersovitz, \ 1981: \ a country that defaults is shut out of borrowing for a while",
                  font_size=22, color=DEBT),
            label(r"and defaults are costly at home: \ output falls, \ banks that hold the bonds suffer", font_size=22,
                  color=INFL),
            label(r"so a country repays while the cost of default exceeds what it would save", font_size=22,
                  color=WHITE),
            label(r"Arellano, \ 2008: \ solve it, \ and defaults come in bad times", font_size=23, color=TAX),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Eaton and Gersovitz, \ \emph{REStud} 48(2) (1981); \ Arellano, \ \emph{AER} 98(3) "
                            r"(2008)", corner=DR, font_size=12)
        with self.voiceover(
            "Why do countries repay at all? <bookmark mark='a'/> No court can seize a sovereign's assets at home. "
            "<bookmark mark='b'/> Jonathan Eaton and Mark Gersovitz's answer, in 1981, was reputation: a country "
            "that defaults is shut out of borrowing for a while, and loses the ability to smooth its spending "
            "through bad years. <bookmark mark='c'/> Defaults are also costly at home: output falls, and banks "
            "holding the bonds are hit. <bookmark mark='d'/> So a country repays as long as the cost of defaulting "
            "exceeds what it would save. <bookmark mark='e'/> Cristina Arellano turned this into a model that can "
            "be solved and simulated, calibrated to Argentina. Here it is, solved on this computer by iterating "
            "the value functions until they stop changing."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(rows[4], shift=UP * 0.1))
        self.clear_scene()

    def prices(self):
        D = load("default")
        debt = -np.array(D["B"])
        ax = plane([0, 0.3], [0, 1.0], center=LEFT * 3.3 + DOWN * 0.3, x_length=5.6, y_length=4.4,
                   xticks=[0, 0.1, 0.2, 0.3], yticks=[0, 0.25, 0.5, 0.75, 1.0], xlabel=r"debt issued, \ share of "
                   r"quarterly output", ylabel=r"price of a bond paying 1", xfmt=lambda v: f"{v:.1f}",
                   yfmt=lambda v: f"{v:.2f}", font_size=14)
        cols = {"low": INFL, "mid": TAX, "high": OUTPUT}
        lines = {k: path(ax, debt, D["sched"][k], cols[k], 3, xr=(0, 0.3), smooth=False) for k in cols}
        y = np.array(D["y"])
        ax2 = plane([0.85, 1.15], [0, 0.36], center=RIGHT * 3.3 + DOWN * 0.3, x_length=5.6, y_length=4.4,
                    xticks=[0.9, 1.0, 1.1], yticks=[0, 0.1, 0.2, 0.3], xlabel=r"output, \ relative to its average",
                    ylabel=r"largest debt still repaid", xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}",
                    font_size=14)
        th = np.array(D["threshold"])
        keep = (y >= 0.85) & (y <= 1.15) & (th < 0.345)        # past 0.345 the grid's edge, not the model, binds
        thr = path(ax2, y[keep], th[keep], DEBT, 3.5, smooth=False)
        k1 = VGroup(label(r"red: \ a bad quarter", font_size=16, color=INFL),
                    label(r"gold: \ an average one", font_size=16, color=TAX),
                    label(r"green: \ a good one", font_size=16, color=OUTPUT)).arrange(RIGHT, buff=0.3).next_to(
            ax, UP, buff=0.15)
        k2 = label(r"default when debt is above the line", font_size=16, color=DEBT).next_to(ax2, UP, buff=0.15)
        tag = published_tag(r"Arellano, \ \emph{AER} 98(3) (2008): \ her calibration, \ solved in Agora "
                            r"(agora.fiscal.arellano)", corner=DR, font_size=12)
        with self.voiceover(
            "Two things come out of it. <bookmark mark='a'/> First, the price lenders pay for the country's bonds. "
            "With little debt, a bond paying one next quarter sells for nearly one. As the country borrows more, "
            "the chance of default rises and the price falls, <bookmark mark='b'/> and it falls sooner in a bad "
            "quarter, in red, than in a good one, in green: the country can borrow least when it needs to most. "
            "<bookmark mark='c'/> Second, the debt a country will still repay rises with its output. "
            "<bookmark mark='d'/> Below the line it repays; above it, it defaults. So defaults happen in recessions, "
            "as in the data."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(ax2), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(lines["mid"]), FadeIn(k1[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lines["low"]), Create(lines["high"]), FadeIn(k1[0]), FadeIn(k1[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(thr), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(k2))
        self.clear_scene()

    def sim(self):
        D = load("default")
        S = D["sim"]
        n = len(S["y"])
        q = np.arange(n)
        ax = plane([0, n], [0.85, 1.15], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.8, y_length=4.4,
                   xticks=[0, 100, 200, 300, 400], yticks=[0.9, 1.0, 1.1], xlabel=r"quarters",
                   ylabel=r"output, \ relative to average", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}",
                   font_size=15)
        out = path(ax, q, S["y"], OUTPUT, 2.5, smooth=False)
        excl = []
        start = None
        for k, e in enumerate(S["excluded"] + [False]):
            if e and start is None:
                start = k
            if not e and start is not None:
                excl.append((start, k))
                start = None
        shades = shade(ax, excl, 0.85, 1.15, INFL, 0.18)
        marks = VGroup(*[Line(ax.ax.c2p(k, 0.85), ax.ax.c2p(k, 1.15), color=INFL, stroke_width=2.5)
                         for k, d in enumerate(S["default"]) if d])
        side = VGroup(
            label(r"green: \ output", font_size=18, color=OUTPUT),
            label(r"red lines: \ defaults; \\ shaded: \ shut out of markets", font_size=18, color=INFL),
            label(rf"defaults: \ {100 * S['default_rate_annual']:.1f}\% a year \\ (Arellano's target: \ 3\%)",
                  font_size=18, color=E.ACCENT),
            label(rf"average spread: \ {100 * S['mean_spread']:.1f} points", font_size=18, color=DEBT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Arellano (2008); \ this film's simulation", corner=DR, font_size=12)
        with self.voiceover(
            "Now let the model run for a hundred years. <bookmark mark='a'/> Output wanders. "
            "<bookmark mark='b'/> The red lines are defaults, and the shading the years the country is shut out of "
            "markets, which ends at random. Each default follows a fall in output. <bookmark mark='c'/> Over a long "
            f"simulation, defaults come at {100 * S['default_rate_annual']:.1f} percent a year, close to the three "
            f"percent Arellano matched for Argentina, <bookmark mark='d'/> and lenders charge "
            f"{100 * S['mean_spread']:.1f} points over the safe rate on average to cover the risk."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(out), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(shades), Create(marks), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def greece(self):
        D = load("default")
        t = np.array(D["gr_t"])
        ax = plane([2007, 2017], [0, 32], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.8, y_length=4.8,
                   xticks=[2008, 2010, 2012, 2014, 2016], yticks=[0, 10, 20, 30],
                   ylabel=r"10-year government bond yield, \ \%", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=15)
        gr = path(ax, t, D["gr"], COUNTRY["GR"], 3.2, smooth=False)
        de = path(ax, t, D["de"], COUNTRY["DE"], 2.4, smooth=False)
        psi = vline(ax, 2012.2, 0, 32, INFL, 2.5)
        side = VGroup(
            label(r"blue: \ Greece; \ grey: \ Germany", font_size=18, color=COUNTRY["GR"]),
            label(rf"peak: \ {D['gr_peak']:.1f}\%, \ {D['gr_peak_date'][:7]}", font_size=18, color=INFL),
            label(r"March 2012: \ private bondholders \\ accept a 53.5\% cut in face value", font_size=18,
                  color=INFL),
            label(r"a default in all but name, \\ inside a currency union", font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"OECD bond yields via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "Real defaults look like this. <bookmark mark='a'/> Greece's ten-year yield against Germany's. "
            f"<bookmark mark='b'/> By early 2012 Greece was paying {D['gr_peak']:.0f} percent, which no country "
            "could pay for long. <bookmark mark='c'/> In March 2012 private holders of Greek bonds exchanged them "
            "for new ones with 53.5 percent less face value: the biggest sovereign debt restructuring in history. "
            "Argentina had "
            "defaulted at the end of 2001, after three years of recession, just as the model predicts. "
            "<bookmark mark='d'/> Inside a currency union, as Part 31 showed, a country cannot inflate its debts "
            "away, and default is the remaining exit."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(gr), Create(de), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(psi), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
