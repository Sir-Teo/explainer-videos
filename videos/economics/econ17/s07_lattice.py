from __future__ import annotations

from videos.economics.econ17.common import *  # noqa: F403

APPS = ("ana", "bo", "chidi", "dara")


class Lattice(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Who should propose?", r"A market can have several stable matchings. \ Which one does the "
             r"algorithm pick, \ and who gains?", "Chapter six. Who should propose?",
             lit={1962: r"Gale and Shapley", 1981: r"Dubins and Freedman", 1982: r"Roth"},
             scale=("person", "market"), horizon=("a year",))
        self.three()
        self.truth()

    def three(self):
        la = load("lattice")
        st = la["stable"]
        names = [r"apprentices propose", r"in between", r"workshops propose"]
        cols = [PROPOSE, GREY_A, PLACES["loft"]]
        rows = VGroup()
        for s, nm, c in zip(st, names, cols):
            pairs = r", \ ".join(rf"{island.CAST[a].name}--{PLACE_NAMES[w].replace('the ', '')}"
                                 for a, w in s["match"].items())
            ar = r" \ ".join(str(s["a_ranks"][a]) for a in APPS)
            wr = r" \ ".join(str(s["w_ranks"][w]) for w in ("boatyard", "kiln", "loft", "grove"))
            rows.add(VGroup(label(nm, font_size=22, color=c), label(pairs, font_size=19),
                            label(rf"apprentices' ranks: \ {ar} \quad workshops' ranks: \ {wr}", font_size=18,
                                  color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(LEFT * 0.9 + DOWN * 0.1)
        arrow = DoubleArrow(rows[0].get_right() + RIGHT * 0.5, rows[2].get_right() + RIGHT * 0.5, color=GREY_B,
                            buff=0.1)
        al = VGroup(label(r"better for \\ apprentices", font_size=18, color=PROPOSE).next_to(arrow.get_top(), RIGHT,
                                                                                         buff=0.15),
                    label(r"better for \\ workshops", font_size=18, color=PLACES["loft"]).next_to(arrow.get_bottom(),
                                                                                              RIGHT, buff=0.15))
        head = label(r"the board has three stable matchings", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.35)
        foot = label(r"every apprentice likes the top one best of the three; \ every workshop likes it least",
                     font_size=22, color=E.ACCENT).to_edge(DOWN, buff=0.4)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Agora checked every one of the twenty-four ways to pair the board, and three are stable. "
            "<bookmark mark='a'/> The algorithm we ran, with apprentices asking, found the top one. "
            "<bookmark mark='b'/> Run it the other way round, with workshops asking, and it finds the bottom one, "
            "in two rounds. <bookmark mark='c'/> And there is one in between. <bookmark mark='d'/> They line up: "
            "every apprentice likes the top matching at least as well as the other two, and every workshop likes "
            "it least. It is a general fact. The asking side gets its best stable matching, as Gale and Shapley "
            "proved, and, as later work showed, the other side gets its worst. Interests are opposed along the line, and the stable matchings "
            "form what mathematicians call a lattice."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(GrowFromCenter(arrow), FadeIn(al), FadeIn(foot))
        self.clear_scene()

    def truth(self):
        rows = VGroup(
            label(r"for the side that asks, \ telling the truth is a dominant strategy", font_size=25, color=PROPOSE),
            label(r"Dubins and Freedman (1981); \ Roth (1982)", font_size=20, color=GREY_A),
            label(r"for the side that is asked, \ a well-judged lie can sometimes pay", font_size=25, color=REJECT),
            label(r"no stable rule makes the truth safe for everyone \ (Roth 1982)", font_size=24, color=GREY_A),
            label(r"but in a large market, \ almost nobody on either side can gain by lying", font_size=25,
                  color=STABLE),
            label(r"so a designer chooses who asks, \ and in large markets it hardly matters: \ the doctors switched "
                  r"in 1998", font_size=23, color=E.ACCENT),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Dubins and Freedman, Amer.\ Math.\ Monthly 88(7) (1981); \ Roth, Math.\ Oper.\ Res.\ "
                            r"7(4) (1982); \ Roth and Peranson, AER 89(4) (1999)", corner=DR, font_size=12)
        with self.voiceover(
            "Who asks matters for honesty too. <bookmark mark='a'/> For the side that asks, telling the truth is a "
            "dominant strategy: no list you could write gets you a better partner. <bookmark mark='b'/> Lester "
            "Dubins and David Freedman proved it in 1981, and Roth independently in 1982. <bookmark mark='c'/> For "
            "the side that is asked, a carefully judged lie, turning down someone you would accept, can sometimes "
            "push the outcome down the lattice in your favour. <bookmark mark='d'/> And Roth showed that no "
            "stable rule makes the truth safe for everyone. <bookmark mark='e'/> But in a large market, with many "
            "people on each side, the room for such lies nearly vanishes: almost nobody can gain. "
            "<bookmark mark='f'/> So a designer chooses who asks, and in a large market the choice hardly changes "
            "anything. The doctors' match switched to applicants asking in 1998, as chapter seven tells."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
