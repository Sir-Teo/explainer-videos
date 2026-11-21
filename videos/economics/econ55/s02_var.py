from __future__ import annotations

from videos.economics.econ55.common import *  # noqa: F403


class VAR(VoiceoverScene):
    def construct(self):
        card(self, 1, r"What a VAR knows, \ and what it does not", r"How many stories fit one history?",
             "Chapter one. What a VAR knows, and what it does not.", lit={1980: r"Sims"}, scale=("nation",),
             horizon=("a decade",))
        self.reduced()
        self.rotations()

    def reduced(self):
        eqs = VGroup(
            MathTex(r"x_t = c + A_1 x_{t-1} + \dots + A_p x_{t-p} + u_t", font_size=40, color=DATA),
            MathTex(r"u_t = B\,\varepsilon_t, \qquad \mathbb{E}[\varepsilon_t \varepsilon_t'] = I \;\Longrightarrow\; "
                    r"\Sigma = \mathbb{E}[u_t u_t'] = B B'", font_size=40, color=MODEL),
            MathTex(r"\text{three variables: } \Sigma \text{ has 6 numbers}, \; B \text{ has 9}", font_size=36,
                    color=ERR),
        ).arrange(DOWN, buff=0.6).move_to(UP * 0.7)
        notes = VGroup(
            label(r"$x_t$: \ output growth, \ inflation, \ the policy rate", font_size=21, color=GREY_A),
            label(r"the $A$'s and $\Sigma$: \ estimated by least squares, \ equation by equation", font_size=21,
                  color=DATA),
            label(r"$\varepsilon_t$: \ the structural shocks, \ supply, \ demand, \ monetary, \ which nobody sees",
                  font_size=21, color=MODEL),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.55)
        tag = published_tag(r"Sims, \ Econometrica 48(1) (1980)", corner=DR, font_size=12)
        hc = history_card(1980, r"Christopher Sims", r"``Macroeconomics and reality'': \ let every variable depend "
                          r"on the past of all, \ and impose only what you must", color=DATA, width=10.0,
                          font_size=24).move_to(UP * 0.4)
        with self.voiceover(
            "In 1980 Christopher Sims proposed that macroeconomists stop imposing restrictions they could not "
            "defend. <bookmark mark='a'/> Let each variable, here output growth, inflation and the policy rate, "
            "depend on the recent past of all of them. That is a vector autoregression, and least squares estimates "
            "it equation by equation. <bookmark mark='b'/> What is left over each quarter, the surprises u, are "
            "mixtures of the shocks we care about, supply, demand and monetary policy, which nobody observes. Their "
            "covariance is B times B transposed. <bookmark mark='c'/> And here is the catch. With three variables "
            "the covariance of the surprises has six distinct numbers, but the mixing matrix B has nine. The data "
            "pin down six of them. Three must come from somewhere else."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.1), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeOut(hc))
            self.play(Write(eqs[0]), FadeIn(notes[0]), FadeIn(notes[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(eqs[1], shift=UP * 0.1), FadeIn(notes[2]))
            vo.wait_until("c")
            self.play(FadeIn(eqs[2], shift=UP * 0.1))
        self.clear_scene()

    def rotations(self):
        R = load("rotations")
        h = np.arange(len(R["rotations"][0]["y"]))
        axy = plane([0, 16], [-3.0, 1.0], center=LEFT * 3.4 + DOWN * 0.45, x_length=5.4, y_length=4.2,
                    xticks=[0, 4, 8, 12, 16], yticks=[-3, -2, -1, 0, 1], xlabel=r"quarters",
                    ylabel=r"output, \ \%", xfmt=lambda v: f"{v:.0f}",
                    yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0", font_size=13)
        axp = plane([0, 16], [-0.6, 2.8], center=RIGHT * 3.2 + DOWN * 0.45, x_length=5.4, y_length=4.2,
                    xticks=[0, 4, 8, 12, 16], yticks=[0, 1, 2], xlabel=r"quarters", ylabel=r"inflation, \ points",
                    xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=13)
        cols = (GRID, EST, ERR)
        names = (r"story 1", r"story 2", r"story 3")
        cy = VGroup(*[path(axy, h, r_["y"], c, 2.6, yr=(-3.0, 1.0)) for r_, c in zip(R["rotations"], cols)])
        cp = VGroup(*[path(axp, h, r_["pi"], c, 2.6, yr=(-0.6, 2.8)) for r_, c in zip(R["rotations"], cols)])
        z1 = DashedLine(axy.ax.c2p(0, 0), axy.ax.c2p(16, 0), color=GREY_D, stroke_width=1)
        z2 = DashedLine(axp.ax.c2p(0, 0), axp.ax.c2p(16, 0), color=GREY_D, stroke_width=1)
        key = VGroup(*[label(rf"{n}", font_size=18, color=c) for n, c in zip(names, cols)]).arrange(RIGHT, buff=0.8)
        head = VGroup(label(r"three answers to ``what does a one-point rise in the rate do?''", font_size=23,
                            color=E.ACCENT), key).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.35)
        foot = label(r"every one reproduces the data's $\Sigma$ exactly: \ the data cannot choose", font_size=21,
                     color=WHITE).to_edge(DOWN, buff=0.3)
        tag = island_tag(r"simulated: \ the Island", corner=DR, font_size=13)
        with self.voiceover(
            f"Here is what that means on the Island. Fit a vector autoregression to {R['T']} quarters of its "
            "history. <bookmark mark='a'/> Then take three different mixing matrices, each of which reproduces the "
            "covariance of the surprises exactly, and in each call one of the shocks monetary policy. <bookmark "
            "mark='b'/> Story one: a rise in the rate barely moves output or inflation. <bookmark mark='c'/> Story "
            "two: output edges up and inflation falls. <bookmark mark='d'/> Story three: output collapses and "
            "inflation jumps. <bookmark mark='e'/> All three fit the data equally well, to the last decimal. A "
            "vector autoregression summarizes a history; it does not, on its own, say what caused what. Every "
            "answer about the effect of policy comes from an assumption added to it, and the rest of this part is "
            "about which assumptions earn their place."
        ) as vo:
            self.play(FadeIn(axy), FadeIn(axp), Create(z1), Create(z2), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(head))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(Create(cy[k]), Create(cp[k]), run_time=1.2)
            vo.wait_until("e")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()
