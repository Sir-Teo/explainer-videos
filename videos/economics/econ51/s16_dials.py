from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ51.common import *  # noqa: F403

GAM = ("#7EC8F5", "#FFFFFF", "#F2A65A")


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 14, r"The Dials: \ parameters against method error", r"Which matters more: the method or the "
                                                                          r"numbers fed to it?",
             "Chapter fourteen. The Dials: parameters against method error.",
             lit={2002: r"Vissing-Jorgensen", 2015: r"Havranek"}, scale=("household", "nation"),
             horizon=("a century",))
        self.eis()
        self.compare()

    def eis(self):
        dial = dials.DIALS["eis"]
        head = status_head(dial, r"the elasticity of intertemporal substitution")
        frame, rows = dial_rows(dial, -0.2, 2.2, [0, 0.5, 1.0, 1.5, 2.0], r"percent change in consumption growth "
                                                                          r"per point of interest", top=2.2,
                                step=0.5, fmt="{:.2f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 11.2, 15, GREY_A).to_edge(DOWN, buff=0.35)
        tag = published_tag(r"explainer.economics.dials, \ checked 2026-11-19", corner=UR, font_size=12)
        with self.voiceover(
            "Every solver in this part was fed numbers: a discount factor, a capital share, and an elasticity of "
            "intertemporal substitution of a half. The last is one of the Dials, from Part seven. <bookmark "
            "mark='a'/> Robert Hall found it near zero in aggregate data; <bookmark mark='b'/> surveys of "
            "hypothetical choices, about 0.2; <bookmark mark='c'/> Annette Vissing-Jorgensen, about a third for "
            "stockholders <bookmark mark='d'/> and nearly one for bondholders; <bookmark mark='e'/> Jonathan Gruber, "
            "from tax variation, about two; <bookmark mark='f'/> Tomas Havranek's meta-analysis, near zero in macro "
            "data <bookmark mark='g'/> and about a third in micro data; <bookmark mark='h'/> and asset-pricing "
            "models assume one and a half. <bookmark mark='z'/> Contested, across a factor of ten or more."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Indicate(rows[0], color=WHITE, scale_factor=1.02))
            for mk, r in zip("bcdefgh", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r), run_time=0.6)
            vo.wait_until("z")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()

    def compare(self):
        D = load("dials")["rows"]
        A = load("accuracy")
        Gr = load("grids")
        best = min(r["max"] for r in A["table"])
        bars = VGroup()
        items = [(rf"EIS {1 / r['gamma']:.2f}: \ consumption {r['diff_pct']:+.1f}\%".replace("-", "{-}")
                  if abs(r["diff_pct"]) > 1e-9 else rf"EIS {1 / r['gamma']:.2f}: \ the film's value",
                  abs(r["diff_pct"]), col) for r, col in zip(D, GAM)]
        items += [(r"a good method's error", 100 * 10 ** best, PROJ),
                  (r"a 30-point grid's steady state", 100 * (1 - Gr["rows"][0]["steady"]), ERR)]
        ax = plane([-6, 1.5], [0, len(items)], center=RIGHT * 1.4 + DOWN * 0.3, x_length=6.4, y_length=4.4,
                   xticks=[-6, -4, -2, 0, 1], yticks=[], xlabel=r"size, \ percent, \ $\log_{10}$",
                   xfmt=lambda v: f"{v:.0f}", font_size=14)
        for i, (name, v, col) in enumerate(items):
            y = len(items) - 1 - i + 0.5
            if v <= 0:
                nm = label(name, font_size=16, color=col).next_to(ax.ax.c2p(-6, y), LEFT, buff=0.15)
                bars.add(VGroup(nm))
                continue
            p0, p1 = ax.ax.c2p(-6, y - 0.3), ax.ax.c2p(np.log10(v), y + 0.3)
            b = Rectangle(width=max(p1[0] - p0[0], 0.02), height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to((p0 + p1) / 2)
            nm = label(name, font_size=16, color=col).next_to(ax.ax.c2p(-6, y), LEFT, buff=0.15)
            bars.add(VGroup(b, nm))
        head = label(r"consumption at 80\% of the steady-state capital: \ what moves it, \ and by how much",
                     font_size=21, color=WHITE).to_edge(UP, buff=0.5)
        foot = label(r"a good method's error is lost in the parameters' uncertainty; \ a bad method's is not",
                     font_size=20, color=E.ACCENT).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Now set the two kinds of uncertainty side by side, on a log scale. Take consumption when capital is "
            "eighty percent of its steady state. <bookmark mark='a'/> Change the elasticity of substitution from "
            f"the film's half to one, and consumption changes by {abs(D[0]['diff_pct']):.0f} percent; to a "
            f"quarter, by {abs(D[2]['diff_pct']):.0f} percent the other way. <bookmark mark='b'/> A good method's "
            "error is about a hundred thousand times smaller: lost entirely in the uncertainty about the parameter. "
            "<bookmark mark='c'/> But a careless one, the thirty-point grid of chapter three, gets the steady state "
            f"wrong by {100 * (1 - Gr['rows'][0]['steady']):.0f} percent, as large as the whole dispute about the "
            "parameter. <bookmark mark='d'/> So a method need not be perfect, only good enough that its error is "
            "small beside what we do not know about the economy; and only measuring shows which side of that line "
            "it is on."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax))
            vo.wait_until("a")
            self.play(*[FadeIn(b) for b in bars[:3]], run_time=1.4)
            vo.wait_until("b")
            self.play(FadeIn(bars[3]))
            vo.wait_until("c")
            self.play(FadeIn(bars[4]))
            vo.wait_until("d")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()
