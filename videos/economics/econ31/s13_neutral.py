from __future__ import annotations

from videos.economics.econ31.common import *  # noqa: F403


class Neutral(VoiceoverScene):
    def construct(self):
        card(self, 11, r"The neutral rate, \ estimated", r"How low is the rate that neither pushes nor pulls?",
             "Chapter eleven. The neutral rate, estimated.",
             lit={1898: r"Wicksell", 2003: r"Laubach and Williams"}, scale=("nation", "world"),
             horizon=("a year", "decades"))
        self.island()
        self.estimates()

    def island(self):
        I = load("rstar")["island"]
        t = np.array(I["t"])
        est, se = np.array(I["estimate"]), np.array(I["se"])
        ax = plane([0, 200], [-3, 6], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.8, y_length=4.8,
                   xticks=[0, 50, 100, 150, 200], yticks=[-2, 0, 2, 4, 6], xlabel=r"quarters",
                   ylabel=r"the natural real rate, \ \%", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:+.0f}" if v else "0", font_size=15)
        zero = seg(ax, 0, 0, 200, 0, GREY_D, 1.2)
        truth = path(ax, t, I["truth"], TRUTH_C, 3, smooth=False)
        b = band(ax, t[5:], (est - 1.645 * se)[5:], (est + 1.645 * se)[5:], CB, 0.2)
        line = path(ax, t, est, CB, 3, smooth=False)
        side = VGroup(
            label(r"white: \ the Island's true natural rate, \\ drifting slowly", font_size=18, color=TRUTH_C),
            label(r"teal: \ the bank's estimate \\ from output and the real rate \\ (the Kalman filter)", font_size=18,
                  color=CB),
            label(rf"shaded: \ 90\% band, \ $\pm${1.645 * I['steady_se']:.1f} points", font_size=18, color=CB),
            label(r"the estimate lags the truth, \\ and the band is wide", font_size=19, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Laubach and Williams, \ \emph{REStat} 85(4) (2003); \ the Island", corner=DR,
                            font_size=12)
        top = label(r"the Island: \ a natural rate that drifts, \ and a bank that must estimate it", font_size=22,
                    color=E.ACCENT).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Part 30 left a question: every rule needs the natural rate of interest, the real rate at which policy "
            "neither pushes the economy nor holds it back, and nobody can see it. How is it estimated? On the "
            "Island, we can check. <bookmark mark='a'/> Here the natural rate drifts slowly, in white, over fifty "
            "years. <bookmark mark='b'/> The bank infers it the way Thomas Laubach and John Williams did for "
            "America: if output keeps falling short while the real rate seems low, the natural rate must be lower "
            "than thought. The Kalman filter turns that into an estimate, in teal. <bookmark mark='c'/> The band "
            f"holds ninety percent of the uncertainty: plus or minus {1.645 * I['steady_se']:.1f} points, even "
            "with the model exactly right. <bookmark mark='d'/> The estimate trails the truth by years, because "
            "the natural rate shows itself only through slow drifts in output that other shocks swamp."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), FadeIn(top), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(truth), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(line), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(b), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def estimates(self):
        R = load("rstar")
        t = np.array(R["t"])
        ax = plane([1961, 2027], [-1, 6.5], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.8, y_length=4.8,
                   xticks=[1970, 1980, 1990, 2000, 2010, 2020], yticks=[0, 2, 4, 6],
                   ylabel=r"natural real rate, \ \% \ (one-sided estimates)", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=15)
        zero = seg(ax, 1961, 0, 2027, 0, GREY_D, 1.2)
        us = path(ax, t, R["us"], COUNTRY["US"], 3.2, smooth=False)
        ca = path(ax, t, R["ca"], COUNTRY["CA"], 2.4, smooth=False)
        ea = path(ax, t, R["ea"], COUNTRY["EA"], 2.6, smooth=False)
        sep = VGroup(*[dot(ax, x, y, PRICE, 0.05) for x, y in zip(R["sep_t"], R["sep_real"])])
        side = VGroup(
            label(r"Holston, \ Laubach and Williams", font_size=18, color=E.ACCENT),
            label(rf"pink: \ United States: \\ {R['us_2000']:.1f}\% in 2000, \ {R['us_2015']:.1f}\% in 2015, \\ "
                  rf"{R['last']['rstar_us']:.1f}\% now", font_size=17, color=COUNTRY["US"]),
            label(r"orange: \ Canada; \ purple: \ euro area", font_size=17, color=COUNTRY["CA"]),
            label(r"gold dots: \ FOMC members' longer-run \\ rate, \ less 2\% inflation", font_size=17, color=PRICE),
            label(r"lower everywhere: \ ageing, \\ slower growth, \ a world \\ that wants safe assets", font_size=18,
                  color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"New York Fed, \ Holston--Laubach--Williams estimates; \ FOMC projections via FRED", corner=DR,
                       font_size=12)
        with self.voiceover(
            "Here are the estimates for real economies. <bookmark mark='a'/> The New York Fed publishes Kathryn "
            "Holston, Thomas Laubach and John Williams's estimates every quarter. <bookmark mark='b'/> For the "
            f"United States: about {R['us_2000']:.1f} percent in 2000, {R['us_2015']:.1f} percent by 2015, and "
            f"{R['last']['rstar_us']:.1f} percent in the latest. <bookmark mark='c'/> Canada's and the euro area's "
            "fell too; the euro area's to about zero. <bookmark mark='d'/> The gold dots are the Federal Reserve's "
            "policymakers' own view of where their rate settles in the long run, less two percent inflation: "
            f"{R['sep_first']:.1f} percent in 2012, as low as {R['sep_min']:.1f}, and {R['sep_last']:.1f} now. "
            "<bookmark mark='e'/> The causes most often given are slower growth, ageing populations that save "
            "more, and a world hungry for safe assets. Whatever the cause, a lower natural rate means the zero "
            "bound is hit more often, which is why the tools of the last three chapters will be needed again."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(us), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(Create(ca), Create(ea), FadeIn(side[2]), run_time=2)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(d) for d in sep], lag_ratio=0.05), FadeIn(side[3]), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
