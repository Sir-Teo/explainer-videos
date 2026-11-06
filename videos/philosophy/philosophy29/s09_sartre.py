from __future__ import annotations

from videos.philosophy.philosophy29.common import *  # noqa: F403


class Sartre(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"Condemned to be free", r"Do we have a nature, \ or make one?", lit=(1943, 1949),
                            part=PART)
        with self.voiceover("Chapter eight. Condemned to be free."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.essence()
        self.bad_faith()
        self.look()
        self.beauvoir()

    def essence(self):
        hc = history_card(1943, r"Jean-Paul Sartre", r"\textit{Being and Nothingness}", width=5.6,
                          color=HIST).to_corner(UL, buff=0.3)
        knife = VGroup(label(r"a paper-knife", font_size=22, color=OBJ),
                       MathTex(r"\text{essence} \;\longrightarrow\; \text{existence}", font_size=30, color=OBJ),
                       label(r"the maker's idea comes first", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.2)
        human = VGroup(label(r"a human being", font_size=22, color=BODY),
                       MathTex(r"\text{existence} \;\longrightarrow\; \text{essence}", font_size=30, color=BODY),
                       label(r"we exist first, \ and define ourselves by what we do", font_size=18, color=GREY_A)
                       ).arrange(DOWN, buff=0.2)
        VGroup(knife, human).arrange(RIGHT, buff=1.6).move_to([0, 0.2, 0])
        foot = stack([(r"`man is condemned to be free': \ no nature, \ no God, \ no excuse", BAD),
                      (r"anguish: \ the awareness that nothing settles our choices for us", GOAL)], font_size=21,
                     buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Jean-Paul Sartre read Husserl in Berlin in the 1930s, and in 1943 published Being and Nothingness. In a "
            "lecture of 1945, Existentialism Is a Humanism, he put its core in a slogan. <bookmark mark='a'/>For a "
            "made thing, like a paper-knife, essence comes before existence: the maker had the idea of it, its "
            "purpose and design, before it existed. <bookmark mark='b'/>For a human being it is the other way round. "
            "Existence precedes essence. We exist first, and only afterwards define ourselves, by what we do. "
            "<bookmark mark='c'/>There is no human nature that settles in advance what we should be, and, for "
            "Sartre, no God who conceived us. So we are condemned to be free. <bookmark mark='d'/>Anguish is the "
            "awareness of this: nothing outside our choices settles them for us."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(knife))
            vo.wait_until("b")
            self.play(FadeIn(human))
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def bad_faith(self):
        head = label(r"Bad faith", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        axis = Line([-5.2, 1.0, 0], [5.2, 1.0, 0], color=GREY_B, stroke_width=3)
        lt = label(r"facticity: \ what I am, \ given", font_size=20, color=OBJ).next_to(axis.get_start(), DOWN, buff=0.2)
        rt = label(r"transcendence: \ what I can make of it", font_size=20, color=ACT).next_to(axis.get_end(), DOWN,
                                                                                              buff=0.2)
        dot = Dot([0, 1.0, 0], radius=0.14, color=BODY)
        dl = label(r"a human being holds both", font_size=18, color=BODY).next_to(dot, UP, buff=0.15)
        rows = [
            (r"the waiter", r"too precise, \ too eager: \ he plays at being a waiter, \ as if he were one the way an "
                            r"inkwell is an inkwell", OBJ),
            (r"the woman on a date", r"leaves her hand in his, \ and treats it as a thing, \ so as not to decide", ACT),
            (r"bad faith", r"lying to oneself: \ collapsing into pure facticity \ (`I am just like this'), \ or into "
                           r"pure transcendence", BAD),
        ]
        g = rows_table(rows, top=-0.4, gap=0.42)
        with self.voiceover(
            "Freedom is hard to bear, so we flee it, and Sartre's name for the flight is bad faith. "
            "<bookmark mark='a'/>A human being is both facticity, what is given, our past, our body, our situation, "
            "and transcendence, what we can make of it. <bookmark mark='b'/>A café waiter's movements are a little "
            "too precise, a little too eager. He is playing at being a waiter, as if he could be a waiter the way an "
            "inkwell is an inkwell. <bookmark mark='c'/>A woman on a first date lets her companion take her hand, "
            "and leaves it there as though it were a thing, not hers, to avoid deciding. "
            "<bookmark mark='d'/>Bad faith is lying to oneself: collapsing into pure facticity, I am just like this, "
            "I can't help it; or into pure transcendence, I am not really what I have done."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(lt), FadeIn(rt))
            vo.wait_until("a")
            self.play(FadeIn(dot), FadeIn(dl))
            vo.wait_until("b")
            self.play(FadeIn(g[0]), dot.animate.move_to(axis.get_start()))
            vo.wait_until("c")
            self.play(FadeIn(g[1]))
            vo.wait_until("d")
            self.play(FadeIn(g[2]), dot.animate.move_to([0, 1.0, 0]))
        self.clear_scene()

    def look(self):
        head = label(r"The look", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the keyhole", r"absorbed in spying, \ I hear footsteps behind me: \ suddenly I \textit{am} someone, \ "
                             r"seen, \ ashamed", BODY),
            (r"being-for-others", r"the other's look makes me an object, \ with a nature I cannot control", OBJ),
            (r"\textit{No Exit} \ (1944)", r"`hell is other people': \ three people, \ one room, \ each the others' "
                                           r"judge", BAD),
            (r"Fanon \ (1952)", r"\textit{Black Skin, \ White Masks}: \ the look that fixes a person by race, \ "
                                r"described from within", ACT),
        ]
        g = rows_table(rows, top=1.6, gap=0.5)
        with self.voiceover(
            "Others complicate freedom. <bookmark mark='a'/>Sartre's example: I am looking through a keyhole, wholly "
            "absorbed in what is going on inside, not even aware of myself. Then I hear footsteps in the corridor "
            "behind me, and suddenly I am someone: seen, a spy, ashamed. <bookmark mark='b'/>The look of the other "
            "makes me an object, with a nature I did not choose and cannot control. <bookmark mark='c'/>In his play No "
            "Exit, three people are shut in a room forever, each the judge of the others, and one of them concludes "
            "that hell is other people. <bookmark mark='d'/>Frantz Fanon, in Black Skin, White Masks, in 1952, turned "
            "the phenomenology of the look on race: what it is to be fixed, from outside, by a gaze that has already "
            "decided what you are."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def beauvoir(self):
        hc = history_card(1949, r"Simone de Beauvoir", r"\textit{The Second Sex}", width=5.0, color=HIST).to_corner(
            UL, buff=0.3)
        q = quote_card(r"One is not born, \ but rather becomes, \ a woman.", r"Simone de Beauvoir", r"1949",
                       width=7.4, font_size=30).move_to([0, 1.2, 0])
        rows = [
            (r"the Other", r"man is defined as the subject, \ the absolute; \ woman as the Other, \ relative to him",
             BODY),
            (r"situated freedom", r"freedom is always exercised in a situation, \ and oppression is a situation that "
                                  r"closes it down", ACT),
            (r"\textit{The Ethics of Ambiguity} \ (1947)", r"to will oneself free is also to will others free", OK),
        ]
        g = rows_table(rows, top=-0.4, gap=0.42)
        with self.voiceover(
            "Simone de Beauvoir, Sartre's companion and an original philosopher in her own right, published The "
            "Second Sex in 1949. <bookmark mark='a'/>Its most famous sentence: one is not born, but rather becomes, "
            "a woman. What it is to be a woman is not given by nature but made, in a situation, by others and by "
            "oneself. <bookmark mark='b'/>Men had defined themselves as the subject, the absolute, and women as the "
            "Other, defined relative to them. <bookmark mark='c'/>Against Sartre's early picture of freedom as "
            "absolute, Beauvoir stressed situated freedom: freedom is always exercised in a situation, and "
            "oppression is a situation that closes it down. <bookmark mark='d'/>Her Ethics of Ambiguity, of 1947, "
            "argued that to will oneself free is also to will others free. The book founded much of modern feminist "
            "philosophy."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(q))
            for mk, r in zip("bcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
