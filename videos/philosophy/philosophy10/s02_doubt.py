from __future__ import annotations

from videos.philosophy.philosophy10.common import *  # noqa: F403


class Doubt(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"The method of doubt", r"What survives, \ if everything doubtful is thrown away?",
                            lit=(1641,), part=PART)
        with self.voiceover("Chapter one. The method of doubt."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.waves()
        self.cogito()
        self.rule()
        self.elisabeth()

    def waves(self):
        hc = history_card(1641, r"René Descartes", r"\textit{Meditations on First Philosophy}", width=5.2,
                          color=HIST).to_corner(UL, buff=0.35)
        beliefs = [r"the tower in the distance is round", r"I am sitting by the fire, \ in a winter gown",
                   r"I have hands and a body", r"there is an earth, \ a sky, \ other people",
                   r"2 + 3 = 5", r"a square has four sides"]
        groups = [(0,), (1, 2, 3), (4, 5)]
        blocks = VGroup(*[label(b, font_size=24, color=WHITE) for b in beliefs]).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.3)
        blocks.move_to([-2.4, -0.6, 0])
        waves = [(r"the senses sometimes deceive", SENSE), (r"I might be dreaming", REASON),
                 (r"an evil demon might deceive me even in arithmetic", DOUBT)]
        tags = VGroup()
        for (g, (t, c)) in zip(groups, waves):
            tg = label(t, font_size=22, color=c).next_to(VGroup(*[blocks[i] for i in g]), RIGHT, buff=0.6)
            tags.add(tg)
        for tg in tags:
            tg.set_x(3.6)
        with self.voiceover(
            "In 1641 René Descartes published his Meditations, which begin by tearing everything down. "
            "<bookmark mark='a'/>Here are some of his beliefs. <bookmark mark='b'/>First wave: the senses sometimes "
            "deceive. A distant square tower looks round. It is prudent never to trust completely what has once "
            "deceived us. <bookmark mark='c'/>Second wave: I might be dreaming. In dreams I have sat by the fire in "
            "my gown, when I was in fact undressed in bed. So even my hands and body, the earth and sky, may be a "
            "dream. <bookmark mark='d'/>Dreams, though, seem to keep arithmetic intact: asleep or awake, two and "
            "three make five. So the third wave: perhaps an evil demon, supremely powerful and cunning, deceives me "
            "even there. Everything goes."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in blocks], lag_ratio=0.2), run_time=2)
            for mk, g, tg in zip("bcd", groups, tags):
                vo.wait_until(mk)
                self.play(FadeIn(tg), *[blocks[i].animate.set_opacity(0.25) for i in g])
                self.play(*[Create(Line(blocks[i].get_left(), blocks[i].get_right(), color=BAD, stroke_width=2))
                            for i in g], run_time=0.8)
        self.clear_scene()

    def cogito(self):
        q = quote_card(r"I am, I exist, is necessarily true whenever it is put forward by me or conceived in my mind.",
                       r"René Descartes", r"Second Meditation \ (trans.\ Cottingham)", width=9.6,
                       font_size=30).move_to([0, 1.5, 0])
        rows = VGroup(
            label(r"even if the demon deceives me, \ I am the one deceived: \ so I exist", font_size=26),
            label(r"`I think, therefore I am' \ (\textit{Discourse on the Method}, 1637): \ the first certainty",
                  font_size=24, color=GOAL),
            label(r"but what am I? \ a thing that thinks: \ doubts, understands, affirms, denies, wills, imagines, "
                  r"senses", font_size=22, color=GREY_A),
            label(r"and the self is known better than the body: \ the wax, melted, \ is grasped by the intellect, "
                  r"not the senses", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.3).move_to([0, -1.4, 0])
        with self.voiceover(
            "One thing survives. <bookmark mark='a'/>I am, I exist, is necessarily true whenever it is put forward by "
            "me or conceived in my mind. <bookmark mark='b'/>Even if the demon deceives me about everything else, "
            "I am the one being deceived, so I exist. <bookmark mark='c'/>Descartes's earlier Discourse on the "
            "Method had put it as: I think, therefore I am. <bookmark mark='d'/>What am I, then? A thing that "
            "thinks: that doubts, understands, affirms, denies, wills, imagines and senses. <bookmark mark='e'/>"
            "And this thinking thing is known better than any body. A piece of wax, melted by the fire, changes "
            "every quality the senses report, yet we judge it the same wax. It is grasped by the intellect, not by "
            "the senses."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            for mk, r in zip("bcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def rule(self):
        head = label(r"From the cogito back to the world", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        steps = VGroup(
            label(r"1. \ why is the cogito certain? \ because I perceive it clearly and distinctly", font_size=24),
            label(r"2. \ so: \ whatever I perceive clearly and distinctly is true?", font_size=24, color=GOAL),
            label(r"3. \ only if no demon deceives me: \ only if a good God exists", font_size=24),
            label(r"4. \ I have the idea of an infinite being; \ only an infinite being could cause it; \ so God exists",
                  font_size=22, color=REASON)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-0.6, 0.6, 0])
        c = Circle(radius=0.9, color=BAD, stroke_width=3).move_to([4.6, -2.2, 0])
        top = Arc(radius=0.9, start_angle=PI * 0.85, angle=-PI * 0.7, color=BAD, stroke_width=3).move_arc_center_to(
            c.get_center())
        bot = Arc(radius=0.9, start_angle=-PI * 0.15, angle=-PI * 0.7, color=BAD, stroke_width=3).move_arc_center_to(
            c.get_center())
        top.add_tip(tip_length=0.18)
        bot.add_tip(tip_length=0.18)
        arr = VGroup(top, bot)
        lt = label(r"God exists", font_size=20, color=WHITE).next_to(c, UP, buff=0.1)
        lb = label(r"clear and distinct ideas are true", font_size=20, color=WHITE).next_to(c, DOWN, buff=0.1)
        circ = VGroup(arr, lt, lb)
        arn = VGroup(label(r"Arnauld (1641): \ the Cartesian circle", font_size=24, color=BAD),
                     label(r"the proof of God relies on clear and distinct ideas, \ and their reliability relies on God",
                           font_size=21, color=GREY_A),
                     label(r"one reply: \ the rule protects the \textit{memory} of past proofs, \ not present insight",
                           font_size=21, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(
            [-2.2, -2.3, 0])
        with self.voiceover(
            "How does Descartes get the world back? <bookmark mark='a'/>The cogito is certain because he perceives it "
            "clearly and distinctly. <bookmark mark='b'/>So perhaps a general rule holds: whatever I perceive "
            "clearly and distinctly is true. <bookmark mark='c'/>But that rule is safe only if there is no deceiving "
            "demon: only if a good God exists. <bookmark mark='d'/>So he proves that God exists. He has the idea of "
            "an infinite and perfect being, and only an infinite being could be the cause of such an idea. "
            "<bookmark mark='e'/>Antoine Arnauld objected at once, in 1641. The proof of God relies on clear and "
            "distinct ideas, and their reliability relies on God. This is the Cartesian circle. One reply, popular "
            "with scholars, is that the guarantee is needed only for remembered proofs, not for what is clearly "
            "seen in the present moment."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s_ in zip("abcd", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s_, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(arn), Create(arr[0]), Create(arr[1]), FadeIn(lt), FadeIn(lb))
        self.clear_scene()

    def elisabeth(self):
        hc = history_card(1643, r"Princess Elisabeth of Bohemia", r"letters to Descartes", width=5.2,
                          color=HIST).to_corner(UL, buff=0.35)
        left = VGroup(label(r"mind", font_size=30, color=REASON),
                      label(r"thinks; \ not extended", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.12)
        right = VGroup(label(r"body", font_size=30, color=SENSE),
                       label(r"extended; \ does not think", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.12)
        pair = VGroup(left, right).arrange(RIGHT, buff=3.0).move_to([0, 0.9, 0])
        arr = DoubleArrow(left.get_right(), right.get_left(), buff=0.3, color=GOAL)
        qm = label(r"?", font_size=40, color=GOAL).next_to(arr, UP, buff=0.1)
        rows = VGroup(
            label(r"the real distinction: \ I can clearly conceive the mind without the body, \ so they are distinct",
                  font_size=23),
            label(r"Elisabeth: \ bodies move bodies by contact and push; \ how can a thing with no extension push?",
                  font_size=23, color=GOAL),
            label(r"Descartes: \ the union of mind and body is a primitive notion, \ known by the senses, \ not the "
                  r"intellect", font_size=21, color=GREY_A),
            label(r"the mind--body problem, \ in its modern form: \ Parts 30 and 31", font_size=22,
                  color=KANT)).arrange(DOWN, buff=0.28).move_to([0, -1.5, 0])
        with self.voiceover(
            "The cogito also gave Descartes his picture of the self. <bookmark mark='a'/>I can clearly conceive my "
            "mind existing without my body, he argued, so the two are really distinct: mind is a thinking thing "
            "without extension, body an extended thing that does not think. <bookmark mark='b'/>In 1643 Princess "
            "Elisabeth of Bohemia, in a sharp exchange of letters, asked the question that has never gone away. "
            "Bodies move bodies by contact and push. How can a mind, which has no extension and touches nothing, "
            "push a body? <bookmark mark='c'/>Descartes replied that the union of mind and body is a primitive "
            "notion, understood through the senses rather than the intellect, an answer Elisabeth found hard to "
            "accept. <bookmark mark='d'/>This is the mind-body problem in its modern form, and Parts 30 and 31 take "
            "it up."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(left), FadeIn(right), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowFromCenter(arr), FadeIn(qm), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
