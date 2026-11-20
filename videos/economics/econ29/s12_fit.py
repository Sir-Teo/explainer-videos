from __future__ import annotations

from videos.economics.econ29.common import *  # noqa: F403


class Fit(VoiceoverScene):
    def construct(self):
        card(self, 10, r"What fits and what does not", r"Hours, \ productivity, \ and what the shocks are made of",
             "Chapter ten. What fits and what does not.", lit={1957: r"Solow", 1992: r"Christiano and Eichenbaum"},
             scale=("nation",), horizon=("a quarter", "a decade"))
        self.scatter()
        self.split()
        self.solow()
        self.hoarding()

    def scatter(self):
        F = load("facts")
        R = load("rbc")
        n_d, w_d = np.array(F["cyc"]["n"]), np.array(F["cyc"]["w"])
        n_m, w_m = np.array(R["sim_hp"]["n"]), np.array(R["sim_hp"]["w"])

        def panel(center, title, col):
            ax = plane([-6, 6], [-4, 4], center=center, x_length=5.0, y_length=3.8, xticks=[-5, 0, 5],
                       yticks=[-4, 0, 4], xlabel=r"hours, \ \% from trend", ylabel=r"output per hour, \ \%",
                       xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
            t = label(title, font_size=21, color=col).next_to(ax, UP, buff=0.25)
            return ax, t

        axd, td = panel(LEFT * 3.4 + DOWN * 0.3, rf"US, \ {F['first'][:4]}--{F['last'][:4]}", OUTPUT)
        axm, tm = panel(RIGHT * 3.4 + DOWN * 0.3, r"the Island", TECH)
        dd = VGroup(*[Dot(axd.ax.c2p(x, y), radius=0.03, color=OUTPUT, fill_opacity=0.7) for x, y in zip(n_d, w_d)
                      if abs(x) < 6 and abs(y) < 4])
        dm = VGroup(*[Dot(axm.ax.c2p(x, y), radius=0.03, color=TECH, fill_opacity=0.7) for x, y in zip(n_m, w_m)
                      if abs(x) < 6 and abs(y) < 4])
        cd = label(rf"correlation \ {F['data']['corr_nw']:.2f}", font_size=20, color=OUTPUT).next_to(axd, DOWN,
                                                                                                    buff=0.55)
        cm = label(rf"correlation \ {F['model']['corr_nw']:.2f}", font_size=20, color=TECH).next_to(axm, DOWN,
                                                                                                   buff=0.55)
        tag = published_tag(r"BLS via FRED; \ the Island: \ simulated; \ Christiano and Eichenbaum, \ \emph{AER} "
                            r"82(3) (1992)", corner=DR, font_size=12)
        with self.voiceover(
            "Start with the worst miss. <bookmark mark='a'/> On the left, every quarter of American data: hours "
            "worked against output per hour, both as gaps from trend. <bookmark mark='b'/> On the right, the "
            "Island. <bookmark mark='c'/> In the model, the only shock is technology, which raises both the "
            "productivity of an hour and the desire to work, so the dots line up: a correlation of "
            f"{F['model']['corr_nw']:.2f}. In America, the cloud has no slope at all: "
            f"{say_num(F['data']['corr_nw'])}. <bookmark mark='d'/> Lawrence Christiano and Martin Eichenbaum "
            "made this the central puzzle in 1992. Hours must also be moved by something that shifts labour supply, "
            "not demand: in their paper, government spending. A model with a single shock gets one line, and the "
            "data are a cloud."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(axd), FadeIn(td), LaggedStart(*[FadeIn(x) for x in dd], lag_ratio=0.003), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(axm), FadeIn(tm), LaggedStart(*[FadeIn(x) for x in dm], lag_ratio=0.003), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(cm), FadeIn(cd))
        self.clear_scene()

    def split(self):
        F = load("facts")
        a, b = F["split"]["1948-1984"], F["split"]["1985-2019"]
        rows = VGroup(
            label(r"and the relationship changed", font_size=27, color=E.ACCENT),
            label(rf"1948--1984: \ output per hour moved with output \ (correlation {a['corr_wy']:.2f}); \ "
                  rf"with hours, \ {a['corr_nw']:.2f}", font_size=22, color=OUTPUT),
            label(rf"1985--2019: \ with output, \ {b['corr_wy']:.2f}; \ with hours, \ {b['corr_nw']:.2f}",
                  font_size=22, color=TECH),
            label(rf"and the cycle calmed: \ output's s.d.\ fell from {a['sd_y']:.1f}\% to {b['sd_y']:.1f}\% \ "
                  r"(the Great Moderation)", font_size=22, color=GREY_A),
            label(r"since the mid-1980s, \ firms cut hours in slumps and keep the most productive work", font_size=22,
                  color=HOURS),
            label(r"a model whose cycles are productivity cycles fits the earlier era better", font_size=22,
                  color=HOLD),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = data_tag(r"BEA and BLS, \ via FRED; \ this film's filtering", corner=DR, font_size=12)
        with self.voiceover(
            "The picture also changed over time. <bookmark mark='a'/> Split the sample in the mid-1980s. "
            "<bookmark mark='b'/> Before, output per hour rose and fell with output, with a correlation of "
            f"{a['corr_wy']:.2f}, which is what Kydland and Prescott saw. <bookmark mark='c'/> Since then, the "
            f"correlation with output is about zero, {say_num(b['corr_wy'])}, and with hours it is strongly "
            f"negative, {say_num(b['corr_nw'])}. <bookmark mark='d'/> At the same time the whole cycle calmed: "
            f"output's standard deviation fell from {a['sd_y']:.1f} to {b['sd_y']:.1f} percent, the Great "
            "Moderation. <bookmark mark='e'/> In recent recessions, firms cut hours hard and kept their most "
            "productive work, so productivity held up as hours fell. <bookmark mark='f'/> A theory in which "
            "productivity drives the cycle fitted the data it was built on better than the data that came after."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def solow(self):
        S = load("solow")
        yrs = np.array(S["years"][1:])
        dA = np.array(S["dA"])
        dY = np.array(S["dY"])
        ax = plane([1950, 2020], [-4, 8], center=LEFT * 1.8 + DOWN * 0.3, x_length=8.6, y_length=4.8,
                   xticks=[1950, 1970, 1990, 2010], yticks=[-4, 0, 4, 8], ylabel=r"growth, \ \% a year",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.0f}" if v else "0", font_size=15)
        zero = seg(ax, 1950, 0, 2020, 0, GREY_D, 1.5)
        bars = VGroup()
        for y, a in zip(yrs, dA):
            p0, p1 = ax.ax.c2p(y - 0.35, 0), ax.ax.c2p(y + 0.35, a)
            bars.add(Rectangle(width=p1[0] - p0[0], height=abs(p1[1] - p0[1]), fill_color=TECH if a < 0 else PROD,
                               fill_opacity=0.85, stroke_width=0).move_to((p0 + p1) / 2))
        out = path(ax, yrs, dY, OUTPUT, 2.5, smooth=False)
        eq = MathTex(r"\Delta \log A = \Delta \log Y - (1-s_L)\, \Delta \log K - s_L\, \Delta \log L",
                     font_size=28).to_edge(UP, buff=0.3)
        side = VGroup(
            label(r"bars: \ the Solow residual's growth", font_size=19, color=PROD),
            label(r"line: \ output's growth", font_size=19, color=OUTPUT),
            label(rf"their cycles: \ correlation {S['corr']:.2f}", font_size=19, color=E.ACCENT),
            label(rf"{S['negative_years']} years of \emph{{negative}} technology: \\ "
                  + r", \ ".join(str(w) for w in sorted(S["worst"])), font_size=19, color=TECH),
            label(rf"1982: \ {S['y1982']:.1f}\%. \ Did America \\ forget how to make things?", font_size=19,
                  color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Penn World Table 11.0, \ United States: \ GDP, \ capital, \ employment, \ hours, \ labour "
                       r"share", corner=DR, font_size=12)
        with self.voiceover(
            "Now the shocks themselves. The model's technology is measured by the Solow residual of Part twenty: "
            "<bookmark mark='a'/> output growth minus the growth that capital and hours account for, weighted by "
            "their shares of income. <bookmark mark='b'/> Here it is for America, year by year, from the Penn "
            "World Table. <bookmark mark='c'/> And output's growth, in green. <bookmark mark='d'/> They move "
            f"together: the cycles have a correlation of {S['corr']:.2f}. This was Prescott's evidence that "
            "technology drives the cycle. <bookmark mark='e'/> But look at the red bars: "
            f"{S['negative_years']} years in which measured technology went backwards. <bookmark mark='f'/> In "
            f"1982, it fell {abs(S['y1982']):.1f} percent. Did America forget how to make things in 1982, in the "
            "middle of a recession caused, by almost every account, by the Federal Reserve's high interest rates?"
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(FadeIn(ax), FadeIn(zero), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.02),
                      FadeIn(side[0]), run_time=2)
            vo.wait_until("c")
            self.play(Create(out), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]), *[Indicate(b, color=WHITE) for b, a in zip(bars, dA) if a < 0])
            vo.wait_until("f")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def hoarding(self):
        S = load("solow")
        rows = VGroup(
            label(r"what else the residual measures", font_size=27, color=E.ACCENT),
            label(r"labour hoarding: \ in a slump, \ firms keep workers they do not fully use", font_size=22,
                  color=HOURS),
            label(r"utilization: \ machines run fewer shifts; \ measured capital does not fall", font_size=22,
                  color=INVEST),
            label(r"so measured productivity falls with demand, \ whatever happens to technology", font_size=22,
                  color=TECH),
            label(rf"2009: \ output fell, \ but the residual rose {S['y2009']:.1f}\%: \ firms shed workers fast",
                  font_size=22, color=PROD),
            label(r"Basu, \ Fernald and Kimball, \ 2006: \ corrected for utilization, \ an improvement in "
                  r"technology cuts hours at first", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Basu, \ Fernald and Kimball, \ \emph{AER} 96(5) (2006); \ Penn World Table 11.0",
                            corner=DR, font_size=12)
        with self.voiceover(
            "The residual measures more than technology. <bookmark mark='a'/> In a slump, firms hold on to workers "
            "they do not fully use, because hiring and training are costly: labour hoarding. "
            "<bookmark mark='b'/> Machines run fewer shifts, but the measured capital stock does not fall. "
            "<bookmark mark='c'/> So measured productivity falls whenever demand falls, whatever happens to "
            "technology, and its correlation with output proves little. <bookmark mark='d'/> The pattern can even "
            f"reverse: in 2009, output fell, but the residual rose {S['y2009']:.1f} percent, because firms shed "
            "workers faster than output fell. <bookmark mark='e'/> Susanto Basu, John Fernald and Miles Kimball "
            "built a measure of technology corrected for utilization and published it in 2006. In their corrected "
            "series, when technology improves, hours and investment fall at first, and output barely moves: the "
            "opposite of the model's prediction. The shocks the theory needed were partly an artefact of "
            "measurement."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
