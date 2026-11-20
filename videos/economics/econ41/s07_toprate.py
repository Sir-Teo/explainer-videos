from __future__ import annotations

from videos.economics.econ41.common import *  # noqa: F403


class TopRate(VoiceoverScene):
    def construct(self):
        card(self, 6, r"The optimal top rate, \ derived", r"Where does $1/(1 + ae)$ come from?",
             "Chapter six. The optimal top rate, derived.", lit={2001: r"Saez", 2011: r"Diamond and Saez"},
             scale=("person", "nation"), horizon=("a year",))
        self.reform()
        self.algebra()

    def reform(self):
        P = load("top")
        a = P["a"]
        ax = plane([0.8, 4.0], [0, 1.1], center=LEFT * 2.0 + DOWN * 0.5, x_length=7.6, y_length=4.4,
                   xticks=[1, 2, 3, 4], yticks=[], xlabel=r"income, \ in units of the top threshold $\bar z$",
                   ylabel=r"number of taxpayers", xfmt=lambda v: f"{v:.0f}", font_size=14)
        z = np.linspace(1.0, 4.0, 120)
        dens = a * z ** (-a - 1) / a
        cur = path(ax, z, dens, TOP, 3.2)
        fill = Polygon(*[ax.ax.c2p(x, y) for x, y in zip(z, dens)], ax.ax.c2p(4.0, 0), ax.ax.c2p(1.0, 0),
                       stroke_width=0, fill_color=TOP, fill_opacity=0.25)
        zbar = vline(ax, 1.0, 0, 1.1, WHITE)
        zm = a / (a - 1)
        zml = vline(ax, zm, 0, 1.0, REVENUE)
        lz = label(r"$\bar z$", font_size=22, color=WHITE).next_to(ax.ax.c2p(1.0, 1.1), UP, buff=0.05)
        lzm = label(rf"$z_m$ = {zm:.1f} $\bar z$", font_size=20, color=REVENUE).next_to(ax.ax.c2p(zm, 1.0), UP,
                                                                                        buff=0.05)
        side = VGroup(
            label(r"raise the top rate \\ by a little, \ $d\tau$", font_size=19, color=WHITE),
            label(r"mechanical gain: \\ $d\tau \, (z_m - \bar z)$ \\ per top earner", font_size=19, color=GAIN),
            label(r"behavioural loss: \\ incomes fall by \\ $e\, z_m\, d\tau / (1 - \tau)$, \\ costing $\tau$ times "
                  r"that", font_size=19, color=LOSS),
            label(r"welfare cost: \\ $g$ times the gain", font_size=19, color=WORKER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = data_tag(rf"the shape of the top: \ $a$ = {a:.2f}, \ Piketty and Saez's 2022 shares", corner=DR,
                       font_size=12)
        with self.voiceover(
            "Here is where the formula comes from, in Emmanuel Saez's 2001 way of thinking. Take everyone above a "
            "high threshold, z bar, where the top rate starts. <bookmark mark='a'/> Their average income is z m, and "
            f"with a Pareto tail it is a over a minus one times the threshold: {zm:.1f} times, for a of "
            f"{a:.2f}. <bookmark mark='b'/> Raise the top rate a little. <bookmark mark='c'/> Mechanically, each top "
            "earner pays d tau more on the part of income above the threshold: that is the gain. "
            "<bookmark mark='d'/> But each top earner also reports less income, by the elasticity times their income "
            "times d tau over one minus tau, and the government loses tau on each dollar not reported. "
            "<bookmark mark='e'/> And top earners lose the gain, which counts against welfare with the weight g."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(cur), FadeIn(fill), Create(zbar), FadeIn(lz), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(zml), FadeIn(lzm))
            for mk, k in zip("bcde", range(4)):
                vo.wait_until(mk)
                self.play(FadeIn(side[k]))
        self.clear_scene()

    def algebra(self):
        P = load("top")
        lines = VGroup(
            MathTex(r"(1 - g)\, d\tau\, (z_m - \bar z) \;=\; \tau\, \frac{e\, z_m\, d\tau}{1 - \tau}", font_size=38),
            MathTex(r"\frac{\tau}{1 - \tau} \;=\; \frac{1 - g}{e}\cdot\frac{z_m - \bar z}{z_m} \;=\; "
                    r"\frac{1 - g}{a\,e}, \qquad a = \frac{z_m}{z_m - \bar z}", font_size=38),
            MathTex(r"\tau^{*} \;=\; \frac{1 - g}{1 - g + a\, e}", font_size=46, color=E.ACCENT),
        ).arrange(DOWN, buff=0.55).move_to(UP * 0.6)
        notes = VGroup(
            label(r"at the optimum, \ the net gain equals the behavioural loss", font_size=19, color=GREY_A),
            label(r"a Pareto tail makes $a$ the same at every high threshold", font_size=19, color=GREY_A),
            label(rf"$g$ = 0: \ the top of the top bracket's Laffer curve; \ with $a$ = {P['a']:.2f}, \ $e$ = 0.25: \ "
                  rf"{100 * P['rates']['0.25']:.0f}\%", font_size=19, color=TOP),
        )
        for n_, l_ in zip(notes, lines):
            n_.next_to(l_, RIGHT, buff=0.3)
        notes.arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "At the best rate, a small change neither helps nor hurts. <bookmark mark='a'/> So the gain, net of its "
            "welfare cost, equals the behavioural loss. <bookmark mark='b'/> Rearranged, the rate over one minus the "
            "rate equals one minus g over a times e, where a is z m over z m minus z bar, the number that the tax "
            "records show is close to constant across high thresholds. <bookmark mark='c'/> So the top rate is one "
            "minus g over one minus g plus a times e. With g equal to zero, it is the top of the Laffer curve for "
            f"the top bracket: {100 * P['rates']['0.25']:.0f} percent with America's a and an elasticity of a "
            "quarter. Three numbers: one the tax records measure well, one a value judgement, and one hard to "
            "measure. That is why the elasticity is the battleground."
        ) as vo:
            self.play(Write(lines[0]), FadeIn(notes[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Write(lines[1]), FadeIn(notes[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Write(lines[2]), FadeIn(notes[2]))
        self.clear_scene()
