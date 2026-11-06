from __future__ import annotations

from videos.philosophy.philosophy29.common import *  # noqa: F403


def box(text, col, dashed=False, w=2.6):
    t = label(text, font_size=21, color=col)
    r = RoundedRectangle(width=max(w, t.width + 0.4), height=0.62, corner_radius=0.12, color=col, stroke_width=2)
    if dashed:
        r = DashedVMobject(r, num_dashes=28)
    return VGroup(r, t)


class Brentano(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"Consciousness of something", r"What makes a thought \textit{about} anything?",
                            lit=(1874,), part=PART)
        with self.voiceover("Chapter one. Consciousness of something."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.thesis()
        self.arrows()
        self.triad()
        self.legacy()

    def thesis(self):
        hc = history_card(1874, r"Franz Brentano", r"\textit{Psychology from an Empirical Standpoint}", width=6.6,
                          color=HIST).to_corner(UL, buff=0.3)
        q = quote_card(r"Every mental phenomenon is characterized by what the Scholastics of the Middle Ages called "
                       r"the intentional \dots\ inexistence of an object, \ and what we might call \dots\ reference to "
                       r"a content, \ direction toward an object.", r"Franz Brentano", r"1874", width=10.6,
                       font_size=24).move_to([0, -0.6, 0])
        foot = label(r"Brentano's thesis: \ intentionality is the mark of the mental", font_size=22,
                     color=GOAL).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "In 1874 Franz Brentano, a former priest teaching in Vienna, set out to make psychology a science, and "
            "began by asking what separates mental phenomena from physical ones. <bookmark mark='a'/>His answer: "
            "every mental phenomenon is characterized by what the Scholastics of the Middle Ages called the "
            "intentional inexistence of an object, what we might call reference to a content, or direction toward "
            "an object. <bookmark mark='b'/>Seeing is seeing something; judging is judging something; loving is "
            "loving someone. No physical phenomenon, he claimed, is directed like this. Intentionality, from the "
            "Latin for aiming, is the mark of the mental. This is Brentano's thesis."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def arrows(self):
        head = label(r"Directed, \ even at nothing", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        acts = [r"seeing", r"fearing", r"hoping for", r"thinking of"]
        objs = [(r"the oak tree", False), (r"the dog next door", False), (r"rain tomorrow", True),
                (r"Pegasus", True)]
        rows = VGroup()
        for i, (a, (o, ghost)) in enumerate(zip(acts, objs)):
            y = 1.5 - 1.05 * i
            ab = box(a, ACT).move_to([-3.6, y, 0])
            ob = box(o, OBJ, dashed=ghost).move_to([2.6, y, 0])
            ar = Arrow(ab.get_right(), ob.get_left(), buff=0.12, color=GREY_B, stroke_width=3)
            rows.add(VGroup(ab, ar, ob))
        tags = VGroup(label(r"not yet", font_size=17, color=GREY_A).next_to(rows[2][2], RIGHT, buff=0.2),
                      label(r"never", font_size=17, color=BAD).next_to(rows[3][2], RIGHT, buff=0.2))
        foot = stack([(r"a physical relation needs both ends: \ you cannot kick what does not exist", WHITE),
                      (r"yet you can think of it: \ the act is complete, \ with nothing at the other end", BAD)],
                     font_size=21, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Picture the acts on one side and their objects on the other. <bookmark mark='a'/>Seeing the oak tree. "
            "Fearing the dog next door. <bookmark mark='b'/>Hoping for rain tomorrow, which does not exist yet. "
            "<bookmark mark='c'/>Thinking of Pegasus, which never will. <bookmark mark='d'/>That is the puzzle. A "
            "physical relation needs both its ends: you cannot kick what does not exist, or stand next to it. "
            "<bookmark mark='e'/>But you can think of it, and the thinking is complete, with nothing at the other "
            "end. Brentano's phrase, intentional inexistence, meant existence in the mind: the object of a thought "
            "exists, he suggested, as an object of the thought. Whether that is an answer or a restatement of the "
            "puzzle has been argued ever since."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(tags[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3]), FadeIn(tags[1]))
            vo.wait_until("d")
            self.play(FadeIn(foot[0]))
            vo.wait_until("e")
            self.play(FadeIn(foot[1]), Indicate(rows[3][1], color=BAD))
        self.clear_scene()

    def triad(self):
        head = label(r"Act, \ content, \ object", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        a = box(r"the act", ACT, w=2.4).move_to([-4.2, 1.4, 0])
        c = box(r"the content", SIGN, w=2.4).move_to([0, 1.4, 0])
        o = box(r"the object", OBJ, w=2.4).move_to([4.2, 1.4, 0])
        ar = VGroup(Arrow(a.get_right(), c.get_left(), buff=0.1, color=GREY_B),
                    Arrow(c.get_right(), o.get_left(), buff=0.1, color=GREY_B))
        subs = VGroup(label(r"thinking", font_size=18, color=ACT).next_to(a, DOWN, buff=0.15),
                      label(r"in the mind: \ always there", font_size=18, color=SIGN).next_to(c, DOWN, buff=0.15),
                      label(r"in the world: \ may be missing", font_size=18, color=OBJ).next_to(o, DOWN, buff=0.15))
        rows = [
            (r"Twardowski \ (1894)", r"separates the content of a presentation from its object: \ the content exists "
                                     r"whenever the act does", SIGN),
            (r"Meinong \ (1904)", r"objects need not exist: \ the golden mountain, \ even the round square, \ have "
                                  r"properties", OBJ),
            (r"Russell \ (1905)", r"no: \ `the golden mountain' is a description, \ not a name \ (Part 27)", HIST),
            (r"Husserl", r"the object is meant through a sense, \ the noema: \ the next chapter", ACT),
        ]
        g = rows_table(rows, top=0.0, gap=0.36)
        with self.voiceover(
            "Brentano's students pulled the thesis apart. <bookmark mark='a'/>Kazimierz Twardowski, in 1894, "
            "distinguished three things: the act of thinking, its content, and its object. The content is in the "
            "mind and exists whenever the act does. The object is what the act is about, and may be missing. "
            "<bookmark mark='b'/>Alexius Meinong went further: there are objects that do not exist, like the golden "
            "mountain, and even impossible ones, like the round square, which really is round and square. "
            "<bookmark mark='c'/>Russell's theory of descriptions, from Part 27, was in part a reply: the golden "
            "mountain is a description, not a name, and no object is needed. <bookmark mark='d'/>And Husserl, "
            "another of Brentano's students, said that an act reaches its object through a sense, which he called "
            "the noema. That is where phenomenology begins."
        ) as vo:
            self.play(FadeIn(head), FadeIn(a), FadeIn(c), FadeIn(o), GrowArrow(ar[0]), GrowArrow(ar[1]),
                      FadeIn(subs))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def legacy(self):
        head = label(r"The thesis, \ since", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Chisholm \ (1957)", r"marks of intentional sentences: \ existence does not follow \ (`I think of "
                                   r"Pegasus'), \ nor does substitution \ (Part 27's belief reports)", SIGN),
            (r"pains and moods", r"is a pain about anything? \ a free-floating anxiety? \ the main counterexamples to "
                                 r"the thesis", BAD),
            (r"intentionalism", r"yes: \ even a pain represents damage in a part of the body \ (Tye, \ Crane)", ACT),
            (r"naturalizing", r"if minds are physical, \ how can a physical state be \textit{about} anything? \ "
                              r"Part 30", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.5)
        with self.voiceover(
            "The thesis has had a long life. <bookmark mark='a'/>Roderick Chisholm, in 1957, gave logical marks of "
            "sentences about intentional states. From I think of Pegasus, it does not follow that there is a "
            "Pegasus; and co-referring names cannot always be swapped without changing the truth value, the failures "
            "of substitution that Part 27 found in belief reports. <bookmark mark='b'/>Is every mental state intentional? The main "
            "counterexamples are pains and moods. Is a pain about anything? Is a free-floating anxiety? "
            "<bookmark mark='c'/>Intentionalists, like Michael Tye and Tim Crane, say yes: a pain represents damage "
            "in a part of the body, and a mood is directed at the world as a whole. <bookmark mark='d'/>And the "
            "hardest question it raises is for physicalists. If minds are physical systems, how can a physical state "
            "be about anything, let alone about something that does not exist? Part 30 takes up that question."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
