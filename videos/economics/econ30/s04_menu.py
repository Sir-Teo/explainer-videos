from __future__ import annotations

from videos.economics.econ30.common import *  # noqa: F403


class Menu(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Why prices stick: \ menu costs", r"Why not change a price the moment conditions change?",
             "Chapter three. Why prices stick: menu costs.", lit={1985: r"Mankiw; \ Akerlof and Yellen"},
             scale=("firm",), horizon=("a month", "a year"))
        self.flat_top()
        self.table()
        self.mankiw()

    def flat_top(self):
        M = load("menu")
        eps, ps = M["eps"], M["markup"]
        r = np.linspace(0.92, 1.12, 161)                  # price relative to the best price
        prof = ((r * ps - 1) * (r * ps) ** (-eps)) / ((ps - 1) * ps ** (-eps))
        qty = r ** (-eps)
        ax = plane([0.92, 1.12], [0, 1.7], center=LEFT * 2.0 + DOWN * 0.3, x_length=8.0, y_length=4.8,
                   xticks=[0.95, 1.0, 1.05, 1.1], yticks=[0, 0.5, 1.0, 1.5], xlabel=r"Bo's fare, \ relative to the "
                   r"best fare", ylabel=r"relative to the best fare's", xfmt=lambda v: f"{v:.2f}",
                   yfmt=lambda v: f"{v:.1f}", font_size=15)
        pl = path(ax, r, prof, PRICE, 3.5)
        ql = path(ax, r, qty, OUTPUT, 3, yr=(0, 1.7))
        best = DashedLine(ax.ax.c2p(1, 0), ax.ax.c2p(1, 1.7), color=GREY_C, stroke_width=1.5)
        g = 1.05
        mark_p = dot(ax, g, float(np.interp(g, r, prof)), PRICE, 0.08)
        mark_q = dot(ax, g, float(np.interp(g, r, qty)), OUTPUT, 0.08)
        row = next(x for x in M["rows"] if abs(x["gap"] - 0.05) < 1e-9)
        side = VGroup(
            label(rf"demand elasticity {eps:.0f}: \\ the best fare is {100 * (ps - 1):.0f}\% \\ above cost",
                  font_size=19, color=GREY_A),
            label(r"gold: \ Bo's profit", font_size=19, color=PRICE),
            label(r"green: \ passengers carried", font_size=19, color=OUTPUT),
            label(rf"a fare 5\% too high: \\ profit {100 * row['profit_loss']:.1f}\% lower; \\ passengers "
                  rf"{100 * row['output_loss']:.0f}\% fewer", font_size=19, color=E.ACCENT),
            label(r"the top of the profit curve \\ is flat", font_size=20, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Back on the Island, Bo's ferry fare is painted on a board by the pier. Repainting it is a nuisance, and "
            "regular passengers dislike surprises. <bookmark mark='a'/> Bo faces a demand elasticity of "
            f"{eps:.0f}, so his best fare is {100 * (ps - 1):.0f} percent above his cost. Now suppose demand falls, "
            "and his best fare falls with it, but the old fare stays on the board. <bookmark mark='b'/> In gold, "
            "Bo's profit, against how far his fare is from the best one. <bookmark mark='c'/> In green, the number "
            "of passengers he carries. <bookmark mark='d'/> With a fare five percent too high, his profit is only "
            f"{100 * row['profit_loss']:.1f} percent below the best he could do, but he carries "
            f"{100 * row['output_loss']:.0f} percent fewer passengers. <bookmark mark='e'/> The top of a profit "
            "curve is flat: near the best price, a mistake costs the seller very little."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(best), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(pl), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(ql), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(GrowFromCenter(mark_p), GrowFromCenter(mark_q), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]), Indicate(pl, color=WHITE, scale_factor=1.0))
        self.clear_scene()

    def table(self):
        M = load("menu")
        heads = (r"fare too high by", r"Bo's profit lost", r"passengers lost", r"ratio")
        xs = [-4.2, -1.3, 1.6, 4.4]
        hrow = VGroup(*[label(h, font_size=22, color=GREY_B).move_to(RIGHT * x + UP * 1.9) for h, x in zip(heads, xs)])
        rule = Line(LEFT * 6.0, RIGHT * 6.0, stroke_color=GREY_D, stroke_width=1.5).move_to(UP * 1.5)
        rows = VGroup()
        for n, r in enumerate(M["rows"]):
            y = 0.95 - 0.7 * n
            rows.add(VGroup(label(rf"{100 * r['gap']:.0f}\%", font_size=24).move_to(RIGHT * xs[0] + UP * y),
                            label(rf"{100 * r['profit_loss']:.2f}\%", font_size=24, color=PRICE).move_to(
                                RIGHT * xs[1] + UP * y),
                            label(rf"{100 * r['output_loss']:.1f}\%", font_size=24, color=OUTPUT).move_to(
                                RIGHT * xs[2] + UP * y),
                            label(rf"{r['ratio']:.0f} to 1", font_size=24, color=E.ACCENT).move_to(
                                RIGHT * xs[3] + UP * y)))
        foot = label(r"profit lost grows with the \emph{square} of the gap; \ passengers lost grow with the gap",
                     font_size=22, color=HOLD).to_edge(DOWN, buff=0.8)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here are the numbers. <bookmark mark='a'/> A fare one percent too high costs Bo "
            f"{100 * M['rows'][0]['profit_loss']:.2f} percent of his profit, and the island "
            f"{100 * M['rows'][0]['output_loss']:.1f} percent of its ferry trips: forty times as much. "
            "<bookmark mark='b'/> At two percent, twenty times. <bookmark mark='c'/> At five percent, eight times. "
            "<bookmark mark='d'/> At ten percent, four times. <bookmark mark='e'/> The reason is general. The loss "
            "of profit grows with the square of the gap, because the profit curve is flat at the top; the loss of "
            "output grows with the gap itself."
        ) as vo:
            self.play(FadeIn(hrow), FadeIn(rule), FadeIn(tag))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def mankiw(self):
        rows = VGroup(
            label(r"Mankiw, \ 1985: \ small menu costs and large business cycles", font_size=26, color=E.ACCENT),
            label(r"for the firm, \ not repricing costs almost nothing: \ a second-order loss", font_size=22,
                  color=PRICE),
            label(r"for society, \ the lost output is first-order", font_size=22, color=OUTPUT),
            label(r"so a tiny cost of changing prices can be enough to leave them alone, \ and to let a fall in "
                  r"money cut output", font_size=22, color=GREY_A),
            label(r"Akerlof and Yellen, \ 1985: \ firms that are only nearly rational lose little, \ the economy a "
                  r"lot", font_size=22, color=CB),
            label(r"the reason money is not neutral, \ in one picture", font_size=24, color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Mankiw, \ \emph{QJE} 100(2) (1985); \ Akerlof and Yellen, \ \emph{QJE} 100 (1985), "
                            r"supplement", corner=DR, font_size=12)
        with self.voiceover(
            "In 1985 Gregory Mankiw turned this into an argument about the whole economy. "
            "<bookmark mark='a'/> For a firm, leaving its price alone after a small change in demand costs almost "
            "nothing: a loss of the second order. <bookmark mark='b'/> But the output lost to society is of the "
            "first order. <bookmark mark='c'/> So even a tiny cost of changing prices, a menu cost, can be enough "
            "to keep prices where they are, and then a fall in the money supply cuts output instead of prices. "
            "<bookmark mark='d'/> George Akerlof and Janet Yellen made the same point the same year: firms that "
            "are only nearly rational lose little, while the economy loses a lot. <bookmark mark='e'/> It is the "
            "reason money is not neutral, in one picture."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
