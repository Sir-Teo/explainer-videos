from __future__ import annotations

from videos.industry.industry4.common import *  # noqa: F403

SHORT = {"Salaries and benefits": "Salaries", "Refinery and other businesses": "Refinery, other businesses",
         "Landing fees and rents": "Landing fees, rents", "Regional partners": "Regional partners",
         "Commissions and selling": "Selling", "Passenger service": "Passenger service"}
H_COL = {0: VAR, 1: FIXED, 2: "#B58CFF"}
H_NAME = {0: "within days", 1: "within a year", 2: "only over the planes' lives"}


class Four(VoiceoverScene):
    def construct(self):
        card(self, 2, "Four words for cost", "When you stop, which costs stop with you?",
             "Chapter two. Four words for cost.", lit=("dollar", "make"))
        self.cancel()
        self.grid()
        self.sunk()

    # --- Delta's costs, sorted by how soon they go away ---------------------------------------------------------------
    def cancel(self):
        D = R["delta"]
        lines = sorted(D["lines"].items(), key=lambda kv: -kv[1])
        items = [(SHORT.get(k, k), v, "#AEB8CC", f"${v:.1f}bn") for k, v in lines]
        tm = viz.treemap(items, width=8.4, height=5.2, size=19).move_to([-2.2, -0.45, 0])
        head = tx(f"Delta Air Lines' operating costs, 2025: ${D['total']:.1f}bn", 28, bold=True).to_edge(UP, buff=0.3)
        src = source("Delta Air Lines Form 10-K 2025; the sort by horizon is this film's")
        jet = draw.plane(2.6).move_to([4.9, 2.2, 0])
        flight = tx("Atlanta to Boston, tomorrow, 7 am", 18, GREY_B).next_to(jet, DOWN, buff=0.2)
        stamp = tx("CANCELLED", 30, LOSS, bold=True).rotate(0.18).move_to(jet)
        stamp_box = SurroundingRectangle(stamp, color=LOSS, buff=0.08, stroke_width=3)

        share = ValueTracker(0.0)
        bar_bg = RoundedRectangle(corner_radius=0.06, width=3.4, height=0.34, stroke_color=GREY_D, stroke_width=1.5,
                                  fill_opacity=0).move_to([4.9, -0.45, 0])
        bar = always_redraw(lambda: Rectangle(width=max(3.4 * share.get_value() / 100, 0.001), height=0.34,
                                              stroke_width=0, fill_color=PROFIT, fill_opacity=0.9).move_to(
            bar_bg.get_left(), aligned_edge=LEFT))
        bar_t = tx("share of the costs that go away", 18, GREY_B).next_to(bar_bg, UP, buff=0.15)
        num = draw.number(share.get_value, 0, suffix="%", size=40, color=PROFIT).next_to(bar_bg, DOWN, buff=0.2).align_to(bar_bg, LEFT)
        steps = VGroup(*[VGroup(Dot(radius=0.07, color=H_COL[h]), tx(H_NAME[h], 19, H_COL[h])).arrange(RIGHT, buff=0.15)
                         for h in range(3)]).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.9, -2.45, 0])
        horizon = [D["horizon"][k] for k, _ in lines]
        cum = [sum(v for (k, v), h in zip(lines, horizon) if h <= H) / D["total"] * 100 for H in range(3)]

        def light(H):
            return [tm[i][0].animate.set_fill(H_COL[horizon[i]], opacity=0.9) for i in range(len(lines))
                    if horizon[i] == H]

        with self.voiceover(
            "Here is a real airline's year. <bookmark mark='a'/> Delta Air Lines spent fifty-seven and a half billion "
            "dollars running its airline in 2025, and every block here is one line of its income statement, drawn to "
            "size: salaries, fuel, the refinery it owns, landing fees, maintenance, depreciation of the fleet. "
            "<bookmark mark='b'/> Now cancel one flight, tomorrow morning, Atlanta to Boston. Which of these costs "
            "go away?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, scale=0.9) for b in tm], lag_ratio=0.06), FadeIn(src), run_time=2.4)
            vo.wait_until("b")
            self.play(FadeIn(jet, shift=RIGHT * 0.4), FadeIn(flight))
            self.play(FadeIn(stamp, scale=1.6), Create(stamp_box), run_time=0.6)

        with self.voiceover(
            "Within days, only the costs of flying that flight. <bookmark mark='a'/> The fuel it would have burned, "
            "the landing fee at Boston, the snacks, the commission on the tickets. That is about "
            f"{cum[0]:.0f} percent of Delta's costs. These are the variable costs: they move with how much you fly. "
            "<bookmark mark='b'/> The crew is still paid this month, the aircraft still sits on the ground, the "
            "headquarters in Atlanta still has its lights on. <bookmark mark='c'/> Cancel flying for a year, and "
            "most of the rest can go too: staff can be let go, contracts ended, maintenance deferred. That reaches "
            f"about {cum[1]:.0f} percent. <bookmark mark='d'/> What is left, the depreciation and rent of the fleet, "
            "goes away only as the planes are sold or reach the end of their lives."
        ) as vo:
            self.play(FadeIn(bar_bg), FadeIn(bar_t), FadeIn(bar), FadeIn(num), FadeIn(steps[0]))
            vo.wait_until("a")
            self.play(*light(0), share.animate.set_value(cum[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Indicate(tm[0], color=FIXED, scale_factor=1.03))
            vo.wait_until("c")
            self.play(FadeIn(steps[1]), *light(1), share.animate.set_value(cum[1]), run_time=2.4)
            vo.wait_until("d")
            self.play(FadeIn(steps[2]), *light(2), share.animate.set_value(cum[2]), run_time=1.6)
        lesson = tx("Whether a cost is fixed depends on how far ahead you look.", 26, PRICE, bold=True).to_edge(
            DOWN, buff=0.2)
        with self.voiceover(
            "So fixed and variable are not properties of a cost. They depend on the horizon of the decision. Over a "
            "day almost everything is fixed; over ten years almost nothing is. Economists call that the short run "
            "and the long run, and they are not lengths of time but the set of things you can still change."
        ):
            self.play(FadeOut(src), FadeIn(lesson, shift=UP * 0.1))
        self.clear_scene()

    # --- the two-by-two: fixed or variable, avoidable or sunk --------------------------------------------------------
    def grid(self):
        W, H = 5.2, 2.7
        cx, cy = 0.9, -0.45
        cells = VGroup()
        for i in range(2):
            for j in range(2):
                cells.add(Rectangle(width=W, height=H, stroke_color=GREY_D, stroke_width=2, fill_color="#141A24",
                                    fill_opacity=1).move_to([cx + (j - 0.5) * W, cy + (0.5 - i) * H, 0]))
        top = VGroup(tx("avoidable", 26, PROFIT, bold=True).move_to([cx - W / 2, cy + H + 0.35, 0]),
                     tx("sunk", 26, LOSS, bold=True).move_to([cx + W / 2, cy + H + 0.35, 0]))
        top_q = tx("Do you get it back if you stop?", 20, GREY_B).next_to(top, UP, buff=0.12)
        side = VGroup(tx("variable", 24, VAR, bold=True), tx("fixed", 24, FIXED, bold=True))
        side[0].move_to([cx - W - 1.05, cy + H / 2, 0])
        side[1].move_to([cx - W - 1.05, cy - H / 2, 0])
        side_q = VGroup(tx("rises with", 16, GREY_B), tx("output", 16, GREY_B)).arrange(DOWN, buff=0.04).next_to(
            side[0], DOWN, buff=0.1)
        side_q2 = VGroup(tx("the same at", 16, GREY_B), tx("any output", 16, GREY_B)).arrange(DOWN, buff=0.04).next_to(
            side[1], DOWN, buff=0.1)

        def chip_(glyph, text, col):
            g = glyph.copy()
            g.scale_to_fit_height(0.5) if g.height > g.width else g.scale_to_fit_width(0.75)
            t = tx(text, 18, col)
            return VGroup(g, t).arrange(RIGHT, buff=0.15)
        drop = VGroup(Circle(radius=0.2, stroke_width=0, fill_color=VAR, fill_opacity=1),
                      Triangle(stroke_width=0, fill_color=VAR, fill_opacity=1).scale(0.2).shift(UP * 0.22))
        fuel = chip_(drop, "jet fuel", VAR)
        land = chip_(draw.plane(1.0, windows=False), "a landing fee", VAR)
        crew = chip_(draw.person(0.6), "this year's pilots", FIXED)
        lease = chip_(draw.house(0.6), "a hangar lease", FIXED)
        jet = chip_(draw.plane(1.0, windows=False), "a jet already bought", GREY_A)
        mask = chip_(draw.chip(0.6), "a chip's design, done", LOSS)
        ad = chip_(draw.note_bill(0.7), "last year's adverts", LOSS)
        spots = dict(fuel=(cx - W / 2, cy + H / 2 + 0.45), land=(cx - W / 2, cy + H / 2 - 0.45),
                     crew=(cx - W / 2, cy - H / 2 + 0.45), lease=(cx - W / 2, cy - H / 2 - 0.45),
                     jet=(cx, cy - H / 2 + 0.0), mask=(cx + W / 2 + 0.2, cy - H / 2 + 0.75),
                     ad=(cx + W / 2 + 0.2, cy - H / 2 - 0.75))
        chips = dict(fuel=fuel, land=land, crew=crew, lease=lease, jet=jet, mask=mask, ad=ad)
        for k, c in chips.items():
            c.move_to([*spots[k], 0])
        jet.move_to([cx, cy - H / 2 - 0.05, 0])
        empty = tx("almost empty", 18, GREY_C, italic=True).move_to([cx + W / 2, cy + H / 2, 0])
        with self.voiceover(
            "That gives four words, and they sort costs along two different lines. <bookmark mark='a'/> The first "
            "line asks whether a cost rises with how much you make. Fuel does: fly twice as far and you buy twice as "
            "much. So do landing fees. Those are variable. <bookmark mark='b'/> A year's pilots, the lease on a "
            "hangar, do not change with one flight more or less. Those are fixed. <bookmark mark='c'/> The second "
            "line asks whether you get the money back if you stop. A fixed cost can still be avoidable: give notice "
            "on the hangar and the rent ends. <bookmark mark='d'/> A sunk cost is gone whatever you do: a chip "
            "design that is finished, last year's advertising. <bookmark mark='e'/> And a jet already bought sits on "
            "the line: it is only partly sunk, because it can be sold, though for less than you paid."
        ) as vo:
            self.play(FadeIn(cells), FadeIn(side), FadeIn(side_q), FadeIn(side_q2))
            vo.wait_until("a")
            self.play(FadeIn(fuel, shift=DOWN * 0.3), FadeIn(land, shift=DOWN * 0.3))
            vo.wait_until("b")
            self.play(FadeIn(crew, shift=DOWN * 0.3), FadeIn(lease, shift=DOWN * 0.3))
            vo.wait_until("c")
            self.play(FadeIn(top), FadeIn(top_q))
            self.play(Indicate(lease, color=PROFIT))
            vo.wait_until("d")
            self.play(FadeIn(mask, shift=LEFT * 0.3), FadeIn(ad, shift=LEFT * 0.3))
            vo.wait_until("e")
            self.play(FadeIn(jet, scale=0.8))
            self.play(jet.animate.shift(RIGHT * 0.25), rate_func=there_and_back, run_time=0.8)
        with self.voiceover(
            "The top right corner is almost empty, and for a reason. A cost that rises with output can be avoided by "
            "making less. Every variable cost is avoidable; the interesting decisions are all about the fixed ones."
        ):
            self.play(FadeIn(empty))
            self.play(Indicate(cells[1], color=GREY_B, scale_factor=1.02))
        self.clear_scene()

    # --- sunk costs: look forward ------------------------------------------------------------------------------
    def sunk(self):
        fac = draw.factory(2.4).move_to([-4.6, 1.2, 0])
        scaffold = VGroup(*[Line([x, -0.1, 0], [x, 1.9, 0], stroke_color=GREY_C, stroke_width=1.5)
                            for x in np.linspace(-5.7, -3.5, 6)],
                          *[Line([-5.8, y, 0], [-3.4, y, 0], stroke_color=GREY_C, stroke_width=1.5)
                            for y in (0.4, 1.0, 1.6)])
        fac.set_opacity(0.45)
        cap = tx("a new plant, 80% built", 20, GREY_B).next_to(fac, DOWN, buff=0.35)
        base = -2.4
        u = 0.42  # height per $m

        def col(x, v, color, name, top=None):
            r = Rectangle(width=1.3, height=v * u, stroke_width=0, fill_color=color, fill_opacity=0.9)
            r.move_to([x, base + (top or 0) * u, 0], aligned_edge=DOWN)
            return VGroup(r, tx(name, 17, color).next_to(r, DOWN, buff=0.12),
                          tx(f"${v:.0f}m", 22, color, bold=True).next_to(r, UP, buff=0.08))
        spent = col(-0.6, 8, "#6B7280", "already spent")
        finish = col(1.5, 2, VAR, "to finish")
        worth = col(3.6, 5, PROFIT, "worth, finished")
        cmp1 = MathTex(r"\$5\text{m} > \$2\text{m}", font_size=40, color=PROFIT).move_to([2.55, 2.9, 0])
        verdict1 = tx("finish it", 28, PROFIT, bold=True).next_to(cmp1, DOWN, buff=0.15)
        with self.voiceover(
            "Sunk costs matter because people find them so hard to ignore. <bookmark mark='a'/> Your company is "
            "building a plant. Eight million dollars are spent; two million more will finish it. Since you began, "
            "the market has turned, and the finished plant is now worth only five million. <bookmark mark='b'/> "
            "Overall the project loses money: ten million in, five million out. Do you finish it? "
            "<bookmark mark='c'/> Yes. From here, two million buys something worth five. The eight already spent "
            "is gone either way."
        ) as vo:
            self.play(FadeIn(fac), Create(scaffold), FadeIn(cap))
            vo.wait_until("a")
            self.play(GrowFromEdge(spent[0], DOWN), FadeIn(spent[1:]))
            self.play(GrowFromEdge(finish[0], DOWN), FadeIn(finish[1:]))
            self.play(GrowFromEdge(worth[0], DOWN), FadeIn(worth[1:]))
            vo.wait_until("b")
            self.play(Indicate(spent, color=GREY_B))
            vo.wait_until("c")
            self.play(Write(cmp1), FadeIn(verdict1))
            self.play(spent.animate.set_opacity(0.25))

        finish2 = col(1.5, 6, VAR, "to finish")
        cmp2 = MathTex(r"\$5\text{m} < \$6\text{m}", font_size=40, color=LOSS).move_to([2.55, 2.9, 0])
        verdict2 = tx("stop, and sell the site", 28, LOSS, bold=True).next_to(cmp2, DOWN, buff=0.15)
        with self.voiceover(
            "Now suppose finishing would cost six million instead. <bookmark mark='a'/> Stop, even though eight "
            "million has been poured in, because six more buys only five. <bookmark mark='b'/> Notice that the eight "
            "million appeared in neither decision. It is the same whichever way you choose, so it cannot tell you "
            "which way to choose. That is all 'ignore sunk costs' means."
        ) as vo:
            self.play(ReplacementTransform(finish, finish2), FadeOut(cmp1), FadeOut(verdict1))
            vo.wait_until("a")
            self.play(Write(cmp2), FadeIn(verdict2))
            vo.wait_until("b")
            self.play(spent.animate.set_opacity(1), run_time=0.5)
            self.play(spent.animate.shift(DOWN * 0.3).set_opacity(0.15), run_time=1.2)

        self.play(*[FadeOut(m) for m in self.mobjects])
        # Concorde: a slender delta
        L = 5.2
        body = Polygon([-0.5 * L, 0.02 * L, 0], [0.42 * L, 0.02 * L, 0], [0.5 * L, -0.012 * L, 0],
                       [0.42 * L, -0.025 * L, 0], [-0.5 * L, -0.025 * L, 0], stroke_width=0, fill_color="#E8EAED",
                       fill_opacity=1)
        wing = Polygon([0.1 * L, -0.02 * L, 0], [-0.42 * L, -0.11 * L, 0], [-0.46 * L, -0.03 * L, 0], stroke_width=0,
                       fill_color="#B9C2CF", fill_opacity=1)
        fin = Polygon([-0.36 * L, 0.02 * L, 0], [-0.5 * L, 0.13 * L, 0], [-0.5 * L, 0.02 * L, 0], stroke_width=0,
                      fill_color="#E8EAED", fill_opacity=1)
        concorde = VGroup(wing, body, fin).move_to([-4.2, 1.4, 0]).scale(0.6)
        name = tx("the Concorde fallacy", 40, PRICE, bold=True).move_to([0, -0.6, 0])
        who = tx("Richard Dawkins and Tamsin Carlisle, Nature, 1976", 22, GREY_B).next_to(name, DOWN, buff=0.2)
        rule = tx("Decide on what a choice changes from here on: the money to come, not the money gone.", 24,
                  WHITE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The mistake has a name. <bookmark mark='a'/> In 1976 the biologists Richard Dawkins and Tamsin Carlisle "
            "called it the Concorde fallacy, after the supersonic airliner that Britain and France kept paying for "
            "long after it was clear it would never pay back, partly, the argument went, because so much had already "
            "been spent. <bookmark mark='b'/> The rule it breaks is the one this part keeps using: decide on what a "
            "choice changes from here on, the money to come, not the money gone."
        ) as vo:
            self.play(FadeIn(concorde, shift=RIGHT * 0.6), run_time=1.0)
            vo.wait_until("a")
            self.play(concorde.animate.scale(1 / 0.6).move_to([1.0, 1.6, 0]), run_time=2.0,
                      rate_func=rate_functions.ease_out_cubic)
            self.play(FadeIn(name, shift=UP * 0.1), FadeIn(who))
            vo.wait_until("b")
            self.play(FadeIn(rule, shift=UP * 0.1), concorde.animate.shift(RIGHT * 9), run_time=2.0,
                      rate_func=rate_functions.ease_in_cubic)
        self.clear_scene()
