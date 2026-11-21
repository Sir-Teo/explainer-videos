from __future__ import annotations

from videos.economics.econ68.common import *  # noqa: F403

STATUS_COL = {"settled within a range": TRUE, "depends on the setting": DATA, "contested": TOLL,
              "not identified": GREY_B}
ORDER = ("settled within a range", "depends on the setting", "contested", "not identified")
ROMAN = ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII")


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 12, r"The Dials, \ final", r"Across sixty-eight parts, \ what is settled, \ what depends on the "
             r"setting, \ and what is still contested?", "Chapter twelve. The Dials, final.", scale=("world",),
             horizon=("a century",))
        self.by_act()
        self.calls()

    def by_act(self):
        D = load("dials")
        ba = {int(k): v for k, v in D["by_act"].items()}
        ax = plane([0, 12], [0, 18], center=LEFT * 1.4 + DOWN * 0.3, x_length=9.0, y_length=4.6, xticks=[],
                   yticks=[0, 6, 12, 18], ylabel=r"Dials opened in the act", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        stacks = VGroup()
        for a in range(1, 13):
            base = 0
            g = VGroup()
            for s_ in ORDER:
                n = ba.get(a, {}).get(s_, 0)
                if n:
                    p0, p1 = ax.ax.c2p(a - 0.85, base), ax.ax.c2p(a - 0.15, base + n)
                    g.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0.6,
                                    stroke_color=BACKGROUND, fill_color=STATUS_COL[s_], fill_opacity=0.85)
                          .move_to((p0 + p1) / 2))
                base += n
            stacks.add(g)
        xl = VGroup(*[label(ROMAN[a - 1], font_size=15, color=GREY_A).next_to(ax.ax.c2p(a - 0.5, 0), DOWN, buff=0.12)
                      for a in range(1, 13)])
        key = legend_rows([(STATUS_COL[s_], f"{s_}: {D['statuses'].get(s_, 0)}") for s_ in ORDER],
                          font_size=15).next_to(ax.ax, RIGHT, buff=0.35).shift(UP * 1.2)
        foot = label(rf"{D['n']} Dials, \ {D['estimates']} estimates", font_size=20, color=E.ACCENT).next_to(
            key, DOWN, buff=0.5).align_to(key, LEFT)
        tag = published_tag(r"explainer/economics/dials.py", corner=DL, font_size=12)
        settled = D["statuses"].get("settled within a range", 0)
        with self.voiceover(
            "The Dials, for the last time. <bookmark mark='a'/> Each act opened Dials as it met numbers the world "
            "has to supply, stacked here by act and coloured by status. <bookmark mark='b'/> Of the "
            f"{D['n']}, {settled} are settled within a range, {D['statuses'].get('depends on the setting', 0)} "
            f"depend on the setting, {D['statuses'].get('contested', 0)} are contested and "
            f"{D['statuses'].get('not identified', 0)} cannot be identified with the data we have. <bookmark "
            "mark='c'/> Settled answers are rare in every act, never more than two Dials in three and usually far "
            "fewer; the acts on markets and on money and the cycle are the most contested, and the graduate core "
            "opened none, since it built tools rather than measured the world. Most of what economics measures depends "
            "on where and when it is measured, and saying so is not a failure of the field but its main finding."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(xl), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_, shift=UP * 0.1) for s_ in stacks], lag_ratio=0.15), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(key), FadeIn(foot))
            vo.wait_until("c")
            self.play(*[Indicate(stacks[k], color=WHITE, scale_factor=1.03) for k in (2, 5)])
        self.clear_scene()

    def calls(self):
        C = load("calls")
        v = C["verdicts"]
        order = (("right", TRUE), ("partly right", DATA), ("wrong", TOLL), ("too early to say", GREY_B))
        tot = sum(v.values())
        bar = VGroup()
        x0 = -6.0
        for k, col in order:
            w = 12.0 * v.get(k, 0) / tot
            bar.add(Rectangle(width=w, height=0.8, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                [x0 + w / 2, 1.2, 0]))
            x0 += w
        labs = VGroup(*[label(rf"{k}: \ {v.get(k, 0)}", font_size=18, color=col).next_to(b, DOWN, buff=0.15)
                        for b, (k, col) in zip(bar, order)])
        head = label(rf"Called it? \ {C['n']} predictions, \ made in advance, \ scored", font_size=28,
                     color=E.ACCENT).to_edge(UP, buff=0.6)
        rows = VGroup(
            label(r"wrong is the commonest verdict; \ fewer than one call in five was simply right", font_size=20,
                  color=GREY_A),
            label(r"the lesson for anyone who forecasts: \ say a range, \ and keep score", font_size=20,
                  color=TRUE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(labs, DOWN, buff=0.7)
        tag = published_tag(r"explainer/economics/calls.py", corner=DL, font_size=12)
        with self.voiceover(
            f"And the series' other ledger: Called it? <bookmark mark='a'/> {C['n']} predictions made in advance "
            f"by economists, officials and markets, each put beside what happened. <bookmark mark='b'/> "
            f"{v.get('right', 0)} were right, {v.get('partly right', 0)} partly right, {v.get('wrong', 0)} wrong, "
            f"and {v.get('too early to say', 0)} are too early to say. <bookmark mark='c'/> Wrong is the commonest "
            "verdict, and fewer than one call in five was simply right. The lesson is not that economists should "
            "stop forecasting, but that a forecast should come with a range, and someone should keep score."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in bar], lag_ratio=0.3), FadeIn(labs), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows))
        self.clear_scene()
