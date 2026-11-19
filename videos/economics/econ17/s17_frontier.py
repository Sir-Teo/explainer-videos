from __future__ import annotations

from videos.economics.econ17.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ refugees, \ learning and large markets", r"What can matching do with data, \ and "
             r"what does it look like when the market is huge?", "Chapter fifteen. Frontier: refugees, learning and "
             "large markets.", lit={2009: r"Kojima and Pathak", 2016: r"Azevedo and Leshno", 2018: r"Bansak et al."},
             scale=("person", "nation", "world"), horizon=("a decade",))
        self.refugees()
        self.cutoffs()
        self.open_q()

    def refugees(self):
        rows = VGroup(
            label(r"refugee families are placed in towns by rules of thumb and the space available",
                  font_size=23),
            label(r"where a family lands can decide whether its adults find work", font_size=23, color=HELD),
            label(r"Kirk Bansak and colleagues, \ 2018: \ learn from past arrivals who found work where", font_size=23,
                  color=MECH),
            label(r"then match each family to the place where it is predicted to do best, \ within capacities",
                  font_size=23, color=STABLE),
            label(r"predicted employment: \ roughly 40 to 70 percent higher, \ in the United States and Switzerland",
                  font_size=23, color=E.ACCENT),
            label(r"a prediction from past data, \ not yet an experiment; \ and the families' own wishes must count",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Bansak et al., Science 359(6373) (2018)", corner=DR, font_size=13)
        with self.voiceover(
            "The newest matching markets learn from data. <bookmark mark='a'/> Refugee families are placed in "
            "towns by rules of thumb and the space available. <bookmark mark='b'/> Yet where a family "
            "lands can decide whether its adults find work. <bookmark mark='c'/> In 2018 Kirk Bansak and colleagues "
            "used past arrivals to learn which kinds of families found work in which places, "
            "<bookmark mark='d'/> and then matched each new family to where it was predicted to do best, within "
            "each place's capacity. <bookmark mark='e'/> Their predicted employment rates were roughly forty to "
            "seventy percent higher, using data from the United States and Switzerland. "
            "<bookmark mark='f'/> These are predictions from past data, not yet the results of an experiment, and a "
            "design must also count what the families themselves want."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def cutoffs(self):
        rows = VGroup(
            label(r"in a very large match, \ almost nobody can gain by lying \ (Kojima and Pathak, \ 2009)",
                  font_size=23, color=STABLE),
            label(r"and a stable matching is described by one number per school: \ its cutoff", font_size=23,
                  color=SCHOOL),
            label(r"each student goes to the best school whose cutoff they clear", font_size=23),
            label(r"cutoffs rise when a school is popular, \ like prices: \ supply and demand again \ (Azevedo and "
                  r"Leshno, \ 2016)", font_size=22, color=E.ACCENT),
            label(r"the market without prices has prices after all: \ they are paid in priority, \ not money",
                  font_size=23, color=HELD),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Kojima and Pathak, AER 99(3) (2009); \ Azevedo and Leshno, JPE 124(5) (2016)",
                            corner=DR, font_size=13)
        with self.voiceover(
            "The other frontier is size. <bookmark mark='a'/> Fuhito Kojima and Parag Pathak showed in 2009 that in "
            "a very large match, almost nobody on either side can gain by lying. <bookmark mark='b'/> And Eduardo "
            "Azevedo and Jacob Leshno showed in 2016 that a large stable matching can be described by one number "
            "per school: its cutoff. <bookmark mark='c'/> Each student goes to the best school whose cutoff they "
            "clear. <bookmark mark='d'/> Cutoffs rise when a school is popular, just like prices, and they settle "
            "where the places demanded equal the places available. <bookmark mark='e'/> The market without prices "
            "had prices after all, paid in priority rather than money."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def open_q(self):
        head = label(r"open questions", font_size=32, color=E.ACCENT).to_edge(UP, buff=0.5)
        qs = VGroup(
            label(r"how should a match learn about people while it places them, \ without treating them as "
                  r"experiments?", font_size=23),
            label(r"how should fairness, \ diversity and priority be written into an algorithm?", font_size=23,
                  color=SCHOOL),
            label(r"when should a platform show prices, \ and when should it simply match?", font_size=23,
                  color=MECH),
            label(r"how can a design earn the trust of the people it places?", font_size=23, color=STABLE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "And the open questions. <bookmark mark='a'/> How should a match learn about people while it places "
            "them, without treating them as experiments? <bookmark mark='b'/> How should fairness, diversity and "
            "priority be written into an algorithm? <bookmark mark='c'/> When should a platform show prices, and "
            "when should it simply match? <bookmark mark='d'/> And how can a design earn the trust of the people "
            "it places?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", qs):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
