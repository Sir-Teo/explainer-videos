from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ24.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ the matching elasticity, \ and the worker's share", r"How sensitive are hires "
             r"to the unemployed, \ and how is a match's surplus split?",
             "Chapter thirteen. The Dials: the matching elasticity, and the worker's share.",
             lit={2001: r"Petrongolo and Pissarides", 2006: r"Cahuc, Postel-Vinay, Robin"},
             scale=("market",), horizon=("a month",))
        self.matching()
        self.share()

    def matching(self):
        dial = dials.DIALS["matching"]
        head = status_head(dial, r"the elasticity of matches to unemployment, \ $\eta$ \ (new)")
        frame, rows = dial_rows(dial, 0.0, 1.0, [0, 0.25, 0.5, 0.75, 1.0], r"$\eta$", top=1.6, step=0.85,
                                fmt="{:.2f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 12.6, 17, GREY_A).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"Petrongolo and Pissarides (2001); \ Shimer (2005); \ this film", corner=DR,
                            font_size=12)
        pp, sh, ours, hires = dial.estimates
        with self.voiceover(
            "Two dials. The first is the matching elasticity, eta. <bookmark mark='a'/> Petrongolo and Pissarides's "
            "survey puts it between a half and seven-tenths. <bookmark mark='b'/> Shimer's regression on half a "
            f"century of American data gives {sh.value:.2f}. <bookmark mark='c'/> This film's estimate from "
            f"chapter five, the unemployed's job-finding rate against openings, gives {ours.value:.2f}. "
            "<bookmark mark='d'/> Counting all hires, including people moving between jobs, gives "
            f"{hires.value:.2f}, a reminder that the answer depends on who you count as searching. "
            "<bookmark mark='e'/> The status: settled within a range. It matters twice: for how much unemployment "
            "responds to openings, and, by Hosios's condition, for how big workers' share should be."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("e")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()

    def share(self):
        dial = dials.DIALS["bargaining_share"]
        head = status_head(dial, r"the worker's bargaining share, \ $\beta$ \ (new)")
        frame, rows = dial_rows(dial, 0.0, 1.0, [0, 0.25, 0.5, 0.75, 1.0], r"$\beta$", top=1.4, step=0.95,
                                fmt="{:.2f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 12.6, 17, GREY_A).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"Shimer (2005); \ Hagedorn and Manovskii (2008); \ Cahuc, Postel-Vinay and Robin (2006)",
                            corner=DR, font_size=12)
        sh, hm, cpr = dial.estimates
        with self.voiceover(
            "The second dial is the worker's share of the surplus, beta, and it is much less settled. "
            f"<bookmark mark='a'/> Shimer set it at {sh.value:.2f}, equal to the matching elasticity, so that the "
            f"market is efficient. <bookmark mark='b'/> Hagedorn and Manovskii set it at {hm.value:.2f}, with a "
            "fallback worth ninety-five percent of output, to make unemployment volatile. <bookmark mark='c'/> "
            "Pierre Cahuc, Fabien Postel-Vinay and Jean-Marc Robin estimated a model in which employers also "
            "compete for workers who search on the job, on French data, and found no significant bargaining power "
            "for low- and intermediate-skill workers: what they earn above their fallback comes from competition "
            "between employers. <bookmark mark='d'/> The status: contested. The share cannot be read off wages "
            "without knowing what the alternative to working is worth, which is the same quantity that decides "
            "the volatility puzzle."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("d")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()
