from __future__ import annotations

from videos.philosophy.philosophy21.common import *  # noqa: F403


class Locke(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"Memory and the brave officer", r"Are you whoever you remember being?",
                            lit=(1694, 1785), part=PART)
        with self.voiceover("Chapter nine. Memory and the brave officer."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.locke()
        self.reid()
        self.butler()
        self.williams()

    def locke(self):
        hc = history_card(1694, r"John Locke", r"\textit{Essay}, \ 2nd ed., \ II.xxvii", width=5.6,
                          color=HIST).to_corner(UL, buff=0.3)
        q = quote_card(r"as far as this consciousness can be extended backwards to any past action or thought, \ so "
                       r"far reaches the identity of that person", r"John Locke", r"II.xxvii.9", width=8.4,
                       font_size=22).move_to([1.4, 1.0, 0])
        rows = stack([(r"a person: \ `a thinking intelligent being, \ that has reason and reflection'", NOM),
                      (r"not the same substance, \ nor the same man \ (animal): \ the same consciousness", GOAL),
                      (r"the prince and the cobbler: \ swap their memories, \ and the persons go with them", UNIV),
                      (r"a forensic notion: \ reward and punishment follow the person", WHOLE)], font_size=20,
                     aligned_edge=LEFT, width=10.6).move_to([0.6, -1.6, 0])
        with self.voiceover(
            "In the second edition of his Essay, in 1694, John Locke added a chapter on identity. "
            "<bookmark mark='a'/>A person, he said, extends as far back as consciousness can reach: whatever past "
            "action you can remember from the inside is yours. <bookmark mark='b'/>A person is a thinking, intelligent "
            "being with reason and reflection. <bookmark mark='c'/>What makes a person the same is not the same "
            "substance, nor even the same human animal, but the same consciousness. <bookmark mark='d'/>If the soul of "
            "a prince entered the body of a cobbler, carrying the prince's memories, the person would be the prince. "
            "<bookmark mark='e'/>Person, for Locke, is a forensic term: reward and punishment follow the person, not "
            "the body."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(q))
            for mk, r in zip("bcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def reid(self):
        d = load("reid")
        hc = history_card(1785, r"Thomas Reid", r"\textit{Essays on the Intellectual Powers of Man}", width=6.6,
                          color=HIST).to_corner(UL, buff=0.3)
        ppl = d["people"]
        pos = {"boy": np.array([-4.6, -1.2, 0]), "officer": np.array([-1.2, -1.2, 0]),
               "general": np.array([2.2, -1.2, 0])}
        lab = {"boy": r"the boy \ (flogged)", "officer": r"the officer \ (takes a standard)",
               "general": r"the general"}
        nodes = VGroup(*[VGroup(Circle(radius=0.5, color=NOM, fill_opacity=0.25),
                                label(p, font_size=17, color=WHITE)).move_to(pos[p]) for p in ppl])
        for n_ in nodes:
            n_[1].move_to(n_[0])
        caps = VGroup(*[label(lab[p], font_size=15, color=GREY_A).next_to(pos[p], DOWN, buff=0.65) for p in ppl])
        mem = VGroup(*[Arrow(pos[a] + LEFT * 0.5, pos[b] + RIGHT * 0.5, buff=0.05, color=OK, stroke_width=3)
                       for a, b in d["memory"]])
        meml = label(r"remembers", font_size=15, color=OK).next_to(mem[0], UP, buff=0.05)
        meml2 = label(r"remembers", font_size=15, color=OK).next_to(mem[1], UP, buff=0.05)
        gap = CurvedArrow(pos["general"] + UP * 0.55, pos["boy"] + UP * 0.55, angle=PI / 3, color=BAD)
        gl = label(r"does not remember", font_size=15, color=BAD).next_to(gap, UP, buff=0.05)
        v = d["verdicts"]
        rows = stack([(r"Locke: \ boy = officer \ (" + (r"yes" if v["boy = officer"] else r"no") + r"); \ officer = "
                       r"general \ (" + (r"yes" if v["officer = general"] else r"no") + r")", OK),
                      (r"but boy = general: \ " + (r"yes" if v["boy = general"] else r"no") + r", \ by memory alone",
                       BAD),
                      (r"identity is transitive; \ remembering is not", GOAL),
                      (r"repair: \ use the ancestral, \ an unbroken \textit{chain} of memories: \ boy to general, \ " +
                       (r"connected" if d["closure_boy_general"] else r"broken"), UNIV)], font_size=19,
                     aligned_edge=LEFT, width=6.2).move_to([3.6, 1.2, 0])
        with self.voiceover(
            "Thomas Reid answered with a story. <bookmark mark='a'/>A boy is flogged for robbing an orchard. As a "
            "young officer, he takes a standard from the enemy, and remembers the flogging. As an old general, he "
            "remembers taking the standard, but has forgotten the flogging. <bookmark mark='b'/>By Locke's criterion "
            "the boy is the officer, and the officer is the general. <bookmark mark='c'/>But the general does not "
            "remember being the boy, so the general is not the boy. <bookmark mark='d'/>Identity is transitive, and "
            "remembering is not. <bookmark mark='e'/>The Reasoner computes the repair later Lockeans adopted: not "
            "direct memory, but an unbroken chain of memories, the ancestral of the relation, which connects the "
            "general to the boy."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(nodes), FadeIn(caps), GrowArrow(mem[0]), FadeIn(meml), GrowArrow(mem[1]), FadeIn(meml2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(Create(gap), FadeIn(gl), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]), Indicate(VGroup(mem, nodes), color=UNIV))
        self.clear_scene()

    def butler(self):
        head = label(r"Circularity, \ and quasi-memory", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Butler \ (1736)", r"`consciousness of personal identity presupposes, \ and therefore cannot "
                                 r"constitute, \ personal identity'", BAD),
            (r"the point", r"I can only \textit{remember} my own experiences: \ memory already assumes identity", GREY_A),
            (r"quasi-memory", r"Shoemaker \ (1970): \ a memory-like state caused in the right way by an experience, \ "
                              r"whoever had it", UNIV),
            (r"the result", r"psychological continuity can be defined first, \ and identity defined from it", OK),
            (r"onward", r"Parfit: \ continuity, \ connectedness, \ and what matters", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.8, x_text=-2.4, label_size=21)
        with self.voiceover(
            "Joseph Butler pressed a deeper objection. <bookmark mark='a'/>Consciousness of personal identity, he "
            "wrote, presupposes, and therefore cannot constitute, personal identity. <bookmark mark='b'/>I can only "
            "remember my own experiences; apparent memories of someone else's are not memories at all. So memory "
            "already assumes identity. <bookmark mark='c'/>Sydney Shoemaker replied with quasi-memory: a memory-like "
            "state caused in the right way by a past experience, whoever had that experience. "
            "<bookmark mark='d'/>Then psychological continuity can be defined first, and personal identity defined "
            "from it, without circularity. <bookmark mark='e'/>Derek Parfit built on exactly this."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def williams(self):
        hc = history_card(1970, r"Bernard Williams", r"`The Self and the Future'", width=5.6, color=HIST).to_corner(
            UL, buff=0.3)

        def body(x, name, col):
            return VGroup(Circle(radius=0.3, color=col, fill_opacity=0.25).move_to([x, 0.9, 0]),
                          RoundedRectangle(width=0.7, height=1.1, corner_radius=0.2, color=col,
                                           fill_opacity=0.25).move_to([x, -0.1, 0]),
                          label(name, font_size=16, color=col).move_to([x, -0.95, 0]))
        A = body(-5.0, r"A-body", NOM)
        B = body(-2.6, r"B-body", PARTC)
        sw = DoubleArrow([-4.6, 0.9, 0], [-3.0, 0.9, 0], buff=0.05, color=GOAL, stroke_width=2)
        sl = label(r"psychologies swapped", font_size=14, color=GOAL).next_to(sw, UP, buff=0.05)
        rows = stack([(r"telling 1: \ A and B swap psychologies; \ one body will be tortured, \ the other paid", WHITE),
                      (r"choose in advance which body gets the money: \ you choose the other body \ (you go with your "
                       r"psychology)", UNIV),
                      (r"telling 2: \ `tomorrow you will be tortured; \ first your memories will be erased, \ and "
                       r"someone else's installed'", BAD),
                      (r"now it seems \textit{you} will be tortured: \ you stay with the body", GOAL),
                      (r"the same case, \ two framings, \ opposite verdicts", ABS)], font_size=19, aligned_edge=LEFT,
                     width=6.6).move_to([3.4, -0.4, 0])
        with self.voiceover(
            "Bernard Williams showed that the same case can pull both ways. <bookmark mark='a'/>Told one way: A and B "
            "will have their psychologies swapped, and afterwards one body will be tortured and the other paid. Each "
            "chooses in advance. Most people choose that the other body be paid, as if they go with their psychology. "
            "<bookmark mark='b'/>Told another way: tomorrow you will be tortured; but first your memories will be "
            "erased, and someone else's installed. Now it seems you should fear the torture: you stay with your body. "
            "<bookmark mark='c'/>The same physical facts, two framings, and opposite verdicts. Williams took this as "
            "evidence for the bodily view; Parfit, as evidence that the question had no deep answer."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(A), FadeIn(B))
            vo.wait_until("a")
            self.play(GrowFromCenter(sw), FadeIn(sl), FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
