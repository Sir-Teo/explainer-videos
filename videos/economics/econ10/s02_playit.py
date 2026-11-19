from __future__ import annotations

from videos.economics.econ10.common import *  # noqa: F403


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Play it: \ set the fare for Bo's ferry", r"What fare would you charge for a crossing that costs "
             r"you nothing?", "Chapter one. Play it: set the fare for Bo's ferry.", horizon=("a day",))
        self.meet()
        self.choose()
        self.reveal()

    def values_axis(self, f, center=DOWN * 0.6):
        ax = plane([0, 100], [0, 10], center=center, x_length=10.5, y_length=3.4, xticks=[0, 25, 50, 75, 100],
                   yticks=[0, 2, 4, 6, 8, 10], xlabel=r"islanders, \ highest value first", ylabel=r"value of a crossing, "
                   r"\ \$", font_size=16)
        v = np.array(f["values"])
        bars = VGroup(*[Rectangle(width=0.085, height=max(ax.ax.c2p(0, x)[1] - ax.ax.c2p(0, 0)[1], 1e-3),
                                  stroke_width=0, fill_color=DEM, fill_opacity=0.8).move_to(ax.ax.c2p(k + 0.5, 0),
                                                                                            aligned_edge=DOWN)
                        for k, x in enumerate(v)])
        return ax, bars

    def meet(self):
        f = load("ferry")
        boat = ferry_glyph(2.0).to_edge(UP, buff=0.6).shift(LEFT * 4.2)
        bo = islander("bo", 1.0, name=True, font_size=20).next_to(boat, RIGHT, buff=0.3)
        ax, bars = self.values_axis(f)
        side = VGroup(
            label(r"Bo runs the ferry to the other island", font_size=24, color=BO),
            label(r"a hundred islanders would like to cross; \ each values it differently", font_size=22),
            label(r"the ferry sails anyway: \ one more passenger costs Bo nothing", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(bo, RIGHT, buff=0.5).align_to(boat, UP)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Back on the Island, Bo runs the ferry to the other island. <bookmark mark='a'/> A hundred islanders "
            "would like to cross. Each would pay something for it, but not the same amount: here is what a crossing "
            "is worth to each of them, from the most eager down. <bookmark mark='b'/> The ferry sails at the same "
            "times whoever is on it, so one more passenger costs Bo nothing. Like Dupuit's bridge."
        ) as vo:
            self.play(FadeIn(boat, shift=RIGHT * 0.3), FadeIn(bo), FadeIn(side[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(ax), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.01), FadeIn(side[1]),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def choose(self):
        f = load("ferry")
        stage = game_stage(12.0, 5.6, center=DOWN * 0.2)
        fares = VGroup()
        for r in f["rows"]:
            box = RoundedRectangle(width=1.9, height=1.3, corner_radius=0.12, stroke_color=E.ACCENT, stroke_width=2.5,
                                   fill_color=BLACK, fill_opacity=0.35)
            fares.add(VGroup(box, label(rf"\${r['fare']:.0f}", font_size=40, color=E.ACCENT).move_to(box)))
        fares.arrange(RIGHT, buff=0.35).move_to(stage.box.get_center() + UP * 0.5)
        q = label(r"which fare earns Bo the most?", font_size=30).next_to(fares, UP, buff=0.5)
        sub = label(r"a passenger crosses if the crossing is worth at least the fare", font_size=22, color=GREY_A
                    ).next_to(fares, DOWN, buff=0.35)
        ring = countdown().next_to(sub, DOWN, buff=0.4)
        with self.voiceover(
            "Bo charges one fare to everyone, and an islander crosses if the crossing is worth at least the fare. "
            "Here are five fares he is thinking about: two dollars, four, five, six, or eight. Which earns him the "
            "most? Pause, and choose."
        ):
            self.play(FadeIn(stage), FadeIn(q))
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in fares], lag_ratio=0.3), FadeIn(sub),
                      run_time=2)
            self.play(FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=6.0, rate_func=linear)
        self.clear_scene()

    def reveal(self):
        f = load("ferry")
        head = VGroup(*[label(t, font_size=21, color=GREY_A) for t in (r"fare", r"crossings", r"Bo's takings",
                                                                       r"value lost by those who stay")])
        rows = VGroup(head)
        best = max(f["rows"], key=lambda r: r["revenue"])
        for r in f["rows"]:
            col = PROFIT if r is best else WHITE
            rows.add(VGroup(label(rf"\${r['fare']:.0f}", font_size=24, color=col),
                            label(f"{r['cross']}", font_size=24, color=col),
                            label(rf"\${r['revenue']:.0f}", font_size=24, color=col),
                            label(rf"\${r['lost']:.0f}", font_size=24, color=DWL)))
        xs = (-6.6, -5.1, -3.3, -1.5)
        for k, row in enumerate(rows):
            for c, x in zip(row, xs):
                c.move_to([x, 2.3 - 0.55 * k, 0], aligned_edge=LEFT)
        ax = plane([0, 10], [0, 300], center=RIGHT * 4.5 + DOWN * 0.1, x_length=4.0, y_length=3.6,
                   xticks=[0, 5, 10], yticks=[0, 100, 200, 300], xlabel=r"fare, \ \$", ylabel=r"takings, \ \$",
                   font_size=15)
        curve = path(ax, f["grid"], f["revenue_curve"], color=PROFIT, width=3, smooth=False)
        peak = Dot(ax.ax.c2p(f["best_fare"], f["best_revenue"]), radius=0.07, color=PROFIT)
        notes = VGroup(
            label(rf"best of the five: \ \${best['fare']:.0f}, \ \${best['revenue']:.0f}; \ the very best fare, "
                  rf"\${f['best_fare']:.2f}, \ earns \${f['best_revenue']:.0f}", font_size=22, color=PROFIT),
            label(rf"at \${best['fare']:.0f}, \ {100 - best['cross']} islanders stay home, \\ though carrying them "
                  rf"would cost nothing: \ \${best['lost']:.0f} of value lost", font_size=22, color=DWL),
            label(r"a fare low enough to fill the ferry earns less, \ and wastes almost nothing", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.45).to_edge(LEFT, buff=0.6)
        with self.voiceover(
            "Here's what each fare does. <bookmark mark='a'/> At two dollars, eighty-two islanders cross and Bo "
            "takes a hundred and sixty-four dollars. At four, he takes two hundred and fifty-six. At five, two "
            "hundred and sixty: the best of the five. At six, fewer cross and he takes less; at eight, much less. "
            "<bookmark mark='b'/> Takings rise and then fall as the fare goes up, and the very best fare is about "
            "five dollars sixty, which earns two hundred and sixty-eight. <bookmark mark='c'/> But look at the "
            "last column. At five dollars, forty-eight islanders stay home, though carrying them would have cost "
            "nothing, and a hundred and twenty-five dollars of value is lost. <bookmark mark='d'/> A low fare that "
            "fills the ferry earns Bo less, but wastes almost nothing. That trade-off is the whole of this part."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r[:3]), shift=RIGHT * 0.1) for r in rows[1:]], lag_ratio=0.4),
                      run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(ax), Create(curve), FadeIn(peak), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r[3]) for r in rows[1:]], lag_ratio=0.2), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.clear_scene()
