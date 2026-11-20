from __future__ import annotations

from videos.economics.econ34.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.day()
        self.band()
        self.question()
        self.title()
        self.objectives()

    def day(self):
        acts = point_cards([
            (r"morning", r"the Bank of England \\ raises its rate \\ from 10\% to 12\%", RATE),
            (r"afternoon", r"it announces 15\%, \\ to take effect \\ the next day", CRISIS),
            (r"all day", r"it buys pounds \\ with its reserves, \\ by the billion", RES),
            (r"evening", r"the Chancellor \\ suspends sterling's \\ membership of the ERM", GBP),
        ], width=12.8, cols=4, font_size=21).move_to(DOWN * 0.3)
        head = label(r"Wednesday 16 September 1992", font_size=34, color=E.ACCENT).to_edge(UP, buff=0.6)
        sub = label(r"one day in four acts", font_size=22, color=GREY_A).next_to(head, DOWN, buff=0.15)
        tag = published_tag(r"Bank of England; \ HM Treasury papers released 2005", corner=DR, font_size=12)
        with self.voiceover(
            "Wednesday the sixteenth of September 1992, in four acts. <bookmark mark='a'/> In the morning the Bank "
            "of England raises its interest rate from ten percent to twelve. Nothing happens; the pound keeps "
            "falling. <bookmark mark='b'/> In the afternoon it announces fifteen percent, to take effect the next "
            "day. Still nothing. <bookmark mark='c'/> All day it buys pounds with its foreign currency reserves, by "
            "the billion. Papers released by the Treasury in 2005 put the eventual cost at about three point three "
            "billion pounds. <bookmark mark='d'/> In the evening the Chancellor of the Exchequer, Norman Lamont, "
            "announces that sterling's membership of the European Exchange Rate Mechanism is suspended. The rise to "
            "fifteen percent never takes effect."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), FadeIn(tag))
            for mk, c in zip("abcd", acts.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def band(self):
        S = load("story")
        ax = plane([1990, 1994], [2.2, 3.3], center=LEFT * 3.1 + DOWN * 0.4, x_length=6.2, y_length=4.4,
                   xticks=[1990, 1991, 1992, 1993, 1994], yticks=[2.4, 2.6, 2.8, 3.0, 3.2],
                   ylabel=r"marks per pound, \ monthly", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}",
                   font_size=14)
        x0, x1 = 1990.77, 1992.71
        bandr = Rectangle(width=(ax.ax.c2p(x1, 0) - ax.ax.c2p(x0, 0))[0],
                          height=(ax.ax.c2p(0, S["ceiling"]) - ax.ax.c2p(0, S["floor"]))[1], fill_color=DEM,
                          fill_opacity=0.12, stroke_width=0).move_to(ax.ax.c2p((x0 + x1) / 2,
                                                                                (S["floor"] + S["ceiling"]) / 2))
        central = seg(ax, x0, S["central"], x1, S["central"], DEM, 1.5, dashed=True)
        line = path(ax, S["t"], S["gbpdem"], GBP, 3.2, xr=(1990, 1994), smooth=False)
        ax2 = plane([1990, 1994], [30, 50], center=RIGHT * 3.4 + DOWN * 0.4, x_length=5.2, y_length=4.4,
                    xticks=[1990, 1991, 1992, 1993, 1994], yticks=[30, 35, 40, 45, 50],
                    ylabel=r"UK reserves, \ \$ billion, \ end of month", xfmt=lambda v: f"{v:.0f}",
                    yfmt=lambda v: f"{v:.0f}", font_size=14)
        res = path(ax2, S["res_t"], S["reserves"], RES, 3.2, smooth=False)
        k1 = VGroup(label(r"gold band: \ the ERM, \ 2.95 marks $\pm$ 6\%", font_size=16, color=DEM),
                    label(rf"August to October 1992: \ {S['aug92']:.2f} $\to$ {S['oct92']:.2f}, \ "
                          rf"$-{S['fall']:.0f}\%$", font_size=16, color=GBP)).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.06).next_to(ax, UP, buff=0.1)
        k2 = label(rf"August {S['res_aug']:.1f}, \ September {S['res_sep']:.1f}", font_size=16, color=RES).next_to(
            ax2, UP, buff=0.1)
        foot = label(r"the speculators did not cause the contradiction: \ they found it", font_size=24,
                     color=WHITE).to_edge(DOWN, buff=0.35)
        tag = data_tag(r"Board of Governors (H.10); \ IMF IFS; \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "Here is the contradiction. <bookmark mark='a'/> In October 1990 Britain had joined the Exchange Rate "
            "Mechanism at two point nine five German marks to the pound, promising to keep within six percent "
            "either side. <bookmark mark='b'/> By the summer of 1992 the pound was near the bottom of its band. "
            "Germany, paying for unification, kept its interest rates high; Britain, in recession, needed lower "
            "ones, and could not cut them without breaking the band. <bookmark mark='c'/> When the attack came, "
            "the reserves went first. <bookmark mark='d'/> Then the peg. Between August and October the pound "
            f"fell {S['fall']:.0f} percent against the mark, and within five months British interest rates were "
            f"down from {S['i_uk_aug92']:.0f} percent to {S['i_uk_feb93']:.0f}. <bookmark mark='e'/> The "
            "speculators, George Soros most famously, did not cause the contradiction. They found it."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(ax2), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(bandr), Create(central), FadeIn(k1[0]))
            vo.wait_until("b")
            self.play(Create(line), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(res), FadeIn(k2), run_time=1.6)
            vo.wait_until("d")
            self.play(FadeIn(k1[1]), Indicate(line, color=WHITE, scale_factor=1.0))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"what pins an exchange rate down: \ prices, \ interest rates, \ or nothing at all?", font_size=26,
                  color=GBP),
            label(r"why can a country not fix its currency, \ move capital freely and set its own interest rate?",
                  font_size=24, color=DEM),
            label(r"why do currencies crash, \ and who runs the world's money?", font_size=26, color=USD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "This part's question: what sets the price of one money in terms of another, and what can a country "
            "not have at once? <bookmark mark='a'/> What pins an exchange rate down: the prices of goods, interest "
            "rates, or nothing at all? <bookmark mark='b'/> Why can a country not fix its currency, let capital "
            "move freely and set its own interest rate, all three? <bookmark mark='c'/> And why do currencies "
            "crash, and who runs the world's money?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        F = load("film")
        mini = plane([1971, 2027], [1.0, 2.7], x_length=4.2, y_length=1.4)
        logo = path(mini, F["t"], F["v"], GBP, 2.6, smooth=False)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 34 \ $\cdot$ \ The Open Economy", font_size=34, color=E.ACCENT)
        VGroup(logo, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part thirty-four: the open economy."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act VII \ $\cdot$ \ The World Economy", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"the balance of payments; \ you are the governor",
            r"purchasing power parity; \ interest parity; \ the carry trade; \ the random walk",
            r"Mundell-Fleming and the trilemma; \ overshooting",
            r"currency crises in three generations; \ the IMF; \ the euro",
            r"global imbalances; \ the dollar; \ two dials",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "Act seven opens the economy to the world, and here is this part's plan. <bookmark mark='a'/> The "
            "balance of payments, and a game: you are the governor of a central bank under attack. "
            "<bookmark mark='b'/> What should pin exchange rates down, prices and interest rates, and how badly "
            "both fail in the data, down to the uncomfortable fact that no model beats a coin-toss forecast. "
            "<bookmark mark='c'/> The model every policymaker carries, Mundell and Fleming's, with its trilemma, "
            "and Dornbusch's overshooting. <bookmark mark='d'/> Currency crises in three generations, the IMF, and "
            "the euro. <bookmark mark='e'/> Global imbalances, the dollar's peculiar role, and two dials."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
