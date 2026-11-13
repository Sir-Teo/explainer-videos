from __future__ import annotations

import numpy as np

from videos.psychology.psych1.common import *  # noqa: F403

class Behaviour(VoiceoverScene):
    def construct(self):
        self.card()
        self.manifesto()
        self.tolman()
        self.lashley()

    def card(self):
        card = chapter_card(7, r"Banning the mind", r"If observing the mind can't be trusted, why not stop?",
                            lit=(1898, 1913, 1938), part=PART, scale=("person",), marr=("what",))
        with self.voiceover(
            "Chapter seven. Banning the mind."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def manifesto(self):
        quote = quote_card(r"Psychology as the behaviorist views it is a purely objective experimental branch of "
                           r"natural science. Its theoretical goal is the prediction and control of behavior. "
                           r"Introspection forms no essential part of its methods.",
                           r"John B. Watson, \emph{Psychological Review}, 1913", width=11.0, font_size=32)
        quote.move_to([0, -0.9, 0])
        hc = history_card(1913, r"John B. Watson, Johns Hopkins", r"``Psychology as the Behaviorist Views It''",
                          color=P.ARCHIVE, width=7.6, font_size=30).to_edge(UP, buff=0.45)
        bb = black_box().scale(1.35).move_to([0, 0.35, 0])
        lock = label(r"out of bounds", font_size=38, color=GREY_B).move_to(bb.box)
        loop = CurvedArrow(bb.out.get_end() + DOWN * 0.15, bb.inp.get_start() + DOWN * 0.15, angle=-PI / 2.4,
                           color=P.REWARD, stroke_width=4)
        rew = label(r"reward and punishment change the link", font_size=32, color=P.REWARD).next_to(loop, DOWN, buff=0.12)
        gains = VGroup(label(r"experiments anyone could repeat", font_size=32, color=WHITE),
                       label(r"laws of learning that hold across species \ (Part 16)", font_size=32, color=WHITE))
        gains.arrange(DOWN, buff=0.2).to_edge(UP, buff=0.4)
        with self.voiceover(
            "The American answer was drastic. If observing the mind can't be trusted, stop observing it. In 1913 "
            "John Watson published a manifesto. <bookmark mark='a'/> Psychology as the behaviorist views it is a "
            "purely objective experimental branch of natural science. Its theoretical goal is the prediction and "
            "control of behavior. Introspection forms no essential part of its methods. <bookmark mark='b'/> For "
            "the next forty years, in America, that was close to the rule. Study what an animal does: the "
            "stimulus going in, the response coming out, and how reward and punishment change the link between "
            "them. <bookmark mark='c'/> What happens in between was declared out of bounds. "
            "<bookmark mark='d'/> It bought a great deal. Experiments that anyone could repeat, with a rat, a "
            "lever and a counter. And laws of learning that hold from pigeons to people, which fill Part 16. "
            "<bookmark mark='e'/> But it left things it couldn't explain, and two of the sharpest came from inside "
            "the camp."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(quote, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(quote), FadeOut(hc), FadeIn(bb.box))
            self.play(GrowArrow(bb.inp), FadeIn(bb[3]))
            self.play(GrowArrow(bb.out), FadeIn(bb[4]))
            self.play(Create(loop), FadeIn(rew))
            vo.wait_until("c")
            self.play(FadeIn(lock, scale=1.2))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.15) for g in gains], lag_ratio=0.6), run_time=4.0)
            vo.wait_until("e")
            self.play(Wiggle(bb.box, scale_value=1.04))
        self.clear_scene()

    def maze(self) -> VGroup:
        """A small maze with a route through it."""
        walls = VGroup()
        s = 0.62
        segs = [((0, 0), (5, 0)), ((0, 4), (5, 4)), ((0, 0), (0, 3)), ((5, 1), (5, 4)), ((1, 1), (1, 4)),
                ((2, 0), (2, 3)), ((3, 1), (3, 4)), ((4, 0), (4, 3))]
        for (x0, y0), (x1, y1) in segs:
            walls.add(Line([x0 * s, y0 * s, 0], [x1 * s, y1 * s, 0], color=GREY_A, stroke_width=4))
        way = [(-0.5, 3.5), (0.5, 3.5), (0.5, 0.5), (1.5, 0.5), (1.5, 3.5), (2.5, 3.5), (2.5, 0.5), (3.5, 0.5),
               (3.5, 3.5), (4.5, 3.5), (4.5, 0.5), (5.5, 0.5)]
        path = VMobject(color=P.ACCENT, stroke_width=3).set_points_as_corners([[x * s, y * s, 0] for x, y in way])
        food = Dot([5.5 * s, 0.5 * s, 0], radius=0.11, color=P.REWARD)
        g = VGroup(walls, path, food)
        g.walls, g.path, g.food = walls, path, food
        return g

    def tolman(self):
        head = heading(r"Tolman's rats: \ learning with no reward")
        mz = self.maze().scale(1.15).move_to([-4.4, -0.2, 0])
        rat = Dot(mz.path.get_start(), radius=0.1, color=WHITE)
        days = np.arange(1, 18)
        rewarded = 3 + 7.0 * np.exp(-(days - 1) / 4.5)
        never = 8.6 + 1.4 * np.exp(-(days - 1) / 6.0)
        late = np.where(days <= 11, never, 2.2 + (never[10] - 2.2) * np.exp(-(days - 11) / 0.9))
        A = axes([1, 17], [0, 11], x_length=6.6, y_length=4.0, xlabel=r"day", ylabel=r"wrong turns per run",
                 xticks=[1, 5, 9, 13, 17], center=[2.9, -0.3, 0])
        ax = A.ax
        c_rew = curve(ax, days, rewarded, GREY_A, 3)
        c_nev = curve(ax, days, never, GREY_C, 3)
        c_late = curve(ax, days, late, P.ACCENT, 4)
        d11 = DashedLine(ax.c2p(11, 0), ax.c2p(11, 10.6), color=P.REWARD, stroke_width=2)
        d11_lab = label(r"food appears", font_size=24, color=P.REWARD).next_to(ax.c2p(11, 10.6), UP, buff=0.05)
        labs = VGroup(label(r"never fed", font_size=26, color=GREY_B).next_to(ax.c2p(15.2, never[14]), UP, buff=0.12),
                      label(r"fed every day", font_size=26, color=GREY_A).next_to(ax.c2p(4.2, rewarded[3]), UR,
                                                                                  buff=0.05),
                      label(r"fed from day 11", font_size=26, color=P.ACCENT).next_to(ax.c2p(12.3, 5.4), RIGHT,
                                                                                    buff=0.1))
        claim = label(r"``a cognitive map''", font_size=38, color=P.ACCENT).to_edge(DOWN, buff=0.5)
        sch = note(r"schematic, after Tolman and Honzik (1930)").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Edward Tolman let hungry rats explore a maze for ten days with no food in it. They wandered, and "
            "made plenty of wrong turns. <bookmark mark='a'/> On the eleventh day he put food at the end. "
            "<bookmark mark='b'/> Within a day or two they were running the maze as well as rats that had been "
            "fed there from the start. <bookmark mark='c'/> They had learned the layout while nothing was "
            "rewarding them. And Tolman said what a behaviourist was not supposed to say: the rat has a map of "
            "the maze in its head."
        ) as vo:
            self.play(FadeIn(head), FadeIn(mz.walls), FadeIn(rat), FadeIn(A), FadeIn(sch))
            self.play(MoveAlongPath(rat, mz.path), Create(c_nev), Create(c_rew), FadeIn(labs[0]), FadeIn(labs[1]),
                      run_time=4.5, rate_func=linear)
            vo.wait_until("a")
            self.play(GrowFromCenter(mz.food), Create(d11), FadeIn(d11_lab))
            vo.wait_until("b")
            rat.move_to(mz.path.get_start())
            self.play(MoveAlongPath(rat, mz.path), Create(c_late), run_time=2.2, rate_func=linear)
            self.play(FadeIn(labs[2]))
            vo.wait_until("c")
            self.play(FadeIn(mz.path), FadeIn(claim, shift=UP * 0.15))
        self.clear_scene()

    def lashley(self):
        head = heading(r"Lashley's pianist: \ too fast for a chain")
        keys = VGroup(*[Rectangle(width=0.5, height=1.7, stroke_color=GREY_C, stroke_width=2, fill_color=WHITE,
                                  fill_opacity=0.95) for _ in range(16)]).arrange(RIGHT, buff=0)
        keys.move_to([0, 1.5, 0])
        blacks = VGroup(*[Rectangle(width=0.3, height=1.05, stroke_width=0, fill_color="#10141C", fill_opacity=1)
                          .move_to(keys[i].get_corner(UR) + DOWN * 0.525) for i in range(15) if i % 7 not in (2, 6)])
        gap_ms, loop_ms = 1000 / 16, 100.0
        unit = 0.03
        x0 = -5.6
        axis = Line([x0, -1.3, 0], [x0 + 385 * unit, -1.3, 0], color=GREY_C, stroke_width=2)
        ticks = VGroup()
        for k in range(7):
            x = x0 + k * gap_ms * unit
            ticks.add(Line([x, -1.3, 0], [x, -0.85, 0], color=WHITE, stroke_width=4))
        t_lab = label(rf"a note every {gap_ms:.0f} ms \ (sixteen a second)", font_size=28, color=WHITE)
        t_lab.next_to(ticks, UP, buff=0.15).align_to(ticks, LEFT)
        fb = Arrow([x0, -1.95, 0], [x0 + loop_ms * unit, -1.95, 0], buff=0, color=KANT, stroke_width=5)
        fb_lab = label(r"feel the key, then react: \ the brain alone takes about 100 ms", font_size=28, color=KANT)
        fb_lab.next_to(fb, RIGHT, buff=0.25)
        late = label(r"too late to trigger the next note", font_size=30, color=P.ERR).next_to(fb, DOWN, buff=0.35)
        late.align_to(fb, LEFT)
        plan = label(r"The sequence is planned before it starts.", font_size=38, color=P.ACCENT)
        plan.to_edge(DOWN, buff=0.45)
        ms_lab = label(r"time", font_size=22, color=GREY_B).next_to(axis, RIGHT, buff=0.12)
        order = [3, 5, 7, 8, 10, 12, 14, 15, 13, 11, 10, 8, 7, 5, 3, 1]
        with self.voiceover(
            "And Karl Lashley asked how a pianist plays a fast passage. A good pianist can play sixteen notes a "
            f"second: about {gap_ms:.0f} milliseconds from one note to the next. <bookmark mark='a'/> But a "
            "reaction takes longer than that. We saw it in chapter two: the brain alone needs about a tenth of a "
            "second. So the feel of one finger landing can't be what triggers the next. The signal would arrive "
            "too late. <bookmark mark='b'/> The sequence has to be planned in advance, as a whole, before it "
            "starts. <bookmark mark='c'/> A map. A plan. Those are things inside the animal. The box had "
            "contents, and the behaviourists' own experiments showed it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(keys), FadeIn(blacks))
            for k in order:
                keys[k].set_fill(P.ACCENT)
                self.wait(1 / 15)
                keys[k].set_fill(WHITE)
            self.play(Create(axis), FadeIn(ms_lab), LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.3),
                      FadeIn(t_lab), run_time=2.0)
            vo.wait_until("a")
            self.play(GrowArrow(fb), FadeIn(fb_lab))
            self.play(FadeIn(late, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(plan, shift=UP * 0.15))
            for k in order:
                keys[k].set_fill(P.ACCENT)
                self.wait(1 / 15)
                keys[k].set_fill(WHITE)
            vo.wait_until("c")
            self.play(Indicate(plan, color=P.ACCENT, scale_factor=1.06))
        self.clear_scene()
