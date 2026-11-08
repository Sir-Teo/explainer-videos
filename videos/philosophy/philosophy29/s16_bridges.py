from __future__ import annotations

from videos.philosophy.philosophy29.common import *  # noqa: F403


class Bridges(VoiceoverScene):
    def construct(self):
        card = chapter_card(15, r"Across the divide", r"Are analytic and continental philosophy one subject?",
                            lit=(1929, 1996), part=PART)
        with self.voiceover("Chapter fifteen. Across the divide."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.divide()
        self.carnap()
        self.bridges()

    def divide(self):
        hc = history_card(1929, r"Davos", r"Cassirer and Heidegger debate Kant", width=5.6, color=HIST).to_corner(
            UL, buff=0.3)
        river = VMobject(color=ACT, stroke_width=10, stroke_opacity=0.5)
        river.set_points_smoothly([np.array([x, 0.4 * math.sin(1.3 * x) - 0.6, 0]) for x in np.linspace(-6.5, 6.5, 40)])
        left = VGroup(*[label(t, font_size=19, color=SIGN) for t in
                        [r"Frege, \ Russell, \ Carnap", r"logic and science", r"clarity, \ argument"]]).arrange(
            DOWN, buff=0.25).move_to([-3.6, 1.2, 0])
        right = VGroup(*[label(t, font_size=19, color=BODY) for t in
                         [r"Husserl, \ Heidegger, \ Sartre", r"history and experience", r"depth, \ interpretation"]]
                       ).arrange(DOWN, buff=0.25).move_to([3.6, -2.2, 0])
        rows = stack([(r"1929: \ Ernst Cassirer against Heidegger on Kant, \ with Carnap in the audience", HIST),
                      (r"a divide of style, \ canon and institutions, \ more than of doctrine", GOAL)], font_size=20,
                     aligned_edge=LEFT, width=12.0, buff=0.2).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "This part has been, mostly, about what is called continental philosophy, and the rest of the series is "
            "mostly analytic. <bookmark mark='a'/>On one bank, Frege, Russell and Carnap: logic and science, "
            "clarity and argument. <bookmark mark='b'/>On the other, Husserl, Heidegger and Sartre: history and "
            "lived experience, depth and interpretation. <bookmark mark='c'/>The divide is often dated to 1929, at "
            "Davos in Switzerland, where Ernst Cassirer and Heidegger debated how to read Kant, with the young "
            "Rudolf Carnap in the audience. <bookmark mark='d'/>It is a divide of style, canon and institutions more "
            "than of doctrine: both grew from the same soil, Kant, Brentano, and the crisis in the foundations of "
            "logic and mathematics around 1900."
        ) as vo:
            self.play(FadeIn(hc), Create(river))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def carnap(self):
        head = label(r"`The nothing itself nothings'", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        a = VGroup(label(r"Heidegger \ (1929), \ `What Is Metaphysics?'", font_size=20, color=BODY),
                   label(r"`Das Nichts selbst nichtet'", font_size=26, color=BODY)).arrange(DOWN, buff=0.15).move_to(
            [-3.4, 1.0, 0])
        b = VGroup(label(r"Carnap \ (1932)", font_size=20, color=SIGN),
                   label(r"a pseudo-sentence: \ `nothing' used as a name", font_size=22, color=SIGN)).arrange(
            DOWN, buff=0.15).move_to([3.4, 1.0, 0])
        f1 = MathTex(r"\neg \exists x\, \text{Outside}(x)", font_size=32, color=OK)
        f2 = MathTex(r"\text{Nothing nothings} \;\leadsto\; ?", font_size=32, color=BAD)
        fs = VGroup(VGroup(label(r"`there is nothing outside' becomes", font_size=19, color=GREY_A), f1).arrange(
            DOWN, buff=0.12), VGroup(label(r"but `the nothing nothings' has no logical form", font_size=19,
                                           color=GREY_A), f2).arrange(DOWN, buff=0.12)).arrange(RIGHT, buff=1.0
                                                                                               ).move_to([0, -1.2, 0])
        foot = label(r"for Carnap, \ metaphysicians are `musicians without musical ability'", font_size=20,
                     color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The sharpest exchange came soon after. <bookmark mark='a'/>In his inaugural lecture of 1929, What Is "
            "Metaphysics?, Heidegger wrote of anxiety revealing the nothing, and said: the nothing itself nothings. "
            "<bookmark mark='b'/>In 1932 Carnap made the sentence his prime example of a pseudo-sentence. "
            "<bookmark mark='c'/>There is nothing outside has a perfectly good logical form: it is not the case "
            "that something is outside. Heidegger, Carnap argued, had treated nothing as a name for something, and "
            "then given that something an activity. The sentence has no logical form at all, and so no meaning. "
            "<bookmark mark='d'/>Metaphysics, Carnap concluded, expresses an attitude toward life, and "
            "metaphysicians are musicians without musical ability."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a))
            vo.wait_until("b")
            self.play(FadeIn(b))
            vo.wait_until("c")
            self.play(FadeIn(fs))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def bridges(self):
        head = label(r"Bridges", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Dreyfus--McDowell", r"\ (2005--07): \ is skilled coping conceptual all the way down? \ McDowell: "
                                   r"yes; \ Dreyfus: no", ACT),
            (r"naturalizing", r"\textit{Naturalizing Phenomenology} \ (Petitot, \ Varela et al., \ 1999): \ "
                              r"Husserl's descriptions as data for cognitive science", WORLD),
            (r"neurophenomenology", r"Varela \ (1996): \ trained first-person reports, \ correlated with brain "
                                    r"measurements", BODY),
            (r"heterophenomenology", r"Dennett \ (1991): \ take reports as data about what seems, \ not as "
                                     r"infallible", SIGN),
            (r"design", r"Winograd and Flores \ (1986): \ Heidegger's breakdowns as a theory of computer "
                        r"interfaces", OBJ),
            (r"prediction", r"protention as prediction: \ predictive-processing theories of the brain", TIME),
        ]
        g = rows_table(rows, top=1.7, gap=0.38)
        with self.voiceover(
            "Bridges have been built from both banks. <bookmark mark='a'/>In a debate from 2005 to 2007, John "
            "McDowell, an analytic philosopher, and Hubert Dreyfus argued over whether skilled coping is conceptual "
            "all the way down: McDowell said yes, Dreyfus no. <bookmark mark='b'/>A volume of 1999, Naturalizing "
            "Phenomenology, edited by Jean Petitot, Francisco Varela and others, proposed treating Husserl's "
            "descriptions as data for cognitive science. <bookmark mark='c'/>Varela's neurophenomenology trained "
            "subjects to give careful first-person reports, and correlated them with measurements of the brain. "
            "<bookmark mark='d'/>Daniel Dennett's heterophenomenology takes the same reports as data about how "
            "things seem, without treating them as infallible. <bookmark mark='e'/>In 1986 Terry Winograd and "
            "Fernando Flores used Heidegger's breakdowns as a theory of how people use computers, a book that "
            "shaped interface design. <bookmark mark='f'/>And theories of the brain as a prediction machine have "
            "given Husserl's protention a second life. The next part asks the question all of this leads to: what is a "
            "mind, and could a machine have one?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
