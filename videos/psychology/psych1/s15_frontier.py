from __future__ import annotations

import numpy as np

from videos.psychology.psych1.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.victorians()
        self.devices()
        self.open_questions()

    def card(self):
        card = chapter_card(14, r"Frontier: \ what is a reaction time measuring?", r"Three things about the oldest "
                            r"measure in psychology that are not settled.", lit=(), part=PART,
                            scale=("neuron", "mind", "person"), marr=("what", "how"))
        with self.voiceover(
            "Chapter fourteen. The frontier: what is a reaction time measuring?"
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def victorians(self):
        d = load("devices")
        w = archive.WOODS_2015.data
        head = heading(r"Were the Victorians faster?")
        unit = 9.4 / 260.0
        x0 = -6.3
        rows = (
            (r"Galton's visitors, London, 1880s", d["galton"], P.ARCHIVE, r"under 190 ms"),
            (rf"{fmt_int(w['n'])} adults, 2015, as recorded", d["woods_raw"], P.HUMAN, rf"{d['woods_raw']:.0f} ms"),
            (r"the same data, minus the hardware's own delay", d["woods_corrected"], STATUS_COLOR["replicated"],
             rf"{d['woods_corrected']:.0f} ms"),
        )
        bars, labs, vals = VGroup(), VGroup(), VGroup()
        for i, (name, ms, color, txt) in enumerate(rows):
            y = 1.55 - 1.6 * i
            b = Rectangle(width=ms * unit, height=0.75, stroke_width=0, fill_color=color, fill_opacity=0.85)
            b.move_to([x0 + ms * unit / 2, y, 0])
            bars.add(b)
            labs.add(label(name, font_size=30, color=color).next_to(b, UP, buff=0.1).align_to(b, LEFT))
            vals.add(label(txt, font_size=36, color=color).next_to(b, RIGHT, buff=0.25))
        delay = Line([x0 + d["woods_corrected"] * unit, bars[1].get_y(), 0], [x0 + d["woods_raw"] * unit,
                                                                              bars[1].get_y(), 0])
        hatch = Rectangle(width=delay.get_length(), height=0.75, stroke_color=P.ERR, stroke_width=2,
                          fill_color=P.ERR, fill_opacity=0.5).move_to(delay)
        h_lab = label(rf"{d['woods_delay']:.0f} ms: \ the display and the button", font_size=24, color=P.ERR)
        h_lab.next_to(hatch, DOWN, buff=0.12)
        chip = status_chip("contested", 26).to_corner(DR, buff=0.5)
        claim = wrapped_label(r"2013: \ simple reaction times have slowed since Galton, so intelligence has "
                              r"declined.", 12.6, 30, GREY_A).to_edge(DOWN, buff=0.8)
        src = published_tag(r"Woodley et al.\ (2013); \ " + archive.WOODS_2015.cite)
        # Galton's clock, in outline: a swinging pendulum, with no screen and no keyboard between it and the hand
        pivot = np.array([5.35, 2.35, 0.0])
        rod = Line(pivot, pivot + DOWN * 2.0, color=P.ARCHIVE, stroke_width=4)
        bob = Circle(radius=0.26, stroke_width=0, fill_color=P.ARCHIVE, fill_opacity=1).move_to(pivot + DOWN * 2.0)
        swing = VGroup(rod, bob).rotate(-0.32, about_point=pivot)
        bracket = Line(pivot + LEFT * 0.55, pivot + RIGHT * 0.55, color=GREY_B, stroke_width=5)
        p_lab = VGroup(label(r"Galton's clock:", font_size=26, color=P.ARCHIVE),
                       label(r"a pendulum", font_size=26, color=P.ARCHIVE)).arrange(DOWN, buff=0.06)
        p_lab.move_to(pivot + DOWN * 2.95)
        sch = note(r"schematic").next_to(p_lab, DOWN, buff=0.1)

        def tick(n=1):
            for _ in range(n):
                self.play(Rotate(swing, 0.64, about_point=pivot), rate_func=there_and_back, run_time=2.2)
        with self.voiceover(
            "In 2013 a paper made headlines with a startling claim. Francis Galton had measured simple reaction "
            "times on thousands of visitors to his London laboratory in the 1880s, and his young adults averaged "
            f"under {d['galton']:.0f} milliseconds. <bookmark mark='a'/> Modern studies report slower times. So, "
            "the authors argued, people have got slower since the Victorians, and since quick reactions go with "
            "high test scores, less intelligent. <bookmark mark='b'/> Two years later a group led by David Woods "
            f"tested {w['n']:,} adults. Their raw average was {d['woods_raw']:.0f} milliseconds. "
            "<bookmark mark='c'/> Then they measured the delays in their own hardware, the time the display "
            "takes to show the stimulus and the button takes to report the press, and subtracted them. "
            f"<bookmark mark='d'/> {d['woods_corrected']:.0f}. Much closer to Galton's subjects, whose "
            "apparatus was a pendulum, with no screen and no keyboard in the loop. <bookmark mark='e'/> "
            "Different instruments, "
            "different numbers. A difference between eras, or between laboratories, or between devices, is "
            "first of all a fact about the apparatus. That's Kant's worry about measurement, turned practical."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), GrowFromEdge(bars[0], LEFT), FadeIn(labs[0]), FadeIn(vals[0]))
            self.play(FadeIn(bracket), FadeIn(swing), FadeIn(p_lab), FadeIn(sch))
            tick(3)
            vo.wait_until("a")
            self.play(FadeIn(claim, shift=UP * 0.15))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1], LEFT), FadeIn(labs[1]), FadeIn(vals[1]))
            vo.wait_until("c")
            self.play(FadeIn(hatch), FadeIn(h_lab))
            vo.wait_until("d")
            self.play(GrowFromEdge(bars[2], LEFT), FadeIn(labs[2]), FadeIn(vals[2]))
            tick(2)
            vo.wait_until("e")
            self.play(FadeOut(claim), FadeIn(chip, scale=1.2))
        self.clear_scene()

    def devices(self):
        d = load("devices")
        rows = d["rows"]
        head = heading(r"One person, three devices")
        names = {"calibrated": r"a calibrated rig", "laptop": r"a laptop", "phone": r"a phone"}
        unit = 0.0185
        x0 = -3.4
        g = VGroup()
        diffs = VGroup()
        for i, r in enumerate(rows):
            y = 1.7 - 1.65 * i
            nm = VGroup(label(names[r["device"]], font_size=32, color=WHITE),
                        label(rf"delay {r['lag']:.0f} ms", font_size=24, color=P.ERR)).arrange(DOWN, buff=0.06,
                                                                                               aligned_edge=RIGHT)
            nm.move_to([x0 - 0.3 - nm.width / 2, y, 0])
            simple = Rectangle(width=r["simple"] * unit, height=0.4, stroke_width=0, fill_color=METHOD["a"],
                               fill_opacity=0.85).move_to([x0 + r["simple"] * unit / 2, y + 0.22, 0])
            choice = Rectangle(width=r["choice"] * unit, height=0.4, stroke_width=0, fill_color=METHOD["b"],
                               fill_opacity=0.85).move_to([x0 + r["choice"] * unit / 2, y - 0.22, 0])
            lag = Rectangle(width=max(r["lag"] * unit, 0.001), height=0.84, stroke_width=0, fill_color=P.ERR,
                            fill_opacity=0.55).move_to([x0 + r["lag"] * unit / 2, y, 0])
            s_val = MathTex(rf"{r['simple']:.0f}", font_size=30, color=METHOD["a"]).next_to(simple, RIGHT, buff=0.12)
            c_val = MathTex(rf"{r['choice']:.0f}", font_size=30, color=METHOD["b"]).next_to(choice, RIGHT, buff=0.12)
            br = Line([simple.get_right()[0], y - 0.52, 0], [choice.get_right()[0], y - 0.52, 0], color=P.ACCENT,
                      stroke_width=4)
            dv = MathTex(rf"{r['difference']:.0f}", font_size=32, color=P.ACCENT).next_to(br, DOWN, buff=0.06)
            g.add(VGroup(nm, simple, choice, lag, s_val, c_val))
            diffs.add(VGroup(br, dv))
        leg = legend([(METHOD["a"], r"simple reaction (ms)"), (METHOD["b"], r"choice reaction (ms)"),
                      (P.ACCENT, r"choice minus simple")], font_size=22).to_corner(UR, buff=0.5).shift(DOWN * 0.7)
        moral = label(r"A constant delay moves every time, and no difference.", font_size=34, color=P.ACCENT)
        moral.to_edge(DOWN, buff=0.55)
        tag = simulated_tag(r"simulated: one person of the Pool; \ the delays are illustrative")
        with self.voiceover(
            "This matters to you, because the experiments on our course site run in your browser, on your "
            "screen, and a phone is not a laboratory. <bookmark mark='a'/> Here is one person from the Pool, "
            "measured on three devices with different delays. The averages move by tens of milliseconds. Compare "
            "two people on different devices, and you're comparing the devices. <bookmark mark='b'/> But look at "
            "the difference between the choice and the simple reaction. It doesn't move at all, because a "
            "constant delay subtracts out. <bookmark mark='c'/> That's Donders' trick, working for us. So the "
            "site reports differences and slopes, and it tells you that it can't vouch for absolute times."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(leg[:2]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in g], lag_ratio=0.5), run_time=4.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in diffs], lag_ratio=0.4), FadeIn(leg[2]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(moral, shift=UP * 0.15))
        self.clear_scene()

    def open_questions(self):
        head = heading(r"What is open")
        items = (
            (r"Is there one mental speed?", r"People quick at one task tend to be quick at others, and speed goes "
             r"with test scores. \ One cause, or many? \ (Part 32)"),
            (r"Are there stages at all?", r"A cascade, in which every level passes on partial results "
             r"continuously, can mimic additive factors (McClelland 1979)."),
            (r"What is the shape telling us?", r"The best current answer: \ deciding is an accumulation of noisy "
             r"evidence to a threshold. \ (Part 25)"),
        )
        rows = VGroup()
        for i, (q, a) in enumerate(items, 1):
            num = label(rf"{i}", font_size=52, color=P.ACCENT)
            body = VGroup(label(q, font_size=40, color=WHITE), wrapped_label(a, 11.6, 29, GREY_A))
            body.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            rows.add(VGroup(num, body).arrange(RIGHT, buff=0.4, aligned_edge=UP))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(head, DOWN, buff=0.35)
        star = VGroup(label(r"$\star$ \ Research problem", font_size=28, color=P.ACCENT),
                      wrapped_label(r"Design an experiment on Battery task 1 whose reaction-time \emph{distributions} "
                                    r"would separate discrete stages from a cascade. \ What must each model "
                                    r"predict that the other cannot?", 12.4, 27, WHITE))
        star.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        box = SurroundingRectangle(star, color=P.ACCENT, buff=0.22, corner_radius=0.12, stroke_width=2)
        sp = VGroup(box, star).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Three things are open. <bookmark mark='a'/> One. Is there a single mental speed, a general "
            "quickness that runs through every task? People who are fast at one thing tend to be fast at others, "
            "and speed goes with test scores. Whether that's one cause or many is unsettled, and Part 32 comes "
            "back to it. <bookmark mark='b'/> Two. Are there stages at all? In 1979 James McClelland showed that "
            "a cascade, where every level passes partial results forward continuously, can imitate the additive "
            "patterns that were supposed to prove separate stages. <bookmark mark='c'/> And three: the question "
            "from the start of this part. What is the shape of a reaction-time distribution telling us? The "
            "best current answer is that a decision is an accumulation of noisy evidence up to a threshold, and "
            "that's Part 25. <bookmark mark='d'/> This part's research problem sits between the last two. Design "
            "an experiment whose reaction-time distributions would tell stages from a cascade."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abc", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r, shift=LEFT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(sp, shift=UP * 0.2))
        self.clear_scene()
