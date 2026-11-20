from __future__ import annotations

from videos.economics.econ30.common import *  # noqa: F403


class IS(VoiceoverScene):
    def construct(self):
        card(self, 6, r"The dynamic IS curve", r"How does the interest rate reach spending?", "Chapter six. The "
             "dynamic IS curve.", lit={1978: r"Hall's Euler equation"}, scale=("household", "nation"),
             horizon=("a quarter",))
        self.euler()
        self.three()

    def euler(self):
        rows = VGroup(
            label(r"from Part 22: \ the household's Euler equation", font_size=25, color=E.ACCENT),
            MathTex(r"c_t = \mathbb{E}_t\, c_{t+1} - \frac{1}{\sigma}\big(i_t - \mathbb{E}_t\, \pi_{t+1} - "
                    r"\rho\big)", font_size=38),
            label(r"a higher real interest rate makes saving more attractive: \ spend less now, \ more later",
                  font_size=22, color=RATE),
            label(r"with no investment or government, \ output is consumption; \ subtract the flexible-price "
                  r"version", font_size=22, color=GREY_A),
            MathTex(r"x_t = \mathbb{E}_t\, x_{t+1} - \frac{1}{\sigma}\big(i_t - \mathbb{E}_t\, \pi_{t+1} - "
                    r"r^n_t\big)", font_size=44, color=OUTPUT),
            label(r"$r^n_t$: \ the natural rate of interest, \ the real rate with flexible prices", font_size=22,
                  color=CB),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Hall, \ \emph{JPE} 86(6) (1978); \ Gal\'i (2015), \ ch.\ 3; \ Part 22", corner=DR,
                            font_size=12)
        with self.voiceover(
            "The second equation comes from households. <bookmark mark='a'/> It is Part twenty-two's Euler "
            "equation, in logs: consumption today equals expected consumption tomorrow, less a term in the real "
            "interest rate. <bookmark mark='b'/> A higher real rate makes saving more attractive, so people spend "
            "less now and more later. <bookmark mark='c'/> With no investment or government in this simplest "
            "version, output equals consumption; subtract the same equation for an economy with flexible prices, "
            "<bookmark mark='d'/> and you get the dynamic IS curve: today's output gap equals tomorrow's expected "
            "gap, less the gap between the real interest rate and the natural rate. <bookmark mark='e'/> The "
            "natural rate is the real rate the economy would have with flexible prices. It is the benchmark the "
            "central bank's rate is measured against."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                if isinstance(r_, MathTex):
                    self.play(Write(r_), run_time=1.3)
                else:
                    self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def three(self):
        eqs = VGroup(
            MathTex(r"\pi_t = \beta\, \mathbb{E}_t\, \pi_{t+1} + \kappa\, x_t + u_t", font_size=40, color=INFL),
            MathTex(r"x_t = \mathbb{E}_t\, x_{t+1} - \frac{1}{\sigma}\big(i_t - \mathbb{E}_t\, \pi_{t+1} - "
                    r"r^n_t\big)", font_size=40, color=OUTPUT),
            MathTex(r"i_t = \rho + \phi_\pi\, \pi_t + \phi_x\, x_t + v_t", font_size=40, color=CB),
        ).arrange(DOWN, buff=0.55).move_to(LEFT * 1.6 + UP * 0.2)
        names = VGroup(
            label(r"firms: \ the New Keynesian \\ Phillips curve", font_size=20, color=INFL),
            label(r"households: \ the \\ dynamic IS curve", font_size=20, color=OUTPUT),
            label(r"the central bank: \\ a rule \ (next chapter)", font_size=20, color=CB),
        )
        for e, n_ in zip(eqs, names):
            n_.next_to(e, RIGHT, buff=0.6).set_x(5.0)
        shocks = label(r"three shocks: \ $u$ (costs), \ $r^n$ (demand), \ $v$ (policy)", font_size=22,
                       color=E.ACCENT).to_edge(DOWN, buff=0.8)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here is the whole model. <bookmark mark='a'/> Firms: inflation depends on expected inflation and the "
            "output gap, plus a cost-push shock u. <bookmark mark='b'/> Households: the output gap depends on "
            "the expected gap and on the real interest rate against the natural rate, which moves with demand. "
            "<bookmark mark='c'/> And the central bank sets the nominal interest rate, by a rule the next chapter "
            "takes from the data, plus a policy shock v. <bookmark mark='d'/> Three equations, three shocks. This "
            "is the model taught in every graduate course, and the core of every model central banks use."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, e, n_ in zip("abc", eqs, names):
                vo.wait_until(mk)
                self.play(Write(e), FadeIn(n_), run_time=1.3)
            vo.wait_until("d")
            self.play(FadeIn(shocks))
        self.clear_scene()
