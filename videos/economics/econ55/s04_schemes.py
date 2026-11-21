from __future__ import annotations

from videos.economics.econ55.common import *  # noqa: F403


class Schemes(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Five ways to identify a shock", r"What can be assumed, \ and what does each assumption buy?",
             "Chapter three. Five ways to identify a shock.",
             lit={1989: r"Blanchard and Quah", 2003: r"Rigobon", 2005: r"Uhlig", 2013: r"Mertens and Ravn"},
             scale=("nation",), horizon=("a decade",))
        self.five()

    def five(self):
        specs = [
            (r"1. \ timing", r"the bank cannot move output or prices within the quarter",
             r"B = \begin{pmatrix} * & 0 & 0 \\ * & * & 0 \\ * & * & * \end{pmatrix}", r"Sims (1980)",
             METHOD["recursive"]),
            (r"2. \ the long run", r"only supply shocks move the level of output for ever",
             r"\big[C(1)\,B\big]_{\text{output}} = (*,\ 0,\ 0)", r"Blanchard and Quah (1989)", METHOD["long_run"]),
            (r"3. \ signs", r"a tightening raises the rate and lowers output and inflation",
             r"b_{\text{money}} = (-,\ -,\ +)", r"Uhlig (2005)", METHOD["sign"]),
            (r"4. \ an outside instrument", r"a series that moves with the monetary shock and no other",
             r"b_{\text{money}} \propto \operatorname{Cov}(u_t, z_t)", r"Stock and Watson (2012); Mertens and Ravn "
             r"(2013)", METHOD["proxy"]),
            (r"5. \ a change in variance", r"monetary shocks are larger in some quarters, the others are not",
             r"\Sigma_1 - \Sigma_0 = (\sigma_1^2 - \sigma_0^2)\, b_{\text{money}} b_{\text{money}}'",
             r"Rigobon (2003)", METHOD["hetero"]),
        ]
        rows = VGroup()
        for name, idea, math, who, col in specs:
            m = MathTex(math, font_size=26, color=col)
            if m.width > 4.2:
                m.width = 4.2
            rows.add(VGroup(label(name, font_size=21, color=col),
                            VGroup(wrapped_label(idea, 4.6, 18, WHITE), label(who, font_size=15, color=GREY_B)
                                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.08), m))
        ys = np.linspace(2.0, -2.9, len(rows))
        for r, y in zip(rows, ys):
            r[0].move_to([-6.7 + r[0].width / 2, y, 0])
            r[1].move_to([-3.6 + r[1].width / 2, y, 0])
            r[2].move_to([4.55, y, 0])
        head = label(r"three restrictions are missing: \ where can they come from?", font_size=26,
                     color=E.ACCENT).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Three restrictions are missing. Economists have found five places to look for them. <bookmark "
            "mark='a'/> The first is timing. If the central bank sets its rate after seeing this quarter's output "
            "and prices, but its decision cannot affect them until next quarter, then the mixing matrix has zeros "
            "above its diagonal. This is the recursive ordering Sims used, and the hook showed what happens when "
            "the bank knows more than the ordering allows. <bookmark mark='b'/> The second is the long run. Olivier "
            "Blanchard and Danny Quah assumed that only supply shocks, technology and the like, can move the level "
            "of output for ever; demand and money only move it for a while. <bookmark mark='c'/> The third is "
            "signs. Harald Uhlig asked only that a tightening raise the rate and lower output and inflation, and "
            "kept every mixing matrix that obeys. The answer is a set of possibilities, not a single one. <bookmark "
            "mark='d'/> The fourth is an outside instrument: a series that moves with the monetary shock and with "
            "nothing else, such as a market surprise on the day of a decision. James Stock and Mark Watson, and "
            "Karel Mertens and Morten Ravn, showed that its covariance with the surprises traces out the shock's "
            "column. <bookmark mark='e'/> The fifth is a change in variance. If monetary shocks are larger in some "
            "quarters, say those with a policy meeting, and nothing else changes, then the difference between the "
            "two covariances points straight at the monetary shock. Roberto Rigobon called this identification "
            "through heteroskedasticity."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_[0]), FadeIn(r_[1]), Write(r_[2]), run_time=1.2)
        self.clear_scene()
