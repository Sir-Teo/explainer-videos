from __future__ import annotations

from videos.economics.econ13.common import *  # noqa: F403


class Fixes(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Guarantees, \ reputations \ and inspectors", r"How do markets for things you can't inspect "
             r"survive, \ and what does it cost?", "Chapter three. Guarantees, reputations and inspectors.",
             scale=("person", "firm", "market"), horizon=("a season", "a decade"))
        self.guarantee()
        self.others()

    def guarantee(self):
        w = load("warranty")
        bars = VGroup()
        ax = plane([0, 3], [0, 100], center=LEFT * 3.2 + DOWN * 0.3, x_length=5.0, y_length=4.6, xticks=[],
                   yticks=[0, 30, 60, 90], ylabel=r"\$", font_size=16, yfmt=lambda v: f"{v:.0f}")
        a = ax.ax

        def bar(x, h, col, txt):
            r = Rectangle(width=0.7, height=a.c2p(0, h)[1] - a.c2p(0, 0)[1], stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to(a.c2p(x, 0), aligned_edge=DOWN)
            t = label(txt, font_size=15, color=col).next_to(r, DOWN, buff=0.12)
            return VGroup(r, t)

        bars.add(bar(0.6, w["premium_good"], GOOD, r"what a good seller \\ gains by being believed"),
                 bar(1.5, w["cost_good"], SIGNAL, r"a guarantee's cost \\ to a good seller"),
                 bar(2.4, w["cost_bad"], LEMON, r"its cost to \\ a bad seller"))
        side = VGroup(
            label(rf"good boats worth \${w['good']:.0f}, \ bad ones \${w['bad']:.0f}, \\ half of each: \ unseen, \ "
                  rf"every boat sells for \${w['pooled_price']:.0f}", font_size=21),
            label(rf"a guarantee: \ the seller pays the \${w['fix']:.0f} repair \\ if the boat breaks within a season",
                  font_size=21, color=SIGNAL),
            label(rf"a good boat breaks one time in {1 / w['break_good']:.0f}: \\ the promise costs its seller "
                  rf"\${w['cost_good']:.0f}", font_size=21, color=GOOD),
            label(rf"a bad boat breaks {100 * w['break_bad']:.0f}\% of the time: \\ \${w['cost_bad']:.0f}, \ more than "
                  rf"the \${w['good'] - w['bad']:.0f} it would gain", font_size=21, color=LEMON),
            label(r"only good sellers offer it, \ so buyers believe it: \\ a promise that is cheap only if it's true",
                  font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "The simplest fix is a promise. <bookmark mark='a'/> Suppose half the island's used boats are good, worth "
            "ninety dollars, and half are bad, worth thirty. If buyers can't tell them apart, every boat sells for "
            "sixty, and good boats are undersold. <bookmark mark='b'/> Now let a seller offer a guarantee: if the boat "
            "breaks within a season, the seller pays the hundred-dollar repair. <bookmark mark='c'/> A good boat "
            "breaks one time in ten, so the promise costs its seller ten dollars, against the thirty it gains by being "
            "believed. <bookmark mark='d'/> A bad boat breaks seven times in ten, so the same promise would cost its "
            "seller seventy dollars, more than the sixty it could gain by passing as good. "
            "<bookmark mark='e'/> Only good sellers offer the guarantee, so buyers are right to believe it. It works "
            "because it is cheap only for those telling the truth, an idea the next chapter makes general."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(bars[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(bars[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(bars[2]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def others(self):
        rows = point_cards([
            (r"reputation", r"a seller who will \\ sell again", GOOD),
            (r"brand names", r"a name with \\ a lot to lose", SIGNAL),
            (r"chains", r"the same meal \\ in every town", POOL),
            (r"inspectors", r"a mechanic, \ a history \\ report, \ an auditor", LEMON),
            (r"licences", r"doctors, \ lawyers, \\ electricians", USED),
            (r"the law", r"disclosure, \ fraud, \\ lemon laws", LOSS),
        ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.2)
        head = label(r"the institutions that grow around not knowing", font_size=32, color=E.ACCENT
                     ).to_edge(UP, buff=0.5)
        foot = label(r"each costs something: \ the premium for a brand, \ the inspector's fee, \ the licence's barrier "
                     r"to entry", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Akerlof listed the institutions that grow up around not knowing. <bookmark mark='a'/> Reputation: a "
            "seller who expects to sell again has a reason to be honest today. A brand name is a reputation with a "
            "great deal to lose. A chain promises the same meal in every town, which a traveller who will never "
            "return can rely on. Inspectors sell information: a mechanic's check, a vehicle history report, an "
            "auditor's signature. Licences certify doctors, lawyers and electricians. And the law punishes fraud, "
            "requires disclosure, and in many American states protects buyers of new cars that turn out to be "
            "lemons. <bookmark mark='b'/> Each of them costs something: the premium paid for a brand, the "
            "inspector's fee, the barrier a licence puts in front of newcomers. That cost is the price of not "
            "knowing."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in rows.cards], lag_ratio=0.6), run_time=16)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()
