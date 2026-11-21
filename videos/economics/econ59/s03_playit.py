from __future__ import annotations

from videos.economics.econ59.common import *  # noqa: F403


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Play it: \ one market or two?", r"Could one owner of both raise both prices by 5\%, \ and "
             r"gain?", "Chapter two. Play it: one market or two?", lit={1982: r"the SSNIP"},
             scale=("market",), horizon=("a year",))
        self.stage()
        self.reveal()

    def stage(self):
        P = load("playit")
        pairs = P["pairs"]
        cols = (BIRCH, SHOPS, CARTEL)
        cards = VGroup()
        for q, col in zip(pairs, cols):
            body = VGroup(
                wrapped_label(tex_safe(q["what"]), 3.5, 18, GREY_A),
                label(rf"diversion: \ {100 * q['D']:.0f}\% of {tex_safe(q['a'])}'s lost sales go to "
                      rf"{tex_safe(q['b'])}".replace("the corner shops", r"the shops"), font_size=18, color=WHITE),
                label(rf"{tex_safe(q['b'])}'s margin: \ {100 * q['M']:.0f}\% of its price"
                      .replace("the corner shops", r"the shops'"), font_size=18, color=WHITE),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            for m in body[1:]:
                if m.width > 3.6:
                    m.width = 3.6
            t = label(tex_safe(q["name"]), font_size=22, color=col)
            inner = VGroup(t, body).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            box = SurroundingRectangle(inner, buff=0.25, color=col, corner_radius=0.12, stroke_width=2)
            cards.add(VGroup(box, inner))
        cards.arrange(RIGHT, buff=0.35).move_to(DOWN * 0.2)
        if cards.width > 13.2:
            cards.width = 13.2
        head = label(r"one owner of both raises both prices by 5\%: \ does it gain?", font_size=26,
                     color=E.ACCENT).to_edge(UP, buff=0.45)
        ask = label(r"which pairs are one market? \ \ (any number of them)", font_size=24, color=WHITE).next_to(
            cards, DOWN, buff=0.6)
        tag = island_tag(r"the Island: \ diversion and margins from agora.merger; \ the kilns are given",
                         corner=DL, font_size=12)
        defs = VGroup(
            label(r"diversion ratio $D$: \ the share of one product's lost sales that go to the other", font_size=21,
                  color=GOV),
            label(r"margin $M$: \ (price $-$ the cost of one more unit) $\div$ price", font_size=21, color=SAVE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "Your turn. A market, for the law, is a set of products that a single owner could profitably make "
            "dearer. The test imagines a hypothetical monopolist of both products in a pair, who raises both prices "
            "by five percent. If that pays, the pair is a market; if customers would escape to something else, it "
            "is not. You are given two numbers for each pair. <bookmark mark='d1'/> The diversion ratio: when one "
            "product's price rises, the share of the sales it loses that go to the other. <bookmark mark='d2'/> And "
            "the other's margin: how much of its price is profit on one more sale. <bookmark mark='a'/> Pair one: Alder and Birch, two superstores. "
            f"{100 * pairs[0]['D']:.0f} percent of the sales Alder loses go to Birch, and Birch's margin is "
            f"{100 * pairs[0]['M']:.0f} percent. <bookmark mark='b'/> Pair two: Alder and the corner shops. Only "
            f"{100 * pairs[1]['D']:.0f} percent of Alder's lost sales go to the shops, whose margin is "
            f"{100 * pairs[1]['M']:.0f} percent. <bookmark mark='c'/> Pair three: two cement kilns, whose cement "
            "is dear to haul far. Only twenty percent of one kiln's lost sales go to the other, but the margin on a "
            "tonne is sixty percent. <bookmark mark='d'/> Which pairs are one market?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("d1")
            self.play(FadeIn(defs[0], shift=DOWN * 0.1))
            vo.wait_until("d2")
            self.play(FadeIn(defs[1], shift=DOWN * 0.1))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(ask))
        ring = countdown().scale(0.6).next_to(ask, DOWN, buff=0.35)
        self.play(FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=7.0, rate_func=linear)
        self.play(FadeOut(ring))
        self.wait(0.5)
        self.clear_scene()

    def reveal(self):
        P = load("playit")
        pairs = P["pairs"]
        ax = plane([-0.5, 2.5], [0, 0.6], center=LEFT * 2.6 + DOWN * 0.4, x_length=6.8, y_length=4.6, xticks=[],
                   yticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], ylabel=r"diversion ratio", yfmt=lambda v: f"{v:.1f}",
                   font_size=15)
        cols = (BIRCH, SHOPS, CARTEL)
        bars, crit, names, marks = VGroup(), VGroup(), VGroup(), VGroup()
        for k, (q, col) in enumerate(zip(pairs, cols)):
            p0, p1 = ax.ax.c2p(k - 0.28, 0), ax.ax.c2p(k + 0.28, q["D"])
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=col, fill_opacity=0.8,
                               stroke_width=0).move_to((p0 + p1) / 2))
            crit.add(Line(ax.ax.c2p(k - 0.42, q["critical"]), ax.ax.c2p(k + 0.42, q["critical"]), color=WHITE,
                          stroke_width=4))
            names.add(label(tex_safe(q["name"]).replace(" and ", r" \\ and "), font_size=15, color=col).next_to(
                ax.ax.c2p(k, 0), DOWN, buff=0.15))
            ok = q["one_market"]
            marks.add(label(r"one market" if ok else r"not a market", font_size=17,
                            color=GAIN if ok else COST).next_to(bars[-1] if q["D"] > q["critical"] else crit[-1],
                                                                 UP, buff=0.1))
        key = label(r"white bar: \ the critical diversion, \ $X / (X + M)$", font_size=16, color=WHITE).next_to(
            ax.ax.c2p(-0.4, 0.6), RIGHT, buff=0.0)
        der = VGroup(
            label(r"the monopolist of both raises both prices by $X$", font_size=19, color=GREY_A),
            MathTex(r"\text{each loses a share } \tfrac{X}{M} \text{ of its sales}, \ "
                    r"\text{but keeps a fraction } D", font_size=26, color=WHITE),
            MathTex(r"\text{it pays when } \ \tfrac{X}{M}(1 - D) < \tfrac{X}{X + M} \iff D > \tfrac{X}{X + M}",
                    font_size=28, color=E.ACCENT),
            label(r"(linear demand, \ symmetric firms, \ prices set by each to maximize profit)", font_size=16,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35).shift(UP * 0.9)
        if der.width > 6.2:
            der.width = 6.2
            der.to_edge(RIGHT, buff=0.35)
        lesson = VGroup(
            label(r"high margins make a market narrow, \ not broad:", font_size=21, color=CARTEL),
            label(r"every sale kept by the partner is worth a lot", font_size=21, color=CARTEL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(der, DOWN, buff=0.5).align_to(der, LEFT)
        with self.voiceover(
            "Here is the arithmetic. <bookmark mark='a'/> When each firm already sets its own price to maximize "
            "profit, its margin tells you how fast its sales fall: a five percent rise loses about five percent "
            "divided by the margin. The monopolist of both keeps the fraction of those lost sales that go to the "
            "partner. Work through the profit, and the rise pays when the diversion ratio exceeds a critical value, "
            f"X over X plus M, where X is the five percent and M the margin. <bookmark mark='b'/> Alder and Birch: "
            f"the critical diversion is {100 * pairs[0]['critical']:.0f} percent, and the diversion is "
            f"{100 * pairs[0]['D']:.0f}. One market. <bookmark mark='c'/> Alder and the corner shops: "
            f"{100 * pairs[1]['D']:.0f} percent against a critical {100 * pairs[1]['critical']:.0f}. Not a market: "
            "customers who leave Alder mostly go to another superstore, not to the shops. <bookmark mark='d'/> The "
            f"kilns: twenty percent against a critical {100 * pairs[2]['critical']:.0f}. One market, though only a "
            "fifth of the lost sales are kept. <bookmark mark='e'/> That surprises people. A high margin means each "
            "kept sale is worth a great deal, so even modest diversion makes the rise pay. So, pairs one and three. "
            "The superstores' case turned on the first kind of number; the next chapter turns on the third."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(names), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(der[0]), FadeIn(der[1]))
            self.play(FadeIn(der[2]), FadeIn(der[3]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowFromEdge(bars[k], DOWN), Create(crit[k]))
                self.play(FadeIn(marks[k], shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(lesson))
        self.clear_scene()
