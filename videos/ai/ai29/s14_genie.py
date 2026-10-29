from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai29.common import AGENT, CLAIM, HIST, MODEL, OBS, PART, REWARD, TOOL, WORLD, node_box

JEPA = C.EMBED


def frame(k, w=1.5, h=1.0, hero_x=0.0, seed=0) -> VGroup:
    """A schematic platform-game frame: ground, two platforms, a hero."""
    g = np.random.default_rng(seed)
    box = RoundedRectangle(width=w, height=h, corner_radius=0.06, stroke_color=GREY_B, stroke_width=1.5,
                           fill_color="#16202E", fill_opacity=1)
    ground = Rectangle(width=w, height=0.12, stroke_width=0, fill_color="#3C5A3A", fill_opacity=1).align_to(box, DOWN)
    plats = VGroup(*[Rectangle(width=0.35, height=0.06, stroke_width=0, fill_color=GREY_C, fill_opacity=1)
                     .move_to(box.get_center() + np.array([x, y, 0])) for x, y in g.uniform([-0.5, -0.2], [0.5, 0.25], (2, 2))])
    hero = Square(0.14, stroke_width=0, fill_color=C.BITS, fill_opacity=1)
    hero.move_to(ground.get_top() + UP * 0.07 + RIGHT * hero_x)
    return VGroup(box, ground, plats, hero)


class Genie(VoiceoverScene):
    def construct(self):
        self.card()
        self.latent_actions()
        self.worlds()
        self.dreamer4()
        self.jepa()

    def card(self):
        card = chapter_card(13, r"Worlds you can walk through", r"Can a model of the world be learned from video?",
                            lit=(2026,), part=PART)
        with self.voiceover("Chapter thirteen. Worlds you can walk through."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def latent_actions(self):
        f0, f1 = frame(0, hero_x=-0.3, seed=1), frame(1, hero_x=0.0, seed=1)
        pair = VGroup(f0, f1).arrange(RIGHT, buff=0.3).move_to([-4.4, 1.6, 0])
        pl = label(r"two frames of a video, \ no controller recorded", font_size=20, color=GREY_A).next_to(pair, UP, buff=0.15)
        lam = node_box(r"latent action model", MODEL, 22, height=0.8).move_to([-0.6, 1.6, 0])
        codes = VGroup(*[Square(0.34, stroke_color=MODEL, stroke_width=1.5, fill_color=MODEL,
                                fill_opacity=0.6 if k == 2 else 0.08) for k in range(8)]).arrange(RIGHT, buff=0.06)
        codes.move_to([3.4, 1.6, 0])
        cl = label(r"one of $8$ codes: \ which ``button'' was pressed", font_size=20, color=MODEL).next_to(codes, UP, buff=0.15)
        a1 = Arrow(pair.get_right(), lam.get_left(), buff=0.1, color=GREY_B)
        a2 = Arrow(lam.get_right(), codes.get_left(), buff=0.1, color=GREY_B)
        dyn = node_box(r"dynamics model: \ next frame from \ past frames and a code", WORLD, 22, height=0.8)
        dyn.move_to([-0.6, -0.9, 0])
        play_ = VGroup(*[frame(k, w=1.3, h=0.9, hero_x=-0.4 + 0.25 * k, seed=1) for k in range(4)]).arrange(RIGHT, buff=0.15)
        play_.move_to([3.4, -0.9, 0])
        pl2 = label(r"a player picks the codes: \ the video becomes a game", font_size=20, color=C.BITS).next_to(play_, DOWN, buff=0.15)
        a3 = Arrow(codes.get_bottom(), dyn.get_right() + UP * 0.2, buff=0.1, color=MODEL)
        a4 = Arrow(dyn.get_right(), play_.get_left(), buff=0.1, color=GREY_B)
        hist = history_card(r"Feb 2024", r"Genie \ (Bruce, Dennis, Edwards et al., Google DeepMind)", r"$11$ billion "
                            r"parameters, \ trained on Internet videos of 2D platform games \ without a single action "
                            r"label", width=6.0, color=HIST, font_size=18).to_corner(DL, buff=0.3)
        tag = note(r"schematic").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Our world models learned from frames paired with the actions that caused them. The Internet is full of "
            "video, but almost none of it records which buttons were pressed. <bookmark mark='a'/> Genie, from Google "
            "DeepMind in 2024, learned the actions too. A latent action model looks at two consecutive frames and "
            "must explain the change with one of just eight codes, <bookmark mark='b'/> as if guessing which button "
            "was pressed. <bookmark mark='c'/> A dynamics model learns to draw the next frame from the past frames "
            "and a code. <bookmark mark='d'/> At play time a person picks the codes, and a video model becomes a game "
            "you can steer, learned from game videos with no labels at all."
        ) as vo:
            self.play(FadeIn(pair), FadeIn(pl), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowArrow(a1), FadeIn(lam), FadeIn(hist))
            vo.wait_until("b")
            self.play(GrowArrow(a2), FadeIn(codes), FadeIn(cl))
            vo.wait_until("c")
            self.play(GrowArrow(a3), FadeIn(dyn))
            vo.wait_until("d")
            self.play(GrowArrow(a4), LaggedStart(*[FadeIn(f_) for f_ in play_], lag_ratio=0.3), FadeIn(pl2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def worlds(self):
        cards = VGroup(
            history_card(r"Dec 2024", r"Genie 2", r"3D worlds from a single image, \ steered with keyboard and mouse", width=6.2,
                         color=HIST, font_size=19),
            history_card(r"Aug 2025", r"Genie 3", r"$720$p at $24$ frames a second, \ in real time; \ consistent for a few "
                         r"minutes, \ remembering what it drew up to a minute ago; \ text prompts change the world "
                         r"as you go; \ used to train DeepMind's SIMA agent", width=6.2, color=HIST, font_size=19),
            history_card(r"Jan 2026", r"Project Genie", r"a prototype on Genie 3 for some subscribers in the US: \ "
                         r"$60$-second worlds", width=6.2, color=HIST, font_size=19),
            history_card(r"27 Oct 2026", r"Genie 4 \ (Google DeepMind's description)", r"sound generated with the "
                         r"pictures; \ Gemini plans events in the world; \ pitched for training robots; \ a research "
                         r"preview, \ and objects can still drift", width=6.2, color=CLAIM, font_size=19),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        if cards.height > 7.0:
            cards.height = 7.0
        cards.to_edge(LEFT, buff=0.35)
        strip = VGroup(*[frame(k, w=1.7, h=1.1, hero_x=-0.5 + 0.3 * k, seed=3 + k // 2) for k in range(4)])
        strip.arrange_in_grid(rows=2, cols=2, buff=0.2).move_to([4.4, 1.0, 0])
        keys = VGroup(*[RoundedRectangle(width=0.42, height=0.42, corner_radius=0.06, stroke_color=GREY_B, stroke_width=1.5)
                        for _ in range(4)])
        keys[0].move_to([4.4, -1.4, 0])
        keys[1].move_to([3.92, -1.88, 0])
        keys[2].move_to([4.4, -1.88, 0])
        keys[3].move_to([4.88, -1.88, 0])
        kl = VGroup(*[MathTex(t, font_size=22, color=GREY_A).move_to(k_) for t, k_ in zip(("W", "A", "S", "D"), keys)])
        kt = label(r"actions in, \ frames out, \ in real time", font_size=20, color=GREY_A).next_to(keys, DOWN, buff=0.2)
        tag = note(r"schematic").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Then the worlds grew. <bookmark mark='a'/> Genie 2, in December 2024, made three-dimensional worlds "
            "from a single picture. <bookmark mark='b'/> Genie 3, in August 2025, drew them at seven hundred and "
            "twenty lines, twenty-four frames a second, in real time, and kept them consistent for a few minutes: "
            "walk away from a wall and come back, and what you painted on it is still there. Text could change the "
            "world as you went, and DeepMind used it to train its SIMA agent. <bookmark mark='c'/> In January 2026 a "
            "prototype opened to some subscribers. <bookmark mark='d'/> And two days ago, on the twenty-seventh of "
            "October, DeepMind announced Genie 4, with sound generated alongside the picture and pitched as a place "
            "to train robots; by DeepMind's own account, objects can still drift over long sessions."
        ) as vo:
            self.play(FadeIn(strip), FadeIn(keys), FadeIn(kl), FadeIn(kt), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=RIGHT * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dreamer4(self):
        steps = VGroup(node_box(r"hours of Minecraft video, \ a little of it with actions", OBS, 22),
                       node_box(r"a world model \ (a transformer, \ shortcut forcing)", MODEL, 22),
                       node_box(r"an agent trained \ only inside it", AGENT, 22),
                       node_box(r"diamonds", REWARD, 24))
        steps.arrange(RIGHT, buff=0.45).move_to([0, 1.3, 0])
        if steps.width > 13.0:
            steps.width = 13.0
        arr = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.06, color=GREY_B, stroke_width=2.5)
                       for a, b in zip(steps, steps[1:])])
        hist = history_card(r"Sep 2025", r"Dreamer 4 \ (Hafner, Yan \& Lillicrap)", r"the first agent to obtain diamonds "
                            r"in Minecraft purely from offline data, \ choosing sequences of over $20{,}000$ mouse and "
                            r"keyboard actions from pixels; \ the world model runs in real time on one GPU", width=9.0,
                            color=HIST, font_size=20).move_to([0, -1.4, 0])
        with self.voiceover(
            "Danijar Hafner's Dreamer line, the subject of the last chapter, reached the same scale. "
            "<bookmark mark='a'/> Dreamer 4, in 2025, learned a world model mostly from Minecraft videos, only a "
            "small part of them labelled with actions, <bookmark mark='b'/> then trained an agent entirely inside "
            "it, <bookmark mark='c'/> and that agent collected diamonds, a task of more than twenty thousand mouse "
            "and keyboard actions, without ever playing the real game during training."
        ) as vo:
            self.play(FadeIn(steps[0]), FadeIn(hist))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(GrowArrow(arr[k]), FadeIn(steps[k + 1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def jepa(self):
        gen = VGroup(label(r"predict the pixels", font_size=26, color=WORLD),
                     label(r"Genie, \ Dreamer, \ video models (Part 22): \\ every leaf, \ every ripple", font_size=20,
                           color=GREY_A)).arrange(DOWN, buff=0.15).move_to([-3.6, 2.3, 0])
        emb = VGroup(label(r"predict an embedding", font_size=26, color=JEPA),
                     label(r"JEPA (Part 24): \ only what the encoder \\ finds worth predicting", font_size=20,
                           color=GREY_A)).arrange(DOWN, buff=0.15).move_to([3.6, 2.3, 0])
        now = VGroup(*[Dot(radius=0.07, color=JEPA).move_to([x, 0, 0]) for x in (-5.2,)])
        goal = Star(n=5, outer_radius=0.22, color=REWARD, fill_opacity=1).move_to([2.6, 0.6, 0])
        gl = label(r"the goal image's embedding", font_size=18, color=REWARD).next_to(goal, UP, buff=0.12)
        g = np.random.default_rng(7)
        paths, best = VGroup(), None
        for k in range(9):
            pts = [np.array([-5.2, 0.0, 0])]
            for t in range(5):
                pts.append(pts[-1] + np.array([1.55, g.normal(0.12, 0.45), 0]))
            m = VMobject(stroke_color=GREY_C, stroke_width=1.5, stroke_opacity=0.6).set_points_smoothly(pts)
            paths.add(m)
            d = np.linalg.norm(pts[-1][:2] - goal.get_center()[:2])
            if best is None or d < best[0]:
                best = (d, k, pts)
        win = VMobject(stroke_color=JEPA, stroke_width=4).set_points_smoothly(best[2])
        pl = label(r"imagined action sequences, \ rolled out in embedding space", font_size=20, color=GREY_A)
        pl.move_to([-1.6, -1.6, 0])
        hist = history_card(r"Jun 2025", r"V-JEPA 2-AC \ (Meta)", r"after a million hours of video, \ $62$ hours of robot "
                            r"video teach it how actions change what it sees; \ it picks and places objects in labs it "
                            r"never saw, \ by searching for actions whose predicted embedding nears the goal's",
                            width=5.6, color=HIST, font_size=18).to_corner(DR, buff=0.3)
        tag = note(r"schematic").to_corner(DL, buff=0.3)
        with self.voiceover(
            "All of these predict pixels: every leaf and every ripple, most of which an agent doesn't need. "
            "<bookmark mark='a'/> Part 24's joint-embedding predictive architectures predict an embedding instead, "
            "only what the encoder finds worth predicting. <bookmark mark='b'/> Meta's V-JEPA 2 turned this into a "
            "world model for a robot. After pretraining on a million hours of video, sixty-two hours of robot video "
            "taught it how the arm's actions change what it sees. <bookmark mark='c'/> To act, it imagines many "
            "action sequences in embedding space <bookmark mark='d'/> and carries out the one whose predicted "
            "embedding comes closest to a picture of the goal. With that, it picked up and placed objects in labs it "
            "had never seen. Planning with a learned model, as in MuZero, but the model is learned from video."
        ) as vo:
            self.play(FadeIn(gen), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(emb))
            vo.wait_until("b")
            self.play(FadeIn(hist, shift=UP * 0.15), FadeIn(now), FadeIn(goal), FadeIn(gl))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(p_) for p_ in paths], lag_ratio=0.1), FadeIn(pl), run_time=2.0)
            vo.wait_until("d")
            self.play(Create(win), paths[best[1]].animate.set_stroke(opacity=0))
        self.wait(0.3)
        self.clear_scene()
