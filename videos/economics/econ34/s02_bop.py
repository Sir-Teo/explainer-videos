from __future__ import annotations

from videos.economics.econ34.common import *  # noqa: F403


class BOP(VoiceoverScene):
    def construct(self):
        card(self, 1, r"The balance of payments", r"What must a country's dealings with the world add up to?",
             "Chapter one. The balance of payments.", lit={2006: r"America's widest deficit"},
             scale=("nation", "world"), horizon=("a year",))
        self.identity()
        self.america()

    def identity(self):
        eqs = VGroup(
            label(r"every purchase from abroad is paid for, \ so the accounts must balance", font_size=25,
                  color=E.ACCENT),
            MathTex(r"\underbrace{\text{current account}}_{\text{exports} - \text{imports} + \text{net income}}"
                    r"\;+\;\underbrace{\text{financial account}}_{\text{net sales of assets abroad}} \;=\; 0",
                    font_size=36, color=WHITE),
            label(r"and from the national accounts:", font_size=22, color=GREY_A),
            MathTex(r"Y = C + I + G + (X - M) \quad\Longrightarrow\quad CA = (Y - C - G) - I = S - I",
                    font_size=38, color=USD),
            label(r"a deficit is not a loss: \ it is a country investing more than it saves, \ and borrowing the "
                  r"difference", font_size=22, color=CALM),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"IMF, \ \emph{Balance of Payments Manual}, \ 6th ed. (2009)", corner=DR, font_size=12)
        with self.voiceover(
            "Start with accounting, because in international economics it settles more arguments than theory does. "
            "<bookmark mark='a'/> Every purchase from abroad has to be paid for, so a country's dealings with the "
            "world must balance. <bookmark mark='b'/> The current account, exports minus imports plus net income "
            "from abroad, and the financial account, what a country sells of its assets to foreigners, add up to "
            "zero. A country that imports more than it exports is selling assets, or borrowing, to pay. "
            "<bookmark mark='c'/> The national accounts of Part three give the same thing another way. "
            "<bookmark mark='d'/> Output is spent on consumption, investment, government purchases and net exports, "
            "so the current account is national saving minus investment. <bookmark mark='e'/> A deficit is not a "
            "loss or a scorecard. It is a country investing more than it saves, and borrowing the difference."
        ) as vo:
            self.play(FadeIn(eqs[0]), FadeIn(tag))
            for mk, r_ in zip("bcde", eqs[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def america(self):
        B = load("bop")
        ax = plane([1999, 2027], [-8, 1], center=LEFT * 3.3 + DOWN * 0.3, x_length=5.6, y_length=4.4,
                   xticks=[2000, 2010, 2020], yticks=[-8, -6, -4, -2, 0], ylabel=r"US current account, \ \% of GDP",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        ax2 = plane([2005, 2027], [-80, 0], center=RIGHT * 3.3 + DOWN * 0.3, x_length=5.6, y_length=4.4,
                    xticks=[2006, 2012, 2018, 2024], yticks=[-80, -60, -40, -20, 0],
                    ylabel=r"US net international investment position, \ \% of GDP", xfmt=lambda v: f"{v:.0f}",
                    yfmt=lambda v: f"{v:.0f}", font_size=14)
        ca = path(ax, B["ca_t"], B["ca"], USD, 3.2, smooth=False)
        ni = path(ax2, B["ni_t"], B["niip"], CRISIS, 3.2, smooth=False)
        z1 = seg(ax, 1999, 0, 2027, 0, GREY_C, 1.2)
        k1 = label(rf"widest: \ {B['ca_min']:.1f}\% in {B['ca_min_t']:.0f}; \ now {B['ca_last']:.1f}\%",
                   font_size=16, color=USD).next_to(ax, UP, buff=0.1)
        k2 = label(rf"{B['niip_first']:.0f}\% in 2006 \ $\to$ \ {B['niip_last']:.0f}\% now", font_size=16,
                   color=CRISIS).next_to(ax2, UP, buff=0.1)
        tag = data_tag(r"BEA, \ via FRED: \ IEABC, \ IIPUSNETIQ, \ GDP", corner=DR, font_size=12)
        with self.voiceover(
            "America is the largest example. <bookmark mark='a'/> It has run a current account deficit every year "
            f"of this century, widest at {abs(B['ca_min']):.1f} percent of GDP in {B['ca_min_t']:.0f}, and "
            f"{abs(B['ca_last']):.1f} percent now. <bookmark mark='b'/> The financial account is the other side: "
            "Americans have sold assets to foreigners and borrowed from them every year, so the country's net "
            f"position against the world went from minus {abs(B['niip_first']):.0f} percent of GDP in 2006 to "
            f"minus {abs(B['niip_last']):.0f} percent now. <bookmark mark='c'/> Whether that is a problem depends on "
            "what the borrowing paid for, what the debts cost, and what currency they are in. For the United "
            "States, as chapter eleven shows, the answers are unusual."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(ax2), FadeIn(z1), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(ca), FadeIn(k1), run_time=1.8)
            vo.wait_until("b")
            self.play(Create(ni), FadeIn(k2), run_time=1.8)
            vo.wait_until("c")
            self.play(Indicate(ni, color=WHITE, scale_factor=1.0))
        self.clear_scene()
