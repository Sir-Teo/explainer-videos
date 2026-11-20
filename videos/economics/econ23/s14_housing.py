from __future__ import annotations

from videos.economics.econ23.common import *  # noqa: F403


class Housing(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Housing as an asset", r"What should a house cost, \ given the rent it would fetch?",
             "Chapter twelve. Housing as an asset.", lit={1984: r"Poterba", 2005: r"Himmelberg, Mayer, Sinai"},
             scale=("household", "market"), horizon=("years",))
        self.user_cost()
        self.ratio()

    def user_cost(self):
        rows = VGroup(
            label(r"owning a home for a year costs:", font_size=25, color=GREY_A),
            MathTex(r"\text{user cost} \;=\; P\,\big(r + \tau_p + \delta + \text{risk} - g_P\big)", font_size=46,
                    color=HOUSE),
            label(r"interest forgone, \ property tax, \ upkeep and a risk premium, \ less expected appreciation",
                  font_size=22, color=GREY_A),
            label(r"in equilibrium, \ owning and renting cost the same:", font_size=24, color=WHITE),
            MathTex(r"\frac{P}{\text{rent}} \;=\; \frac{1}{r + \tau_p + \delta + \text{risk} - g_P}", font_size=46,
                    color=HOUSE),
            label(r"so the price-to-rent ratio rises when interest rates fall, \ or when people expect prices to "
                  r"keep rising", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Poterba, QJE 99(4) (1984); \ Himmelberg, Mayer and Sinai, JEP 19(4) (2005)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "A house is the largest asset most families own, and Jorgenson's user cost applies to it directly. "
            "<bookmark mark='a'/> Owning a home for a year costs the interest you could have earned on its price, "
            "the property tax, upkeep, and a premium for the risk of owning one large asset, less the rise in its "
            "price that you expect. <bookmark mark='b'/> James Poterba wrote it down in 1984. "
            "<bookmark mark='c'/> If owning and renting are both possible, they should cost about the same. "
            "<bookmark mark='d'/> So the ratio of price to rent is one over the user cost rate. "
            "<bookmark mark='e'/> It rises when interest rates fall, a Gordon formula for houses, or when people "
            "expect prices to keep rising: which is how expectations can feed a boom."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), FadeIn(tag))
            for mk, r_ in zip("bcde", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def ratio(self):
        h = load("housing")
        ax = plane([1987, 2027], [0.8, 1.6], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.6, y_length=4.8,
                   xticks=[1990, 2000, 2010, 2020], yticks=[0.8, 1.0, 1.2, 1.4, 1.6],
                   ylabel=r"home prices $\div$ rents \ (January 2000 $= 1$)", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.1f}", font_size=16)
        line_ = path(ax, h["t"], h["ratio"], color=HOUSE, width=4, smooth=False)
        one = seg(ax, 1987, 1.0, 2027, 1.0, color=GREY_B, width=2, dashed=True)
        side = VGroup(
            label(rf"peak: \ {h['peak']:.2f} \\ ({h['peak_when'][:7]})", font_size=20, color=HOUSE),
            label(rf"trough: \ {h['trough']:.2f} \\ ({h['trough_when'][:7]})", font_size=20, color=RISK),
            label(rf"latest: \ {h['last']:.2f} \\ ({h['last_when'][:7]})", font_size=20, color=HOUSE),
            label(r"the 2000s boom rode on \\ low rates and expected \\ gains; \ the bust took \\ banks with it "
                  r"\ (Part 33)", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = data_tag(rf"S\&P CoreLogic Case-Shiller U.S. National Home Price Index; \ BLS, \ CPI rent of primary "
                       rf"residence; \ via FRED, \ retrieved {h['retrieved']}", corner=DR, font_size=12)
        with self.voiceover(
            "Here is the ratio for the United States: the national index of home prices divided by the consumer "
            "price index for rents, set to one in January 2000. <bookmark mark='a'/> Through the 1990s it barely "
            "moved. Then prices pulled away from rents, to a peak of "
            f"{h['peak']:.2f} in {h['peak_when'][:4]}. <bookmark mark='b'/> They fell back to "
            f"{h['trough']:.2f} by {h['trough_when'][:4]}. <bookmark mark='c'/> Since then the ratio has climbed "
            f"again, to {h['last']:.2f}. <bookmark mark='d'/> Part of the 2000s boom was low interest rates, which "
            "the user cost says should raise the ratio. Part was expectations of further gains, which fed on "
            "themselves; and the bust that followed took banks with it, which Part thirty-three takes up."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(one), FadeIn(tag), Create(line_), run_time=2.5)
            for mk, r_ in zip("abcd", side):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
        self.clear_scene()
