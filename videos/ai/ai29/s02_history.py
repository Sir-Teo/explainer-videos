from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai29.common import AGENT, EXPERT, FAIL, GOOD, HIST, MODEL, OBS, PART, TOOL, WORLD, node_box


def shakey(scale=1.0) -> VGroup:
    """A drawing of SRI's Shakey: a wheeled base, a box of electronics, a mast with a camera and a range finder."""
    base = RoundedRectangle(width=1.3, height=0.32, corner_radius=0.06, stroke_color=GREY_B, stroke_width=2,
                            fill_color=GREY_D, fill_opacity=1)
    wheels = VGroup(*[Circle(radius=0.12, stroke_color=GREY_B, stroke_width=2, fill_color="#10141C", fill_opacity=1)
                      .move_to(base.get_bottom() + RIGHT * dx) for dx in (-0.42, 0.42)])
    body = Rectangle(width=0.9, height=0.9, stroke_color=GREY_B, stroke_width=2, fill_color="#2A3140", fill_opacity=1)
    body.next_to(base, UP, buff=0)
    mast = Line(body.get_top(), body.get_top() + UP * 0.9, color=GREY_B, stroke_width=4)
    cam = RoundedRectangle(width=0.5, height=0.3, corner_radius=0.05, stroke_color=OBS, stroke_width=2,
                           fill_color=OBS, fill_opacity=0.3).move_to(mast.get_end() + UP * 0.1)
    lens = Dot(cam.get_right() + LEFT * 0.06, radius=0.05, color=OBS)
    whisk = VGroup(*[Line(base.get_corner(c), base.get_corner(c) + d * 0.25, color=GREY_C, stroke_width=1.5)
                     for c, d in ((DL, LEFT + DOWN * 0.2), (DR, RIGHT + DOWN * 0.2))])
    g = VGroup(whisk, base, wheels, body, mast, cam, lens)
    return g.scale(scale)


class History(VoiceoverScene):
    def construct(self):
        self.card()
        self.shakey()
        self.darpa()
        self.learning()
        self.llm_agents()

    def card(self):
        card = chapter_card(1, r"From Shakey to agents", r"How did machines learn to act?", lit=(1968, 1971, 2026),
                            part=PART)
        with self.voiceover("Chapter one. From Shakey to agents."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def shakey(self):
        robot = shakey(1.2).move_to([-4.6, -0.4, 0])
        rooms = VGroup(*[Rectangle(width=1.6, height=1.3, stroke_color=GREY_C, stroke_width=1.5) for _ in range(3)])
        rooms.arrange(RIGHT, buff=0).move_to([-4.6, -2.75, 0])
        box_ = Square(0.28, stroke_width=0, fill_color=C.BITS, fill_opacity=0.9).move_to(rooms[2].get_center())
        card = history_card(r"1966--72", r"Shakey, \ SRI International \ (Nilsson, Rosen, Hart and others)",
                            r"the first mobile robot to reason about its own actions: \ it saw with a TV camera and a "
                            r"range finder, \ planned with logic, \ and moved slowly through a few rooms", width=6.6,
                            color=HIST).move_to([2.6, 2.1, 0])
        loop = VGroup(node_box(r"sense: \ camera", OBS, 22), node_box(r"plan: \ STRIPS, \ A*", MODEL, 22),
                      node_box(r"act: \ roll, \ push", AGENT, 22)).arrange(RIGHT, buff=0.55).move_to([2.6, -0.4, 0])
        arr = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.08, color=GREY_B, stroke_width=2.5)
                       for a, b in zip(loop, loop[1:])])
        back = CurvedArrow(loop[2].get_bottom() + DOWN * 0.05, loop[0].get_bottom() + DOWN * 0.05, angle=-0.6,
                           color=GREY_B)
        gifts = label(r"its by-products: \ the A* search (1968), \\ the STRIPS planner (1971), \ the Hough transform for "
                      r"lines", font_size=26, color=GREY_A).move_to([2.6, -2.4, 0])
        if gifts.width > 7.6:
            gifts.width = 7.6
        tag = note(r"drawing, \ after SRI's photographs").next_to(rooms, DOWN, buff=0.12)
        with self.voiceover(
            "The story of agents starts in a few rooms at the Stanford Research Institute. From 1966 to 1972, Nils "
            "Nilsson, Charles Rosen and their colleagues built Shakey, the first mobile robot that reasoned about its "
            "own actions. <bookmark mark='a'/> It looked with a television camera, <bookmark mark='b'/> planned in "
            "logic, <bookmark mark='c'/> and then moved, so slowly that its name came from how it wobbled. "
            "<bookmark mark='d'/> Its by-products outlived it: the A-star search of Part 2, the STRIPS planner, and a "
            "better way to find lines in pictures. <bookmark mark='e'/> And it fixed a pattern for decades: sense "
            "the world, build a model of it, plan, act, and sense again."
        ) as vo:
            self.play(FadeIn(robot, shift=UP * 0.2), Create(rooms), FadeIn(box_), FadeIn(card), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(loop[0]), Indicate(robot[5], color=OBS))
            vo.wait_until("b")
            self.play(GrowArrow(arr[0]), FadeIn(loop[1]))
            vo.wait_until("c")
            self.play(GrowArrow(arr[1]), FadeIn(loop[2]), robot.animate.shift(RIGHT * 0.5), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(gifts))
            vo.wait_until("e")
            self.play(Create(back), robot.animate.shift(LEFT * 0.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def darpa(self):
        head = label(r"The DARPA challenges: \ robots that drive", font_size=36).to_edge(UP, buff=0.4)
        W = 6.6
        x0 = -4.6
        rows = []
        data = [(r"2004", r"Mojave desert, \ about $142$ miles", 7.4 / 142, r"no one finished; \ the best, CMU's Sandstorm, "
                 r"went about $7$ miles", FAIL),
                (r"2005", r"desert, \ $132$ miles", 1.0, r"five finished; \ Stanford's Stanley won in under $7$ hours", GOOD),
                (r"2007", r"Urban Challenge, \ about $60$ miles of streets, \ with traffic", 1.0,
                 r"six finished; \ CMU's Boss won", GOOD)]
        for k, (yr, what, frac, res, col) in enumerate(data):
            y = 1.7 - 1.55 * k
            yl = label(yr, font_size=34, color=HIST).move_to([x0 - 1.3, y, 0])
            wl = label(what, font_size=22, color=GREY_A)
            if wl.width > W:
                wl.width = W
            wl.move_to([x0, y + 0.42, 0], aligned_edge=LEFT)
            track = Line([x0, y, 0], [x0 + W, y, 0], color=GREY_D, stroke_width=6)
            prog = Line([x0, y, 0], [x0 + W * frac, y, 0], color=col, stroke_width=6)
            car = Dot([x0, y, 0], radius=0.1, color=WHITE)
            rl = label(res, font_size=22, color=col)
            if rl.width > W:
                rl.width = W
            rl.move_to([x0, y - 0.42, 0], aligned_edge=LEFT)
            rows.append((yl, wl, track, prog, car, rl, frac))
        key = history_card(2005, r"Stanley \ (Thrun and the Stanford team)", r"what won was learning: \ it taught itself "
                           r"to tell road from desert, \ labelling far-off camera pixels with what its lasers said up "
                           r"close", width=4.4, color=HIST, font_size=22).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.2)
        cite_ = cite(r"Thrun et al., \textit{Stanley} (2006); \ Urmson et al., \textit{Boss} (2008)", corner=DL)
        with self.voiceover(
            "The next leap came from the desert. In March 2004, the American defence research agency DARPA offered a "
            "million dollars to any robot car that could drive about a hundred and forty miles across the Mojave "
            "on its own. <bookmark mark='a'/> None came close: the best, Carnegie Mellon's Sandstorm, went about "
            "seven miles and got stuck on an embankment. <bookmark mark='b'/> Eighteen months later, five cars finished a "
            "hundred-and-thirty-two-mile course, and Stanford's Stanley won in under seven hours. "
            "<bookmark mark='c'/> What made the difference was learning: Stanley taught itself to recognise the road "
            "far ahead in its camera images, using what its lasers measured up close as the labels. "
            "<bookmark mark='d'/> In 2007 the Urban Challenge put the cars in traffic, among stop signs and other "
            "robots; six finished, and Carnegie Mellon's Boss won. The engineers from these races went on to build "
            "today's self-driving cars."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_), *[FadeIn(VGroup(r[0], r[1], r[2])) for r in rows[:1]])
            self.add(rows[0][4])
            vo.wait_until("a")
            r = rows[0]
            self.play(Create(r[3]), r[4].animate.move_to(r[3].get_end()), run_time=1.2)
            self.play(r[4].animate.set_color(FAIL), FadeIn(r[5]))
            vo.wait_until("b")
            r = rows[1]
            self.play(FadeIn(VGroup(r[0], r[1], r[2])))
            self.add(r[4])
            self.play(Create(r[3]), r[4].animate.move_to(r[3].get_end()), run_time=2.0)
            self.play(FadeIn(r[5]))
            vo.wait_until("c")
            self.play(FadeIn(key, shift=UP * 0.2))
            vo.wait_until("d")
            r = rows[2]
            self.play(FadeIn(VGroup(r[0], r[1], r[2])))
            self.add(r[4])
            self.play(Create(r[3]), r[4].animate.move_to(r[3].get_end()), FadeIn(r[5]), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def learning(self):
        head = label(r"Robots that learn", font_size=36).to_edge(UP, buff=0.4)
        cards = VGroup(
            history_card(1989, r"ALVINN \ (Pomerleau, CMU)", r"a small network steers a van by copying a human "
                         r"driver: \ imitation learning (chapter 9)", width=6.5, color=HIST, font_size=28),
            history_card(2016, r"end-to-end visuomotor policies \ (Levine, Finn, Darrell \& Abbeel)", r"one network "
                         r"from camera pixels to motor torques; \ the same year, Google's arm farm learned to grasp "
                         r"from hundreds of thousands of tries", width=6.5, color=HIST, font_size=28),
            history_card(2019, r"Dactyl \ (OpenAI)", r"a robot hand solves a Rubik's cube, \ trained only in "
                         r"simulation, \ randomized (chapter 14)", width=6.5, color=HIST, font_size=28),
            history_card(2022, r"SayCan, \ RT-1 \ (Google)", r"language models choose the robot's next skill; \ a "
                         r"transformer trained on $130{,}000$ demonstrations (chapter 15)", width=6.5, color=HIST,
                         font_size=28),
        )
        cards.arrange_in_grid(rows=2, cols=2, buff=(0.35, 0.5))
        if cards.width > 13.2:
            cards.width = 13.2
        if cards.height > 6.0:
            cards.height = 6.0
        cards.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Meanwhile robots began to learn their skills instead of having them programmed. <bookmark mark='a'/> "
            "In 1989 Dean Pomerleau's ALVINN steered a van along a road with a small neural network that copied a "
            "human driver, the idea of chapter nine. <bookmark mark='b'/> In 2016 Sergey Levine, Chelsea Finn and "
            "colleagues trained one network from camera pixels straight to motor torques, and a room of robot arms "
            "at Google learned to grasp from hundreds of thousands of attempts. <bookmark mark='c'/> In 2019 an "
            "OpenAI robot hand solved a Rubik's cube after training only in simulations it never fully trusted. "
            "<bookmark mark='d'/> And in 2022 language models began choosing what a robot should do next, while "
            "Google's RT-1, a transformer, learned seven hundred tasks from a hundred and thirty thousand "
            "demonstrations."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def llm_agents(self):
        head = label(r"Language models that act", font_size=36).to_edge(UP, buff=0.4)
        ev = [(r"2021", r"WebGPT: \ a model that browses", TOOL),
              (r"2022", r"ReAct: \ reason, \ act, \ observe", AGENT),
              (r"2023", r"Toolformer; \ function calling; \ AutoGPT", TOOL),
              (r"2024", r"SWE-agent; \ computer use; \ MCP", AGENT),
              (r"2025", r"coding agents in the terminal", AGENT),
              (r"2026", r"agents working for hours", GOOD)]
        X0, X1 = -6.0, 6.0
        Y = 0.7
        axis = Line([X0, Y, 0], [X1, Y, 0], color=GREY_C, stroke_width=2)
        marks = VGroup()
        for k, (yr, what, col) in enumerate(ev):
            x = X0 + 0.6 + k * (X1 - X0 - 1.2) / (len(ev) - 1)
            d = Dot([x, Y, 0], radius=0.1, color=col)
            yl = label(yr, font_size=30, color=HIST).next_to(d, UP if k % 2 == 0 else DOWN, buff=0.2)
            wl = label(what, font_size=28, color=col)
            if wl.width > 3.9:
                wl.width = 3.9
            wl.next_to(yl, UP if k % 2 == 0 else DOWN, buff=0.12)
            keep_in_frame(wl, margin=0.25)
            marks.add(VGroup(d, yl, wl))
        loop = VGroup(node_box(r"a language model", AGENT, 28), node_box(r"a tool, \ a browser, \ a terminal", TOOL, 28))
        loop.arrange(RIGHT, buff=2.8).move_to([0, -2.4, 0])
        a1 = CurvedArrow(loop[0].get_top() + UP * 0.05, loop[1].get_top() + UP * 0.05, angle=-0.6, color=GREY_B)
        a2 = CurvedArrow(loop[1].get_bottom() + DOWN * 0.05, loop[0].get_bottom() + DOWN * 0.05, angle=-0.6, color=GREY_B)
        l1 = label(r"action", font_size=20, color=GREY_B).next_to(a1, UP, buff=0.05)
        l2 = label(r"observation", font_size=20, color=GREY_B).next_to(a2, DOWN, buff=0.05)
        with self.voiceover(
            "The newest agents grew out of language models. <bookmark mark='a'/> In 2021 OpenAI's WebGPT learned to "
            "search the web and quote what it found. In 2022 ReAct had a model alternate between thinking and acting. "
            "<bookmark mark='b'/> In 2023 models learned to call tools, from calculators to any program described "
            "in a few lines of JSON. <bookmark mark='c'/> In 2024 agents fixed real bugs in real repositories, and "
            "began to use a computer's screen and mouse; <bookmark mark='d'/> by 2025 they wrote code in a terminal "
            "for long stretches, and by 2026 for hours on end. <bookmark mark='e'/> Underneath all of it is one "
            "loop, older than Shakey: act, see what happened, decide again. The rest of this part is about that "
            "loop, in software and in the physical world."
        ) as vo:
            self.play(FadeIn(head), Create(axis))
            vo.wait_until("a")
            self.play(FadeIn(marks[0]), FadeIn(marks[1]))
            vo.wait_until("b")
            self.play(FadeIn(marks[2]))
            vo.wait_until("c")
            self.play(FadeIn(marks[3]))
            vo.wait_until("d")
            self.play(FadeIn(marks[4]), FadeIn(marks[5]))
            vo.wait_until("e")
            self.play(FadeIn(loop), Create(a1), Create(a2), FadeIn(l1), FadeIn(l2))
        self.wait(0.3)
        self.clear_scene()
