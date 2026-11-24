from __future__ import annotations

from videos.industry.industry9.common import *  # noqa: F403

OPS = [COPPER, "#E0A458", "#9C6B9E", "#6F8FB8"]
NAMES = ["Grasberg", "Escondida", "Freeport\nSouth America", "Freeport\nUS mines"]
OWN = ["Freeport, Indonesia (Indonesia's state holds 51%)", "BHP 57.5%, Rio Tinto 30%, Japanese partners, Chile",
       "Cerro Verde (Peru), El Abra (Chile)", "Arizona and New Mexico"]


class Curve(VoiceoverScene):
    def construct(self):
        card(self, 5, "The cost curve", "Which mines make money at today's price, and which do not?",
             "Chapter five. The cost curve.", lit=("dollar", "moat"))
        self.curve()

    def curve(self):
        C = R["curve"]
        pts = C["points"]
        lme = C["lme"]
        today = R["prices"]["copper_last_lb"]
        pa = viz.plot_axes([0, 3000], [-1.0, 7.0], x_length=9.4, y_length=5.2, xticks=[0, 1000, 2000, 3000],
                           yticks=[-1, 0, 1, 2, 3, 4, 5, 6, 7], xfmt=lambda v: f"{v:,.0f} kt",
                           yfmt=lambda v: f"${v:g}", ylabel="net cash cost, dollars a pound", size=14).move_to(
            [-1.6, -0.2, 0])
        xl = tx("copper produced in 2025, thousand tonnes (100% basis)", 14, "#9AA3B2").next_to(pa, DOWN, buff=0.1)
        zero = Line(pa.ax.c2p(0, 0), pa.ax.c2p(3000, 0), stroke_color=GREY_B, stroke_width=1.5)
        blocks = VGroup()
        labels = VGroup()
        for (name, c, x0, x1), col, nm in zip(pts, OPS, NAMES):
            p0, p1 = pa.ax.c2p(x0, 0), pa.ax.c2p(x1, c)
            b = Rectangle(width=p1[0] - p0[0] - 0.03, height=abs(p1[1] - p0[1]), stroke_width=0, fill_color=col,
                          fill_opacity=0.9).move_to([(p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, 0])
            blocks.add(b)
            labels.add(VGroup(tx(nm, 14, col, bold=True), tx(f"${c:.2f}", 15, WHITE)).arrange(DOWN, buff=0.03))
        for lab, b, (name, c, x0, x1) in zip(labels, blocks, pts):
            lab.next_to(b, DOWN if c < 0 else UP, buff=0.1)
        labels[0].next_to(blocks[0], DOWN, buff=0.1)
        pr = ValueTracker(lme)
        pline = always_redraw(lambda: Line(pa.ax.c2p(0, pr.get_value()), pa.ax.c2p(3000, pr.get_value()),
                                           stroke_color=PRICE, stroke_width=3))
        plab = always_redraw(lambda: tx(f"copper ${pr.get_value():.2f}", 16, PRICE, bold=True).next_to(
            pa.ax.c2p(3000, pr.get_value()), RIGHT, buff=0.1))

        def margins():
            g = VGroup()
            p = pr.get_value()
            for (name, c, x0, x1), b in zip(pts, blocks):
                if p > c:
                    a, z = pa.ax.c2p(x0, max(c, 0) if c > 0 else 0), pa.ax.c2p(x1, p)
                    lo_ = pa.ax.c2p(x0, c)[1] if c > 0 else pa.ax.c2p(x0, 0)[1]
                    g.add(Rectangle(width=z[0] - a[0] - 0.03, height=z[1] - lo_, stroke_width=0, fill_color=GREEN_C,
                                    fill_opacity=0.25).move_to([(a[0] + z[0]) / 2, (lo_ + z[1]) / 2, 0]))
                else:
                    a, z = pa.ax.c2p(x0, p), pa.ax.c2p(x1, c)
                    g.add(Rectangle(width=z[0] - a[0] - 0.03, height=z[1] - a[1], stroke_width=0, fill_color=STATE,
                                    fill_opacity=0.55).move_to([(a[0] + z[0]) / 2, (a[1] + z[1]) / 2, 0]))
            return g
        marg = always_redraw(margins)
        side = VGroup()
        for (name, c, x0, x1), col, nm in zip(pts, OPS, NAMES):
            num = draw.number(lambda c=c: abs(pr.get_value() - c), 2, prefix="$", suffix=" a pound", size=17,
                              color=WHITE)
            word = draw.memo_redraw(lambda c=c: pr.get_value() >= c,
                                    lambda up: tx("margin" if up else "loss", 17, GREEN_C if up else STATE, bold=True),
                                    place=lambda m, num=num: m.next_to(num, LEFT, buff=0.1))
            side.add(VGroup(tx(nm.replace("\n", " "), 16, col, bold=True), VGroup(word, num)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.04))
            num.shift(RIGHT * 0.75)
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([5.3, 0.3, 0])
        own = VGroup(*[tx(o, 12, GREY_B) for o in OWN])
        for o, s_ in zip(own, side):
            o.next_to(s_, DOWN, buff=0.03, aligned_edge=LEFT)
        side_g = VGroup(*[VGroup(s_, o) for s_, o in zip(side, own)]).arrange(DOWN, aligned_edge=LEFT, buff=0.22
                                                                             ).move_to([5.25, 0.2, 0])
        head = tx("Four real copper operations, 2025", 24, WHITE, bold=True).to_edge(UP, buff=0.4)
        src = source("BHP, year to June 2025 (Escondida); Freeport-McMoRan, Form 10-K for 2025; LME average 2025; "
                     "copper price: IMF via FRED, September 2026", size=13)
        with self.voiceover(
            "Every mine has its own cost, and if you line them up from cheapest to dearest you get the industry's cost "
            "curve, the idea from Part four. The full curve, covering every mine on Earth, is sold by consultancies. "
            "Here are four real operations, drawn from what their owners publish. <bookmark mark='a'/> The width of "
            "each block is the copper it produced in 2025; the height is its net cash cost per pound. "
            "<bookmark mark='b'/> Escondida, as we saw, at about a dollar twenty. <bookmark mark='c'/> Freeport's mines "
            "in Peru and Chile, at about two forty, and its mines in Arizona and New Mexico, low grade and largely "
            "leached, at about three dollars. <bookmark mark='d'/> And Grasberg, in the mountains of Indonesian Papua, "
            "sits below zero. Its net cost is minus fifty-five cents a pound, because Grasberg is also one of the "
            "world's great gold mines, and Freeport subtracts the gold and silver it sells, at an average of "
            "three thousand four hundred dollars an ounce last year, from the cost of its copper. That is a "
            "by-product credit, and it can be worth more than the main product's costs. <bookmark mark='e'/> Copper "
            f"averaged {say_money(lme)} a pound on the London Metal Exchange in 2025. Every mine here made money, "
            "and the green shows how much per pound. <bookmark mark='f'/> In September 2026 the price reached "
            f"{say_money(today)}, and the margins doubled. <bookmark mark='g'/> But drop the price to two fifty, and the "
            "American mines lose money on every pound, while Grasberg barely notices. The low-cost mine is the one "
            "that survives the bad years, and that, not size, is a miner's moat."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(xl), Create(zero), FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(GrowFromEdge(blocks[1], DOWN), FadeIn(labels[1]))
            vo.wait_until("b")
            self.play(Indicate(labels[1], color=WHITE))
            vo.wait_until("c")
            self.play(GrowFromEdge(blocks[2], DOWN), FadeIn(labels[2]))
            self.play(GrowFromEdge(blocks[3], DOWN), FadeIn(labels[3]))
            vo.wait_until("d")
            self.play(GrowFromEdge(blocks[0], UP), FadeIn(labels[0]))
            vo.wait_until("e")
            self.add(marg)
            self.play(Create(pline), FadeIn(plab), FadeIn(side_g))
            vo.wait_until("f")
            self.play(pr.animate.set_value(today), run_time=3.0)
            vo.wait_until("g")
            self.play(pr.animate.set_value(2.5), run_time=3.5)
            self.wait(1.5)
            self.play(pr.animate.set_value(lme), run_time=2.0)
        for s_ in side:
            s_[1][1].clear_updaters()
            s_[1][0].clear_updaters()
        self.clear_scene()
        self.moving()

    def moving(self):
        E = R["esc"]
        pa = viz.plot_axes([0, 2000], [0, 2.4], x_length=8.0, y_length=4.4, xticks=[0, 500, 1000, 1500, 2000],
                           yticks=[0.5, 1.0, 1.5, 2.0], xfmt=lambda v: f"{v:,.0f} kt", yfmt=lambda v: f"${v:.2f}",
                           xlabel="copper a year, thousand tonnes", ylabel="unit cost, dollars a pound", size=14
                           ).move_to([-1.2, -0.4, 0])
        steps = [("year to June 2025", E["output"], E["unit_cost"]),
                 ("2026, guidance (mid-point)", get("esc.output.2026"), get("esc.cost.2026")),
                 ("2027-2031, outlook (mid-point)", get("esc.medium"), get("esc.cost.medium"))]

        def block(q, c, op=0.9):
            p0, p1 = pa.ax.c2p(0, 0), pa.ax.c2p(q, c)
            return Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=OPS[1],
                             fill_opacity=op).move_to([(p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, 0])
        b = block(steps[0][1], steps[0][2])
        ghost = block(steps[0][1], steps[0][2], 0.0).set_stroke(OPS[1], 2, opacity=0.7)
        lab = VGroup(*[VGroup(tx(n, 17, OPS[1] if k == 0 else WHITE, bold=True),
                              tx(f"{q:,.0f} kt at ${c:.2f}", 16, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
                       for k, (n, q, c) in enumerate(steps)]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(
            [5.0, 0.4, 0])
        head = tx("Escondida's block on the curve, moving", 24, WHITE, bold=True).to_edge(UP, buff=0.4)
        note = VGroup(tx("narrower and taller:", 18, STATE, bold=True), tx("less copper, at a higher cost", 18, STATE)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.05).next_to(lab, DOWN, buff=0.5, aligned_edge=LEFT)
        src = source("BHP, results for the year to June 2025: actuals, guidance and medium-term outlook", size=13)
        with self.voiceover(
            "And the curve does not stand still. Each mine's block changes shape as its grade falls. "
            "<bookmark mark='a'/> Here is Escondida last year: wide and low. <bookmark mark='b'/> This year, on BHP's "
            "guidance, a little narrower and taller. <bookmark mark='c'/> And on its outlook for the five years from "
            "2027, narrower and taller again. A whole industry of mines is doing this at once, so the curve creeps "
            "upward, year after year. Unless new, richer deposits are found and built to replace them, the cost of "
            "the marginal pound of copper rises, and with it, over the long run, the price."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(GrowFromEdge(b, DOWN), FadeIn(lab[0]))
            self.add(ghost)
            vo.wait_until("b")
            self.play(Transform(b, block(steps[1][1], steps[1][2])), FadeIn(lab[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Transform(b, block(steps[2][1], steps[2][2])), FadeIn(lab[2]), run_time=1.5)
            self.play(FadeIn(note, shift=UP * 0.1))
        self.clear_scene()
