from __future__ import annotations

from videos.economics.econ25.common import *  # noqa: F403

LETTERS = "ABCD"
CHIP = ("#F2C14E", "#7EC8F5", "#7BD88F", "#F2788F")
GOOD_C = (SALT, COCO, FISH)


def good(name: str, color, r: float = 0.32) -> VGroup:
    c = Circle(radius=r, fill_color=color, fill_opacity=0.85, stroke_color=WHITE, stroke_width=1.5)
    return VGroup(c, label(name, font_size=16, color=BLACK).move_to(c))


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Play it: \ which good becomes money?", r"Three goods, \ three kinds of islander. \ Which "
             r"good will be passed from hand to hand?", "Chapter two. Play it: which good becomes money?",
             lit={1989: r"Kiyotaki and Wright"}, scale=("market",), horizon=("a month",))
        self.setup_()
        self.reveal()

    def traders(self):
        k = load("kw")
        cols = VGroup()
        for i, (name, eats, makes) in enumerate(zip(k["names"], (0, 1, 2), (1, 2, 0))):
            head = label(name, font_size=26, color=WHITE)
            e = VGroup(label(r"eats", font_size=18, color=GREY_B), good(k["goods"][eats], GOOD_C[eats])).arrange(
                RIGHT, buff=0.15)
            m = VGroup(label(r"makes", font_size=18, color=GREY_B), good(k["goods"][makes], GOOD_C[makes])).arrange(
                RIGHT, buff=0.15)
            cols.add(VGroup(head, e, m).arrange(DOWN, buff=0.18))
        cols.arrange(RIGHT, buff=1.3)
        return cols

    def setup_(self):
        k = load("kw")
        stage = game_stage(12.6, 6.6, center=DOWN * 0.05)
        cols = self.traders().move_to(stage.box.get_top() + DOWN * 1.35)
        costs = VGroup(*[label(rf"{g}: \ costs {c:g} a month to keep", font_size=19, color=col)
                         for g, c, col in zip(k["goods"], k["c"], GOOD_C)]).arrange(RIGHT, buff=0.5)
        costs.next_to(cols, DOWN, buff=0.35)
        rule = label(r"everyone meets one random islander a month; \ two swap only if both want to", font_size=20,
                     color=GREY_A).next_to(costs, DOWN, buff=0.25)
        q = label(r"which good will islanders accept only to pass it on?", font_size=25,
                  color=E.ACCENT).next_to(rule, DOWN, buff=0.3)
        opts = (r"salt", r"coconuts", r"fish", r"salt and fish")
        chips = VGroup(*[VGroup(RoundedRectangle(width=2.6, height=0.9, corner_radius=0.12, stroke_color=c,
                                                 stroke_width=3, fill_color=c, fill_opacity=0.12),
                                label(rf"{LETTERS[i]}: \ {o}", font_size=24, color=c))
                         for i, (c, o) in enumerate(zip(CHIP, opts))]).arrange(RIGHT, buff=0.3)
        for ch in chips:
            ch[1].move_to(ch[0])
        chips.next_to(q, DOWN, buff=0.3)
        ring = countdown().scale(0.8).next_to(chips, DOWN, buff=0.2)
        with self.voiceover(
            "Your turn. The Island has three goods: salt, coconuts and fish, and three kinds of islander. "
            "<bookmark mark='a'/> Ana eats salt and can make coconuts. Bo eats coconuts and can catch fish. Dara eats "
            "fish and can make salt. Nobody eats what they make, so nobody can trade directly with the one person "
            "who wants their good and has what they want. <bookmark mark='b'/> Goods are costly to keep: salt "
            "hardly at all, coconuts a little, fish a lot, because fish spoils. <bookmark mark='c'/> Each month "
            "everyone meets one islander at random, and two swap only if both want to. <bookmark mark='d'/> Which "
            "good will islanders take, not to eat, but only to pass on? A, salt; B, coconuts; C, fish; or D, both "
            "salt and fish. Pause, and choose."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(cols[0][0]), FadeIn(cols[1][0]), FadeIn(cols[2][0]))
            vo.wait_until("a")
            self.play(*[FadeIn(c[1:]) for c in cols])
            vo.wait_until("b")
            self.play(FadeIn(costs))
            vo.wait_until("c")
            self.play(FadeIn(rule))
            vo.wait_until("d")
            self.play(FadeIn(q), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.3),
                      FadeIn(ring), run_time=2.5)
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.clear_scene()

    def reveal(self):
        k = load("kw")
        f = k["fund"]
        ax = plane([-0.6, 2.6], [0, 1.0], center=LEFT * 3.3 + DOWN * 0.4, x_length=5.2, y_length=4.2, xticks=[],
                   yticks=[0, 0.5, 1.0], ylabel=r"share of trades where it is passed on", yfmt=lambda v: f"{v:g}",
                   font_size=15)
        bars, names = VGroup(), VGroup()
        for i, (g, col) in enumerate(zip(k["goods"], GOOD_C)):
            lo, hi = ax.ax.c2p(i, 0), ax.ax.c2p(i, max(f["medium"][i], 0.004))
            bars.add(Rectangle(width=0.8, height=hi[1] - lo[1], fill_color=col, fill_opacity=0.85,
                               stroke_width=0).move_to((lo + hi) / 2))
            names.add(label(g, font_size=18, color=col).next_to(lo, DOWN, buff=0.15))
        hold = VGroup()
        for i, name in enumerate(k["names"]):
            parts = [rf"{100 * f['dist'][i][g]:.0f}\% {k['goods'][g]}" for g in range(3) if f["dist"][i][g] > 0.005]
            hold.add(label(rf"{name} holds: \ " + r", \ ".join(parts), font_size=20, color=WHITE))
        hold.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        why = label(r"Bo takes salt for fish: \ salt keeps, \\ and Dara, \ who has salt, \ wants fish", font_size=20,
                    color=SALT)
        ans = label(r"A: \ salt is the Island's money", font_size=28, color=E.ACCENT)
        block = VGroup(hold, why, ans).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        if block.width > 6.2:
            block.width = 6.2
        block.next_to(ax, RIGHT, buff=0.9).shift(UP * 0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            f"Agora runs the Island: {k['n']} islanders of each kind, {k['periods']} months of random meetings, "
            "each swapping only when it makes them better off, given that fish spoils. "
            "<bookmark mark='a'/> Here is what gets passed on. Salt, in every such trade. <bookmark mark='b'/> Look "
            "at who holds what. Ana always holds coconuts, waiting to meet a salt-holder. Dara holds salt, which she "
            "made. And Bo holds salt half the time and fish the other half. <bookmark mark='c'/> Bo accepts salt in "
            "exchange for fish, though he cannot eat salt, because salt costs almost nothing to keep, and Dara, who "
            "wants fish, has salt. <bookmark mark='d'/> If you chose A, you were right: salt became the Island's "
            "money. Nobody decreed it. It emerged from people choosing what to accept."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(names), *[GrowFromEdge(b_, DOWN) for b_ in bars], run_time=1.5)
            vo.wait_until("a")
            self.play(Indicate(bars[0], color=WHITE))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(h) for h in hold], lag_ratio=0.5), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(why))
            vo.wait_until("d")
            self.play(FadeIn(ans, shift=UP * 0.1))
        self.clear_scene()
