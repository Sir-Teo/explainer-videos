from __future__ import annotations

from videos.philosophy.philosophy1.common import *  # noqa: F403

POS = {
    "D": (r"Piety is not god-lovedness", r"Socrates (10e--11b): being loved by the gods is something that happens "
                                         r"to the pious, not what piety is"),
    "E1": (r"Divine command", r"the pious is pious because the gods love it: Ockham's voluntarism; Robert Adams's "
                              r"modified theory (1973)"),
    "E2": (r"No `because' on that side", r"deny that being god-loved is constituted by the gods' loving: almost "
                                         r"no one"),
    "Sub": (r"Substitution fails", r"`because' is hyperintensional: co-referring names cannot be swapped inside it "
                                   r"(Parts 20, 22, 27)"),
    "Asym": (r"Circular explanation", r"let explanation run both ways: very few take this exit"),
}


class Euthyphro(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Socrates' question", r"Is the good good because the gods command it?",
                            lit=(-400,), part=PART)
        with self.voiceover("Chapter four. Socrates' question."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.scene_()
        self.dilemma()
        self.price()

    def scene_(self):
        hc = history_card(r"399 BCE", r"Socrates on trial", r"charged with impiety; on his way to court he meets "
                          r"Euthyphro, prosecuting his own father", width=5.6, color=HIST).to_corner(UL, buff=0.4)
        q = quote_card(r"Is the pious loved by the gods because it is pious, or is it pious because it is loved?",
                       r"Socrates, \textit{Euthyphro} 10a", r"trans.\ Grube", width=9.6, font_size=32)
        q.move_to([0.4, -1.0, 0])
        dfn = definition_card(r"Euthyphro's definition", r"the pious is what all the gods love", width=5.4,
                              font_size=24, color=P.CLAIM).to_corner(UR, buff=0.4)
        with self.voiceover(
            "Athens, 399 before our era. Socrates is on his way to the court where he will be tried, and condemned, "
            "for impiety. <bookmark mark='a'/>At the door he meets Euthyphro, who is prosecuting his own father for "
            "murder, and is very sure he knows what piety is. <bookmark mark='b'/>Socrates asks for a definition, "
            "and after some false starts Euthyphro offers one: the pious is what all the gods love. "
            "<bookmark mark='c'/>Then comes one of the most famous questions in philosophy. Is the pious loved by the "
            "gods because it is pious? Or is it pious because it is loved?"
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("b")
            self.play(FadeIn(dfn, shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(q, shift=UP * 0.2))
        self.clear_scene()

    def dilemma(self):
        left = VGroup(label(r"pious, so loved", font_size=32, color=P.CLAIM),
                      label(r"the gods respond to a standard", font_size=24, color=GREY_A),
                      label(r"that is independent of them", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.15)
        right = VGroup(label(r"loved, so pious", font_size=32, color=P.AGENT),
                       label(r"piety is whatever they happen", font_size=24, color=GREY_A),
                       label(r"to love: arbitrary", font_size=24, color=GREY_A)).arrange(DOWN, buff=0.15)
        both = VGroup(left, right).arrange(RIGHT, buff=2.2).move_to([0, 1.3, 0])
        arr = DoubleArrow(left.get_right(), right.get_left(), buff=0.3, color=GREY_C)
        modern = label(r"today: \ is something right because God commands it, or commanded because it is right?",
                       font_size=26, color=GOAL).move_to([0, -0.6, 0])
        socr = label(r"Socrates' argument: \ Euthyphro already accepts the first; then the definition fails",
                     font_size=26).move_to([0, -1.6, 0])
        with self.voiceover(
            "The two horns pull opposite ways. <bookmark mark='a'/>If the gods love the pious because it is pious, "
            "then piety is a standard the gods respond to, and it is independent of them. <bookmark mark='b'/>If the "
            "pious is pious because the gods love it, then piety is whatever they happen to love, and seems "
            "arbitrary. <bookmark mark='c'/>The same dilemma is still argued about God and morality: is an act right "
            "because God commands it, or does God command it because it is right? <bookmark mark='d'/>Socrates' own "
            "argument is subtler. Euthyphro already agrees that the gods love the pious because it is pious. Then, "
            "Socrates shows, 'pious' and 'god-loved' cannot be the same thing."
        ) as vo:
            self.play(FadeIn(left, shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(Indicate(left, color=P.CLAIM))
            vo.wait_until("b")
            self.play(FadeIn(right, shift=LEFT * 0.2), GrowArrow(arr))
            vo.wait_until("c")
            self.play(FadeIn(modern))
            vo.wait_until("d")
            self.play(FadeIn(socr))
        self.clear_scene()

    def price(self):
        d = load("euthyphro")
        pl = PriceList([(c["key"], c["text"]) for c in d["claims"]], mus=d["mus"], radius=2.6, width=4.0,
                       font_size=23, center=[0, -0.35, 0])
        title = label(r"The Price List: \ the \textit{Euthyphro}", font_size=34, color=P.PRICE).to_edge(UP, buff=0.25)
        with self.voiceover(
            "Make the argument exact, and it becomes our first Price List. Five claims. <bookmark mark='a'/>The pious "
            "and the god-loved are one thing, under two names. The gods love the pious because it is pious. The "
            "god-loved is god-loved because the gods love it. If two names name one thing, you may swap them inside "
            "a 'because'. And explanation does not run in a circle: nothing is so because of something that is so "
            "because of it. <bookmark mark='b'/>Swap the names in the second claim: the gods love it because it is "
            "god-loved. With the third, that is a circle. The five cannot all be true, and the Reasoner confirms "
            "that every one of them is needed for the contradiction."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, scale=0.9) for c in pl.cards], lag_ratio=0.35), run_time=3)
            vo.wait_until("b")
            self.play(Create(pl.conflict), run_time=1.5)
        def show(k):
            name, holders = POS[k]
            return pl.position((k,), name, holders, width=4.2)[0]

        with self.voiceover(
            "Give up the identity, as Socrates does: being loved by the gods is something that happens to the pious, "
            "not what piety is."
        ):
            self.play(*show("D"), run_time=1.2)
        self.play(*pl.reset(), run_time=0.8)
        with self.voiceover(
            "Give up the first 'because': things are pious because the gods love them. That is divine command "
            "theory, from William of Ockham to Robert Adams."
        ):
            self.play(*show("E1"), run_time=1.2)
        self.play(*pl.reset(), run_time=0.8)
        with self.voiceover(
            "Or give up substitution, and this exit is the most interesting. 'Because' may be a context where you "
            "cannot swap names for the same thing. We will meet such contexts again: in a Chinese logic text in "
            "Chapter ten, and in Parts 20, 22 and 27."
        ):
            self.play(*show("Sub"), run_time=1.2)
        self.play(*pl.reset(), run_time=0.8)
        with self.voiceover(
            "The remaining two exits, denying that god-lovedness comes from the gods' loving, or allowing circular "
            "explanation, find almost no takers. Five exits, all found by calculation; which one to take is the "
            "philosophy."
        ):
            self.play(Indicate(pl.cards, color=P.PRICE, scale_factor=1.02))
        self.clear_scene()
