from __future__ import annotations

from videos.economics.econ30.common import *  # noqa: F403

SHOCKS = (("monetary", r"a monetary tightening", CB), ("demand", r"a rise in demand", OUTPUT),
          ("cost", r"a cost-push shock", COST))


class Solved(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Three equations, \ solved", r"What does the model say a shock will do?", "Chapter eight. "
             "Three equations, solved.", lit={1999: r"Clarida, \ Gal\'i and Gertler"}, scale=("nation",),
             horizon=("a quarter", "three years"))
        self.principle()
        self.responses()

    def principle(self):
        D = load("determinacy")
        fps, fxs = np.array(D["phi_pi"])[::2], np.array(D["phi_x"])[::2]
        U = np.array(D["unique"])[::2, ::2]
        fxs_all = np.array(D["phi_x"])
        ax = plane([0, 3], [0, 1], center=LEFT * 2.2 + DOWN * 0.3, x_length=7.2, y_length=4.8,
                   xticks=[0, 0.5, 1, 1.5, 2, 2.5, 3], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"$\phi_\pi$, \ response to inflation", ylabel=r"$\phi_x$, \ response to the gap",
                   xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:.2f}", font_size=15)
        cells = VGroup()
        dx, dy = fps[1] - fps[0], fxs[1] - fxs[0]
        for j, fx in enumerate(fxs[:-1]):
            for i, fp in enumerate(fps[:-1]):
                p0, p1 = ax.ax.c2p(fp, fx), ax.ax.c2p(fp + dx, fx + dy)
                cells.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0,
                                    fill_color=CB if U[j, i] else INFL, fill_opacity=0.35).move_to((p0 + p1) / 2))
        bound = path(ax, D["boundary"], fxs_all, WHITE, 3, smooth=False, xr=(0, 3))
        taylor = dot(ax, 1.5, 0.125, E.ACCENT, 0.1)
        tl = label(r"Taylor", font_size=18, color=E.ACCENT).next_to(taylor, UP, buff=0.1)
        side = VGroup(
            label(r"green: \ one equilibrium", font_size=20, color=CB),
            label(r"red: \ many: \ self-fulfilling \\ inflations and deflations", font_size=20, color=INFL),
            MathTex(r"\kappa(\phi_\pi - 1) + (1-\beta)\,\phi_x > 0", font_size=28, color=WHITE),
            label(r"the Taylor principle: \\ raise the rate more than \\ one for one with inflation", font_size=20,
                  color=E.ACCENT),
            label(r"1970s estimates: \ below one; \\ after 1979: \ above \\ (Clarida, \ Gal\'i and Gertler)",
                  font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Clarida, \ Gal\'i and Gertler, \ \emph{QJE} 115(1) (2000); \ Bullard and Mitra "
                            r"(2002); \ the Island", corner=DR, font_size=12)
        with self.voiceover(
            "Before solving the model, check that it has one solution. Both variables, inflation and the gap, are "
            "free to jump, so by the counting rule of Part twenty-nine, both roots of the system must lie outside "
            "the unit circle. <bookmark mark='a'/> Here is the answer for every rule, the response to inflation "
            "across the bottom and to the gap up the side. In green, rules that pin down a unique equilibrium. "
            "<bookmark mark='b'/> In red, rules that leave many: any inflation people expect can come true. "
            "<bookmark mark='c'/> The boundary has a formula: kappa times phi pi minus one, plus one minus beta "
            "times phi x, must be positive. <bookmark mark='d'/> In words, the Taylor principle: when inflation "
            "rises, raise the nominal rate by more, so that the real rate rises. Taylor's own rule is safely inside. "
            "<bookmark mark='e'/> Richard Clarida, Jordi Galí and Mark Gertler estimated the Federal Reserve's "
            "response before 1979 and found it below one, and after 1979 above: one account of why the 1970s went "
            "wrong and the 1980s right."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(bound), Write(side[2]))
            vo.wait_until("d")
            self.play(GrowFromCenter(taylor), FadeIn(tl), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def _panel(self, R, center, title, col):
        q = np.array(R["q"])
        ys = np.concatenate([R["x"], R["pi"], R["i"]])
        lo, hi = float(min(-0.5, np.floor(ys.min() * 2) / 2)), float(max(0.5, np.ceil(ys.max() * 2) / 2))
        ax = plane([0, 11], [lo, hi], center=center, x_length=3.9, y_length=3.4, xticks=[0, 4, 8],
                   yticks=[lo, 0, hi], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.1f}" if v else "0",
                   font_size=13)
        zero = seg(ax, 0, 0, 11, 0, GREY_D, 1.2)
        lines = VGroup(path(ax, q, R["x"], OUTPUT, 3, smooth=False), path(ax, q, R["pi"], INFL, 3, smooth=False),
                       path(ax, q, R["i"], RATE, 2.5, smooth=False))
        t = label(title, font_size=19, color=col).next_to(ax, UP, buff=0.15)
        return VGroup(ax, zero, t), lines

    def responses(self):
        R = load("irfs")
        panels = [self._panel(R[k], c, t, col) for (k, t, col), c in
                  zip(SHOCKS, (LEFT * 4.6 + DOWN * 0.2, DOWN * 0.2, RIGHT * 4.6 + DOWN * 0.2))]
        key = VGroup(label(r"green: \ output gap, \ \%", font_size=18, color=OUTPUT),
                     label(r"red: \ inflation, \ annual rate", font_size=18, color=INFL),
                     label(r"pink: \ the policy rate, \ annual", font_size=18, color=RATE)).arrange(
            RIGHT, buff=0.6).to_edge(UP, buff=0.35)
        m, c = R["monetary"], R["cost"]
        foot = label(r"each shock: \ one point a year, \ fading by half each quarter; \ quarters across",
                     font_size=17, color=GREY_B).to_edge(DOWN, buff=0.6)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Now the responses, with Galí's numbers on the Island: each shock is one point at an annual rate, "
            "fading by half each quarter. <bookmark mark='a'/> A monetary tightening: the policy rate rises "
            f"{m['i'][0]:.2f} points, the output gap falls {abs(m['x'][0]):.2f} percent, and inflation falls "
            f"{abs(m['pi'][0]):.2f} points. Money is not neutral, because prices cannot all adjust at once. "
            "<bookmark mark='b'/> A rise in demand: output and inflation both rise, and the rule raises the rate "
            "to lean against them. <bookmark mark='c'/> A cost-push shock: inflation rises by "
            f"{c['pi'][0]:.1f} points while output falls {abs(c['x'][0]):.2f} percent, because the central bank "
            "raises rates against the inflation. <bookmark mark='d'/> Demand shocks move output and inflation "
            "together; cost shocks move them apart, and that difference is the next chapter."
        ) as vo:
            self.play(FadeIn(key), FadeIn(foot), FadeIn(tag), *[FadeIn(p[0]) for p in panels])
            for mk, p in zip("abc", panels):
                vo.wait_until(mk)
                self.play(LaggedStart(*[Create(l_) for l_ in p[1]], lag_ratio=0.3), run_time=1.8)
            vo.wait_until("d")
            self.play(Indicate(panels[1][0][2], color=WHITE), Indicate(panels[2][0][2], color=WHITE))
        self.clear_scene()
