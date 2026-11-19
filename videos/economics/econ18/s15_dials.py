from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ18.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ the value of a statistical life", r"Across methods, \ what do people accept "
             r"for a small risk of death?", "Chapter thirteen. The Dials: the value of a statistical life.",
             scale=("person", "nation"), lit={2004: r"the speed limits", 2024: r"DOT's value"})
        self.dial()
        self.why()

    def dial(self):
        dial = dials.DIALS["vsl"]
        lo, hi, x0, x1 = 0.0, 16.0, -0.2, 6.3
        head = status_head(dial, r"the value of a statistical life \ (new)")
        frame, rows = dial_rows(dial, lo, hi, [0, 2, 4, 6, 8, 10, 12, 14, 16],
                                r"millions of 2024 dollars \ (CPI-U)", top=1.9, step=0.85, fmt="{:.1f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 12.6, 17, GREY_A).to_edge(DOWN, buff=0.22)
        tag = published_tag(r"JPE 112(S1) (2004); \ EPA, \emph{Mortality Risk Valuation}; \ DOT guidance (2024)",
                            corner=UR, font_size=12)
        r0, r1, r2 = dial.estimates
        with self.voiceover(
            "Here is the dial, every value converted to 2024 dollars. <bookmark mark='a'/> Ashenfelter and "
            "Greenstone's speed limits give an upper bound of about three million dollars, with wide uncertainty. "
            "<bookmark mark='b'/> The Environmental Protection Agency's central value, from a distribution fitted to "
            "twenty-six studies, mostly of wages and risks, is seven point four million in 2006 dollars, about "
            f"{say_num(r1.value, 1)} million today. <bookmark mark='c'/> And the Department of Transportation "
            f"uses {say_num(r2.value, 1)} million for analyses in 2024. <bookmark mark='d'/> The status: contested. "
            "The number moves by more than a factor of four with the method and with whose choices are observed. It returns "
            "in part fifty-eight, where a bill is scored."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("d")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()

    def why(self):
        rows = VGroup(
            label(r"why the methods disagree", font_size=28, color=E.ACCENT),
            label(r"wage studies: \ risky jobs differ from safe ones in more than risk \ (omitted variables, \ part "
                  r"four)", font_size=22),
            label(r"workers in risky jobs may care less about risk: \ they chose them", font_size=22, color=GREY_A),
            label(r"people misjudge small risks, \ so what they accept may not be what they would choose informed",
                  font_size=22, color=LIFE),
            label(r"the speed limit counts time at the wage: \ an upper bound, \ by design", font_size=22,
                  color=MONEY),
            label(r"a regulator still needs one number: \ the choice among them is part of the policy", font_size=22,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        with self.voiceover(
            "Why such a spread? <bookmark mark='a'/> Wage studies compare risky jobs with safe ones, but risky jobs "
            "differ in more than risk, the omitted variables of part four. <bookmark mark='b'/> The people in "
            "risky jobs may also care less about risk; they chose those jobs. <bookmark mark='c'/> People misjudge "
            "small probabilities, so what they accept may not be what they would choose if they understood the "
            "risk. <bookmark mark='d'/> And the speed-limit study values time at the wage, which makes it an upper "
            "bound by design. <bookmark mark='e'/> A regulator still needs one number, and choosing it is part of "
            "the policy."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
