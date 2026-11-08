from __future__ import annotations

from videos.philosophy.philosophy8.common import *  # noqa: F403


class Ancient(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"An old puzzle", r"Who first noticed, and what did they make of it?", lit=(-340,),
                            part=PART)
        with self.voiceover("Chapter one. An old puzzle."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.greece()
        self.mohists()
        self.india()
        self.medieval()

    def greece(self):
        cards = VGroup(
            history_card(r"c.\ 350 BCE", r"Eubulides of Miletus", r"`a man says that he is lying: \ is what he says "
                         r"true or false?'", width=5.4, color=HIST),
            history_card(r"c.\ 280 BCE", r"Chrysippus", r"wrote several books on the liar; \ none survive",
                         width=5.0, color=HIST)).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.5)
        ep = VGroup(label(r"`One of themselves, a prophet of their own, said, \ the Cretans are always liars'",
                          font_size=26),
                    label(r"Paul, \ Letter to Titus 1:12, \ quoting Epimenides the Cretan", font_size=22,
                          color=GREY_A)).arrange(DOWN, buff=0.2).move_to([0, -0.3, 0])
        note = label(r"not yet a paradox: \ it is simply false if some Cretan once told the truth", font_size=24,
                     color=GOAL).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "The liar is Greek. <bookmark mark='a'/>Eubulides of Miletus, a rival of Aristotle, asked about a man "
            "who says that he is lying: is what he says true, or false? <bookmark mark='b'/>The Stoic Chrysippus "
            "wrote several books about it, all lost. <bookmark mark='c'/>A cousin of it reached a wider audience "
            "through the New Testament, where Paul quotes a Cretan prophet saying that Cretans are always liars. "
            "<bookmark mark='d'/>That one is not yet a paradox. If some Cretan, once, told the truth, the prophet's "
            "saying is simply false. The real liar leaves no such exit."
        ) as vo:
            self.play(FadeIn(cards[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(cards[1]))
            vo.wait_until("c")
            self.play(FadeIn(ep))
            vo.wait_until("d")
            self.play(FadeIn(note))
        self.clear_scene()

    def mohists(self):
        hc = history_card(r"c.\ 300 BCE", r"the Later Mohist canon", r"\textit{Mojing}, \ Canon B 71", width=5.8,
                          color=HIST).to_corner(UL, buff=0.35)
        zh = label(r"`to say that all saying is contrary \ is contrary'", font_size=32, color=SELF).move_to([0, 0.9, 0])
        gloss = VGroup(label(r"if the claim `all saying is contrary' is acceptable, \ then it is itself contrary: \ "
                             r"so it is not", font_size=24),
                       label(r"the Mohists used the point against the Daoist \textit{Zhuangzi}: \ a theory that "
                             r"rejects all claims rejects itself", font_size=24, color=GREY_A)).arrange(
            DOWN, buff=0.25).next_to(zh, DOWN, buff=0.6)
        with self.voiceover(
            "Chinese logicians found a relative of the liar on their own. <bookmark mark='a'/>The Later Mohist "
            "canon, from around 300 BCE, says: to say that all saying is contrary is contrary. "
            "<bookmark mark='b'/>If the claim that every claim is unacceptable were acceptable, it would be a claim, "
            "and so unacceptable. The Mohists used it against sceptics like the Daoist Zhuangzi: a doctrine that "
            "rejects every doctrine undermines itself. It is self-refutation rather than full paradox, but it is "
            "the same move, a sentence turned back on itself."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(zh))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(g) for g in gloss], lag_ratio=0.5))
        self.clear_scene()


    def india(self):
        hc = history_card(r"c.\ 450", r"Bhartṛhari", r"\textit{Vākyapadīya}", width=4.8, color=HIST).to_corner(UL,
                                                                                                    buff=0.35)
        w = label(r"`unnameable' \ (\textit{avācya})", font_size=34, color=SELF).move_to([0, 1.0, 0])
        rows = VGroup(label(r"to call something unnameable \ is to name it", font_size=26),
                      label(r"Bhartṛhari: \ a word can be used without being \textit{about} itself; \ the paradox "
                            r"turns on what words signify", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.3).next_to(
            w, DOWN, buff=0.5)
        with self.voiceover(
            "In India, the grammarian-philosopher Bhartṛhari, around the fifth century, wrestled with a close "
            "relative. <bookmark mark='a'/>The word 'unnameable'. <bookmark mark='b'/>To call something unnameable "
            "is to name it. Bhartṛhari's answer turned on the difference between what a word conveys and what it "
            "is about, a distinction modern logicians would call use and mention."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(w))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.5))
        self.clear_scene()

    def medieval(self):
        head = label(r"The \textit{insolubilia}", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        rows = VGroup(
            VGroup(label(r"Thomas Bradwardine \ (c.\ 1324)", font_size=26, color=GOAL),
                   label(r"every sentence also says that it is true; \ so the liar says it is true \textit{and} not "
                         r"true: \ simply false", font_size=24, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                      buff=0.12),
            VGroup(label(r"John Buridan \ (\textit{Sophismata}, \ c.\ 1350)", font_size=26, color=GOAL),
                   label(r"every sentence \textit{virtually implies} that it is true: \ so the liar implies both, \ "
                         r"and is false", font_size=24, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.12),
            VGroup(label(r"`restrictionists'", font_size=26, color=GOAL),
                   label(r"a sentence cannot refer to itself: \ the liar says nothing", font_size=24,
                         color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, -0.1, 0])
        moral = label(r"three answers we will meet again in modern dress", font_size=26, color=OK).to_edge(DOWN,
                                                                                                           buff=0.6)
        with self.voiceover(
            "In the fourteenth century the liar became one of the insolubilia, the unsolvables, and the schools "
            "competed to solve it. <bookmark mark='a'/>Thomas Bradwardine argued that every sentence also signifies "
            "that it is true. So the liar says both that it is true and that it is not, and is simply false. "
            "<bookmark mark='b'/>John Buridan gave a related answer: every sentence virtually implies that it is "
            "true, so the liar implies both its truth and its falsehood, and is false. <bookmark mark='c'/>Others, the "
            "restrictionists, denied that a sentence can refer to itself at all. <bookmark mark='d'/>Each of these "
            "answers comes back in modern dress."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(moral))
        self.clear_scene()
