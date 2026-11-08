from __future__ import annotations

from videos.philosophy.philosophy27.common import *  # noqa: F403


def person(x, y, name, col):
    head = Circle(0.25, color=col, fill_opacity=0.35).move_to([x, y + 0.45, 0])
    body = Line([x, y + 0.2, 0], [x, y - 0.5, 0], color=col, stroke_width=3)
    nm = label(name, font_size=19, color=col).next_to(body, DOWN, buff=0.1)
    return VGroup(head, body, nm)


class Twin(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Twin Earth", r"Are meanings in the head?", lit=(1975, 1979), part=PART)
        with self.voiceover("Chapter six. Twin Earth."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.planets()
        self.labour()
        self.arthritis()
        self.debate()

    def planets(self):
        d = load("twin")
        head = label(r"Oscar and Twin Oscar, \ in 1750", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        e = Circle(1.1, color=WORLD, fill_opacity=0.15).move_to([-3.8, 0.9, 0])
        t = Circle(1.1, color=SPEAK, fill_opacity=0.15).move_to([3.8, 0.9, 0])
        el = label(r"Earth", font_size=20, color=WORLD).next_to(e, UP, buff=0.1)
        tl = label(r"Twin Earth", font_size=20, color=SPEAK).next_to(t, UP, buff=0.1)
        lake_e = Ellipse(width=1.2, height=0.45, color=NAME, fill_opacity=0.6).move_to(e.get_center() + DOWN * 0.3)
        lake_t = Ellipse(width=1.2, height=0.45, color=NAME, fill_opacity=0.6).move_to(t.get_center() + DOWN * 0.3)
        fe = MathTex(r"\text{H}_2\text{O}", font_size=24, color=WHITE).move_to(lake_e)
        ft = MathTex(r"\text{XYZ}", font_size=24, color=WHITE).move_to(lake_t)
        o1 = person(-1.6, 0.5, r"Oscar", WORLD)
        o2 = person(1.6, 0.5, r"Twin Oscar", SPEAK)
        rows = d["rows"]
        assert d["same_inner"] and not d["same_extension"]
        bubble = label(r"`water': \ " + rows[0]["inner"], font_size=18, color=GREY_A).move_to([0, 2.0, 0])
        hd = [r"\text{speaker}", r"\text{in the head}", r"\text{extension of `water'}"]
        cells = [[label(r["speaker"], font_size=20, color=WORLD if i == 0 else SPEAK),
                  label(r["inner"], font_size=19, color=GREY_A),
                  MathTex(r"\text{H}_2\text{O}" if r["extension"] == "H2O" else r"\text{XYZ}", font_size=24,
                          color=REF)] for i, r in enumerate(rows)]
        grid = ValueGrid(hd, cells, col_w=[2.4, 5.0, 3.6], cell_h=0.5, font_size=20).move_to([0, -1.9, 0])
        q = label(r"`Cut the pie any way you like, \ \textit{meanings} just ain't in the \textit{head}!' \ (Putnam)",
                  font_size=21, color=GOAL).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "In 1975 Hilary Putnam told a story about a planet. <bookmark mark='a'/>Twin Earth is exactly like Earth, "
            "except that the clear, drinkable liquid in its lakes and rain is not H2O but a different substance, "
            "with a long formula he abbreviated XYZ. <bookmark mark='b'/>Go back to 1750, before chemistry. Oscar on "
            "Earth and his twin on Twin Earth are molecule for molecule alike, and have the same experiences and the "
            "same thoughts about the stuff they call water. <bookmark mark='c'/>Yet Oscar's word water refers to H2O, "
            "and his twin's to XYZ. The Reasoner tabulates it: same state in the head, different extension. "
            "<bookmark mark='d'/>So whatever fixes the extension of water is not in the head. Cut the pie any way "
            "you like, Putnam wrote, meanings just ain't in the head."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(e), FadeIn(el), FadeIn(lake_e), FadeIn(fe), FadeIn(t), FadeIn(tl), FadeIn(lake_t),
                      FadeIn(ft))
            vo.wait_until("b")
            self.play(FadeIn(o1), FadeIn(o2), FadeIn(bubble))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(cells)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.5)
            vo.wait_until("d")
            self.play(FadeIn(q))
        self.clear_scene()

    def labour(self):
        head = label(r"The division of linguistic labour", font_size=30, color=CONN).to_edge(UP, buff=0.3)

        def tree(x, col):
            trunk = Rectangle(width=0.18, height=0.9, color=REF, fill_opacity=0.8).move_to([x, -0.2, 0])
            crown = Circle(0.6, color=col, fill_opacity=0.5).move_to([x, 0.6, 0])
            return VGroup(trunk, crown)

        elm, beech = tree(-4.6, WORLD), tree(-2.4, WORLD)
        tags = VGroup(label(r"an elm", font_size=19, color=WORLD).next_to(elm, DOWN, buff=0.1),
                      label(r"a beech", font_size=19, color=WORLD).next_to(beech, DOWN, buff=0.1))
        me = person(-3.5, -2.0, r"Putnam", SPEAK)
        thought = label(r"`a common deciduous tree'", font_size=17, color=GREY_A).next_to(me, RIGHT, buff=0.2)
        side = stack([(r"Putnam's concepts of elm and beech are the same", WHITE),
                      (r"yet his `elm' refers to elms, \ and his `beech' to beeches", REF),
                      (r"because the community includes experts who can tell them apart", OK),
                      (r"reference is fixed socially, \ as well as by the environment", GOAL)], font_size=21,
                     aligned_edge=LEFT, width=6.0, buff=0.3).move_to([3.3, 0.0, 0])
        with self.voiceover(
            "Putnam's second point was social. <bookmark mark='a'/>He confessed that he could not tell an elm from a "
            "beech. His concept of each was the same: a common deciduous tree. <bookmark mark='b'/>Yet his word elm "
            "refers to elms and his word beech to beeches. <bookmark mark='c'/>That is possible because language is "
            "a cooperative enterprise: a community of speakers includes experts who can tell the trees apart, and "
            "ordinary speakers defer to them. Putnam called it the division of linguistic labour. "
            "<bookmark mark='d'/>So reference is fixed by the world and by other people, as well as by what is in "
            "a speaker's head."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(elm), FadeIn(beech), FadeIn(tags), FadeIn(me), FadeIn(thought))
            for mk, r in zip("abcd", side):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def arthritis(self):
        d = load("burge")
        hc = history_card(1979, r"Tyler Burge", r"`Individualism and the Mental'", width=5.6, color=HIST).to_corner(
            UL, buff=0.3)
        claim = label(r"`I have arthritis in my thigh.'", font_size=30, color=TRUTH).move_to([0, 1.3, 0])
        hd = [r"\text{community}", r"\text{`arthritis' applies to}", r"\text{the patient's belief}"]
        cells = [[label(r["community"], font_size=21, color=WORLD),
                  label(r", \ ".join(r["applies_to"]), font_size=21, color=REF), tv(r["belief_true"], 24)]
                 for r in d["rows"]]
        grid = ValueGrid(hd, cells, col_w=[3.0, 4.0, 3.6], cell_h=0.55, font_size=21).move_to([0, -0.1, 0])
        assert [r["belief_true"] for r in d["rows"]] == [False, True] and d["same_patient"]
        rows = stack([(r"the same patient: \ the same body, \ history and inner life", SPEAK),
                      (r"different beliefs, \ because the community's usage differs", OK),
                      (r"externalism reaches thought itself, \ not only the meanings of words", GOAL)], font_size=21,
                     aligned_edge=LEFT, width=11.0, buff=0.25).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Tyler Burge, in 1979, carried the argument from words to thoughts. <bookmark mark='a'/>A patient tells "
            "his doctor: I have arthritis in my thigh. Arthritis is inflammation of the joints, so his belief is "
            "false. <bookmark mark='b'/>Now imagine a community where the experts apply the word arthritis to "
            "ailments of the thigh as well. <bookmark mark='c'/>Put the same patient there: the same body, the same "
            "history described without reference to meanings, the same inner life. His words now express a true "
            "belief. <bookmark mark='d'/>So the contents of his beliefs depend on his community's usage. "
            "Externalism is not only about the meanings of words; it reaches the contents of thought."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(claim))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(cells)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def debate(self):
        head = label(r"What externalism costs", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"narrow content", r"Fodor \ (1987): \ there is also a content shared by Oscar and his twin, \ the one "
                                r"psychology needs to explain behaviour", SENSE),
            (r"self-knowledge", r"if content depends on the environment, \ how do I know what I think without "
                                r"checking the world?", BAD),
            (r"Burge's reply", r"thinking `I am thinking that water is wet' fixes its own content: \ self-knowledge "
                               r"is safe", OK),
            (r"where it leads", r"minds extended into the world, \ and the mind--machine questions of Parts 30 and "
                                r"31", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "Externalism has costs, and they are still argued over. <bookmark mark='a'/>Jerry Fodor held that there "
            "must also be a narrow content, which Oscar and his twin share, since it is what psychology needs to "
            "explain why they both drink when thirsty. <bookmark mark='b'/>And there is a worry about self-knowledge. "
            "If what I am thinking depends on my environment, how can I know what I am thinking without investigating "
            "the world? <bookmark mark='c'/>Burge replied that a thought like I am thinking that water is wet "
            "inherits its content from the thought it is about, so it cannot go wrong in that way. "
            "<bookmark mark='d'/>These debates lead to the mind, and to the questions about minds and machines in "
            "Parts 30 and 31."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
