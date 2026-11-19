from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ9.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 14, r"The Dials: \ what misallocation costs", r"How far are real economies from equal marginal "
             r"products, and what does the gap cost?", "Chapter fourteen. The Dials: what misallocation costs.",
             scale=("firm", "market", "nation"), horizon=("a decade",))
        self.idea()
        self.dial()

    def idea(self):
        d = load("dial")
        sims = d["sims"]
        rows = VGroup(
            label(r"the first welfare theorem, \ for firms: \ in a competitive equilibrium \\ every plant's "
                  r"marginal product of capital and labour is the same", font_size=25),
            label(r"subsidized credit, \ licences, \ connections, \ taxes that depend on size: \\ some plants "
                  r"get too much, \ others too little", font_size=24, color=HOLD),
            label(r"measure the spread of revenue productivity across plants, \\ and ask how much more the same "
                  r"capital and labour could make", font_size=24),
            label(r"with lognormal spread $s$ and elasticity $\sigma$: \ "
                  r"$\log(Y_{\text{efficient}}/Y) = \tfrac{\sigma}{2}\,s^2$", font_size=26, color=E.ACCENT),
            label(rf"Agora, \ 100{{,}}000 simulated plants, \ $\sigma = 3$: \ "
                  rf"spread as in the US (1997), \ {100 * sims['US 1997']['gain']:.0f}\% more; \ "
                  rf"as in China (2005), \ {100 * sims['China 2005']['gain']:.0f}\% more", font_size=22,
                  color=E.AGORA),
        ).arrange(DOWN, buff=0.35)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "This part's dial asks how far real economies are from the first welfare theorem. "
            "<bookmark mark='a'/> In a competitive equilibrium with production, every plant pays the same for "
            "capital and labour, so the last unit of each is worth the same everywhere. <bookmark mark='b'/> In "
            "real economies some plants get cheap credit, licences or political favour, and others face taxes and "
            "red tape, so the marginal products differ. <bookmark mark='c'/> Chang-Tai Hsieh and Peter Klenow's "
            "idea was to measure that spread from data on plants, and ask how much more the same capital and labour "
            "would produce if it were moved to where it earns most. <bookmark mark='d'/> If the spread is "
            "lognormal, the answer has a simple form: the log of the gain is half the elasticity of substitution "
            "times the variance. <bookmark mark='e'/> Agora checks it on a hundred thousand simulated plants: with "
            "America's spread of 1997, output could be forty-three percent higher; with China's of 2005, eighty-three "
            "percent."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def dial(self):
        dial = dials.DIALS["misallocation"]
        b = load("dial")["bkr"]
        head = status_head(dial, r"TFP gain from equalizing marginal products \ (new)")
        frame, rows = dial_rows(dial, 0.0, 140.0, [0, 20, 40, 60, 80, 100, 120, 140], r"percent more manufacturing "
                                r"output from the same capital and labour", top=2.2, step=0.62, fmt="{:.0f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 12.6, 18, GREY_A).to_edge(DOWN, buff=0.15)
        bk = label(rf"Bils, Klenow and Ruane (2021): \ measurement error inflates the gaps; \ correcting it lowers "
                   rf"India's potential gains by {100 * b['india_cut']:.0f}\%, \ America's by "
                   rf"{100 * b['us_cut']:.0f}\%", font_size=19, color=HOLD).next_to(meaning, UP, buff=0.2)
        tag = published_tag(r"Hsieh and Klenow, QJE 124(4) (2009), tables 4 and 6; Bils, Klenow and Ruane, NBER WP "
                            r"26711", corner=UR, font_size=12)
        with self.voiceover(
            "Here are the measurements. <bookmark mark='a'/> Hsieh and Klenow found that if China's factories in 2005 "
            "were only as unequal as America's in 1997, manufacturing output would be about thirty percent higher; "
            "for India in 1994, about sixty percent. <bookmark mark='b'/> Equalizing marginal products completely, "
            "even America's factories would produce forty-three percent more, China's eighty-seven and India's about a "
            "hundred and twenty-eight. <bookmark mark='c'/> Those are large numbers, and part of them may not be "
            "real: if output or inputs are measured with error, plants look more unequal than they are. Mark "
            "Bils, Peter Klenow and Cian Ruane estimated how much, and found that correcting for it lowers India's "
            "potential gains by a fifth and America's by three fifths. <bookmark mark='d'/> So this dial is "
            "contested. The direction is clear: unequal marginal products cost a great deal of output. How much "
            "is still being measured, and Part twenty-one returns to it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[:2]], lag_ratio=0.4), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[2:]], lag_ratio=0.4), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(bk))
            vo.wait_until("d")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()
