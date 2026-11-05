from __future__ import annotations

from videos.philosophy.philosophy2.common import *  # noqa: F403

POSITIONS = {
    "G": (r"Atheism", r"Mackie's conclusion; in the 2020 PhilPapers survey about two in three philosophers accepted "
                      r"or leaned toward atheism", 0.67),
    "omnipotent": (r"A limited God", r"process theology (Whitehead, Hartshorne): God persuades, does not coerce; "
                                     r"Kushner, \textit{When Bad Things Happen to Good People} (1981)", None),
    "omniscient": (r"Limited foreknowledge", r"some open theists: the future free choices of creatures are not yet "
                                             r"there to be known", None),
    "good": (r"A God not wholly good", r"rare among philosophers; argued by a few `dystheists'", None),
    "bridge": (r"The free-will defense", r"Plantinga (1974): a world with free creatures who sometimes do wrong "
                                         r"may be better than any world without evil; Hick's soul-making (1966)",
               None),
    "evil": (r"Evil is not real", r"evil as illusion (Mary Baker Eddy); compare Augustine, for whom evil is a "
                                  r"privation of good", None),
}


class Evil(VoiceoverScene):
    def construct(self):
        card = chapter_card(15, r"The first Price List: the problem of evil", r"Can God and evil both exist?",
                            lit=(1779,), part=PART)
        with self.voiceover("Chapter fifteen. The first Price List: the problem of evil."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.d = load("evil")
        self.history()
        self.list_()
        self.limits()

    def history(self):
        q = quote_card(r"Epicurus's old questions are yet unanswered. Is he willing to prevent evil, but not able? "
                       r"then is he impotent. Is he able, but not willing? then is he malevolent. Is he both able "
                       r"and willing? whence then is evil?", r"Philo, in Hume's \textit{Dialogues Concerning Natural "
                       r"Religion} (1779), Part X", width=11.0, font_size=28).move_to([0, 1.2, 0])
        hc = history_card(1955, r"J.\ L.\ Mackie", r"`Evil and Omnipotence': the theist's beliefs are not merely "
                          r"unsupported but `positively irrational'", width=6.6, color=HIST).move_to([0, -2.2, 0])
        with self.voiceover(
            "The argument is very old. Lactantius, writing around the year 300, attributed it to Epicurus. "
            "<bookmark mark='a'/>David Hume gave it to Philo in his Dialogues Concerning Natural Religion: Is he "
            "willing to prevent evil, but not able? then is he impotent. Is he able, but not willing? then is he "
            "malevolent. Is he both able and willing? whence then is evil? <bookmark mark='b'/>In 1955 J. L. Mackie "
            "sharpened it into a charge of inconsistency. The theist's beliefs, he said, are not merely unsupported "
            "but positively irrational: they contradict one another."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(hc, shift=UP * 0.2))
        self.clear_scene()

    def list_(self):
        d = self.d
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        pl = PriceList(claims, mus=d["mus"], radius=2.75, width=3.8, font_size=24, center=[0, -0.25, 0])
        title = label(r"The Price List", font_size=36, color=P.PRICE).to_edge(UP, buff=0.25)
        verdict = label(r"inconsistent; \ the only minimal inconsistent set: all six", font_size=24, color=BAD)
        verdict.to_edge(DOWN, buff=0.25)
        assert len(d["mcs"]) == 6 and all(len(m) == 1 for m in d["mcs"])
        with self.voiceover(
            "State it as six claims. <bookmark mark='a'/>God exists. God is omnipotent. God is omniscient. God is "
            "wholly good. A good, all-knowing, all-powerful being would prevent all evil. And there is evil. "
            "<bookmark mark='b'/>The Reasoner confirms Mackie: the six are inconsistent. And the only minimal "
            "inconsistent set is all six of them. So the positions are exactly six: give up any one claim, and "
            "consistency returns."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, scale=0.9) for c in pl.cards], lag_ratio=0.3), run_time=3)
            vo.wait_until("b")
            self.play(Create(pl.conflict), FadeIn(verdict), run_time=1.5)
        self.play(FadeOut(verdict))

        def show(k):
            name, holders, share = POSITIONS[k]
            anims, _ = pl.position((k,), name, holders, share=share, share_note=r"PhilPapers 2020" if share else "",
                                   width=4.2)
            return anims

        with self.voiceover(
            "Give up the first: there is no God. That was Mackie's own conclusion, and in the 2020 PhilPapers survey "
            "about two in three philosophers accepted or leaned toward atheism."
        ):
            self.play(*show("G"), run_time=1.2)
        self.play(*pl.reset(), run_time=0.8)
        with self.voiceover(
            "Give up omnipotence: God's power is limited. Process theologians, after Whitehead and Hartshorne, hold "
            "that God persuades rather than coerces."
        ):
            self.play(*show("omnipotent"), run_time=1.2)
        self.play(*pl.reset(), run_time=0.8)
        with self.voiceover(
            "Limit what God knows: some open theists hold that the future free choices of creatures are not yet "
            "there to be known."
        ):
            self.play(*show("omniscient"), run_time=1.2)
        self.play(*pl.reset(), run_time=0.8)
        with self.voiceover("Give up perfect goodness: an exit very few philosophers take."):
            self.play(*show("good"), run_time=1.2)
        self.play(*pl.reset(), run_time=0.8)
        with self.voiceover(
            "Deny that evil is real: some traditions call it illusion. Augustine's view, that evil is a privation, "
            "an absence of good, comes close to this exit without quite taking it."
        ):
            self.play(*show("evil"), run_time=1.2)
        self.play(*pl.reset(), run_time=0.8)
        with self.voiceover(
            "Or give up the bridge premise: a good, all-powerful being might allow evil for the sake of a greater "
            "good. Alvin Plantinga's free-will defense, from 1974, argues that a world of free creatures who "
            "sometimes do wrong may be better than any world God could make without evil. Most philosophers, theists "
            "or not, now agree that this exit is at least logically open, and that the purely logical problem of "
            "evil fails."
        ):
            self.play(*show("bridge"), run_time=1.2)
        self.clear_scene()

    def limits(self):
        q1 = VGroup(label(r"what the calculation did:", font_size=28, color=OK),
                    label(r"found every exit, exactly", font_size=28)).arrange(RIGHT, buff=0.3)
        q2 = VGroup(label(r"what it did not do:", font_size=28, color=BAD),
                    label(r"say which exits are open", font_size=28)).arrange(RIGHT, buff=0.3)
        g = VGroup(q1, q2).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(UP, buff=0.6)
        fwd = label(r"Part 23: the evidential argument, with probabilities (Rowe 1979)", font_size=24,
                    color=GREY_A).next_to(g, DOWN, buff=0.35)
        am = ArgumentMap(["p", "q"], "r", width=4.0, font_size=40, center=[-3.4, -1.7, 0])
        words = VGroup(label(r"$p$: all humans are mortal", font_size=24, color=GREY_A),
                       label(r"$q$: Socrates is human", font_size=24, color=GREY_A),
                       label(r"$r$: Socrates is mortal", font_size=24, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.6, -0.6, 0])
        v = am.verdict(font_size=24)
        with self.voiceover(
            "Notice what the calculation did, and what it did not. <bookmark mark='a'/>It found every exit, exactly, "
            "with nothing overlooked. <bookmark mark='b'/>It did not say which exits are open. Whether free will is "
            "worth the evil it permits is not a question of propositional logic. Part 23 returns to it, where the "
            "argument becomes one about probabilities."
        ) as vo:
            self.play(FadeIn(q1[0]))
            vo.wait_until("a")
            self.play(FadeIn(q1[1]))
            vo.wait_until("b")
            self.play(FadeIn(q2), FadeIn(fwd))
        with self.voiceover(
            "And notice one more thing. We wrote 'all evil' and 'every being' inside the atoms, where the logic "
            "cannot see them. <bookmark mark='a'/>Propositional logic can't look inside a sentence. 'All humans are "
            "mortal; Socrates is human; so Socrates is mortal' is, to it, p and q, therefore r: <bookmark mark='b'/>"
            "invalid, with a countermodel. To see inside sentences we need 'all' and 'some', quantifiers. That is "
            "Part 3."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(am), FadeIn(words))
            vo.wait_until("b")
            self.play(FadeIn(v, scale=1.2))
        self.clear_scene()
