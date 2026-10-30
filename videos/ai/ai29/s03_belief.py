from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai29.common import AGENT, BELIEF, OBS, PART, WORLD, load, node_box


class Belief(VoiceoverScene):
    def construct(self):
        self.card()
        self.define()
        self.corridor()
        self.derive()
        self.belief_mdp()

    def card(self):
        card = chapter_card(2, r"Acting without seeing everything", r"Where am I, and how sure am I?", part=PART)
        with self.voiceover("Chapter two. Acting without seeing everything."):
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
        right = abs(int(B[-1].argmax()) - int(pos[-1])) <= 1
        end = (f"to {ent[-1]:.1f} bits, with its best guess right where the robot is." if right else
               f"to {ent[-1]:.1f} bits, with its best guess still off by more than a cell.")
        with self.voiceover(
            "Here's the classic example: a robot in a corridor with "
            "a few doors, which doesn't know where it is. Its knowledge is a belief: a probability for every cell, "
            "spread evenly at first. <bookmark mark='a'/> Each step it moves right, sometimes slipping, so the belief "
            "shifts and blurs. Then it senses: door, or no door, and Bayes' rule from part five multiplies the "
            "belief by how well each cell explains what it saw. <bookmark mark='b'/> Watch the uncertainty fall as "
            f"the pattern of doors gives the place away: from {ent[0]:.1f} bits {end} <bookmark mark='c'/> "
            "This is part seven's hidden Markov model, run forward, with the robot's own moves added."
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
            vo.wait_until("c")
            self.play(Indicate(f, color=WHITE, scale_factor=1.05))
        bars.freeze()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def define(self):
        card = definition_card(r"Partially observable Markov decision process (POMDP)",
                               r"states $s$, \ actions $a$, \ transitions $P(s' \mid s, a)$, \ rewards $r(s, a)$, "
                               r"\ as in Part 26's MDP; \ plus observations $o$ with probabilities $P(o \mid s')$. \ "
                               r"The agent never sees $s$, \ only $o$.", width=7.4, color=BELIEF).move_to([-2.7, 0.7, 0])
        world = node_box(r"world: \ state $s$ \ (hidden)", WORLD, 24, height=0.9).move_to([4.3, 1.7, 0])
        agent = node_box(r"agent: \ belief $b(s)$", AGENT, 24, height=0.9).move_to([4.3, -1.3, 0])
        a1 = CurvedArrow(agent.get_right() + RIGHT * 0.05, world.get_right() + RIGHT * 0.05, angle=1.3, color=GREY_B)
        a2 = CurvedArrow(world.get_left() + LEFT * 0.05, agent.get_left() + LEFT * 0.05, angle=1.3, color=OBS)
        l1 = label(r"action $a$", font_size=22, color=GREY_B).next_to(a1, RIGHT, buff=0.08)
        keep_in_frame(l1)
        l2 = label(r"observation $o$", font_size=22, color=OBS).next_to(a2, LEFT, buff=0.08)
        hist = history_card(1965, r"K.~J.~\AA str\"om", r"optimal control with incomplete state information: \ act on "
                            r"the probability of each state", width=7.4, color=C.HUMAN, font_size=20)
        hist.move_to([-2.7, -2.3, 0])
        with self.voiceover(
            "An agent acts in a world it can only partly see. Part 26's Markov decision process assumed the agent "
            "sees the state. <bookmark mark='a'/> Drop that, and you get a partially observable Markov decision "
            "process, a POMDP. <bookmark mark='b'/> The world still has a state, and moves on when the agent acts. "
            "<bookmark mark='c'/> But all the agent gets back is an observation, a clue, drawn from a distribution "
            "that depends on the state. <bookmark mark='d'/> Karl Johan Åström showed in 1965 what to do: keep a "
            "probability for every state, a belief, and act on that."
        ) as vo:
            self.play(FadeIn(world), FadeIn(agent))
            vo.wait_until("a")
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Create(a1), FadeIn(l1))
            vo.wait_until("c")
            self.play(Create(a2), FadeIn(l2))
            vo.wait_until("d")
            self.play(FadeIn(hist, shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        colors = {r"b'(s')": BELIEF, r"P(o \mid s')": OBS}
        rows = [
            cmath(r"b'(s')", r"=", r"P(s' \mid b, a, o)", colors=colors, font_size=36),
            cmath(r"b'(s')", r"=", r"\frac{P(o \mid s')\, P(s' \mid b, a)}{P(o \mid b, a)}", colors=colors, font_size=36),
            cmath(r"P(s' \mid b, a)", r"=", r"\sum_s P(s' \mid s, a)\, b(s)", font_size=36),
            cmath(r"b'(s')", r"=", r"\eta\;", r"P(o \mid s')", r"\sum_s P(s' \mid s, a)\, b(s)", colors=colors,
                  font_size=36),
            cmath(r"\alpha_t(j)", r"=", r"P(o_t \mid j) \sum_i \alpha_{t-1}(i)\, A_{ij}", font_size=36),
        ]
        whys = [why(r"the belief after acting and seeing"), why(r"Bayes' rule"), why(r"total probability: \ predict"),
                why(r"$\eta$: \ divide by the total, \ so it sums to $1$"),
                why(r"Part 7's forward algorithm, \ $A$ the transitions")]
        step = ladder(self, rows, whys, keep=5, top=2.9, x=-2.2, buff=0.45, edge=6.9)
        tail = label(r"predict with the model of motion, \ correct with the model of the sensor", font_size=26,
                     color=BELIEF).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Where did that update come from? The new belief is the probability of each state after the agent's "
            "action and the observation it got. <bookmark mark='a'/> Bayes' rule turns it around: how likely the "
            "observation is from each state, times how likely the state was before seeing it. "
            "<bookmark mark='b'/> And that prior is the old belief pushed through the transitions: the prediction. "
            "<bookmark mark='c'/> Together, with eta just making it sum to one: predict, then correct. "
            "<bookmark mark='d'/> Strip out the actions, and it is exactly the forward recursion of Part 7's hidden "
            "Markov model. With Gaussians in place of tables, it is the Kalman filter that tracks a car on a map."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
            self.play(FadeIn(tail))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def belief_mdp(self):
        b = load("belief")
        B = np.asarray(b["beliefs"])
        picks = [0, 6, len(B) - 1]  # three beliefs from the corridor run, as small bar charts
        charts = VGroup()
        for t in picks:
            bars = VGroup(*[Rectangle(width=0.06, height=max(1.5 * v / B[t].max(), 0.01), stroke_width=0,
                                      fill_color=BELIEF, fill_opacity=0.9) for v in B[t]])
            bars.arrange(RIGHT, buff=0.015, aligned_edge=DOWN)
            cap = MathTex(rf"b_{{{t}}}", font_size=30, color=BELIEF).next_to(bars, DOWN, buff=0.15)
            charts.add(VGroup(bars, cap))
        charts.arrange(RIGHT, buff=1.3, aligned_edge=DOWN).move_to([0, 1.7, 0])
        arr = VGroup(*[Arrow(a_.get_right(), c_.get_left(), buff=0.15, color=GREY_B) for a_, c_ in zip(charts, charts[1:])])
        al = VGroup(*[label(r"act, \ observe", font_size=20, color=GREY_B).next_to(a_, UP, buff=0.1) for a_ in arr])
        thm = theorem_card(r"the belief is enough", r"the belief $b_t$ sums up the whole history $o_1, a_1, \ldots, o_t$: "
                           r"\ a POMDP is an MDP whose states are beliefs, \ so Part 26's Bellman equation applies, "
                           r"\ over a continuum of states", who=r"\AA str\"om (1965); \ Kaelbling, Littman \& Cassandra (1998)",
                           width=9.6, color=BELIEF).move_to([0, -0.9, 0])
        llm = label(r"a language-model agent's belief: \ its context window, \ everything it has seen so far",
                    font_size=24, color=AGENT).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The belief is more than bookkeeping. <bookmark mark='a'/> It sums up everything the agent has seen and "
            "done: nothing else in the history says more about the present. So a POMDP is an ordinary MDP whose "
            "states are beliefs, and Part 26's Bellman equation applies, over a continuum of states. That is why "
            "exact POMDPs are so hard to solve, and why the best policy sometimes acts just to learn: walk to a door, "
            "to find out where you are. <bookmark mark='b'/> A language-model agent keeps no explicit belief. Its "
            "context window plays the part: everything it has read and done so far, from which it must work out "
            "what is going on."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c_) for c_ in charts], lag_ratio=0.3), *[GrowArrow(a_) for a_ in arr],
                      FadeIn(al))
            vo.wait_until("a")
            self.play(FadeIn(thm, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(llm))
        self.wait(0.3)
        self.clear_scene()
