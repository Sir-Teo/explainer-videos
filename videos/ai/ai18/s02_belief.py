from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai18.compute import load


class Belief(VoiceoverScene):
    def construct(self):
        self.card()
        self.corridor()

    def card(self):
        card = chapter_card(1, r"Acting without seeing everything", r"Where am I, and how sure am I?", part=18)
        with self.voiceover("Chapter one. Acting without seeing everything."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def corridor(self):
        b = load("belief")
        n = int(b["n"])
        B = np.asarray(b["beliefs"])
        pos, obs = np.asarray(b["pos"]), np.asarray(b["obs"])
        ent = np.asarray(b["entropy"])
        doors = [int(d) for d in b["doors"]]
        W = 12.0
        cw = W / n
        x0 = -W / 2
        floor = Line([x0, -0.6, 0], [x0 + W, -0.6, 0], color=GREY_C, stroke_width=2)
        door_m = VGroup(*[Rectangle(width=cw * 0.9, height=0.7, stroke_color=C.BITS, stroke_width=2, fill_color=C.BITS,
                                    fill_opacity=0.25).move_to([x0 + cw * (d + 0.5), -0.25, 0]) for d in doors])
        bars = LiveBars(B[0], max_value=float(B.max()) * 1.02, height=2.5, bar_width=cw * 0.8, gap=cw * 0.2, colors=C.TRUE_P)
        bars.place(base_y=0.5, x=0.0)
        pm = float(b["p_move"])
        robot = VGroup(Circle(radius=0.16, color=WHITE, fill_opacity=1, fill_color=GREY_D), Dot(radius=0.04, color=C.BITS))
        robot.move_to([x0 + cw * (pos[0] + 0.5), -0.95, 0])
        sense = Text("door!", font="DejaVu Sans Mono", font_size=22, color=C.BITS)
        bl = label(r"its belief: \ how likely each cell is", font_size=22, color=C.TRUE_P).move_to([3.4, 3.35, 0])  # clear of the citation at the top left
        er = VGroup(label(r"uncertainty:", font_size=24, color=GREY_A), DecimalNumber(float(ent[0]), num_decimal_places=2,
                                                                                       font_size=28, color=C.SURPRISE),
                    label(r"bits", font_size=24, color=GREY_A)).arrange(RIGHT, buff=0.15).to_corner(DL, buff=0.4)
        colors = {r"b'(s')": C.TRUE_P, r"P(o \mid s')": C.BITS, r"P(s' \mid s, a)": GREY_A}
        f = cmath(r"b'(s')", r"\;\propto\;", r"P(o \mid s')", r"\sum_s", r"P(s' \mid s, a)", r"\,b(s)", colors=colors,
                  font_size=34).to_corner(DR, buff=0.4)
        fl = label(r"move: \ shift and blur; \ sense: \ multiply and renormalize", font_size=20, color=GREY_B)
        fl.next_to(f, UP, buff=0.12).align_to(f, RIGHT)
        tag = note(rf"a corridor of ${n}$ cells and ${len(doors)}$ doors; \ it sees a door ${int(100 * b['p_hit'])}\%$ "
                   rf"of the time it's at one, \ and imagines one ${int(100 * b['p_false'])}\%$ of the time it isn't").to_edge(DOWN, buff=0.15)
        cite_ = cite(r"S.~Thrun, W.~Burgard \& D.~Fox, \textit{Probabilistic Robotics} (2005)", corner=UL)
        with self.voiceover(
            "An agent acts in a world it can only partly see. Here's the classic example: a robot in a corridor with "
            "a few doors, which doesn't know where it is. Its knowledge is a belief: a probability for every cell, "
            "spread evenly at first. <bookmark mark='a'/> Each step it moves right, sometimes slipping, so the belief "
            "shifts and blurs. Then it senses: door, or no door, and Bayes' rule from part four multiplies the "
            "belief by how well each cell explains what it saw. <bookmark mark='b'/> Watch the uncertainty fall as "
            "the pattern of doors gives the place away. This is part six's hidden Markov model, run forward: an "
            "agent in a partly observed world, a POMDP, acts on its belief, not on the truth."
        ) as vo:
            self.play(Create(floor), FadeIn(door_m), FadeIn(bars), FadeIn(robot), FadeIn(bl), FadeIn(er), FadeIn(tag), FadeIn(cite_))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(fl))
            # the first steps slowly, in two halves: predict (shift and blur), then update on what it sensed
            phase = VMobject()
            for t in range(1, 4):
                pred = pm * np.roll(B[t - 1], 1) + (1 - pm) * B[t - 1]
                p1 = label(r"move: \ shift and blur", font_size=24, color=GREY_A).move_to([0, -1.75, 0])
                self.play(*bars.to(pred), robot.animate.move_to([x0 + cw * (pos[t] + 0.5), -0.95, 0]), FadeOut(phase),
                          FadeIn(p1), run_time=0.9)
                seen = Text("door!" if obs[t - 1] else "no door", font="DejaVu Sans Mono", font_size=22,
                            color=C.BITS if obs[t - 1] else GREY_B).next_to(robot, DOWN, buff=0.15)
                p2 = label(r"sense: \ multiply by $P(o \mid s')$, \ renormalize", font_size=24, color=C.BITS).move_to([0, -1.75, 0])
                self.play(FadeIn(seen, scale=1.3), FadeOut(p1), FadeIn(p2), run_time=0.5)
                self.play(*bars.to(B[t]), er[1].animate.set_value(float(ent[t])), run_time=0.9)
                self.play(FadeOut(seen), run_time=0.2)
                phase = p2
            self.play(FadeOut(phase), run_time=0.3)
            vo.wait_until("b")
            for t in range(4, len(B)):
                anims = [*bars.to(B[t]), robot.animate.move_to([x0 + cw * (pos[t] + 0.5), -0.95, 0]),
                         er[1].animate.set_value(float(ent[t]))]
                if obs[t - 1]:
                    flash = sense.copy().next_to([x0 + cw * (pos[t] + 0.5), -0.95, 0], DOWN, buff=0.25)
                    self.play(*anims, FadeIn(flash), run_time=0.32)
                    self.remove(flash)
                else:
                    self.play(*anims, run_time=0.32)
            self.play(Indicate(bars.bar(int(B[-1].argmax())), color=WHITE))
        bars.freeze()
        self.wait(0.3)
        self.clear_scene()
