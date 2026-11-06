from __future__ import annotations

from videos.philosophy.philosophy8.common import *  # noqa: F403


class Moore(VoiceoverScene):
    def construct(self):
        card = chapter_card(16, r"Moore's paradox", r"Why can't I say what may well be true?", part=PART)
        with self.voiceover("Chapter sixteen. Moore's paradox."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.puzzle()
        self.logic()
        self.updates()

    def puzzle(self):
        hc = history_card(1942, r"G. E. Moore", r"a remark that fascinated Wittgenstein",
                          width=6.6, color=HIST).to_corner(UL, buff=0.35)
        s = label(r"`It is raining, \ but I don't believe that it is raining.'", font_size=34, color=SELF).move_to(
            [0, 1.0, 0])
        rows = VGroup(label(r"it may well be true: \ it is raining, \ and I have not noticed", font_size=26,
                            color=OK),
                      label(r"but I cannot sincerely \textit{say} it, \ or believe it", font_size=26, color=BAD),
                      label(r"not a contradiction: \ an absurdity of the first person", font_size=26,
                            color=GOAL)).arrange(DOWN, buff=0.3).next_to(s, DOWN, buff=0.6)
        with self.voiceover(
            "One more puzzle, this time about belief. <bookmark mark='a'/>G. E. Moore noticed that there is "
            "something absurd in saying: it is raining, but I don't believe that it is raining. Wittgenstein "
            "was fascinated by it. <bookmark mark='b'/>The sentence may well be true: it is "
            "raining, and I have not noticed. <bookmark mark='c'/>But I cannot sincerely say it, or believe it. "
            "<bookmark mark='d'/>It is not a contradiction. Someone else can say it of me without absurdity. The "
            "trouble is in the first person."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(s))
            for mk, r in zip("bcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=DOWN * 0.1))
        self.clear_scene()

    def logic(self):
        d = load("moore")
        head = label(r"The Reasoner, \ in the belief logic of Part 4", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        rows = VGroup(
            VGroup(MathTex(r"p \wedge \lnot B p", font_size=44, color=OK),
                   label(r"`it is raining and I don't believe it': \ \textbf{satisfiable}", font_size=24,
                         color=OK)).arrange(DOWN, buff=0.15),
            VGroup(MathTex(r"B\,(p \wedge \lnot B p)", font_size=44, color=BAD),
                   label(r"believing it: \ \textbf{unsatisfiable} \ on every serial, transitive frame (KD4) up to three "
                         r"worlds", font_size=24, color=BAD)).arrange(DOWN, buff=0.15)).arrange(DOWN, buff=0.7).move_to(
            [0, 0.6, 0])
        why = VGroup(label(r"belief distributes: \ $Bp \wedge B\lnot Bp$", font_size=24),
                     label(r"positive introspection (4): \ $Bp \to BBp$", font_size=24),
                     label(r"so $B(Bp \wedge \lnot Bp)$: \ inconsistent beliefs, \ which D rules out", font_size=24,
                           color=GOAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.4).shift(LEFT * 1.6)
        nxt = label(r"Part 12: \ the logic of knowledge and belief", font_size=22, color=GREY_B).to_corner(DR, buff=0.3)
        assert d["said_satisfiable"] and not d["believed_satisfiable"]
        with self.voiceover(
            "The modal logic of Part 4 explains why, with B for 'I believe'. <bookmark mark='a'/>The Reasoner finds a "
            "model where p holds and I do not believe p: the sentence is perfectly consistent. "
            "<bookmark mark='b'/>Now ask whether I can believe it. On every frame that is serial and transitive, "
            "the logic KD4, with up to three worlds, the Reasoner finds no model. <bookmark mark='c'/>The reason: "
            "believing the conjunction means believing p, and believing that I do not believe p. By introspection, "
            "believing p means believing that I believe it. So I would believe a contradiction, which the D axiom "
            "forbids. Jaakko Hintikka gave this analysis in 1962. <bookmark mark='d'/>Part 12 takes up the logic of "
            "knowledge and belief properly."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(w_) for w_ in why], lag_ratio=0.4), run_time=3)
            vo.wait_until("d")
            self.play(FadeIn(nxt))
        self.clear_scene()

    def updates(self):
        head = label(r"Sentences that cannot survive being believed", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"`$p$, \ but you don't know it' \ can be true when I say it to you", font_size=26),
            label(r"once you believe me, \ you know $p$: \ and it is false", font_size=26, color=BAD),
            label(r"an \textit{unsuccessful update}: \ true when said, \ false once taken in", font_size=26,
                  color=GOAL),
            label(r"the surprise exam announcement is one; \ so is Moore's sentence, \ in the first person",
                  font_size=24, color=GREY_A),
            label(r"Wittgenstein: \ if there were a verb meaning `to believe falsely', \ it would have no "
                  r"first-person present", font_size=22, color=GREY_B)).arrange(DOWN, aligned_edge=LEFT,
                                                                                 buff=0.35).move_to([0, -0.3, 0])
        with self.voiceover(
            "Moore's sentence belongs to a family. <bookmark mark='a'/>I can say to you, truly: it is raining, but "
            "you don't know it. <bookmark mark='b'/>But once you believe me, you do know it, and what I said has "
            "become false. <bookmark mark='c'/>Logicians call this an unsuccessful update: a sentence that is true "
            "when said and false once taken in. <bookmark mark='d'/>The surprise exam announcement is one, as "
            "Gerbrandy's analysis showed, and Moore's sentence is the first-person case. "
            "<bookmark mark='e'/>Wittgenstein put the point memorably: if there were a verb meaning 'to believe "
            "falsely', it would have no meaningful first person present tense."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.clear_scene()
