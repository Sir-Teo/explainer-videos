from __future__ import annotations

import numpy as np

from videos.psychology.psych7.common import *  # noqa: F403


class Networks(VoiceoverScene):
    def construct(self):
        self.card()
        self.answer()
        self.ten()

    def card(self):
        card = chapter_card(11, r"One place, or everywhere?", r"What is today's answer?", lit=(), part=PART,
                            scale=("brain",), marr=("how", "tissue"))
        with self.voiceover(
            "Chapter eleven. One place, or everywhere?"
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def answer(self):
        head = heading(r"Neither camp was right, \ and both were")
        brain = brain_side(6.0, fill=0.14).move_to([-3.7, 0.2, 0])
        nets = [
            (THRESH, [(-0.36, -0.02), (0.22, 0.06), (0.05, -0.25)], r"speech and language"),
            (PARIETAL, [(-0.5, 0.4), (0.3, 0.5), (0.45, 0.25)], r"attending"),
            (OCCIPITAL, [(0.75, 0.05), (0.4, -0.2), (0.6, 0.3)], r"seeing"),
        ]
        drawn = VGroup()
        for col, pts, _ in nets:
            ps = [at(brain, x, y) for x, y in pts]
            g = VGroup(*[Line(ps[i], ps[j], color=col, stroke_width=4) for i in range(len(ps)) for j in range(i + 1, len(ps))],
                       *[Dot(p_, radius=0.11, color=col) for p_ in ps])
            drawn.add(g)
        lg = legend([(col, name) for col, _, name in nets], font_size=22).next_to(brain, DOWN, buff=0.15)
        rows = VGroup(
            wrapped_label(r"specialized: \ a small region can be needed for one thing and not for another "
                          r"(Broca, H.M., the maps)", 6.0, 29, WHITE),
            wrapped_label(r"connected: \ every task uses several regions and the cables between them; \ cut a "
                          r"cable and the task fails", 6.0, 29, WHITE),
            wrapped_label(r"redundant: \ most tasks can be done more than one way, \ so damage is often "
                          r"partly made good (Lashley's maze)", 6.0, 29, WHITE),
            wrapped_label(r"The unit is a network. \ A lesion finds a part the network needs.", 6.0, 31, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to([3.6, -0.2, 0])
        keep_in_frame(rows)
        tag = note(r"schematic: the dots are not anatomy").to_corner(DR, buff=0.2)
        with self.voiceover(
            "So, one place or everywhere? After a hundred and sixty years of patients, here's where the "
            "evidence has settled. <bookmark mark='a'/> The brain is specialized. A small region can be "
            "needed for one thing and not for another. Broca's patients, H.M. and the maps all say so, and "
            "Flourens was wrong. <bookmark mark='b'/> And it's connected. No task we've looked at is done "
            "by one region. Speech needed a front box, a back box and a pathway. Cut the pathway, and a "
            "task fails though every box is intact. <bookmark mark='c'/> And it's redundant. Most real "
            "tasks can be done more than one way, which is why Lashley's rats kept finding the food, and "
            "why people recover part of what a stroke takes. <bookmark mark='d'/> So the unit isn't a "
            "place, and it isn't the whole. It's a network of specialized parts. What a lesion finds is "
            "one part that the network can't do without. That's a narrower claim than this is where "
            "speech lives, and it's the one the evidence supports."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(brain))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(g) for g in drawn], lag_ratio=0.5), FadeIn(lg), FadeIn(rows[1]),
                      run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def ten(self):
        t = load("tour")
        head = heading(r"``We only use ten percent of our brains''")
        bars = VGroup()
        data = [(r"the brain's share of your weight", t["mass_share"], VOLT),
                (r"its share of your energy", t["energy_share"], LESION)]
        for i, (name, v, col) in enumerate(data):
            y = 1.5 - 1.0 * i
            bar = Rectangle(width=22.0 * v, height=0.5, stroke_width=0, fill_color=col, fill_opacity=0.9)
            bar.move_to([-6.2 + 11.0 * v, y, 0])
            bars.add(VGroup(bar, label(rf"{name}: \ {pct(v)}", font_size=27, color=col).next_to(bar, RIGHT, buff=0.2)))
        rows = VGroup(
            wrapped_label(rf"A tissue that costs {t['times_fair_share']:.0f} times its share is not kept "
                          r"nine-tenths idle.", 12.4, 29, WHITE),
            wrapped_label(rf"If a tenth did all the work, \ that tenth would be burning "
                          rf"{t['tenth_times_fair_share']:.0f} times its share.", 12.4, 29, WHITE),
            wrapped_label(r"And no lesion is free: \ damage almost anywhere costs something. \ This part has been "
                          r"a list of what.", 12.4, 29, WHITE),
            wrapped_label(r"The myth probably began as a misreading of William James, \ who said we use a small "
                          r"part of our \emph{resources}.", 12.4, 27, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([0, -1.4, 0])
        src = published_tag(archive.RAICHLE_2002.cite)
        myth = big_number(r"10\%", r"of the brain in use, \ says the myth", LESION, 96, width=4.4, cap_size=28)
        myth.move_to([4.5, 1.15, 0])
        with self.voiceover(
            "Which brings us to the best-known thing that people believe about the brain: that we use only "
            "ten percent of it. Recall two numbers from the tour. <bookmark mark='a'/> The brain is two "
            "percent of your weight, and it uses twenty percent of your energy. <bookmark mark='b'/> No "
            f"body pays {t['times_fair_share']:.0f} times the going rate, every hour of its life, for a "
            "tissue that sits nine-tenths idle. <bookmark mark='c'/> And if a tenth of it were doing all "
            f"the work, that tenth would be burning energy at {t['tenth_times_fair_share']:.0f} times the "
            "body's average rate, which no tissue does. <bookmark mark='d'/> Then there's the evidence of "
            "this whole part. If nine-tenths were spare, most damage would cost nothing. Instead, damage "
            "almost anywhere costs something, and we've spent an hour listing what. <bookmark mark='e'/> The "
            "myth seems to have started as a misreading of William James, who wrote that people use only a "
            "small part of their mental resources. He meant effort. He didn't mean tissue."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            self.play(FadeIn(myth, scale=1.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.15) for b in bars], lag_ratio=0.7), run_time=3.0)
            for k, mark_ in enumerate("bcde"):
                vo.wait_until(mark_)
                self.play(FadeIn(rows[k], shift=UP * 0.1))
        self.clear_scene()
