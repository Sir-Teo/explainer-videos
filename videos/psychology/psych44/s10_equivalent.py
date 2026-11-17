from __future__ import annotations

from videos.psychology.psych44.common import *  # noqa: F403
from videos.psychology.psych44.diagrams import three


class Equivalent(VoiceoverScene):
    def construct(self):
        self.card()
        self.four()
        self.lesson()

    def card(self):
        card = chapter_card(9, r"Equivalent models", r"Can the data choose the direction of the arrows?",
                            lit={1993: r"MacCallum et al."}, part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter nine. Equivalent models."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def four(self):
        d = load("equivalent")
        head = heading(r"Four diagrams, \ one matrix")
        kinds = (("chain", r"X causes M, \ M causes Y"), ("reverse", r"Y causes M, \ M causes X"),
                 ("fork", r"M causes both"), ("collider", r"X and Y both cause M"))
        cols = (MODEL, MODEL, MODEL, AUTH)
        panels = VGroup()
        for (k, txt), c in zip(kinds, cols):
            dg = three(k, color=c).scale(0.6)
            stat = label(rf"$\chi^2 = {d[k]:.1f}$ on 1 df", font_size=16, color=c)
            panels.add(VGroup(dg, wrapped_label(txt, 4.6, 16, GREY_A), stat).arrange(DOWN, buff=0.18))
        panels.arrange_in_grid(2, 2, buff=(1.2, 0.5)).move_to([0, 0.3, 0])
        foot = rows_of([
            (r"the first three imply the same conditional independence, \ X and Y independent given M, \ so they fit "
             r"identically, \ always", MODEL),
            (r"the collider implies something else, \ X and Y independent, \ and these data reject it", AUTH),
        ], 12.4, 20, 0.3).move_to([0, -2.7, 0])
        tag = psyche_tag(rf"\texttt{{sem.markov\_equivalent}}, \ {num(d['n'])} simulated people")
        with self.voiceover(
            "Psyche makes three variables, with X causing M and M causing Y. Now fit four diagrams. "
            "<bookmark mark='a'/> The true chain. <bookmark mark='b'/> The chain reversed: Y causes M, M causes X. "
            "<bookmark mark='c'/> A fork: M causes both. <bookmark mark='d'/> The first three fit identically, "
            "to every decimal. They imply the same thing, that X and Y are independent given M. The data can't "
            "choose among them, ever. <bookmark mark='e'/> Only the collider differs. It says X and Y are independent, "
            "and the data reject it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, p in zip("abc", panels[:3]):
                vo.wait_until(m)
                self.play(FadeIn(p))
            vo.wait_until("d")
            self.play(FadeIn(foot[0]))
            vo.wait_until("e")
            self.play(FadeIn(panels[3]), FadeIn(foot[1]))
        self.clear_scene()

    def lesson(self):
        head = heading(r"What fit cannot tell you")
        rows = rows_of([
            (r"MacCallum and colleagues, \ 1993: \ for most published models there were equivalent models, \ often "
             r"many, \ with arrows reversed or replaced by correlations", PERSON),
            (r"in a survey of 53 published applications, \ almost none acknowledged them", AUTH),
            (r"a good fit says the model is one of a family that the data cannot tell apart; \ the arrows come from "
             r"design, \ time order and theory, \ not from the fit", MODEL),
            (r"Part 2's lesson again: \ a direction is something an experiment tests, \ not something a "
             r"correlation matrix announces", YOU),
        ], 12.4, 22, 0.44).move_to([0, -0.2, 0])
        tag = published_tag(r"MacCallum et al. (1993)")
        with self.voiceover(
            "This is general. <bookmark mark='a'/> In 1993 Robert MacCallum and colleagues showed that most "
            "published models had equivalent models, often many, with arrows reversed or replaced by correlations. "
            "<bookmark mark='b'/> In a survey of fifty-three published applications, almost none acknowledged them. "
            "<bookmark mark='c'/> A good fit says the model belongs to a family the data can't tell apart. The arrows "
            "come from design, time order and theory, not from the fit. <bookmark mark='d'/> It's Part 2's lesson "
            "again. A direction is something an experiment tests, not something a correlation matrix announces."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
