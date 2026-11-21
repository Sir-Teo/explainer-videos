from __future__ import annotations

from videos.economics.econ65.common import *  # noqa: F403

COLS = {"0.00": GREY_B, "0.50": TEXT, "0.75": MACH, "0.90": IDEA, "1.00": NAIVE}
LETTER = {"0.00": "A", "0.50": "B", "0.75": "C", "0.90": "D", "1.00": "E"}


def lab_row(share, n=20, w=0.42):
    """A research lab as a row of tasks: the first ``share`` of them done by machines (blue squares), the rest by
    people (pink circles)."""
    k = int(round(share * n))
    g = VGroup()
    for j in range(n):
        if j < k:
            m = Square(side_length=w * 0.8, stroke_color=MACH, stroke_width=2, fill_color=MACH, fill_opacity=0.35)
        else:
            m = Circle(radius=w * 0.42, stroke_color=WORK, stroke_width=2, fill_color=WORK, fill_opacity=0.35)
        g.add(m)
    return g.arrange(RIGHT, buff=0.1)


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Play it: \ automate the lab", r"If machines do more of the research, \ how fast does the "
             r"economy grow a century on?", "Chapter one. Play it: automate the lab.", scale=("nation", "world"),
             horizon=("a century",))
        self.stage()
        self.reveal()

    def stage(self):
        G = load("growth")
        head = label(r"an economy where ideas come from research tasks", font_size=26, color=GREY_A).to_edge(
            UP, buff=0.4)
        rows = VGroup()
        for b in G["shares"]:
            key = f"{b:.2f}"
            r = VGroup(label(LETTER[key], font_size=26, color=E.ACCENT), lab_row(b),
                       label(rf"{100 * b:.0f}\% of research tasks by machines", font_size=18, color=COLS[key]))
            r.arrange(RIGHT, buff=0.3)
            rows.add(r)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(DOWN * 0.2)
        key = legend_rows([(WORK, "a task done by researchers (their number grows 1% a year)"),
                           (MACH, "a task done by machines (as many as capital allows)")], font_size=16)
        key.to_edge(DOWN, buff=0.35)
        tag = island_tag(r"a model: \ semi-endogenous growth with automatable research \ (after Aghion, \ Jones "
                         r"and Jones); \ agora.automation.ideas\_growth", corner=DL, font_size=12)
        g0 = 100 * G["paths"]["0.00"]["growth"][100]
        with self.voiceover(
            "Your turn. Here is an economy whose growth comes from ideas, and ideas come from research. Research "
            "is a long list of tasks: <bookmark mark='a'/> designing, testing, checking, writing up. <bookmark "
            "mark='b'/> Each task can be done by researchers, whose number grows one percent a year with the "
            "population, or, once it is automated, by machines, of which there are as many as the economy's "
            "capital allows. The tasks are complements: every one of them has to be done. <bookmark mark='c'/> "
            f"With no automation the economy grows about {g0:.0f} percent a year per person, for ever. Now "
            "automate a share of the research tasks: none, half, three quarters, ninety percent, or all. "
            "<bookmark mark='d'/> For each, what is the growth rate a century from now?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(key))
            vo.wait_until("c")
            self.play(Indicate(rows[0], scale_factor=1.03))
            vo.wait_until("d")
        ring = countdown().scale(0.5).to_corner(DR, buff=0.3)
        self.play(FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.play(FadeOut(ring))
        self.wait(0.3)
        self.clear_scene()

    def reveal(self):
        G = load("growth")
        P = G["paths"]
        top = 26
        ax = plane([0, 200], [0, top], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.6, y_length=5.0,
                   xticks=[0, 50, 100, 150, 200], yticks=[0, 5, 10, 15, 20, 25], xlabel=r"years from now",
                   ylabel=r"growth of output per person, \ \% a year", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        lines = {k: path(ax, p["year"], [100 * g for g in p["growth"]], COLS[k], 3.0, yr=(0, top))
                 for k, p in P.items()}
        hund = vline(ax, 100, 0, top, GREY_C)
        side = VGroup()
        for k in ("0.00", "0.50", "0.75", "0.90", "1.00"):
            p = P[k]
            if p["exploded"]:
                txt = rf"{LETTER[k]}: \ {100 * float(k):.0f}\%: \ above 50\% a year by year {p['last_year']}"
            else:
                txt = (rf"{LETTER[k]}: \ {100 * float(k):.0f}\%: \ peak {100 * p['peak']:.0f}\% (year "
                       rf"{p['peak_year']}), \ year 100: \ {100 * p['at100']:.1f}\%")
            side.add(label(txt, font_size=15, color=COLS[k]))
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(ax.ax, RIGHT, buff=0.3).shift(UP * 1.2)
        if side.width > 4.3:
            side.scale_to_fit_width(4.3).next_to(ax.ax, RIGHT, buff=0.3).shift(UP * 1.2)
        lesson = label(r"while people do any essential task, \ that task sets the pace", font_size=20,
                       color=E.ACCENT).to_edge(DOWN, buff=0.3)
        tag = island_tag(r"computed: \ agora.automation.ideas\_growth", corner=DL, font_size=12)
        p5, p9, p1 = P["0.50"], P["0.90"], P["1.00"]
        with self.voiceover(
            "Here is what the model does. <bookmark mark='a'/> With no automation, growth stays near "
            f"{100 * P['0.00']['growth'][100]:.0f} percent. <bookmark mark='b'/> Automate half the tasks, and "
            f"growth jumps, to about {100 * p5['peak']:.0f} percent within {p5['peak_year']} years, because "
            "machines multiply as capital grows. Then it falls back. <bookmark mark='c'/> At three quarters, and "
            f"at ninety percent, the boom is bigger and longer: ninety percent reaches about {100 * p9['peak']:.0f} "
            f"percent a year around year {p9['peak_year']}. But a century on it is back to "
            f"{100 * p9['at100']:.0f} percent and still falling. <bookmark mark='d'/> Automate every task, and "
            f"growth does not fall back. It explodes, passing fifty percent a year by year {p1['last_year']}, "
            "where we stopped the model. <bookmark mark='e'/> The reason is the most important idea in this part. "
            "With complementary tasks, the ones machines cannot do become the bottleneck. As machines get cheap, "
            "the work left to people takes over the cost of research, and its slow growth sets the pace. Only "
            "when no task is left does the bottleneck disappear."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(hund), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(lines["0.00"]), FadeIn(side[0]), run_time=1.2)
            vo.wait_until("b")
            self.play(Create(lines["0.50"]), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(lines["0.75"]), FadeIn(side[2]), run_time=1.6)
            self.play(Create(lines["0.90"]), FadeIn(side[3]), run_time=2.0)
            vo.wait_until("d")
            self.play(Create(lines["1.00"]), FadeIn(side[4]), run_time=1.6)
            vo.wait_until("e")
            self.play(FadeIn(lesson))
        self.clear_scene()
