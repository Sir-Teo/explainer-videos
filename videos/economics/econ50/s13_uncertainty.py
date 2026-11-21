from __future__ import annotations

from videos.economics.econ50.common import *  # noqa: F403

NAMES = {"elasticity": r"participation elasticity \\ 0 to 0.5", "income_effect": r"income effect \\ 0 to 0.5",
         "take_up": r"take-up \\ 85\% to 100\%"}


def tornado_bars(ax, rows, x_lo, scale, col, fmt):
    g = VGroup()
    rows = sorted(rows, key=lambda r: -abs(r["at_high"] - r["at_low"]))
    for i, r in enumerate(rows):
        y = len(rows) - 1 - i + 0.5
        lo, hi = sorted((r["at_low"] * scale, r["at_high"] * scale))
        p0, p1 = ax.ax.c2p(lo, y - 0.28), ax.ax.c2p(max(hi, lo + 1e-9), y + 0.28)
        w = max(p1[0] - p0[0], 0.04)
        b = Rectangle(width=w, height=p1[1] - p0[1], stroke_width=0, fill_color=col, fill_opacity=0.8)
        b.move_to([p0[0] + w / 2, (p0[1] + p1[1]) / 2, 0])
        nm = label(NAMES[r["dial"]], font_size=15, color=GREY_A).next_to(ax.ax.c2p(x_lo, y), LEFT, buff=0.2)
        vl = label(fmt(r["at_low"] * scale), font_size=14, color=WHITE)
        vh = label(fmt(r["at_high"] * scale), font_size=14, color=WHITE)
        left_v, right_v = (vl, vh) if r["at_low"] * scale <= r["at_high"] * scale else (vh, vl)
        left_v.next_to(b, LEFT, buff=0.08)
        right_v.next_to(b, RIGHT, buff=0.08)
        g.add(VGroup(b, nm, left_v, right_v))
    return g


class Uncertainty(VoiceoverScene):
    def construct(self):
        card(self, 11, r"The uncertainty, \ stated", r"What would change the advice?",
             "Chapter eleven. The uncertainty, stated.", lit={2021: r"Corinth et al."}, scale=("nation",),
             horizon=("a year", "a generation"))
        self.poverty()
        self.cost()
        self.switches()

    def poverty(self):
        T = load("tornado")
        ax = plane([8, 16], [0, 3], center=RIGHT * 0.6 + DOWN * 0.3, x_length=8.0, y_length=4.2,
                   xticks=[8, 10, 12, 14, 16], yticks=[], xlabel=r"children in poverty under the allowance, \ \%",
                   xfmt=lambda v: f"{v:.0f}", font_size=14)
        base = vline(ax, 100 * T["base_poverty"], 0, 3, NEW)
        bl = label(rf"central: \ {100 * T['base_poverty']:.1f}", font_size=15, color=NEW).next_to(
            ax.ax.c2p(100 * T["base_poverty"], 3), UP, buff=0.1)
        old = Line(ax.ax.c2p(100 * T["old_poverty"], 0), ax.ax.c2p(100 * T["old_poverty"], 3), color=OLD,
                   stroke_width=3)
        ol = label(rf"old credit: \ {100 * T['old_poverty']:.1f}", font_size=15, color=OLD).next_to(
            ax.ax.c2p(100 * T["old_poverty"], 3), UP, buff=0.1)
        bars = tornado_bars(ax, T["child_poverty"], 8, 100, WORK, lambda v: f"{v:.1f}")
        foot = label(r"every bar stays left of the old credit: \ the direction is robust; \ the size is not",
                     font_size=20, color=GAIN).to_edge(DOWN, buff=0.45)
        tag = island_tag(corner=DR, font_size=13)
        with self.voiceover(
            "A memo's most useful page says how sure it is, and what would change its advice. The tool is a "
            "tornado chart: move one dial at a time across its range, holding the others at their central values, "
            "and draw how far the answer moves. <bookmark mark='a'/> The central estimate of child poverty under "
            f"the allowance is {100 * T['base_poverty']:.1f} percent; the old credit's is "
            f"{100 * T['old_poverty']:.1f}. <bookmark mark='b'/> The participation elasticity moves the answer "
            "most, by more than three points across its range. <bookmark mark='c'/> An income effect on work, "
            "which the central case leaves out, moves it by about one. <bookmark mark='d'/> Take-up below a "
            "hundred percent, by less than one. <bookmark mark='e'/> And every bar stays to the left of the old "
            "credit. The direction of the answer survives every dial; its size does not."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(base), FadeIn(bl))
            vo.wait_until("a")
            self.play(Create(old), FadeIn(ol))
            for mk, b in zip("bcd", bars):
                vo.wait_until(mk)
                self.play(FadeIn(b[1]), GrowFromCenter(b[0]), FadeIn(b[2:]))
            vo.wait_until("e")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()

    def cost(self):
        T = load("tornado")
        ax = plane([1100, 1600], [0, 3], center=RIGHT * 0.6 + DOWN * 0.3, x_length=8.0, y_length=4.2,
                   xticks=[1100, 1200, 1300, 1400, 1500, 1600], yticks=[],
                   xlabel=r"cost per child, \ \$ a year", xfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"),
                   font_size=14)
        base = vline(ax, T["base_per_child"], 0, 3, NEW)
        bl = label(rf"central: \ \${T['base_per_child']:,.0f}".replace(",", "{,}"), font_size=15,
                   color=NEW).next_to(ax.ax.c2p(T["base_per_child"], 3), UP, buff=0.1)
        bars = tornado_bars(ax, T["per_child"], 1100, 1, BUDGET,
                            lambda v: f"{v:,.0f}".replace(",", "{,}"))
        foot = label(r"the cost is known within a few percent, \ unless take-up falls short", font_size=20,
                     color=WHITE).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The same for the cost. <bookmark mark='a'/> Here take-up dominates: if only eighty-five percent of "
            "families claim, the cost per child falls by about two hundred dollars. <bookmark mark='b'/> The "
            "elasticity and the income effect barely move it, for the reason chapter six gave: the parents who "
            "stop working paid little tax. <bookmark mark='c'/> So the budget line of the memo is the firmest "
            "number in it, and the poverty line the least firm."
        ) as vo:
            self.play(FadeIn(ax), Create(base), FadeIn(bl))
            vo.wait_until("a")
            self.play(FadeIn(bars[0][1]), GrowFromCenter(bars[0][0]), FadeIn(bars[0][2:]))
            vo.wait_until("b")
            self.play(*[FadeIn(b[1]) for b in bars[1:]], *[GrowFromCenter(b[0]) for b in bars[1:]],
                      *[FadeIn(b[2:]) for b in bars[1:]])
            vo.wait_until("c")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()

    def switches(self):
        Fn = load("fan")
        B = load("budget")
        cards = point_cards([
            (r"if parents respond strongly", rf"above an elasticity of about {Fn['deep_cross']:.2f}, \ deep poverty "
                                             r"rises: \ keep a small phase-in for the extra", WORK),
            (r"if little comes back later", rf"with a surtax, \ {B['rows'][1]['mvpf']:.2f} of value per dollar: "
                                            r"\ the case rests on the weight given to poor children", BUDGET),
            (r"if the poorest do not claim", r"fix delivery first: \ automatic payment from records, \ not a "
                                             r"tax return", HOLD),
            (r"if long-run gains are found", r"a large share repaid later makes it pay for itself, \ whatever the "
                                             r"weights", EVIDENCE),
        ], width=12.4, cols=2, font_size=21).move_to(DOWN * 0.2)
        head = label(r"what would change the advice", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "So: what would change the advice? A memo should name the switching points. <bookmark mark='a'/> If "
            "parents respond strongly to a permanent allowance, with an elasticity above about "
            f"{Fn['deep_cross']:.2f}, deep poverty rises, and a design that keeps a small phase-in for the extra "
            "amount becomes attractive. <bookmark mark='b'/> If little of the cost comes back in children's later "
            f"taxes and the money comes from a surtax, the allowance delivers {B['rows'][1]['mvpf']:.2f} dollars "
            "of value per dollar taken, and the case rests entirely on the weight given to poor children. "
            "<bookmark mark='c'/> If the poorest families do not claim, the first task is delivery: paying "
            "automatically from records the government already holds, rather than waiting for a tax return. "
            "<bookmark mark='d'/> And if research finds the long-run gains that the old evidence suggests, the "
            "allowance pays for itself, whatever the weights."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
