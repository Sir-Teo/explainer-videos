from __future__ import annotations

from videos.economics.econ25.common import *  # noqa: F403


class Barter(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Barter, \ and what money does", r"Why is trading without money so hard?",
             "Chapter one. Barter, and what money does.", lit={1875: r"Jevons", 1998: r"Kocherlakota"},
             scale=("person", "market"), horizon=("a day",))
        self.zelie()
        self.coincidence()
        self.functions()
        self.memory()

    def zelie(self):
        rows = VGroup(
            label(r"Jevons, \emph{Money and the Mechanism of Exchange}, \ 1875: \ a singer from Paris gives a concert "
                  r"in the Society Islands", font_size=21, color=GREY_A),
            label(r"her share of the takings:", font_size=24, color=WHITE),
            VGroup(label(r"3 pigs", font_size=30, color=COCO), label(r"23 turkeys", font_size=30, color=COCO),
                   label(r"44 chickens", font_size=30, color=COCO), label(r"5{,}000 coconuts", font_size=30,
                                                                         color=COCO)).arrange(RIGHT, buff=0.6),
            label(r"and quantities of bananas, \ lemons and oranges", font_size=22, color=GREY_A),
            label(r"she could eat almost none of it, \ and there was no one to sell it to: \ she fed the fruit to the "
                  r"pigs", font_size=23, color=PRICE),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.2)
        tag = published_tag(r"Jevons, \emph{Money and the Mechanism of Exchange} (1875), \ ch.\ 1", corner=DR,
                            font_size=12)
        with self.voiceover(
            "William Stanley Jevons opened his book on money, in 1875, with a story. "
            "<bookmark mark='a'/> Mademoiselle Zélie, a singer from a Paris theatre, gave a concert in the Society "
            "Islands, in the Pacific, for a third of the takings. <bookmark mark='b'/> Her share came to three pigs, "
            "twenty-three turkeys, forty-four chickens, five thousand coconuts, <bookmark mark='c'/> and quantities "
            "of bananas, lemons and oranges. <bookmark mark='d'/> Coins were scarce on the islands, she could eat "
            "very little of it herself, and there was nobody to sell it to. So, Jevons reports, the fruit went to "
            "feed the pigs and the poultry."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in rows[2]], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def coincidence(self):
        b = load("barter")
        ax = plane([2, 12], [0, 1.0], center=LEFT * 2.2 + DOWN * 0.3, x_length=7.2, y_length=4.8,
                   xticks=[2, 4, 6, 8, 10, 12], yticks=[0, 0.25, 0.5, 0.75, 1.0], xlabel=r"number of goods",
                   ylabel=r"chance a stranger will trade with you", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:g}", font_size=16)
        ns = np.linspace(2, 12, 200)
        bar = path(ax, ns, 1 / (ns - 1) ** 2, color=PRICE, width=4)
        mon = path(ax, ns, 1 / (ns - 1), color=MONEY, width=4)
        k = b["n"].index(10)
        side = VGroup(
            label(r"barter: \ they must have what \\ you want \emph{and} want what \\ you have: \ $1/(n-1)^2$",
                  font_size=20, color=PRICE),
            label(r"with money: \ only one side \\ has to match: \ $1/(n-1)$", font_size=20, color=MONEY),
            label(rf"ten goods: \ 1 in {1 / b['barter'][k]:.0f} \ against \ 1 in {1 / b['money'][k]:.0f}",
                  font_size=23, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.35)
        tag = agora_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Jevons named the problem: the double coincidence of wants. Suppose there are n goods, you hold one and "
            "want another, and you meet a stranger at random. <bookmark mark='a'/> Under barter, the stranger "
            "must have exactly what you want and also want exactly what you have: a chance of one over n minus one, "
            "squared. <bookmark mark='b'/> If everyone accepts one good, money, in payment, only one side has to "
            "match: you can sell to anyone who wants what you have, and buy from anyone who has what you want. "
            f"<bookmark mark='c'/> With ten goods, that is one chance in {1 / b['barter'][k]:.0f} against one in "
            f"{1 / b['money'][k]:.0f}. The more goods an economy has, the more it needs money."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(bar), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Indicate(bar, color=WHITE))
            vo.wait_until("b")
            self.play(Create(mon), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def functions(self):
        n = 100
        rows = VGroup(
            label(r"money's three jobs", font_size=30, color=E.ACCENT),
            label(r"a medium of exchange: \ accepted in payment by people who do not want it for itself", font_size=23,
                  color=MONEY),
            label(rf"a unit of account: \ prices in one unit; \ with {n} goods, \ {n - 1} prices instead of "
                  rf"{commas(n * (n - 1) // 2)}", font_size=23, color=COCO),
            label(r"a store of value: \ a way to carry purchasing power from today to later, \ if prices are stable",
                  font_size=23, color=CB),
            label(r"the second and third can be done by other things; \ the first is what makes money money",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        with self.voiceover(
            "Textbooks give money three jobs. <bookmark mark='a'/> It is a medium of exchange: people accept it in "
            "payment though they do not want it for itself, only to pass it on. <bookmark mark='b'/> It is a unit "
            f"of account: with a hundred goods, prices in one unit need {n - 1} numbers, while every pair's rate of "
            f"exchange would need {n * (n - 1) // 2:,}. <bookmark mark='c'/> And it is a store of value, if its "
            "purchasing power is stable. <bookmark mark='d'/> Bonds and houses store value; any unit can be used to "
            "count. The first job, being accepted in payment, is what makes money money."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def memory(self):
        rows = VGroup(
            label(r"Narayana Kocherlakota, \ 1998: \ \emph{money is memory}", font_size=28, color=E.ACCENT),
            label(r"if everyone could see a complete public record of everyone's past trades and gifts,", font_size=22,
                  color=GREY_A),
            label(r"credit and reputation could do everything money does", font_size=24, color=BANK),
            label(r"money is a crude record: \ holding it shows you once gave something of value", font_size=24,
                  color=MONEY),
            label(r"Yap's stones were a public ledger; \ so is a bank's database, \ and a blockchain", font_size=22,
                  color=CB),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Kocherlakota, JET 81(2) (1998): \ 232--251", corner=DR, font_size=12)
        with self.voiceover(
            "There is a deeper way to see it. <bookmark mark='a'/> Narayana Kocherlakota proved in 1998 that money is "
            "a kind of memory. <bookmark mark='b'/> If everyone could consult a complete public record of who had "
            "given what to whom, <bookmark mark='c'/> then credit and reputation could do everything that money "
            "does: you would be served because the record shows you have served others. "
            "<bookmark mark='d'/> Money is a crude substitute for that record. Holding it shows that at some point you "
            "gave something of value in exchange for it. <bookmark mark='e'/> Yap's stones, whose owners everyone "
            "remembered, were a public ledger. So is a bank's database, and so is a blockchain."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
