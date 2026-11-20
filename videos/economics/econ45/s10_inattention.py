from __future__ import annotations

from videos.economics.econ45.common import *  # noqa: F403


class Inattention(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Inattention", r"What happens to prices nobody reads?",
             "Chapter eight. Inattention.", lit={2006: r"Gabaix and Laibson", 2012: r"Lacetera, Pope and Sydnor"},
             scale=("person", "market"), horizon=("a day",))
        self.shrouded()
        self.curse()
        self.digits()

    def shrouded(self):
        S = load("shrouded")
        cost = TRUTH["shrouded"]["cost"]
        ax = plane([0, 3], [0, 32], center=LEFT * 2.4 + DOWN * 0.4, x_length=6.0, y_length=4.6, xticks=[],
                   yticks=[0, 10, 20, 30], ylabel=r"dollars", yfmt=lambda v: f"{v:.0f}", font_size=14)

        def stack(x, parts):
            g = VGroup()
            base = 0.0
            for val, col, nm in parts:
                p0, p1 = ax.ax.c2p(x - 0.35, base), ax.ax.c2p(x + 0.35, base + val)
                r = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                              fill_opacity=0.85).move_to((p0 + p1) / 2)
                t = label(nm, font_size=14, color=WHITE).move_to(r)
                g.add(VGroup(r, t))
                base += val
            return g
        my = stack(0.9, [(S["base_price"], PLAN, r"printer"), (TRUTH["shrouded"]["addon_price"], LOSS, r"ink")])
        so = stack(2.1, [(S["base_price"], PLAN, r"printer"), (TRUTH["shrouded"]["effort"], SOPH, r"effort")])
        lm = label(r"the myope", font_size=17, color=LOSS).next_to(ax.ax.c2p(0.9, 0), DOWN, buff=0.15)
        ls = label(r"the sophisticate", font_size=17, color=SOPH).next_to(ax.ax.c2p(2.1, 0), DOWN, buff=0.15)
        cl = VGroup(seg(ax, 0, cost, 3, cost, GREY_B, 1.8, dashed=True),
                    label(rf"the printer's cost, \${cost:.0f}", font_size=15, color=GREY_B).next_to(
                        ax.ax.c2p(3, cost), RIGHT, buff=0.1))
        side = VGroup(
            label(rf"{100 * S['alpha']:.0f}\% of buyers do not \\ think about the ink", font_size=19, color=LOSS),
            label(rf"competition prices \\ the printer at \${S['base_price']:.2f}, \\ below its cost", font_size=19,
                  color=PLAN),
            label(rf"myopes pay \${S['myope_pays']:.2f} in all; \\ sophisticates \${S['soph_pays']:.2f}", font_size=19,
                  color=WHITE),
            label(r"the myopes subsidize \\ the sophisticates", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = published_tag(tables.INATTENTION_45.tag + r"; \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "Some prices are on the tag; others arrive later. A printer, then its ink. A hotel room, then its "
            "minibar. A bank account, then its overdraft fee. <bookmark mark='a'/> On the Island, most buyers of "
            f"printers do not think about ink when they buy; it costs {TRUTH['shrouded']['addon_cost']:.0f} dollars "
            f"to make and sells for {TRUTH['shrouded']['addon_price']:.0f}. <bookmark mark='b'/> Competition does "
            "not drive the ink's price down, because nobody chooses a printer by it. It drives the printer's price "
            f"down instead, to {money_words(S['base_price'])}, below its cost of {cost:.0f} dollars, paid for by "
            f"the ink. <bookmark mark='c'/> Myopic buyers pay {money_words(S['myope_pays'])} in all. Sophisticated "
            "buyers take the cheap printer and avoid the dear ink, refilling cartridges or printing elsewhere, "
            f"and pay {money_words(S['soph_pays'])}. <bookmark mark='d'/> In a competitive market the inattentive "
            "subsidize the attentive. Xavier Gabaix and David Laibson called these shrouded attributes."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(cl), FadeIn(lm), FadeIn(ls), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(my[0], DOWN), GrowFromEdge(so[0], DOWN), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(my[1], DOWN), GrowFromEdge(so[1], DOWN), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def curse(self):
        steps = flow_chain([(r"a firm reveals \\ the ink's price", PLAN), (r"myopes learn \\ to avoid ink", SOPH),
                            (r"they avoid it at \\ every firm", GYM), (r"the revealer \\ gains no one", LOSS)],
                           notes=[r"an advertisement: \\ ``our rivals \\ overcharge for ink''", r"they become \\ "
                                  r"sophisticates", r"and buy the cheap \\ printer anywhere", r"so no firm \\ "
                                  r"unshrouds"], box_w=2.8, font_size=20, note_size=16).move_to(UP * 0.4)
        foot = label(r"the curse of debiasing: \ the market can keep a bias alive", font_size=23,
                     color=E.ACCENT).to_edge(DOWN, buff=0.9)
        tag = published_tag(tables.INATTENTION_45.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Why does no firm advertise the truth about ink and steal the customers? <bookmark mark='a'/> Suppose a "
            "firm does. <bookmark mark='b'/> The myopes it educates become sophisticates. <bookmark mark='c'/> But "
            "a sophisticate does not need the honest firm: the cheapest move is to buy any firm's subsidized "
            "printer and avoid its ink. <bookmark mark='d'/> The firm that revealed the shroud gains nobody, and "
            "pays for the advertising. So in equilibrium no firm unshrouds, even in a competitive market. Gabaix "
            "and Laibson called it the curse of debiasing."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(foot), FadeIn(steps.boxes[0]), FadeIn(steps.notes[0]))
            vo.wait_until("a")
            self.play(Indicate(steps.boxes[0], scale_factor=1.05))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(steps.arrows[k]), FadeIn(steps.boxes[k + 1]), FadeIn(steps.notes[k + 1]))
        self.clear_scene()

    def digits(self):
        C = load("cars")
        mid = np.array(C["mid"]) / 1000
        mp = np.array(C["mean_price"]) / 1000
        ax = plane([0, 120], [4.5, 12], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 20, 40, 60, 80, 100, 120], yticks=[6, 8, 10, 12],
                   xlabel=r"miles on the odometer, \ thousands", ylabel=r"wholesale price, \ thousand dollars",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        pts = VGroup(*[dot(ax, x, y, BUY, 0.035) for x, y in zip(mid, mp)])
        thr = VGroup(*[vline(ax, k, 4.5, 12, GREY_D, 1.0) for k in range(10, 121, 10)])
        fit = np.polyfit(mid, mp, 1)
        res = (mp - np.polyval(fit, mid)) * 1000
        ax2 = plane([0, 120], [-160, 160], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                    xticks=[0, 20, 40, 60, 80, 100, 120], yticks=[-150, -75, 0, 75, 150],
                    xlabel=r"miles on the odometer, \ thousands", ylabel=r"price minus the straight-line trend, \ "
                    r"dollars", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        pts2 = VGroup(*[dot(ax2, x, y, BUY, 0.035) for x, y in zip(mid, np.clip(res, -160, 160))])
        thr2 = VGroup(*[vline(ax2, k, -160, 160, LOSS, 1.2) for k in range(10, 121, 10)])
        eq = MathTex(r"\hat m = L + (1-\theta)(m - L), \quad \hat\theta = \frac{\text{jump}}{\text{jump} + "
                     r"\text{slope}\times 10{,}000}", font_size=28, color=THEORY).to_edge(UP, buff=0.4)
        side = VGroup(
            label(r"each dot: \ the average \\ price in a 500-mile bin", font_size=18, color=BUY),
            label(rf"a jump of \${C['jump']:.0f} \\ at every 10,000", font_size=18, color=LOSS),
            label(rf"$\hat\theta$ = {C['theta_hat']:.2f} \ (planted {C['theta']:.1f})", font_size=19, color=E.ACCENT),
            label(r"Lacetera, \ Pope and \\ Sydnor: \ steps of about \\ \$150--200 in 22 million \\ auction sales",
                  font_size=17, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).to_edge(RIGHT, buff=0.35)
        tag = published_tag(tables.INATTENTION_45.tag + r"; \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "Inattention leaves fingerprints in prices. <bookmark mark='a'/> Here are wholesale prices of used cars "
            f"on the Island, by mileage, from {C['n'] // 1000:,} thousand sales. Each dot averages the cars in a "
            "five-hundred-mile bin. More miles, lower price, as it should be. <bookmark mark='b'/> Take away the "
            "straight-line trend, and a sawtooth appears: at every ten thousand miles the price drops by a step, "
            "as if 49,999 miles and 50,000 were very different cars, by about "
            f"{C['jump']:.0f} dollars. <bookmark mark='c'/> Buyers here read the first digit fully and "
            "only part of the rest. If theta is the share of the remaining digits they ignore, the step and the "
            "slope between steps pin it down: theta is the step divided by the step plus ten thousand miles' worth "
            f"of slope. The estimate is {C['theta_hat']:.2f}, against a planted {C['theta']:.1f}. "
            "<bookmark mark='d'/> Nicola Lacetera, Devin Pope and Justin Sydnor found these steps in more than 22 "
            "million real wholesale car sales, drops of roughly 150 to 200 dollars at each ten-thousand-mile mark. "
            "The buyers at those auctions are professional dealers; the evidence fits partial inattention by the "
            "retail customers they sell to, whose bias the dealers pass back into wholesale prices."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(thr), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.005), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeOut(ax), FadeOut(thr), FadeIn(ax2), FadeIn(thr2), Transform(pts, pts2), FadeIn(side[1]),
                      run_time=1.5)
            vo.wait_until("c")
            self.play(Write(eq), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
