from __future__ import annotations

from videos.economics.econ47.common import *  # noqa: F403


class Rents(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Rent seeking", r"How much is spent chasing a privilege?",
             "Chapter three. Rent seeking.", lit={1967: r"Tullock", 1974: r"Krueger"}, scale=("market", "nation"),
             horizon=("a year",))
        self.rectangle()
        self.contest()
        self.krueger()

    def rectangle(self):
        ax = plane([0, 10], [0, 10], center=LEFT * 2.3 + DOWN * 0.3, x_length=6.0, y_length=5.0, xticks=[],
                   yticks=[], xlabel=r"quantity", ylabel=r"price", font_size=15)
        demand = seg(ax, 0, 10, 10, 0, MANY, 3.0)
        mc = seg(ax, 0, 2, 10, 2, GREY_B, 2.4)
        # monopoly: MR = 10 - 2q = 2 -> q = 4, p = 6; competition: q = 8, p = 2
        tri = Polygon(ax.ax.c2p(4, 6), ax.ax.c2p(8, 2), ax.ax.c2p(4, 2), stroke_width=0, fill_color=LOSS,
                      fill_opacity=0.55)
        rect = Polygon(ax.ax.c2p(0, 2), ax.ax.c2p(4, 2), ax.ax.c2p(4, 6), ax.ax.c2p(0, 6), stroke_width=0,
                       fill_color=FEW, fill_opacity=0.55)
        labs = VGroup(label(r"demand", font_size=15, color=MANY).next_to(ax.ax.c2p(9, 1), UR, buff=0.05),
                      label(r"cost", font_size=15, color=GREY_B).next_to(ax.ax.c2p(10, 2), UP, buff=0.05))
        side = VGroup(
            label(r"a licence, \ a quota \\ or a monopoly raises \\ the price", font_size=19, color=WHITE),
            label(r"red: \ Harberger's triangle, \\ output lost", font_size=19, color=LOSS),
            label(r"gold: \ the rent, \\ a transfer to the holder", font_size=19, color=FEW),
            label(r"Tullock: \ if people compete \\ to get the rent, \ they \\ spend up to the rectangle", font_size=19,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.45)
        tag = published_tag(tables.RENTS_47.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Economists used to measure the cost of a monopoly, a tariff or a licence by a small triangle. "
            "<bookmark mark='a'/> A privilege raises the price above cost. <bookmark mark='b'/> The units no longer "
            "bought are a loss to society: Harberger's triangle, usually small. <bookmark mark='c'/> The rest, the "
            "rectangle, is not a loss but a transfer: buyers pay more, and the holder of the privilege collects it. "
            "<bookmark mark='d'/> In 1967 Gordon Tullock pointed out that privileges are not handed out for free. "
            "If firms compete to win the licence, with lobbyists, lawyers and favours, they will spend up to what "
            "it is worth. Then the rectangle is wasted too, and the true cost of the privilege is the triangle and "
            "the rectangle together."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(demand), Create(mc), FadeIn(labs), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(tri), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(rect), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), Indicate(rect, color=WHITE))
        self.clear_scene()

    def contest(self):
        Tl = load("tullock")
        ax = plane([2, 20], [0, 1], center=LEFT * 1.9 + DOWN * 0.35, x_length=7.6, y_length=4.6,
                   xticks=[2, 5, 10, 15, 20], yticks=[0, 0.25, 0.5, 0.75, 1.0], xlabel=r"players in the contest",
                   ylabel=r"share of the prize spent chasing it", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        ln = path(ax, Tl["n"], Tl["dissipated"], LOBBY, 3.2, smooth=False)
        dots = VGroup(*[dot(ax, n, d, LOBBY, 0.05) for n, d in zip(Tl["n"], Tl["dissipated"])])
        one = DashedLine(ax.ax.c2p(2, 1), ax.ax.c2p(20, 1), color=GREY_B, stroke_width=1.6)
        eq = MathTex(r"x^* = R\,\frac{n-1}{n^2}, \qquad n\,x^* = R\,\frac{n-1}{n}", font_size=30, color=THEORY)
        side = VGroup(
            label(r"$n$ players spend $x_i$; \\ each wins the prize $R$ \\ with probability \\ $x_i / \sum_j x_j$",
                  font_size=19, color=WHITE),
            eq,
            label(r"two players: \ half \\ the prize spent; \\ ten: \ 90\%", font_size=19, color=LOBBY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Tullock's own contest makes this exact. <bookmark mark='a'/> Each of n players spends something, and "
            "wins the prize with probability equal to their share of all the spending, as in the game you just "
            "played. <bookmark mark='b'/> In equilibrium each spends the prize times n minus one over n squared, so "
            "all together they spend the prize times n minus one over n. <bookmark mark='c'/> With two players, "
            "half the prize is spent chasing it. With ten, ninety percent. With many, nearly all of it. Competition, "
            "which in a market drives prices down to cost, here drives spending up to the value of the prize."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(one), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Write(side[1]))
            vo.wait_until("c")
            self.play(Create(ln), FadeIn(dots), FadeIn(side[2]), run_time=2.5)
        self.clear_scene()

    def krueger(self):
        T = tables.RENTS_47.data
        bars = VGroup()
        rows = [(r"India, \ 1964: \ all regulation", T["india"], FEW),
                (r"India, \ 1964: \ import restrictions", T["india_imports"], FEW),
                (r"Turkey, \ 1968: \ import licences", T["turkey"], LOSS)]
        for i, (nm, v, col) in enumerate(rows):
            y = 1.2 - 1.0 * i
            w = v / 16 * 7.0
            r = Rectangle(width=w, height=0.6, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([-1.8 + w / 2, y, 0]))
            bars.add(VGroup(label(nm, font_size=19, color=col).next_to(np.array([-2.0, y, 0]), LEFT, buff=0.1), r,
                            label(rf"{v}\%", font_size=22, color=WHITE).next_to(r, RIGHT, buff=0.15)))
        head = label(r"Krueger, \ 1974: \ rents as a share of national income", font_size=28,
                     color=E.ACCENT).to_edge(UP, buff=0.6)
        foot = label(r"she did not estimate how much of the rents was spent chasing them: \ the rectangle's upper "
                     r"bound", font_size=19, color=GREY_A).to_edge(DOWN, buff=0.7)
        tag = published_tag(tables.RENTS_47.tag, corner=DR, font_size=11)
        with self.voiceover(
            "How big are the rectangles? In 1974 Anne Krueger, who coined the phrase rent seeking, estimated them "
            f"for two economies run by licences. <bookmark mark='a'/> In India in 1964, rents created by government "
            f"regulation were about {T['india']} percent of national income; <bookmark mark='b'/> import "
            f"restrictions alone, {T['india_imports']} percent. <bookmark mark='c'/> In Turkey in 1968, import "
            f"licences alone created rents of about {T['turkey']} percent of national output. <bookmark mark='d'/> "
            "She did not estimate how much of those rents was spent chasing them. But if even part of it was, the "
            "cost of the licence system was far larger than any triangle."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), *[FadeIn(b[0]) for b in bars])
            for mk, b in zip("abc", bars):
                vo.wait_until(mk)
                self.play(GrowFromEdge(b[1], LEFT), FadeIn(b[2]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
