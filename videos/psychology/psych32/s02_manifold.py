from __future__ import annotations

from videos.psychology.psych32.common import *  # noqa: F403

HS_NAMES = [r"visual perception", r"cubes", r"lozenges", r"paragraphs", r"sentences", r"word meaning",
            r"speeded addition", r"counting dots", r"straight/curved"]


class Manifold(VoiceoverScene):
    def construct(self):
        self.card()
        self.spearman()
        self.hierarchy()
        self.holzinger()

    def card(self):
        card = chapter_card(1, r"The positive manifold", r"Do abilities go together?",
                            lit={1904: r"Spearman", 1939: r"Holzinger \& Swineford"}, part=PART,
                            scale=("person", "group"), marr=("what",))
        with self.voiceover("Chapter one. The positive manifold."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def spearman(self):
        d = load("spearman")
        head = heading(r"Spearman's table, \ 1904")
        hm = heatmap(d["R"], names=d["names"], cell=0.75, font_size=18)
        hm.move_to([-2.6, -0.4, 0])
        tops = VGroup(*[label(nm[:4] + ".", font_size=17, color=GREY_A).next_to(hm.cells[0][j], UP, buff=0.12)
                        for j, nm in enumerate(d["names"])])
        rows = rows_of([
            (r"boys at a preparatory school: \ examination marks in four subjects, \ a test of telling two tones "
             r"apart, \ and musical talent", WHITE),
            (r"every correlation is positive: \ the boy good at Classics tends to be good at Mathematics, \ and at "
             r"pitch", G),
            (r"Spearman called this a ``Universal Unity of the Intellective Function''", GREY_A),
            (r"today it is the \emph{positive manifold}: \ among the most replicated findings in psychology", GOOD),
        ], 5.2, 22, 0.36).move_to([3.9, -0.3, 0])
        tag = historical_tag(r"Spearman (1904)")
        with self.voiceover(
            "Here is Spearman's table. <bookmark mark='a'/> The boys of a preparatory school, with their examination "
            "marks in four subjects, a test of how finely they could tell two tones apart, and a rating of musical "
            "talent. <bookmark mark='b'/> Every correlation is positive. The boy who is good at Classics tends to be "
            "good at Mathematics, and at pitch. <bookmark mark='c'/> Spearman called it a universal unity of the "
            "intellective function. <bookmark mark='d'/> Today it's called the positive manifold, and it's among "
            "the most replicated findings in all of psychology."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in hm[0]], lag_ratio=0.02), FadeIn(hm[1]), FadeIn(tops),
                      FadeIn(rows[0]), run_time=2.5)
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def hierarchy(self):
        d = load("spearman")
        head = heading(r"A hierarchy")
        hm = heatmap(d["R"], names=d["names"], cell=0.75, font_size=18).move_to([-3.0, -0.4, 0])
        avg = [0.77, 0.72, 0.70, 0.67]
        bars_ = VGroup()
        for i, a in enumerate(avg):
            b = Rectangle(width=1.6 * a, height=0.38, stroke_width=0, fill_color=G, fill_opacity=0.8)
            b.next_to(hm.cells[i][5], RIGHT, buff=0.35).align_to(hm.cells[i][5].get_right() + RIGHT * 0.35, LEFT)
            bars_.add(VGroup(b, label(f"{a:.2f}", font_size=17, color=G).next_to(b, RIGHT, buff=0.08)))
        rows = rows_of([
            (r"order the subjects by their average correlation: \ Classics .77, \ French .72, \ English .70, \ "
             r"Mathematics .67", G),
            (r"then every row falls from left to right, \ and every column from top to bottom: \ pitch and music "
             r"follow the same order", WHITE),
            (r"that is what one common cause would produce: \ each test's correlations are proportional to how "
             r"much of the common factor it carries", MODEL),
        ], 4.2, 21, 0.36).move_to([4.6, -1.2, 0])
        tag = historical_tag(r"Spearman (1904)")
        with self.voiceover(
            "Spearman saw more than positivity. <bookmark mark='a'/> Order the subjects by their average "
            "correlation with the others: Classics 0.77, French 0.72, English 0.70, Mathematics 0.67. "
            "<bookmark mark='b'/> Then every row falls from left to right, and every column from top to bottom, and "
            "pitch and music follow the same order. He called it a hierarchy. <bookmark mark='c'/> That pattern is "
            "what one common cause would produce: each test's correlations would be proportional to how much of the "
            "common factor it carries. The next chapter makes that exact."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(hm))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in bars_], lag_ratio=0.3), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), *[Indicate(hm.cells[i][4], color=WHITE) for i in range(4)])
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def holzinger(self):
        d = load("holzinger")
        head = heading(r"A real battery: \ 301 children, \ nine tests")
        hm = heatmap(d["R"], names=HS_NAMES, cell=0.56, font_size=14).move_to([-2.0, -0.5, 0])
        groups = VGroup(*[SurroundingRectangle(VGroup(hm.cells[i0][i0], hm.cells[i0 + 2][i0 + 2]), color=c,
                                               buff=0.02, stroke_width=3)
                          for i0, c in ((0, VIS), (3, VERB), (6, SPEED))])
        rows = rows_of([
            (r"Karl Holzinger and Frances Swineford, \ 1939: \ seventh- and eighth-graders at two "
             r"schools, \ Pasteur and Grant-White; \ the nine-test set analysed ever since", WHITE),
            (rf"35 of the 36 correlations are positive, \ mean {d['mean_r']:.2f}; \ one is slightly negative, \ "
             rf"{d['min_r']:.2f}", G),
            (r"and blocks stand out: \ visual tests with visual, \ verbal with verbal, \ speeded with speeded", VERB),
            (r"a general factor and something more: \ the question of chapter three", YOU),
        ], 4.9, 21, 0.36).move_to([4.3, -0.3, 0])
        tag = published_tag(r"data: Holzinger \& Swineford (1939), \ recomputed")
        with self.voiceover(
            "Spearman's table is a hundred and twenty years old. Here is a battery you can recompute yourself. "
            "<bookmark mark='a'/> In 1939 Karl Holzinger and Frances Swineford tested seventh- and eighth-graders at "
            "two schools; nine of their tests, given to three hundred and one children, have been "
            "analysed ever since, and the data are open. <bookmark mark='b'/> Thirty-five of the thirty-six "
            f"correlations are positive, with a mean of {d['mean_r']:.2f}. One is slightly negative, "
            f"{d['min_r']:.2f}: the manifold is a strong regularity, not a law of nature. <bookmark mark='c'/> And "
            "blocks stand out: visual tests correlate most with visual ones, verbal with verbal, speeded with "
            "speeded. <bookmark mark='d'/> So there's a general factor and something more. That's chapter three's "
            "question."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in hm[0]], lag_ratio=0.01), FadeIn(hm[1]), FadeIn(rows[0]),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(groups), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
