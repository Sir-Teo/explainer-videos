from __future__ import annotations

from videos.philosophy.philosophy24.common import *  # noqa: F403


class Universals(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Laws that govern", r"Is a law a necessity between properties?",
                            lit=(1977, 2007), part=PART)
        with self.voiceover("Chapter three. Laws that govern."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.relation()
        self.virtues()
        self.inference()
        self.powers()
        self.scorecard()

    def relation(self):
        hc = history_card(1983, r"David Armstrong", r"\textit{What Is a Law of Nature?}", width=5.8,
                          color=HIST).to_corner(UL, buff=0.3)
        F = Circle(radius=0.75, color=LAW, fill_color=LAW, fill_opacity=0.15).move_to([-2.4, 0.9, 0])
        G = Circle(radius=0.75, color=CHANCE, fill_color=CHANCE, fill_opacity=0.15).move_to([2.4, 0.9, 0])
        Fl = MathTex(r"F", font_size=40, color=LAW).move_to(F)
        Gl = MathTex(r"G", font_size=40, color=CHANCE).move_to(G)
        N = Arrow(F.get_right(), G.get_left(), buff=0.1, color=GOAL, stroke_width=5)
        Nl = MathTex(r"N", font_size=36, color=GOAL).next_to(N, UP, buff=0.1)
        parts = VGroup(*[Dot([x, -1.2, 0], radius=0.1, color=WHITE) for x in (-3.0, -1.5, 0.0, 1.5, 3.0)])
        pl = VGroup(*[MathTex(n, font_size=24).next_to(p, DOWN, buff=0.12) for n, p in zip("abcde", parts)])
        linesF = VGroup(*[Line(p.get_center(), F.get_bottom(), color=LAW, stroke_width=1.5, stroke_opacity=0.6)
                          for p in parts])
        linesG = VGroup(*[Line(p.get_center(), G.get_bottom(), color=CHANCE, stroke_width=1.5, stroke_opacity=0.6)
                          for p in parts])
        f = MathTex(r"N(F, G) \;\Rightarrow\; \forall x\,(Fx \to Gx)", r"\qquad", r"\text{but not conversely}",
                    font_size=32).to_edge(DOWN, buff=0.5)
        f[2].set_color(GREY_A)
        with self.voiceover(
            "In 1977 Fred Dretske and Michael Tooley, and in 1983 David Armstrong, gave a rival answer: laws are "
            "relations between properties. <bookmark mark='a'/>Take two universals, F and G: being a sphere of "
            "uranium-235 above critical mass, say, and exploding. <bookmark mark='b'/>A law is a second-order "
            "relation between them, which Armstrong called necessitation, and wrote N of F and G. "
            "<bookmark mark='c'/>The particulars come below: each thing that has F <bookmark mark='d'/>also has G, "
            "because the universals stand in N. <bookmark mark='e'/>So the law entails the regularity: if F "
            "necessitates G, everything that is F is G. But the regularity does not entail the law. That gap is "
            "the difference between a law and an accident."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(GrowFromCenter(F), GrowFromCenter(G), FadeIn(Fl), FadeIn(Gl))
            vo.wait_until("b")
            self.play(GrowArrow(N), FadeIn(Nl))
            vo.wait_until("c")
            self.play(FadeIn(parts), FadeIn(pl), Create(linesF))
            vo.wait_until("d")
            self.play(Create(linesG))
            vo.wait_until("e")
            self.play(Write(f))
        self.clear_scene()

    def virtues(self):
        head = label(r"What the relation buys", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"laws and accidents", r"uranium spheres: \ $N$ holds; \ gold spheres: \ nothing holds, \ the pattern is "
                                    r"luck", OK),
            (r"counterfactuals", r"if this were a big uranium sphere, \ $N$ would still hold, \ so it would explode",
             LAW),
            (r"explanation", r"the regularity holds \textit{because} the universals are related: \ no circle", CHANCE),
            (r"induction", r"Armstrong: \ $N(F,G)$ is the best explanation of the observed pattern, \ so inference "
                           r"to it is rational \ (Part 15)", ABS),
        ]
        g = rows_table(rows, top=1.7, gap=0.5, width=9.0, x_text=-3.0, label_size=22, text_size=21)
        with self.voiceover(
            "The relation buys a great deal. <bookmark mark='a'/>It separates laws from accidents: N holds between "
            "the uranium properties, and nothing holds between gold and smallness; that pattern is luck. "
            "<bookmark mark='b'/>It supports counterfactuals: had there been a large uranium sphere, N would still "
            "have held, so the sphere would have exploded. <bookmark mark='c'/>It explains: the regularity holds "
            "because the universals are related, and there is no circle, since the relation is something over and "
            "above the pattern. <bookmark mark='d'/>And Armstrong thought it solved Hume's problem of induction, "
            "the subject of Part 15: the law is the best explanation of the observed pattern, so inferring it is "
            "rational, and the law then covers the unobserved cases too."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def inference(self):
        q = quote_card(r"It can't enter into them just by bearing a name, \ any more than one can have mighty biceps "
                       r"just by being called `Armstrong'.", r"David Lewis",
                       r"`New Work for a Theory of Universals' \ (1983)", width=10.0, font_size=26).to_edge(UP,
                                                                                                    buff=0.5)
        rows = stack([(r"the inference problem: \ why does $N(F,G)$ and $Fa$ \textit{entail} $Ga$?", BAD),
                      (r"the identification problem: \ which relation is $N$, \ and what makes it the law-making one?",
                       BAD),
                      (r"van Fraassen \ (1989): \ the two problems cannot both be solved", ABS),
                      (r"Armstrong's reply: \ $N$ is a universal whose instances are causings, \ seen in our own "
                       r"agency", HIST)], font_size=22, aligned_edge=LEFT, width=11.6, buff=0.32).move_to(
            [0, -0.6, 0])
        with self.voiceover(
            "The trouble is in the word. <bookmark mark='a'/>Armstrong called the relation necessitation, and of "
            "course if F necessitates G and a is F, a must be G. But David Lewis pointed out that the relation does "
            "not get its power from its name: it cannot enter into necessary connections just by bearing a name, he "
            "wrote, any more than one can have mighty biceps just by being called Armstrong. "
            "<bookmark mark='b'/>This is the inference problem. What is it about the relation N that makes N of F "
            "and G, together with a being F, entail that a is G? <bookmark mark='c'/>And the identification problem: "
            "which relation is N? <bookmark mark='d'/>Bas van Fraassen argued that any answer to one leaves the "
            "other unsolved. <bookmark mark='e'/>Armstrong's late answer was that N is the relation whose instances "
            "are causings, and that we meet causing directly, when we push and pull things ourselves."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            for mk, r in zip("bcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def powers(self):
        head = label(r"Powers, \ and primitive laws", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"dispositional essentialism", r"Bird \ (2007): \ properties are powers; \ to be charged \textit{is} to "
                                            r"repel like charges. \ Laws flow from essences, \ and are necessary", ENT),
            (r"its price", r"spatial and geometric properties seem not to be powers; \ and symmetries and conservation "
                           r"laws are not about any one property", BAD),
            (r"primitivism", r"Maudlin \ (2007): \ laws are basic, \ not analyzed; \ they produce later states "
                             r"from earlier ones", TIME),
            (r"its price", r"nothing more can be said about what a law is", BAD),
        ]
        g = rows_table(rows, top=1.7, gap=0.5, width=8.6, x_text=-2.4, label_size=22, text_size=21)
        with self.voiceover(
            "Two more answers. <bookmark mark='a'/>Dispositional essentialism, defended by Alexander Bird: "
            "properties are powers. To be negatively charged is to be disposed to repel other negative charges; that "
            "is the whole nature of the property. Then the laws flow from the essences of properties, and they are "
            "necessary: there is no world where charge behaves otherwise, because it would not be charge. "
            "<bookmark mark='b'/>The price: some properties, like shape and distance, do not look like powers, and "
            "the deepest laws, symmetries and conservation laws, are not about any one property. "
            "<bookmark mark='c'/>Primitivism, defended by Tim Maudlin: the laws are basic. They are not summaries "
            "and not relations between universals; they are what produces each state of the world from the one "
            "before. <bookmark mark='d'/>Its price is honesty: nothing more can be said about what a law is."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def scorecard(self):
        head = label(r"Four views of law", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        T = lambda s, c=WHITE: label(s, font_size=19, color=c)  # noqa: E731
        hd = [T(r"view", CONN), T(r"laws are", CONN), T(r"govern?", CONN), T(r"necessary?", CONN),
              T(r"the hard question", CONN)]
        rows = [[T(r"Lewis", LAW), T(r"the best summary"), mark(False), mark(False), T(r"natural properties; explanation")],
                [T(r"Armstrong", CHANCE), T(r"relations of universals"), mark(True), mark(False), T(r"the inference problem")],
                [T(r"Bird", ENT), T(r"essences of powers"), mark(True), mark(True), T(r"spatial properties; symmetries")],
                [T(r"Maudlin", TIME), T(r"primitive"), mark(True), mark(False), T(r"what more is there to say?")]]
        grid = ValueGrid(hd, rows, col_w=[1.8, 3.2, 1.4, 1.7, 4.4], cell_h=0.6, font_size=20).move_to([0, 0.3, 0])
        foot = label(r"the arrow of time will test them: \ the world runs one way, \ the laws run both",
                     font_size=21, color=GOAL).next_to(grid, DOWN, buff=0.9)
        with self.voiceover(
            "So there are four views. <bookmark mark='a'/>For Lewis the laws are the best summary of the mosaic: "
            "they do not govern, and they are contingent. <bookmark mark='b'/>For Armstrong they are relations "
            "between universals that govern, though they hold contingently. <bookmark mark='c'/>For Bird they are "
            "essences of powers, and necessary. <bookmark mark='d'/>For Maudlin they are primitive, and govern "
            "the passage from one moment to the next. <bookmark mark='e'/>Each has a hard question. Keep the "
            "scorecard: the arrow of time will put the views to the test, because the arrow is a pattern that the "
            "laws themselves seem not to contain."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            for mk, r in zip("abcd", range(4)):
                vo.wait_until(mk)
                self.play(*[FadeIn(c) for c in grid.cell[r]])
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
