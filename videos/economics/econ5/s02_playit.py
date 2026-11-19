from __future__ import annotations

from videos.economics.econ5.common import *  # noqa: F403


def mini_panel(A: float, B: float, k: int, size: float = 1.45):
    """One small budget: axes to 12, the line from A fish to B coconuts, its number and its two ends."""
    from explainer.ai.viz import axes

    ax = axes([0, 13], [0, 13], x_length=size, y_length=size, xticks=None, yticks=None, font_size=12)
    a = ax.ax
    ln = Line(a.c2p(A, 0), a.c2p(0, B), color=BUDGET, stroke_width=3)
    num = label(str(k), font_size=20, color=E.ACCENT).move_to(a.c2p(10.5, 11.5))
    ends = VGroup(label(rf"{A:g}", font_size=14, color=FISHC).next_to(a.c2p(A, 0), DOWN, buff=0.06),
                  label(rf"{B:g}", font_size=14, color=COCO).next_to(a.c2p(0, B), LEFT, buff=0.06))
    g = VGroup(ax, ln, num, ends)
    g.ax, g.line = ax, ln
    return g


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Play it: \ eleven budgets", r"What would you buy, eleven times over?",
             "Chapter one. Play it: eleven budgets.")
        self.example()
        self.choose()

    def example(self):
        L = load("budgets")["lines"]
        ax = goods_axes(center=LEFT * 2.8 + DOWN * 0.2, top=13)
        a = ax.ax
        A, B = L[0]
        ln = budget_line(ax, A, B)
        dots = VGroup(*[Dot(a.c2p(x, B - B / A * x), radius=0.08, color=WHITE) for x in (1.0, 3.0, 5.0)])
        lab = VGroup(label(rf"\${INCOME:.0f}: \ {A:g} fish, \ or {B:g} coconuts, \\ or any mix on the line",
                           font_size=24, color=BUDGET),
                     label(rf"fish \${INCOME / A:.0f} each, \ coconuts \${INCOME / B:.0f} each", font_size=22,
                           color=GREY_A),
                     label(r"you write down how many fish; \\ the rest of the money buys coconuts", font_size=24),
                     label(r"there is no right answer: \\ only answers that fit together, or don't", font_size=24,
                           color=E.ACCENT)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.6)
        lab.shift(DOWN * 0.4)
        tag = island_tag(r"the Island market: fish and coconuts", corner=DR, font_size=15)
        intro = label(rf"a game: \ eleven trips to the market, \ \${INCOME:.0f} each", font_size=30,
                      color=E.ACCENT).to_edge(UP, buff=0.4).to_edge(RIGHT, buff=0.6)
        with self.voiceover(
            "Before any theory, a game. You'll go shopping eleven times at the Island market, with sixty dollars "
            f"each time. <bookmark mark='a'/> On the first trip, fish and coconuts both cost ten dollars, so you "
            "can buy six fish, or six coconuts, or any mix on this line. <bookmark mark='b'/> Pick a point on the "
            "line: say how many fish you'd buy, and the rest of the money goes on coconuts. "
            "<bookmark mark='c'/> On each trip the prices change, so the line changes. There's no right answer. "
            "The only question, which we'll come back to in chapter eight, is whether your eleven answers fit "
            "together."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(intro))
            vo.wait_until("a")
            self.play(Create(ln), FadeIn(lab[0]), FadeIn(lab[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.3), FadeIn(lab[2]))
            vo.wait_until("c")
            self.play(FadeIn(lab[3]))
        self.clear_scene()

    def choose(self):
        L = load("budgets")["lines"]
        stage = game_stage(13.2, 7.0, center=DOWN * 0.05)
        panels = VGroup(*[mini_panel(A, B, k + 1) for k, (A, B) in enumerate(L)])
        sheet = VGroup(label(r"your sheet", font_size=20, color=E.ACCENT),
                       label(r"1: \ \_\_ fish \\ 2: \ \_\_ fish \\ $\cdots$ \\ 11: \ \_\_ fish", font_size=17,
                             color=GREY_A)).arrange(DOWN, buff=0.12)
        cells = VGroup(*panels, sheet)
        cells.arrange_in_grid(rows=3, cols=4, buff=(0.45, 0.35))
        cells.move_to(stage.box.get_center() + LEFT * 2.0 + DOWN * 0.15)
        side = VGroup(label(r"eleven trips, \ \$60 each", font_size=26, color=E.ACCENT),
                      label(r"the numbers at the ends: \\ the most fish (across), \\ or the most coconuts (up)",
                            font_size=20, color=GREY_A),
                      label(r"how many fish \\ on each line?", font_size=28)).arrange(DOWN, aligned_edge=LEFT,
                                                                                     buff=0.35)
        side.move_to(stage.box.get_center() + RIGHT * 4.6 + UP * 1.0)
        ring = countdown().next_to(side, DOWN, buff=0.45)
        site = label(r"or play it on the course site, \\ which scores you as you go", font_size=18,
                     color=GREY_B).next_to(ring, DOWN, buff=0.3)
        with self.voiceover(
            "Here are all eleven. <bookmark mark='a'/> Each line is one trip. The number at the bottom is the most "
            "fish you could buy, and the number on the left the most coconuts. Some trips make fish cheap, some "
            "make coconuts cheap, some make everything dear. <bookmark mark='b'/> Pause the film, and on each line "
            "write down how many fish you'd buy. Take your time, and buy what you'd actually want. "
            "<bookmark mark='c'/> Keep the sheet. Chapter eight will score it."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p, scale=0.9) for p in panels], lag_ratio=0.12), FadeIn(side[1]),
                      run_time=2.6)
            vo.wait_until("b")
            self.play(FadeIn(side[2]), FadeIn(sheet), FadeIn(ring), FadeIn(site))
            vo.wait_until("c")
            self.play(Indicate(sheet, color=E.ACCENT))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=5.0, rate_func=linear)
        self.clear_scene()
