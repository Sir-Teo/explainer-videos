from __future__ import annotations

from videos.economics.econ20.common import *  # noqa: F403


class Transition(VoiceoverScene):
    def construct(self):
        card(self, 5, r"How fast does an economy converge?", r"Out of its steady state, \ how quickly does an "
             r"economy close the gap?", "Chapter five. How fast does an economy converge?",
             lit={1992: r"Barro and Sala-i-Martin; \ MRW"}, scale=("nation",), horizon=("decades",))
        self.linearize()
        self.paths()
        self.puzzle()

    def linearize(self):
        rows = VGroup(
            MathTex(r"\frac{d\ln k}{dt} = s\,k^{\alpha-1} - (n+g+\delta)", font_size=44),
            MathTex(r"\approx -(1-\alpha)(n+g+\delta)\,\big(\ln k - \ln k^\ast\big)", font_size=44),
            MathTex(r"\ln y_t - \ln y^\ast = e^{-\lambda t}\,\big(\ln y_0 - \ln y^\ast\big), \quad "
                    r"\lambda = (1-\alpha)(n+g+\delta)", font_size=40, color=E.ACCENT),
        ).arrange(DOWN, buff=0.5).move_to(UP * 0.9)
        notes = VGroup(
            label(r"divide the Solow equation by $k$", font_size=21, color=GREY_A),
            label(r"a first-order Taylor expansion in $\ln k$ around the steady state", font_size=21, color=GREY_A),
            label(r"each year a share $\lambda$ of the remaining gap closes \ (and $y = k^\alpha$ closes at the same "
                  r"rate)", font_size=21, color=GREY_A),
        )
        for n_, r in zip(notes, rows):
            n_.next_to(r, DOWN, buff=0.12)
        t = load("transition")
        nar = t["narrow"]
        res = label(rf"island: \ $\lambda = \tfrac{{2}}{{3}} \times 8\% = {pc(nar['lambda'])}$ \ a year; \ "
                    rf"half-life $\ln 2 / \lambda = {nar['half_life']:.0f}$ years", font_size=25,
                    color=OUTPUT).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "If an economy is below its steady state, how fast does it get there? <bookmark mark='a'/> Divide the "
            "Solow equation by k: the growth rate of capital per effective worker is the saving rate times the "
            "average product of capital, less the break-even rate. <bookmark mark='b'/> Near the steady state, a "
            "first-order expansion in the log of k turns this into a simple rule. <bookmark mark='c'/> The gap "
            "between log output and its steady state shrinks exponentially, at a rate lambda equal to one minus "
            "alpha, times n plus g plus delta. Each year, the same share of the remaining gap is closed. "
            f"<bookmark mark='d'/> On the island, two thirds of eight percent: {100 * nar['lambda']:.1f} percent a "
            f"year, so half of any gap closes in about {nar['half_life']:.0f} years."
        ) as vo:
            self.play(Write(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            for mk, r, n_ in zip("bc", rows[1:], notes[1:]):
                vo.wait_until(mk)
                self.play(Write(r), FadeIn(n_))
            vo.wait_until("d")
            self.play(FadeIn(res, shift=UP * 0.1))
        self.clear_scene()

    def paths(self):
        t = load("transition")
        yrs = np.array(t["years"], float)
        ax = plane([0, 120], [0, 1.05], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.6, y_length=5.0,
                   xticks=[0, 20, 40, 60, 80, 100, 120], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   ylabel=r"share of the initial gap left", xlabel=r"years", yfmt=lambda v: f"{100 * v:.0f}\\%",
                   font_size=16)
        half = DashedLine(ax.ax.c2p(0, 0.5), ax.ax.c2p(120, 0.5), color=GREY_B, stroke_width=1.5)
        narrow = path(ax, yrs, t["paths"]["0.33"]["gap"], color=OUTPUT, width=4, smooth=False)
        broad = path(ax, yrs, t["paths"]["0.75"]["gap"], color=CAPITAL, width=4, smooth=False)
        nar, bro = t["narrow"], t["broad"]
        side = VGroup(
            label(r"from a quarter of the steady state's capital", font_size=20, color=GREY_A),
            label(rf"$\alpha = 1/3$: \ half gone in {nar['half_life_simulated']} years", font_size=22,
                  color=OUTPUT),
            label(r"(faster than 13: \ far from $k^\ast$ \\ the returns to capital are higher)", font_size=18,
                  color=GREY_B),
            label(rf"$\alpha = 3/4$: \ $\lambda = {pc(bro['lambda'], 0)}$, \\ half gone in "
                  rf"{bro['half_life_simulated']} years \ (linear: {bro['half_life']:.0f})", font_size=22,
                  color=CAPITAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Here is the exact path, simulated year by year, for an island that starts with a quarter of its "
            "steady-state capital. <bookmark mark='a'/> With capital's share at a third, half of the gap in output "
            f"is gone in {nar['half_life_simulated']} years, a little faster than the rule's thirteen, because far "
            "from the steady state capital is scarce and earns more. Within a generation the island is nearly there. "
            "<bookmark mark='b'/> Now suppose capital's share were much larger, three quarters, as it would be if "
            "capital meant not only boats but the skills of the people who use them. Diminishing returns set in more "
            f"slowly, and lambda falls to {100 * bro['lambda']:.0f} percent: half the gap closes in about "
            f"{bro['half_life']:.0f} years."
        ) as vo:
            self.play(FadeIn(ax), Create(half), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(narrow), run_time=2.5)
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(Create(broad), run_time=2.5)
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def puzzle(self):
        c = load("convergence")["lit"]
        rows = VGroup(
            label(r"the textbook model: \ about 5\% a year", font_size=27, color=OUTPUT),
            label(rf"the cross-country regressions of the early 1990s: \ about 2\% \ (MRW: {pc(c['mrw_lambda_nonoil'])})",
                  font_size=25, color=E.ACCENT),
            label(r"so either capital's share is far larger than a third, \ or the steady states differ, \ or both",
                  font_size=24, color=GREY_A),
            label(r"the data, \ in the next chapter", font_size=24, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(DOWN * 0.1)
        head = label(r"the model against the data", font_size=34, color=GREY_A).to_edge(UP, buff=0.8)
        with self.voiceover(
            "That is the model's prediction, and it can be checked. <bookmark mark='a'/> With capital's share at "
            "a third, the textbook says about five percent a year. <bookmark mark='b'/> When economists in the early "
            "1990s measured how fast countries closed their gaps, they kept finding about two percent, so often that "
            "Robert Barro later called it an iron law. Mankiw, Romer and Weil's estimate was "
            f"{100 * c['mrw_lambda_nonoil']:.1f} percent. <bookmark mark='c'/> Two percent fits the model only if "
            "capital's share is about three quarters, far above the third that the national accounts pay to "
            "capital. <bookmark mark='d'/> To see how those numbers were found, and whether poor countries catch up "
            "at all, we need the data."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
