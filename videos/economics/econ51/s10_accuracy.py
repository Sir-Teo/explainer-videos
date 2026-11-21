from __future__ import annotations

from videos.economics.econ51.common import *  # noqa: F403

FAMILY = {"value iteration": VFI, "between points": POLICY, "collocation": PROJ, "perturbation": PERT}


def _col(name):
    for k, c in FAMILY.items():
        if name.startswith(k):
            return c
    return WHITE


class Accuracy(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Accuracy: \ Euler-equation errors", r"How do you know a computed answer is right?",
             "Chapter eight. Accuracy: Euler-equation errors.",
             lit={1992: r"Judd", 1994: r"Den Haan and Marcet", 2006: r"Aruoba et al."}, scale=("nation",),
             horizon=("a century",))
        self.definition()
        self.table()
        self.tolerance()

    def definition(self):
        eq = MathTex(r"\mathcal{E}(k) \;=\; \left|\, 1 - \frac{u'^{-1}\!\big(\beta\, \mathbb{E}\,[\,u'(c(k'))\, "
                     r"R(k')\,]\big)}{c(k)} \,\right|", font_size=42, color=THEORY).move_to(UP * 1.7)
        rows = VGroup(
            label(r"the share of consumption the household would have to change \\ to satisfy its own first-order "
                  r"condition", font_size=22, color=WHITE),
            label(r"$\log_{10}\mathcal{E} = -3$: \ a mistake of one dollar in a thousand", font_size=22, color=ERR),
            label(r"unit-free, \ checkable at any point, \ needs no `true' answer", font_size=22, color=GAIN),
            label(r"for simulated series: \ Den Haan and Marcet's test of the errors' predictability", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.3).next_to(eq, DOWN, buff=0.55)
        tag = published_tag(r"Judd (1992); \ Den Haan and Marcet, \ REStud (1994)", corner=DR, font_size=12)
        with self.voiceover(
            "Every chapter so far has quoted an Euler-equation error. Here is what it is. <bookmark mark='a'/> At "
            "any capital stock, take the computed rule, and ask what consumption today the household's own Euler "
            "equation would demand, given what the rule does tomorrow. The error is the gap, as a share of "
            "consumption. <bookmark mark='b'/> It is unit-free: minus three on the log scale means a mistake of one "
            "dollar in a thousand. <bookmark mark='c'/> And it needs no true answer to compare with, which is the "
            "whole point: in a real problem there is none. Kenneth Judd proposed it in 1992. <bookmark mark='d'/> "
            "For long simulated series, Wouter den Haan and Albert Marcet's test of 1994 asks whether the errors "
            "can be predicted from information the household had; if they can, the rule is wrong."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def table(self):
        A = load("accuracy")
        rows = A["table"]
        ax = plane([-8, 0], [0, len(rows)], center=RIGHT * 1.3 + DOWN * 0.3, x_length=6.6, y_length=5.0,
                   xticks=[-8, -6, -4, -2, 0], yticks=[], xlabel=r"worst Euler error, \ $\log_{10}$",
                   xfmt=lambda v: f"{v:.0f}", font_size=14)
        bars = VGroup()
        for i, r in enumerate(rows):
            y = len(rows) - 1 - i + 0.5
            p0, p1 = ax.ax.c2p(r["max"], y - 0.32), ax.ax.c2p(0, y + 0.32)
            b = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=_col(r["method"]),
                          fill_opacity=0.85).move_to((p0 + p1) / 2)
            nm = label(tex_safe(r["method"]).replace("1,000", "1{,}000"), font_size=15,
                       color=_col(r["method"])).next_to(ax.ax.c2p(-8, y), LEFT, buff=0.15)
            sec = label(rf"{1000 * r['seconds']:.0f} ms" if r["seconds"] >= 0.0015 else r"< 1 ms", font_size=13,
                        color=GREY_A).next_to(b, LEFT, buff=0.08)
            bars.add(VGroup(b, nm, sec))
        head = label(r"the growth model, \ eight ways", font_size=26, color=E.ACCENT).to_edge(UP, buff=0.4)
        foot = label(r"longer bars are better: \ smooth methods win, \ and cost almost nothing", font_size=20,
                     color=WHITE).to_edge(DOWN, buff=0.35)
        tag = label(r"times measured on the machine that built the cache", font_size=12, color=GREY_B).to_corner(
            DR, buff=0.3)
        with self.voiceover(
            "Now line the methods up on one problem, as Borağan Aruoba, Jesús Fernández-Villaverde and Juan Rubio-"
            "Ramírez did in 2006 for a family of growth models. <bookmark mark='a'/> Value iteration on a thousand "
            "grid points: the slowest, and among the least accurate. <bookmark mark='b'/> Searching between forty "
            "grid points with straight lines, slightly worse; with a cubic spline, or with twelve Chebyshev points, "
            "thousands of times better. <bookmark mark='c'/> Collocation reaches the same accuracy in a few "
            "milliseconds. <bookmark mark='d'/> Perturbation is the fastest of all and, on this wide range of "
            "capital, the least accurate of the smooth methods. <bookmark mark='e'/> The ranking is specific to "
            "this smooth model; with a borrowing limit, a kink or a big shock it can turn over. That is why the "
            "error must be shown for the problem at hand, every time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(bars[0][1]), GrowFromEdge(bars[0][0], RIGHT), FadeIn(bars[0][2]))
            vo.wait_until("b")
            self.play(*[FadeIn(b[1]) for b in bars[1:4]], *[GrowFromEdge(b[0], RIGHT) for b in bars[1:4]],
                      *[FadeIn(b[2]) for b in bars[1:4]], run_time=1.5)
            vo.wait_until("c")
            self.play(*[FadeIn(b[1]) for b in bars[4:6]], *[GrowFromEdge(b[0], RIGHT) for b in bars[4:6]],
                      *[FadeIn(b[2]) for b in bars[4:6]])
            vo.wait_until("d")
            self.play(*[FadeIn(b[1]) for b in bars[6:]], *[GrowFromEdge(b[0], RIGHT) for b in bars[6:]],
                      *[FadeIn(b[2]) for b in bars[6:]])
            vo.wait_until("e")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()

    def tolerance(self):
        A = load("accuracy")
        G = load("growth")
        T = A["tolerance"]
        ax = plane([-8.5, -0.5], [-3, 0], center=LEFT * 1.6 + DOWN * 0.3, x_length=7.6, y_length=4.4,
                   xticks=[-8, -6, -4, -2, -1], yticks=[-3, -2, -1, 0],
                   xlabel=r"stopping tolerance, \ $\log_{10}$", ylabel=r"worst Euler error, \ $\log_{10}$",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        pts = VGroup(*[dot(ax, np.log10(r["tol"]), r["ee"], VFI, 0.09) for r in T])
        line = path(ax, [np.log10(r["tol"]) for r in T], [r["ee"] for r in T], VFI, 2.2, smooth=False)
        its = VGroup(*[label(str(r["iters"]), font_size=13, color=GREY_A).next_to(
            ax.ax.c2p(np.log10(r["tol"]), r["ee"]), DOWN, buff=0.15) for r in T])
        side = VGroup(
            label(r"value iteration, \\ 1,000 points, \\ stopped earlier \\ or later".replace(",", "{,}"),
                  font_size=18, color=VFI),
            label(r"grey: \ rounds taken", font_size=16, color=GREY_A),
            label(r"the error does not move: \\ the grid limits it, \\ not the stopping rule", font_size=18,
                  color=WHITE),
            label(rf"(the policy settled \\ at round {G['policy_settled']} \\ on 300 points)", font_size=16,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "One more lesson the errors teach. Stop value iteration earlier or later, with tolerances from one "
            "tenth down to a hundred millionth. <bookmark mark='a'/> Each tighter tolerance costs more rounds. "
            "<bookmark mark='b'/> But the error does not move at all. On a grid, the rule is decided by which grid "
            "point is best, and that settles long before the values do; after that, more rounds polish digits that "
            "do not matter. <bookmark mark='c'/> Two sources of error, the approximation and the stopping rule, and "
            "only measuring tells you which one binds."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(line), LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.2), FadeIn(its),
                      FadeIn(side[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(Indicate(line, color=WHITE, scale_factor=1.0))
        self.clear_scene()
