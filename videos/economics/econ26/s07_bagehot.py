from __future__ import annotations

from videos.economics.econ26.common import *  # noqa: F403


class Bagehot(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Bagehot's rule: \ the lender of last resort", r"Who lends to a bank that everyone is "
             r"running from?", "Chapter six. Bagehot's rule: the lender of last resort.",
             lit={1866: r"Overend, Gurney", 1873: r"\emph{Lombard Street}"}, scale=("nation",),
             horizon=("a day",))
        self.overend()
        self.rule()
        self.numbers()

    def overend(self):
        rows = VGroup(
            label(r"London, \ May 1866: \ Overend, Gurney and Company, \ the great discount house, \ fails",
                  font_size=23, color=RUN),
            label(r"the next day, \ ``Black Friday'', \ depositors run on banks across the City", font_size=23,
                  color=RUN),
            label(r"the Bank of England lends, \ heavily, \ to anyone with sound security", font_size=23, color=CB),
            label(r"Walter Bagehot, \ editor of \emph{The Economist}, \ draws the lesson in \emph{Lombard Street}, \ "
                  r"1873", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.2)
        tag = published_tag(r"Bagehot, \emph{Lombard Street: A Description of the Money Market} (1873)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "The third cure is older. <bookmark mark='a'/> In May 1866, Overend, Gurney and Company, the biggest "
            "discount house in London, failed. <bookmark mark='b'/> The next day, remembered as Black Friday, "
            "depositors ran on banks across the City. <bookmark mark='c'/> The Bank of England lent heavily to "
            "anyone who could offer good security, and the panic subsided. <bookmark mark='d'/> Walter Bagehot, "
            "the editor of The Economist, turned that into a rule in his book Lombard Street, in 1873."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def rule(self):
        rows = VGroup(
            label(r"Bagehot's rule, \ in a panic:", font_size=28, color=E.ACCENT),
            label(r"lend freely: \ without limit, \ so that nobody need run for fear of being last", font_size=24,
                  color=CB),
            label(r"at a penalty rate: \ so only banks that need it borrow, \ and they repay quickly", font_size=24,
                  color=RATE),
            label(r"against good collateral: \ to banks that are illiquid, \ not to banks that are insolvent",
                  font_size=24, color=EQUITY),
            label(r"the hard part is telling the two apart in a hurry", font_size=22, color=HOLD),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        with self.voiceover(
            "Bagehot's rule has three parts, as it is usually summarized. <bookmark mark='a'/> In a panic, the "
            "central bank should lend freely, without limit, so that nobody needs to run for fear of being last. "
            "<bookmark mark='b'/> At a penalty rate, so that only banks that need the money borrow it, and repay as "
            "soon as they can. <bookmark mark='c'/> And against good collateral: to banks that are illiquid, short of "
            "cash but sound, not to banks that are insolvent. <bookmark mark='d'/> The hard part, every time, is "
            "telling the two apart in the middle of a panic."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def numbers(self):
        L = load("llr")
        rows = VGroup(
            label(rf"a sound bank: \ reserves {L['liquid']:.0f}, \ loans {L['loans']:.0f}, \ deposits "
                  rf"{L['deposits']:.0f}, \ equity {L['equity']:.0f}", font_size=23, color=GREY_A),
            label(rf"a panic: \ depositors withdraw {L['withdraw']:.0f}; \ it needs {L['need']:.0f} beyond its "
                  r"reserves", font_size=23, color=RUN),
            label(rf"no lender: \ sell loans in a hurry at {100 * L['fire_price']:.0f}\% of their value: \ "
                  rf"{L['sold']:.0f} of loans sold, \ equity {L['equity_fire']:.1f}: \ insolvent", font_size=23,
                  color=RUN),
            label(rf"Bagehot's lender: \ borrow {L['need']:.0f} against loans at {100 * L['penalty']:.0f}\% \ \ "
                  rf"equity {L['equity_llr']:.1f}: \ it survives", font_size=23, color=CB),
            label(r"the fire sale turns a liquidity problem into a solvency problem", font_size=25, color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Agora makes the point with numbers. <bookmark mark='a'/> A sound bank holds ten in reserves and ninety "
            f"in loans, against ninety of deposits and ten of equity. <bookmark mark='b'/> In a panic, depositors "
            f"withdraw {L['withdraw']:.0f}, twenty more than its reserves. <bookmark mark='c'/> With no lender, it "
            f"must sell loans in a hurry, at sixty percent of their value: {L['sold']:.0f} of loans to raise twenty, "
            f"and its equity falls to {L['equity_fire']:.1f}. It is insolvent. <bookmark mark='d'/> With Bagehot's "
            "lender, it borrows twenty against its loans at a penalty rate of five percent, and its equity is "
            f"{L['equity_llr']:.0f}. <bookmark mark='e'/> The fire sale is what kills it: it turns a shortage of "
            "cash into a hole in the balance sheet."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
