from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import GAIN, LOSS, PART, TRADE


class Short(VoiceoverScene):
    def construct(self):
        self.card()
        self.mechanics()
        self.payoff()
        self.vw()

    def card(self):
        c = chapter_card(5, r"Short selling", r"How do you sell what you don't own?", lit=(2008,), part=PART)
        with self.voiceover("Chapter five. Short selling."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def mechanics(self):
        steps = VGroup(
            label(r"1. locate: find a lender (a pension fund, an index fund) through your broker", font_size=24),
            label(r"2. borrow the shares, post cash collateral (about 102\% of their value), and sell them", font_size=24),
            label(r"3. pay a borrow fee while short: a fraction of a percent a year, or far more for scarce shares", font_size=24),
            label(r"4. the lender can recall the shares at any time; you must buy them back and return them", font_size=24),
            label(r"5. the lender keeps its dividends: the short seller pays them", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(UP * 0.3)
        if steps.width > 13.0:
            steps.scale_to_fit_width(13.0)
        foot = wrapped_label(r"what makes it possible: the securities-lending market, which lends trillions of dollars "
                             r"of shares and bonds; what makes it dangerous: the next two pictures", 11.4, 22, GREY_A)
        foot.to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "To bet that a price will fall, you sell something you don't own. First your broker locates a lender: "
            "often a pension fund or an index fund, which lends its shares for a fee. <bookmark mark='a'/> You borrow "
            "the shares, post cash collateral worth a little more than they are, and sell them. <bookmark mark='b'/> "
            "While you are short you pay a borrow fee: a fraction of a percent a year for most stocks, and far more "
            "when shares are scarce. <bookmark mark='c'/> The lender can recall its shares at any moment, and then "
            "you must buy them back, at whatever the price is. <bookmark mark='d'/> And any dividend paid while you "
            "are short is yours to pay."
        ) as vo:
            self.play(FadeIn(steps[0]))
            for i, mk in enumerate("abcd", start=1):
                vo.wait_until(mk)
                self.play(FadeIn(steps[i], shift=UP * 0.1))
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def payoff(self):
        g = axes([0, 300], [-210, 110], x_length=6.6, y_length=4.4, xlabel=r"price when you close (sold at 100)",
                 ylabel=r"profit per share", xticks=[0, 100, 200, 300], yticks=[-200, -100, 0, 100], font_size=18)
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        ax = g.ax
        xs = np.array([0, 300])
        long_ = curve(ax, xs, np.clip(xs - 100, -210, 110), GAIN, stroke_width=3)
        short = curve(ax, xs, np.clip(100 - xs, -210, 110), LOSS, stroke_width=4)
        leg = legend([(GAIN, r"long: lose at most 100, gain without limit"),
                      (LOSS, r"short: gain at most 100, lose without limit")], font_size=22)
        leg.to_edge(RIGHT, buff=0.5).shift(UP * 1.6)
        squeeze = VGroup(
            label(r"A short squeeze:", font_size=26, color=QC.IDEA),
            label(r"the price rises, losses mount,", font_size=24),
            label(r"short sellers buy to close or are forced to,", font_size=24),
            label(r"their buying pushes the price higher still.", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(leg, DOWN, buff=0.6).align_to(leg, LEFT)
        with self.voiceover(
            "The payoff is the mirror image of owning. A buyer can lose at most what they paid, and gain without "
            "limit. A short seller can gain at most the price, if it falls to zero, and can lose without limit. "
            "<bookmark mark='a'/> That asymmetry has a dynamic version, the short squeeze. The price rises, short "
            "sellers' losses mount, some buy back to stop the bleeding, some are forced to by margin calls or "
            "recalls, and every purchase pushes the price higher, forcing the next."
        ) as vo:
            self.play(FadeIn(g), Create(long_), Create(short), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in squeeze], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()

    def vw(self):
        pts = [(0, 210.85, r"24 Oct: \texteuro 211"), (2, 1005, r"28 Oct, intraday: above \texteuro 1{,}000"),
               (2.6, 945, r"28 Oct close: \texteuro 945"), (3, 517, r"29 Oct: nearly halved")]
        g = axes([-0.5, 4.5], [0, 1150], x_length=6.0, y_length=4.2, xlabel=r"trading days from Friday 24 October 2008",
                 ylabel=r"Volkswagen ordinary share, reported prices", xticks=[0, 1, 2, 3, 4], yticks=[0, 500, 1000],
                 yfmt=lambda v: rf"\texteuro{int(v)}", font_size=17).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.09, color=LOSS) for x, y, _ in pts])
        labs = VGroup(*[label(t, font_size=19, color=GREY_A).next_to(ax.c2p(x, y), RIGHT if i != 1 else LEFT, buff=0.15)
                        for i, (x, y, t) in enumerate(pts)])
        c = crisis_card(r"26--28 October 2008", r"Volkswagen: the squeeze",
                        r"Porsche disclosed that it held, in shares and cash-settled options, 74.1\% of Volkswagen's "
                        r"ordinary shares. With the state of Lower Saxony holding about 20\%, very few shares were left "
                        r"to buy, and short sellers rushed to cover. For a few hours VW was the world's most valuable "
                        r"company. Hedge funds later sued Porsche, alleging it misled the market; Porsche denied it.",
                        stats=[(r"74.1\%", r"held or controlled by Porsche"),
                               (r"\times 4.8", r"Friday's close to Tuesday's intraday high")],
                        width=6.0, font_size=21).to_edge(RIGHT, buff=0.3)
        src = note(r"reported prices (Reuters, The Wall Street Journal); a schematic of four points, not a price series",
                   font_size=16).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "The most famous squeeze. On Sunday the 26th of October 2008, in the middle of the financial crisis, "
            "Porsche disclosed that, through shares and cash-settled options, it held or controlled seventy-four "
            "point one percent of Volkswagen's ordinary shares. The state of Lower Saxony held about another fifth. "
            "Very few shares were left for anyone to buy, and short sellers needed them. <bookmark mark='a'/> On "
            "Monday and Tuesday the price went from about two hundred and ten euros to above a thousand, and for a "
            "few hours Volkswagen was the most valuable company in the world. Then Porsche released some shares to "
            "ease the squeeze, and the price nearly halved in a day. <bookmark mark='b'/> Hedge funds that had been "
            "short later sued Porsche, alleging that it had misled the market about its intentions; Porsche denied "
            "the claims. Prices in a squeeze are set not by value but by who must buy, and how much there is to buy."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(dots[0]), FadeIn(labs[0]))
            self.play(FadeIn(c, shift=LEFT * 0.2))
            vo.wait_until("a")
            for i in range(1, 4):
                self.play(FadeIn(dots[i]), FadeIn(labs[i]), run_time=0.8)
            vo.wait_until("b")
            self.wait(0.5)
        self.wait(0.4)
        self.clear_scene()
