from __future__ import annotations

import numpy as np

from videos.psychology.psych8.common import *  # noqa: F403


class Reverse(VoiceoverScene):
    def construct(self):
        self.card()
        self.two_ways()
        self.bayes()
        self.decoding()

    def card(self):
        card = chapter_card(10, r"Reading a mind backwards", r"The region lit up. What was the person doing?",
                            lit={2006: r"reverse inference"}, part=PART, scale=("brain", "mind"), marr=("what",))
        with self.voiceover(
            "Chapter ten. Reading a mind backwards."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def two_ways(self):
        head = heading(r"Two directions, \ and only one of them was measured")
        task = RoundedRectangle(width=3.6, height=1.3, corner_radius=0.15, color=MODEL, stroke_width=3,
                                fill_color=MODEL, fill_opacity=0.1).move_to([-4.6, 1.2, 0])
        region = RoundedRectangle(width=3.6, height=1.3, corner_radius=0.15, color=BLOOD, stroke_width=3,
                                  fill_color=BLOOD, fill_opacity=0.1).move_to([-4.6, -1.9, 0])
        tl = wrapped_label(r"a mental process: \ fear", 3.2, 30, MODEL).move_to(task)
        rl = wrapped_label(r"a region is active: \ the amygdala", 3.2, 30, BLOOD).move_to(region)
        fwd = Arrow(task.get_bottom() + LEFT * 0.8, region.get_top() + LEFT * 0.8, buff=0.08, color=MODEL, stroke_width=6)
        back = Arrow(region.get_top() + RIGHT * 0.8, task.get_bottom() + RIGHT * 0.8, buff=0.08, color=BAD, stroke_width=6)
        fl = label(r"forward", font_size=26, color=MODEL).next_to(fwd, LEFT, buff=0.12)
        bl = label(r"reverse", font_size=26, color=BAD).next_to(back, RIGHT, buff=0.12)
        rows = rows_of([
            (r"forward: \ frighten people, \ and the amygdala responds. \ An experiment; \ this is what "
             r"studies measure.", MODEL),
            (r"reverse: \ the amygdala responded, \ so they were afraid. \ This is what headlines say.", BAD),
            (r"``If it rains the street is wet'' does not give ``the street is wet, so it rained''.", WHITE),
            (r"It depends on what else makes the amygdala respond: \ faces, novelty, reward, surprise.", THRESH),
        ], 6.3, 29, 0.3).move_to([3.5, -0.3, 0])
        keep_in_frame(rows)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "The third way a map misleads isn't in the statistics. It's in the sentence written "
            "underneath. <bookmark mark='a'/> An imaging experiment runs forward. You control what people "
            "do, frighten them, say, and observe which regions respond. Fear, therefore amygdala. "
            "<bookmark mark='b'/> The sentence in the newspaper runs the other way. People looked at a "
            "politician's face, their amygdala responded, therefore they were afraid of him. Amygdala, "
            "therefore fear. Nobody measured that direction. <bookmark mark='c'/> It's an old mistake in "
            "logic. If it rains, the street is wet. But a wet street doesn't prove rain. "
            "<bookmark mark='d'/> Whether the backward step is any good depends on what else makes that "
            "region respond. And the amygdala responds to faces, to anything new, to rewards, to surprise. "
            "Russell Poldrack named this in 2006. He called it reverse inference, and he showed how to "
            "put a number on it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(task), FadeIn(tl), FadeIn(region), FadeIn(rl))
            vo.wait_until("a")
            self.play(GrowArrow(fwd), FadeIn(fl), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowArrow(back), FadeIn(bl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def bayes(self):
        r = load("reverse")
        p = archive.POLDRACK_2006.data
        head = heading(r"The number is Bayes' rule, \ and the base rates matter")
        A = axes([0, 1], [0, 1], x_length=5.4, y_length=4.0, xticks=[0, 0.5, 1], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.1f}",
                 xlabel=r"how likely the process was, before the scan", ylabel=r"after seeing the region active",
                 center=[-3.7, -0.6, 0])
        ax = A.ax
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(1, 1), color=GREY_D, stroke_width=2)
        cw = curve(ax, r["priors"], r["weak"], THRESH, stroke_width=4)
        cs = curve(ax, r["priors"], r["strong"], MODEL, stroke_width=3)
        pts = VGroup(*[Dot(ax.c2p(x, y), radius=0.08, color=WHITE) for x, y in
                       ((0.5, r["at_half"]), (0.2, r["at_fifth"]), (0.1, r["at_tenth"]))])
        lw = label(rf"this region: \ odds $\times\,{p['bayes_factor']}$", font_size=26, color=THRESH).next_to(ax.c2p(0.6, 0.5), RIGHT, buff=0.1)
        ls = label(r"a selective region: \ odds $\times\,10$", font_size=23, color=MODEL).next_to(ax.c2p(1.0, 1.0), RIGHT, buff=0.12)
        rows = rows_of([
            (rf"{p['region']} and {p['process']}, \ from a database of studies", DATA),
            (rf"start at {p['prior']:.1f}: \ the activation takes you to {p['posterior']:.2f}", THRESH),
            (rf"start at 0.2: \ to {r['at_fifth']:.2f}. \ At 0.1: \ to {r['at_tenth']:.2f}", WHITE),
            (r"A region that many tasks activate tells you little about any one of them.", P.ACCENT),
        ], 5.2, 29, 0.3).move_to([4.2, -0.5, 0])
        keep_in_frame(rows)
        src = published_tag(archive.POLDRACK_2006.cite)
        tag = psyche_tag(r"curves: computed from the published factor")
        with self.voiceover(
            "The number is Bayes' rule, from Part 4. What you want is the probability that a process was "
            "engaged, given that a region was active. That depends on how often the region is active when "
            "the process is engaged, against how often it's active when it isn't. "
            f"<bookmark mark='a'/> Poldrack took one of the safest cases there is: {p['region']} and "
            f"{p['process']}. In a database of published experiments, activation there multiplies the "
            f"odds of language by about {p['bayes_factor']}. <bookmark mark='b'/> So if you thought "
            f"language was fifty-fifty beforehand, the scan moves you to {p['posterior']:.2f}. By his own "
            "description, that's weak evidence. <bookmark mark='c'/> And it's weaker still when the idea "
            f"was unlikely to begin with. Start at one in five, and you end at {r['at_fifth']:.2f}. Start "
            f"at one in ten, and you end at {r['at_tenth']:.2f}. <bookmark mark='d'/> A region that "
            "responded to one thing only would multiply the odds by far more. Few do. The regions that "
            "turn up in the most headlines are among the least selective in the brain, which is partly why "
            "they turn up."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(A), FadeIn(diag))
            vo.wait_until("a")
            self.play(Create(cw), FadeIn(lw), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(pts[0], scale=2.0), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[1], scale=2.0), FadeIn(pts[2], scale=2.0), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(cs), FadeIn(ls), FadeIn(rows[3]), run_time=2.0)
        self.clear_scene()

    def decoding(self):
        head = heading(r"When reading backwards is honest")
        rows = VGroup(
            VGroup(label(r"train", font_size=36, color=MODEL),
                   wrapped_label(r"fit a model that predicts the mental state from the whole pattern of "
                                 r"activity, \ not one region", 12.4, 31, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"test", font_size=36, color=THRESH),
                   wrapped_label(r"on scans the model has never seen, \ and report how often it is right",
                                 12.4, 31, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"compare", font_size=36, color=DATA),
                   wrapped_label(r"with chance, \ and with what you could have guessed without the scanner",
                                 12.4, 31, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"then the claim is a number", font_size=36, color=P.ACCENT),
                   wrapped_label(r"``right 70 times in 100, on new people'' can be checked. \ ``The fear centre "
                                 r"lit up'' cannot.", 12.4, 31, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, -0.35, 0])
        # the opening picture: a whole pattern of activity goes into a model, and a guess comes out
        g = np.random.default_rng(11)
        cells = VGroup(*[Square(side_length=0.3, stroke_width=0, fill_color=interpolate_color(
            ManimColor("#1B2230"), ManimColor(THRESH), float(g.beta(1.2, 2.5))), fill_opacity=1)
            for _ in range(60)]).arrange_in_grid(rows=6, cols=10, buff=0.04)
        pattern = VGroup(cells, label(r"one scan: \ a pattern over thousands of voxels", font_size=28,
                                      color=GREY_A).next_to(cells, DOWN, buff=0.2))
        box = VGroup(RoundedRectangle(width=2.6, height=1.2, corner_radius=0.12, color=MODEL, stroke_width=3),
                     label(r"a model", font_size=34, color=MODEL))
        guess = VGroup(label(r"listening?", font_size=34, color=WHITE), label(r"looking?", font_size=34, color=GREY_B),
                       label(r"resting?", font_size=34, color=GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        flow = VGroup(pattern, box, guess).arrange(RIGHT, buff=1.5).move_to([0, -0.2, 0])
        box.match_y(cells)
        guess.match_y(cells)
        arrows = VGroup(Arrow(cells.get_right(), box.get_left(), buff=0.2, color=GREY_B, stroke_width=4),
                        Arrow(box.get_right(), guess.get_left(), buff=0.2, color=GREY_B, stroke_width=4))
        opening = VGroup(flow, arrows)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "None of this means a scan can never tell you what someone is doing. It means the claim has to "
            "be earned, and there's an honest way to earn it. <bookmark mark='a'/> Fit a model that "
            "predicts the mental state from the whole pattern of activity, across thousands of voxels, "
            "instead of from one region's name. <bookmark mark='b'/> Then test it on scans it's never "
            "seen, and report how often it's right. <bookmark mark='c'/> Compare that with chance, and "
            "with what you could have guessed without a scanner at all. <bookmark mark='d'/> Then the "
            "claim is a number, and a number can be checked. Right seventy times in a hundred, on new "
            "people, is a statement about the world. The fear centre lit up is a story. This is called "
            "decoding, it's Part 4's prediction on fresh data once more, and it's where the frontier of "
            "this part is."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(pattern))
            self.play(GrowArrow(arrows[0]), FadeIn(box), run_time=1.2)
            self.play(GrowArrow(arrows[1]), FadeIn(guess, lag_ratio=0.3), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeOut(opening), FadeOut(tag))
            for k, mark_ in enumerate("abcd"):
                vo.wait_until(mark_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.15))
        self.clear_scene()
