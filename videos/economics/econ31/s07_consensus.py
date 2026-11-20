from __future__ import annotations

from videos.economics.econ31.common import *  # noqa: F403


class Consensus(VoiceoverScene):
    def construct(self):
        card(self, 6, r"The consensus response", r"After a tightening, \ what happens to output and prices, \ and "
             r"when?", "Chapter six. The consensus response.",
             lit={2004: r"Romer and Romer", 2012: r"Coibion", 2016: r"Ramey"}, scale=("nation",),
             horizon=("a month", "four years"))
        self.us()
        self.sizes()

    def us(self):
        U = load("usvar")
        c = U["commod"]
        h = np.array(U["h"])
        axi = plane([0, 48], [-2.0, 0.8], center=LEFT * 3.3 + DOWN * 0.1, x_length=5.6, y_length=4.0,
                    xticks=[0, 12, 24, 36, 48], yticks=[-2, -1, 0], xlabel=r"months after the shock",
                    ylabel=r"industrial production, \ \%", xfmt=lambda v: f"{v:.0f}",
                    yfmt=lambda v: f"{v:+.0f}" if v else "0", font_size=14)
        axc = plane([0, 48], [-1.4, 0.8], center=RIGHT * 3.3 + DOWN * 0.1, x_length=5.6, y_length=4.0,
                    xticks=[0, 12, 24, 36, 48], yticks=[-1, -0.5, 0, 0.5], xlabel=r"months after the shock",
                    ylabel=r"consumer prices, \ \%", xfmt=lambda v: f"{v:.0f}",
                    yfmt=lambda v: f"{v:+.1f}" if v else "0", font_size=14)
        zeros = VGroup(seg(axi, 0, 0, 48, 0, GREY_D, 1.2), seg(axc, 0, 0, 48, 0, GREY_D, 1.2))
        bi = band(axi, h, np.clip(c["ip_lo"], -2.0, 0.8), np.clip(c["ip_hi"], -2.0, 0.8), OUTPUT, 0.16)
        li = path(axi, h, c["ip"], OUTPUT, 3.5)
        bc = band(axc, h, np.clip(c["cpi_lo"], -1.4, 0.8), np.clip(c["cpi_hi"], -1.4, 0.8), INFL, 0.16)
        lc = path(axc, h, c["cpi"], INFL, 3.5)
        head = label(r"a one-point rise in the federal funds rate, \ US, \ 1965--2007, \ with commodity prices",
                     font_size=21, color=E.ACCENT).to_edge(UP, buff=0.4)
        n1 = label(rf"trough: \ {c['ip_trough']['value']:+.1f}\%, \ month {c['ip_trough']['h']}", font_size=18,
                   color=OUTPUT).next_to(axi.ax.c2p(24, -2.0), UP, buff=0.15)
        n2 = label(rf"four years on: \ {c['cpi_48']:+.2f}\%", font_size=18, color=INFL).next_to(
            axc.ax.c2p(30, -1.4), UP, buff=0.15)
        foot = label(r"output falls after a year or more; \ prices fall later still, \ and less surely", font_size=22,
                     color=WHITE).to_edge(DOWN, buff=0.7)
        tag = data_tag(r"FRED: \ industrial production, \ CPI, \ PPI (all commodities), \ the funds rate; \ this film",
                       corner=DR, font_size=12)
        with self.voiceover(
            "What do the better methods find for America? <bookmark mark='a'/> Here is the recursive VAR with "
            "commodity prices, on monthly data from 1965 to 2007, with bands from re-running it on resampled data. "
            "<bookmark mark='b'/> Industrial production falls slowly after a one-point tightening, and bottoms out "
            f"{c['ip_trough']['value']:.1f} percent lower after {c['ip_trough']['h']} months. <bookmark mark='c'/> "
            "Consumer prices barely move for two years, then begin to fall, and the band includes zero almost "
            "throughout. <bookmark mark='d'/> That shape is the consensus, and it is what Part 30's model was "
            "given habits and indexation to match: output first, after a year or more; prices later, and less "
            "surely."
        ) as vo:
            self.play(FadeIn(axi), FadeIn(axc), FadeIn(zeros), FadeIn(head), FadeIn(tag), run_time=0.6)
            vo.wait_until("b")
            self.play(FadeIn(bi), Create(li), run_time=1.6)
            self.play(FadeIn(n1))
            vo.wait_until("c")
            self.play(FadeIn(bc), Create(lc), run_time=1.6)
            self.play(FadeIn(n2))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def sizes(self):
        U = load("usvar")
        rows = VGroup(
            label(r"how big? \ a one-point tightening, \ industrial production at its lowest", font_size=25,
                  color=E.ACCENT),
            label(r"a standard recursive VAR, \ 1969--96: \ about $-0.7\%$", font_size=23, color=METHOD["var"]),
            label(r"Romer and Romer's narrative shocks, \ 1969--96: \ about $-4.3\%$; \ prices about $-6\%$ after four "
                  r"years", font_size=23, color=METHOD["narrative"]),
            label(r"Coibion, \ 2012: \ most of the gap comes from 1979--82 and from lag lengths; \ about $-2$ to "
                  r"$-3\%$", font_size=23, color=PRICE),
            label(rf"this film's VAR with commodity prices: \ {U['commod']['ip_trough']['value']:+.1f}\%", font_size=23,
                  color=OUTPUT),
            label(r"the direction is settled; \ the size still differs by a factor of six", font_size=24,
                  color=HOLD),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = published_tag(r"Romer and Romer, \ \emph{AER} 94(4) (2004); \ Coibion, \ \emph{AEJ: Macro} 4(2) "
                            r"(2012); \ "
                            r"Ramey, \ \emph{Handbook of Macroeconomics} 2A (2016)", corner=DR, font_size=12)
        with self.voiceover(
            "How big is the effect? <bookmark mark='a'/> A standard recursive VAR on 1969 to 1996 finds that a "
            "one-point tightening lowers industrial production by about seven tenths of a percent at the worst. "
            "<bookmark mark='b'/> The Romers' narrative shocks, on the same years, find four point three percent, "
            "with prices about six percent lower after four years. <bookmark mark='c'/> Olivier Coibion traced most "
            "of the gap to the years 1979 to 1982, when the Federal Reserve targeted reserves rather than a rate, "
            "and to the number of lags each method allows; reconciled, he put the effect at two to three percent. "
            f"<bookmark mark='d'/> This film's own VAR gives {abs(U['commod']['ip_trough']['value']):.1f}. "
            "<bookmark mark='e'/> The direction and the delays are settled. The size still varies by a factor of "
            "six across careful studies, as Valerie Ramey's survey for the Handbook of Macroeconomics documents."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
