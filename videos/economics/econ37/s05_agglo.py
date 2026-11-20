from __future__ import annotations

from videos.economics.econ37.common import *  # noqa: F403


class Agglo(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Why cities exist", r"What do people gain from crowding together?",
             "Chapter four. Why cities exist.", lit={1890: r"Marshall", 2004: r"Duranton and Puga"},
             scale=("firm", "city"), horizon=("a decade",))
        self.forces()
        self.sorting()
        self.movers()

    def forces(self):
        q = quote_card(r"The mysteries of the trade become no mysteries; \ but are as it were in the air, \ and "
                       r"children learn many of them unconsciously.",
                       r"Alfred Marshall, \ \emph{Principles of Economics} (1890), \ Book IV, \ ch.\ 10", width=11.0,
                       font_size=24).to_edge(UP, buff=0.4)
        cards = point_cards([
            (r"sharing", r"one big airport, \\ suppliers and \\ specialists \\ for many firms", CITY),
            (r"matching", r"a larger market \\ pairs workers \\ and jobs better, \\ and faster", WAGE),
            (r"learning", r"ideas spread \\ face to face; \\ young workers \\ learn by watching", AMENITY),
        ], width=12.0, cols=3, font_size=20).next_to(q, DOWN, buff=0.45)
        foot = label(r"against them: \ rents, \ commutes and congestion", font_size=20, color=RENT).to_edge(
            DOWN, buff=0.45)
        tag = published_tag(r"Marshall (1890); \ Duranton and Puga, \ \emph{Handbook of Regional and Urban "
                            r"Economics} vol.\ 4 (2004)", corner=DR, font_size=11)
        with self.voiceover(
            "Why pay those rents? Alfred Marshall wrote in 1890 that where a trade gathers, its mysteries become "
            "no mysteries, but are as it were in the air. Gilles Duranton and Diego Puga sorted the reasons into "
            "three. <bookmark mark='a'/> Sharing: a big city supports one large airport, specialised suppliers and "
            "lawyers that many firms use. <bookmark mark='b'/> Matching: in a thick labour market workers find jobs "
            "that suit them, and firms find workers, better and faster. <bookmark mark='c'/> Learning: ideas spread "
            "face to face, and young workers learn by watching the best. <bookmark mark='d'/> Against them stand the "
            "rents, the commutes and the congestion of the last chapter. A city is as large as the balance allows."
        ) as vo:
            self.play(FadeIn(q), FadeIn(tag))
            for mk, c in zip("abc", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def sorting(self):
        A = load("agglo")
        d, w, n = np.array(A["d"]), np.array(A["mean_w"]), np.array(A["count"])
        ax = plane([-2.6, 2.6], [-0.35, 0.35], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[-2, -1, 0, 1, 2], yticks=[-0.3, -0.15, 0, 0.15, 0.3],
                   xlabel=r"a town's density \ (log, \ relative to the average)",
                   ylabel=r"the town's average wage \ (log)", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.2f}",
                   font_size=14)
        pts = VGroup(*[Dot(ax.ax.c2p(x, y), radius=0.035 + 0.05 * np.sqrt(k / n.max()), color=CITY,
                           fill_opacity=0.85) for x, y, k in zip(d, w, n) if k > 0])
        b0 = float(np.mean(w[n > 0]) - A["naive"] * np.mean(d[n > 0]))
        naive = seg(ax, -2.5, b0 - 2.5 * A["naive"], 2.5, b0 + 2.5 * A["naive"], E.ACCENT, 3.0)
        truth = seg(ax, -2.5, b0 - 2.5 * A["gamma"], 2.5, b0 + 2.5 * A["gamma"], GAIN, 3.0, dashed=True)
        side = VGroup(
            label(rf"the slope across towns: \ {A['naive']:.3f}", font_size=20, color=E.ACCENT),
            label(rf"planted: \ {A['gamma']:.2f}", font_size=20, color=GAIN),
            label(r"abler workers choose \\ denser towns: \ the slope \\ mixes what a town does \\ with who lives "
                  r"there", font_size=18, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "How much more productive does density make a worker? The number economists want is the agglomeration "
            "elasticity. On the Island I planted it: doubling a town's density raises everyone's productivity by "
            f"about {100 * (2 ** A['gamma'] - 1):.0f} percent, an elasticity of {A['gamma']:.2f}. Each dot is one of "
            "sixty towns. <bookmark mark='a'/> Fit a line across towns and you find "
            f"{A['naive']:.3f}, nearly double the truth. <bookmark mark='b'/> The planted line is flatter. "
            "<bookmark mark='c'/> The trouble is sorting: abler workers choose denser towns, so dense towns pay more "
            "partly because of who lives there. Cities attract talent, and talent is not the same thing as "
            "productivity that a city creates."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(pts, lag_ratio=0.02), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(naive), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(truth), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def movers(self):
        A = load("agglo")
        C = A["cdgr"]
        dd, dw = np.array(A["mover_dd"]), np.array(A["mover_dw"])
        ax = plane([-4.5, 4.5], [-0.5, 0.5], center=LEFT * 3.2 + DOWN * 0.45, x_length=6.2, y_length=4.4,
                   xticks=[-4, -2, 0, 2, 4], yticks=[-0.5, -0.25, 0, 0.25, 0.5],
                   xlabel=r"change in density on moving \ (log)", ylabel=r"change in the mover's wage \ (log)",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.2f}", font_size=13)
        pts = VGroup(*[Dot(ax.ax.c2p(x, y), radius=0.025, color=WAGE, fill_opacity=0.6) for x, y in zip(dd, dw)
                       if abs(y) < 0.5])
        fit = seg(ax, -4.3, -4.3 * A["movers"], 4.3, 4.3 * A["movers"], E.ACCENT, 3.2)
        res = VGroup(
            label(rf"movers: \ {A['movers']:.3f} \ (planted {A['gamma']:.2f})", font_size=21, color=E.ACCENT),
            label(rf"{A['n_movers']:,} workers who moved: \\ the same person, \ two towns, \\ so ability cancels",
                  font_size=17, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(ax, UP, buff=0.3).align_to(ax, LEFT)
        bars = VGroup()
        rows = ((r"raw", C["raw"]), (r"worker effects", C["quality"]), (r"both corrections", C["both"]),
                (r"preferred", C["preferred"]))
        for k, (nm, v) in enumerate(rows):
            r = Rectangle(width=v * 60, height=0.38, stroke_width=0, fill_color=CITY if k else E.ACCENT,
                          fill_opacity=0.85)
            r.move_to(np.array([2.1 + v * 30, 0.9 - 0.7 * k, 0]))
            bars.add(VGroup(r, label(nm, font_size=16, color=GREY_A).next_to(r, LEFT, buff=0.15).align_to(
                np.array([2.0, 0, 0]), RIGHT), label(f"{v:.3f}".rstrip("0").rstrip("."), font_size=16,
                                                     color=WHITE).next_to(r, RIGHT, buff=0.1)))
        bh = label(r"France, \ 306 areas: \ the elasticity of wages to density", font_size=17,
                   color=GREY_A).next_to(bars, UP, buff=0.3)
        tag = published_tag(tables.CDGR_2010.tag + r"; \ the Island", corner=DR, font_size=12)
        with self.voiceover(
            "The cure is to follow the same people as they move. <bookmark mark='a'/> A worker who moves from a "
            "sparse town to a dense one keeps their ability, so the change in their wage measures what the town did. "
            f"On the Island the movers give {A['movers']:.3f}, close to the planted {A['gamma']:.2f}. "
            "<bookmark mark='b'/> Pierre-Philippe Combes, Gilles Duranton, Laurent Gobillon and Sébastien Roux did "
            "this with French wage records. The raw elasticity was about 0.05; following workers brought it to "
            f"{C['quality']:.3f}; their preferred estimate, {C['preferred']:.2f}. Real, but modest: doubling density "
            "raises wages by one or two percent. The rest of the big-city premium is who lives there."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(pts, lag_ratio=0.01), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(fit), FadeIn(res))
            vo.wait_until("b")
            self.play(FadeIn(bh), LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.1) for b_ in bars], lag_ratio=0.4),
                      run_time=2.0)
        self.clear_scene()
