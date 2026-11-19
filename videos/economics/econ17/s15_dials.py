from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ17.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ what a sought-after school adds", r"Do the schools everyone wants raise their "
             r"pupils' scores?", "Chapter thirteen. The Dials: what a sought-after school adds.",
             scale=("person", "city"), lit={2014: r"the elite illusion", 2017: r"Denver's match"})
        self.houses()
        self.dial()

    def houses(self):
        nw = load("schools")["newton_waltham"]
        rows = VGroup(
            label(r"across one street, \ outside Boston:", font_size=25),
            label(rf"a three-bedroom house in Newton: \ \${nw['newton']:,}".replace(",", "{,}"), font_size=25,
                  color=HELD),
            label(rf"a similar one in Waltham: \ \${nw['waltham']:,}".replace(",", "{,}"), font_size=25,
                  color=GREY_A),
            label(rf"Newton's high-school pupils proficient in math: \ {nw['proficient_newton'] * 100:.0f}\%; \ "
                  rf"Waltham's: \ {nw['proficient_waltham'] * 100:.0f}\%", font_size=23, color=SCHOOL),
            label(r"parents pay for the schools: \ but is a school with stronger pupils a better school?",
                  font_size=24, color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Abdulkadiroğlu, Angrist and Pathak, Econometrica 82(1) (2014), introduction (2008 "
                            r"dollars)", corner=DR, font_size=12)
        with self.voiceover(
            "Parents pay a great deal for schools. <bookmark mark='a'/> Across a single street outside Boston, a "
            "three-bedroom house in Newton sold, on average, for about four hundred and twelve thousand dollars, "
            "<bookmark mark='b'/> and a similar one in Waltham for about three hundred and sixteen thousand. "
            "<bookmark mark='c'/> Ninety-two percent of Newton's high-school pupils are proficient in math, and "
            "seventy-eight percent of Waltham's. <bookmark mark='d'/> But is a school whose pupils score higher a "
            "better school, or just a school with stronger pupils? This part opens a dial for that."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def dial(self):
        dial = dials.DIALS["school_effects"]
        lo, hi, x0, x1 = -0.15, 0.55, -0.2, 6.3
        head = status_head(dial, r"what a sought-after school adds \ (new)")
        frame, rows = dial_rows(dial, lo, hi, [-0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5],
                                r"effect on test scores, \ in standard deviations", top=1.9, step=0.75, fmt="{:+.3f}")

        def X(v):
            return x0 + (x1 - x0) * (v - lo) / (hi - lo)

        zero = VGroup(DashedLine([X(0), 2.35, 0], [X(0), -1.0, 0], color=GREY_C, stroke_width=2),
                      label(r"no effect", font_size=15, color=GREY_B).move_to([X(0), 2.55, 0]))
        meaning = wrapped_label(tex_safe(dial.meaning), 12.6, 18, GREY_A).to_edge(DOWN, buff=0.25)
        tag = published_tag(r"NBER WP 17264 (2011), Table 4; \ IZA DP 10429 (2016), Table 6", corner=UR, font_size=12)
        with self.voiceover(
            "Here is the dial. <bookmark mark='a'/> Boston's three exam schools admit by a test score, with a sharp "
            "cutoff. Abdulkadiroğlu, Angrist and Pathak compared applicants just above and just below it. Pupils "
            "who just got in move to schools whose pupils score far higher, yet their own math scores changed by "
            "about nothing, <bookmark mark='b'/> and their English scores by about nothing too. They called it the "
            "elite illusion. <bookmark mark='c'/> Denver's charter schools, evaluated through the match, raised "
            "math scores by about four tenths of a standard deviation, <bookmark mark='d'/> and reading by about "
            "one sixth. <bookmark mark='e'/> So the status is: depends on the setting. Which schools are sought "
            "after tells you little about which ones teach more. The dial returns in part forty-nine."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag), FadeIn(zero))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("e")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()
