from __future__ import annotations

from videos.economics.econ50.common import *  # noqa: F403


class Value(VoiceoverScene):
    def construct(self):
        card(self, 9, r"The cost and the value of public funds", r"What does a dollar of the allowance buy?",
             "Chapter nine. The cost, and the value of public funds.", lit={2020: r"Hendren and Sprung-Keyser"},
             scale=("nation",), horizon=("a year", "a generation"))
        self.ledger()
        self.table()
        self.weights()

    def ledger(self):
        B = load("budget")
        wtp, cost = B["wtp"] / 1e6, B["cost"] / 1e6
        ax = plane([0, 4], [0, 120], center=LEFT * 2.0 + DOWN * 0.4, x_length=7.6, y_length=4.6, xticks=[],
                   yticks=[0, 30, 60, 90, 120], ylabel=r"millions of dollars a year", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        items = [(r"what families \\ would pay", wtp, NEW), (r"the cost \\ to the budget", cost, BUDGET),
                 (r"net of a quarter \\ repaid later", cost - 0.25 * wtp, EVIDENCE),
                 (r"net of a half \\ repaid later", cost - 0.5 * wtp, EVIDENCE)]
        bars = VGroup()
        for i, (n, v, c) in enumerate(items):
            p0, p1 = ax.ax.c2p(i + 0.2, 0), ax.ax.c2p(i + 0.8, v)
            r = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=c,
                          fill_opacity=0.85).move_to((p0 + p1) / 2)
            bars.add(VGroup(r, label(f"{v:.1f}", font_size=16, color=WHITE).next_to(r, UP, buff=0.06),
                            label(n, font_size=14, color=c).next_to(ax.ax.c2p(i + 0.5, 0), DOWN, buff=0.15)))
        f = MathTex(r"\text{MVPF} = \frac{\text{what recipients would pay}}{\text{net cost to the government}}",
                    font_size=32, color=THEORY).to_edge(UP, buff=0.45)
        side = VGroup(
            label(rf"no later return: \\ {wtp:.1f} / {cost:.1f} = {B['rows'][0]['mvpf']:.2f}", font_size=18,
                  color=WHITE),
            label(rf"a quarter repaid: \ {B['rows'][3]['mvpf']:.2f}", font_size=18, color=EVIDENCE),
            label(rf"a half repaid: \ {B['rows'][6]['mvpf']:.2f}", font_size=18, color=EVIDENCE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=13)
        with self.voiceover(
            "Now the value of a dollar, with Part forty-two's yardstick: the marginal value of public funds, what "
            "recipients would pay for the policy divided by its net cost to the government. <bookmark mark='a'/> "
            "What would families pay? By the envelope theorem, as in Part forty-two, the payment itself: the parents "
            "who "
            "stop working were close to indifferent, so their change of plans adds nothing to the value. That is "
            f"{wtp:.1f} million dollars a year. <bookmark mark='b'/> The cost to the budget is {cost:.1f} million. "
            f"<bookmark mark='c'/> Without any return later, the ratio is {B['rows'][0]['mvpf']:.2f}: a dollar spent "
            "delivers a dollar of value, no more and no less. <bookmark mark='d'/> But if the children grow up "
            "healthier and better educated and pay more tax as adults, part of the cost comes back. If a quarter "
            f"of it returns, in today's money, the ratio is {B['rows'][3]['mvpf']:.2f}; <bookmark mark='e'/> if "
            f"half, {B['rows'][6]['mvpf']:.2f}. The Island cannot measure that return; it is planted as a range, "
            "because the evidence of chapter seven is too old and too indirect to pin it down."
        ) as vo:
            self.play(FadeIn(f), FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1:]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1:]))
            vo.wait_until("c")
            self.play(FadeIn(side[0]))
            vo.wait_until("d")
            self.play(GrowFromEdge(bars[2][0], DOWN), FadeIn(bars[2][1:]), FadeIn(side[1]))
            vo.wait_until("e")
            self.play(GrowFromEdge(bars[3][0], DOWN), FadeIn(bars[3][1:]), FadeIn(side[2]))
        self.clear_scene()

    def table(self):
        B = load("budget")
        crs = sorted({r["child_return"] for r in B["rows"]})
        mcs = B["mcpfs"]
        cell_w, cell_h = 2.4, 1.05
        x0, y0 = -1.2, 1.0
        cells = VGroup()
        for i, cr in enumerate(crs):
            for j, mc in enumerate(mcs):
                v = next(r["mvpf"] for r in B["rows"] if r["child_return"] == cr and abs(r["mcpf"] - mc) < 1e-9)
                col = GAIN if v >= 1.0 - 1e-6 else (NEW if v >= 0.75 else LOSS)
                box = Rectangle(width=cell_w, height=cell_h, stroke_color=GREY_D, stroke_width=1.2, fill_color=col,
                                fill_opacity=0.18 + 0.25 * min(v / 2, 1))
                box.move_to([x0 + j * cell_w, y0 - i * cell_h, 0])
                cells.add(VGroup(box, label(f"{v:.2f}", font_size=26, color=WHITE).move_to(box)))
        col_h = VGroup(*[label(t, font_size=17, color=BUDGET).move_to([x0 + j * cell_w, y0 + 0.95, 0])
                         for j, t in enumerate([r"no extra cost \\ (1.00)", rf"surtax, \ ETI 0.25 \\ ({mcs[1]:.2f})",
                                                rf"surtax, \ ETI 0.4 \\ ({mcs[2]:.2f})"])])
        row_h = VGroup(*[label(t, font_size=17, color=EVIDENCE).move_to([x0 - 2.6, y0 - i * cell_h, 0])
                         for i, t in enumerate([r"nothing repaid", r"a quarter repaid", r"half repaid"])])
        top = label(r"value delivered per dollar the payers give up", font_size=24, color=E.ACCENT).to_edge(
            UP, buff=0.5)
        ch = label(r"how it is paid for \ (the cost of a dollar of revenue)", font_size=16, color=GREY_A).next_to(
            col_h, UP, buff=0.2)
        rh = label(r"children's \\ later taxes", font_size=16, color=GREY_A).next_to(row_h, UP, buff=0.25)
        foot = label(r"above 1: \ more value than it costs; \ below 1: \ worth it only if a dollar to these families "
                     r"counts for more", font_size=18, color=WHITE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Now combine the two unknowns: how much the children later repay, and how the money is raised. "
            "<bookmark mark='a'/> Down the side, the share of the cost that children's later taxes repay: "
            "nothing, a quarter, half. <bookmark mark='b'/> Across the top, the cost of raising a dollar: one "
            f"dollar if it costs nothing extra, {mcs[1]:.2f} or {mcs[2]:.2f} if it comes from a top surtax, from "
            "chapter six. <bookmark mark='c'/> Each cell is the value delivered to families per dollar that the "
            "people paying for it give up. <bookmark mark='d'/> With nothing repaid and a surtax, the allowance "
            "delivers seventy-five or sixty cents of value per dollar taken. <bookmark mark='e'/> With half "
            "repaid, it delivers more than it takes, whichever way it is financed. <bookmark mark='f'/> So the "
            "answer turns on a number the evidence cannot yet supply, and on a judgment the evidence never will."
        ) as vo:
            self.play(FadeIn(top))
            vo.wait_until("a")
            self.play(FadeIn(row_h), FadeIn(rh))
            vo.wait_until("b")
            self.play(FadeIn(col_h), FadeIn(ch))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.12), run_time=2.0)
            vo.wait_until("d")
            self.play(Indicate(VGroup(cells[1], cells[2]), color=WHITE, scale_factor=1.05))
            vo.wait_until("e")
            self.play(Indicate(VGroup(*cells[6:9]), color=WHITE, scale_factor=1.05))
            vo.wait_until("f")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()

    def weights(self):
        B = load("budget")
        v = next(r["mvpf"] for r in B["rows"] if r["child_return"] == 0.0 and abs(r["mcpf"] - B["mcpfs"][1]) < 1e-9)
        cards = point_cards([
            (r"the judgment", rf"is a dollar to a family below the line worth at least {1 / v:.2f} dollars to a "
                              r"top earner?", NEW),
            (r"Hendren's comparison", r"the allowance's value per dollar against the surtax's: \ with equal "
                                      r"weights, \ spend if the first is larger", BUDGET),
            (r"what the economist adds", r"the numbers on each side of the judgment, \ and how sure they are", WORK),
            (r"what the economist cannot add", r"the weights themselves: \ that is the minister's, \ and the "
                                               r"voters'", HOLD),
        ], width=12.4, cols=2, font_size=21).move_to(DOWN * 0.2)
        head = label(r"where the numbers stop", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Where do the numbers stop? <bookmark mark='a'/> Take the cell with nothing repaid and a surtax at an "
            f"elasticity of a quarter: {v:.2f} dollars of value per dollar taken. The allowance is worth doing if a "
            f"dollar to a family below the line is worth at least {1 / v:.2f} dollars to a top earner. <bookmark "
            "mark='b'/> That is Nathaniel Hendren's way of comparing policies: the value per dollar of the "
            "spending against the value per dollar of the tax that pays for it. <bookmark mark='c'/> The "
            "economist can supply the numbers on both sides, and how uncertain they are. <bookmark mark='d'/> The "
            "weight a society puts on a poor child's dollar is not an economic finding. It belongs to the minister, "
            "and to the voters, and the memo should say so in as many words."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
