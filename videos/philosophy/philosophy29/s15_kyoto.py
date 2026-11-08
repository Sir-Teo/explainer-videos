from __future__ import annotations

from videos.philosophy.philosophy29.common import *  # noqa: F403


class Kyoto(VoiceoverScene):
    def construct(self):
        card = chapter_card(14, r"The place of nothingness", r"What is experience before subject and object?",
                            lit=(1240, 1911), part=PART)
        with self.voiceover("Chapter fourteen. The place of nothingness."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.nishida()
        self.basho()
        self.school()
        self.dogen()

    def nishida(self):
        hc = history_card(1911, r"Nishida Kitar\=o", r"\textit{An Inquiry into the Good}", width=5.6,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = [
            (r"pure experience", r"experience before it is split into a subject and an object: \ hearing the music, "
                                 r"\ not yet `I hear music'", ACT),
            (r"sources", r"William James's radical empiricism, \ and the practice of Zen", HIST),
            (r"the aim", r"to explain everything from pure experience as the only reality", GOAL),
        ]
        g = rows_table(rows, top=1.0, gap=0.6)
        with self.voiceover(
            "Phenomenology also met a philosophy that had grown up in Kyoto. In 1911 Nishida Kitarō published An "
            "Inquiry into the Good, the first major work of modern Japanese philosophy. "
            "<bookmark mark='a'/>Its starting point is pure experience: experience before it is split into a subject "
            "and an object. When you are absorbed in music, there is the music; only afterwards comes the judgement, "
            "I hear music. <bookmark mark='b'/>Nishida drew on William James's radical empiricism, and on years of "
            "Zen practice. <bookmark mark='c'/>His aim was to explain everything from pure experience, as the only "
            "reality."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abc", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def basho(self):
        head = label(r"The logic of place \ (\textit{basho}, \ 1926)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        cen = np.array([-3.3, -0.5, 0])
        rings = VGroup(Circle(radius=3.0, color=BODY, fill_opacity=0.08).move_to(cen),
                       Circle(radius=2.0, color=TIME, fill_opacity=0.10).move_to(cen),
                       Circle(radius=1.05, color=OBJ, fill_opacity=0.15).move_to(cen))
        tags = VGroup(VGroup(label(r"being", font_size=17, color=OBJ), label(r"objects judged", font_size=15,
                                                                            color=OBJ)).arrange(DOWN, buff=0.08
                                                                                                ).move_to(cen),
                      label(r"relative nothingness: \ consciousness", font_size=16, color=TIME).move_to(
                          cen + UP * 1.52),
                      label(r"absolute nothingness", font_size=17, color=BODY).move_to(cen + UP * 2.5))
        rows = stack([(r"every judgement places a subject \textit{in} a universal: \ `the rose is red'", OBJ),
                      (r"objects are placed in consciousness, \ which is no object: \ a relative nothing", TIME),
                      (r"consciousness is placed in what has no further place: \ absolute nothingness", BODY),
                      (r"not a thing, \ but the field in which everything, \ the self included, \ appears", GOAL)],
                     font_size=19, aligned_edge=LEFT, width=5.4, buff=0.3).move_to([3.6, -0.3, 0])
        with self.voiceover(
            "Nishida's mature thought is a logic of place, basho. <bookmark mark='a'/>Aristotle's logic is a logic of "
            "the subject: the rose is red puts the rose in the universal red. Nishida reads every judgement as "
            "placing something within a wider place. <bookmark mark='b'/>Objects are placed within consciousness. "
            "But consciousness is not one more object; relative to objects, it is a nothing. "
            "<bookmark mark='c'/>And consciousness in turn is placed within a place that has no further place: "
            "absolute nothingness. <bookmark mark='d'/>This nothingness is not a thing, and not the mere absence of "
            "things. It is the field in which everything, the self included, appears: closer, Nishida thought, to "
            "the Buddhist idea of emptiness than to any Western concept of being."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rings[2]), FadeIn(tags[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rings[1]), FadeIn(tags[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rings[0]), FadeIn(tags[2]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def school(self):
        head = label(r"The Kyoto school", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Nishitani Keiji", r"\textit{Religion and Nothingness} \ (1961): \ through nihilism to the field of "
                                 r"emptiness, \ \textit{\'s\=unyat\=a}", BODY),
            (r"Watsuji Tetsur\=o", r"\textit{F\=udo} \ (1935): \ Heidegger neglected space and climate; \ the human "
                                   r"being is `betweenness', \ \textit{aidagara}", WORLD),
            (r"with Heidegger", r"`A Dialogue on Language between a Japanese and an Inquirer' \ (1959)", HIST),
            (r"the war", r"members joined wartime discussions on Japan's world-historical role: \ \textit{Rude "
                         r"Awakenings} \ (1994) \ weighs the record", BAD),
        ]
        g = rows_table(rows, top=1.6, gap=0.45)
        with self.voiceover(
            "Nishida's students and colleagues became known as the Kyoto school. <bookmark mark='a'/>Nishitani Keiji, "
            "who had studied with Heidegger in Freiburg, argued in Religion and Nothingness that the way through "
            "European nihilism leads to the Buddhist field of emptiness, śūnyatā. <bookmark mark='b'/>Watsuji "
            "Tetsurō, reading Being and Time, objected that Heidegger had made existence a matter of time and "
            "neglected space, climate and community; the human being, ningen, is a betweenness, aidagara. "
            "<bookmark mark='c'/>Heidegger, for his part, wrote a dialogue with a Japanese visitor, published "
            "in 1959, about whether the two traditions could understand each other at all. <bookmark mark='d'/>Like "
            "Heidegger, the school has a wartime shadow: some of its members joined published discussions on Japan's "
            "world-historical role, and how far the philosophy of nothingness lent itself to nationalism is weighed in "
            "a collection of 1994, Rude Awakenings."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def dogen(self):
        q = quote_card(r"The time we call `being-time' means that time is already being, \ and all being is time.",
                       r"D\=ogen", r"\textit{Sh\=ob\=ogenz\=o}, \ `Uji' \ (1240)", width=9.6, font_size=26).move_to(
            [0, 1.4, 0])
        rows = stack([(r"no being outside time, \ no time apart from beings: \ the pine is time, \ the bamboo is time",
                       TIME),
                      (r"N\=ag\=arjuna \ (c. 150): \ emptiness is dependent origination: \ nothing has a nature on "
                       r"its own", BODY),
                      (r"his four corners \ (Part 5): \ is, \ is not, \ both, \ neither", SIGN),
                      (r"seven centuries before Heidegger, \ being thought \textit{as} time", GOAL)], font_size=21,
                     aligned_edge=LEFT, width=12.0, buff=0.28).move_to([0, -1.4, 0])
        with self.voiceover(
            "The dialogue had deep roots. <bookmark mark='a'/>In 1240 the Zen master Dōgen wrote an essay called "
            "Uji, being-time: time is already being, and all being is time. <bookmark mark='b'/>There is no being "
            "outside time, and no time apart from beings: the pine tree is time, the bamboo is time. "
            "<bookmark mark='c'/>Behind Dōgen stands Nāgārjuna, around the year 150, for whom emptiness means "
            "dependent origination: nothing has a nature on its own, apart from its relations. "
            "<bookmark mark='d'/>His four-cornered logic, is, is not, both, neither, was Part 5's. "
            "<bookmark mark='e'/>Seven centuries before Being and Time, being had been thought as time."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            for mk, r in zip("bcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
