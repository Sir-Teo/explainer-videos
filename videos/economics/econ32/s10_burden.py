from __future__ import annotations

from videos.economics.econ32.common import *  # noqa: F403


class Burden(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Is debt a burden?", r"Who pays for government debt, \ and does it matter when r is below g?",
             "Chapter eight. Is debt a burden?", lit={1965: r"Diamond", 1974: r"Barro", 2019: r"Blanchard"},
             scale=("household", "nation"), horizon=("a generation",))
        self.views()
        self.rg()

    def views(self):
        rows = VGroup(
            label(r"three views", font_size=27, color=E.ACCENT),
            label(r"Barro, \ 1974: \ debt is only delayed taxes; \ households who care about their heirs save to pay "
                  r"them, \ and nothing changes", font_size=21, color=TAX),
            label(r"Diamond, \ 1965 \ (Part 23): \ in an economy of generations, \ debt absorbs savings that would "
                  r"have built capital: \ crowding out", font_size=21, color=DEBT),
            label(r"the evidence of Part 22: \ many households spend cheques at once, \ so full Ricardian equivalence "
                  r"fails", font_size=21, color=SPEND),
            label(r"Blanchard, \ 2019: \ when the safe rate is below growth, \ debt may cost less than it seems",
                  font_size=21, color=OUTPUT),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Barro, \ \emph{JPE} 82(6) (1974); \ Diamond, \ \emph{AER} 55(5) (1965); \ Blanchard, \ "
                            r"\emph{AER} 109(4) (2019)", corner=DR, font_size=12)
        with self.voiceover(
            "Is government debt a burden on the future? Three views. <bookmark mark='a'/> Robert Barro argued in "
            "1974 that debt is only taxes delayed. Households who care about their heirs save to pay them, and "
            "nothing real changes: Ricardian equivalence. <bookmark mark='b'/> Peter Diamond's economy of "
            "overlapping generations, from Part 23, says the opposite: debt soaks up savings that would otherwise "
            "have built capital, so future workers have less to work with. <bookmark mark='c'/> The evidence of "
            "Part 22, households spending cheques at once, says equivalence fails in practice. "
            "<bookmark mark='d'/> And in 2019 Olivier Blanchard, in his presidential address to the American "
            "Economic Association, pointed out that when the safe interest rate is below the growth rate, debt "
            "can be rolled over and shrink as a share of output by itself, so its cost may be smaller than it "
            "looks."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def rg(self):
        G = load("rg")
        yrs = np.array(G["years"])
        ax = plane([1953, 2026], [-12, 8], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.8, y_length=4.8,
                   xticks=[1960, 1980, 2000, 2020], yticks=[-10, -5, 0, 5], ylabel=r"r minus g, \ percentage points",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.0f}" if v else "0", font_size=15)
        zero = seg(ax, 1953, 0, 2026, 0, GREY_C, 1.5)
        below = shade(ax, [(1953, 2026)], -12, 0, OUTPUT, 0.07)
        l1 = path(ax, yrs, G["rg1"], RATE, 3, yr=(-12, 8), smooth=False)
        l10 = DashedVMobject(path(ax, yrs, G["rg10"], DEBT, 2.4, yr=(-12, 8), smooth=False), num_dashes=70)
        side = VGroup(
            label(r"r: \ the 1-year Treasury yield \ (pink) \\ or the 10-year \ (purple, \ dashed)", font_size=18,
                  color=RATE),
            label(r"g: \ growth of nominal GDP", font_size=18, color=GREY_A),
            label(rf"r below g in {100 * G['share1']:.0f}\% of years \\ (with the 10-year rate: \ "
                  rf"{100 * G['share10']:.0f}\%)", font_size=18, color=OUTPUT),
            label(r"above it through the 1980s, \\ and in slumps such as 2009 and 2020", font_size=18, color=INFL),
            label(r"the exception, \ not the rule, \\ is r above g", font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Federal Reserve Board and BEA, \ via FRED; \ after Blanchard, \ \emph{AER} 109(4) (2019)",
                       corner=DR, font_size=12)
        with self.voiceover(
            "Here is r minus g for the United States since 1954. <bookmark mark='a'/> The interest rate on "
            "one-year Treasury bills, and on ten-year bonds, dashed, <bookmark mark='b'/> less the growth of "
            f"nominal GDP. <bookmark mark='c'/> The one-year rate was below growth in {100 * G['share1']:.0f} "
            f"percent of years, the ten-year in {100 * G['share10']:.0f} percent. <bookmark mark='d'/> The big "
            "exceptions were the 1980s, when Volcker's rates were far above growth, and slumps such as 2009 and "
            "2020, when growth itself collapsed. <bookmark mark='e'/> Blanchard's point: in American history r "
            "below g has been the rule. That "
            "does not make debt free. Rates can rise, as they did after 2022, and debt still competes with capital "
            "for savings. But it changes the arithmetic of how much is too much."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(below), FadeIn(zero), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(Create(l1), Create(l10), FadeIn(side[0]), run_time=2)
            for mk, s_ in zip("bcde", side[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(s_))
        self.clear_scene()
