from __future__ import annotations

from explainer.industry.register import get
from videos.industry.industry8.common import *  # noqa: F403


class Price(VoiceoverScene):
    def construct(self):
        card(self, 8, "One price, many barrels", "Who sets 'the' price of oil, and how did it go below zero?",
             "Chapter eight. One price, many barrels.", lit=("dollar", "change"))
        self.benchmarks()
        self.futures()

    def benchmarks(self):
        S = R["shock"]
        world = VGroup(
            VGroup(Circle(radius=0.28, stroke_width=0, fill_color=WTI, fill_opacity=1), tx("WTI", 22, WTI, bold=True),
                   tx("light crude delivered at Cushing, Oklahoma", 15, GREY_A)).arrange(DOWN, buff=0.08).move_to([-4.6, 1.2, 0]),
            VGroup(Circle(radius=0.28, stroke_width=0, fill_color=BRENT, fill_opacity=1), tx("Brent", 22, BRENT, bold=True),
                   tx("North Sea crudes, loaded on tankers", 15, GREY_A)).arrange(DOWN, buff=0.08).move_to([0, 1.2, 0]),
            VGroup(Circle(radius=0.28, stroke_width=0, fill_color=OPEC, fill_opacity=1), tx("Dubai and Oman", 22, OPEC, bold=True),
                   tx("Gulf crudes, mostly sold to Asia", 15, GREY_A)).arrange(DOWN, buff=0.08).move_to([4.6, 1.2, 0]))
        ms, br, wt = S["months"], S["brent"], S["wti"]
        pa = viz.plot_axes([2025, 2026.9], [40, 140], x_length=8.6, y_length=2.6, xticks=[2025, 2026],
                           yticks=[60, 100, 140], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}", size=13)
        pa.move_to([0.2, -1.9, 0])
        lb = VMobject(stroke_color=BRENT, stroke_width=4).set_points_as_corners(
            [pa.ax.c2p(mx(m), v) for m, v in zip(ms, br) if v])
        lw = VMobject(stroke_color=WTI, stroke_width=4).set_points_as_corners(
            [pa.ax.c2p(mx(m), v) for m, v in zip(ms, wt) if v])
        gap = tx(f"31 March 2026: Brent ${S['spread']:.0f} above WTI", 17, WHITE, bold=True).next_to(
            pa, UP, buff=0.08).align_to(pa, LEFT)
        src = source("EIA spot prices (Brent, WTI), monthly; EIA, Today in Energy, 7 April 2026", size=13)
        with self.voiceover(
            "There is no single price of oil. There are prices of particular crudes, at particular places, and a few "
            "of them are used as yardsticks for all the rest. <bookmark mark='a'/> West Texas Intermediate, a light "
            "American crude, delivered at Cushing. <bookmark mark='b'/> Brent, a blend of North Sea crudes loaded "
            "onto ships, the yardstick for most of the world's oil. <bookmark mark='c'/> And Dubai and Oman, for the "
            "heavier crudes of the Gulf, sold mostly to Asia. Every other crude is priced as a premium or a discount "
            "to one of these. <bookmark mark='d'/> Usually they move together. But in March 2026, with tankers "
            "unable to leave the Gulf, Brent rose much faster than American crude, which was not stuck behind the "
            f"strait. By the end of the month Brent was {S['spread']:.0f} dollars a barrel above WTI."
        ) as vo:
            bhead = tx("Benchmarks: the yardsticks for every barrel", 24, WHITE, bold=True).to_edge(UP, buff=0.45)
            brls = VGroup(*[draw.barrel(0.5, color=c) for c in (WTI, BRENT, OPEC, STONE, GREY_B, WTI, BRENT)]).arrange(
                RIGHT, buff=0.35).move_to([0, -1.6, 0])
            self.play(FadeIn(src), FadeIn(bhead), LaggedStart(*[FadeIn(b_, shift=UP * 0.2) for b_ in brls],
                                                             lag_ratio=0.15), *[FadeIn(w_[0]) for w_ in world], run_time=2.0)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(world[k][1:], shift=UP * 0.2), Indicate(world[k][0], color=WHITE))
                if k == 2:
                    self.play(FadeOut(brls))
            vo.wait_until("d")
            self.play(FadeIn(pa), Create(lw), Create(lb), run_time=2.5)
            self.play(FadeIn(gap))
        self.clear_scene()

    def futures(self):
        N = R["negative"]
        # a futures curve in normal times and in April 2020 (contango): illustrative shapes
        pa = viz.plot_axes([0, 12], [0, 60], x_length=5.4, y_length=3.6, xticks=[1, 3, 6, 9, 12],
                           yticks=[20, 40, 60], xfmt=lambda v: f"+{int(v)}m", yfmt=lambda v: f"${v:g}", size=13)
        pa.move_to([-3.4, -0.4, 0])
        normal = VMobject(stroke_color=GREY_B, stroke_width=3).set_points_smoothly(
            [pa.ax.c2p(m, 50 - 0.4 * m) for m in range(1, 13)])
        cont = VMobject(stroke_color=STATE, stroke_width=4).set_points_smoothly(
            [pa.ax.c2p(m, 20 + 18 * (1 - np.exp(-m / 3))) for m in range(1, 13)])
        nl = tx("usually: oil for later costs about the same", 15, GREY_B).next_to(pa, UP, buff=0.1)
        cl = tx("April 2020: oil for later far dearer than oil now", 15, STATE).next_to(nl, UP, buff=0.05)
        head = tx("the futures curve: today's price for oil delivered in each month ahead", 16, GREY_A).next_to(pa, DOWN, buff=0.15)
        tankg = VGroup(*[draw.tank(0.7, 0.76) for _ in range(6)]).arrange_in_grid(rows=2, cols=3, buff=(0.15, 0.25))
        tankg.move_to([3.2, 1.2, 0])
        steps = VGroup(
            tx("1. Most futures are closed out before they expire;", 16, WHITE),
            tx("   about 1% end in a delivery of real oil", 16, GREY_A),
            tx(f"2. Cushing was {N['cushing']:.0f}% full, and some empty space was leased", 16, WHITE),
            tx(f"3. US refineries were running {N['runs']:.1f}m barrels a day, a quarter below normal", 16, WHITE),
            tx(f"4. Last day of trading: sellers paid buyers to take it, {N['settle']:.2f}", 16, STATE),
            tx(f"   while Brent for June closed at ${get('eia.brent.2020'):.2f} the next day", 16, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).move_to([3.0, -1.4, 0])
        src = source("EIA, Today in Energy, 27 April 2020; CFTC, Interim Staff Report (2020); illustrative curve shapes",
                     size=13)
        with self.voiceover(
            "Most oil is traded for delivery later, in futures contracts, and the price for each month ahead forms a "
            "curve. <bookmark mark='a'/> Usually oil for delivery in a year costs about the same as oil now, or a "
            "little less. <bookmark mark='b'/> But when there is far too much oil today, today's oil gets cheap and "
            "tomorrow's stays dear, and anyone with a tank can buy now, store it, and sell it forward at a profit. "
            "Traders call that contango. It lasts until the tanks are full. <bookmark mark='c'/> Which is what happened "
            "in April 2020. Almost every futures contract is closed out before it expires; only about one percent "
            "ends in a real delivery. <bookmark mark='d'/> But the tanks at Cushing were filling, <bookmark mark='e'/> "
            "refineries were running a quarter below normal, <bookmark mark='f'/> and on the last day of trading the "
            "people still holding May contracts could not take delivery. They paid others to take them off their "
            "hands. Brent, priced on oil at sea, never went below zero: on the next day it closed at nineteen dollars."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pa), FadeIn(head))
            vo.wait_until("a")
            self.play(Create(normal), FadeIn(nl))
            vo.wait_until("b")
            self.play(Create(cont), FadeIn(cl))
            vo.wait_until("c")
            self.play(FadeIn(steps[:2]))
            vo.wait_until("d")
            self.play(FadeIn(tankg), FadeIn(steps[2]))
            vo.wait_until("e")
            self.play(FadeIn(steps[3]))
            vo.wait_until("f")
            self.play(FadeIn(steps[4:]))
        self.clear_scene()
