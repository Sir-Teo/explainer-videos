from __future__ import annotations

from videos.economics.econ45.common import *  # noqa: F403


def mug(color=SELL, scale=1.0):
    body = RoundedRectangle(width=1.5, height=1.8, corner_radius=0.18, stroke_color=color, stroke_width=4,
                            fill_color=color, fill_opacity=0.18)
    handle = Arc(radius=0.45, start_angle=-PI / 2, angle=PI, stroke_color=color, stroke_width=6).next_to(
        body, RIGHT, buff=-0.05)
    rim = Ellipse(width=1.5, height=0.3, stroke_color=color, stroke_width=3).move_to(body.get_top())
    word = label(r"the Island", font_size=18, color=color).move_to(body)
    return VGroup(body, handle, rim, word).scale(scale)


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Play it: \ your mug", r"What would it take for you to sell it?",
             "Chapter two. Play it: your mug.", lit={1990: r"Kahneman, Knetsch and Thaler"}, scale=("person",),
             horizon=("a day",))
        self.ask()
        self.market()
        self.many()

    def ask(self):
        m = mug().move_to(LEFT * 3.2 + UP * 0.3)
        head = label(r"Your turn: \ this mug is now yours", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        q1 = label(r"the lowest price \\ at which you would \\ sell it back:", font_size=26, color=SELL)
        q2 = label(r"\$ \underline{\hspace{2.4cm}}", font_size=34, color=WHITE)
        qs = VGroup(q1, q2).arrange(DOWN, buff=0.4).move_to(RIGHT * 2.2 + UP * 0.5)
        other = label(r"in the next room, \ others without a mug \\ name the most they would pay for one",
                      font_size=21, color=BUY).to_edge(DOWN, buff=1.2)
        ring = countdown().scale(0.6).next_to(qs, DOWN, buff=0.45)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Your turn. Here is a mug from the Island's gift shop, and it is yours to keep. "
            "<bookmark mark='a'/> Before you take it home, someone offers to buy it. What is the lowest price at "
            "which you would sell it? Not what you think it is worth to others: the price at which you would rather "
            "have the money than the mug. <bookmark mark='b'/> In the next room, people who were not given a mug "
            "are asked the mirror question: the most they would pay for one. Pause, and write down your price."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), DrawBorderThenFill(m), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(qs, shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(other), FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.play(FadeOut(ring))
        self.clear_scene()

    def market(self):
        M = load("mugs")
        k = M["k"]
        ask, ask0, bid = np.array(M["ask"]), np.array(M["ask0"]), np.array(M["bid"])
        ax = plane([0, k], [0, 16], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 5, 10, 15, 20], yticks=[0, 4, 8, 12, 16], xlabel=r"mugs, \ in order",
                   ylabel=r"dollars", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)

        def steps(vals, color, width=3.0, dashed=False):
            xs, ys = [], []
            for i, v in enumerate(vals):
                xs += [i, i + 1]
                ys += [min(v, 16), min(v, 16)]
            ln = path(ax, xs, ys, color, width, smooth=False)
            return DashedVMobject(ln, num_dashes=60) if dashed else ln
        s0 = steps(ask0, SELL, 2.2, dashed=True)
        s1 = steps(ask, SELL, 3.2)
        d = steps(bid, BUY, 3.2)
        t0 = VGroup(vline(ax, M["trades0"], 0, 16, GREY_B), label(rf"{M['trades0']} trades", font_size=16,
                                                                   color=GREY_B).next_to(ax.ax.c2p(M["trades0"], 16),
                                                                                         UP, buff=0.05))
        t1 = VGroup(vline(ax, M["trades"], 0, 16, LOSS), label(rf"{M['trades']} trades", font_size=16,
                                                               color=LOSS).next_to(ax.ax.c2p(M["trades"], 14.5),
                                                                                   LEFT, buff=0.1))
        side = VGroup(
            label(rf"{M['n']} people: \ {k} given a mug", font_size=19, color=WHITE),
            label(r"blue: \ buyers' bids, \\ highest first", font_size=18, color=BUY),
            label(r"dashed: \ owners' asks if \\ they valued the mug \\ as buyers do", font_size=18, color=SELL),
            label(rf"gold: \ owners' asks with \\ losses counted {M['lam']:.0f}$\times$", font_size=18, color=SELL),
            label(r"trade happens \\ where bids beat asks", font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            f"Here is one session on the Island: {M['n']} people, {k} of them given a mug at random. "
            "<bookmark mark='a'/> In blue, the buyers' bids, highest first. <bookmark mark='b'/> If owners valued "
            "the mug just as buyers do, their asks would be the dashed line, and every mug whose owner values it "
            f"less than some buyer would change hands: here {M['trades0']} of {k}, close to half, as the Coase "
            "theorem of Part fifteen predicts when trading is free. <bookmark mark='c'/> But the Island's owners "
            f"feel giving up the mug as a loss, and losses count {M['lam']:.0f} times as much as gains, so every "
            "ask doubles. <bookmark mark='d'/> Now bids beat asks for only "
            f"{M['trades']} mugs. Nothing about the mugs or the people changed, only who happened to be holding one."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(d), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(s0), FadeIn(side[2]), FadeIn(t0), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(s1), FadeIn(side[3]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(t1), FadeIn(side[4]))
        self.clear_scene()

    def many(self):
        M = load("mugs")
        P, L = M["plain"], M["loss"]
        bars = VGroup()
        rows = [(r"no loss aversion", P["share_traded"], GREY_B), (rf"losses count {M['lam']:.0f}$\times$",
                                                                   L["share_traded"], LOSS)]
        for i, (nm, v, col) in enumerate(rows):
            y = 0.9 - 1.3 * i
            w = v * 12
            r = Rectangle(width=w, height=0.7, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([-2.2 + w / 2, y, 0]))
            bars.add(VGroup(label(nm, font_size=21, color=col).next_to(np.array([-2.4, y, 0]), LEFT, buff=0.1), r,
                            label(rf"{100 * v:.0f}\%", font_size=22, color=WHITE).next_to(r, RIGHT, buff=0.15)))
        head = label(rf"share of mugs that change hands, \ average of {TRUTH['mugs']['reps']:,} Island sessions",
                     font_size=24, color=E.ACCENT).to_edge(UP, buff=0.6)
        ratio = label(rf"median ask \${L['median_ask']:.2f} \ against median bid \${L['median_bid']:.2f}: \ "
                      rf"{L['ratio']:.1f} to 1", font_size=22, color=SELL).next_to(bars, DOWN, buff=0.7)
        kkt = label(r"Kahneman, \ Knetsch and Thaler, \ 1990: \ owners asked about twice what buyers bid, \\ and "
                    r"far fewer than half the mugs traded", font_size=21, color=GREY_A).to_edge(DOWN, buff=0.6)
        tag = published_tag(tables.KKT_1990.tag + r"; \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            f"Run the session {TRUTH['mugs']['reps']:,} times. <bookmark mark='a'/> Without loss aversion, half "
            f"the mugs change hands on average. <bookmark mark='b'/> With it, {100 * L['share_traded']:.0f} percent "
            f"do. <bookmark mark='c'/> The median owner asks {money_words(L['median_ask'])}, the median buyer bids "
            f"{money_words(L['median_bid'])}. <bookmark mark='d'/> In 1990 Daniel Kahneman, Jack Knetsch and Richard "
            "Thaler ran this experiment with real coffee mugs and real money. Owners asked about twice what buyers "
            "would pay, and far fewer mugs traded than the half that standard theory predicts. They called it the "
            "endowment effect. Compare your own price with what you would have paid."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(bars[0][0]), FadeIn(bars[1][0]))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0][1], LEFT), FadeIn(bars[0][2]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1][1], LEFT), FadeIn(bars[1][2]))
            vo.wait_until("c")
            self.play(FadeIn(ratio))
            vo.wait_until("d")
            self.play(FadeIn(kkt))
        self.clear_scene()
