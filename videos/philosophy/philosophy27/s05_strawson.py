from __future__ import annotations

from videos.philosophy.philosophy27.common import *  # noqa: F403


class Strawson(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Presupposition and use", r"Is a sentence about nothing false, \ or neither?",
                            lit=(1950, 1966), part=PART)
        with self.voiceover("Chapter four. Presupposition and use."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.gaps()
        self.incomplete()
        self.party()
        self.semantic()

    def gaps(self):
        d = load("strawson")
        hc = history_card(1950, r"P. F. Strawson", r"`On Referring'", width=5.0, color=HIST).to_corner(UL, buff=0.3)
        rows = stack([(r"a sentence is not true or false; \ a \textit{use} of it, \ to make a statement, \ is", WHITE),
                      (r"using `the K' presupposes that there is a unique K", NAME),
                      (r"if the presupposition fails, \ the question of truth does not arise: \ a gap", BAD)],
                     font_size=21, aligned_edge=LEFT, width=7.4, buff=0.26).next_to(hc, RIGHT, buff=0.4).align_to(
            hc, UP)
        hd = [r"\text{model}", r"\text{Russell: } B", r"\text{Russell: } \neg B", r"\text{Strawson: } B",
              r"\text{Strawson: } \neg B"]
        rows_g = [[label(r["model"], font_size=20, color=WORLD), tv(r["russell"]["the K is B"], 22),
                   tv(r["russell"]["the K is not B"], 22), tv(r["strawson"]["the K is B"], 22),
                   tv(r["strawson"]["the K is not B"], 22)] for r in d["rows"]]
        grid = ValueGrid(hd, rows_g, col_w=[3.4, 2.0, 2.2, 2.2, 2.4], cell_h=0.45, font_size=20).move_to([0, -1.5, 0])
        nk = next(r for r in d["rows"] if r["model"] == "no king")
        assert nk["strawson"] == {"the K is B": None, "the K is not B": None}
        assert nk["russell"] == {"the K is B": False, "the K is not B": False}
        foot = label(r"dash: \ neither true nor false \ (Part 5's three values return)", font_size=18,
                     color=GREY_A).next_to(grid, DOWN, buff=0.15)
        with self.voiceover(
            "In 1950 Peter Strawson objected. <bookmark mark='a'/>Sentences, he said, are not true or false; uses of "
            "sentences, to make statements, are. <bookmark mark='b'/>Someone who uses the phrase the present king of "
            "France presupposes that there is one. <bookmark mark='c'/>If there is not, they have failed to say "
            "anything true or false: the question of truth does not arise. <bookmark mark='d'/>Here are the two "
            "views side by side, model by model. Where there is exactly one king, they agree. Where there is no "
            "king, or two, Russell says false, and false again for the narrow negation; Strawson says neither. "
            "Truth-value gaps, from Part 5's three-valued logics, have come back as a theory of meaning."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("d")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(rows_g)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.4)
            self.play(FadeIn(foot))
        self.clear_scene()

    def incomplete(self):
        d = load("incomplete")
        head = label(r"`The table is covered with books'", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        room = RoundedRectangle(width=3.6, height=2.6, corner_radius=0.15, color=WORLD).move_to([-3.6, 0.2, 0])
        rtag = label(r"this room", font_size=18, color=WORLD).next_to(room, UP, buff=0.1)
        t1 = Rectangle(width=1.4, height=0.5, color=REF, fill_opacity=0.4).move_to([-3.6, 0.0, 0])
        books = VGroup(*[Rectangle(width=0.18, height=0.32, color=TRUTH, fill_opacity=0.8) for _ in range(4)]).arrange(
            RIGHT, buff=0.05).next_to(t1, UP, buff=0.02)
        far = VGroup(*[Rectangle(width=1.0, height=0.36, color=REF, fill_opacity=0.25).move_to([x, -2.0, 0])
                       for x in (-5.2, -3.6, -2.0)][1:])
        ftag = label(r"two more tables, \ elsewhere in the world", font_size=17, color=GREY_A).next_to(far, DOWN,
                                                                                                     buff=0.1)
        assert d["tables_in_world"] == 3 and not d["unrestricted"] and d["restricted"]
        rows = stack([(r"over the whole world: \ no unique table, \ so false", BAD),
                      (r"over the domain the context makes relevant: \ true", OK),
                      (r"so context restricts the quantifiers, \ as in `everyone is here'", GOAL),
                      (r"the incomplete descriptions problem, \ for Russell and Strawson alike", HIST)], font_size=21,
                     aligned_edge=LEFT, width=6.0, buff=0.3).move_to([3.4, 0.0, 0])
        with self.voiceover(
            "Both views face a problem with ordinary talk. <bookmark mark='a'/>Say the table is covered with books, "
            "in a room with one table. <bookmark mark='b'/>But the world has many tables. Read literally, Russell's "
            "uniqueness clause fails, and the sentence comes out false. The Reasoner checks: false over the whole "
            "world. <bookmark mark='c'/>Restricted to the room, true. <bookmark mark='d'/>The usual answer is that "
            "context restricts the domain of quantification, as it does in everyone is here, which never means "
            "everyone in the universe. <bookmark mark='e'/>How context does this, and whether it is semantics or "
            "pragmatics, is still debated."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(room), FadeIn(rtag), FadeIn(t1), FadeIn(books))
            vo.wait_until("b")
            self.play(FadeIn(far), FadeIn(ftag))
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]), Indicate(room, color=OK))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def party(self):
        d = load("donnellan")
        hc = history_card(1966, r"Keith Donnellan", r"`Reference and Definite Descriptions'", width=6.2,
                          color=HIST).to_corner(UL, buff=0.3)
        people = {}
        xs = {"jones": -3.8, "smith": 0.0, "brown": 3.8}
        for p, x in xs.items():
            body = VGroup(Circle(0.28, color=SPEAK, fill_opacity=0.3), Line([x, -0.15, 0], [x, -1.0, 0], color=SPEAK))
            body[0].move_to([x, 0.2, 0])
            nm = label(p.capitalize(), font_size=21, color=SPEAK).next_to(body, DOWN, buff=0.12)
            dr = label(d["drinks"][p], font_size=17, color=GREY_A).next_to(nm, DOWN, buff=0.08)
            people[p] = VGroup(body, nm, dr)
        sent = label(r"`The man drinking a martini is a philosopher.'", font_size=26, color=TRUTH).move_to([0, 1.7, 0])
        assert d["semantic_referent"] == "smith" and d["speaker_referent"] == "jones"
        assert not d["attributive_true"] and d["referential_true"]
        a_sem = Arrow(sent.get_bottom() + RIGHT * 0.3, people["smith"][0].get_top(), color=REF, buff=0.1)
        a_spk = Arrow(sent.get_bottom() + LEFT * 1.5, people["jones"][0].get_top(), color=SPEAK, buff=0.1)
        tags = stack([(r"attributive: \ whoever uniquely drinks a martini: \ Smith, \ not a philosopher: \ false",
                       REF),
                      (r"referential: \ the man the speaker means: \ Jones, \ a philosopher: \ true", SPEAK)],
                     font_size=21, aligned_edge=LEFT, width=12.0, buff=0.25).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Keith Donnellan, in 1966, noticed that descriptions are used in two ways. <bookmark mark='a'/>At a "
            "party, someone says: the man drinking a martini is a philosopher. <bookmark mark='b'/>The speaker is "
            "looking at Jones, whose martini glass holds only water. In the corner, unnoticed, Smith is drinking the "
            "only martini. <bookmark mark='c'/>Used attributively, the description is about whoever fits it: Smith, "
            "who is no philosopher, so the statement is false. <bookmark mark='d'/>Used referentially, it is a "
            "tool for picking out the man the speaker has in mind: Jones, who is a philosopher. Something true has "
            "been said about him, with a description he does not fit."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(sent))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(people[p]) for p in ("jones", "smith", "brown")], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(GrowArrow(a_sem), FadeIn(tags[0]))
            vo.wait_until("d")
            self.play(GrowArrow(a_spk), FadeIn(tags[1]))
        self.clear_scene()

    def semantic(self):
        head = label(r"What is said, \ and what is meant", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Kripke \ (1977)", r"semantic reference is fixed by the words; \ speaker's reference by the speaker's "
                                 r"intentions", HIST),
            (r"so", r"Russell's theory can stand as semantics; \ Donnellan's cases are about communication", REF),
            (r"the test", r"would a language that encoded both uses separately behave differently? \ Kripke thought "
                          r"not", SENSE),
            (r"today", r"linguists still divide over whether `the' quantifies \ (Russell) \ or refers to a familiar "
                       r"object \ (Strawson, \ Heim)", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "Saul Kripke replied in 1977 with a distinction that is now standard. <bookmark mark='a'/>Semantic "
            "reference is fixed by the words and the conventions of the language; speaker's reference by what the "
            "speaker intends to talk about. <bookmark mark='b'/>So Russell's theory can stand as an account of "
            "semantics, and Donnellan's cases become facts about communication: the speaker said something false, "
            "and conveyed something true. <bookmark mark='c'/>Kripke's test: imagine a language that encoded the two "
            "uses with different words. If it would work just as English does, the distinction is not semantic. "
            "<bookmark mark='d'/>The debate continues in linguistics, between treating the as a quantifier, with "
            "Russell, and treating it as a marker of a familiar, presupposed object, with Strawson and Irene Heim."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
