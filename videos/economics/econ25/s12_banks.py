from __future__ import annotations

from videos.economics.econ25.common import *  # noqa: F403


def tacct(title: str, color, assets: list, liabilities: list, width: float = 4.2) -> VGroup:
    """A T-account: a title, a horizontal rule, a vertical rule, assets on the left and liabilities on the right."""
    head = label(title, font_size=22, color=color)
    top = Line(LEFT * width / 2, RIGHT * width / 2, color=color, stroke_width=3)
    mid = Line(ORIGIN, DOWN * 2.0, color=color, stroke_width=3)
    VGroup(head, top).arrange(DOWN, buff=0.12)
    mid.next_to(top, DOWN, buff=0).shift(LEFT * 0)
    mid.move_to(top.get_center() + DOWN * 1.0)
    left = VGroup(*[label(a, font_size=18, color=c) for a, c in assets]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
    right = VGroup(*[label(a, font_size=18, color=c) for a, c in liabilities]).arrange(DOWN, aligned_edge=LEFT,
                                                                                       buff=0.15)
    left.next_to(top, DOWN, buff=0.2).align_to(top, LEFT).shift(RIGHT * 0.15)
    right.next_to(top, DOWN, buff=0.2).align_to(mid, LEFT).shift(RIGHT * 0.15)
    return VGroup(head, top, mid, left, right)


class Banks(VoiceoverScene):
    def construct(self):
        card(self, 10, r"What money is today: \ banks and the central bank", r"Where do deposits come from?",
             "Chapter ten. What money is today: banks and the central bank.",
             lit={2014: r"McLeay, Radia and Thomas"}, scale=("firm", "nation"), horizon=("a day", "years"))
        self.layers()
        self.loan()
        self.multiplier()

    def layers(self):
        ba = load("base")
        rows = VGroup(
            label(r"three kinds of money", font_size=30, color=E.ACCENT),
            label(r"currency: \ notes and coins, \ the central bank's liability, \ held by anyone", font_size=23,
                  color=CB),
            label(r"reserves: \ banks' accounts at the central bank, \ its other liability, \ held only by banks",
                  font_size=23, color=CB),
            label(r"deposits: \ a bank's liability to you, \ the money most people use", font_size=23, color=BANK),
            label(rf"in the United States today, \ currency is about {100 * ba['currency_share_last']:.0f}\% of M2; "
                  r"\ in Britain in 2013, \ deposits were 97\% of broad money", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"McLeay, Radia and Thomas, Bank of England Quarterly Bulletin 2014 Q1", corner=DR,
                            font_size=12)
        with self.voiceover(
            "What is money today? <bookmark mark='a'/> Three things. Currency: notes and coins, which are the "
            "central bank's promise, and which anyone can hold. <bookmark mark='b'/> Reserves: the accounts banks "
            "keep at the central bank, its other kind of liability, which only banks can hold. "
            "<bookmark mark='c'/> And deposits: what your bank owes you. That is the money most people use. "
            f"<bookmark mark='d'/> In the United States, currency is now only about {100 * ba['currency_share_last']:.0f} "
            "percent of M2. In Britain in 2013, the Bank of England counted ninety-seven percent of broad money as "
            "bank deposits. So the question is where deposits come from."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def loan(self):
        t = mo.taccounts(loan=100.0)
        bank0 = tacct(r"the bank", BANK, [(r"reserves \ 10", CB), (r"loans \ 90", BANK)],
                      [(r"deposits \ 90", BANK), (r"capital \ 10", GREY_A)])
        hh0 = tacct(r"Ana", COCO, [(r"(nothing yet)", GREY_D)], [(r"(nothing yet)", GREY_D)])
        VGroup(bank0, hh0).arrange(RIGHT, buff=1.2).move_to(UP * 0.9)
        bank1 = tacct(r"the bank", BANK, [(r"reserves \ 10", CB), (r"loans \ 90", BANK),
                                          (rf"$+$ loan to Ana \ {t['bank']['assets']['loan']:.0f}", MONEY)],
                      [(r"deposits \ 90", BANK), (rf"$+$ Ana's deposit \ {t['bank']['liabilities']['deposit']:.0f}",
                                                  MONEY), (r"capital \ 10", GREY_A)]).move_to(bank0)
        hh1 = tacct(r"Ana", COCO, [(rf"$+$ deposit \ {t['household']['assets']['deposit']:.0f}", MONEY)],
                    [(rf"$+$ loan \ {t['household']['liabilities']['loan']:.0f}", MONEY)]).move_to(hh0)
        rows = VGroup(
            label(r"a bank lends by typing: \ the loan and the deposit appear together", font_size=24,
                  color=E.ACCENT),
            label(r"broad money rises by 100; \ reserves have not changed", font_size=23, color=MONEY),
            label(r"when the loan is repaid, \ the deposit is destroyed", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.7)
        tag = published_tag(r"McLeay, Radia and Thomas (2014): \ ``Money creation in the modern economy''", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Watch two balance sheets. A bank with reserves, loans, deposits and capital, and Ana, who owns a bakery "
            "and wants to borrow a hundred to buy an oven. <bookmark mark='a'/> The bank approves the loan. It does "
            "not hand over anyone else's savings. It writes a new loan on the asset side, and a new deposit in Ana's "
            "name on the liability side, at the same moment. Ana now owns a deposit of a hundred and owes a hundred. "
            "<bookmark mark='b'/> Broad money has risen by a hundred, and the bank's reserves have not changed at all. "
            "<bookmark mark='c'/> When the loan is repaid, the deposit disappears again. In the words of the Bank "
            "of England's 2014 article, lending creates deposits."
        ) as vo:
            self.play(FadeIn(bank0), FadeIn(hh0), FadeIn(tag))
            vo.wait_until("a")
            self.play(ReplacementTransform(bank0, bank1), ReplacementTransform(hh0, hh1), FadeIn(rows[0]),
                      run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def multiplier(self):
        ba = load("base")
        t = np.array(ba["t"])
        ax = plane([1959, 2027], [0, 26000], center=LEFT * 2.0 + DOWN * 0.3, x_length=7.8, y_length=4.8,
                   xticks=[1960, 1980, 2000, 2020], yticks=[0, 5000, 10000, 15000, 20000, 25000],
                   ylabel=r"billions of dollars", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v / 1000:.0f}t",
                   font_size=16)
        m2 = path(ax, t, ba["m2"], color=BANK, width=3, smooth=False)
        base = path(ax, t, ba["base"], color=CB, width=3, smooth=False)
        side = VGroup(
            label(r"the textbook multiplier: \\ banks lend out reserves, \\ so M2 = (a multiple) $\times$ base",
                  font_size=19, color=GREY_A),
            label(rf"2007: \ M2 was {ba['mult_2007']:.1f} times the base", font_size=20, color=BANK),
            label(rf"2008--2014: \ the base rose from \\ {commas(ba['base_2007'])} to {commas(ba['base_2014'])} "
                  r"billion; \\ M2 rose by half", font_size=20, color=CB),
            label(rf"2014: \ {ba['mult_2014']:.1f} times", font_size=20, color=BANK),
            label(r"banks lend when lending pays; \\ reserves follow, \\ not the other way round", font_size=20,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Federal Reserve Board: \ M2 and the monetary base, \ via FRED", corner=DR, font_size=12)
        with self.voiceover(
            "That overturns a story still told in many textbooks. <bookmark mark='a'/> In the story, the central "
            "bank fixes reserves, banks lend out a multiple of them, and the money supply is a fixed multiple of "
            f"base money. <bookmark mark='b'/> In 2007, M2 was about {ba['mult_2007']:.0f} times America's monetary "
            "base. <bookmark mark='c'/> Then, after the crisis, the Federal Reserve bought bonds on a vast scale and "
            f"the base rose from about {ba['base_2007']:,.0f} billion dollars to about {ba['base_2014']:,.0f} billion. "
            "If the multiplier held, M2 should have multiplied too. It rose by about half. "
            f"<bookmark mark='d'/> By 2014, M2 was only {ba['mult_2014']:.1f} times the base. "
            "<bookmark mark='e'/> Banks lend when lending pays, given the interest rate the central bank sets, and "
            "reserves follow. What the central bank controls is the price of reserves, not the quantity of money. "
            "Part thirty-one builds monetary policy on that."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(m2), Create(base), FadeIn(side[0]), run_time=2)
            for mk, r_ in zip("bcde", side[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
        self.clear_scene()
