from __future__ import annotations

from videos.philosophy.philosophy11.common import *  # noqa: F403


class Older(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Older than Gettier", r"Who noticed first?", lit=(770,), part=PART)
        with self.voiceover("Chapter three. Older than Gettier."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.mirage()
        self.others()
        self.arrow()

    def mirage(self):
        hc = history_card(r"c.\ 770", r"Dharmottara", r"Buddhist epistemologist, \ commentator on Dharmakīrti",
                          width=5.4, color=HIST).to_corner(UL, buff=0.35)
        sand = Rectangle(width=12.0, height=1.2, stroke_width=0, fill_color="#5A4A2A", fill_opacity=0.5).move_to(
            [0, -1.6, 0])
        trav = person(r"a thirsty traveller", color=WHITE, scale=0.7).move_to([-5.0, -0.6, 0])
        shimmer = VGroup(*[Line([2.0 + 0.0 * i, -1.1 - 0.12 * i, 0], [4.6, -1.1 - 0.12 * i, 0], color=BEL,
                                stroke_width=3, stroke_opacity=0.7 - 0.12 * i) for i in range(4)])
        sh_l = label(r"a mirage: \ there seems to be water", font_size=22, color=BEL).next_to(shimmer, UP, buff=0.5)
        rock = Polygon([3.1, -1.6, 0], [3.9, -1.6, 0], [3.7, -1.15, 0], [3.25, -1.2, 0], color=GREY_B,
                       fill_opacity=0.6)
        water = Ellipse(width=0.9, height=0.25, color="#4FA3FF", fill_opacity=0.8).move_to([3.5, -1.75, 0])
        w_l = label(r"but under a rock, \ there really is water", font_size=22, color=OK).next_to(water, DOWN,
                                                                                               buff=0.15)
        rows = VGroup(label(r"he believes there is water there: \ true, \ and on the evidence of his eyes",
                            font_size=24),
                      label(r"what he saw was not what made it true", font_size=24, color=LUCK)).arrange(
            DOWN, buff=0.2).move_to([0, 1.4, 0])
        with self.voiceover(
            "Gettier did not know it, but his cases had ancestors. <bookmark mark='a'/>In eighth-century India, the "
            "Buddhist philosopher Dharmottara gave this one. A traveller in the desert is looking for water. Ahead "
            "he sees a shimmering blue expanse: a mirage. <bookmark mark='b'/>But when he reaches the spot, there "
            "really is water there, hidden under a rock. <bookmark mark='c'/>He believed there was water there, the "
            "belief was true, and he had the evidence of his eyes. But what he saw was not the water that made his "
            "belief true. Dharmottara used cases like this to argue about what a genuine source of knowledge, a "
            "pramāṇa, must be."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(sand), FadeIn(trav))
            vo.wait_until("a")
            self.play(Create(shimmer), FadeIn(sh_l))
            vo.wait_until("b")
            self.play(trav.animate.move_to([0.3, -0.6, 0]), run_time=2)
            self.play(FadeIn(rock), FadeIn(water), FadeIn(w_l))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def others(self):
        head = label(r"The same shape, \ again and again", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        hd = [label(r"case", font_size=22, color=P.CLAIM), label(r"the evidence", font_size=22, color=P.CLAIM),
              label(r"what makes it true", font_size=22, color=P.CLAIM)]
        rows = [[label(r"Dharmottara (c.\ 770)", font_size=20), label(r"a mirage", font_size=20, color=BEL),
                 label(r"water under a rock", font_size=20, color=OK)],
                [label(r"Russell (1948)", font_size=20), label(r"a stopped clock", font_size=20, color=BEL),
                 label(r"you look at the right minute", font_size=20, color=OK)],
                [label(r"Gettier (1963)", font_size=20), label(r"Jones will get the job", font_size=20, color=BEL),
                 label(r"Smith's own ten coins", font_size=20, color=OK)],
                [label(r"Chisholm (1966)", font_size=20), label(r"a dog that looks like a sheep", font_size=20,
                                                                color=BEL),
                 label(r"a sheep behind a hill", font_size=20, color=OK)]]
        grid = ValueGrid(hd, rows, col_w=[3.6, 3.9, 3.9], cell_h=0.6, font_size=20).move_to([0, 0.1, 0])
        tail = VGroup(label(r"step 1: \ evidence that points the wrong way", font_size=24, color=BEL),
                      label(r"step 2: \ luck that makes the belief true anyway", font_size=24, color=LUCK)).arrange(
            DOWN, buff=0.2).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Once you see the shape, you find it everywhere. <bookmark mark='a'/>Dharmottara's mirage. Bertrand "
            "Russell's stopped clock, from 1948. Gettier's coins. And Roderick Chisholm's sheep: a man in a field "
            "sees what he takes to be a sheep. It is a dog, disguised by distance; but a real sheep is grazing out of "
            "sight, behind a hill. <bookmark mark='b'/>Every case has two steps. First, evidence that points the "
            "wrong way. Then luck, which makes the belief true anyway."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), FadeIn(grid.rule), FadeIn(grid.rows_bg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[r])) for r in range(4)], lag_ratio=0.6), run_time=6)
            vo.wait_until("b")
            self.play(FadeIn(tail[0]))
            self.play(FadeIn(tail[1]))
        self.clear_scene()

    def arrow(self):
        head = label(r"A lucky arrow", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        archer = person(r"", color=WHITE, scale=0.8).move_to([-5.6, 0.3, 0])
        target = VGroup(*[Circle(radius=r, stroke_color=c, stroke_width=3) for r, c in
                          ((0.7, WHITE), (0.45, BAD), (0.2, GOAL))]).move_to([5.0, 0.3, 0])
        start = np.array([-5.2, 0.4, 0])
        aim = Line(start, target.get_center(), color=GREY_D, stroke_width=1.5)
        aim_l = label(r"the aim: \ the evidence", font_size=20, color=JUST).next_to(aim, UP, buff=0.1).shift(
            LEFT * 2.5)
        path = VMobject(color=LUCK, stroke_width=3)
        path.set_points_smoothly([start, [-2.5, 0.6, 0], [-0.6, 1.8, 0], [1.6, 2.2, 0], [3.4, 1.2, 0],
                                  target.get_center()])
        g1 = label(r"a gust", font_size=20, color=LUCK).move_to([-0.6, 2.4, 0])
        g2 = label(r"another gust", font_size=20, color=LUCK).move_to([3.6, 1.9, 0])
        tip = Dot(start, color=LUCK)
        rows = VGroup(label(r"it hits the centre: \ true", font_size=24, color=OK),
                      label(r"it was well aimed: \ justified", font_size=24, color=JUST),
                      label(r"but it did not hit \textit{because} it was well aimed", font_size=26, color=LUCK)
                      ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here is the shape as a picture, which we will use again. <bookmark mark='a'/>An archer aims well at the "
            "target. <bookmark mark='b'/>A gust of wind blows the arrow off course; a second gust blows it back, and "
            "it lands in the centre. <bookmark mark='c'/>The shot is accurate. It was skilfully aimed. But it did not "
            "hit because it was skilfully aimed. Belief is the arrow, truth the target, justification the aim; and a "
            "Gettier case is a lucky arrow. Whatever knowledge is, it is not a lucky arrow."
        ) as vo:
            self.play(FadeIn(head), FadeIn(archer), Create(target))
            vo.wait_until("a")
            self.play(Create(aim), FadeIn(aim_l))
            vo.wait_until("b")
            self.add(tip)
            self.play(MoveAlongPath(tip, path), Create(path), FadeIn(g1), run_time=3, rate_func=linear)
            self.play(FadeIn(g2), Flash(target.get_center(), color=GOAL))
            vo.wait_until("c")
            for r in rows:
                self.play(FadeIn(r))
        self.clear_scene()
