from __future__ import annotations

from videos.economics.econ29.common import *  # noqa: F403


class Critics(VoiceoverScene):
    def construct(self):
        card(self, 11, r"The critics", r"What does a technology shock really do to hours?", "Chapter eleven. The "
             "critics.", lit={1986: r"Summers", 1999: r"Gal\'i", 2003: r"Christiano, \ Eichenbaum, \ Vigfusson"},
             scale=("nation",), horizon=("a quarter", "three years"))
        self.summers()
        self.var()
        self.gali()
        self.money()
        self.called()

    def summers(self):
        rows = VGroup(
            label(r"Lawrence Summers, \ ``Some Skeptical Observations on Real Business Cycle Theory'', \ 1986",
                  font_size=23, color=E.ACCENT),
            label(r"the parameters: \ the labour-supply response the theory needs is not what workers show",
                  font_size=21, color=HOURS),
            label(r"the shocks: \ what are they? \ Where is the evidence of technical regress in recessions?",
                  font_size=21, color=TECH),
            label(r"prices: \ the theory predicts how wages and interest rates move; \ those predictions go "
                  r"unchecked", font_size=21, color=PROD),
            label(r"exchange: \ in the Depression, \ markets and banks broke down; \ the theory has no room for "
                  r"that", font_size=21, color=HOLD),
            label(r"Prescott, \ in the same issue: \ theory ahead of measurement", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Summers; \ Prescott, \ ``Response to a Skeptic'', \ Federal Reserve Bank of Minneapolis "
                            r"\emph{Quarterly Review} 10(4) (1986)", corner=DR, font_size=12)
        with self.voiceover(
            "The first sharp critique came in 1986, in the same issue of the Minneapolis Fed's Quarterly Review "
            "that carried Prescott's case. Lawrence Summers called it some skeptical observations. "
            "<bookmark mark='a'/> The parameters: the labour-supply response the theory needs is far larger than "
            "what studies of workers find, as chapter six showed. <bookmark mark='b'/> The shocks: what are they? "
            "Where is the evidence that technology goes backwards in recessions? <bookmark mark='c'/> Prices: the "
            "theory predicts how wages and interest rates should move, and those predictions had not been checked. "
            "<bookmark mark='d'/> And exchange: in the Depression, markets and banks broke down, and a theory "
            "without money, credit or failures has nothing to say about that. <bookmark mark='e'/> Prescott's "
            "reply, in the same issue, was that theory was ahead of measurement: better data would come round."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def var(self):
        rows = VGroup(
            label(r"Jordi Gal\'i, \ 1999: \ let the data say what a technology shock is", font_size=25,
                  color=E.ACCENT),
            label(r"a vector autoregression in two series: \ productivity's growth, \ and hours", font_size=22,
                  color=GREY_A),
            label(r"identify technology as the only shock that moves productivity \emph{for ever}", font_size=22,
                  color=TECH),
            label(r"(Blanchard and Quah's long-run restriction, \ 1989)", font_size=20, color=GREY_B),
            label(r"demand shocks can move productivity for a while, \ through hoarding; \ only technology moves "
                  r"it in the long run", font_size=21, color=HOURS),
            label(r"then ask: \ what does that shock do to hours?", font_size=23, color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Gal\'i, \ \emph{AER} 89(1) (1999); \ Blanchard and Quah, \ \emph{AER} 79(4) (1989)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "The decisive test came from Jordi Galí in 1999. <bookmark mark='a'/> Instead of measuring technology "
            "with the Solow residual, let the data say what a technology shock is. <bookmark mark='b'/> Fit a "
            "statistical model to two series together, the growth of output per hour and hours worked: a vector "
            "autoregression. <bookmark mark='c'/> Then call a technology shock whatever moves productivity for "
            "ever. <bookmark mark='d'/> This is Blanchard and Quah's long-run restriction, from 1989. "
            "<bookmark mark='e'/> The logic: a fall in demand can lower measured productivity for a while, as "
            "firms hoard labour, but only technology can change it permanently. <bookmark mark='f'/> Having found "
            "the technology shock that way, ask what it does to hours."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def _panel(self, G, center, title, col):
        h = np.array(G["h"])
        ax = plane([0, 12], [-0.8, 1.2], center=center, x_length=5.2, y_length=3.6, xticks=[0, 4, 8, 12],
                   yticks=[-0.5, 0, 0.5, 1.0], xlabel=r"quarters", ylabel=r"hours, \ \%",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.1f}" if v else "0", font_size=14)
        zero = seg(ax, 0, 0, 12, 0, GREY_C, 1.5)
        lo, hi = np.array(G["hours_lo"]), np.array(G["hours_hi"])
        band = Polygon(*[ax.ax.c2p(x, y) for x, y in zip(h, np.clip(hi, -0.8, 1.2))],
                       *[ax.ax.c2p(x, y) for x, y in zip(h[::-1], np.clip(lo[::-1], -0.8, 1.2))],
                       stroke_width=0, fill_color=col, fill_opacity=0.22)
        line = path(ax, h, G["hours"], col, 3.5, smooth=False)
        t = label(title, font_size=20, color=col).next_to(ax, UP, buff=0.2)
        return VGroup(ax, zero), band, line, t

    def gali(self):
        G = load("gali")
        d, lv = G["diff"], G["levels"]
        pd_ = self._panel(d, LEFT * 3.4 + DOWN * 0.1, r"hours in growth rates \ (Gal\'i)", TECH)
        pl = self._panel(lv, RIGHT * 3.4 + DOWN * 0.1, r"hours in levels \ (Christiano et al.)", OUTPUT)
        s_d, s_l = d["tech_share_output"][8], lv["tech_share_output"][8]
        notes = VGroup(
            label(rf"on impact: \ {d['hours'][0]:+.2f}\%; \ {100 * d['share_negative_impact']:.0f}\% of "
                  rf"resamples below zero", font_size=17, color=TECH).next_to(pd_[0], DOWN, buff=0.35),
            label(rf"on impact: \ {lv['hours'][0]:+.2f}\%; \ {100 * lv['share_negative_impact']:.0f}\% of "
                  rf"resamples below zero", font_size=17, color=OUTPUT).next_to(pl[0], DOWN, buff=0.35),
        )
        shares = VGroup(
            label(rf"technology's share of output's variance at two years: \ {100 * s_d:.0f}\%", font_size=17,
                  color=TECH).next_to(notes[0], DOWN, buff=0.15),
            label(rf"technology's share at two years: \ {100 * s_l:.0f}\%", font_size=17,
                  color=OUTPUT).next_to(notes[1], DOWN, buff=0.15),
        )
        head = label(rf"US, \ {G['first'][:4]}--{G['last'][:4]}: \ hours after a technology shock, \ with 68\% "
                     r"bands", font_size=22, color=E.ACCENT).to_edge(UP, buff=0.3)
        tag = data_tag(r"BLS: \ output per hour and hours, \ nonfarm business, \ via FRED; \ this film's VARs",
                       corner=DR, font_size=12)
        with self.voiceover(
            f"Here is that test, run in this film on American data from {G['first'][:4]} to {G['last'][:4]}. "
            "<bookmark mark='a'/> With hours entered in growth rates, as Galí did, a technology improvement "
            f"lowers hours, by {abs(d['hours'][0]):.2f} percent on impact, and the band of plausible answers is "
            f"below zero throughout the first year. {100 * d['share_negative_impact']:.0f} percent of resampled "
            "histories agree. That is the opposite of the model. <bookmark mark='b'/> But in 2003 Lawrence "
            "Christiano, Martin Eichenbaum and Robert Vigfusson entered hours in levels instead, and hours rise: "
            f"{lv['hours'][0]:+.2f} percent on impact, climbing for a year, though with a band that reaches below "
            "zero. <bookmark mark='c'/> The two specifications disagree about everything that matters. In the "
            f"first, technology explains about {100 * s_d:.0f} percent of output's variance two years out; in the "
            f"second, about {100 * s_l:.0f}. <bookmark mark='d'/> Which is right depends on whether hours have a "
            "trend that never reverses, which twenty years of argument have not settled. John Fernald showed in "
            "2007 that allowing for breaks in productivity's trend growth pulls the levels result towards Galí's, "
            "and the corrected technology series of Basu, Fernald and Kimball also says hours fall."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(pd_[0]), FadeIn(pl[0]), FadeIn(pd_[3]), FadeIn(pl[3]),
                      run_time=0.8)
            vo.wait_until("a")
            self.play(FadeIn(pd_[1]), Create(pd_[2]), FadeIn(notes[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(pl[1]), Create(pl[2]), FadeIn(notes[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(shares))
        self.clear_scene()

    def money(self):
        rows = VGroup(
            label(r"and money", font_size=28, color=E.ACCENT),
            label(r"in the model, \ money does not exist; \ the central bank cannot matter", font_size=22,
                  color=GREY_A),
            label(r"Friedman and Schwartz, \ 1963: \ the money supply fell by a third, \ 1929--33", font_size=22,
                  color=INVEST),
            label(r"Romer and Romer, \ 1989: \ after each deliberate tightening, \ output fell", font_size=22,
                  color=TECH),
            label(r"1981--82: \ the Volcker recession, \ chosen to end inflation \ (Part 28)", font_size=22,
                  color=HOURS),
            label(r"and housing, \ the most interest-sensitive spending, \ turns first \ (chapter two)",
                  font_size=22, color=HOUSING),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Friedman and Schwartz (1963); \ Romer and Romer, \ \emph{NBER Macroeconomics Annual} "
                            r"(1989)", corner=DR, font_size=12)
        with self.voiceover(
            "The third front was money. <bookmark mark='a'/> The model has no money, so in it the central bank "
            "cannot matter at all. <bookmark mark='b'/> But Milton Friedman and Anna Schwartz had shown that "
            "America's money supply fell by about a third between 1929 and 1933. <bookmark mark='c'/> Christina "
            "and David Romer, in 1989, read the Federal Reserve's own records to find the dates when it deliberately "
            "tightened to fight inflation, and found that output fell after each one. <bookmark mark='d'/> The "
            "recession of 1981 and 1982, the one where measured technology fell, was chosen by the central bank to "
            "end inflation. <bookmark mark='e'/> And housing, the spending most sensitive to interest rates, turns "
            "first. All of this says money and interest rates move output, and the next two parts build models in "
            "which they do."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["prescott_75"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=16).move_to(UP * 0.05)
        tag = published_tag(r"Prescott (1986); \ Gal\'i (1999); \ Christiano, \ Eichenbaum and Vigfusson (2003); \ "
                            r"Basu, \ Fernald and Kimball (2006); \ Fernald (2007)", corner=DR, font_size=12)
        with self.voiceover(
            "Time for this part's forecast. Called it? <bookmark mark='a'/> In the autumn of 1986, Prescott wrote "
            "that technology shocks account for more than half of America's postwar fluctuations, with a best "
            "estimate near seventy-five percent, and in his theory a technology improvement raises output, "
            "investment and hours together. <bookmark mark='b'/> What happened: the measured shocks turned out to "
            "be partly not technology at all. Corrected for utilization, technology improvements cut hours at "
            "first. Long-run VARs split, as you just saw, depending on how hours enter. "
            "<bookmark mark='c'/> Partly right. Few economists now put technology's share near three quarters, and "
            "the mechanism through hours is in doubt. But technology does move the economy, and the way Prescott "
            "asked the question became the way everyone asks it."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
        self.clear_scene()
