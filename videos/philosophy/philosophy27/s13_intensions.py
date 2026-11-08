from __future__ import annotations

from videos.philosophy.philosophy27.common import *  # noqa: F403

WORLDS3 = ["w1", "w2", "w3"]
TALLEST = {"w1": "Ortcutt", "w2": "Ann", "w3": "Ortcutt"}
SNOW = {"w1": True, "w2": True, "w3": False}


class Intensions(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"Intensions and omniscience", r"Are propositions sets of worlds?",
                            lit=(1962, 2019), part=PART)
        with self.voiceover("Chapter twelve. Intensions and omniscience."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.intension()
        self.omniscience()
        self.responses()

    def intension(self):
        head = label(r"Intensions: \ functions from worlds", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"\text{expression}"] + [rf"\text{{{w}}}" for w in WORLDS3] + [r"\text{its intension}"]
        cells = [[label(r"`Ortcutt'", font_size=20, color=NAME)] +
                 [label(r"Ortcutt", font_size=20, color=REF) for _ in WORLDS3] +
                 [label(r"constant: \ rigid", font_size=19, color=OK)],
                 [label(r"`the tallest spy'", font_size=20, color=NAME)] +
                 [label(TALLEST[w], font_size=20, color=REF) for w in WORLDS3] +
                 [label(r"varies", font_size=19, color=BAD)],
                 [label(r"`snow is white'", font_size=20, color=NAME)] + [tv(SNOW[w], 22) for w in WORLDS3] +
                 [label(r"the set $\{w_1, w_2\}$", font_size=19, color=SENSE)]]
        assert [w for w in WORLDS3 if SNOW[w]] == ["w1", "w2"] and len(set(TALLEST.values())) == 2
        grid = ValueGrid(hd, cells, col_w=[3.2, 1.6, 1.6, 1.6, 3.4], cell_h=0.55, font_size=21).move_to([0, 0.6, 0])
        rows = stack([(r"Carnap \ (1947): \ extension at a world; \ intension: \ the function from worlds to "
                       r"extensions", HIST),
                      (r"a proposition: \ the set of worlds where a sentence is true \ (Lewis, \ Stalnaker)", SENSE),
                      (r"Frege's senses, \ made precise as functions", GOAL)], font_size=21, aligned_edge=LEFT,
                     width=12.0, buff=0.25).move_to([0, -1.9, 0])
        with self.voiceover(
            "Possible worlds, from Part 22, give the cleanest precise version of Frege's senses. "
            "<bookmark mark='a'/>Take three worlds. A name like Ortcutt picks out the same man in each. "
            "<bookmark mark='b'/>A description like the tallest spy picks out different people in different worlds. "
            "<bookmark mark='c'/>And a sentence like snow is white is true in some worlds and false in others. "
            "<bookmark mark='d'/>Rudolf Carnap, in 1947, called what an expression picks out at a world its extension "
            "there, and the function from worlds to extensions its intension. <bookmark mark='e'/>A sentence's "
            "intension is, in effect, a set of worlds: the worlds where it is true. David Lewis and Robert Stalnaker "
            "took that set to be the proposition it expresses. <bookmark mark='f'/>Senses, which Frege left "
            "mysterious, become mathematical objects."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            for mk, r in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(*[FadeIn(x) for x in grid.cell[r]])
            for mk, r in zip("def", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def omniscience(self):
        d = load("omni")
        head = label(r"The problem of logical omniscience", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["worlds"] == 4 and d["propositions"] == 15 and d["formulas"] == 786 and d["tautologies"] == 212
        nums = VGroup(
            VGroup(MathTex(str(d["formulas"]), font_size=60, color=NAME),
                   label(r"formulas built from $p$, $q$", font_size=19, color=GREY_A)).arrange(DOWN, buff=0.15),
            VGroup(MathTex(str(d["propositions"]), font_size=60, color=SENSE),
                   label(r"distinct sets of worlds", font_size=19, color=GREY_A)).arrange(DOWN, buff=0.15),
            VGroup(MathTex(str(d["tautologies"]), font_size=60, color=TRUTH),
                   label(r"tautologies: \ all one set, \ every world", font_size=19, color=GREY_A)).arrange(
                DOWN, buff=0.15)).arrange(RIGHT, buff=1.3).move_to([0, 1.1, 0])
        arrow = Arrow(nums[0].get_right(), nums[1].get_left(), buff=0.2, color=GREY_B)
        rows = stack([(r"belief as a set of worlds: \ to believe $\varphi$ is for $\varphi$ to hold in all of them", SENSE),
                      (r"then believing anything means believing all its logical consequences", BAD),
                      (r"`2 + 2 = 4' and Fermat's last theorem: \ the same proposition, \ the set of all worlds", BAD),
                      (r"Hintikka \ (1962): \ the logic of knowledge has this built in", HIST)], font_size=21,
                     aligned_edge=LEFT, width=12.0, buff=0.25).move_to([0, -1.6, 0])
        with self.voiceover(
            "But sets of worlds are too coarse. <bookmark mark='a'/>The Reasoner builds every formula from two "
            "letters, p and q, with not, and, or and if, nested two deep: seven hundred and eighty-six formulas. "
            "<bookmark mark='b'/>Over the four worlds that settle p and q, they express only fifteen different sets "
            "of worlds. <bookmark mark='c'/>And the two hundred and twelve tautologies among them all express the "
            "same one: the set of every world. <bookmark mark='d'/>Now model belief the same way, as a set of worlds "
            "the believer cannot rule out. <bookmark mark='e'/>Then anyone who believes anything believes all its "
            "logical consequences. <bookmark mark='f'/>Two plus two is four and Fermat's last theorem express the same "
            "proposition, so believing one is believing the other, and, on this model, every mathematician knew "
            "Fermat's theorem long before Andrew Wiles proved it. <bookmark mark='g'/>Jaakko Hintikka's logic of knowledge, of 1962, has "
            "this property built in. It is called the problem of logical omniscience."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(nums[0]))
            vo.wait_until("b")
            self.play(GrowArrow(arrow), FadeIn(nums[1]))
            vo.wait_until("c")
            self.play(FadeIn(nums[2]))
            for mk, r in zip("defg", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def responses(self):
        head = label(r"Finer than worlds", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"impossible worlds", r"add worlds where logic fails, \ so that distinct necessary truths differ \ "
                                   r"(Part 22; \ Berto and Jago, \ 2019)", WORLD),
            (r"structured propositions", r"a proposition has parts, \ like a sentence: \ Russell; \ Soames; \ King",
             SENSE),
            (r"fragmentation", r"a mind holds several belief states, \ each closed under logic, \ that it never "
                               r"combines \ (Stalnaker)", SPEAK),
            (r"hyperintensionality", r"contexts that distinguish even necessarily equivalent sentences: \ belief, \ "
                                     r"explanation, \ grounding", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "There are four main responses. <bookmark mark='a'/>Add impossible worlds, where logic fails, so that "
            "different necessary truths come apart, as Part 22 described. <bookmark mark='b'/>Give propositions "
            "structure, like sentences, with parts, a view going back to Russell and defended today by Scott Soames "
            "and Jeffrey King. <bookmark mark='c'/>Or keep the worlds, and say with Robert Stalnaker that a mind holds "
            "several separate belief states, each closed under logic, which it never puts together. "
            "<bookmark mark='d'/>Whatever the answer, contexts like belief are hyperintensional: they distinguish "
            "even sentences true in exactly the same worlds. That is the setting of the next chapter."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
