from __future__ import annotations

from videos.philosophy.philosophy23.common import *  # noqa: F403


class Traditions(VoiceoverScene):
    def construct(self):
        card = chapter_card(14, r"Arguments beyond the West", r"What did Buddhist, \ Nyāya and Islamic philosophers "
                            r"argue?", lit=(640, 1037), part=PART)
        with self.voiceover("Chapter fourteen. Arguments beyond the West."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.udayana()
        self.dharmakirti()
        self.avicenna()
        self.dao()

    def udayana(self):
        hc = history_card(984, r"Udayana", r"\textit{Nyāyakusumāñjali}", width=5.4, color=HIST).to_corner(UL,
                                                                                                         buff=0.3)
        rows = stack([(r"the earth is an effect, \ like a pot: \ so it has a maker with knowledge of its materials",
                       DIV),
                      (r"atoms combine at creation: \ something must set them in motion", ARG),
                      (r"the world is held in place, \ and will be dissolved: \ by a sustaining will", NAT),
                      (r"Nyāya: \ a careful theory of inference, \ applied to Īśvara, \ the lord", ABS),
                      (r"the objections he answers: \ the pot's maker has a body, \ and is many; \ Īśvara has neither",
                       GOAL)], font_size=21, aligned_edge=LEFT, width=12.2, buff=0.3).move_to([0, -0.4, 0])
        with self.voiceover(
            "Philosophy of religion is not only a Western conversation. <bookmark mark='a'/>In India, the Nyāya "
            "school built arguments for a creator, Īśvara, on its theory of inference. Udayana, around 984, argued: "
            "the earth is an effect, like a pot, so it has a maker who knows its materials. <bookmark mark='b'/>At "
            "creation the atoms combine, and something must set them moving. <bookmark mark='c'/>The world is held "
            "in place and will one day be dissolved, which requires a sustaining will. <bookmark mark='d'/>These are "
            "design and cosmological arguments, framed in Nyāya's careful theory of inference from signs. "
            "<bookmark mark='e'/>Udayana answered objections: the makers of pots have bodies and are many; Īśvara has "
            "no body and is one, so the analogy fails there. He argued that such differences are irrelevant to the "
            "inference."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def dharmakirti(self):
        d = load("dharma")
        hc = history_card(640, r"Dharmakīrti", r"\textit{Pramāṇavārttika}", width=5.2, color=HIST).to_corner(
            UL, buff=0.3)
        rows = VGroup()
        for i, c in enumerate(d["claims"]):
            y = 1.3 - 0.62 * i
            a = label(c["text"], font_size=21, color=WHITE)
            a.move_to([-6.2 + a.width / 2, y, 0])
            b = MathTex(c["formula"].replace("->", r"\to").replace("&", r"\land").replace("~", r"\lnot "),
                        font_size=24, color=ABS)
            b.move_to([4.2 + b.width / 2, y, 0])
            rows.add(VGroup(a, b))
        verdict = label(r"jointly inconsistent: \ the Reasoner finds each single claim a way out", font_size=21,
                        color=BAD).move_to([0, -1.3, 0])
        rows2 = stack([(r"Dharmakīrti: \ so a permanent God cannot be the cause of a changing world", WHITE),
                       (r"Nyāya's reply: \ God's will works through other conditions, \ which change", DIV)],
                      font_size=20, aligned_edge=LEFT, width=12.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Buddhist philosophers argued the other way. <bookmark mark='a'/>Dharmakīrti, in the seventh century, "
            "posed a dilemma for a permanent creator. The creator is permanent, unchanging at every moment. It is by "
            "itself a sufficient cause of the world's events. Those events arise one after another, not all at once. "
            "And an unchanging sufficient cause would produce all its effects at once, since nothing about it is "
            "different at one moment from another. <bookmark mark='b'/>The four claims are inconsistent, and the "
            "Reasoner shows that giving up any one of them restores consistency. <bookmark mark='c'/>Dharmakīrti "
            "concluded that nothing permanent can cause a changing world. <bookmark mark='d'/>The Nyāya reply gave up "
            "the second claim: God's will operates together with other conditions, the merits of beings, the "
            "seasons, the materials, and those conditions change."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.35), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(verdict))
            for mk, r in zip("cd", rows2):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def avicenna(self):
        hc = history_card(1037, r"Avicenna \ (Ibn Sīnā)", r"\textit{al-Ishārāt}; \ \textit{al-Najāt}", width=6.0,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = stack([(r"every existent is, \ in itself, \ either necessary or possible", ABS),
                      (r"a possible existent exists only through something else, \ which makes it exist", WHITE),
                      (r"the whole collection of possibles is itself possible, \ so it too needs a cause", ARG),
                      (r"that cause cannot be within the collection: \ so a Necessary Existent exists", DIV),
                      (r"unlike the \textit{kalām}, \ it needs no beginning: \ an eternal world still depends on it",
                       GOAL)], font_size=21, aligned_edge=LEFT, width=12.2, buff=0.3).move_to([0, -0.4, 0])
        with self.voiceover(
            "Avicenna, the Persian philosopher Ibn Sīnā, gave the contingency argument its classic form, five "
            "centuries before Leibniz. <bookmark mark='a'/>Every existent is, considered in itself, either necessary "
            "or merely possible. <bookmark mark='b'/>A merely possible existent exists only through something else "
            "that makes it exist. <bookmark mark='c'/>The whole collection of possible existents is itself possible, "
            "so it too needs a cause. <bookmark mark='d'/>That cause cannot be inside the collection; so there is a "
            "Necessary Existent, which exists through itself. <bookmark mark='e'/>Unlike the kalām, the argument "
            "needs no beginning in time. Avicenna held the world to be eternal, yet eternally dependent; it was "
            "al-Ghazālī who objected, and argued for a beginning."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def dao(self):
        head = label(r"A ground that is not a person", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        q = quote_card(r"The Dao that can be told \ is not the constant Dao.", r"\textit{Daodejing}", r"chapter 1",
                       width=7.6, font_size=26).move_to([0, 1.4, 0])
        rows = stack([(r"the Dao gives rise to the ten thousand things \ without intending, \ ruling or owning them",
                       NAT),
                      (r"an answer to Leibniz's question \ that is not an agent: \ compare Spinoza's \textit{Deus sive "
                       r"Natura}", ABS),
                      (r"and Buddhist dependent arising \ (Part 21): \ no first cause, \ only conditions", HUM),
                      (r"the arguments of this part assume a personal God: \ these traditions question the "
                       r"assumption", GOAL)], font_size=21, aligned_edge=LEFT, width=12.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Some traditions answer Leibniz's question without a person at all. <bookmark mark='a'/>The Daodejing "
            "opens: the Dao that can be told is not the constant Dao. <bookmark mark='b'/>The Dao gives rise to the "
            "ten thousand things without intending, ruling or owning them. <bookmark mark='c'/>It is a ground that "
            "is not an agent; compare Spinoza's God or Nature. <bookmark mark='d'/>Buddhist dependent arising, from "
            "Part 21, offers no first cause, only conditions. <bookmark mark='e'/>Most of the arguments in this part "
            "assume that the answer, if there is one, is a person. These traditions question that assumption."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(q))
            for mk, r in zip("bcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
