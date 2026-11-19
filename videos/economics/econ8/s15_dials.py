from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ8.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ capital's elasticity, \ and substitution", r"How much does output respond to "
             r"capital, and how easily does capital replace labour?", "Chapter thirteen. The Dials: capital's "
             "elasticity, and substitution.", scale=("firm", "market", "nation"), horizon=("a decade", "a century"))
        self.capital()
        self.substitution()

    def capital(self):
        dial = dials.DIALS["capital_share"]
        head = status_head(dial, r"output elasticity of capital \ (new)")
        frame, rows = dial_rows(dial, 0.0, 0.6, [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], r"percent change in output per "
                                r"percent change in capital", top=1.8, step=0.75)
        meaning = wrapped_label(tex_safe(dial.meaning), 12.6, 18, GREY_A).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Two dials open in this part. The first is the output elasticity of capital: by how much output rises, in "
            "percent, when capital rises one percent. <bookmark mark='a'/> Cobb and Douglas's own data give a "
            "quarter, constrained or not. <bookmark mark='b'/> Under competition the elasticity equals capital's "
            "share of income, which is easier to measure. Douglas Gollin, correcting for the income of the "
            "self-employed, found labour's share between sixty-five and eighty percent in most countries, so "
            "capital's between a fifth and a third. The Penn World Table puts America's at about three eighths in the "
            "second half of the twentieth century. <bookmark mark='c'/> Settled within a range, then, but with a "
            "caveat: labour's share has been falling since 2000, so the number isn't a constant of nature."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[:2]], lag_ratio=0.4), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[2:]], lag_ratio=0.5), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()

    def substitution(self):
        dial = dials.DIALS["kl_substitution"]
        head = status_head(dial, r"elasticity of substitution, \ capital and labour \ (new)")
        frame, rows = dial_rows(dial, 0.0, 1.5, [0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5], r"percent change in $K/L$ per "
                                r"percent change in $w/r$", top=2.1, step=0.62)
        one = DashedLine([frame[0].get_start()[0] + (frame[0].get_end()[0] - frame[0].get_start()[0]) / 1.5,
                          frame[0].get_y(), 0],
                         [frame[0].get_start()[0] + (frame[0].get_end()[0] - frame[0].get_start()[0]) / 1.5,
                          2.45, 0], color=OUT, stroke_width=1.8)
        ol = label(r"Cobb--Douglas", font_size=16, color=OUT).next_to(one, UP, buff=0.05)
        meaning = wrapped_label(tex_safe(dial.meaning), 12.6, 18, GREY_A).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "The second dial is the elasticity of substitution between capital and labour, the sigma of chapter two. "
            "<bookmark mark='a'/> Robert Chirinko's survey of seventy-five years of estimates concluded in 2008 that "
            "the weight of the evidence puts it between nought point four and nought point six. "
            "<bookmark mark='b'/> A meta-analysis of more than three thousand estimates, by Sebastian Gechert and "
            "his colleagues, found a reported average of nought point nine, but nought point three once publication "
            "bias and certain choices of method are corrected: a result that, they wrote, emphatically rejects "
            "Cobb–Douglas. Ezra Oberfield and Devesh Raval, building it up from American manufacturing plants, find "
            "between a half and nought point seven. <bookmark mark='c'/> Against these, Loukas Karabarbounis and "
            "Brent Neiman's influential estimate is one and a quarter, which would let cheaper machines explain part "
            "of labour's falling share. <bookmark mark='d'/> Contested, and consequential: on one side of one, cheaper "
            "capital helps workers' share; on the other, it hurts it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), Create(one), FadeIn(ol))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[1:4]], lag_ratio=0.5), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(rows[4]))
            vo.wait_until("d")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()
