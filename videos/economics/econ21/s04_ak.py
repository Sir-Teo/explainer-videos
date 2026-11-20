from __future__ import annotations

from videos.economics.econ21.common import *  # noqa: F403


class AK(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Growth without end: \ AK and learning by doing", r"What if returns to capital never "
             r"diminish?", "Chapter three. Growth without end: AK and learning by doing.",
             lit={1962: r"Arrow", 1986: r"Romer", 1988: r"Lucas"}, scale=("firm", "nation"), horizon=("decades",))
        self.ak()
        self.learning()
        self.scale()

    def ak(self):
        a = load("ak")
        t = np.array(a["t"], float)
        ax = plane([0, 60], [0, np.log10(7)], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.4, y_length=4.8,
                   xticks=[0, 20, 40, 60], yticks=[0, np.log10(2), np.log10(4)], xlabel=r"years",
                   ylabel=r"output \ (year 0 $= 1$, \ log)", yfmt=lambda v: f"{10 ** v:.0f}", font_size=16)
        akl = path(ax, t, np.log10(np.array(a["K"]) / a["K"][0]), color=IDEA, width=4, smooth=False)
        sy = np.array(a["solow_y"])
        sol = path(ax, t, np.log10(sy / sy[0]), color=OUTPUT, width=4, smooth=False)
        side = VGroup(
            MathTex(r"Y = A K", font_size=46, color=IDEA),
            MathTex(r"\frac{\dot K}{K} = sA - \delta", font_size=42),
            label(rf"$s = 0.2$, \ $A = 0.4$, \ $\delta = 0.05$: \\ {pc(a['growth'], 0)} a year, \ for ever",
                  font_size=20, color=IDEA),
            label(r"Solow with the same saving: \\ growth fades as returns diminish", font_size=20, color=OUTPUT),
        ).arrange(DOWN, buff=0.35).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "The simplest way to get growth without end is to remove diminishing returns. <bookmark mark='a'/> Let "
            "output be proportional to capital: Y equals A K. <bookmark mark='b'/> Then capital grows at the saving "
            "rate times A, less depreciation, whatever its level. <bookmark mark='c'/> Saving a fifth, with A at "
            f"0.4, the economy grows {100 * a['growth']:.0f} percent a year from the first year to the last: a "
            "straight line on a log scale. <bookmark mark='d'/> Solow's economy, with the same saving and capital's "
            "share at a third, grows fast at first and then fades to nothing without technical progress. In AK, "
            "saving more raises growth for ever. But why would returns to capital not diminish?"
        ) as vo:
            self.play(FadeIn(ax), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(akl), FadeIn(side[2]), run_time=2)
            vo.wait_until("d")
            self.play(Create(sol), FadeIn(side[3]), run_time=2)
        self.clear_scene()

    def learning(self):
        rows = VGroup(
            label(r"Kenneth Arrow, \ 1962: \ learning by doing", font_size=27, color=E.ACCENT),
            label(r"productivity rises with experience, \ even with no new machines", font_size=23, color=GREY_A),
            label(r"his example: \ the Horndal iron works in Sweden, \ where output per worker kept rising for years "
                  r"with no new investment", font_size=21, color=GREY_A),
            label(r"Paul Romer, \ 1986: \ each firm's investment adds to knowledge that spills over to all", font_size=23,
                  color=IDEA),
            MathTex(r"Y_i = A(K)\,K_i^{\alpha} L_i^{1-\alpha}, \quad A(K) \propto K^{1-\alpha} \;\Rightarrow\; Y = "
                    r"\text{const}\cdot K", font_size=36),
            label(r"Robert Lucas, \ 1988: \ the same with human capital", font_size=23, color=SKILL),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.1)
        tag = published_tag(r"Arrow, REStud 29(3) (1962); \ Romer, JPE 94(5) (1986); \ Lucas, JME 22(1) (1988)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Two answers came from spillovers. <bookmark mark='a'/> In 1962 Kenneth Arrow argued that productivity "
            "rises with experience: workers and managers learn by doing. <bookmark mark='b'/> His example was the "
            "Horndal iron works in Sweden, where output per worker kept rising for years with no new investment at "
            "all. <bookmark mark='c'/> In 1986 Paul Romer made the learning a by-product of investment: each firm's "
            "capital adds to a stock of knowledge that every firm can use. <bookmark mark='d'/> If knowledge rises "
            "in just the right proportion to the economy's capital, each firm faces diminishing returns but the "
            "economy as a whole does not: aggregate output is proportional to aggregate capital, an AK economy. "
            "<bookmark mark='e'/> Robert Lucas told the same story in 1988 with human capital in place of machines."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def scale(self):
        rows = VGroup(
            label(r"two problems", font_size=30, color=E.ACCENT),
            label(r"knife edge: \ the exponent must be exactly right, \ or growth dies out or explodes", font_size=23,
                  color=WEDGE),
            label(r"scale: \ if knowledge is shared across the whole economy, \ bigger economies should grow faster",
                  font_size=23, color=WEDGE),
            label(r"neither has the look of a law of nature", font_size=23, color=GREY_A),
            label(r"the next step: \ make ideas the product of deliberate work, \ for profit", font_size=24,
                  color=IDEA),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        with self.voiceover(
            "The spillover models have two problems. <bookmark mark='a'/> The first is a knife edge, like Harrod's: "
            "if knowledge grows slightly less than one for one with capital, growth dies out; slightly more, and it "
            "explodes. <bookmark mark='b'/> The second is scale. If knowledge is shared across the whole economy, a "
            "bigger economy accumulates it faster and should grow faster for ever. <bookmark mark='c'/> Neither looks "
            "like a law of nature. <bookmark mark='d'/> Romer's next step, in 1990, was to make ideas the product of "
            "deliberate work, done for profit."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
