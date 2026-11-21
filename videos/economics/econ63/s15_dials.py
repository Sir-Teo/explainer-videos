from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ63.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ granular shocks and substitution", r"How much of the cycle comes from firms' "
             r"own shocks, \ and how easily can firms swap inputs?",
             "Chapter thirteen. The Dials: granular shocks and substitution.", scale=("firm", "nation"),
             horizon=("a year", "a decade"))
        self.share()
        self.substitution()

    def share(self):
        dial = dials.DIALS["idiosyncratic_share"]
        head = status_head(dial, r"the cycle from firms' own shocks \ (new)")
        frame, rows = dial_rows(dial, 0, 1, [0, 0.25, 0.5, 0.75, 1.0], r"share of the variance of output growth",
                                top=1.7, step=0.8, fmt="{:.2f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 11.6, 17, GREY_A).to_edge(DOWN, buff=0.5)
        tag = published_tag(r"the dial's record: \ explainer/economics/dials.py", corner=DR, font_size=12)
        D = load("dials")["granular"]
        with self.voiceover(
            "This part opens two Dials. The first: what share of the swings in aggregate output comes from firms' "
            "and industries' own shocks, rather than from shocks that hit everyone? <bookmark mark='a'/> Gabaix's "
            "granular residual, the hundred largest American firms: about a third. <bookmark mark='b'/> Andrew "
            "Foerster, Pierre-Daniel Sarte and Mark Watson, separating industries' own shocks from common ones in "
            "industrial production: about half, after the mid-1980s, when common shocks grew quieter. <bookmark "
            "mark='c'/> Enghin Atalay, letting the elasticities of substitution be estimated rather than set to "
            "one: at least half. <bookmark mark='d'/> And the Island, where the truth is planted at "
            f"{D['truth']:.2f}: Gabaix's method finds {D['median']:.2f} in the typical forty-year history, because "
            "it sees only the largest hundred firms, with a wide spread from one history to the next. <bookmark "
            "mark='e'/> The status is contested: a third to more than half, depending on the years, the data, and "
            "above all on the elasticities, which is the second Dial."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k]))
            vo.wait_until("e")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.wait(0.5)
        self.clear_scene()

    def substitution(self):
        dial = dials.DIALS["input_substitution"]
        head = status_head(dial, r"swapping inputs within a year \ (new)")
        frame, rows = dial_rows(dial, 0, 1, [0, 0.25, 0.5, 0.75, 1.0], r"elasticity of substitution between "
                                r"intermediate inputs", top=1.4, step=0.9, fmt="{:.2f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 11.6, 17, GREY_A).to_edge(DOWN, buff=0.5)
        tag = published_tag(r"the dial's record: \ explainer/economics/dials.py", corner=DR, font_size=12)
        S = load("dials")["substitution"]
        with self.voiceover(
            "The second: how easily can a firm swap one input for another within a year? An elasticity of one is "
            "the Cobb-Douglas case, where Hulten's rule is exact; zero is Leontief's fixed recipe. <bookmark "
            "mark='a'/> Atalay, from American industries' input shares and prices: between zero and about 0.15, "
            "depending on the specification. <bookmark mark='b'/> Boehm, Flaaen and Pandalai-Nayar, from the "
            "Japanese-owned plants after the earthquake: about 0.2 among materials. <bookmark mark='c'/> And the "
            f"Island: from thirty years of its tables, {S['estimate']:.2f}, with the truth planted at "
            f"{S['theta']:.2f}. <bookmark mark='d'/> Settled within a range: in the short run, inputs are close "
            "to fixed proportions. That is why chapter five's curves bend, and why a disaster's cost depends on "
            "what flows along the links."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k]))
            vo.wait_until("d")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.wait(0.5)
        self.clear_scene()
