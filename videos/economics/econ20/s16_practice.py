from __future__ import annotations

from videos.economics.econ20.common import *  # noqa: F403

HOURS = 0.004          # an assumed growth of hours worked, a year (not a forecast)


class Practice(VoiceoverScene):
    def construct(self):
        card(self, 14, r"In practice: \ potential output and the long-term budget", r"How do forecasters use the "
             r"Solow model, \ and what does it say about public debt?",
             "Chapter fourteen. In practice: potential output and the long-term budget.",
             lit={1989: r"Abel, Mankiw, Summers, Zeckhauser", 2001: r"CBO's method", 2019: r"Blanchard"},
             scale=("nation",), horizon=("a decade", "decades"))
        self.potential()
        self.debt()
        self.jobs()

    def potential(self):
        a = load("accounting")
        us = a["countries"]["USA"]
        alpha = us["alpha"]
        recent = a["us_periods"]["2005-2019"]["tfp"]
        long_ = us["tfp"]
        g1 = HOURS + recent / (1 - alpha)
        g2 = HOURS + long_ / (1 - alpha)
        rows = VGroup(
            label(r"the Congressional Budget Office: \ potential output built on a Solow growth model",
                  font_size=22, color=GREY_A),
            MathTex(r"g_Y = \alpha\,g_K + (1-\alpha)\,g_L + g_A", font_size=44),
            MathTex(r"\text{balanced path: } g_K = g_Y \;\Rightarrow\; g_Y = g_L + \frac{g_A}{1-\alpha}",
                    font_size=42, color=E.ACCENT),
            label(rf"hours: \ +{100 * HOURS:.1f}\% a year \ (an assumption) \ $\cdot$ \ $\alpha = {alpha:.2f}$",
                  font_size=22, color=LABOUR),
            label(rf"residual as in 2005--2019, \ {pc(recent, 2)}: \ potential growth {pc(g1)}", font_size=24,
                  color=TFP),
            label(rf"residual as in 1950--2019, \ {pc(long_, 2)}: \ potential growth {pc(g2)}", font_size=24,
                  color=OUTPUT),
        ).arrange(DOWN, buff=0.32).move_to(UP * 0.1)
        tag = published_tag(r"CBO, \emph{CBO's Method for Estimating Potential Output: An Update} (2001)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "This part's model is at work every year in budget offices. <bookmark mark='a'/> The Congressional "
            "Budget Office describes its estimate of potential output, the economy's output at full employment, "
            "as built on a Solow growth model. <bookmark mark='b'/> Output's growth is the share-weighted growth of "
            "capital and labour, plus the residual. <bookmark mark='c'/> On a balanced path capital grows as fast as "
            "output, so the residual counts more than once: output grows at the rate of hours plus the residual "
            "divided by one minus alpha. <bookmark mark='d'/> Suppose hours grow by "
            f"{100 * HOURS:.1f} percent a year, an assumption for the arithmetic. <bookmark mark='e'/> If the "
            f"residual grows as it did from 2005 to 2019, potential growth is about {100 * g1:.1f} percent a year. "
            f"<bookmark mark='f'/> If it grows as it did on average since 1950, about {100 * g2:.1f}. Half a point "
            "of the residual, and the whole budget outlook, ride on a number the model does not explain."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def debt(self):
        rows = VGroup(
            MathTex(r"b_{t+1} = \frac{1+r}{1+g}\, b_t + d_t", font_size=50),
            label(r"$b$: \ debt $\div$ GDP \ $\cdot$ \ $d$: \ the primary deficit $\div$ GDP", font_size=21,
                  color=GREY_A),
            label(r"if $r > g$, \ debt grows of itself unless the budget runs surpluses", font_size=23,
                  color=LABOUR),
            label(r"if $r < g$, \ a debt ratio can fall with no surplus at all \ (Blanchard, \ 2019)", font_size=23,
                  color=CONS),
            label(r"Ramsey's economy has $r = \rho + \theta g > g$: \ $r < g$ is a sign of saving beyond the golden "
                  r"rule", font_size=22, color=RATE),
            label(r"Abel, Mankiw, Summers and Zeckhauser (1989): \ capital earns more than is invested, \ year after "
                  r"year: \ the US is not over-saving", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.1)
        tag = published_tag(r"Blanchard, AER 109(4) (2019); \ Abel, Mankiw, Summers and Zeckhauser, REStud 56(1) "
                            r"(1989)", corner=DR, font_size=12)
        with self.voiceover(
            "The second use is the long-term budget. <bookmark mark='a'/> Debt as a share of output evolves with the "
            "interest rate, r, and the growth rate, g. <bookmark mark='b'/> Each year the ratio is multiplied by one "
            "plus r over one plus g, and the primary deficit is added. <bookmark mark='c'/> If the interest rate "
            "exceeds growth, debt grows of itself unless the government runs surpluses. <bookmark mark='d'/> If "
            "growth exceeds the interest rate, as it did for most of the 2010s, a debt ratio can fall without any "
            "surplus, a point Olivier Blanchard made in his presidential address of 2019. <bookmark mark='e'/> The "
            "growth models say which is normal. In Ramsey's economy the interest rate is impatience plus theta "
            "times growth, above growth; an economy with r below g for ever would be saving beyond the golden rule. "
            "<bookmark mark='f'/> Andrew Abel, Gregory Mankiw, Lawrence Summers and Richard Zeckhauser proposed a "
            "test that does not need the interest rate: an economy is not over-saving if what capital earns exceeds "
            "what is invested, year after year. By that test, they found, the United States and the other large "
            "economies are not."
        ) as vo:
            self.play(Write(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def jobs(self):
        cards = point_cards([
            (r"budget offices", r"potential output, \\ long-term projections", OUTPUT),
            (r"central banks", r"the output gap; \\ the neutral rate", RATE),
            (r"the IMF and World Bank", r"medium-term growth \\ for every member", SAVE),
            (r"investors", r"long-run growth \\ and returns", CAPITAL),
        ], width=12.6, cols=2, font_size=23).move_to(DOWN * 0.2)
        head = label(r"who uses this", font_size=34, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Who does this work? <bookmark mark='a'/> Budget offices, for potential output and the long-term "
            "projections. <bookmark mark='b'/> Central banks, for the output gap and the neutral rate of interest, "
            "which part thirty takes up. <bookmark mark='c'/> The IMF and the World Bank, which project "
            "medium-term growth for every member country, and, as Easterly showed, have not always used the best "
            "model to do it. <bookmark mark='d'/> And long-horizon investors, for whom a growth rate is the main "
            "input to what stocks and bonds will pay."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
