from __future__ import annotations

from videos.economics.econ54.common import *  # noqa: F403

OPTIONS = (r"wealth just \\ before retirement", r"wealth in the \\ last years", r"consumption growth \\ while young",
           r"none of them \\ on its own")


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Play it: \ which fact pins down which parameter?", r"Can four facts tell patience from "
             r"caution?", "Chapter three. Play it: which fact pins down which parameter?",
             lit={2002: r"Gourinchas and Parker", 2017: r"Andrews, Gentzkow and Shapiro"}, scale=("household",),
             horizon=("a century",))
        self.ask()
        self.reveal()
        self.lesson()

    def ask(self):
        P = load("playit")
        rows = VGroup(
            label(r"the Island's households work 40 years, \ then live 10 on a pension; \ incomes are risky",
                  font_size=22, color=WHITE),
            label(r"patience, \ $\beta$: \ how much the future counts", font_size=22, color=PATIENCE),
            label(r"caution, \ $\gamma$: \ how much they dislike risk", font_size=22, color=CAUTION),
            label(r"both make people save more", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(UP, buff=0.6)
        q = label(r"Which of these facts tells patience apart from caution?", font_size=25,
                  color=E.ACCENT).next_to(rows, DOWN, buff=0.5)
        opts = VGroup()
        cols = (DATA, DATA, DATA, E.ACCENT)
        for t, c in zip(OPTIONS, cols):
            b = RoundedRectangle(width=2.9, height=1.0, corner_radius=0.1, stroke_color=c, stroke_width=2,
                                 fill_color=c, fill_opacity=0.1)
            opts.add(VGroup(b, label(t, font_size=18, color=c).move_to(b)))
        opts.arrange(RIGHT, buff=0.3).next_to(q, DOWN, buff=0.45)
        ring = countdown().scale(0.55).next_to(opts, DOWN, buff=0.35)
        del P
        with self.voiceover(
            "Your turn. <bookmark mark='a'/> The Island's households work for forty years on risky incomes, then "
            "live ten more on a pension. Two hidden numbers drive their saving. <bookmark mark='b'/> Patience, "
            "beta: how much the future counts against the present. <bookmark mark='c'/> And caution, gamma: how "
            "much they dislike risk. <bookmark mark='d'/> Both make people save more, so both raise wealth. "
            "<bookmark mark='e'/> You can measure four facts about them: wealth just before retirement, wealth in "
            "the last years, how fast consumption grows while they are young, and how it changes at retirement. "
            "Which fact tells patience apart from caution? Pause, and choose."
        ) as vo:
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(q), LaggedStart(*[FadeIn(o) for o in opts], lag_ratio=0.3), FadeIn(ring),
                      run_time=1.5)
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.play(FadeOut(ring))
        self.clear_scene()

    def reveal(self):
        P = load("playit")
        G = np.array(P["G"])
        names = [r"consumption growth while young", r"wealth just before retirement", r"wealth in the last years",
                 r"consumption's change at retirement"]
        head = VGroup(label(r"the fact", font_size=19, color=GREY_A),
                      label(r"patience $+0.01$", font_size=19, color=PATIENCE),
                      label(r"caution $+1$", font_size=19, color=CAUTION),
                      label(r"ratio", font_size=19, color=E.ACCENT))
        cells = [*head]
        for k, nm in enumerate(names):
            cells += [label(nm, font_size=19, color=DATA),
                      label(f"{0.01 * G[k, 0]:+.3f}".replace("-", "{-}"), font_size=20, color=PATIENCE),
                      label(f"{G[k, 1]:+.3f}".replace("-", "{-}"), font_size=20, color=CAUTION),
                      label(f"{0.01 * G[k, 0] / G[k, 1]:.2f}", font_size=20, color=E.ACCENT)]
        tab = VGroup(*cells).arrange_in_grid(rows=5, cols=4, buff=(0.6, 0.3), col_alignments="lccc").move_to(UP * 1.2)
        rule = Line(tab.get_corner(UL) + DOWN * 0.42, tab.get_corner(UR) + DOWN * 0.42, color=GREY_D,
                    stroke_width=1)
        ans = label(r"none on its own: \ every fact moves as if caution $+1$ were patience $+0.011$", font_size=23,
                    color=E.ACCENT).next_to(tab, DOWN, buff=0.6)
        note_ = label(r"how much each fact changes, \ in its own units, \ around the truth", font_size=18,
                      color=GREY_A).next_to(ans, DOWN, buff=0.35)
        with self.voiceover(
            "Here is how each fact moves. <bookmark mark='a'/> The first column: what a little more patience, one "
            "hundredth on beta, does to each fact. <bookmark mark='b'/> The second: what one more unit of caution "
            "does. <bookmark mark='c'/> Now compare them, row by row. They are almost the same. On every one of "
            "the four facts, one more unit of caution does what about one hundredth more patience does. <bookmark "
            "mark='d'/> So the answer is the last: none of them, on its own or together, separates the two. "
            "They all move along the same line, and any pair of values along that line explains them almost "
            "equally well."
        ) as vo:
            self.play(FadeIn(VGroup(*cells[:4])), Create(rule), *[FadeIn(c) for c in cells[4::4]])
            vo.wait_until("a")
            self.play(*[FadeIn(c) for c in cells[5::4]])
            vo.wait_until("b")
            self.play(*[FadeIn(c) for c in cells[6::4]])
            vo.wait_until("c")
            self.play(*[FadeIn(c) for c in cells[7::4]])
            vo.wait_until("d")
            self.play(FadeIn(ans, shift=UP * 0.1), FadeIn(note_))
        self.clear_scene()

    def lesson(self):
        P = load("playit")
        Sig = np.array(P["Sigma"])
        b0, g0 = P["truth"]
        ax = plane([b0 - 0.015, b0 + 0.015], [g0 - 1.5, g0 + 1.5], center=LEFT * 2.0 + DOWN * 0.3, x_length=6.4,
                   y_length=5.0, xticks=[b0 - 0.01, b0, b0 + 0.01], yticks=[g0 - 1, g0, g0 + 1],
                   xlabel=r"patience, \ $\beta$", ylabel=r"caution, \ $\gamma$", xfmt=lambda v: f"{v:.2f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        G = np.array(P["G"])
        cols = (DATA, PATIENCE, CAUTION, MODEL)
        lines = VGroup()
        for k in range(4):
            slope = -G[k, 0] / G[k, 1]
            xs = np.array([b0 - 0.015, b0 + 0.015])
            ys = g0 + slope * (xs - b0)
            lines.add(seg(ax, xs[0], ys[0], xs[1], ys[1], cols[k], 2.2))
        # the 95% region from all four facts, efficiently weighted
        w, V = np.linalg.eigh(Sig)
        t = np.linspace(0, 2 * np.pi, 120)
        r = np.sqrt(5.99)
        pts = [(b0 + r * (V[0, 0] * np.sqrt(w[0]) * np.cos(a) + V[0, 1] * np.sqrt(w[1]) * np.sin(a)),
                g0 + r * (V[1, 0] * np.sqrt(w[0]) * np.cos(a) + V[1, 1] * np.sqrt(w[1]) * np.sin(a))) for a in t]
        ell = Polygon(*[ax.ax.c2p(x, y) for x, y in pts], stroke_color=EST, stroke_width=2.5, fill_color=EST,
                      fill_opacity=0.15)
        truth = Cross(stroke_color=TRUTHC, stroke_width=3).scale(0.1).move_to(ax.ax.c2p(b0, g0))
        side = VGroup(
            label(r"each line: \ the values that \\ leave one fact unchanged", font_size=18, color=WHITE),
            label(r"gold: \ the 95\% region \\ from all four, \ weighted well", font_size=18, color=EST),
            label(r"to separate them, \ use variation \\ that moves one and not the other:", font_size=18,
                  color=E.ACCENT),
            label(r"households facing more \\ or less income risk; \\ different interest rates", font_size=18,
                  color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"simulated: \ the Island's households", corner=DR, font_size=13)
        with self.voiceover(
            "Draw it. <bookmark mark='a'/> Each line holds one fact fixed at its value in the data: every "
            "combination of patience and caution on it reproduces that fact. All four lines lie almost on top of "
            "each other. <bookmark mark='b'/> Put the four facts together, weight them well, and the region the "
            "data allow is this long thin sliver along the lines: patience is pinned to within a few thousandths, "
            "caution only to within about a unit either way, and the two errors move together. <bookmark "
            "mark='c'/> This is identification, the subject of Chapter 8. To tell two parameters apart you need "
            "variation in the data that moves one and not the other. <bookmark mark='d'/> Caution matters only "
            "where there is risk, so households facing more or less income risk would separate them; so would "
            "different interest rates. Pierre-Olivier Gourinchas and Jonathan Parker used the shape of the whole "
            "life-cycle profile; Isaiah Andrews, Matthew Gentzkow and Jesse Shapiro gave us a way to see which "
            "facts an estimate leans on."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(truth), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(ln) for ln in lines], lag_ratio=0.3), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(ell), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
