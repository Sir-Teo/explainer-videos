from __future__ import annotations

import numpy as np

from videos.psychology.psych3.common import *  # noqa: F403


class Jingle(VoiceoverScene):
    def construct(self):
        self.card()
        self.names()
        self.grit()

    def card(self):
        card = chapter_card(8, r"Jingle and jangle", r"When is a new name a new thing?",
                            lit={1927: r"Kelley names the jangle fallacy"}, part=PART, scale=("person", "group"),
                            marr=("what",))
        with self.voiceover(
            "Chapter eight. Jingle and jangle."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def names(self):
        fl = archive.FLAKE_FRIED_2020.data
        head = heading(r"Two ways a name can mislead")

        def tagbox(text, color):
            t = label(text, font_size=28, color=color)
            return VGroup(SurroundingRectangle(t, color=color, buff=0.18, stroke_width=2.5, corner_radius=0.1), t)

        thing_a = Circle(radius=0.5, stroke_width=0, fill_color=GROUP_A, fill_opacity=0.9)
        thing_b = Square(0.9, stroke_width=0, fill_color=GROUP_B, fill_opacity=0.9)
        # jingle: one name over two different things
        j_name = tagbox(r"``self-regulation''", P.ACCENT)
        j_things = VGroup(thing_a.copy(), thing_b.copy()).arrange(RIGHT, buff=1.2)
        j_caps = VGroup(label(r"a questionnaire", font_size=24, color=GROUP_A),
                        label(r"a laboratory task", font_size=24, color=GROUP_B))
        jingle = VGroup(j_name, j_things).arrange(DOWN, buff=0.9)
        for c, t in zip(j_caps, j_things):
            c.next_to(t, DOWN, buff=0.15)
        j_lines = VGroup(*[Line(j_name.get_bottom(), t.get_top(), color=GREY_B, stroke_width=2, buff=0.08) for t in j_things])
        j_title = VGroup(label(r"jingle", font_size=44, color=WHITE),
                         label(r"one name, two things", font_size=30, color=GREY_A)).arrange(DOWN, buff=0.1)
        left = VGroup(j_title, VGroup(jingle, j_caps, j_lines)).arrange(DOWN, buff=0.45).move_to([-3.6, 0.25, 0])
        # jangle: two names over one thing
        g_names = VGroup(tagbox(r"``grit''", GRIT), tagbox(r"``conscientiousness''", TRAIT["conscientious"]))
        g_names.arrange(RIGHT, buff=0.4)
        g_thing = Circle(radius=0.5, stroke_width=0, fill_color=TRUE, fill_opacity=0.9)
        jangle = VGroup(g_names, g_thing).arrange(DOWN, buff=0.9)
        g_lines = VGroup(*[Line(n.get_bottom(), g_thing.get_top(), color=GREY_B, stroke_width=2, buff=0.08) for n in g_names])
        g_title = VGroup(label(r"jangle", font_size=44, color=WHITE),
                         label(r"two names, one thing", font_size=30, color=GREY_A)).arrange(DOWN, buff=0.1)
        right = VGroup(g_title, VGroup(jangle, g_lines)).arrange(DOWN, buff=0.45).move_to([3.6, 0.45, 0])
        fact = label(rf"depression alone has at least {fl['depression_scales']} different scales", font_size=28,
                     color=P.ACCENT).to_edge(DOWN, buff=0.75)
        src = published_tag(archive.FLAKE_FRIED_2020.cite)
        with self.voiceover(
            "Validity has two failures so common that they have nicknames, both about a hundred years old. "
            "<bookmark mark='a'/> The jingle fallacy is assuming that two measures with the same name measure "
            "the same thing. A questionnaire about self-regulation and a laboratory task called a test of "
            "self-regulation share a word. Whether they share anything else is a question for the data, and "
            "it has been raised about exactly this pair. <bookmark mark='b'/> The count gives you a sense of the problem. For "
            f"depression alone, researchers have a choice of at least {fl['depression_scales']} different "
            "scales, with different questions in them. Two studies of depression may not have studied the same "
            "thing. <bookmark mark='c'/> The jangle fallacy is the reverse: assuming that two measures with "
            "different names measure different things. It's the more tempting of the two, because a new name "
            "feels like a discovery. So let's look at a famous case."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(left, lag_ratio=0.1), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(fact, shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(right, lag_ratio=0.1), run_time=2.0)
        self.clear_scene()

    def grit(self):
        d = load("jingle")
        head = heading(r"Grit, and an older name for nearly the same thing")
        pub = VGroup(
            label(r"grit: \ ``perseverance and passion for long-term goals''", font_size=26, color=GRIT),
            label(rf"{d['k_samples']} samples, {fmt_int(d['n_people'])} people", font_size=26, color=GREY_A),
            label(rf"grit with conscientiousness: \ $\rho = {r2(d['rho'])}$", font_size=40, color=P.ACCENT),
            label(r"after correcting for unreliability", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.14).move_to([0, 2.15, 0])
        rng_ = np.random.default_rng(7)

        def named(text, sub, color):
            t = label(text, font_size=40, color=color)
            return VGroup(VGroup(SurroundingRectangle(t, color=color, buff=0.25, stroke_width=3, corner_radius=0.12), t),
                          label(sub, font_size=26, color=GREY_A)).arrange(DOWN, buff=0.25)

        intro = VGroup(named(r"conscientiousness", r"measured for decades", TRAIT["conscientious"]),
                       named(r"grit", r"introduced in 2007", GRIT)).arrange(RIGHT, buff=1.6, aligned_edge=UP)
        intro.move_to([0, -0.9, 0])
        jit = lambda v: np.asarray(v) + rng_.uniform(-0.35, 0.35, len(v))  # noqa: E731

        def plot(x, y, xl, yl, color, cx, r):
            A = axes([10, 62], [10, 62], x_length=3.5, y_length=2.9, xticks=[12, 36, 60], yticks=[12, 36, 60],
                     xlabel=xl, ylabel=yl, center=[cx, -1.1, 0], font_size=18)
            pts = scatter(A.ax, jit(x), jit(y), color, radius=0.025, opacity=0.6)
            rl = label(rf"$r = {r2(r)}$", font_size=34, color=color).next_to(A, RIGHT, buff=0.2).shift(UP * 0.6)
            return VGroup(A, pts, rl)

        same = plot(d["c1"], d["c2"], r"conscientiousness, form A", r"form B", TRAIT["conscientious"], -4.7, d["r_forms"])
        other = plot(d["c1"], d["grit"], r"conscientiousness, form A", r"the grit scale", GRIT, 1.5, d["r_grit"])
        same_cap = label(r"a scale and its twin", font_size=22, color=GREY_A).next_to(same[2], DOWN, buff=0.15)
        other_cap = VGroup(label(r"a scale and", font_size=22, color=GREY_A),
                           label(r"``another trait''", font_size=22, color=GREY_A),
                           label(rf"corrected: \ {r2(d['corrected'])}", font_size=26, color=P.ACCENT))
        other_cap.arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(other[2], DOWN, buff=0.15).align_to(other[2], LEFT)
        src = published_tag(archive.CREDE_2017.cite)
        tag = simulated_tag(r"scatter plots: simulated, the Pool")
        with self.voiceover(
            "In 2007 grit was introduced as a trait of its own: perseverance and passion for long-term goals. "
            "It was presented as highly predictive of success, and it became famous. Psychology already had a "
            "trait called conscientiousness, measured for decades: being organized, persistent, dependable. "
            f"<bookmark mark='a'/> In 2017 a meta-analysis put the two side by side: {d['k_samples']} samples, "
            f"nearly nineteen thousand people. Corrected for unreliability, as Spearman taught, grit and "
            f"conscientiousness correlate {d['rho']:.2f}. <bookmark mark='b'/> What does that look like? In the "
            "Pool, here is a conscientiousness questionnaire against a second form of itself: the same trait, "
            f"measured twice. They correlate {d['r_forms']:.2f}. <bookmark mark='c'/> And here's the same "
            f"questionnaire against a grit scale built to the published figure: {d['r_grit']:.2f}. A measure "
            "of a supposedly different trait agrees with it nearly as well as its own twin does. "
            "<bookmark mark='d'/> This doesn't make grit worthless. It makes it mostly an old trait under a new "
            "name, and it sets the test for any new construct: correct for unreliability first, then show that "
            "the new measure predicts something the old one doesn't. Whether grit passes that second test is "
            "still argued, and we return to it in Part 28."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pub[0]))
            self.play(FadeIn(intro[1], shift=UP * 0.15))
            self.wait(7.0)
            self.play(FadeIn(intro[0], shift=UP * 0.15))
            vo.wait_until("a")
            self.play(FadeIn(pub[1]), FadeIn(pub[2], shift=UP * 0.1), FadeIn(pub[3]), FadeIn(src))
            vo.wait_until("b")
            self.play(FadeOut(intro), FadeIn(same[0]), FadeIn(same[1], lag_ratio=0.01), FadeIn(tag), run_time=2.0)
            self.play(FadeIn(same[2]), FadeIn(same_cap))
            vo.wait_until("c")
            self.play(FadeIn(other[0]), FadeIn(other[1], lag_ratio=0.01), run_time=2.0)
            self.play(FadeIn(other[2]), FadeIn(other_cap[0]), FadeIn(other_cap[1]))
            vo.wait_until("d")
            self.play(FadeIn(other_cap[2], shift=UP * 0.1))
        self.clear_scene()
