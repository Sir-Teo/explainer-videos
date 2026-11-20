from __future__ import annotations

from videos.economics.econ21.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 16, r"Frontier: \ growth with fewer people", r"If ideas come from people, \ what happens to growth "
             r"when the world's population starts to fall?", "Chapter sixteen. Frontier: growth with fewer people.",
             lit={2019: r"AI and growth", 2022: r"The End of Economic Growth?"}, scale=("world",),
             horizon=("a century",))
        self.empty()
        self.machines()
        self.open_()

    def empty(self):
        s = load("semi")
        rows = VGroup(
            MathTex(r"g_A = \frac{\lambda\, n}{1 - \phi}", font_size=54, color=IDEA),
            label(r"semi-endogenous growth: \ the growth of ideas follows the growth of researchers", font_size=23,
                  color=GREY_A),
            label(r"fertility in rich countries is below replacement; \ the UN projects world population to peak, \ "
                  r"then fall \ (Part 19)", font_size=22, color=WEDGE),
            label(r"with $n < 0$: \ the stock of ideas stops growing, \ and living standards stagnate", font_size=23,
                  color=WEDGE),
            label(r"Charles Jones, \ 2022: \ ``an empty planet''; \ even an optimal policy can be trapped if it starts "
                  r"too late", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Jones, AER 112(11) (2022): \ 3489--3527, \ abstract", corner=DR, font_size=12)
        with self.voiceover(
            "The semi-endogenous model ends with an unsettling implication. <bookmark mark='a'/> Long-run growth of "
            "ideas is proportional to the growth of the number of researchers, n. <bookmark mark='b'/> In the "
            "long run, that means the growth of population. <bookmark mark='c'/> Fertility in the rich countries is "
            "already below replacement, and the United Nations projects the world's population to peak this century "
            "and then decline, as part nineteen showed. <bookmark mark='d'/> If population shrinks, n turns "
            "negative, the stock of ideas stops growing, and living standards stagnate. "
            "<bookmark mark='e'/> Charles Jones worked this out in 2022: rather than continued exponential growth, "
            "living standards stagnate for a population that vanishes, and even an optimal policy can be caught in "
            "that trap if it begins too late."
        ) as vo:
            self.play(Write(rows[0]), FadeIn(tag))
            for mk, r in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        del s
        self.clear_scene()

    def machines(self):
        rows = VGroup(
            label(r"unless researchers need not be people", font_size=28, color=E.ACCENT),
            label(r"if machines can do part of research, \ the researchers in $n$ can grow without more people",
                  font_size=23, color=RESEARCH),
            label(r"Aghion, \ Jones and Jones, \ 2019: \ automation of idea production could raise growth, \ "
                  r"or even bring a singularity", font_size=22, color=IDEA),
            label(r"or the hardest tasks, \ the ones machines cannot do, \ set the pace: \ Baumol's cost disease",
                  font_size=22, color=HOLD),
            label(r"Part 65 takes this up: \ the economics of AI", font_size=23, color=GREY_A),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Aghion, Jones and Jones, in Agrawal, Gans and Goldfarb (eds), \emph{The Economics of "
                            r"Artificial Intelligence} (2019)", corner=DR, font_size=12)
        with self.voiceover(
            "There is an escape, and it is the subject of a later part. <bookmark mark='a'/> The model needs "
            "researchers, not people. <bookmark mark='b'/> If machines can do part of the work of research, the "
            "effective number of researchers can grow even when the population does not. <bookmark mark='c'/> "
            "Philippe Aghion, Benjamin Jones and Charles Jones showed that automating the production of ideas could "
            "raise growth, in some versions without limit. <bookmark mark='d'/> Or growth could be held back by the "
            "tasks machines cannot do, as the slowest sectors set the pace in William Baumol's cost disease. "
            "<bookmark mark='e'/> Part sixty-five takes up the economics of artificial intelligence."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def open_(self):
        cards = point_cards([
            (r"research productivity", r"why ideas get harder: \\ fishing out, \ or burden of knowledge?", IDEA),
            (r"misallocation", r"real, \ or measurement error?", WEDGE),
            (r"institutions", r"how they change, \\ and how to change them", INST),
            (r"population and AI", r"who, \ or what, \\ will do the research?", RESEARCH),
        ], width=12.6, cols=2, font_size=23).move_to(DOWN * 0.2)
        head = label(r"open questions", font_size=34, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Four questions for a doctoral student. <bookmark mark='a'/> Why ideas get harder to find: the easy "
            "ones fished out, or a growing burden of knowledge that each new researcher must master. "
            "<bookmark mark='b'/> How much measured misallocation is real. <bookmark mark='c'/> How institutions "
            "change, and whether outsiders can help. <bookmark mark='d'/> And who, or what, will do the research of "
            "the next century."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
