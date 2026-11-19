from __future__ import annotations

from videos.economics.econ18.common import *  # noqa: F403


class Comparisons(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Comparing people: \ Sen's enlargement", r"If we can say who is worse off, \ or who gains more, "
             r"\ does Arrow's wall come down?", "Chapter six. Comparing people: Sen's enlargement.",
             lit={1932: r"Robbins", 1970: r"Sen", 1977: r"d'Aspremont and Gevers"}, scale=("person", "nation"),
             horizon=("a decade",))
        self.robbins()
        self.grid()

    def robbins(self):
        rows = VGroup(
            label(r"Arrow used only rankings: \ who prefers what, \ not by how much, \ nor who is better off",
                  font_size=24),
            label(r"Lionel Robbins, \ 1932: \ comparing one person's satisfaction with another's is not science",
                  font_size=24, color=GREY_A),
            label(r"but every judgment that a policy helps the poor more than it hurts the rich makes one",
                  font_size=24, color=RAWLS),
            label(r"Amartya Sen, \ 1970: \ the impossibility comes from the poverty of the information, \ not from "
                  r"democracy", font_size=23, color=E.ACCENT),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Robbins, \emph{An Essay on the Nature and Significance of Economic Science} (1932); \ "
                            r"Sen, \emph{Collective Choice and Social Welfare} (1970)", corner=DR, font_size=12)
        with self.voiceover(
            "The third way out asks for more information. <bookmark mark='a'/> Arrow's rules used only rankings: who "
            "prefers what, but not by how much, and not who is better off than whom. <bookmark mark='b'/> That was "
            "deliberate. In 1932 Lionel Robbins had argued that comparing one person's satisfaction with another's "
            "is not science, and a generation of economists agreed. <bookmark mark='c'/> But every judgment that a "
            "policy helps the poor more than it hurts the rich makes exactly such a comparison. "
            "<bookmark mark='d'/> Amartya Sen argued from 1970 that the impossibility comes from the poverty of the "
            "information allowed, not from democracy itself."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def grid(self):
        head = label(r"what we may compare, \ and the rules it allows", font_size=28, color=E.ACCENT).to_edge(UP,
                                                                                                   buff=0.35)
        cells = [
            (r"only rankings", r"Arrow: \\ a dictator", CYCLE),
            (r"who is worse off \\ (levels)", r"Rawls: \\ help the worst-off first", RAWLS),
            (r"who gains more \\ (units)", r"Bentham: \\ maximize the sum", HARS),
            (r"levels and units", r"a family between: \\ Atkinson, \ chapter seven", WELF),
        ]
        cards = VGroup()
        for i, (k, v, c) in enumerate(cells):
            box = RoundedRectangle(width=5.6, height=1.9, corner_radius=0.15, stroke_color=c, stroke_width=3)
            t = VGroup(label(k, font_size=22, color=GREY_A), label(v, font_size=25, color=c)).arrange(DOWN, buff=0.18)
            t.move_to(box)
            cards.add(VGroup(box, t))
        cards.arrange_in_grid(2, 2, buff=0.4).next_to(head, DOWN, buff=0.45)
        foot = label(r"add comparability, \ keep Arrow's other conditions, \ and the rules that survive are these",
                     font_size=22, color=GREY_A).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"Hammond, Econometrica 44(4) (1976); \ d'Aspremont and Gevers, RES 44(2) (1977)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "In the 1970s, several economists worked out what each kind of comparison allows. "
            "<bookmark mark='a'/> With only rankings, Arrow's conditions leave a dictator. <bookmark mark='b'/> If "
            "we may say who is worse off, the conditions allow Rawls's rule: improve the lot of the worst-off "
            "first. <bookmark mark='c'/> If we may say who gains more, they allow Bentham's: maximize the sum. "
            "<bookmark mark='d'/> With both, a whole family between them opens up, which chapter seven measures. "
            "Peter Hammond, Claude d'Aspremont and Louis Gevers proved versions of these results. The choice of rule "
            "is then a choice of how to compare people, which is an ethical choice, made openly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            self.play(FadeIn(foot))
        self.clear_scene()
