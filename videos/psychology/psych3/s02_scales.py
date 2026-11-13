from __future__ import annotations

from videos.psychology.psych3.common import *  # noqa: F403

# scale -> (what the numbers record, what may be done to them, what still means something, an example)
ROWS = [
    ("nominal", r"which class", r"relabel freely", r"counts, \ the mode", r"shirt numbers"),
    ("ordinal", r"which is more", r"stretch, keeping order", r"the median", r"finishing places"),
    ("interval", r"how much more", r"$x' = ax + b$", r"the mean, \ the SD", r"degrees Celsius"),
    ("ratio", r"how many times", r"$x' = ax$", r"ratios: \ ``twice as''", r"length, \ time"),
]


class Scales(VoiceoverScene):
    def construct(self):
        self.card()
        self.rule()
        self.twice()
        self.ratings()
        self.sums()

    def card(self):
        card = chapter_card(1, r"What a number survives", r"What may you do to a number without losing what it records?",
                            lit={1946: r"Stevens's four scales"}, part=PART, scale=("person",), marr=("what",))
        with self.voiceover(
            "Chapter one. What a number survives."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def rule(self):
        d = archive.STEVENS_1946.data
        hc = history_card(1946, r"S. S. Stevens, Harvard", r"measurement is ``the assignment of numerals to objects "
                          r"or events according to rules''", color=P.ARCHIVE, width=8.6, font_size=26)
        hc.to_edge(UP, buff=0.35)
        cols = [-6.7, -4.85, -1.75, 1.45, 4.45]
        heads = VGroup(*[label(t, font_size=24, color=GREY_B).move_to([x, 1.25, 0], aligned_edge=LEFT) for x, t in zip(
            cols, [r"scale", r"the numbers record", r"you may", r"what still means", r"for example"])])
        rows = VGroup()
        for i, (name, rec, may, keep, ex) in enumerate(ROWS):
            y = 0.4 - 0.95 * i
            c = SCALE[name]
            row = VGroup(label(name, font_size=36, color=c), label(rec, font_size=30, color=WHITE),
                         label(may, font_size=30, color=c), label(keep, font_size=30, color=WHITE),
                         label(ex, font_size=28, color=GREY_A))
            for cell, x in zip(row, cols):
                cell.move_to([x, y, 0], aligned_edge=LEFT)
            rows.add(row)
        more = label(r"each scale keeps everything the ones above it keep", font_size=26, color=GREY_B)
        more.to_edge(DOWN, buff=0.45).shift(RIGHT * 2.2)
        src = historical_tag(archive.STEVENS_1946.cite + r", Table 1")
        assert set(d["scales"]) == {r[0] for r in ROWS}
        with self.voiceover(
            "The reply came from the man whose loudness scale was on trial: Stanley Stevens, at Harvard. "
            "<bookmark mark='a'/> He began by giving up the argument about addition. Call measurement the "
            "assignment of numbers to things according to a rule, any rule. Then the question is no longer "
            "whether you have measured. It's what kind of rule you used, and so what you're allowed to do with "
            "the numbers afterwards. <bookmark mark='b'/> There are four kinds. On a nominal scale the numbers "
            "are names, like the numbers on football shirts. You could swap them around and lose nothing, so all "
            "you may do is count. <bookmark mark='c'/> On an ordinal scale the numbers record an order, like "
            "finishing places in a race. You could stretch or squeeze them any way that keeps the order, so the "
            "median means something and the mean doesn't. <bookmark mark='d'/> On an interval scale equal "
            "differences mean equal amounts, as with degrees Celsius. You may change the unit and move the zero, "
            "and now means and standard deviations are meaningful. <bookmark mark='e'/> And on a ratio scale "
            "the zero is real, as with length or time. You may only change the unit. Only here can you say that "
            "one thing is twice another."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(heads))
            for m, row in zip("bcde", rows):
                vo.wait_until(m)
                self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.12) for c in row], lag_ratio=0.25), run_time=2.2)
            self.play(FadeIn(more))
        self.clear_scene()

    def twice(self):
        head = heading(r"The test: \ does the statement survive a permitted change?")

        def line(values, labels, color, y, x0, length, lo, hi):
            ax = Line([x0, y, 0], [x0 + length, y, 0], color=GREY_B, stroke_width=2)
            g = VGroup(ax)
            for v, t in zip(values, labels):
                x = x0 + length * (v - lo) / (hi - lo)
                g.add(Line([x, y - 0.12, 0], [x, y + 0.12, 0], color=color, stroke_width=4))
                g.add(label(t, font_size=26, color=color).move_to([x, y + 0.42, 0]))
            return g

        # temperature: an interval scale
        t_head = label(r"temperature", font_size=32, color=SCALE["interval"]).move_to([-3.6, 2.2, 0])
        c_line = line([10, 20], [r"$10^\circ$C", r"$20^\circ$C"], SCALE["interval"], 1.2, -6.0, 4.8, 0, 25)
        f_line = line([50, 68], [r"$50^\circ$F", r"$68^\circ$F"], SCALE["interval"], -0.1, -6.0, 4.8, 32, 77)
        t_say = VGroup(label(r"``twice as hot''", font_size=30, color=WHITE),
                       label(r"$20/10 = 2$ \ \ but \ \ $68/50 = 1.36$", font_size=28, color=ERRC),
                       label(r"does not survive: \ it says nothing", font_size=26, color=ERRC))
        t_say.arrange(DOWN, buff=0.14).move_to([-3.6, -1.55, 0])
        # reaction time: a ratio scale
        r_head = label(r"reaction time", font_size=32, color=SCALE["ratio"]).move_to([3.6, 2.2, 0])
        ms_line = line([200, 400], [r"200 ms", r"400 ms"], SCALE["ratio"], 1.2, 1.2, 4.8, 0, 500)
        s_line = line([0.2, 0.4], [r"0.2 s", r"0.4 s"], SCALE["ratio"], -0.1, 1.2, 4.8, 0, 0.5)
        r_say = VGroup(label(r"``twice as long''", font_size=30, color=WHITE),
                       label(r"$400/200 = 2$ \ \ and \ \ $0.4/0.2 = 2$", font_size=28, color=TRUE),
                       label(r"survives: \ it is a fact about the two times", font_size=26, color=TRUE))
        r_say.arrange(DOWN, buff=0.14).move_to([3.6, -1.55, 0])
        rule = label(r"A statement about numbers means something only if every permitted change of scale leaves "
                     r"it true.", font_size=28, color=P.ACCENT).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "This gives a test you can apply to any sentence with a number in it. Change the scale in a way "
            "that's allowed, and see whether the sentence is still true. <bookmark mark='a'/> Today it's twenty "
            "degrees Celsius, and yesterday it was ten. Was today twice as hot? <bookmark mark='b'/> Put the same "
            "two days in Fahrenheit: sixty-eight and fifty. The ratio is now one point three six. Nothing about "
            "the weather changed, only the scale, and the claim came out false. So it wasn't a claim about the "
            "weather. <bookmark mark='c'/> Now a reaction time of four hundred milliseconds against one of two "
            "hundred. <bookmark mark='d'/> In seconds: point four against point two. Still twice. That "
            "sentence is about the two reactions. <bookmark mark='e'/> This is Stevens's answer to the committee. "
            "Don't ask whether a number is a measurement. Ask which sentences about it survive. For a rating of "
            "loudness, or of anything else, that becomes a question you can investigate."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(t_head), FadeIn(c_line), FadeIn(t_say[0]))
            vo.wait_until("b")
            self.play(FadeIn(f_line, shift=DOWN * 0.2))
            self.play(FadeIn(t_say[1]), FadeIn(t_say[2]))
            vo.wait_until("c")
            self.play(FadeIn(r_head), FadeIn(ms_line), FadeIn(r_say[0]))
            vo.wait_until("d")
            self.play(FadeIn(s_line, shift=DOWN * 0.2))
            self.play(FadeIn(r_say[1]), FadeIn(r_say[2]))
            vo.wait_until("e")
            self.play(FadeIn(rule, shift=UP * 0.15))
        self.clear_scene()

    def ratings(self):
        d = load("scales")
        s, c = d["shifted"], d["crossed"]
        head = heading(r"May you average ratings?")
        item = label(r"``I enjoyed this course.'' \ \ 1 strongly disagree \ \dots\ 5 strongly agree", font_size=26,
                     color=GREY_A).next_to(head, DOWN, buff=0.22)

        def case(x, title, pa, pb, lines):
            a = rating_bars(pa, GROUP_A, width=2.9, height=1.55, font_size=22)
            b = rating_bars(pb, GROUP_B, width=2.9, height=1.55, font_size=22)
            pair = VGroup(a, b).arrange(RIGHT, buff=0.5)
            names = VGroup(label(r"class A", font_size=24, color=GROUP_A).next_to(a, UP, buff=0.12),
                           label(r"class B", font_size=24, color=GROUP_B).next_to(b, UP, buff=0.12))
            t = label(title, font_size=30, color=WHITE)
            text = VGroup(*lines).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
            g = VGroup(t, VGroup(pair, names), text).arrange(DOWN, buff=0.28)
            g.move_to([x, -0.95, 0])
            g.title, g.plot, g.text = t, g[1], text
            return g

        # the five answers on a line, first equally spaced, then not: nobody has shown which spacing is right
        even = [-3.0, -1.5, 0.0, 1.5, 3.0]
        uneven = [[-3.0, -0.4, 0.3, 1.2, 3.0], [-3.0, -2.4, -1.5, 1.0, 3.0], even]
        words = [r"strongly disagree", r"disagree", r"neither", r"agree", r"strongly agree"]
        strip_line = Line([-3.6, 0.2, 0], [3.6, 0.2, 0], color=GREY_B, stroke_width=2)
        knobs = VGroup(*[VGroup(Circle(radius=0.3, color=P.ACCENT, stroke_width=3, fill_color=BACKGROUND, fill_opacity=1),
                                label(rf"{i + 1}", font_size=30, color=P.ACCENT)).move_to([x, 0.2, 0])
                         for i, x in enumerate(even)])
        ends = VGroup(label(words[0], font_size=24, color=GREY_A).next_to(knobs[0], DOWN, buff=0.2),
                      label(words[4], font_size=24, color=GREY_A).next_to(knobs[4], DOWN, buff=0.2))
        ask = label(r"is the step from 1 to 2 as big as the step from 4 to 5?", font_size=30, color=WHITE)
        ask.move_to([0, -1.4, 0])
        strip = VGroup(strip_line, knobs, ends, ask)
        left = case(-3.6, r"one class answers higher throughout", s["pa"], s["pb"], [
            label(rf"means: \ {s['mean_a']:.2f} against {s['mean_b']:.2f}", font_size=28, color=WHITE),
            label(r"respace the answers, keeping their order:", font_size=24, color=GREY_A),
            label(rf"A stays ahead in all {fmt_int(20000)} tries", font_size=28, color=TRUE),
        ])
        right = case(3.6, r"one class in the middle, one at the ends", c["pa"], c["pb"], [
            label(rf"means: \ {c['mean_a']:.2f} against {c['mean_b']:.2f}", font_size=28, color=WHITE),
            label(rf"count answer 1 as $-1$: \ {c['stretched_a']:.2f} against {c['stretched_b']:.2f}",
                  font_size=24, color=ERRC),
            label(rf"the order reverses in {100 * c['flip_share']:.0f}\% of tries", font_size=28, color=ERRC),
        ])
        tag = simulated_tag()
        with self.voiceover(
            "Now the quarrel this started, which is still going. A rating scale gives you an order: agree is more "
            "than disagree. Nobody has shown that the step from one to two is as big as the step from four to "
            "five. So by Stevens's rule you shouldn't average ratings at all. And yet everybody does. Who's right? "
            "We can compute when it matters. <bookmark mark='a'/> Two classes rate a course. In the first case, "
            "class A simply answers higher, all the way along the scale. "
            f"<bookmark mark='b'/> Their means are {s['mean_a']:.1f} and {s['mean_b']:.1f}. Now respace the five "
            "answers at random, in any way that keeps their order, twenty thousand times. Class A stays ahead "
            "every time. The mean was safe, because the conclusion didn't depend on the spacing. "
            "<bookmark mark='c'/> In the second case class A sits in the middle of the scale, and class B is "
            "split between the two ends. <bookmark mark='d'/> With the usual spacing, B's mean is a little "
            "higher. But count strongly disagree as a bigger step down than the others, and A's mean is higher. "
            f"Across random spacings, the order reverses {100 * c['flip_share']:.0f} per cent of the time. Here "
            "the comparison of means is a fact about the spacing you happened to choose."
        ) as vo:
            self.play(FadeIn(head), FadeIn(item), FadeIn(tag))
            self.play(FadeIn(strip_line), FadeIn(knobs, lag_ratio=0.15), FadeIn(ends), run_time=1.5)
            self.wait(4.0)
            self.play(FadeIn(ask))
            for xs in uneven:
                self.play(*[k.animate.move_to([x, 0.2, 0]) for k, x in zip(knobs, xs)], run_time=1.6)
                self.wait(0.6)
            vo.wait_until("a")
            self.play(FadeOut(strip), FadeIn(left.title), FadeIn(left.plot))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in left.text], lag_ratio=0.6), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(right.title), FadeIn(right.plot))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in right.text], lag_ratio=0.6), run_time=4.0)
        self.clear_scene()

    def sums(self):
        d = load("scales")
        head = heading(r"When it matters, and when it does not")
        rule = VGroup(
            label(r"the order of two means can be reversed by respacing", font_size=30, color=WHITE),
            label(r"exactly when the two groups' answers cross:", font_size=30, color=WHITE),
            label(r"neither group answers higher all the way along the scale", font_size=30, color=P.ACCENT),
        ).arrange(DOWN, buff=0.15).move_to([0, 1.75, 0])
        tiles = VGroup()
        for big, small, color in ((r2(d["sum_r_median"]), r"a ten-item sum, respaced at random: \ its typical "
                                   r"correlation with the plain sum", TRUE),
                                  (r2(d["sum_r_p05"]), r"the same, for the worst twentieth of the respacings",
                                   SCALE["interval"])):
            num = label(big, font_size=64, color=color)
            cap = wrapped_label(small, 4.6, 24, GREY_A)
            tiles.add(VGroup(num, cap).arrange(DOWN, buff=0.18))
        tiles.arrange(RIGHT, buff=1.2, aligned_edge=UP).move_to([0, -0.75, 0])
        end = label(r"Sums of many items are forgiving. \ One item, in groups that differ in spread, is not.",
                    font_size=28, color=WHITE).to_edge(DOWN, buff=0.7)
        tag = simulated_tag()
        with self.voiceover(
            "So there's a clean answer, and it isn't either side's slogan. <bookmark mark='a'/> The order of two "
            "means can be reversed by respacing the scale exactly when the two sets of answers cross: when "
            "neither group answers higher all the way along. If one group is simply shifted up, average away. "
            "If the groups differ in spread, look at the whole distribution before you believe a difference in "
            "means. <bookmark mark='b'/> And most psychological scores aren't single ratings. They're sums of "
            "many items. Take a ten-item scale, respace its answers at random, and the new total correlates "
            f"{d['sum_r_median']:.2f} with the old one in the typical case, <bookmark mark='c'/> and "
            f"about {d['sum_r_p05']:.2f} in the worst twentieth. <bookmark mark='d'/> Sums are "
            "forgiving. That's the practical reason the field treats them as interval scales. It's a "
            "reason, not a proof, and we'll come back to what it leaves out at the frontier."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in rule], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(tiles[0], shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(tiles[1], shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(end))
        self.clear_scene()
