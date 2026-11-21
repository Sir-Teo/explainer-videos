from __future__ import annotations

from videos.economics.econ51.common import *  # noqa: F403

COLS = (ERR, POLICY, EGM)


def _one_in(e):
    v = 10 ** (-e)
    if v >= 1e6:
        return f"{v / 1e6:.1f} million"
    return f"{v:,.0f}".replace(",", "{,}")


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Play it: \ which grid is fine enough?", r"How many points does the answer need?",
             "Chapter three. Play it: which grid is fine enough?", lit={2006: r"Aruoba et al."}, scale=("nation",),
             horizon=("a century",))
        self.ask()
        self.reveal()
        self.errors()

    def ask(self):
        R = load("grids")
        ax = plane([0.5, 1.5], [0.5, 1.5], center=LEFT * 2.6 + DOWN * 0.3, x_length=5.2, y_length=5.0,
                   xticks=[0.5, 1.0, 1.5], yticks=[0.5, 1.0, 1.5], xlabel=r"capital now \ (share of steady state)",
                   ylabel=r"capital next year", xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}", font_size=13)
        diag = seg(ax, 0.5, 0.5, 1.5, 1.5, GREY_B, 1.4, dashed=True)
        pols = VGroup()
        for r, col in zip(R["rows"][:2], COLS):
            pols.add(path(ax, r["grid"], r["kprime"], col, 2.4, smooth=False))
        acc = path(ax, R["k"], R["accurate"], WHITE, 2.0)
        key = VGroup(*[label(t, font_size=16, color=c) for t, c in (
            (rf"{R['rows'][0]['n']} points", COLS[0]), (rf"{R['rows'][1]['n']} points", COLS[1]),
            (r"1,000 points: \ indistinguishable".replace("1,000", "1{,}000"), COLS[2]))]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).move_to(ax.ax.c2p(1.22, 0.68))
        q = label(r"You must report the steady-state capital \\ to within 1\%. \ Which grid will do?", font_size=24,
                  color=E.ACCENT).to_edge(RIGHT, buff=0.5).shift(UP * 1.8)
        opts = VGroup()
        for t, c in ((r"30 points", COLS[0]), (r"100 points", COLS[1]), (r"1,000 points".replace(",", "{,}"),
                                                                           COLS[2]), (r"none of them", GREY_B)):
            b = RoundedRectangle(width=2.6, height=0.8, corner_radius=0.1, stroke_color=c, stroke_width=2,
                                 fill_color=c, fill_opacity=0.1)
            opts.add(VGroup(b, label(t, font_size=20, color=c).move_to(b)))
        opts.arrange_in_grid(rows=2, cols=2, buff=0.25).next_to(q, DOWN, buff=0.45).align_to(q, RIGHT)
        ring = countdown().scale(0.55).next_to(opts, DOWN, buff=0.4)
        with self.voiceover(
            "Your turn. Value iteration chooses next year's capital from a grid of points. <bookmark mark='a'/> On "
            "a grid of thirty points the policy is a staircase; <bookmark mark='b'/> on a hundred, a finer "
            "staircase; on a thousand, it is hard to tell from the accurate rule. <bookmark mark='c'/> You must "
            "report the economy's steady-state capital, where the policy crosses the diagonal, to within one "
            "percent. <bookmark mark='d'/> Which grid will do: thirty points, a hundred, a thousand, or none of "
            "them? Pause, and choose."
        ) as vo:
            self.play(FadeIn(ax), Create(diag))
            vo.wait_until("a")
            self.play(Create(pols[0]), FadeIn(key[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(pols[1]), FadeIn(key[1]), Create(acc), FadeIn(key[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(q))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(o) for o in opts], lag_ratio=0.3), FadeIn(ring), run_time=1.5)
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.play(FadeOut(ring))
        self.clear_scene()

    def reveal(self):
        R = load("grids")
        rows = R["rows"]
        ax = plane([0, 3], [0.88, 1.02], center=LEFT * 1.8 + DOWN * 0.3, x_length=7.0, y_length=4.4, xticks=[],
                   yticks=[0.9, 0.95, 1.0], ylabel=r"steady-state capital, \ share of the true",
                   yfmt=lambda v: f"{v:.2f}", font_size=14)
        true = DashedLine(ax.ax.c2p(0, 1.0), ax.ax.c2p(3, 1.0), color=WHITE, stroke_width=2)
        band_ = Rectangle(width=ax.ax.c2p(3, 0)[0] - ax.ax.c2p(0, 0)[0],
                          height=ax.ax.c2p(0, 1.0)[1] - ax.ax.c2p(0, 0.99)[1], stroke_width=0, fill_color=GAIN,
                          fill_opacity=0.18)
        band_.move_to((ax.ax.c2p(0, 0.99) + ax.ax.c2p(3, 1.0)) / 2)
        dots = VGroup()
        for i, (r, c) in enumerate(zip(rows, COLS)):
            d = dot(ax, i + 0.5, r["steady"], c, 0.1)
            lab = VGroup(label(rf"{r['n']:,}".replace(",", "{,}") + r" points", font_size=16, color=c),
                         label(rf"{100 * (r['steady'] - 1):+.1f}\%".replace("-", "{-}"), font_size=16,
                               color=WHITE)).arrange(DOWN, buff=0.06).next_to(d, DOWN, buff=0.15)
            dots.add(VGroup(d, lab))
        side = VGroup(
            label(r"green: \ within 1\%", font_size=18, color=GAIN),
            label(r"the coarse grids \\ put the steady \\ state too low", font_size=18, color=WHITE),
            label(r"only 1,000 points \\ will do".replace(",", "{,}"), font_size=20, color=EGM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Here are the steady states each grid implies, as a share of the true one. <bookmark mark='a'/> Thirty "
            f"points: {100 * (1 - rows[0]['steady']):.1f} percent too low. <bookmark mark='b'/> A hundred: "
            f"{100 * (1 - rows[1]['steady']):.1f} percent too low, still outside the band. <bookmark mark='c'/> A "
            f"thousand: {100 * (1 - rows[2]['steady']):.2f} percent, inside it. Only the finest grid will do. "
            "<bookmark mark='d'/> Notice the direction: on a grid the household can only choose among a few "
            "capital stocks, and the rounding does not cancel out; it drags the steady state down."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(band_), Create(true), FadeIn(side[0]))
            for mk, d in zip("abc", dots):
                vo.wait_until(mk)
                self.play(FadeIn(d, scale=1.3))
                if mk == "c":
                    self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[1]))
        self.clear_scene()

    def errors(self):
        R = load("grids")
        rows = R["rows"]
        ax = plane([0.6, 1.4], [-4, 0], center=LEFT * 1.8 + UP * 0.1, x_length=7.0, y_length=4.2,
                   xticks=[0.6, 0.8, 1.0, 1.2, 1.4], yticks=[-4, -3, -2, -1, 0],
                   xlabel=r"capital, \ share of steady state", ylabel=r"Euler-equation error, \ $\log_{10}$",
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        curves = VGroup(*[path(ax, r["ee"]["k"], np.maximum(r["ee"]["log10"], -4), c, 1.6, smooth=False)
                          for r, c in zip(rows, COLS)])
        side = VGroup(*[label(rf"{r['n']:,}".replace(",", "{,}") + rf" points: \ worst $10^{{{r['ee']['max']:.1f}}}$"
                              r" \\ one dollar in " + _one_in(r["ee"]["max"]), font_size=18, color=c)
                        for r, c in zip(rows, COLS)]).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        side.to_edge(RIGHT, buff=0.35)
        foot = label(r"fine enough depends on the question: \ measure the error, \ do not guess it", font_size=21,
                     color=E.ACCENT).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "A better yardstick than any one number is the Euler-equation error, which chapter eight builds "
            "properly. For now: at each capital stock, how far is the rule from satisfying the household's own "
            "first-order condition, as a fraction of consumption? <bookmark mark='a'/> With thirty points the "
            f"worst mistake is about one dollar in {_one_in(rows[0]['ee']['max'])} of consumption. <bookmark "
            f"mark='b'/> With a hundred, one in {_one_in(rows[1]['ee']['max'])}. <bookmark mark='c'/> With a "
            f"thousand, one in {_one_in(rows[2]['ee']['max'])}. <bookmark mark='d'/> Ten times the points buys "
            "about ten times the accuracy, and costs a hundred times the work, because each point must compare "
            "itself with every other. Fine enough depends on the question; the habit to learn is to measure the "
            "error rather than guess it."
        ) as vo:
            self.play(FadeIn(ax))
            for mk, c_, s_ in zip("abc", curves, side):
                vo.wait_until(mk)
                self.play(Create(c_), FadeIn(s_), run_time=1.4)
            vo.wait_until("d")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()
