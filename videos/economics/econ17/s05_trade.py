from __future__ import annotations

from videos.economics.econ17.common import *  # noqa: F403


class Trade(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Myerson and Satterthwaite: \ no perfect bargain", r"A buyer and a seller each know only their "
             r"own value. \ Can any rule get every good trade done?", "Chapter four. Myerson and Satterthwaite: no "
             "perfect bargain.", lit={1983: r"Myerson and Satterthwaite; \ Chatterjee and Samuelson"},
             scale=("person",), horizon=("a day",))
        self.square()
        self.subsidy()

    def square(self):
        t = load("trade")
        ax = plane([0, 1], [0, 1], center=LEFT * 2.9 + DOWN * 0.35, x_length=5.0, y_length=5.0,
                   xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 0.25, 0.5, 0.75, 1],
                   xlabel=r"the seller's cost $c$", ylabel=r"the buyer's value $v$", font_size=16,
                   xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}")
        a = ax.ax
        eff = Polygon(a.c2p(0, 0), a.c2p(1, 1), a.c2p(0, 1), stroke_width=0, fill_color=STABLE, fill_opacity=0.25)
        dbl = Polygon(a.c2p(0, 0.25), a.c2p(0.75, 1), a.c2p(0, 1), stroke_width=0, fill_color=HELD, fill_opacity=0.45)
        post = Polygon(a.c2p(0, 0.5), a.c2p(0.5, 0.5), a.c2p(0.5, 1), a.c2p(0, 1), stroke_width=2.5,
                       stroke_color=MONEY, fill_opacity=0)
        diag = DashedLine(a.c2p(0, 0), a.c2p(1, 1), color=GREY_B, stroke_width=2)
        ex, sh = t["exact"], t["share"]
        side = VGroup(
            label(r"values and costs: \ uniform from 0 to 1, \\ each known only to its owner", font_size=20,
                  color=GREY_A),
            label(rf"every trade with $v > c$: \ gains {ex['efficient']:.3f} \ (1/6)", font_size=22, color=STABLE),
            label(rf"a posted price of $\tfrac12$: \ {ex['posted']:.3f} \ ({sh['posted'] * 100:.0f}\%)", font_size=22,
                  color=MONEY),
            label(rf"the double auction: \ trade if $v \ge c + \tfrac14$: \\ {ex['double']:.4f} \ "
                  rf"({sh['double'] * 100:.0f}\%)", font_size=22, color=HELD),
            label(r"no voluntary rule that pays for itself, \\ with truthful reports, \ does better", font_size=22,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Now the simplest market of all: one buyer, one seller, one good. The seller's cost and the buyer's "
            "value are each somewhere between nothing and one, equally likely, and each knows only their own. "
            "<bookmark mark='a'/> Trade is worth doing whenever the value is above the cost: the green triangle. "
            "Done every time, the expected gains are one sixth. <bookmark mark='b'/> A posted price of one half "
            "trades only in the red square, where the cost is below a half and the value above it, and gets three "
            "quarters of the gains. <bookmark mark='c'/> In the double auction, where both name a price and trade "
            "happens at the midpoint if the buyer's is higher, each shades, and in equilibrium they trade only when "
            "the value beats the cost by a quarter: the yellow triangle, eighty-four percent of the gains. "
            "<bookmark mark='d'/> Roger Myerson and Mark Satterthwaite proved in 1983 that no voluntary rule that "
            "pays for itself does better, and none gets every good trade done."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(diag), FadeIn(side[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(eff), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(post), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(dbl), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def subsidy(self):
        t = load("trade")
        rows = VGroup(
            label(r"why: \ run Vickrey's rule on both sides", font_size=26, color=MECH),
            label(r"the buyer pays the seller's cost; \ the seller receives the buyer's value", font_size=24),
            label(r"truth is safe for both, \ and every good trade happens", font_size=24, color=STABLE),
            label(rf"but each trade leaves a gap, \ $v - c$, \ that someone outside must pay: \ "
                  rf"{t['exact']['efficient']:.3f} on average, \ the whole surplus", font_size=24, color=MONEY),
            label(r"by the envelope argument of part sixteen, \ every efficient truthful rule costs as much", font_size=23,
                  color=GREY_A),
            label(r"so bargaining under private information always wastes some trades: \ the market's own friction",
                  font_size=24, color=E.ACCENT),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Myerson and Satterthwaite, JET 29(2) (1983); \ Chatterjee and Samuelson, Oper.\ Res.\ "
                            r"31(5) (1983)", corner=DR, font_size=12)
        with self.voiceover(
            "There is a short way to see why. <bookmark mark='a'/> Run Vickrey's rule on both sides at once. "
            "<bookmark mark='b'/> The buyer pays the seller's cost, and the seller receives the buyer's value. "
            "<bookmark mark='c'/> Each now gains the whole surplus of the trade, so the truth is safe for both, and "
            "every good trade happens. <bookmark mark='d'/> But each trade leaves a gap, the value less the cost, "
            "that someone outside must pay. On average that is one sixth: the entire surplus. "
            "<bookmark mark='e'/> By the envelope argument of part sixteen, any rule that gets every trade done "
            "with truthful reports costs the same. <bookmark mark='f'/> So when values are private, bargaining "
            "always wastes some good trades. It is a friction in the market itself, and no designer can remove it."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
