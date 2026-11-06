from __future__ import annotations

from videos.philosophy.philosophy11.common import *  # noqa: F403


class Gettier(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"Three pages", r"Is justified true belief knowledge?", lit=(1963,), part=PART)
        with self.voiceover("Chapter two. Three pages."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.paper()
        self.coins()
        self.ford()

    def paper(self):
        hc = history_card(1963, r"Edmund Gettier", r"`Is Justified True Belief Knowledge?', \ \textit{Analysis} 23, "
                          r"pp.\ 121--123", width=7.0, color=HIST).to_corner(UL, buff=0.35)
        ps = VGroup(
            label(r"two assumptions:", font_size=26, color=GOAL),
            label(r"(i) \ one can be justified in believing something false", font_size=25),
            label(r"(ii) \ if S is justified in believing $P$, \ and deduces $Q$ from $P$,", font_size=25),
            label(r"\quad then S is justified in believing $Q$", font_size=25)).arrange(DOWN, aligned_edge=LEFT,
                                                                                      buff=0.25).move_to([0, 0.1, 0])
        tail = label(r"so: \ deduce a truth from a justified falsehood", font_size=27, color=LUCK).to_edge(DOWN,
                                                                                                   buff=0.8)
        with self.voiceover(
            "Edmund Gettier was a young philosopher at Wayne State University who needed a publication. In 1963 the "
            "journal Analysis printed his paper: three pages, two counterexamples, and almost no other writing in "
            "his career. <bookmark mark='a'/>He makes two assumptions, both widely accepted. <bookmark mark='b'/>"
            "First, justification is fallible: one can be justified in believing something false. "
            "<bookmark mark='c'/>Second, justification passes along deduction: if you are justified in believing P, "
            "and you correctly deduce Q from P and believe Q as a result, you are justified in believing Q. "
            "<bookmark mark='d'/>Put them together. Start from a justified falsehood, and deduce from it something "
            "that happens to be true."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(ps[0]))
            vo.wait_until("b")
            self.play(FadeIn(ps[1]))
            vo.wait_until("c")
            self.play(FadeIn(ps[2]), FadeIn(ps[3]))
            vo.wait_until("d")
            self.play(FadeIn(tail))
        self.clear_scene()

    def coins(self):
        g = load("gettier")["coins"]
        head = label(r"Case I: \ ten coins", font_size=32, color=CONN).to_edge(UP, buff=0.3)
        smith = person(r"Smith", color=BEL, scale=0.8).move_to([-5.2, 1.6, 0])
        jones = person(r"Jones", color=WHITE, scale=0.8).move_to([-2.6, 1.6, 0])
        cj = coins(10).next_to(jones, RIGHT, buff=0.2)
        pres = label(r"the president: \ `Jones will get the job'", font_size=21, color=JUST).next_to(jones, UP,
                                                                                                   buff=0.25)
        ev = VGroup(*[MathTex(t, font_size=32, color=JUST) for t in g["evidence_tex"]]).arrange(DOWN, buff=0.15)
        bar = Line(LEFT * 1.6, RIGHT * 1.6, color=GREY_B)
        concl = MathTex(g["belief_tex"], font_size=32, color=BEL)
        proof = VGroup(ev, bar, concl).arrange(DOWN, buff=0.15).move_to([3.6, 1.5, 0])
        valid = label(r"the Reasoner: \ valid \ (a closed tableau)", font_size=20, color=OK).next_to(proof, DOWN,
                                                                                                     buff=0.2)
        cs = coins(10).next_to(smith, RIGHT, buff=0.2)
        job = label(r"gets the job", font_size=20, color=GOAL).next_to(smith, UP, buff=0.15)
        rows = check_rows([(r"the belief is true \ (Smith is the man, \ with ten coins)", g["true"]),
                           (r"Smith believes it", g["believed"]),
                           (r"Smith is justified \ (a valid deduction from justified premises)", g["justified"]),
                           (r"every premise is true \ (`Jones will get the job')", not g["false_lemma"])],
                          font_size=22, buff=0.2)
        rows.move_to([-0.6, -1.85, 0])
        verdict = label(r"does Smith know? \ no", font_size=26, color=BAD).next_to(rows, RIGHT, buff=0.6)
        with self.voiceover(
            "Case one. Smith and Jones have applied for the same job. <bookmark mark='a'/>The company president has "
            "assured Smith that Jones will get it, and Smith has counted the coins in Jones's pocket: ten. "
            "<bookmark mark='b'/>So Smith infers: the man who will get the job has ten coins in his pocket. The "
            "Reasoner checks the inference: from Jones gets the job, and Jones has ten coins, it follows that "
            "someone gets the job and has ten coins. Valid. <bookmark mark='c'/>But unknown to Smith, he himself will "
            "get the job, and, also unknown to him, he too has ten coins in his pocket. <bookmark mark='d'/>The "
            "Reasoner evaluates the belief in the actual world. It is true: Smith is the man. Smith believes it. "
            "Smith is justified, by valid deduction from justified premises. Every condition of the analysis holds. "
            "But a premise is false. <bookmark mark='e'/>Does Smith know that the man who will get the job has ten "
            "coins in his pocket? Almost everyone says no."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(smith), FadeIn(jones), FadeIn(cj), FadeIn(pres))
            vo.wait_until("b")
            self.play(FadeIn(ev), Create(bar), FadeIn(concl))
            self.play(FadeIn(valid))
            vo.wait_until("c")
            self.play(FadeIn(cs, shift=DOWN * 0.1), FadeIn(job))
            vo.wait_until("d")
            for i in range(4):
                self.play(FadeIn(rows.texts[i]), FadeIn(rows.marks[i]), run_time=0.7)
            vo.wait_until("e")
            self.play(FadeIn(verdict))
        self.clear_scene()

    def ford(self):
        g = load("gettier")["ford"]
        head = label(r"Case II: \ a Ford, \ or Barcelona", font_size=32, color=CONN).to_edge(UP, buff=0.3)
        ev = MathTex(g["evidence_tex"][0], font_size=34, color=JUST)
        bar = Line(LEFT * 2.2, RIGHT * 2.2, color=GREY_B)
        concl = MathTex(g["belief_tex"], font_size=34, color=BEL)
        proof = VGroup(ev, bar, concl).arrange(DOWN, buff=0.15).move_to([-3.2, 1.3, 0])
        rule = label(r"disjunction introduction: \ valid", font_size=20, color=OK).next_to(proof, DOWN, buff=0.2)
        world = VGroup(label(r"in fact:", font_size=24, color=GREY_A),
                       label(r"Jones does not own a Ford \ (he rents one)", font_size=23, color=BAD),
                       label(r"and Brown, \ by chance, \ is in Barcelona", font_size=23, color=OK)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.3, 1.3, 0])
        rows = check_rows([(r"true", g["true"]), (r"believed", g["believed"]), (r"justified", g["justified"]),
                           (r"no false premise", not g["false_lemma"])], font_size=23, buff=0.16)
        rows.move_to([-3.5, -1.7, 0])
        near = VGroup(label(r"a nearby world: \ Brown is in Boston", font_size=23, color=GREY_A),
                      label(r"same evidence, \ same inference, \ same belief:", font_size=23, color=WHITE),
                      label(r"false", font_size=26, color=BAD)).arrange(DOWN, buff=0.15).move_to([3.2, -1.6, 0])
        assert not g["nearby_true"]
        foot = label(r"justified true belief is not sufficient for knowledge", font_size=27, color=GOAL).to_edge(
            DOWN, buff=0.3)
        with self.voiceover(
            "Case two. Smith has strong evidence that Jones owns a Ford: Jones has always owned one, and just gave "
            "Smith a ride in one. <bookmark mark='a'/>Smith picks a city at random and infers: either Jones owns a "
            "Ford, or Brown is in Barcelona. That follows by disjunction introduction, so he is justified in "
            "believing it. <bookmark mark='b'/>In fact Jones does not own a Ford: he is driving a rented car. But by "
            "sheer chance, Brown is in Barcelona. <bookmark mark='c'/>The belief is true, believed and justified. "
            "<bookmark mark='d'/>Now the Reasoner moves to a nearby world, where Brown went to Boston instead. Smith's "
            "evidence is exactly the same, so is his inference, so is his belief; and there it is false. What made "
            "the belief true had nothing to do with why Smith believed it. <bookmark mark='e'/>Justified true belief "
            "is not sufficient for knowledge."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ev), Create(bar), FadeIn(concl), FadeIn(rule))
            vo.wait_until("b")
            self.play(FadeIn(world))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(t, m)) for t, m in zip(rows.texts, rows.marks)], lag_ratio=0.4))
            vo.wait_until("d")
            self.play(FadeIn(near))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
