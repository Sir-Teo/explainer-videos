from __future__ import annotations

from videos.philosophy.philosophy28.common import *  # noqa: F403


class Quine(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"Gavagai", r"Is there a fact of the matter about translation?", lit=(1960,), part=PART)
        with self.voiceover("Chapter five. Gavagai."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.field()
        self.indeterminacy()
        self.proxy()
        self.responses()

    def field(self):
        d = load("gavagai")
        hc = history_card(1960, r"W. V. O. Quine", r"\textit{Word and Object}", width=4.8, color=HIST).to_corner(UL,
                                                                                                     buff=0.3)
        assert d["same_assent"] and d["scenes"] == 40
        rabbit = VGroup(Ellipse(width=1.0, height=0.6, color=GREY_A, fill_opacity=0.5),
                        Ellipse(width=0.25, height=0.6, color=GREY_A, fill_opacity=0.5).shift(UP * 0.45 + RIGHT * 0.3),
                        Ellipse(width=0.25, height=0.6, color=GREY_A, fill_opacity=0.5).shift(UP * 0.45 + RIGHT * 0.05)
                        ).move_to([-4.0, -0.8, 0])
        said = label(r"`Gavagai!'", font_size=30, color=WORD).move_to([-4.0, 0.6, 0])
        hd = [r"\text{translation}", r"\text{assents in scenes}"]
        cells = [[label(h, font_size=21, color=USE), label(rf"the same {d['rabbits']} of {d['scenes']}", font_size=21,
                                                            color=OK)] for h in d["hypotheses"]]
        grid = ValueGrid(hd, cells, col_w=[4.2, 3.4], cell_h=0.55, font_size=21).move_to([2.6, 0.3, 0])
        foot = label(r"same stimulus meaning: \ no observation can choose between them", font_size=22,
                     color=GOAL).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "W. V. O. Quine, in Word and Object of 1960, imagined a linguist among speakers of a language no one has "
            "translated. <bookmark mark='a'/>A rabbit scurries by, and a speaker says: Gavagai! The linguist writes "
            "down, tentatively, gavagai means rabbit. <bookmark mark='b'/>But it could mean undetached rabbit part, or "
            "rabbit stage, a temporal slice of a rabbit. The Reasoner shows the speaker forty scenes and asks "
            "gavagai? under each hypothesis. In every scene with a rabbit there are also undetached rabbit parts and "
            "a rabbit stage, so the speaker assents in exactly the same twenty scenes. <bookmark mark='c'/>The three "
            "translations have the same stimulus meaning. No observation of when speakers assent can choose between "
            "them."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(rabbit), FadeIn(said))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(cells)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.5)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def indeterminacy(self):
        head = label(r"The indeterminacy of translation", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the thesis", r"manuals of translation can fit every disposition to speech behaviour, \ and still be "
                            r"incompatible with each other", WORLD),
            (r"the mechanism", r"adjust the translation of `is the same as', \ plurals and pronouns, \ and `rabbit' "
                               r"can become `rabbit part' consistently, \ everywhere", RULE_C),
            (r"no fact of the matter", r"not that we cannot find out which manual is right: \ there is nothing to find",
             BAD),
            (r"not just physics", r"Quine: \ physics is underdetermined by data, \ but within it there is a truth; \ "
                                  r"translation has none over and above behaviour", HIST),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "Quine drew a sweeping conclusion. <bookmark mark='a'/>Manuals for translating one language into another "
            "can be set up in divergent ways, all compatible with the totality of speech dispositions, yet "
            "incompatible with one another. <bookmark mark='b'/>The trick is to adjust everything together: translate "
            "the native expressions for same, for plurals and for pronouns differently, and rabbit part can replace "
            "rabbit everywhere without any mismatch with behaviour. <bookmark mark='c'/>And this is not ignorance. "
            "There is, Quine says, no fact of the matter about which manual is right. <bookmark mark='d'/>Physics, "
            "too, is underdetermined by the evidence, but Quine held that within our best physics there is a fact. "
            "In translation there is no fact beyond behaviour at all."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def proxy(self):
        d = load("proxy")
        head = label(r"Proxy functions, \ computed", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        perm = d["permutation"]
        dom = sorted(perm)
        top = VGroup(*[label(x, font_size=26, color=WORLD) for x in dom]).arrange(RIGHT, buff=0.8).move_to([-3.0, 1.5, 0])
        bot = VGroup(*[label(perm[x], font_size=26, color=USE) for x in dom]).arrange(RIGHT, buff=0.8).move_to(
            [-3.0, -0.2, 0])
        arrows = VGroup(*[Arrow(t.get_bottom(), b.get_top(), buff=0.1, color=RULE_C if perm[x] != x else GREY_C,
                                stroke_width=3, max_tip_length_to_length_ratio=0.15) for x, t, b in zip(dom, top, bot)])
        ftag = label(r"a permutation $f$ of the domain", font_size=19, color=RULE_C).next_to(top, UP, buff=0.2)
        assert d["sentences"] == 300 and d["same_truth_value"] == 300 and d["predicates_changed"] == 2
        rset = label(r"$R$ was true of \{" + ", ".join(d["R_before"]) + r"\}; \ reinterpreted, \ of \{" +
                     ", ".join(d["R_after"]) + r"\}", font_size=20, color=WORD).move_to([-3.0, -1.4, 0])
        side = stack([(r"carry every predicate along: \ $P' = f[P]$", RULE_C),
                      (r"300 random sentences of first-order logic: \ every one keeps its truth value", OK),
                      (r"yet the names and predicates now apply to different things", BAD),
                      (r"truth fixes sentences; \ it does not fix reference: \ the inscrutability of reference \ "
                       r"(`Ontological Relativity', \ 1968)", GOAL)], font_size=20, aligned_edge=LEFT, width=5.6,
                     buff=0.28).move_to([3.9, -0.1, 0])
        with self.voiceover(
            "Quine made the point exact with what he called proxy functions. <bookmark mark='a'/>Take a model with "
            "five objects, and a permutation of them. <bookmark mark='b'/>Now reinterpret every predicate: wherever R "
            "was true of an object, make it true of that object's image. <bookmark mark='c'/>The Reasoner generates "
            "three hundred random sentences of first-order logic and evaluates each under both interpretations. Every "
            "one keeps its truth value. <bookmark mark='d'/>Yet the predicate R, which applied to a and c, now applies "
            "to a and e. <bookmark mark='e'/>So the truth values of all our sentences, the most any evidence could "
            "fix, leave reference unfixed. Quine called it the inscrutability of reference."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(top), FadeIn(ftag))
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15), FadeIn(bot))
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(rset), FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def responses(self):
        head = label(r"Replies", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Chomsky", r"this is only the ordinary underdetermination of theory by evidence, \ found in every science",
             HIST),
            (r"Lewis", r"some properties are more natural than others: \ `rabbit' is a joint in nature, \ `rabbit stage "
                       r"or prime number' is not; \ reference is drawn to the natural \ (1983)", WORLD),
            (r"Davidson", r"interpretation is constrained by charity, \ across a whole theory of truth: \ the next "
                          r"chapter", USE),
            (r"the stakes", r"if reference is inscrutable, \ so are Part 27's semantic values, \ except relative to a "
                            r"chosen manual", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "There are three main replies. <bookmark mark='a'/>Noam Chomsky argued that this is just the "
            "underdetermination of theory by evidence that every science faces, and gives no special reason to doubt "
            "facts about meaning. <bookmark mark='b'/>David Lewis argued in 1983 that some properties are more natural "
            "than others. Rabbit carves nature at a joint; rabbit-stage-or-prime-number does not. Reference is drawn "
            "toward the natural, as by a magnet. <bookmark mark='c'/>And Donald Davidson tied interpretation to a "
            "principle of charity, applied across a whole theory: the next chapter. <bookmark mark='d'/>What is at "
            "stake: if reference is inscrutable, so are all of Part 27's semantic values, except relative to a "
            "manual we choose."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
