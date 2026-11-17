from __future__ import annotations

from videos.psychology.psych36.common import *  # noqa: F403


class System(VoiceoverScene):
    def construct(self):
        self.card()
        self.ladder()
        self.limits()

    def card(self):
        card = chapter_card(11, r"From bias to system", r"How do small biases add up?", lit=(), part=PART,
                            scale=("group", "society"), marr=("what",))
        with self.voiceover("Chapter eleven. From bias to system."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def ladder(self):
        d = load("ladder")
        head = heading(r"Eight rungs of a ladder")
        A = axes([1, 8], [0.2, 0.5], x_length=5.6, y_length=3.6, xticks=[1, 2, 3, 4, 5, 6, 7, 8],
                 yticks=[0.2, 0.3, 0.4, 0.5], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%",
                 xlabel=r"level", ylabel=r"the other group's share", center=[-3.2, -0.3, 0], font_size=15)
        lv = np.arange(1, 9)
        cs = VGroup(*[curve(A.ax, lv, d[k], c) for k, c in (("a05", IN), ("a10", PERSON), ("a20", OUTG))])
        key = legend([(IN, r"advantage 0.05 SD"), (PERSON, r"0.1 SD"), (OUTG, r"0.2 SD")], font_size=14).move_to(
            A.ax.c2p(2.6, 0.27))
        rows = rows_of([
            (r"Psyche's ladder: \ at each of eight levels, \ everyone is scored afresh and the top half moves up; "
             r"\ the two groups start equal", WHITE),
            (r"one group gets a small advantage in every score: \ a tenth of a standard deviation, \ invisible in "
             r"any single decision", PERSON),
            (rf"by the top level the other group's share has fallen from 50\% to {pct(d['a10'][-1])}", OUTG),
            (r"no single evaluator is much biased; \ the system is, \ because small biases compound over "
             r"repeated selections", YOU),
        ], 6.0, 20, 0.36).move_to([3.4, -0.3, 0])
        tag = psyche_tag(r"\texttt{social.pipeline}")
        with self.voiceover(
            "The last idea is the simplest, and it's arithmetic. <bookmark mark='a'/> Psyche's ladder has eight "
            "levels. At each one, everyone is scored afresh, and the top half moves up. The two groups start "
            "equal. <bookmark mark='b'/> One group gets a small advantage in every score, a tenth of a standard "
            "deviation, invisible in any single decision. <bookmark mark='c'/> By the top level, the other group's "
            f"share has fallen from fifty percent to {spct(d['a10'][-1])}. <bookmark mark='d'/> No single "
            "evaluator is much biased. The system is, because small biases compound over repeated selections."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cs[1]), FadeIn(rows[1]), run_time=2)
            vo.wait_until("c")
            self.play(Create(cs[0]), Create(cs[2]), FadeIn(key), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def limits(self):
        head = heading(r"The limits of individual explanation")
        left = VGroup(word_chip(r"in a person", color=PERSON, font_size=22, width=5.2),
                      wrapped_label(r"an IAT score; \ a stereotype; \ a moment's favouritism for a group label", 5.2,
                                    20, WHITE),
                      wrapped_label(r"small, \ noisy, \ hard to change, \ weakly tied to behaviour", 5.2, 20, GREY_A)
                      ).arrange(DOWN, buff=0.3)
        right = VGroup(word_chip(r"in a system", color=OUTG, font_size=22, width=5.2),
                       wrapped_label(r"callbacks over 25 years; \ a ladder of selections; \ norms that people think "
                                     r"others hold", 5.2, 20, WHITE),
                       wrapped_label(r"large, \ stable, \ measurable as behaviour, \ and changeable by design", 5.2,
                                     20, GOOD)).arrange(DOWN, buff=0.3)
        VGroup(left, right).arrange(RIGHT, buff=0.9, aligned_edge=UP).move_to([0, 0.5, 0])
        foot = wrapped_label(r"the psychology of individuals explains how bias starts; \ measuring and changing it "
                             r"often happens at the level of decisions, \ rules and norms", 12.0, 21, YOU).to_edge(
            DOWN, buff=0.8)
        with self.voiceover(
            "Put the part together. <bookmark mark='a'/> In a person, bias shows up as an IAT score, a stereotype, "
            "a moment's favouritism for a label. These are small, noisy, hard to change, and weakly tied to "
            "behaviour. <bookmark mark='b'/> In a system, it shows up as callbacks over twenty-five years, a ladder "
            "of selections, norms that people think others hold. These are large, stable, measurable as "
            "behaviour, and changeable by design. <bookmark mark='c'/> The psychology of individuals explains how "
            "bias starts. Measuring and changing it often happens at the level of decisions, rules and norms."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
