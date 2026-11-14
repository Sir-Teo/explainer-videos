from __future__ import annotations

import numpy as np

from videos.music.music12.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 10, r"Frontier: \ why five to seven unequal steps?", r"Why do the world's scales look alike?", extra=((2009, r"scales and the harmonic series"),),
                spoken="Chapter 10. The frontier: why five to seven unequal steps?")
        self.scatter()
        self.equal()
        self.reasons()

    # ------------------------------------------------------------------
    def scatter(self):
        d = load("frontier")
        rows = d["rows"]
        g = axes([0, 0.58], [1.5, 6.5], x_length=8.4, y_length=4.0, xlabel=r"how evenly the seven notes are spread", ylabel=r"fifths in the scale", xticks=[0, 0.2, 0.4], yticks=[2, 3, 4, 5, 6], font_size=22).move_to(LEFT * 1.6 + DOWN * 0.3)
        rough = np.array([r["roughness"] for r in rows])
        lo, hi = rough.min(), rough.max()
        rng = np.random.default_rng(2)
        dots = VGroup()
        for r in rows:
            w = (r["roughness"] - lo) / (hi - lo)
            col = interpolate_color(ManimColor(GOOD), ManimColor(BAD), float(w))
            dots.add(Dot(g.ax.c2p(r["evenness"], r["fifths"] + float(rng.uniform(-0.14, 0.14))), radius=0.07, color=col, fill_opacity=0.9))
        k = [r["steps"] for r in rows].index(d["diatonic"])
        ring = Circle(radius=0.22, color=WHITE, stroke_width=3).move_to(dots[k])
        tag = label(r"the white keys", font_size=26, color=WHITE).next_to(ring, RIGHT, buff=0.15)
        key = VGroup(label(r"each dot: \ one of the 66 shapes", font_size=22, color=GREY_A), label(r"green: \ smooth, \ by Part 5's roughness", font_size=22, color=GOOD), label(r"red: \ rough", font_size=22, color=BAD)).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(RIGHT * 4.7 + UP * 0.6)
        rank = label(rf"smoothest of the 66: \ number {d['roughness_rank']}", font_size=26, color=TUNE).next_to(key, DOWN, buff=0.5)
        with self.voiceover(
            "Five to seven notes, in steps of two sizes: why does so much of the world's music settle "
            "there? One kind of answer is that such scales are good at something. Take our sixty-six "
            "shapes of seven notes and score each one three ways. <bookmark mark='a'/> Across: how evenly "
            "its notes are spread. Up: how many of its pairs of notes are a fifth apart. Colour: how "
            "smooth all its pairs sound together, by the roughness model of Part 5. "
            "<bookmark mark='b'/> One shape is the most even, has the most fifths, and is the smoothest "
            "of all sixty-six. It is the white keys again. On twelve notes, the three things a scale "
            "might want do not compete. One shape wins all of them."
        ) as vo:
            cols = [x.get_color() for x in dots]
            for x in dots:
                x.set_color(GREY_B)
            self.play(FadeIn(g), FadeIn(key[0]))
            self.play(LaggedStart(*[FadeIn(x, scale=2.0) for x in dots], lag_ratio=0.08), run_time=8.0)
            vo.wait_until("a")
            self.play(*[x.animate.set_color(c_) for x, c_ in zip(dots, cols)], FadeIn(key[1]), FadeIn(key[2]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(ring), FadeIn(tag), FadeIn(rank))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def equal(self):
        d = load("frontier")
        c = clip("frontier.equal")
        card = listen_card(r"A scale, \ and then the start of the Tune in it. \ Is this scale major, \ minor, \ or neither?", width=9.6, font_size=26)
        with self.voiceover(
            "But why unequal steps at all? If evenness is good, seven equal steps would be perfectly "
            "even. Listen to a scale, and then the start of the Tune played in it. Is it major, minor, or "
            "neither?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        bar = step_bar([d["equal_step"]] * 7, width=10.0, height=0.6, colors=(LONG,), font_size=22).move_to(UP * 0.8)
        self.play(FadeOut(card), FadeIn(bar))
        with self.listen(c) as snd:
            window(snd, r"a scale; \ then the Tune's first phrase", detail=r"Part 7's piano, \ retuned", corner=DL, tag_corner=DR)
            t0 = d["starts"][0]
            for j in range(7):
                snd.wait_until(t0 + 0.3 * j)
                self.play(bar.cells[j].animate(rate_func=there_and_back).shift(UP * 0.14), run_time=0.2)
            pulse(snd, bar, d["starts"][1], c.duration - 0.3, buff=0.12)
        facts = VGroup(label(rf"seven equal steps of {d['equal_step']:.0f} cents", font_size=28, color=TUNE),
                       label(rf"its third: \ {d['equal_third']:.0f} cents, \ between minor (300) and major (400)", font_size=26, color=GREY_A),
                       label(rf"its fifth: \ {d['equal_fifth']:.0f} cents, \ 16 flat of pure", font_size=26, color=GREY_A),
                       label(r"every note has the same neighbours: \ no landmark, \ no home", font_size=26, color=EAR)).arrange(DOWN, buff=0.25).move_to(DOWN * 1.5)
        with self.voiceover(
            "Neither. That was seven equal steps to the octave. <bookmark mark='a'/> Its third lies "
            "between a minor and a major third. Its fifth is a little flat. <bookmark mark='b'/> And "
            "something subtler is missing. Every note of an equal scale has exactly the same neighbours "
            "at exactly the same distances. Nothing marks any note as different from the rest. Chapter "
            "four's landmark, the interval that occurs only once, is gone. In 1999 Sandra Trehub and her "
            "colleagues tested babies nine months old on scales they had never heard: one with unequal "
            "steps, one with equal. The babies noticed a mistuned note in the unequal scale, and not in "
            "the equal one. Unequal steps seem to give the ear something to hold on to."
        ) as vo:
            self.play(FadeIn(facts[0]))
            vo.wait_until("a")
            self.play(FadeIn(facts[1]), FadeIn(facts[2]))
            vo.wait_until("b")
            self.play(FadeIn(facts[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reasons(self):
        head = label(r"Four explanations, \ none of them settled", font_size=36, color=LIMIT).to_edge(UP, buff=0.4)
        rows = rows_card([
            (r"memory", r"listeners can keep only about five to nine pitch categories apart; \\ more notes than that, \ and a scale stops being a set of landmarks."),
            (r"unequal steps", r"they tell a listener where in the scale a melody is; \\ infants hear mistunings in unequal scales and not in equal ones."),
            (r"consonance", r"the scales used most are those whose notes agree best with a harmonic series \\ (Gill and Purves, 2009), \ or that pack in the most fifths (McBride and Tlusty)."),
            (r"transmission", r"scales are learned by ear and sung by voices; \ only what survives being \\ passed on, \ imperfectly, \ for generations is still here."),
        ], left=-6.5, text_left=-3.2, top=1.9, step=1.42, name_size=26, text_size=23, color=LIMIT)
        self.play(FadeIn(head), run_time=0.5)
        with self.voiceover(
            "So why five to seven unequal steps? There are at least four explanations, and none is "
            "settled. <bookmark mark='a'/> Memory: people can keep only a handful of categories of pitch "
            "apart, and a scale with too many notes stops being a set of landmarks. <bookmark mark='b'/> "
            "Orientation: unequal steps tell a listener where in the scale a melody is. "
            "<bookmark mark='c'/> Consonance: the scales the world uses most are the ones whose notes "
            "agree best with a harmonic series, or that pack in the most fifths. We saw a version of "
            "that a minute ago. <bookmark mark='d'/> And transmission: scales are passed on by ear and "
            "by voice, and only what survives being copied imperfectly for generations is still with us. "
            "These are not rivals so much as pressures, and they mostly push the same way. Telling them "
            "apart needs scales where they disagree, and people who use them. That work is being done "
            "now, and the answers so far differ from one culture's music to the next."
        ) as vo:
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()
