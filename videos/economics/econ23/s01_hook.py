from __future__ import annotations

from videos.economics.econ23.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.numbers()
        self.why()
        self.question()
        self.advice()
        self.title()
        self.objectives()

    def numbers(self):
        mp = load("moments")["published"]
        hc = history_card(1985, r"Rajnish Mehra and Edward Prescott", r"\emph{The Equity Premium: A Puzzle}, \ "
                          r"Journal of Monetary Economics", color=STOCK, width=11.0, font_size=23).to_edge(UP, buff=0.5)
        left = VGroup(label(r"the model", font_size=26, color=SDF),
                      label(rf"at most {100 * mp['model_max_premium']:.2f}\%", font_size=44, color=SDF),
                      label(r"a year more for stocks than for bills, \\ with sensible patience and risk aversion",
                            font_size=19, color=GREY_A)).arrange(DOWN, buff=0.2)
        right = VGroup(label(r"the record, \ 1889--1978", font_size=26, color=STOCK),
                       label(rf"{100 * mp['premium_mean']:.2f}\%", font_size=44, color=STOCK),
                       label(rf"stocks {100 * mp['stock']:.2f}\% a year after inflation, \\ short-term bills "
                             rf"{100 * mp['bill']:.2f}\%", font_size=19, color=GREY_A)).arrange(DOWN, buff=0.2)
        VGroup(left, right).arrange(RIGHT, buff=1.6).next_to(hc, DOWN, buff=0.8)
        gap = label(r"a factor of about seventeen", font_size=28, color=HOLD).next_to(VGroup(left, right), DOWN,
                                                                                     buff=0.6)
        tag = published_tag(r"Mehra and Prescott, JME 15(2) (1985): \ 145--161", corner=DR, font_size=12)
        with self.voiceover(
            "In 1985 two economists, Rajnish Mehra and Edward Prescott, took the standard model of how assets are "
            "priced and fed it ninety years of American consumption. Then they asked what stocks should have paid "
            "over safe, short-term government bills. <bookmark mark='a'/> With patience and risk aversion in any "
            "range they thought sensible, the model's answer was at most "
            f"{100 * mp['model_max_premium']:.2f} percent a year. <bookmark mark='b'/> The record, from 1889 to "
            f"1978, was {100 * mp['premium_mean']:.2f} percent: stocks returned "
            f"{100 * mp['stock']:.2f} percent a year after inflation, bills {100 * mp['bill']:.2f}. "
            "<bookmark mark='c'/> The gap is a factor of about seventeen. They called it a puzzle, and forty years "
            "later it still has that name."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(left, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(right, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(gap))
        self.clear_scene()

    def why(self):
        rows = rows_card([
            (r"why it matters beyond Wall Street", E.ACCENT, 28),
            (r"the premium is the price of risk: \ what investors demand to bear bad times", STOCK, 24),
            (r"it sets the cost of capital, \ and so which factories, \ houses and ideas get built", FIRM, 24),
            (r"it values pensions, \ insurance, \ and the long-run future in climate policy", BILL, 24),
            (r"and a model that cannot price it does not understand how people fear risk", SDF, 24),
        ])
        with self.voiceover(
            "Why should anyone outside a trading floor care? <bookmark mark='a'/> Because the premium is the price "
            "of risk: what people demand for holding something that does badly in bad times. "
            "<bookmark mark='b'/> It sets the cost of capital, and so which factories, houses and ideas get built. "
            "<bookmark mark='c'/> It values pensions and insurance, and the long-run future in climate policy. "
            "<bookmark mark='d'/> And a model that cannot price it does not yet understand how people fear risk."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"how does a firm decide whether to build, \ and when to wait?", font_size=26, color=FIRM),
            label(r"what makes one asset pay more than another?", font_size=26, color=STOCK),
            label(r"and do prices track value, \ or run away from it?", font_size=26, color=VALUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "This part's question: what is a claim on the future worth, and how does that decide what gets built? "
            "<bookmark mark='a'/> How does a firm decide whether to build, and when to wait? "
            "<bookmark mark='b'/> What makes one asset pay more than another? <bookmark mark='c'/> And do prices "
            "track value, or run away from it?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def advice(self):
        box = RoundedRectangle(width=10.6, height=3.0, corner_radius=0.15, stroke_color=GREY_B, stroke_width=2,
                               fill_color=GREY_E, fill_opacity=0.5)
        t = VGroup(label(r"Not investment advice", font_size=38, color=WHITE),
                   label(r"this part is about how assets are priced and how the theories are tested; \\ its returns "
                         r"are history, \ and its trees and firms are models, \\ not recommendations to buy or sell "
                         r"anything", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.35).move_to(box)
        with self.voiceover(
            "One card before we start. This part is about how assets are priced and how the theories are tested. "
            "Its returns are history, and its trees and firms are models, not recommendations to buy or sell "
            "anything."
        ):
            self.play(FadeIn(box), FadeIn(t))
        self.wait(1.0)
        self.clear_scene()

    def title(self):
        f = load("film")
        mini = plane([1871, 2013], [0, np.log10(10000)], x_length=4.2, y_length=1.5)
        logo = VGroup(path(mini, f["years"], np.log10(f["stock"]), STOCK, width=4, smooth=False),
                      path(mini, f["years"], np.log10(f["bill"]), BILL, width=4, smooth=False))
        t = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 23 \ $\cdot$ \ Capital and Asset Prices", font_size=34, color=E.ACCENT)
        VGroup(logo, t, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part twenty-three: capital and asset prices."):
            self.play(Create(logo), run_time=1.4)
            self.play(Write(t), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act V \ $\cdot$ \ The Long Run", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"present value and the Gordon formula; \ the user cost, \ Tobin's q and adjustment costs",
            r"the option to wait; \ Modigliani and Miller's pie",
            r"the Lucas tree and the stochastic discount factor; \ risk premia as covariance",
            r"the equity premium puzzle computed; \ habits, \ long-run risk and rare disasters",
            r"excess volatility, \ predictability, \ bubbles, \ housing; \ the return on everything",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "This part continues Act Five. <bookmark mark='a'/> You'll value a stream of dividends, "
            "and see how a firm decides how much to invest when building takes time and costs more in a hurry. "
            "<bookmark mark='b'/> You'll see why waiting can be worth more than building, and why, in a perfect "
            "market, how a firm is financed does not matter. <bookmark mark='c'/> You'll price a tree that bears "
            "fruit, and find that risk is priced by when it hurts. <bookmark mark='d'/> Then the puzzle, computed "
            "three ways, and three ways economists have tried to repair it. <bookmark mark='e'/> And whether prices "
            "move too much, bubbles in the laboratory, houses as assets, and the long-run return on everything."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
