from __future__ import annotations

from videos.economics.econ29.common import *  # noqa: F403


class Labour(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Why work more in a boom?", r"How much do people change their hours when wages change?",
             "Chapter six. Why work more in a boom?", lit={1985: r"Hansen", 1988: r"Rogerson"},
             scale=("person", "nation"), horizon=("a quarter", "a year"))
        self.substitution()
        self.frisch()
        self.lottery()

    def substitution(self):
        rows = VGroup(
            label(r"hours worked swing almost as much as output: \ a model of the cycle must explain why",
                  font_size=23, color=HOURS),
            MathTex(r"u(c, n) = \log c - A\, \frac{n^{1 + 1/\varphi}}{1 + 1/\varphi}", font_size=38),
            label(r"a \emph{temporary} rise in the wage: \ work now, \ rest later, \ when work pays less",
                  font_size=23, color=E.ACCENT),
            label(r"intertemporal substitution: \ like a fisherman who fishes hardest when the fish are running",
                  font_size=22, color=GREY_A),
            label(r"$\varphi$, \ the Frisch elasticity: \ the \% change in hours per 1\% change in a temporary wage",
                  font_size=23, color=HOURS),
            label(r"a permanent rise does much less: \ richer people also want more leisure", font_size=22,
                  color=HOLD),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Lucas and Rapping, \ \emph{JPE} 77(5) (1969); \ Frisch (1932)", corner=DR, font_size=12)
        with self.voiceover(
            "The model so far has no labour. But in the data, hours worked swing almost as much as output, so a "
            "model of the cycle must say why people work more in booms. <bookmark mark='a'/> Give the household a "
            "dislike of working, n hours, with a parameter phi that sets how strongly the dislike rises with hours. "
            "<bookmark mark='b'/> In a boom, productivity and so the wage are temporarily high. The smart response "
            "is to work now and rest later, when work pays less. <bookmark mark='c'/> Robert Lucas and Leonard "
            "Rapping proposed this in 1969: it is the logic of a fisherman who fishes hardest when the fish are "
            "running. <bookmark mark='d'/> Phi measures it: the percentage change in hours for a one percent "
            "change in a temporary wage, called the Frisch elasticity after Ragnar Frisch. "
            "<bookmark mark='e'/> A permanent rise does much less, because people who are richer for good also "
            "want more leisure, and the two pulls roughly cancel."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def frisch(self):
        F = load("frisch")
        D = load("facts")["data"]
        rows = F["rows"]
        xs = [np.log2(r["frisch"]) for r in rows]
        ax = plane([-2.5, 4.0], [0, 1.0], center=LEFT * 2.0 + DOWN * 0.3, x_length=8.0, y_length=4.8,
                   xticks=[-2, -1, 0, 1, 2], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"Frisch elasticity $\varphi$ \ (log scale)", ylabel=r"hours' volatility relative to output",
                   xfmt=lambda v: f"{2 ** v:g}", yfmt=lambda v: f"{v:.2f}", font_size=15)
        pts = VGroup(*[dot(ax, x, r["n_rel"], HOURS, 0.08) for x, r in zip(xs, rows)])
        line = path(ax, xs, [r["n_rel"] for r in rows], HOURS, 3)
        data_l = seg(ax, -2.5, D["n"]["rel"], 4.0, D["n"]["rel"], OUTPUT, 2.5, dashed=True)
        data_t = label(rf"US data: \ {D['n']['rel']:.2f}", font_size=17, color=OUTPUT).next_to(
            ax.ax.c2p(-2.4, D["n"]["rel"]), UP, buff=0.08).align_to(ax.ax.c2p(-2.4, 0), LEFT)
        inf = dot(ax, 3.6, F["hansen"]["n_rel"], E.ACCENT, 0.1)
        inf_t = label(r"$\varphi = \infty$", font_size=17, color=E.ACCENT).next_to(inf, DOWN, buff=0.12)
        micro = Rectangle(width=ax.ax.c2p(np.log2(0.8), 0)[0] - ax.ax.c2p(np.log2(0.25), 0)[0], height=4.8,
                          fill_color=CONS, fill_opacity=0.12, stroke_width=0).move_to(
            ax.ax.c2p((np.log2(0.25) + np.log2(0.8)) / 2, 0.5))
        side = VGroup(
            label(r"the Island's model, \\ solved again for each $\varphi$", font_size=19, color=HOURS),
            label(r"blue band: \ what studies of \\ individual workers find, \\ about 0.25 to 0.8", font_size=19,
                  color=CONS),
            label(rf"at $\varphi = 0.5$: \ hours move \\ {rows[1]['n_rel']:.2f} as much as output", font_size=19,
                  color=HOURS),
            label(rf"to get halfway to the data \\ needs $\varphi \approx {F['half']:.1f}$", font_size=19,
                  color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "How big is phi? Here is the whole model of this part, solved again for each value. "
            "<bookmark mark='a'/> Across the bottom, the Frisch elasticity, on a log scale; up the side, how much "
            "hours move relative to output. <bookmark mark='b'/> In the data, hours move "
            f"{D['n']['rel']:.2f} times as much as output. <bookmark mark='c'/> Studies of individual workers find "
            "elasticities somewhere around a quarter to four fifths: the blue band. <bookmark mark='d'/> With phi at "
            f"a half, the model's hours move only {rows[1]['n_rel']:.2f} times as much as output: a cycle in which "
            "hardly anyone changes how much they work. <bookmark mark='e'/> To get even halfway to the data, the "
            f"model needs phi of about {F['half']:.1f}, far above what workers' own records show. This is the "
            "central weakness of the theory, and the next idea is the attempt to fix it."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=0.6)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromCenter(p) for p in pts], lag_ratio=0.2), Create(line), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(data_l), FadeIn(data_t))
            vo.wait_until("c")
            self.play(FadeIn(micro), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(Indicate(pts[1], color=WHITE), FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]), GrowFromCenter(inf), FadeIn(inf_t))
        self.clear_scene()

    def lottery(self):
        F = load("frisch")
        D = load("facts")["data"]
        rng = np.random.default_rng(4)
        n_people = 60
        grid = VGroup(*[Circle(radius=0.13, stroke_width=0, fill_color=GREY_D, fill_opacity=1)
                        for _ in range(n_people)]).arrange_in_grid(rows=6, cols=10, buff=0.18)
        grid.move_to(LEFT * 3.6 + DOWN * 0.4)
        order = rng.permutation(n_people)
        normal = set(order[:36].tolist())
        boom = set(order[:40].tolist())
        slump = set(order[:31].tolist())

        def colour(on):
            return [c.animate.set_fill(HOURS if i in on else GREY_D) for i, c in enumerate(grid)]

        side = VGroup(
            label(r"Rogerson, \ 1988: \ most jobs are a full shift or nothing", font_size=20, color=E.ACCENT),
            label(r"so the economy adjusts by \emph{how many} people work, \\ not how long each works",
                  font_size=20, color=HOURS),
            label(r"with insurance against not being picked, \\ the economy behaves as if one household had \\ an "
                  r"infinite Frisch elasticity", font_size=20, color=GREY_A),
            label(rf"Hansen, \ 1985: \ hours now move {F['hansen']['n_rel']:.2f} as much as output \\ (data: "
                  rf"{D['n']['rel']:.2f})", font_size=20, color=OUTPUT),
            label(r"each person's elasticity is zero; \ the economy's is infinite", font_size=20, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Rogerson, \ \emph{JME} 21(1) (1988); \ Hansen, \ \emph{JME} 16(3) (1985)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Richard Rogerson and Gary Hansen found a way around the problem. <bookmark mark='a'/> Most jobs come as "
            "a full shift or nothing: you work forty hours a week or you do not work. <bookmark mark='b'/> So "
            "an economy adjusts mostly by changing how many people work, not how long each person works. Here are "
            "sixty people in a normal quarter. In a boom, a few more are at work; in a slump, a few fewer. "
            "<bookmark mark='c'/> Rogerson showed that if people can insure themselves against being the one who "
            "is not hired, the whole economy behaves as if a single household had an infinite Frisch elasticity. "
            "<bookmark mark='d'/> Hansen put this into the growth model in 1985, and hours now move "
            f"{F['hansen']['n_rel']:.2f} times as much as output, against {D['n']['rel']:.2f} in the data. "
            "<bookmark mark='e'/> Each person's elasticity is zero, and the economy's is infinite. The Island uses "
            "Hansen's version from here on. Whether this is a solution or a trick is still argued, and it is this "
            "part's dial."
        ) as vo:
            self.play(FadeIn(grid), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), *colour(normal), run_time=1.0)
            self.play(*colour(boom), run_time=0.8)
            self.play(*colour(slump), run_time=0.8)
            self.play(*colour(normal), run_time=0.8)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
