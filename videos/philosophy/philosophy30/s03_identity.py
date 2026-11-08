from __future__ import annotations

from videos.philosophy.philosophy30.common import *  # noqa: F403


class Identity(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"Behaviour, \ and the brain", r"Is the mind what we do, \ or what our brains are?",
                            lit=(1949, 1959), part=PART)
        with self.voiceover("Chapter two. Behaviour, and the brain."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.ryle()
        self.behaviourism()
        self.identity()
        self.kripke()

    def ryle(self):
        hc = history_card(1949, r"Gilbert Ryle", r"\textit{The Concept of Mind}", width=5.0, color=HIST).to_corner(
            UL, buff=0.3)
        bld = VGroup(*[VGroup(Rectangle(width=1.3, height=0.9, color=PHYS, fill_opacity=0.12),
                              label(t, font_size=15, color=PHYS)) for t in
                       (r"colleges", r"libraries", r"laboratories", r"offices")]).arrange(RIGHT, buff=0.35).move_to(
            [0, 0.6, 0])
        for b in bld:
            b[1].move_to(b[0])
        q = label(r"`but where is the University?'", font_size=24, color=BAD).next_to(bld, DOWN, buff=0.5)
        rows = stack([(r"a category mistake: \ the University is the way all of these are organized, \ not one more "
                       r"building", GOAL),
                      (r"`the dogma of the ghost in the machine': \ the mind treated as a hidden extra thing", MIND)],
                     font_size=21, aligned_edge=LEFT, width=12.0, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "In 1949 Gilbert Ryle mocked Descartes's picture as the dogma of the ghost in the machine. "
            "<bookmark mark='a'/>His parable: a visitor to Oxford is shown the colleges, the libraries, the "
            "laboratories and the offices, <bookmark mark='b'/>and then asks: but where is the University? "
            "<bookmark mark='c'/>He has made a category mistake. The University is not one more building alongside "
            "the others; it is the way they are all organized. <bookmark mark='d'/>The mind, Ryle argued, is like "
            "that: not a hidden extra thing inside the body, but the way a person's doings and dispositions hang "
            "together."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bld], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(q))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def behaviourism(self):
        head = label(r"Behaviourism", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        eq = MathTex(r"\text{Jones is in pain} \;\;\equiv\;\; \text{Jones is disposed to wince, \ cry out, \ reach for "
                     r"aspirin} \dots", font_size=28, color=BEHAV).move_to([0, 2.0, 0])
        rows = [
            (r"logical behaviourism", r"mental words mean dispositions to behave, \ as `fragile' means disposed to "
                                      r"break \ (Hempel, \ Carnap, \ Ryle)", BEHAV),
            (r"circularity", r"whether pain makes you reach for aspirin depends on what you believe and want: \ more "
                             r"mental terms", BAD),
            (r"super-spartans", r"Putnam \ (1963): \ people who feel pain but are trained never to show it", BAD),
            (r"perfect actors", r"and people who show it, \ but feel nothing", BAD),
        ]
        g = rows_table(rows, top=1.0, gap=0.5)
        with self.voiceover(
            "Behaviourists made the thought precise. <bookmark mark='a'/>To say that Jones is in pain is to say that "
            "Jones is disposed to wince, cry out, reach for aspirin, and so on, as to call glass fragile is to say "
            "it would break if struck. <bookmark mark='b'/>It failed for three reasons. First, circularity: whether "
            "pain makes you reach for aspirin depends on whether you believe aspirin helps and want the pain to stop, "
            "so the analysis needs more mental terms. <bookmark mark='c'/>Second, Hilary Putnam's super-spartans, "
            "people who feel pain as we do but are trained never to show it. <bookmark mark='d'/>Third, perfect "
            "actors, who show pain and feel nothing. Pain and its behaviour can come apart in both directions."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(g[0]))
            for mk, r in zip("bcd", g[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def identity(self):
        hc = history_card(1956, r"U. T. Place \ (and J. J. C. Smart, \ 1959)", r"`Is Consciousness a Brain Process?'",
                          width=7.0, color=HIST).to_corner(UL, buff=0.3)
        pairs = VGroup()
        for i, (a, b) in enumerate([(r"lightning", r"electrical discharge"), (r"water", r"H$_2$O"),
                                    (r"heat", r"mean molecular kinetic energy"), (r"pain", r"C-fibre firing")]):
            y = 1.2 - 0.75 * i
            col = FEEL if a == "pain" else GREY_A
            pairs.add(VGroup(label(a, font_size=22, color=col).move_to([-2.6, y, 0]),
                             MathTex("=", font_size=30, color=col).move_to([0, y, 0]),
                             label(b, font_size=22, color=PHYS if a == "pain" else GREY_A).move_to([2.8, y, 0])))
        rows = stack([(r"an identity discovered empirically, \ not by analysing meanings", GOAL),
                      (r"`C-fibre firing' is a philosophers' placeholder for whatever neuroscience finds", HIST)],
                     font_size=21, aligned_edge=LEFT, width=12.0, buff=0.22).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The next proposal was bolder. In 1956 U. T. Place, and in 1959 J. J. C. Smart, argued that sensations "
            "are simply brain processes. <bookmark mark='a'/>Science has discovered that lightning is electrical "
            "discharge, that water is H two O, that heat is mean molecular kinetic energy. "
            "<bookmark mark='b'/>Why not that pain is C-fibre firing? <bookmark mark='c'/>The identity would be "
            "discovered by science, not by analysing what the word pain means, so the behaviourists' problems do not "
            "arise. <bookmark mark='d'/>C-fibre firing became the philosophers' standard example, a placeholder for "
            "whatever neuroscience eventually finds."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pairs[:3]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(pairs[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def kripke(self):
        head = label(r"Two objections", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Kripke \ (1970)", r"identities are necessary \ (Part 22); \ yet pain without C-fibres seems possible",
             BAD),
            (r"the disanalogy", r"heat could feel different and still be heat; \ but anything that feels like pain "
                                r"\textit{is} pain: \ the appearance cannot be explained away", FEEL),
            (r"multiple realizability", r"an octopus, \ a Martian, \ a robot: \ pain without C-fibres; \ so pain is not "
                                        r"C-fibre firing", FUNC),
            (r"the next step", r"if pain is not a kind of stuff, \ perhaps it is a kind of role", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55)
        with self.voiceover(
            "Two objections changed the field. <bookmark mark='a'/>Saul Kripke argued in 1970 that identities "
            "between rigidly designated things are necessary, as Part 22 showed, so if pain is C-fibre firing it is "
            "so in every possible world. Yet it seems possible to have pain without C-fibres. "
            "<bookmark mark='b'/>With heat, the appearance can be explained away: something could feel like heat "
            "without being heat, or heat could feel different. But anything that feels like pain is pain. "
            "<bookmark mark='c'/>The second objection was Putnam's. An octopus, with a very different nervous system, "
            "can surely be in pain, and so could a Martian, or a robot. Pain is multiply realizable, so it cannot be "
            "identical with any one kind of physical state. <bookmark mark='d'/>If pain is not a kind of stuff, "
            "perhaps it is a kind of role."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
