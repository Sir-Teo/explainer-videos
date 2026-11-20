from __future__ import annotations

from videos.economics.econ36.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 14, r"Frontier: \ market power, \ services, \ time", r"What do the models still leave out?",
             "Chapter fourteen. Frontier: market power, services, time.",
             lit={2019: r"markups and trade", 2023: r"Boehm et al."}, scale=("firm", "world"),
             horizon=("a year", "a decade"))
        self.questions()
        self.gains()

    def questions(self):
        rows = VGroup(
            label(r"open questions", font_size=27, color=E.ACCENT),
            label(r"market power: \ when a few large firms trade, \ do gains go to markups or to buyers?",
                  font_size=21, color=FIRM),
            label(r"services: \ the fastest-growing trade, \ and the hardest to measure", font_size=21, color=FISH),
            label(r"time: \ elasticities of one in a year and two in a decade; \ which governs the gains?",
                  font_size=21, color=ARCH),
            label(r"adjustment: \ why workers and places recover so slowly from shocks", font_size=21, color=CHINA),
            label(r"geography: \ why activity clusters in a few places \ (Part 37)", font_size=21, color=GAIN),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.2)
        tag = published_tag(tables.BOEHM_2023.tag + r"; \ Autor, \ Dorn and Hanson (2013)", corner=DR, font_size=12)
        with self.voiceover(
            "The frontier. <bookmark mark='a'/> Market power: when trade is dominated by a few large firms, how much "
            "of its gain goes into markups rather than lower prices? <bookmark mark='b'/> Services: the fastest-"
            "growing kind of trade, from software to tourism, and the hardest to measure. <bookmark mark='c'/> "
            "Time: an elasticity of one in the first year and two after a decade, so which governs the gains, and "
            "how should a counterfactual handle the path between? <bookmark mark='d'/> Adjustment: why the places "
            "hit by the China shock were still worse off a decade later. <bookmark mark='e'/> And geography: why "
            "economic activity clusters in a few places at all, the subject of the next part."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def gains(self):
        G = load("gains_int")
        regs = ("USA", "CHN", "JPN", "DEU", "GBR", "MEX")
        names = {"USA": "America", "CHN": "China", "JPN": "Japan", "DEU": "Germany", "GBR": "Britain",
                 "MEX": "Mexico"}
        idx = [G["regions"].index(r) for r in regs]
        bars = VGroup()
        for k, i in enumerate(idx):
            x = -5.0 + 1.75 * k
            h1, h2 = G["one"][i] * 18, G["inter"][i] * 18
            b1 = Rectangle(width=0.6, height=h1, stroke_width=0, fill_color=GREY_B, fill_opacity=0.8).move_to(
                np.array([x - 0.33, -2.3 + h1 / 2, 0]))
            b2 = Rectangle(width=0.6, height=h2, stroke_width=0, fill_color=GAIN, fill_opacity=0.9).move_to(
                np.array([x + 0.33, -2.3 + h2 / 2, 0]))
            bars.add(VGroup(b1, label(f"{100 * G['one'][i]:.1f}", font_size=15, color=GREY_A).next_to(b1, UP,
                                                                                                    buff=0.05),
                            b2, label(f"{100 * G['inter'][i]:.1f}", font_size=15, color=GAIN).next_to(b2, UP,
                                                                                                    buff=0.05),
                            label(names[regs[k]], font_size=16, color=WHITE).move_to(np.array([x, -2.7, 0]))))
        eq = MathTex(r"1 - \lambda^{1/\theta} \quad \to \quad 1 - \lambda^{1/(\theta(1-\beta))}", font_size=34).to_edge(
            UP, buff=0.4)
        keys = label(rf"percent of real income lost in autarky: \ grey, \ one sector; \ green, \ with a share "
                     rf"$\beta$ = {G['beta']:.1f} of costs in traded inputs", font_size=17, color=GREY_A).next_to(
            eq, DOWN, buff=0.25)
        foot = label(rf"Costinot and Rodr\'iguez-Clare (2018): \ for America, \ {G['crc_lo']} to {G['crc_hi']}\% "
                     r"of GDP", font_size=18, color=E.ACCENT).to_edge(RIGHT, buff=0.4).shift(UP * 0.6)
        tag = published_tag(r"CEPII 2019 flows; \ Costinot and Rodr\'iguez-Clare (2014, \ 2018)", corner=DR,
                            font_size=11)
        with self.voiceover(
            "One frontier is how large the gains from trade really are. Part thirty-five's formula gave America about "
            f"{100 * G['one'][idx[0]]:.1f} percent of real income. <bookmark mark='a'/> But that formula assumes "
            "one sector and no traded inputs. When firms import parts to make goods that are themselves traded, a "
            "fall in trade costs compounds through the chain: with half of costs in traded inputs, the exponent "
            f"doubles, and America's gain rises to {100 * G['inter'][idx[0]]:.1f} percent, Germany's to "
            f"{100 * G['inter'][idx[3]]:.0f}. <bookmark mark='b'/> Arnaud Costinot and Andrés Rodríguez-Clare showed "
            "how many sectors, intermediate goods and other features change the answer; their later estimates put "
            f"America's gains between {G['crc_lo']} and {G['crc_hi']} percent of GDP. The same simple formula, with "
            "the economy's structure added, gives answers several times larger."
        ) as vo:
            self.play(Write(eq), FadeIn(keys), FadeIn(tag), *[FadeIn(b_[4]) for b_ in bars],
                      LaggedStart(*[FadeIn(b_[:2]) for b_ in bars], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_[2:4], shift=UP * 0.1) for b_ in bars], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()
