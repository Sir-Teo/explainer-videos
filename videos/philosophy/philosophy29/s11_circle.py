from __future__ import annotations

from videos.philosophy.philosophy29.common import *  # noqa: F403

TEXT_COL = {"the boatman's text": WORLD, "a text that cannot answer back": GREY_A, "a mixed text": SIGN}


class Hermeneutic(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"The hermeneutic circle", r"How can we understand a whole from its parts, \ and the "
                                                            r"parts from the whole?", lit=(1960,), part=PART)
        with self.voiceover("Chapter ten. The hermeneutic circle."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.history()
        self.gadamer()
        self.toy()
        self.debates()

    def history(self):
        head = label(r"Interpretation, \ from Bible to being", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Schleiermacher", r"understanding a text: \ each sentence through the whole work, \ the work through "
                                r"its sentences \ (lectures, \ 1819--1833)", SIGN),
            (r"Dilthey", r"the human sciences \textit{understand} \ (\textit{Verstehen}); \ the natural sciences "
                         r"\textit{explain} \ (1883)", ACT),
            (r"Heidegger", r"understanding is not a method but our way of being: \ we always come with a "
                           r"fore-structure", WORLD),
        ]
        g = rows_table(rows, top=1.4, gap=0.6)
        with self.voiceover(
            "Hermeneutics began as the art of interpreting texts: the Bible, the law, the classics. "
            "<bookmark mark='a'/>Friedrich Schleiermacher, in lectures in the early nineteenth century, made it "
            "general, and noticed a circle: each sentence of a work is understood through the whole, and the whole "
            "only through its sentences. <bookmark mark='b'/>Wilhelm Dilthey made it the method of the human "
            "sciences. The natural sciences explain; history and the study of culture understand, from the inside. "
            "<bookmark mark='c'/>Heidegger made it ontology. Understanding is not a method we sometimes apply, but "
            "our way of being: we never come to anything without a fore-structure of expectations."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def gadamer(self):
        hc = history_card(1960, r"Hans-Georg Gadamer", r"\textit{Truth and Method}", width=5.0, color=HIST).to_corner(
            UL, buff=0.3)
        spiral = VMobject(color=SIGN, stroke_width=3)
        pts = [np.array([4.4 + 0.1 * t * math.cos(1.3 * t), 1.5 + 0.1 * t * math.sin(1.3 * t), 0])
               for t in np.linspace(14, 0.5, 200)]
        spiral.set_points_smoothly(pts)
        part = label(r"part", font_size=20, color=ACT).move_to([2.6, 2.6, 0])
        whole = label(r"whole", font_size=20, color=WORLD).move_to([6.3, 0.4, 0])
        rows = [
            (r"prejudice", r"\textit{Vorurteil}, \ pre-judgement: \ not an obstacle but a condition of "
                           r"understanding", BAD),
            (r"tradition", r"we understand from within a history that has shaped us: \ effective history", TIME),
            (r"fusion of horizons", r"understanding is not escaping our horizon, \ but widening it to meet the "
                                    r"text's", OK),
        ]
        g = rows_table(rows, top=-0.6, gap=0.42, width=7.2)
        with self.voiceover(
            "Hans-Georg Gadamer, a student of Heidegger, published Truth and Method in 1960. "
            "<bookmark mark='a'/>The circle is not vicious; it spirals. We start with a guess about the whole, read "
            "the parts in its light, revise the guess, and read again. <bookmark mark='b'/>Gadamer's most "
            "provocative move was to rehabilitate prejudice, in its literal sense of pre-judgement. The "
            "Enlightenment taught us to put prejudices aside; but we cannot, and without them we could not begin to "
            "understand at all. <bookmark mark='c'/>We understand from within a tradition that has shaped us, what "
            "he called effective history. <bookmark mark='d'/>And understanding is a fusion of horizons: not "
            "escaping our own point of view, but widening it until it meets the text's."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Create(spiral), FadeIn(part), FadeIn(whole), run_time=3)
            for mk, r in zip("bcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def toy(self):
        d = load("circle")
        head = label(r"The circle as an iteration \ (an analogy)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        T = d["texts"]
        assert d["iters"] == 12
        bt = {r["prejudice"]: r for r in T["the boatman's text"]["runs"]}
        am = {r["prejudice"]: r for r in T["a text that cannot answer back"]["runs"]}
        mx = {r["prejudice"]: r for r in T["a mixed text"]["runs"]}
        assert bt[0.1]["final"] == 0.9989 and bt[0.9]["final"] == 0.9999 and bt[0.1]["trajectory"][1] == 0.4857
        assert am[0.1]["final"] == 0.1 and am[0.9]["final"] == 0.9
        assert mx[0.1]["final"] == 0.4991 and mx[0.9]["final"] == 0.5009
        words = VGroup(*[label(w, font_size=19, color=WORLD if w in ("fish", "boat", "reeds") else SIGN)
                         for w in T["the boatman's text"]["words"]]).arrange(RIGHT, buff=0.3).move_to([0, 2.1, 0])
        wl = label(r"bank, \ current, \ deposit, \ branch: \ river or money? \quad fish, \ boat, \ reeds: \ river",
                   font_size=17, color=GREY_A).next_to(words, DOWN, buff=0.15)
        ax = Axes(x_range=[0, 12, 2], y_range=[0, 1, 0.25], x_length=6.4, y_length=3.0, tips=False,
                  axis_config={"color": GREY_B, "font_size": 16},
                  y_axis_config={"include_numbers": True, "decimal_number_config": {"num_decimal_places": 2}}
                  ).move_to([-2.4, -1.3, 0])
        xs = VGroup(*[MathTex(str(k), font_size=16, color=GREY_A).next_to(ax.c2p(k, 0), DOWN, buff=0.1)
                      for k in range(0, 13, 2)])
        xl = label(r"rounds of part and whole", font_size=16, color=GREY_A).next_to(xs, DOWN, buff=0.08)
        yl = label(r"P(the text is about the river)", font_size=16, color=GREY_A).next_to(ax.y_axis, UP, buff=0.1)
        curves = {}
        for name, col in TEXT_COL.items():
            for r in T[name]["runs"]:
                pts = [ax.c2p(k, v) for k, v in enumerate(r["trajectory"])]
                curves[(name, r["prejudice"])] = VMobject(color=col, stroke_width=3).set_points_as_corners(pts)
        side = stack([(r"the boatman's text: \ from either prejudice, \ to the river", WORLD),
                      (r"all four ambiguous words: \ the prejudice stays exactly as it was", GREY_A),
                      (r"one river word, \ one money word: \ both readers meet at a half", SIGN)], font_size=19,
                     aligned_edge=LEFT, width=4.6, buff=0.28).move_to([4.6, -1.2, 0])
        with self.voiceover(
            "The Reasoner can play out the shape of the circle, as an analogy, not as Gadamer's theory. "
            "<bookmark mark='a'/>Here is a short text. Some of its words are ambiguous: bank, current, deposit and "
            "branch could belong to a story about a river or about money. Others, fish, boat, reeds, belong only to "
            "the river. <bookmark mark='b'/>The reader starts with a prejudice about the whole, say only one chance "
            "in ten that it is about the river. Reading each word in the light of that, and re-estimating the "
            "whole from the readings, the guess climbs to about a half after one round, and to the river within a "
            "few more. Start with the opposite prejudice, and it arrives at the same place. "
            "<bookmark mark='c'/>Now a text of only the four ambiguous words. It cannot answer back, and the "
            "prejudice stays exactly where it began: one in ten, or nine in ten. <bookmark mark='d'/>And a mixed "
            "text, with one river word and one money word, brings both readers to the same point: a half. "
            "<bookmark mark='e'/>That is the lesson Gadamer drew. Prejudice is where understanding starts, and a "
            "text that can speak back corrects it. A text that cannot simply returns it to us."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(words), FadeIn(wl))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(xs), FadeIn(xl), FadeIn(yl))
            self.play(Create(curves[("the boatman's text", 0.1)]), run_time=1.5)
            self.play(Create(curves[("the boatman's text", 0.9)]), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("c")
            self.play(Create(curves[("a text that cannot answer back", 0.1)]),
                      Create(curves[("a text that cannot answer back", 0.9)]), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(Create(curves[("a mixed text", 0.1)]), Create(curves[("a mixed text", 0.9)]), FadeIn(side[2]))
            vo.wait_until("e")
            self.wait(0.5)
        self.clear_scene()

    def debates(self):
        head = label(r"Arguments about interpretation", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Habermas \ (1967--71)", r"tradition can be distorted by power: \ interpretation needs a critique of "
                                       r"ideology", SIGN),
            (r"Ricoeur \ (1965)", r"a hermeneutics of suspicion: \ Marx, \ Nietzsche and Freud read meaning as "
                                  r"disguise", BAD),
            (r"Hirsch \ (1967)", r"a text means what its author meant; \ Gadamer: \ its meaning always goes beyond its "
                                  r"author", ACT),
        ]
        g = rows_table(rows, top=1.6, gap=0.55)
        with self.voiceover(
            "Gadamer's view drew strong replies. <bookmark mark='a'/>Jürgen Habermas, in a debate that ran from 1967 "
            "to 1971, objected that tradition is not innocent: it can be distorted by power, so interpretation "
            "needs a critique of ideology, not only a fusion of horizons. <bookmark mark='b'/>Paul Ricoeur named a "
            "hermeneutics of suspicion, practised by Marx, Nietzsche and Freud, which reads meaning as a disguise "
            "for something else: class interest, the will to power, desire. <bookmark mark='c'/>And E. D. Hirsch, in "
            "1967, defended the author: a text means what its author meant. Gadamer held that its meaning always "
            "goes beyond its author."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
