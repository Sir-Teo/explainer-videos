from __future__ import annotations

import numpy as np

from videos.psychology.psych7.common import *  # noqa: F403


class Bumps(VoiceoverScene):
    def construct(self):
        self.card()
        self.gall()
        self.flourens()
        self.lashley()

    def card(self):
        card = chapter_card(2, r"Bumps, pigeons and rats", r"Can you find a faculty by looking for it?",
                            lit={1929: r"Lashley's mass action"}, part=PART, scale=("brain",), marr=("tissue",))
        with self.voiceover(
            "Chapter two. Bumps, pigeons and rats."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def gall(self):
        head = heading(r"Around 1800: \ a good idea and a bad method")
        hd = head_outline(5.0).move_to([-4.0, -0.3, 0])
        c = hd.get_center() + np.array([-0.3, 0.9, 0])
        names = [r"caution", r"wit", r"pride", r"love of children", r"tune", r"number", r"secretiveness"]
        g = np.random.default_rng(18)
        patches = VGroup()
        for i, n in enumerate(names):
            a = PI * (0.1 + 0.8 * i / (len(names) - 1))
            p = c + np.array([1.55 * np.cos(a), 1.05 * np.sin(a) - 0.1 * (i % 2), 0])
            patches.add(VGroup(Ellipse(width=0.9, height=0.5, color=THRESH, stroke_width=2).move_to(p),
                               label(n, font_size=15, color=THRESH).move_to(p)))
        good = VGroup(label(r"the good idea", font_size=32, color=SPARED),
                      wrapped_label(r"The brain is the organ of the mind, \ and it has parts with different "
                                    r"jobs.", 5.8, 28, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        bad = VGroup(label(r"the bad method", font_size=32, color=LESION),
                     wrapped_label(r"A strong faculty swells its organ; \ the organ raises a bump on the skull; "
                                   r"\ so read the bumps.", 5.8, 28, WHITE),
                     wrapped_label(r"Evidence: \ striking cases that fit. \ Cases that did not fit were explained "
                                   r"away.", 5.8, 28, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        side = VGroup(good, bad).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([3.4, -0.2, 0])
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Around 1800 the Viennese physician Franz Joseph Gall proposed something that scandalized his "
            "contemporaries. <bookmark mark='a'/> The brain is the organ of the mind, he said, and it isn't "
            "one organ but many. Each faculty of the mind has its own piece of brain. That was a good idea, "
            "and in outline it's what we believe today. <bookmark mark='b'/> Then came the method. A strong "
            "faculty, Gall reasoned, must have a large organ. A large organ must push out the skull above "
            "it. So you could read a person's character from the bumps on their head. He mapped more than "
            "two dozen faculties this way: caution, wit, pride, the love of children. <bookmark mark='c'/> "
            "And look at his evidence, with Part 4 in mind. He collected striking cases that fitted. A "
            "pickpocket with a bump in the right place. A poet with another. Cases that didn't fit were "
            "explained away. There was no control group and no way for the idea to fail. Phrenology had a "
            "long career in fairgrounds, and none in science."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(hd))
            vo.wait_until("a")
            self.play(FadeIn(good, shift=RIGHT * 0.15))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p, scale=0.7) for p in patches], lag_ratio=0.25), FadeIn(bad[0]),
                      FadeIn(bad[1]), run_time=4.0)
            vo.wait_until("c")
            self.play(FadeIn(bad[2], shift=UP * 0.1))
        self.clear_scene()

    def flourens(self):
        head = heading(r"The 1820s: \ take a piece out, and see what is lost")
        brain = brain_side(5.2, fill=0.3).move_to([-3.8, 0.2, 0])
        cut_cb = lesion_mark(brain.lobe["cerebellum"].get_center(), 0.5)
        cut_cx = lesion_mark(at(brain, -0.2, 0.35), 0.75)
        rows = VGroup(
            VGroup(label(r"remove the cerebellum", font_size=30, color=CEREBELLUM),
                   wrapped_label(r"the bird can no longer fly or walk straight; \ it still sees and wants", 5.6, 27,
                                 WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"remove the cerebral hemispheres", font_size=30, color=FRONTAL),
                   wrapped_label(r"the bird sits, and starts nothing by itself", 5.6, 27, WHITE)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"remove part of the hemispheres", font_size=30, color=PARIETAL),
                   wrapped_label(r"everything is a little weaker, \ wherever the cut", 5.6, 27, WHITE)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.08),
            wrapped_label(r"His conclusion: \ the big parts differ, \ and inside the hemispheres there are no "
                          r"separate organs.", 5.6, 28, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([3.5, -0.2, 0])
        tag = note(r"schematic: a human brain stands in for a pigeon's").to_corner(DR, buff=0.2)
        with self.voiceover(
            "The first person to test Gall by experiment was a French physiologist, Pierre Flourens, in the "
            "eighteen-twenties. His method was the one this whole part is about. Take a piece out, and see "
            "what's lost. He worked on pigeons and rabbits. <bookmark mark='a'/> Remove the cerebellum, and "
            "the bird could no longer fly or walk straight, though it still saw and still wanted to. "
            "<bookmark mark='b'/> Remove the cerebral hemispheres, and the bird sat where it was put and "
            "started nothing by itself. So the large parts do different things. <bookmark mark='c'/> But "
            "when he removed only a part of the hemispheres, he found no particular faculty missing. "
            "Everything was a little weaker, wherever he cut. <bookmark mark='d'/> Flourens concluded that "
            "Gall was wrong. Within the hemispheres, he said, there are no separate organs. They work as "
            "one. That became the accepted view for a generation."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(brain))
            vo.wait_until("a")
            self.play(FadeIn(cut_cb, scale=0.5), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeOut(cut_cb), *[brain.lobe[n].animate.set_fill(opacity=0.05) for n in LOBES], FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(*[brain.lobe[n].animate.set_fill(opacity=0.3) for n in LOBES], FadeIn(cut_cx, scale=0.5),
                      FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def lashley(self):
        m = load("massaction")
        head = heading(r"Thirty years of rats, \ and a result with two readings")
        panels = VGroup()
        axs = []
        for i, (name, title, col) in enumerate((("one", r"a task with one place", LESION),
                                                ("many", r"a task that can be done six ways", MODEL))):
            A = axes([0, 0.65], [0, 80], x_length=4.6, y_length=3.3, xticks=[0, 0.2, 0.4, 0.6], yticks=[0, 40, 80],
                     xfmt=lambda v: f"{100 * v:.0f}", xlabel=r"cortex removed (\%)", ylabel=r"errors in the maze",
                     center=[-4.1 + 5.3 * i, -0.75, 0])
            ax = A.ax
            keep = slice(0, 160)
            dots = VGroup(*[Dot(ax.c2p(s + 0.012 * ((k % 5) - 2), e), radius=0.035, color=col, fill_opacity=0.7)
                            for k, (s, e) in enumerate(zip(m[f"{name}_size"][keep], m[f"{name}_errors"][keep]))])
            means = curve(ax, m["sizes"], m[f"{name}_mean_by_size"], WHITE, stroke_width=3)
            t = label(title, font_size=26, color=col).next_to(A, UP, buff=0.12)
            panels.add(VGroup(A, dots, means, t))
            axs.append(ax)
        side = VGroup(
            wrapped_label(rf"one place: \ errors follow \emph{{where}} the cut was \ ($r = {r2(m['one_r_place'])}$)",
                          3.3, 25, LESION),
            wrapped_label(rf"six ways: \ errors follow \emph{{how much}} was cut \ ($r = {r2(m['many_r_size'])}$), "
                          rf"\ hardly where \ ($r = {r2(m['many_r_place'])}$)", 3.3, 25, MODEL),
            wrapped_label(r"In both model brains every job has its own place.", 3.3, 26, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([5.3, -0.6, 0])
        keep_in_frame(side)
        VGroup(panels, side).shift(LEFT * 0.35)
        story = wrapped_label(r"Lashley, 1929: \ how badly a rat learns a maze depends on how much cortex is "
                              r"gone, hardly on where. \ ``Mass action.''", 12.6, 28, WHITE).move_to([0, 2.35, 0])
        src = historical_tag(archive.LASHLEY_1929.cite)
        tag = psyche_tag(r"computed: two model brains")
        with self.voiceover(
            "A century later the American psychologist Karl Lashley ran the same kind of experiment on a "
            "question we met in Part 6: where is a memory? <bookmark mark='a'/> He trained rats in mazes, "
            "removed pieces of their cortex, different pieces in different rats, and counted their errors. "
            "How badly a rat did depended on how much cortex was gone, and hardly at all on where it came "
            "from. He called it mass action. After thirty years of looking, he reported that he had not "
            "found the memory trace anywhere. <bookmark mark='b'/> That reads like a victory for the brain "
            "as one undivided organ. Before accepting it, think about the task. A rat can get through a maze "
            "by sight, by smell, by the feel of the walls, or by remembering its own turns. So here are two "
            "model brains. In both of them, every job has its own place. <bookmark mark='c'/> Give the first "
            "a task that needs one place, and remove random pieces. The errors depend on where the cut was: "
            "they jump when the cut takes that place, and otherwise don't. <bookmark mark='d'/> Give the "
            "second a task that can be done six ways, each with its own place. Now the errors climb with the "
            "amount removed, wherever it was removed. That's Lashley's result, from a brain in which nothing "
            "is spread out. <bookmark mark='e'/> So his finding doesn't show that the cortex is undivided. "
            "It shows that what you find depends on the task you use to look. Hold on to that. It comes back "
            "in every chapter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(story))
            vo.wait_until("c")
            self.play(FadeIn(panels[0][0]), FadeIn(panels[0][3]))
            self.play(FadeIn(panels[0][1], lag_ratio=0.01), run_time=2.0)
            self.play(Create(panels[0][2]), FadeIn(side[0]))
            vo.wait_until("d")
            self.play(FadeIn(panels[1][0]), FadeIn(panels[1][3]))
            self.play(FadeIn(panels[1][1], lag_ratio=0.01), run_time=2.0)
            self.play(Create(panels[1][2]), FadeIn(side[1]))
            vo.wait_until("e")
            self.play(FadeIn(side[2], shift=UP * 0.1))
        self.clear_scene()
