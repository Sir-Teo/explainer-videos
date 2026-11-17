from __future__ import annotations

from videos.psychology.psych27.common import *  # noqa: F403


def node(text, col, pos, w=2.2, h=0.8):
    box = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=col, stroke_width=2,
                           fill_color=BLACK, fill_opacity=0.6).move_to(pos)
    return VGroup(box, label(text, font_size=20, color=col).move_to(box))


class Blindsight(VoiceoverScene):
    def construct(self):
        self.card()
        self.tests()
        self.routes()
        self.doubts()

    def card(self):
        card = chapter_card(3, r"Blindsight", r"Is it really blind?",
                            lit={1974: r"Weiskrantz et al.", 1983: r"Campion et al.", 1995: r"Cowey \& Stoerig",
                                 2007: r"Persaud et al.", 2010: r"Schmid et al."},
                            part=PART, scale=("mind", "brain"), marr=("what", "how"))
        with self.voiceover("Chapter three. Blindsight."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def tests(self):
        head = heading(r"Guessing in the blind field")
        field = VGroup(Circle(radius=1.8, color=GREY_C, stroke_width=2),
                       AnnularSector(inner_radius=0, outer_radius=1.8, angle=PI, start_angle=PI / 2, color=LOST,
                                     fill_opacity=0.25, stroke_width=0)).move_to([-3.6, 0.3, 0])
        fix = Cross(scale_factor=0.07, stroke_color=WHITE, stroke_width=3).move_to(field.get_center())
        blind = label(r"blind half", font_size=20, color=LOST).next_to(field, DOWN, buff=0.2).shift(LEFT * 0.9)
        seeing = label(r"seeing half", font_size=20, color=SEEN).next_to(field, DOWN, buff=0.2).shift(RIGHT * 0.9)
        target = Dot(field.get_center() + np.array([-1.0, 0.6, 0]), radius=0.1, color=WHITE)
        bar = Line(ORIGIN, UP * 0.7, color=WHITE, stroke_width=6).move_to(field.get_center() + np.array([-1.0, -0.6, 0]))
        rows = rows_of([
            (r"where was the light? \ point to it: \ accurate, \ though he saw nothing", UNSEEN),
            (r"vertical or horizontal? \ an X or an O? \ far above chance", UNSEEN),
            (r"moving or still? \ in some patients, \ like G.\,Y., \ a feeling that something moved, \ but no "
             r"visual experience of it", HOT),
            (r"D.\,B., \ shown his scores: \ ``did I get that right?''", WHITE),
        ], 5.8, 22, 0.32).move_to([3.4, 0.1, 0])
        tag = historical_tag(r"Weiskrantz, \ Warrington, \ Sanders \& Marshall (1974); \ Weiskrantz (1986)")
        with self.voiceover(
            "Here's what the tests with D.B. looked like. <bookmark mark='a'/> He fixates the centre. A light "
            "appears somewhere in his blind half, and he is asked to point to where it was. He protests that he saw "
            "nothing, then points, and is accurate. <bookmark mark='b'/> Asked whether a line there is vertical or "
            "horizontal, or whether a shape is an X or an O, he guesses far above chance. <bookmark mark='c'/> Some "
            "later patients, like G.Y., report a feeling that something has moved, but no visual experience of it. "
            "<bookmark mark='d'/> And when D.B. was shown his scores, he asked whether he'd really got them right."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(field), FadeIn(fix), FadeIn(blind), FadeIn(seeing))
            vo.wait_until("a")
            self.play(FadeIn(target, scale=2), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeOut(target), FadeIn(bar), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def routes(self):
        head = heading(r"How information bypasses V1")
        retina = node(r"retina", WHITE, [-5.2, 0.4, 0], w=1.6)
        lgn = node(r"LGN", SEEN, [-2.6, 1.6, 0], w=1.6)
        v1 = node(r"V1 \ (damaged)", LOST, [0.2, 1.6, 0], w=2.4)
        sc = node(r"superior colliculus", UNSEEN, [-2.6, -0.9, 0], w=2.8)
        pulv = node(r"pulvinar", UNSEEN, [0.2, -0.9, 0], w=1.8)
        mt = node(r"MT \ (motion)", SEEN, [3.4, 0.4, 0], w=2.2)
        ar = lambda a, b, c, dash=False: (DashedLine if dash else Line)(a.get_right(), b.get_left(), color=c,  # noqa: E731
                                                                         stroke_width=3).add_tip(tip_length=0.15)
        e1 = ar(retina, lgn, SEEN)
        e2 = ar(lgn, v1, SEEN)
        e3 = ar(v1, mt, LOST, True)
        e4 = ar(retina, sc, UNSEEN)
        e5 = ar(sc, pulv, UNSEEN)
        e6 = ar(pulv, mt, UNSEEN)
        e7 = CurvedArrow(lgn.get_top() + RIGHT * 0.3, mt.get_top() + LEFT * 0.3, angle=-PI / 3, color=GNW,
                         stroke_width=3, tip_length=0.15)
        lab7 = label(r"LGN to MT, \ directly", font_size=18, color=GNW).next_to(e7, UP, buff=0.05)
        rows = rows_of([
            (r"the main route, \ through V1, \ is cut", LOST),
            (r"older routes, \ through the superior colliculus and pulvinar, \ reach motion areas like MT", UNSEEN),
            (r"Schmid and colleagues, \ 2010, \ in monkeys with V1 lesions: \ silence the LGN and blindsight goes", GNW),
        ], 12.0, 23, 0.25).to_edge(DOWN, buff=0.65)
        tag = published_tag(r"Cowey \& Stoerig (1995); \ Schmid et al.\ (2010)")
        with self.voiceover(
            "How can information get through? <bookmark mark='a'/> The main route from the eye runs through the "
            "lateral geniculate nucleus to V1, the primary visual cortex, and that's what was damaged. "
            "<bookmark mark='b'/> But there are older routes: from the eye to the superior colliculus in the "
            "midbrain, then through the pulvinar to visual areas like MT, which handles motion. "
            "<bookmark mark='c'/> And some cells of the geniculate project straight to MT. In 2010 Michael Schmid "
            "and colleagues showed, in monkeys with V1 lesions, that silencing the geniculate abolishes blindsight. "
            "Alan Cowey and Petra Stoerig had shown in 1995 that such monkeys also have blindsight: they locate "
            "targets they will otherwise classify as blank."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(retina), FadeIn(mt))
            vo.wait_until("a")
            self.play(FadeIn(lgn), Create(e1), FadeIn(v1), Create(e2), Create(e3), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(sc), Create(e4), FadeIn(pulv), Create(e5), Create(e6), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(e7), FadeIn(lab7), FadeIn(rows[2]))
        self.clear_scene()

    def doubts(self):
        head = heading(r"Is blindsight really unconscious?")
        rows = rows_of([
            (r"Campion, \ Latto and Smith, \ 1983: \ could light scattered into the seeing field explain it? \ "
             r"controls with the natural blind spot, \ and the monkey studies, \ say not all of it", WHITE),
            (r"Overgaard and colleagues, \ 2008: \ with a graded awareness scale, \ a blindsight patient reported "
             r"faint glimpses on trials a yes or no had called unseen", HOT),
            (r"Persaud, \ McLeod and Cowey, \ 2007: \ G.\,Y. would not bet on his correct blind-field answers; \ his "
             r"wagers did not track his accuracy", UNSEEN),
            (r"so: \ the effect replicates, \ in patients and in monkeys; \ whether it is degraded conscious vision is "
             r"still argued, \ and the criterion problem of chapter two is why", GNW),
        ], 12.2, 24, 0.38).move_to([0, -0.2, 0])
        tag = published_tag(r"Campion, \ Latto \& Smith (1983); \ Overgaard et al.\ (2008); \ Persaud, \ McLeod \& "
                            r"Cowey (2007)")
        with self.voiceover(
            "Is blindsight really unconscious? There have been three kinds of doubt. <bookmark mark='a'/> In 1983 "
            "John Campion, Richard Latto and Yvonne Smith asked whether light scattered into the seeing half of the "
            "field could explain it. Controls using the eye's natural blind spot, and the monkey studies, suggest "
            "scatter can't explain all of it. <bookmark mark='b'/> In 2008 Morten Overgaard and colleagues gave a "
            "blindsight patient the graded awareness scale, and the patient reported faint glimpses on trials that a yes or "
            "no would have counted as unseen: degraded vision, perhaps, rather than none. <bookmark mark='c'/> On "
            "the other side, in 2007 Navindra Persaud, Peter McLeod and Cowey had G.Y. bet on his answers. In his "
            "blind field he wouldn't bet on his correct answers; his wagers didn't track his accuracy, which is "
            "what you'd expect with no awareness at all. <bookmark mark='d'/> So the effect replicates, in "
            "patients and in monkeys. Whether it's a weak form of conscious vision is still argued, and the "
            "criterion problem of the last chapter is the reason it's so hard to settle."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
