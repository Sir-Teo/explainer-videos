from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs61.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


class Hook(VoiceoverScene):
    def construct(self):
        self.same_program()
        self.where()
        self.plan()

    def same_program(self):
        b = load("bias")
        env = b["env"]
        head = label(r"The same program, \ timed again and again", font_size=36).to_edge(UP, buff=0.3)
        lo = min(r["median"] for r in env)
        hi = max(r["median"] for r in env)
        ax = Axes(x_range=[0, 4096, 1024], y_range=[lo * 0.9, hi * 1.08, (hi - lo) / 3], x_length=10.0,
                  y_length=4.2, axis_config={"color": GREY_D, "include_numbers": False}).next_to(head, DOWN, buff=0.5)
        xt = VGroup(*[label(rf"{v:,}", font_size=16, color=GREY_B).next_to(ax.c2p(v, lo * 0.9), DOWN, buff=0.1)
                      for v in (0, 1024, 2048, 3072, 4096)])
        xl = label(r"bytes added to the environment", font_size=18, color=GREY_A).next_to(ax, DOWN, buff=0.45)
        yt = VGroup(*[label(rf"{v:.3f}", font_size=16, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.12)
                      for v in (lo, (lo + hi) / 2, hi)])
        yl = label(r"seconds", font_size=18, color=GREY_A).next_to(yt, UP, buff=0.25).align_to(yt, RIGHT)
        dots = VGroup(*[Dot(ax.c2p(r["bytes"], r["median"]), radius=0.06, color=HEAD) for r in env])
        line = VMobject(color=HEAD, stroke_width=1.5).set_points_as_corners([d.get_center() for d in dots])
        spread = label(rf"spread of the medians: \ {100 * b['env_spread']:.0f}\%", font_size=22, color=NO).next_to(
            ax, UP, buff=0.05).align_to(ax, RIGHT)
        foot = wrapped_label(r"one C program, \ compiled once; \ only an unused environment variable changes \ "
                             r"(after Mytkowicz, \ Diwan, \ Hauswirth and Sweeney, \ 2009)", 12.4, font_size=19,
                             color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is one C program, compiled once, timed on this machine. <bookmark mark='a'/> The only thing we "
            "change between runs is the size of an environment variable the program never reads, from nothing to "
            "four kilobytes. <bookmark mark='b'/> The median time moves by up to "
            f"{100 * b['env_spread']:.0f} percent. In 2009 Todd Mytkowicz and colleagues showed that such changes "
            "shift where the stack begins, and with it the alignment of hot data, and that this alone could swing a "
            "program's speed by a third. <bookmark mark='c'/> But is our spread that effect, or only noise? This machine "
            "randomizes where the stack begins on every run, which smears the effect out, and chapter two will show "
            "that noise alone could explain what we see. Telling the two apart, and not fooling yourself, is what "
            "this part is about."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.08), run_time=3)
            vo.wait_until("b")
            self.play(Create(line), FadeIn(spread))
            vo.wait_until("c")
            self.play(Indicate(spread, color=HEAD))
        self.wait(0.4)
        self.clear_scene()

    def where(self):
        head = label(r"Where do results come from?", font_size=36).to_edge(UP, buff=0.3)
        steps = VGroup()
        for t, d, c in ((r"a question", r"sharp enough that an answer could be wrong", HEAD),
                        (r"a method", r"a proof, \ a measurement, \ a construction", DATA),
                        (r"evidence", r"that would convince a sceptic who wants you to be wrong", YES),
                        (r"a paper", r"the argument, \ written so that others can check it", LAM)):
            r = RoundedRectangle(width=2.9, height=2.0, corner_radius=0.15, stroke_color=c, stroke_width=2,
                                 fill_color=BG, fill_opacity=1)
            g = VGroup(label(t, font_size=24, color=c), wrapped_label(d, 2.6, font_size=17, color=GREY_A)).arrange(
                DOWN, buff=0.2).move_to(r)
            steps.add(VGroup(r, g))
        steps.arrange(RIGHT, buff=0.45).move_to(UP * 0.4)
        arrows = VGroup(*[Arrow(steps[i].get_right(), steps[i + 1].get_left(), buff=0.05, color=GREY_C,
                                stroke_width=2) for i in range(3)])
        foot = wrapped_label(r"this series has quoted a thousand results; \ each one went through these four steps, "
                             r"\ and most of them could have gone wrong at any of them", 12.4, font_size=21,
                             color=WHITE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "This series has quoted perhaps a thousand results. Where do they come from? <bookmark mark='a'/> Every "
            "one began as a question sharp enough that an answer could be wrong. <bookmark mark='b'/> Then a method: "
            "a proof, a measurement, or something built. <bookmark mark='c'/> Then evidence good enough to convince "
            "a sceptic who wants you to be wrong. <bookmark mark='d'/> And a paper, written so that others can check "
            "it. This last part is about doing that yourself."
        ) as vo:
            self.play(FadeIn(head))
            for mk, i in zip("abcd", range(4)):
                vo.wait_until(mk)
                anims = [FadeIn(steps[i], shift=UP * 0.15)]
                if i:
                    anims.append(GrowArrow(arrows[i - 1]))
                self.play(*anims)
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Doing Research", font_size=36).to_edge(UP, buff=0.3)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"measurement bias, \ reproduced on this machine",
            r"rigorous timing: \ intervals, \ repetitions, \ geometric means",
            r"benchmarks, \ reproducibility and p-hacking",
            r"proof and computer search as research",
            r"reading, \ reviewing, \ finding problems, \ writing",
            r"the open-problems map, \ and the tower one last time",
        ], font_size=25).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 61 of Computer Science, Built, the last part of the series. <bookmark mark='a'/> We will "
            "reproduce measurement bias; time things rigorously, with intervals and repetitions; see how benchmarks "
            "fail; use proof and computer search to settle conjectures, or at least their small cases; learn to "
            "read, review, find problems and write; and gather the open problems the series met onto one map."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()


_ = (BG, DATA, KERN, LAM, NO, YES)
