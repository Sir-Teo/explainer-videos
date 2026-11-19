from __future__ import annotations

from videos.economics.econ8.common import *  # noqa: F403

REGIMES = (("first best", r"if investment \\ could be contracted", GREY_B),
           ("A owns", r"the yard \\ owns the dies", OUT),
           ("B owns", r"the supplier \\ owns them", LAB), ("apart", r"each owns \\ its own", CAP))


class Property(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Who should own the asset?", r"If contracts can't cover everything, what does ownership do?",
             "Chapter twelve. Who should own the asset?", lit={1990: r"Hart and Moore"}, scale=("firm",),
             horizon=("a decade",))
        self.idea()
        self.bars()

    def idea(self):
        rows = VGroup(
            label(r"Grossman and Hart (1986); \ Hart and Moore (1990)", font_size=26, color=GREY_B),
            label(r"contracts are incomplete: \ nobody can write down every future contingency", font_size=27),
            label(r"ownership is the right to decide whatever the contract left out: \\ \emph{residual control "
                  r"rights}", font_size=27, color=FIRM),
            label(r"owning an asset improves your position when you bargain later, \\ so it strengthens your "
                  r"incentive to invest now", font_size=26),
            label(r"and weakens the incentive of whoever doesn't own it", font_size=26, color=HOLD),
            label(r"integration is not free: \ it moves incentives from one party to another", font_size=27,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Williamson said that specific assets belong inside a firm. Sanford Grossman, Oliver Hart and John Moore "
            "asked what being inside a firm actually changes. <bookmark mark='a'/> Their starting point: contracts "
            "are incomplete. Nobody can write down what should happen in every future circumstance. "
            "<bookmark mark='b'/> Ownership of an asset is the right to decide whatever the contract left out: what "
            "they called residual control rights. <bookmark mark='c'/> If you own the machine, you're in a stronger "
            "position when the two of you bargain later, so you have more reason to invest in the relationship now. "
            "<bookmark mark='d'/> And the party who doesn't own it has less. <bookmark mark='e'/> So integration "
            "isn't free. Buying your supplier strengthens your incentives and weakens his."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            for mk, r_ in zip("abcde", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def bars(self):
        b = load("boundary")
        g = b["ghm"]
        ax = plane([-0.5, 3.5], [0, 9.5], center=LEFT * 3.0 + DOWN * 0.3, x_length=6.4, y_length=4.8, xticks=[],
                   yticks=[0, 2, 4, 6, 8], ylabel=r"joint surplus", font_size=17)
        a = ax.ax
        bars, labs = VGroup(), VGroup()
        for k, (key, name, col) in enumerate(REGIMES):
            v = g[key]["surplus"]
            r_ = Rectangle(width=0.62, height=a.c2p(0, v)[1] - a.c2p(0, 0)[1], stroke_width=0, fill_color=col,
                           fill_opacity=0.85).move_to(a.c2p(k, 0), aligned_edge=DOWN)
            bars.add(VGroup(r_, label(f"{v:.2f}", font_size=20, color=col).next_to(r_, UP, buff=0.06)))
            labs.add(label(name, font_size=17, color=col).next_to(a.c2p(k, 0), DOWN, buff=0.15))
        side = VGroup(
            label(r"two parties: \ Crusoe's yard (A) \\ and a die maker (B)", font_size=23),
            label(r"A's investment matters four times as much", font_size=22, color=OUT),
            label(r"the owner keeps 80\% of its own investment's \\ value if the relationship breaks down",
                  font_size=21, color=GREY_A),
            label(rf"A owns: \ A invests {g['A owns']['eA']:.1f} (best {g['first best']['eA']:.0f}), \ B "
                  rf"{g['A owns']['eB']:.1f}", font_size=22, color=OUT),
            label(rf"B owns: \ A {g['B owns']['eA']:.1f}, \ B {g['B owns']['eB']:.1f}", font_size=22, color=LAB),
            label(r"give the asset to the party whose investment \\ matters most: \ here, integrate under A",
                  font_size=23, color=E.ACCENT),
            label(r"swap the importance, and B should own: \\ ownership follows incentives, \ not size",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.35)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Here is their model on the Island. <bookmark mark='a'/> Crusoe's yard and a maker of dies can each invest "
            "in their relationship, and the yard's investment matters four times as much. Whoever owns the dies "
            "keeps most of the value of their own investment if the relationship breaks down. "
            "<bookmark mark='b'/> If investment could be written into a contract, the surplus would be eight and a "
            "half. <bookmark mark='c'/> With the yard owning the dies, the yard invests nearly as much as it should, "
            "and the surplus is eight point three. With the die maker owning them, six and a half; with each keeping "
            "its own, less still. <bookmark mark='d'/> So the asset should go to the party whose investment matters "
            "most: here, the yard should integrate. Swap the importance of the two investments and the die maker "
            "should own. Ownership follows incentives, not size. Part fourteen takes up incentives inside the firm, "
            "and Part sixty-two the modern evidence."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(labs), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeIn(bars[0], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in bars[1:]], lag_ratio=0.5),
                      FadeIn(side[3]), FadeIn(side[4]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(side[5]), FadeIn(side[6]))
        self.clear_scene()
