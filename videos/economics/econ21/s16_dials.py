from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ21.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 14, r"The Dials: \ the return to research, \ and misallocation", r"What is a dollar of research "
             r"worth to society, \ and how much does misallocation cost?",
             "Chapter fourteen. The Dials: the return to research, and misallocation.", scale=("firm", "nation"),
             lit={1998: r"Jones and Williams", 2013: r"Bloom et al.", 2019: r"Lucking et al."})
        self.rd()
        self.gap()

    def rd(self):
        dial = dials.DIALS["social_return_rd"]
        head = status_head(dial, r"the social return to R\&D \ (new)")
        frame, rows = dial_rows(dial, 0, 70, [0, 10, 20, 30, 40, 50, 60, 70], r"percent a year", top=1.6, step=0.95,
                                fmt="{:.0f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 12.6, 17, GREY_A).to_edge(DOWN, buff=0.2)
        tag = published_tag(r"Jones and Williams (1998); \ Bloom, Schankerman and Van Reenen (2013); \ Lucking, Bloom "
                            r"and Van Reenen (2019)", corner=UR, font_size=12)
        jw, bsv, lbv = dial.estimates
        with self.voiceover(
            "This part opens a dial: the social rate of return to research and development, what a dollar of R and "
            "D returns to society each year, counting what it does for other firms. <bookmark mark='a'/> Charles "
            "Jones and John Williams showed that the usual regression estimates are a lower bound, and took thirty "
            "percent as a conservative value: at that return, the optimal amount of research is two to four times "
            "what America does. <bookmark mark='b'/> Nicholas Bloom, Mark Schankerman and John Van Reenen separated "
            "the spillovers that help other firms from the business stealing that hurts rivals, using American "
            f"firms from 1981 to 2001: a social return of about {bsv.value:.0f} percent, against a private return of "
            "21. <bookmark mark='c'/> Redone on three decades of data by Brian Lucking and the same authors: "
            f"{lbv.value:.0f} percent, against a private return of 14. <bookmark mark='d'/> The status: settled "
            "within a range. The social return is large and several times the private one. The market does too "
            "little research, which is the case for subsidizing it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("d")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        del jw
        self.clear_scene()

    def gap(self):
        rows = VGroup(
            label(r"what the dials say together", font_size=30, color=E.ACCENT),
            label(r"research: \ the market does too little, \ by a factor of two to four", font_size=24, color=IDEA),
            label(r"misallocation: \ tens of percent of manufacturing output, \ contested by measurement error",
                  font_size=24, color=WEDGE),
            label(r"so the residual is not one thing: \ ideas found, \ ideas adopted, \ ideas used well", font_size=24,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.5).move_to(UP * 0.1)
        with self.voiceover(
            "Put the two dials side by side. <bookmark mark='a'/> On research, the evidence says the market does "
            "too little, perhaps by a factor of two to four. <bookmark mark='b'/> On misallocation, the gains from "
            "moving resources to better firms could be tens of percent of manufacturing output in poor countries, "
            "though measurement error inflates them. <bookmark mark='c'/> The residual, in other words, is not one "
            "thing. It is ideas found, ideas adopted and ideas used well, and each has its own policy."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r in zip("abc", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
