from __future__ import annotations

from videos.economics.econ2.common import *  # noqa: F403


class Limits(VoiceoverScene):
    def construct(self):
        card(self, 11, r"When the picture fails", r"What does the scissors picture assume?",
             "Chapter eleven. When the picture fails.", scale=("market",), horizon=("a year",))
        self.assumes()
        self.payoff()

    def assumes(self):
        head = heading(r"What the picture assumed")
        items = [
            (r"many traders", r"nobody big enough to move the price alone", E.DEMAND),
            (r"everyone knows what is sold", r"a fish is a fish; \ no hidden faults", E.SUPPLY),
            (r"the trade affects only the traders", r"no smoke drifting onto the neighbours", E.TRUTH),
            (r"values and costs come first", r"not from guesses about tomorrow's price", E.ACCENT),
        ]
        pc = point_cards(items, width=12.8, cols=2, font_size=24).move_to(DOWN * 0.2)
        with self.voiceover(
            "The scissors picture has done a great deal of work in one part, so it's worth saying what it "
            "assumed. <bookmark mark='a'/> It assumed many traders, none big enough to move the price on his "
            "own. <bookmark mark='b'/> It assumed everyone knows what's being sold. <bookmark mark='c'/> It assumed "
            "a trade affects only the two people making it. <bookmark mark='d'/> And it assumed that people's "
            "values and costs come first, and the price follows, rather than people buying because they expect the "
            "price to rise. Each of these fails somewhere, and each failure is a part of this series."
        ) as vo:
            self.play(FadeIn(head))
            for mark, c in zip("abcd", pc.cards):
                vo.wait_until(mark)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def payoff(self):
        pc = payoff_card([
            (r"one seller, or a few", [10, 11, 12]),
            (r"hidden quality", [13]),
            (r"spillovers", [15]),
            (r"prices that feed on themselves", [23, 33]),
            (r"markets built on purpose", [16, 17]),
        ], font_size=24)
        with self.voiceover(
            "Here is where each comes back. <bookmark mark='a'/> A seller who can set his own price, and a few "
            "sellers watching each other: Parts ten to twelve. <bookmark mark='b'/> A used car whose faults only "
            "the seller knows: Part thirteen. <bookmark mark='c'/> A factory whose smoke costs people who never "
            "agreed to anything: Part fifteen. <bookmark mark='d'/> Assets bought because their price is rising, "
            "and crises: Parts twenty-three and thirty-three. <bookmark mark='e'/> And markets that have to be "
            "designed because the picture fails, auctions and matching: Parts sixteen and seventeen."
        ) as vo:
            self.play(FadeIn(pc.head))
            for mark, r in zip("abcde", pc.rows):
                vo.wait_until(mark)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.clear_scene()
