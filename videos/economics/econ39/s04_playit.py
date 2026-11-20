from __future__ import annotations

from videos.economics.econ39.common import *  # noqa: F403

SHORT = {"managers": r"managers", "professionals": r"professionals", "financial sales": r"financial sales",
         "retail sales": r"retail sales", "clerical and administrative": r"clerical and \\ administrative",
         "food preparation and service": r"food preparation \\ and service", "health service aides": r"health aides",
         "building and grounds": r"cleaning and \\ grounds keeping", "child care": r"child care",
         "precision production": r"skilled \\ production crafts",
         "machine operators and assemblers": r"machine operators \\ and assemblers",
         "transport and material moving": r"drivers and \\ material movers"}


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Play it: \ what happened to twelve kinds of work",
             r"Which grew and which shrank, \ 1980--2005?", "Chapter three. Play it: what happened to twelve kinds "
             "of work.", lit={2013: r"Autor and Dorn"}, scale=("nation",), horizon=("a decade",))
        self.choose()
        self.reveal()
        self.why()

    def _tiles(self, game, colours=None):
        tiles = VGroup()
        for k, g in enumerate(game):
            col = colours[k] if colours else GREY_B
            box = RoundedRectangle(width=2.85, height=1.05, corner_radius=0.1, stroke_color=col, stroke_width=2.2,
                                   fill_color="#141821", fill_opacity=1)
            tiles.add(VGroup(box, label(SHORT[g], font_size=19, color=WHITE).move_to(box)))
        tiles.arrange_in_grid(rows=3, cols=4, buff=(0.3, 0.3))
        return tiles

    def choose(self):
        P = load("polar")
        tiles = self._tiles(P["game"]).move_to(DOWN * 0.1)
        q = wrapped_label(r"Between 1980 and 2005, \ which of these twelve kinds of work grew as a share of American "
                          r"jobs, \ and which shrank?", 12.0, 26, E.ACCENT).to_edge(UP, buff=0.5)
        ring = countdown().scale(0.7).next_to(tiles, DOWN, buff=0.4)
        tag = data_tag(r"Autor and Dorn (2013), \ replication data", corner=DR, font_size=12)
        with self.voiceover(
            "Your turn. Here are twelve kinds of work, from managers to machine operators, from health aides to "
            "clerks. <bookmark mark='a'/> Between 1980 and 2005, computers spread through American offices and "
            "factories. Which of these grew as a share of all jobs, and which shrank? Sort them in your head into "
            "growers and shrinkers, and guess which shrank most. Pause, and choose."
        ) as vo:
            self.play(FadeIn(q), FadeIn(tag), LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in tiles],
                                                          lag_ratio=0.12), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.clear_scene()

    def reveal(self):
        P = load("polar")
        G, order = P["groups"], P["order"]
        bars = VGroup()
        x0, scale = -0.4, 4.6
        for k, g in enumerate(order):
            v = G[g]["change"]
            y = 2.75 - 0.46 * k
            col = GAIN if v > 0 else LOSS
            w = abs(v) * scale
            r = Rectangle(width=w, height=0.34, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([x0 + (w / 2 if v > 0 else -w / 2), y, 0]))
            nm = label(SHORT[g].replace(r" \\ ", " "), font_size=17, color=WHITE)
            if v > 0:
                nm.next_to(np.array([x0, y, 0]), LEFT, buff=0.15)
            else:
                nm.next_to(np.array([x0 - w, y, 0]), LEFT, buff=0.15)
            val = label(f"{100 * v:+.0f}\\%", font_size=16, color=col).next_to(r, RIGHT if v > 0 else LEFT,
                                                                            buff=0.1)
            if v < 0:
                val.next_to(np.array([x0, y, 0]), RIGHT, buff=0.1)
            bars.add(VGroup(r, nm, val))
        axis = Line(np.array([x0, 3.05, 0]), np.array([x0, 3.05 - 0.46 * 12, 0]), color=GREY_B, stroke_width=2)
        head = label(r"change in each one's share of American jobs, \ 1980--2005", font_size=22,
                     color=E.ACCENT).to_edge(UP, buff=0.25)
        side = label(r"the shrinkers: \\ factory, \ office \\ and craft work \\ in the middle \\ of the pay scale",
                     font_size=19, color=LOSS).to_edge(RIGHT, buff=0.4).shift(DOWN * 1.6)
        tag = data_tag(r"Autor and Dorn (2013), \ census and ACS data, \ 1980--2005", corner=DR, font_size=12)
        shrink = [g for g in order if G[g]["change"] < 0]
        with self.voiceover(
            "Here is what happened. <bookmark mark='a'/> The biggest loser: machine operators and assemblers, whose "
            f"share of jobs fell by {say_pct(-G[order[0]]['change'], 0)}. Skilled "
            f"production crafts fell {say_pct(-G[order[1]]['change'], 0)}; clerical work and driving fell too. "
            "<bookmark mark='b'/> The growers sit at both ends of the pay scale: professionals, managers and "
            "financial sales at the top, and at the bottom child care, health aides, food service and cleaning. "
            f"<bookmark mark='c'/> {len(shrink)} of the twelve shrank, and they share one thing: in 1980 they paid "
            "middling wages, for work that followed rules."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axis), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=LEFT * 0.1) for b in bars[:len(shrink)]], lag_ratio=0.3),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in bars[len(shrink):]], lag_ratio=0.2),
                      run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(side))
        self.clear_scene()

    def why(self):
        P = load("polar")
        G = P["groups"]
        ax = plane([1.6, 3.0], [-0.7, 0.8], center=LEFT * 1.5 + DOWN * 0.4, x_length=8.0, y_length=4.8,
                   xticks=[1.8, 2.2, 2.6, 3.0], yticks=[-0.6, -0.3, 0, 0.3, 0.6],
                   xlabel=r"mean log hourly wage in 1980", ylabel=r"change in share of jobs, \ 1980--2005",
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{100 * v:+.0f}\\%", font_size=14)
        zero = seg(ax, 1.6, 0, 3.0, 0, GREY_B, 1.5, dashed=True)
        pts, cols = VGroup(), []
        rk = sorted(P["game"], key=lambda g: -G[g]["rti"])
        for g in P["game"]:
            v, w = G[g]["change"], G[g]["wage1980"]
            k = rk.index(g)
            cols.append(LOSS if k < 4 else (MIDS if k < 8 else GAIN))
            side_ = {"retail sales": UL, "clerical and administrative": LEFT, "transport and material moving": DR,
                     "building and grounds": DOWN}.get(g, UP)
            pts.add(VGroup(dot(ax, w, v, GREY_B, 0.1), label(SHORT[g].replace(r" \\ ", " "), font_size=13,
                                                             color=GREY_A).next_to(ax.ax.c2p(w, v), side_,
                                                                                   buff=0.08)))
        side = VGroup(
            label(r"colour: \ how routine \\ the work was in 1980", font_size=17, color=WHITE),
            label(r"red: \ the four most routine", font_size=17, color=LOSS),
            label(r"green: \ the four least routine", font_size=17, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"Autor and Dorn (2013): \ routine task intensity", corner=DR, font_size=12)
        with self.voiceover(
            "Plot the same twelve against their pay in 1980. <bookmark mark='a'/> The losses cluster in the middle "
            "of the pay scale; gains are at the low end and the high end. <bookmark mark='b'/> Now colour each by "
            "how routine its tasks were, a measure built from the government's job descriptions: how much of the "
            "work follows explicit rules a machine could be programmed to follow. The most routine work, clerical "
            "jobs and machine operating, shrank most. But routineness is a tendency, not a law: food service counts "
            "as fairly routine and still grew, and driving counts as hardly routine and still shrank. The next "
            "chapter builds the idea properly."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_[0], scale=1.4) for p_ in pts], lag_ratio=0.1),
                      LaggedStart(*[FadeIn(p_[1]) for p_ in pts], lag_ratio=0.1), run_time=2.5)
            vo.wait_until("b")
            self.play(*[p_[0].animate.set_color(c) for p_, c in zip(pts, cols)], FadeIn(side), run_time=1.5)
        self.clear_scene()
